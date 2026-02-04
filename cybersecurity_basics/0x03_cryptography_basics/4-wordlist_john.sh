#!/bin/bash
john --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt "$1"
john --format=Raw-MD5 --show "$1" | cut -d: -f2 | grep -v "password hashes cracked" | grep . > 4-password.txt

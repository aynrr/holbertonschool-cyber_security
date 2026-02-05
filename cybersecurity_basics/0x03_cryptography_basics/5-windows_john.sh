#!/bin/bash
john --wordlist=/usr/share/wordlists/rockyou.txt --format=nt "$1" && john --format=nt --show "$1" | awk -F: '{print $2}' | grep -v '^$'  > 5-password.txt

#!/bin/bash
hashcat -m 0 -a 0 "$1" /usr/share/wordlists/rockyou.txt --outfile-format 2 --outfile 7-password.txt

#!/bin/bash
nmap -p 443 --script -ssl-enum-ciphres "$1"

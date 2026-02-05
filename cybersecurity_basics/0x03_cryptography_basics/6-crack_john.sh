#!/bin/bash
john "$1" --format=Raw-SHA256 && john --show "$1" --format=Raw-SHA256 | awk -F: '{print $2}' | grep -v '^$' > 6-password.txt

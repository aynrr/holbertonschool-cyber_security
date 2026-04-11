#!/bin/bash
log_file = ${1:-logs.txt}
attacker_ip = $(awk '{print $1}' "log_file" | sort | uniq -c | uniq -nr | head -n 1| awk '{print $2}')
awk -v ip="$attacker_ip" '$1 == ip {count++} END {print count}' "$log_file"

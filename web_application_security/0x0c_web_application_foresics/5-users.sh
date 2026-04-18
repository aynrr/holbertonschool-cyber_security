#!/bin/bash
grep 'new user' auth.log | awk -F 'name=' '{print $2}' | awk '{print $1'} | sort -u | tr -d ',' | paste -sd ',' -

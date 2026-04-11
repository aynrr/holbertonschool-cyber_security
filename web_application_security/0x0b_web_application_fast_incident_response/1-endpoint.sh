#!/bin/bash
awk '{print $7}' logs.txt | sort | uniq -c | uniq -nr| head -n 1 | awk '{print $2}'

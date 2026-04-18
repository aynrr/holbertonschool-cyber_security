#!/bin/bash
grep 'Invalid user access' auth.log* | awk '{print $10}' | sort | uniq -c| awk '{print $1}'

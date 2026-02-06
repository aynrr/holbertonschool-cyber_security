#!/bin/bash
find "$1" -type file -perm -2000 -exec ls {} \;

#!bin/bash
find "$1" -type file -user user2 -exec chown user3 {}\;

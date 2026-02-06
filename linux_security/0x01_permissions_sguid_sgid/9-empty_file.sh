#!/bin/bash
find "$1" -type file -empty -exec chmod 777 {} \;

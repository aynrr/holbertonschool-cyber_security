#!/bin/bash
find "$1" -type file -exec chmod 0=r {} \;

#!/bin/bash
sudo iptables -t FILTER -A INPUT -p tcp 80 -j ACCEPT

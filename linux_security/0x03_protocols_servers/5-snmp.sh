#!/bin/bash
grep -v "^#" /etc/nmp/snmpd.conf | grep "public"

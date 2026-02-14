#!/bin/bash
grep -ev "^#|^$" /etc/ssh/sshd_config

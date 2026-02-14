#!/bin/bash
grep "^smtpd_tls_level_security" || echo "STARTTLS not configured"

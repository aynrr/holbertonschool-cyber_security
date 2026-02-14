#!/bin/bash
grep "^smtpd_tls_security_level" || echo "STARTTLS not configured"

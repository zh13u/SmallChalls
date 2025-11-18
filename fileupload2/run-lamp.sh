#!/bin/bash

# Enable Apache site and modules
a2ensite 000-default.conf
a2enmod rewrite

# Suppress ServerName warning (use dynamic hostname for flexible deployment)
HOSTNAME=$(hostname -f 2>/dev/null || hostname || echo "localhost")
echo "ServerName $HOSTNAME" >> /etc/apache2/apache2.conf

# Start Apache in foreground
apache2ctl -DFOREGROUND
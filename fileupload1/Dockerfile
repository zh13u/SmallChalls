# syntax=docker/dockerfile:1
FROM php:8.2-apache

# Enable recommended Apache settings
RUN a2enmod rewrite

WORKDIR /var/www/html

# Copy app
COPY . /var/www/html/

# Add our apache conf and enable it
COPY apache-ctf.conf /etc/apache2/conf-available/ctf.conf
RUN a2enconf ctf

# ensure uploads dir exists and owned by www-data
RUN mkdir -p /var/www/html/uploads \
    && chown -R www-data:www-data /var/www/html \
    && find /var/www/html -type d -exec chmod 755 {} \; \
    && find /var/www/html/uploads -type d -exec chmod 775 {} \; \
    && find /var/www/html/uploads -type f -exec chmod 664 {} \;

EXPOSE 80

# restart apache in foreground (default php:apache uses apache2-foreground)
CMD ["apache2-foreground"]

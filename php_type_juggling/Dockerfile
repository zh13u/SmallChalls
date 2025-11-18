FROM php:8.2-apache
COPY index.php /var/www/html/index.php
RUN a2enmod rewrite headers && chown -R www-data:www-data /var/www/html
EXPOSE 80

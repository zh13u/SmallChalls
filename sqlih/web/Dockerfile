FROM php:8.2-apache

# enable mysqli extension
RUN docker-php-ext-install mysqli

# copy web files
COPY . /var/www/html/

# set permissions
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80

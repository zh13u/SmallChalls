FROM ubuntu:14.04

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y zip unzip tzdata curl
RUN apt-get install -y php5
RUN apt-get install -y apache2 libapache2-mod-php5

COPY index.html /var/www/html/
COPY upload.php /var/www/html/

COPY flag.txt /var/www/flag.txt
RUN chmod 644 /var/www/flag.txt
COPY apache_default.conf /etc/apache2/sites-available/000-default.conf

COPY run-lamp.sh /usr/sbin/run-lamp.sh
RUN chmod +x /usr/sbin/run-lamp.sh

RUN mkdir -p /var/www/html/upload \
 && chown -R www-data:www-data /var/www/html/upload \
 && chmod -R 0775 /var/www/html/upload

EXPOSE 80
CMD ["/usr/sbin/run-lamp.sh"]

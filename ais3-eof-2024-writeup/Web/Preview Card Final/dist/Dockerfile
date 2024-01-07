FROM php:apache


######## PHPMyAdmin ########

# Set environment variables for PHPMyAdmin
ENV PHPMYADMIN_VERSION=5.2.1
ENV PHPMYADMIN_DIR=/var/www/phpmyadmin

RUN docker-php-ext-install mysqli pdo pdo_mysql

# Install dependencies and PHP extensions required by PHPMyAdmin
RUN apt-get update && \
    apt-get install -y \
        wget \
        unzip \
        libzip-dev && \
    docker-php-ext-install zip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install PHPMyAdmin
RUN mkdir -p ${PHPMYADMIN_DIR} && \
    wget https://files.phpmyadmin.net/phpMyAdmin/${PHPMYADMIN_VERSION}/phpMyAdmin-${PHPMYADMIN_VERSION}-all-languages.zip && \
    unzip phpMyAdmin-${PHPMYADMIN_VERSION}-all-languages.zip -d ${PHPMYADMIN_DIR} && \
    rm phpMyAdmin-${PHPMYADMIN_VERSION}-all-languages.zip && \
    mv ${PHPMYADMIN_DIR}/phpMyAdmin-${PHPMYADMIN_VERSION}-all-languages/* ${PHPMYADMIN_DIR} && \
    rm -r ${PHPMYADMIN_DIR}/phpMyAdmin-${PHPMYADMIN_VERSION}-all-languages



COPY config.inc.php ${PHPMYADMIN_DIR}/config.inc.php

# Configure Apache to serve PHPMyAdmin
COPY phpmyadmin.conf /etc/apache2/phpmyadmin.conf
RUN echo "Include /etc/apache2/phpmyadmin.conf" >> /etc/apache2/apache2.conf


######## Webapp ########

COPY app/ /var/www/app/
ENV APACHE_DOCUMENT_ROOT /var/www/app/public

RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
RUN a2enmod rewrite

WORKDIR /var/www/app
RUN chown -R www-data:www-data storage bootstrap/cache

RUN sed -i 's/APP_DEBUG=true/APP_DEBUG=false/g' .env
RUN sed -i 's/APP_ENV=local/APP_ENV=production/g' .env

RUN php artisan key:generate

ARG FLAG

RUN echo $FLAG > /flag
# unset FLAG environment variable
ENV FLAG ""

RUN chmod 0400 /flag
COPY readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod 4755 /readflag

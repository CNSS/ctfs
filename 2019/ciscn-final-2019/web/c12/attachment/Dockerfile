FROM linode/lamp
WORKDIR /var/www
RUN mkdir /var/www/ciscn
RUN mkdir /var/www/ciscn/www
COPY ./www /var/www/ciscn/www
COPY ./ciscn.conf /etc/apache2/sites-enabled
COPY ./data.sql /tmp
RUN mv /etc/apache2/sites-enabled/example.com.conf /etc/apache2/sites-enabled/example.com.conf.bak
COPY ./start.sh /tmp/start.sh
RUN rm -f /etc/php5/apache2/php.ini
COPY ./php.ini /etc/php5/apache2
RUN groupadd ciscn && \
	useradd -g ciscn ciscn -m && \
	password=$(openssl passwd -1 -salt 'abcdefg' 'xxxxffff') && \
	sed -i 's/^ciscn:!/ciscn:'$password'/g' /etc/shadow
RUN sed -i 's/www-data/ciscn/g' /etc/apache2/envvars
WORKDIR /var/www/ciscn
RUN chown -R ciscn:ciscn . && \
	chmod -R 750 .
RUN chmod 777 -R /var/www/ciscn/www/logs
RUN chmod +x /tmp/start.sh
RUN apt-get update
RUN apt-get -y install openssh-server
RUN apt-get -y install php5-mysql
RUN apt-get -y install php5-mysqlnd
EXPOSE 80
CMD /tmp/start.sh
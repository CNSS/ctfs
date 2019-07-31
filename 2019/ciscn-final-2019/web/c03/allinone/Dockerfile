FROM phusion/baseimage

ENV SPRING_PROFILES_ACTIVE prod

ADD ./files /tmp/files

RUN cp -rf /tmp/files/sources.list /etc/apt/ && \
		apt update && \
		apt install nginx default-jdk zip unzip -y && \
		cp -rf /tmp/files/default /etc/nginx/sites-enabled/ && \
 		cp -rf /tmp/files/nginx.conf /etc/nginx/ && \
		rm -rf /var/www/html/* && \
		cp -rf /tmp/files/html/* /var/www/html/ && \
		cp -rf /tmp/files/reg_center-0.0.1-SNAPSHOT.jar /usr/bin && \
		cp -rf /tmp/files/frontend_consumer-0.0.1-SNAPSHOT.jar /usr/bin && \
		cp -rf /tmp/files/flag_provider-0.0.1-SNAPSHOT.jar /usr/bin && \
 		cp -rf /tmp/files/storage_provider-0.0.1-SNAPSHOT.jar /usr/bin && \
 		cp -rf /tmp/files/start.sh /etc/my_init.d/start.sh && \
 		chmod u+x /etc/my_init.d/start.sh && \
		groupadd java1 && \
		useradd -g java1 java1 -m && \
		groupadd java2 && \
		useradd -g java2 java2 -m && \
		groupadd java3 && \
		useradd -g java3 java3 -m && \
		groupadd java4 && \
		useradd -g java4 java4 -m && \
		chmod -R 755 /usr/bin/reg_center-0.0.1-SNAPSHOT.jar && \
		chmod -R 755 /usr/bin/frontend_consumer-0.0.1-SNAPSHOT.jar && \
		chmod -R 755 /usr/bin/flag_provider-0.0.1-SNAPSHOT.jar && \
		chmod -R 755 /usr/bin/storage_provider-0.0.1-SNAPSHOT.jar && \
		mkdir /tmp/uploads/ && \
		mkdir /tmp/tmp_uploads/ && \
 		cp -rf /tmp/files/25cb83a6-ca1a-4e83-95da-2d3d8dc8abf8.zip /tmp/uploads/ && \
		echo 'flag{flag_test}' > /flag && \
		rm -rf /tmp/files

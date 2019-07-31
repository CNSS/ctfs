#!/bin/bash

service nginx start

chown java2:java2 /flag
chmod 700 /flag

chown java3:java3 /tmp/uploads/
chown java3:java3 /tmp/tmp_uploads/

su - java1 -c "nohup java -Xms64m -Xmx512m -Xss1024K -Dspring.profiles.active=prod -jar /usr/bin/reg_center-0.0.1-SNAPSHOT.jar &"
su - java2 -c "nohup java -Xms64m -Xmx512m -Xss1024K -Dspring.profiles.active=prod -jar /usr/bin/flag_provider-0.0.1-SNAPSHOT.jar &"
su - java3 -c "nohup java -Xms64m -Xmx512m -Xss1024K -Dspring.profiles.active=prod -jar /usr/bin/storage_provider-0.0.1-SNAPSHOT.jar &"
su - java4 -c "nohup java -Xms64m -Xmx512m -Xss1024K -Dspring.profiles.active=prod -Dfile.sign_key=`openssl rand -hex 16` -jar /usr/bin/frontend_consumer-0.0.1-SNAPSHOT.jar &"

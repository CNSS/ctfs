#!/bin/sh
export TERM=dumb
a2enmod rewrite
sudo service ssh start
sudo service mysql start
sudo service apache2 start
mysqladmin -h 127.0.0.1 -u root -pAdmin2015 password "xxx123abc"
mysql -h 127.0.0.1 -u root -pxxx123abc --default-character-set=UTF8 < /tmp/data.sql
echo flag{flag_test} > /flag
chmod 777 /flag
tail -f /dev/null

#!/bin/bash
set -e

service nginx restart
/etc/init.d/php7.2-fpm start

touch ./1
tail -f ./1

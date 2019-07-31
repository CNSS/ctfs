FROM ubuntu:18.04

RUN echo "ZGViIGh0dHA6Ly9taXJyb3JzLmFsaXl1bi5jb20vdWJ1bnR1LyBiaW9uaWMgbWFpbiByZXN0cmljdGVkIHVuaXZlcnNlIG11bHRpdmVyc2UKCmRlYi1zcmMgaHR0cDovL21pcnJvcnMuYWxpeXVuLmNvbS91YnVudHUvIGJpb25pYyBtYWluIHJlc3RyaWN0ZWQgdW5pdmVyc2UgbXVsdGl2ZXJzZQoKZGViIGh0dHA6Ly9taXJyb3JzLmFsaXl1bi5jb20vdWJ1bnR1LyBiaW9uaWMtc2VjdXJpdHkgbWFpbiByZXN0cmljdGVkIHVuaXZlcnNlIG11bHRpdmVyc2UKCmRlYi1zcmMgaHR0cDovL21pcnJvcnMuYWxpeXVuLmNvbS91YnVudHUvIGJpb25pYy1zZWN1cml0eSBtYWluIHJlc3RyaWN0ZWQgdW5pdmVyc2UgbXVsdGl2ZXJzZQoKZGViIGh0dHA6Ly9taXJyb3JzLmFsaXl1bi5jb20vdWJ1bnR1LyBiaW9uaWMtdXBkYXRlcyBtYWluIHJlc3RyaWN0ZWQgdW5pdmVyc2UgbXVsdGl2ZXJzZQoKZGViLXNyYyBodHRwOi8vbWlycm9ycy5hbGl5dW4uY29tL3VidW50dS8gYmlvbmljLXVwZGF0ZXMgbWFpbiByZXN0cmljdGVkIHVuaXZlcnNlIG11bHRpdmVyc2UKCmRlYiBodHRwOi8vbWlycm9ycy5hbGl5dW4uY29tL3VidW50dS8gYmlvbmljLWJhY2twb3J0cyBtYWluIHJlc3RyaWN0ZWQgdW5pdmVyc2UgbXVsdGl2ZXJzZQoKZGViLXNyYyBodHRwOi8vbWlycm9ycy5hbGl5dW4uY29tL3VidW50dS8gYmlvbmljLWJhY2twb3J0cyBtYWluIHJlc3RyaWN0ZWQgdW5pdmVyc2UgbXVsdGl2ZXJzZQoKZGViIGh0dHA6Ly9taXJyb3JzLmFsaXl1bi5jb20vdWJ1bnR1LyBiaW9uaWMtcHJvcG9zZWQgbWFpbiByZXN0cmljdGVkIHVuaXZlcnNlIG11bHRpdmVyc2UKCmRlYi1zcmMgaHR0cDovL21pcnJvcnMuYWxpeXVuLmNvbS91YnVudHUvIGJpb25pYy1wcm9wb3NlZCBtYWluIHJlc3RyaWN0ZWQgdW5pdmVyc2UgbXVsdGl2ZXJzZQo=" | base64 -d > /etc/apt/sources.list

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get purge -y libcurl3-gnutls 
RUN apt-get install -y apt-utils && apt-get install -y nginx curl wget vim

RUN apt-get install -y php7.2-fpm php7.2-mysql php7.2-common php7.2-mbstring php7.2-gd php7.2-json php7.2-cli unzip composer

COPY ./default /etc/nginx/sites-available/default
ADD ./source.tar.gz /var/www/html/
COPY ./start.sh /root/start.sh
RUN chmod a+x /root/start.sh

RUN echo 'flag{flag_test}' > /flag
RUN chown -R www-data:www-data /var/www/html \
    && ln -s /var/www/html /html
RUN rm /var/www/html/index.nginx-debian.html

ENTRYPOINT cd /root; ./start.sh

EXPOSE 80

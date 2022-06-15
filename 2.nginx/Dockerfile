FROM ubuntu:20.04

MAINTAINER shpark <emailaddress> 

RUN apt-get update && \
    apt-get install nginx -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    # echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
    echo "<h1>Hello JK</h1>" > /var/www/html/index.html

# Clean up APT when done.
# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#ENTRYPOINT ["nginx"]
# CMD ["nginx"]
CMD ["nginx", "-g", "daemon off;"]

#docker-compose가 참고하는 용이라 없어도 되긴 함
EXPOSE 80

#! /bin/bash
sudo docker run -d -p 80:80 \
 --name nginx -v /tmp/nginx:/etc/nginx/conf.d \
 -v $(pwd)/gdmap/static:/data/static \
 -t nginx
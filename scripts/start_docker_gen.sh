#! /bin/bash
sudo docker run -d --volumes-from nginx \
 --name docker-gen \
 -v /var/run/docker.sock:/tmp/docker.sock \
 -v $(pwd)/docker/nginx:/etc/docker-gen/templates \
 -t jwilder/docker-gen -notify-sighup nginx -watch -only-published \
 /etc/docker-gen/templates/nginx.tmpl \
 /etc/nginx/conf.d/default.conf
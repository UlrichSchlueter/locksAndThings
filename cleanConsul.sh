#!/bin/bash

volume_id=$(docker inspect consul-server | jq '.[] | .Mounts' | jq '.[] | .Name' | tr -d '"') 

echo $volume_id

docker volume inspect $volume_id

docker stop -t 5 consul-server 

docker rm consul-server 

docker volume rm $volume_id

ansible-playbook prepDocker.yml
#!/bin/bash

sudo docker cp $(sudo docker ps | grep physical_process | awk '{print $1}'):/workdir/$(sudo docker exec -it $(sudo docker ps | grep physical_process | awk '{print $1}') ls /workdir | grep update_log.tsv | awk '{print $1}') ./

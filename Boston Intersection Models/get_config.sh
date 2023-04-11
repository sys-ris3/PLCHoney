#!/bin/bash

sudo docker cp $(sudo docker ps | grep physical_process | awk '{print $1}'):/workdir/reflectors.json ./physical_process/

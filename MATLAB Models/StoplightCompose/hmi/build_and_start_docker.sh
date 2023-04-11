#!/bin/bash

docker build -t scadabr .
docker run -it --rm --privileged -p 8084:9090 scadabr


#!/bin/bash

docker build -t openplc:v3 .
docker run -it -d --rm --privileged -p 8080:8080 openplc:v3

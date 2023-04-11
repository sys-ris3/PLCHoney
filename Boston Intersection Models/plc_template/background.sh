#!/bin/bash
nohup ./start_openplc.sh &

# openplc has a script that must be run from the webserver directory
cd webserver
./scripts/change_hardware_layer.sh simulink_linux
cd ..

while :
do
    sleep 1
done

#!/bin/bash
nohup ./start_openplc.sh &
./webserver/scripts/change_hardware_layer.sh simulink
./simlink

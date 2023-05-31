# Proxy for HoneyPLC
This python server runs as a proxy for PLC node and handles the different response requests.

## Features
* Spoofing the identity of a Modbus device (through device enumeration)
* Modifying Modbus data (e.g. reading and writing coils and registers) acting as an intermediary between the **OpenPLC** and **PLCScan**

## Usage
To run the Honeypot proxy:
```
sudo python mod_honeypot_proxy.py
```

This will bring up the common 5 PLC profiles that we discovered. Choosing a number from `1` to `5` will set the respective PLC profile as the active one.

### Using PLCScan with the Proxy 

To test the device enumeration
```
sudo python plcscan.py 0.0.0.0:504
```

### Sample output
![device enumeration]/figures/device_enumeration.svg

To test reading a coil
```
sudo python plcscan.py --modbus-function=1 --modbus-data='\x00\x00\x00\x01' --hosts-list="hosts.txt" --timeout=20 
```

To test writing to a coil
```
sudo python plcscan.py --modbus-function=5 --modbus-data='\x00\x64\xFF\x00' --hosts-list="hosts.txt" --timeout=20
```

where file hosts.txt looks like:
```
0.0.0.0:504
192.168.1.107:102
example.host:504
```

# PLCHoney

## Overview
With the emergence of virtual PLCs, we introduce the honeypot PLCHoney, to overcome the existing challenges in a cost-effective approach. We designed and implemented PLCHoney with a proxy profiler, dockerized virtual PLCs, a physical process simulator, and a security analysis engine. PLCHoney was able to correctly simulate responses to various internet requests and tested effectively on a network of virtualized traffic light applications. We enabled further security analysis with a dataset containing PLC I/O status, collected with and without attacks. 

![PLCHoney_arch](/figures/arch-1.png)

## Requirements
* Docker
* Python 2.7+
* Flask

## Installation
```
git clone https://github.com/thiagoralves/OpenPLC_v3.git
cd OpenPLC_v3
./install.sh docker
```

## Running the program
```
cd Boston\ Intersection\ Models/
sudo ./start_stoplights.py
```

## Citing our paper
```
@inproceedings {
author = {Samin Y. Chowdhury and Brandon Dudley and Ruimin Sun},
title = {The Case for Virtual PLC-enabled Honeypot Design},
booktitle = {Re-design Industrial Control Systems with Security (RICSS) (co-located with 8th IEEE EuroS&P)}
year = {2023},
url = {},
publisher = {{IEEE}},
month = July,
}
```

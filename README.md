# PLCHoney

## Overview
Programmable logic controllers (PLCs) are essential components of Industrial Control System (ICS) in acting as a practical link between the cyber and physical worlds. In recent years, we have seen an increase in attacks targeting PLCs. Honeypot for PLCs, as an effective technique to gather attacker information and attack tactics, is limited in vendor-specific implementation, configuration, extensibility, and scalability. With the emergence of virtual PLCs, this paper introduces a honeypot, named PLCHoney, to overcome the existing challenges in a cost-effective approach. We designed and implemented PLCHoney with a proxy profiler, dockerized virtual PLCs, a physical process simulator, and a security analysis engine. PLCHoney was able to correctly simulate responses to various internet requests and tested effectively on a network of virtualized traffic light applications. We enabled further security analysis with a dataset containing PLC I/O status, collected with and without attacks. We envision that PLCHoney paves the avenue for the future development of PLC-based honeypots.

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

#!/usr/bin/env python3

import requests, json, time

LOG_TIME = time.time()

def log(message):
    file = open(str(LOG_TIME)+"_error_log.txt", 'w')
    file.write(time.ctime()+"\t")
    file.write(message+"\n")

# parse container_port_reference.txt
file = open("container_port_reference.txt", 'r')
lines = file.readlines()
file.close()

containers = {}
i = ""
for line in lines:
    if "_" in line and line.strip().replace(":", "") not in containers:
        i = line.strip().replace(":", "")
        containers[i] = {}
    if "Docker internal IP" in line:
        containers[i]["ip"] = line.split(" ")[-6].split("/")[0]
    if "management" in line:
        containers[i]["management_port"] = line.split(" ")[-1].strip()

# check the number of bad states detected
def bad_states():
    states = json.loads(requests.get('http://localhost:8000/bad_states').text)
    if len(states) > 0:
        log(states)
        return True
    return False

# make sure all PLCs are still up
def plc_is_down(port):
    status = json.loads(requests.get('http://localhost:'+str(port)+"/plc_status_noauth").text)
    if status["status"] == "Running":
        return False
    print("PLC on port "+str(port)+" is down.")
    return True

if bad_states():
    print("Bad/unsafe states detected.")
    exit()

# check each container
for c in containers:
    if plc_is_down(containers[c]["management_port"]):
        print(c+" is down.")
        log(c+" is down.")
        exit()

print("1")

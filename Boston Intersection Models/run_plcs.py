import os, requests, time

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


for container in containers:
    print(""+container)
    # check the status
    status = requests.get('http://localhost:'+containers[container]['management_port']+"/plc_status_noauth")
    print(status.text)
    compile = requests.get('http://localhost:'+containers[container]['management_port']+"/compile_program_noauth")
    print(compile.text)

    status = requests.get('http://localhost:'+containers[container]['management_port']+"/plc_status_noauth")
    print(status.text)
    time.sleep(5)
    start = requests.get('http://localhost:'+containers[container]['management_port']+"/start_plc_noauth")
    print(start.text)

#!/usr/bin/env python3
import os

containers = []

build = "docker build -t openplc:v3 station"

# start station 0
run0 = "docker run -it -d --rm --privileged -p 8080:8080 openplc:v3"
os.system(build+'0')
containers.append(os.popen(run0).read())

# start station 1
run1 = "docker run -it -d --rm --privileged -p 8082:8080 -p 26001:26001/udp -p 26002:26002/udp -p 26003:26003/udp openplc:v3"
os.system(build+'1')
containers.append(os.popen(run1).read())

# start station 2
run2 = "docker run -it -d --rm --privileged -p 8081:8080 -p 26004:26004/udp -p 26005:26005/udp -p 26006:26006/udp openplc:v3"
os.system(build+'2')
containers.append(os.popen(run2).read())

# start station 3
run3 = "docker run -it -d --rm --privileged -p 8083:8080 -p 26007:26007/udp -p 26008:26008/udp -p 26009:26009/udp openplc:v3"
os.system(build+'3')
containers.append(os.popen(run3).read())

file = open("stop_stoplights.sh", 'w')
for container in containers:
	file.write("docker stop "+container)
file.close()

os.system("chmod +x stop_stoplights.sh")

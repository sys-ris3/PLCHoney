#!/usr/bin/env python3

config_files = ["station0/", "station1/", "station2/", "station3/"]

ip = input("Enter the IP address where the Simulink Model will be running >>>")

print(ip)

for config in config_files:
	file = open(config+"interface.cfg", 'r')
	lines = file.readlines()
	file.close()

	new_file = open(config+"interface.cfg", 'w')
	for line in lines:
		if "simulink.ip" in line:
			new_file.write('simulink.ip = "'+ip+'"'+"\n")
		else:
			new_file.write(line)
	new_file.close()

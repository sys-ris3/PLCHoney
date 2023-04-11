#!/usr/bin/env python3
import os, time, json

# the order of these directories is important for the port mappings, don't
# change them unless you update the state dictionary in the physical process
# visualization script to match
plcs = ['parker_huntington', 'ruggles_huntington', 'forsyth_huntington', 'field_master']

#################################################################
# first, generate an appropriate interface.cfg for the ST program
# this parser includes comments in the interface.cfg to indicate
# which port maps to which variable/coil
#################################################################
# get the interface.cfg template
fstream = open("interface_template.cfg", 'r')
interface_template = fstream.read()
fstream.close()

# this is the state that will be used in the physical process simulation, it will
# keep track of variables and programs while associating them with a port
state = {}
inputs = {}

simlink_port = 26000
digital_out = "station0.add(digital_out) = "
digital_in = "station0.add(digital_in) = "
analog_in = "station0.add(analog_in) = "
analog_out = "station0.add(analog_out) = "
for directory in plcs:
    # identify the ST files, it uses the first ST file found, so
    # so make sure there is only one ST file in the directory
    st_candidates = os.listdir(directory)
    st_file = ""
    for f in st_candidates:
        if ".st" in f.lower():
            st_file = f
            break
    st_path = os.path.join(directory, st_file)

    # find the variables that have coils mapped, write them to
    # config file with some descriptive comments
    fstream = open(st_path, 'r')
    st_lines = fstream.readlines()
    fstream.close()

    # set a few config options
    current_config = interface_template
    #current_config = current_config.replace("SIMULINK_IP", simulink_ip)
    current_config = current_config.replace("ST_PROGRAM", st_file)

    config_lines = []
    for line in st_lines:
        if "%QX" in line:
            config_lines.append('''# Generated from '''+st_file+" on line "+str(st_lines.index(line)))
            config_lines.append('''# '''+line.strip())
            config_lines.append(digital_out+"\""+str(simlink_port)+"\"\n")
            state[simlink_port] = []
            state[simlink_port].append(False)
            state[simlink_port].append(line.strip()+" "+directory)
            simlink_port += 1
        if "%QW" in line:
            config_lines.append('''# Generated from '''+st_file+" on line "+str(st_lines.index(line)))
            config_lines.append('''# '''+line.strip())
            config_lines.append(analog_out+"\""+str(simlink_port)+"\"\n")
            state[simlink_port] = []
            state[simlink_port].append(False)
            state[simlink_port].append(line.strip()+" "+directory)
            simlink_port += 1
        if "%IX" in line:
            config_lines.append('''# Generated from '''+st_file+" on line "+str(st_lines.index(line)))
            config_lines.append('''# '''+line.strip())
            config_lines.append(digital_in+"\""+str(simlink_port)+"\"\n")
            state[simlink_port] = []
            state[simlink_port].append(False)
            state[simlink_port].append(line.strip()+" "+directory)
            simlink_port += 1
        if "%IW" in line:
            config_lines.append('''# Generated from '''+st_file+" on line "+str(st_lines.index(line)))
            config_lines.append('''# '''+line.strip())
            config_lines.append(analog_in+"\""+str(simlink_port)+"\"\n")
            state[simlink_port] = []
            state[simlink_port].append(False)
            state[simlink_port].append(line.strip()+" "+directory)
            simlink_port += 1

    current_config = current_config.replace("PORT_MAPPINGS", "\n".join(config_lines))

    # write the config in the appropriate directory
    fstream = open(os.path.join(directory, "interface.cfg"), 'w')
    fstream.write(current_config)
    fstream.close()

# save the state in the physical process directory
state_file = os.path.join("physical_process", "state.json")
with open(state_file, 'w') as fp:
    json.dump(state, fp)


#################################################################
# start the physical process docker container, get the necessary
# info from the container once it is running
#################################################################
os.system("docker build -t physical_process physical_process")
container = os.popen("docker run -it -d --name physical_process --rm --privileged -p 8000:8000 physical_process").read()
ifconfig = os.popen("docker exec -it "+container.strip()+" ip addr").read()

# parse out the internal docker ip
simulink_ip = ''
for i in ifconfig.split("\n"):
    if "global" in i:
        for token in i.split():
            if "/16" in token:
                simulink_ip = token.split("/")[0]
                break
if len(simulink_ip) < 7:
    print("Problem getting Docker internal net IP from physical process container, check it, and start again.")
    exit()

# replace the SIMULINK_IP with what we just generated
for directory in plcs:
    fstream = open(os.path.join(directory, "interface.cfg"), 'r')
    template = fstream.read()
    fstream.close()

    updated_config = template.replace("SIMULINK_IP", simulink_ip)

    fstream = open(os.path.join(directory, "interface.cfg"), 'w')
    fstream.write(updated_config)
    fstream.close()

#################################################################
# Build the containers that communicate with the already-running
# instance of the physical process script.
#################################################################

containers = []

build = "docker build -t openplc:v3 "

file = open("container_port_reference.txt", 'w')
port = 8080
fuzz_port = 5000
for plc in plcs:
    run = "docker run -it -d --name "+plc+" --rm --privileged -p "+str(port)+":8080 -p "+str(fuzz_port)+":502 openplc:v3"

    # make sure the OpenPLC files are in the correct directory
    os.system("cp -r ./plc_template "+plc+"/plc_template")

    os.system(build+' '+plc)

    # make sure the container actually starts
    id = os.popen(run).read()
    print("Started "+id.strip())
    time.sleep(3)
    while int(os.popen("docker ps | grep "+plc+" | wc -l").read().strip()) < 1:
        # this means the container failed to build, try again
        print("Container failed to build, retrying...")
        id = os.popen(run).read()
        time.sleep(3)

    containers.append(id)
    internal_ip = os.popen("docker exec -it "+containers[-1].strip()+" ip addr | grep global").read()

    # write to the reference file
    file.write(plc+":\n\t-Web management port: "+str(port)+"\n\t-Modbus port (for fuzzing): "+str(fuzz_port)+"\n\t-Container ID: "+containers[-1].strip()+"\n\t-Docker internal IP: "+internal_ip+"\n\n")

    port += 1
    fuzz_port += 1

    # cleanup the OpenPLC files
    os.system("rm -rf "+plc+"/plc_template")
file.close()

# copy the reference to the physical process container
os.system("docker cp container_port_reference.txt "+container.strip()+":/workdir/")

file = open("stop_stoplights.sh", 'w')
file.write("./get_logs.sh\n")
file.write("docker stop "+container)
for container in containers:
	file.write("docker stop "+container)
file.write("rm stop_stoplights.sh")
file.close()

os.system("chmod +x stop_stoplights.sh")

print("Compiling ST programs and starting PLCs...")

os.system("python3 run_plcs.py")

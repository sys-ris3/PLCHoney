import socket, time, json

#######################################################################################
# This part of the script reads in the state.json file and parses the container port
# reference that is automatically generated when the containers start.
#######################################################################################
ANALOG_BUF_SIZE = 128
DIGITAL_BUF_SIZE = 128

# recreating the below struct
#struct plcData
#{
#        uint16_t analogIn[ANALOG_BUF_SIZE];
#        uint16_t analogOut[ANALOG_BUF_SIZE];
#        bool digitalIn[DIGITAL_BUF_SIZE];
#        bool digitalOut[DIGITAL_BUF_SIZE];
#};

def get_clean_state():
    plcData = {'analogIn': [], 'analogOut': [], 'digitalIn': [], 'digitalOut': []}

    for x in range(0, ANALOG_BUF_SIZE):
        plcData['analogIn'].append({'value': b'\x00\x00'})
    for x in range(0, ANALOG_BUF_SIZE):
        plcData['analogOut'].append({'value': b'\x00\x00'})
    for x in range(0, DIGITAL_BUF_SIZE):
        plcData['digitalIn'].append({'value': b'\x00'})
    for x in range(0, DIGITAL_BUF_SIZE):
        plcData['digitalOut'].append({'value': b'\x00'})

    return plcData


def initialize_state():
    file = open("container_port_reference.txt", 'r')
    data = file.readlines()
    file.close()

    file = open("state.json", 'r')
    parsed_state = json.loads(file.read())
    file.close()

    # parse the internal IPs from the docker container reference file
    containers = {}
    i = ""
    for line in data:
        if "_" in line and line.strip().replace(":", "") not in containers:
            i = line.strip().replace(":", "")
            containers[i] = {}
        if "Docker internal IP" in line:
            containers[i]['ip'] = line.split(" ")[-6].split("/")[0]
            containers[i]['state'] = get_clean_state()

    # enrich the container dict for descriptive information
    # '26135': [False, 'manual_offset_ruggles AT %IW4: INT := 0; field_master']
    for key in parsed_state:
        c = parsed_state[key][-1].split(' ')[-1]
        if c in parsed_state[key][-1]:
            if "%QX" in parsed_state[key][-1]:
                qx_index = 0
                while 'raw' in containers[c]['state']['digitalOut'][qx_index]:
                    qx_index += 1
                containers[c]['state']['digitalOut'][qx_index]['varName'] = parsed_state[key][-1].split(" ")[0]
                containers[c]['state']['digitalOut'][qx_index]['type'] = parsed_state[key][-1].replace(":", " ").split()[3].replace(";", "")
                containers[c]['state']['digitalOut'][qx_index]['raw'] = parsed_state[key][-1]
                qx_index += 1
            if "%QW" in parsed_state[key][-1]:
                qw_index = 0
                while 'raw' in containers[c]['state']['analogOut'][qw_index]:
                    qw_index += 1
                containers[c]['state']['analogOut'][qw_index]['varName'] = parsed_state[key][-1].split(" ")[0]
                containers[c]['state']['analogOut'][qw_index]['type'] = parsed_state[key][-1].replace(":", " ").split()[3].replace(";", "")
                containers[c]['state']['analogOut'][qw_index]['raw'] = parsed_state[key][-1]
                qw_index += 1
            if "%IX" in parsed_state[key][-1]:
                ix_index = 0
                while 'raw' in containers[c]['state']['digitalIn'][ix_index]:
                    ix_index += 1
                containers[c]['state']['digitalIn'][ix_index]['varName'] = parsed_state[key][-1].split(" ")[0]
                containers[c]['state']['digitalIn'][ix_index]['type'] = parsed_state[key][-1].replace(":", " ").split()[3].replace(";", "")
                containers[c]['state']['digitalIn'][ix_index]['raw'] = parsed_state[key][-1]
                ix_index += 1
            if "%IW" in parsed_state[key][-1]:
                iw_index = 0
                while 'raw' in containers[c]['state']['analogIn'][iw_index]:
                    iw_index += 1
                containers[c]['state']['analogIn'][iw_index]['varName'] = parsed_state[key][-1].split(" ")[0]
                containers[c]['state']['analogIn'][iw_index]['type'] = parsed_state[key][-1].replace(":", " ").split()[3].replace(";", "")
                containers[c]['state']['analogIn'][iw_index]['raw'] = parsed_state[key][-1]
                iw_index += 1

    return containers


def log(ts, container, coil, old, new, index, c_type, LOG_TIME):
    # timestamp    container    variable    old_hex    new_hex    type
    try:
        #print(str(ts)+"\t"+container+"\t"+coil['varName']+"\t"+old.hex()+"\t"+new.hex()+"\t"+coil['type'])
        file = open(str(LOG_TIME)+"_update_log.tsv", 'a')
        file.write(str(ts)+"\t"+container+"\t"+coil['varName']+"\t"+old.hex()+"\t"+new.hex()+"\t"+coil['type']+"\n")
        file.close()
    except:
        #print("Coil never initialized, should this value be updated? - ", container, coil, "at index", index, "in", c_type)
        file = open(str(LOG_TIME)+"_error_log.tsv", 'a')
        file.write("Coil never initialized, should this value be updated? - "+container+" "+str(coil)+" at index "+str(index)+" in "+c_type+"\n")
        file.close()

def update_plcdata(data, containers, container, FILE_LOG_TIME):
    log_time = time.time()
    for x in range(0, ANALOG_BUF_SIZE):
        if containers[container]['state']['analogIn'][x]['value'] != data[:2]:
            old = containers[container]['state']['analogIn'][x]['value']
            containers[container]['state']['analogIn'][x]['value'] = data[:2]
            new = containers[container]['state']['analogIn'][x]['value']
            log(log_time, container, containers[container]['state']['analogIn'][x], old, new, x, 'analogIn', FILE_LOG_TIME)
        data = data[2:]
    for x in range(0, ANALOG_BUF_SIZE):
        if containers[container]['state']['analogOut'][x]['value'] != data[:2]:
            old = containers[container]['state']['analogOut'][x]['value']
            containers[container]['state']['analogOut'][x]['value'] = data[:2]
            new = containers[container]['state']['analogOut'][x]['value']
            log(log_time, container, containers[container]['state']['analogOut'][x], old, new, x, 'analogOut', FILE_LOG_TIME)
        data = data[2:]
    for x in range(0, DIGITAL_BUF_SIZE):
        if containers[container]['state']['digitalIn'][x]['value'] != data[:1]:
            old = containers[container]['state']['digitalIn'][x]['value']
            containers[container]['state']['digitalIn'][x]['value'] = data[:1]
            new = containers[container]['state']['digitalIn'][x]['value']
            log(log_time, container, containers[container]['state']['digitalIn'][x], old, new, x, 'digitalIn', FILE_LOG_TIME)
        data = data[1:]
    for x in range(0, DIGITAL_BUF_SIZE):
        if containers[container]['state']['digitalOut'][x]['value'] != data[:1]:
            old = containers[container]['state']['digitalOut'][x]['value']
            containers[container]['state']['digitalOut'][x]['value'] = data[:1]
            new = containers[container]['state']['digitalOut'][x]['value']
            log(log_time, container, containers[container]['state']['digitalOut'][x], old, new, x, 'digitalOut', FILE_LOG_TIME)
        data = data[1:]

    return containers


def c_to_payload(containers, container):
    payload = b''
    for type_desc in containers[container]['state']:
        for x in range(0, len(containers[container]['state'][type_desc])):
            payload += containers[container]['state'][type_desc][x]['value']
    return payload


def get_coil(source_variable, source_container, containers):
    for c_type in containers[source_container]['state']:
        for index in containers[source_container]['state'][c_type]:
            if 'raw' in index and source_variable == index['varName']:
                return index
    return None


def update_single_state(containers, container, variable, value):
    for c_type in containers[container]['state']:
        for index in containers[container]['state'][c_type]:
            if 'raw' in index and variable == index['varName']:
                index['value'] = value
    return containers

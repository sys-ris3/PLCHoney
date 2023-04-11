## Starting the PLCs
To start all of the PLCs, simply run the Python script:

`sudo ./start_stoplights.py`

This will create a file called `container_port_reference.txt` which contains, by PLC, which ports contain the web interface, and which ports expose the modbus interface for fuzzing.  An example of this file is included in the repository.  It will also create a script called `stop_stoplights.sh`, which will stop all of the docker containers.

To stop all PLC containers:

`sudo ./stop_stoplights.sh`

To easily reference which container corresponds to which intersection, run `sudo docker ps` and check the name in the right hand column:

`
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                                           NAMES

51a72c5dba36        openplc:v3          "./background.sh"   5 seconds ago       Up 4 seconds        0.0.0.0:5002->502/tcp, 0.0.0.0:8082->8080/tcp   forsyth_huntington

0985a3d9f83c        52038fb0398c        "./background.sh"   9 seconds ago       Up 8 seconds        0.0.0.0:5001->502/tcp, 0.0.0.0:8081->8080/tcp   ruggles_huntington

d2c5d659b386        0debb6423ff3        "./background.sh"   13 seconds ago      Up 12 seconds       0.0.0.0:8080->8080/tcp, 0.0.0.0:5000->502/tcp   parker_huntington
`

The hardware layer on OpenPLC is automatically selected, but manual upload of ST programs is still necessary.  Visit localhost on the web interface to select programs.

NOTE: It is recommended that you have more than one core if you are running above 2 instances of OpenPLC containers on a VM.

## Connecting Coils of Different PLCs
After starting all of the containers, visit localhost:8000 (or <your_vm_ip>:8000) to see a listing of all PLC variables at one time.  Find the output coil you want to
use as the input for another coil and click "Reflect Port <port_number>".  On the subsequent page, select which input you want this coil's output to be reflected to.
This will take all UDP packets received on that port and duplicate them to the socket specified in the top table.  You can map a single output to as many inputs as 
you want, and this method does not require any recompiling or restarts.

## Adding New PLCs to the Automated Build Process
To add a new PLC (a new intersection, for example) simply create a directory like `longwood_huntington` and create an ST program with corresponding interface.cfg.  Put these two files, with the standard Dockerfile in the directory and add the directory name to the PLC list in the python script, `start_stoplights.py`.

## Naming Convention for Coils in ST Code
In ST code, the coils are referenced and numbered in the ST code based on the order they are introduced in the Simlink interface.

The following Simlink interface creates three inputs, and one output coil:

```
num_stations = "1"
comm_delay = "100"

# ------------
#   SIMULINK
# ------------
simulink.ip = "192.168.88.254"

# ------------
#  STATION 0
# ------------
station0.ip = "localhost"
station0.add(digital_out) = "25001"
station0.add(digital_out) = "25002"
station0.add(digital_out) = "25003"
station0.add(digital_in) = "26001"
```

In the ST code uploaded to the PLC, they are referenced like this:

```
VAR
  lamp_red AT %QX0.0 : BOOL;
  lamp_yel AT %QX0.1 : BOOL;
  lamp_gre AT %QX0.2 : BOOL;
  lamp_status AT %IX0.0 : BOOL;
END_VAR
```

Inputs are incremented as necessary, maxing out at 8, and carrying over to the number left of the decimal:

%QX0.0, %QX0.1, %QX0.2, %QX0.3, %QX0.4, %QX0.5, %QX0.6, %QX0.7, %QX1.0, %QX1.1, etc.

## Python UDP Server - Simulink Replacement
This script runs a UDP server that listens on the ports specified in the dictionary at the top.  More specific 
structure is outlined in the code, but generally the top level key is the port that is listening with the 
values that are replaced in the ASCII art representation, as well as the current state (a bool).

Running the script is simple:

`python3 stoplight_model.py`

This automatically creates a logfile in the directory where it is run, with tab-separated fields about the
information it receives from Simlink, which is still a required component.  Updated intersection state is
visualized every second, but that can be easily adjusted in the script.

This script is running in its own Docker container, so get the ID of the container:

`sudo docker ps | grep physical_process`

and then check the stdout of that container to see the status of the physical process:

`sudo docker logs -f <container_id>`

## Fuzzing Notes
The PLC modbus port (port 502) is exposed through the docker containers at the port specified in the `container_port_reference.txt`.  This will give direct access to the Modbus port on a specified PLC.

For example, given the following automatically generated configuration file:

```
parker_huntington:
	-Web management port: 8080
	-Modbus port (for fuzzing): 5000
	-Container ID: 4d1c21455572e950d34de78db2a1dd292a89aca1bb612941dae3327a4630731c
	-Docker internal IP:     inet 172.17.0.3/16 brd 172.17.255.255 scope global eth0


ruggles_huntington:
	-Web management port: 8081
	-Modbus port (for fuzzing): 5001
	-Container ID: b0fea264adec41260e6e007bc37d057bfdae12d7fae5e3880b028dfe2c87505e
	-Docker internal IP:     inet 172.17.0.4/16 brd 172.17.255.255 scope global eth0


forsyth_huntington:
	-Web management port: 8082
	-Modbus port (for fuzzing): 5002
	-Container ID: 42882d50f1b55ab1b966a28dcb85e138ea7c5635a5f1f4df78431d205ffb178b
	-Docker internal IP:     inet 172.17.0.5/16 brd 172.17.255.255 scope global eth0
```

you can send Modbus packets to parker_huntington at localhost:5000, ruggles_huntington at localhost:5001, and forsyth_huntington at localhost:5002.  Any additional hosts added via the method described above will automatically expose port 502 and document that port mapping here.

## Getting the Logs from OpenPLC on Docker
Once the physical process is running and logs are being generated, easily access the logs by running the following command:

`./get_logs.sh`

This will copy the TSV logs from the running physical process container.  If the logs are updated, it will copy the most recent version to the host.

# API Documentation
## GET /
Human-friendly reflector management page.  This allows you to dynamically configure reflectors, and save the config.  These requests will go the the physical process host on port 8000.

A reflector receives a UDP packet and resends the payload to a config-specified socket.

## GET /get_state_verbose
Returns JSON with the following structure:

```
[
  {
    "container": "parker_huntington",
    "ip": "172.17.0.3",
    "var_name": "N_G",
    "var_type": "BOOL",
    "coil": "%QX0.0",
    "current_state": false,
    "port": "26000"
  },
  {
    "container": "parker_huntington",
    "ip": "172.17.0.3",
    "var_name": "S_G",
    "var_type": "BOOL",
    "coil": "%QX0.1",
    "current_state": false,
    "port": "26001"
  },
  {
    "container": "parker_huntington",
    "ip": "172.17.0.3",
    "var_name": "EW_Ped_Pressed",
    "var_type": "BOOL",
    "coil": "%IX0.0",
    "current_state": false,
    "port": "26031"
  }
]
```

## GET /bad_states
Returns a JSON structure with the following structure:

```
[
  {
    'ts': 1602100337.0196698,
    'message': 'Unsafe/conflicting green lights.'
  },
  {
    'ts': 1602100337.0196698,
    'message': 'Unsafe/conflicting green/yellow lights.'
  }
]
```

## GET /set_true/\<ip\>/\<port\>
This request is used to provide input to vehicle sensors, pedestrian crossing buttons, or other sources of input.  It sends a BOOL True value to the specified ip and port, which can be found from the /get_state_verbose request above.

**Example:**
GET /set_true/172.17.0.3/26031


# OpenPLC Control REST API
These requests should be sent to individual OpenPLC instances, whose IP addresses can be obtained from the verbose request above.  All requests return a JSON structure like the following:

```
{
  'status': 'Running'
}
```
OR 

```
{
  'status': 'Stopped'
}
```

## GET /start_plc_noauth
This GET request to any of the PLC stations will start a stopped instance of OpenPLC.


## GET /stop_plc_noauth
This GET request to any of the PLC stations will stop a started instance of OpenPLC.


## GET /plc_status_noauth
This GET request will return the current status of an OpenPLC instance.

## GET /check_logs (In Browser)
This gives a quick and useful overview of the logs, the time events occurred, and error states in these events.  Click on the error state link to see the specific error:


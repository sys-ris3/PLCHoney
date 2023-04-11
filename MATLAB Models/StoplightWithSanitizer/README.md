## Deploy Stoplight Model
This is a model that uses 4 docker containers to simulate multiple PLCs controlling stoplights at an intersection.  The steps to deploy are as follow:

1. Identify the IP where the Simulink software will be running the stoplight model, and run the IP address configuration script, following the prompts.
`./config.py`
2. Open the included stoplight .slx file in Simulink and run it.
Be sure to update the IP addresses in the UDP send blocks to the IP address where OpenPLC will be running.  If all of this is happening on the same host, this can be localhost.
3. Run the start script to build and launch the docker containers.
`sudo ./start_stoplights.py`
4. Visit the IP address where the Docker containers are running in a browser on port 8080.  (e.g. for a bridged VM at 192.168.1.15, go to http://192.168.1.15:8080)
5. Log in with the username `openplc` and the password `openplc`.
6. Set hardware layer to Simulink and compile.
7. Upload `master_8080.st` and compile.
8. Start OpenPLC.
9. Visit port 8081 on the same IP, performing steps 5-8 above, but upload `mirror_8081.st` instead.
10. Visit port 8082 on the same IP, performing steps 5-8 above, but upload `parity_8082_8083.st`.
11. Visit port 8083 on the same IP, performing steps 5-8 above, but upload `parity_8082_8083.st`.
12. After all containers start, launch the HMI container

`cd hmi && ./build_and_start_docker.sh`

Take note of the hosts IP, HMI is available at http://<host_ip>:8084/ScadaBR

## Run Fuzzing Interface
1. Get a shell on the HMI container

`sudo docker exec -it <hmi_container_id> /bin/bash`

2. Go to the /workdir directory.
3. Run the `fuzz_client.py` script with the following positional arguments:

`./fuzz_client.py <plc_ip> <state> <index>`

A few notes:
1. State must be 'on' or 'off'.
2. For the stoplight model, index 0 == red, index 1 == yellow, and index 2 == green.
3. The HMI does an nmap scan of the internal docker subnet after starting, so the PLC station IPs will be displayed in order from Station0 to Station3.

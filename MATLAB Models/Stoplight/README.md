# OpenPLC and Simulink Stoplight Simulation
This is a simulation of a 4 way intersection controlled by a stoplight.  A single instance of OpenPLC controls all 4 lights, and Simlink connects the PLC and Simulink.

**Quickstart**
1. Open and run `Stoplight.slx` with Simulink.
2. Edit `interface.cfg` and set *simulink.ip* to the IP address where Simulink is installed with the `Stoplight.slx` loaded and running.
3. Run the installation script for OpenPLC and start an instance on the local machine.
4. Set the OpenPLC hardware layer to Simulink.
5. Upload and compile `stoplight.st`.
6. Start OpenPLC.
7. Compile the executable from [this repository](https://github.com/thiagoralves/OpenPLC_Simulink-Interface.git) and run it in the same directory as `interface.cft` above.
8. Admire traffic light.
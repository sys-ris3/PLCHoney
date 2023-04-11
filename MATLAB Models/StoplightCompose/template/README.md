## Changelog
- Patched compile script to always use Linux as the platform.  **This will not work on Windows**
- Fixed install script to successfully install all python dependencies, this required a manual pip install and a change of the python command

## Simulink Integration
To use the Hello World Example:

**OpenPLC**

Clone this repository

`./install`

If OpenPLC is not started automatically:

`./start_openplc.sh`

Navigate to the hardware section and install the Simulink Hardware layer.
Start OpenPLC.

**Simulink**

Install Mathworks Simulink, open the Hello World Example .slx file from the repository below.

**SimLink**

Install OpenPLC SimLink Interface

`git clone https://github.com/thiagoralves/OpenPLC_Simulink-Interface.git`

`g++ simlink.cpp -o simlink -pthread`

Make sure the correct interface.cfg is in the same directory as the executable.

`./simlink`

## README From Original Repository
# OpenPLC Runtime version 3

[![Build Status](https://travis-ci.org/thiagoralves/OpenPLC_v3.svg?branch=master)](https://travis-ci.org/thiagoralves/OpenPLC_v3)
[![Build status](https://ci.appveyor.com/api/projects/status/ut3466ixwtyf68qg?svg=true)](https://ci.appveyor.com/project/shrmrf/openplc-v3)

OpenPLC is an open-source [Programmable Logic Controller](https://en.wikipedia.org/wiki/Programmable_logic_controller) that is based on easy to use software. Our focus is to provide a low cost industrial solution for automation and research. OpenPLC has been used in [many research papers](https://scholar.google.com/scholar?as_ylo=2014&q=openplc&hl=en&as_sdt=0,1) as a framework for industrial cyber security research, given that it is the only controller to provide the entire source code.
The OpenPLC Project consists of three sub-projects:
1. [Runtime](https://github.com/thiagoralves/OpenPLC_v3)
2. [Programming editor](http://www.openplcproject.com/plcopen-editor)
3. [HMI builder](http://www.openplcproject.com/reference-installing-scadabr)

## Installation:
```bash
git clone https://github.com/thiagoralves/OpenPLC_v3.git
cd OpenPLC_v3
./install.sh [platform]
```

Where `[platform]` can be:

`win` - Install OpenPLC on Windows over Cygwin

`linux` - Install OpenPLC on a Debian-based Linux distribution

`docker` - Used by the `Dockerfile` (i.e. doesn't invoke `sudo`)

`rpi` - Install OpenPLC on a Raspberry Pi

`custom` - Skip all specific package installation and tries to install OpenPLC assuming your system already has all dependencies met. This option can be useful if you're trying to install OpenPLC on an unsuported Linux platform or had manually installed all the dependency packages before.

### Building, Installing and Running inside Docker
Make sure [`docker` is installed](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

#### Build
```
# instead of running install.sh as stated above, run:
docker build -t openplc:v3 .
```

#### RUN
_Devices can be passed to the `docker` daemon using the `-v` flag (e.g. `-v /dev/ttyACM0:/dev/ttyACM0`)_

```bash
docker run -it --rm --privileged -p 8080:8080 openplc:v3
```


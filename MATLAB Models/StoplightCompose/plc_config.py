#!/usr/bin/env python3

from webbot import Browser
from selenium import webdriver
import os, time, sys, requests

# This script automatically configures the OpenPLC instances by selecting the
# Simlink interface and compiling the hardware layer, then uploading the ST
# program and compiling it as well.  This currently happens in series, not parallel,
# which means deploying ~10 PLCs takes about 15 minutes.
# NOTE: This is only tested and working on Ubuntu and requires google chrome

def usage():
    print("./plc_config.py <ST_File> <OpenPLC_IP_and_Port>")
    print("Example: ./plc_config.py program.st 192.168.88.54:8080")
    exit()

if len(sys.argv) != 3:
    print(str(len(sys.argv)-1)+" args provided, 2 required.")
    usage()

# make sure the ST file exists
filepath = sys.argv[1]
if os.path.isfile(filepath):
    filepath = os.path.abspath(filepath)
    print(filepath)
else:
    print("There is a problem with "+filepath)
    exit()

# parse the OpenPLC IP
ip = sys.argv[2]
try:
    response = requests.get("http://"+ip)
    if response.status_code == 200:
        print("OpenPLC is online, continuing.")
    else:
        print("OpenPLC returns status code "+str(response.status_code))
        exit()
except:
    print("Invalid IP, or OpenPLC is offline.")
    exit()

web = Browser()

# log in to the page
web.go_to('http://'+ip+'/login')
web.type('openplc', into='username')
web.type('openplc', into='password')
web.click('login', tag='button')

# set the hardware layer to Simulink
web.go_to('http://'+ip+'/hardware')
web.click(xpath="//select[@id='hardware_layer']/option[@value='simulink_linux']")
web.click("Save Changes", tag='input')

# monitor for compilation completion
# this means waiting for teh 'Go to Dashboard' button to enable
complete = 'background: rgb(224, 34, 34); pointer-events: auto; width: 310px; height: 53px; margin: 0px 20px;'
while(web.find_elements(id="dashboard_button")[0].get_attribute('style') != complete):
    time.sleep(1)
print("Hardware layer compiled.")
time.sleep(2)

# select specified ST program
web.go_to('http://'+ip+'/programs')
#web.click(id='file', classname='input')
time.sleep(1)
filepath = 'C:\\Users\\brandon\\Desktop\\master_8080.st'
WebElement = web.driver.find_element_by_class_name('inputfile')
WebElement.send_keys(filepath)
web.click('Upload Program')

# create a temporary name
web.type('Production PLC ST Program', id='prog_name')
web.click('Upload program')

# wait for the program to compile
complete = 'background: rgb(224, 34, 34); pointer-events: auto; width: 310px; height: 53px; margin: 0px 20px;'
while(web.find_elements(id="dashboard_button")[0].get_attribute('style') != complete):
    time.sleep(1)
print("ST program compiled.")

# go to the dashboard and start the PLC
web.click('Go to Dashboard')
web.click('Start PLC')

web.quit()

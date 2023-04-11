#!/usr/bin/env python3

import socket
import sys

def help():
    print("Usage: ./fuzz_client.py <IP> <state> <coil_index>")
    exit()

ip = sys.argv[1]
state = sys.argv[2]
unit = sys.argv[3]

# lazy checks
# make sure the arguments are valid
try:
    socket.inet_aton(ip)
except:
    print("IP address is not valid.")
    help()
if state != 'on' and state != 'off':
    print("Second argument must be 'on' or 'off'")
    help()
try:
    unit_index = int(unit)
except:
    print("Third argument must be a valid int")
    help()

# establish the TCP connection with the PLC
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
plc = (ip, 502)
sock.connect(plc)

# transaction identifier
transaction_identifier = '\x0d\x58'
# protocol identifier
protocol_identifier = '\x00\x00'
# length
length = '\x00\x06'
# unit identifier
unit_identifier = '\x01'
# function code, 5 == write
function_code = '\x05'
# reference number
reference_number = '\x00' + chr(unit_index)

# data
if state == 'on':
    data = '\xff'
if state == 'off':
    data = '\x00'

# padding
padding = '\x00'

# send the modbus packet
message = transaction_identifier + protocol_identifier + length + unit_identifier + function_code + reference_number + data + padding
sock.sendall(message.encode())

# the plc should send confirmation that the instruction was understood
response = sock.recv(1024)
print(response)

sock.close()

import socket
import sys
import base64
import os
import json


def send_modbus(target_ip):
    # this is a modbus packet that asks to read coils with referenc enumber 0
    modbus_bytes = b'\x00\x01\x00\x00\x00\x06\x0a\x01\x00\x00\x00\x01'

    # if the code below fails to send to the server, the python error will tell you why
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    server_address = (target_ip, 502)
    sock.connect(server_address)
    sock.sendall(modbus_bytes)
    sock.close()


def scan_ip(target_ip):
    # make sure our scan directory exists
    if os.path.exists('scan') == False:
        os.mkdir('scan')

    if os.path.exists(os.path.join('scan', target_ip)):
        print("Already scanned "+target_ip+", skipping...")
        return

    scan_result = {}
    scan_result['error'] = None
    scan_result['target_ip'] = target_ip

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.settimeout(1)

    server_address = (target_ip, 502)
    print('connecting to ', server_address)
    try:
        sock.connect(server_address)
    except:
        scan_result['error'] = 'Failed to connect to TCP socket.'
        fstream = open(os.path.join('scan', target_ip), 'w')
        fstream.write(json.dumps(scan_result))
        fstream.close()
        return

    try:
        # Send data
        message = b'\x00\x01\x00\x00\x00\x05\x00+\x0e\x01\x00'
        print('sending enumeration command')
        sock.sendall(message)

        try:
            # Look for the response
            all_data = None

            amount_received = 0
            data = sock.recv(1024)

            print('received', data)

            scan_result['response_bytes'] = base64.b64encode(data).decode('utf8')

        except:
            scan_result['error'] = 'Timeout waiting for modbus response.'
            fstream = open(os.path.join('scan', target_ip), 'w')
            fstream.write(json.dumps(scan_result))
            fstream.close()

    finally:
        print('closing socket')
        sock.close()
        fstream = open(os.path.join('scan', target_ip), 'w')
        fstream.write(json.dumps(scan_result))
        fstream.close()

# this is the main scanning function used for plc enumeration, feed it the output of
# an nmap or zmap scan of the entire internet on port 502 as an argument
def main():
    fstream = open(sys.argv[1], 'r')
    lines = fstream.readlines()
    fstream.close()

    for line in lines:
        scan_ip(line.strip())

# this sends a valid, non modbus, command to the proxy.  This should be routed to the
# physical process simulation
def test():
    ip = input("Enter the modbus IP to scan >>>")
    print(ip)
    send_modbus(ip)

test()

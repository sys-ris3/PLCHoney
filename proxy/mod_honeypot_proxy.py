import os, socket, sys, time, struct, json, base64

# select a PLC profile from the most common PLCs
try:
    fstream = open('common_plc_profiles.json', 'r')
    plc_data = json.loads(fstream.read())
    fstream.close()
    for i in range(len(plc_data)):
        print(i+1, ".", plc_data[i]['device_id_objects'][0]['value'], plc_data[i]['device_id_objects'][1]['value'])
except:
    print('Couldn\'t load a PLC profile.')    

index = int(input('Choose a PLC profile: '))
jdata = plc_data[index - 1]

# this is the internal modbus IP address to pass modbus traffic to
# should be an accessible interface of openplc, conpot, etc.
MODBUS_HOST = '0.0.0.0'


# directory to store structurd logs
if os.path.exists('data') == False:
    os.mkdir('data')


def modbus_proxy_response(byte_payload):
    # takes a modbus payload and sends it to modbus endpoint and physical process simulation
    # accepts response and passes that response to host
    # if the modbus server is running on the same host as the proxy you will probably need to choose a port different from 502
    try:
        modbus_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        modbus_sock.settimeout(1.0)
        modbus_address = (MODBUS_HOST, 5000)
        modbus_sock.connect(modbus_address)
        modbus_sock.sendall(byte_payload)
        response = modbus_sock.recv(1024)
        modbus_sock.close()
        print("Successfully proxied response to modbus.")
    except:
        # this is a generic modbus response, "Exception Code: Gateway target device failed to respond (11)
        # it's a good alternative to an empty response if the proxy server is down
        response = b'\x00\x00\x00\x00\x00\x03\x0a\x88\x0b'
        print("Failed to proxy response to modbus, is the modbus ip and port reachable?")

    return response


def log(message):
    fstream = open('honeypot.log', 'a')
    # make sure we're actually writing a string to disk, could be bytes
    fstream.write("["+time.ctime()+"] "+str(message)+"\n")
    fstream.close()


def is_device_query(packet_bytes):
    # returns false if it's nothing, or the structured (JSON) format of the packet
    # if it's a proper query

    # packet less than 11 bytes cannot be a device query, skip even parsing it
    if len(packet_bytes) < 11:
        return False

    # this next section parsed the would be modbus packet, checking to make sure
    # it's a device query while structuring it

    parsed_modbus = {}

    # transaction identifier == first two bytes, it seems like most scanners choose something arbitrary
    transaction_identifier = struct.unpack('>h', packet_bytes[0:2])[0]
    parsed_modbus['transaction_identifier'] = transaction_identifier

    # protocol identifier, should be 0 in most modbus use cases
    protocol_identifier = struct.unpack('>h', packet_bytes[2:4])[0]
    parsed_modbus['protocol_identifier'] = protocol_identifier

    # bytes following this part of the packet
    payload_length = struct.unpack('>h', packet_bytes[4:6])[0]
    parsed_modbus['payload_length'] = payload_length

    # unit identifier, this could be anything and we should consider routing to different components based on the value
    unit_identifier = packet_bytes[6]
    parsed_modbus['unit_identifier'] = unit_identifier

    # function code, this should always be 43, for Read Device Identification
    function_code = packet_bytes[7]
    parsed_modbus['function_code'] = function_code

    # MEI type, should be 14 for most enumeration
    mei_type = packet_bytes[8]
    parsed_modbus['mei_type'] = mei_type

    # read device id, Basic Device Identification should be 1
    read_device_id = packet_bytes[9]
    parsed_modbus['read_device_id'] = read_device_id

    # object id should usually be vendor name, or 0
    object_id = packet_bytes[10]
    parsed_modbus['object_id'] = object_id

    # this next section does some simple checks in addition to payload length to make
    # sure we are seeing a device query
    # if this isn't a function code 43 request, it's not after the device ID
    if function_code != 43:
        return False

    return parsed_modbus


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 504)
sock.bind(server_address)

sock.listen(1)


while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)
        log('new connection from '+str(client_address))

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print('received "%s"' % data)
            if data:
                print('received', len(data), 'bytes')
            else:
                print('no more data from', client_address)
                break

            modbus_traffic = is_device_query(data)

            # if it's a device query, log the attempt and send the pre-chosen response since openplc will not
            # send something desirable
            if modbus_traffic:
                # if a profile is set, load the profile and respond as the selected device
                try:
                    modbus_response = base64.b64decode(jdata['response_bytes'])

                    # set the transaction identifier to what was in the request to be more realistic
                    transaction_id = struct.pack('>h', modbus_traffic['transaction_identifier'])
                    modbus_response = transaction_id + modbus_response[2:]

                except:
                    # this is a generic modbus response, "Exception Code: Gateway target device failed to respond (11)
                    modbus_response = b'\x00\x00\x00\x00\x00\x03\x0a\x88\x0b'
                    print("Failed to load PLC profile, this server will send a generic Modbus error response.")

                print("This is a device enumeration request, send a canned response.")
                event_record = {}
                event_record['timestamp'] = time.time()
                event_record['parsed_modbus'] = modbus_traffic
                event_record['remote_ip'] = client_address[0]

                fstream = open(os.path.join('data', str(int(time.time()))+'_modbus.json'), 'w')
                fstream.write(json.dumps(event_record))
                fstream.close()
                print(event_record)
                connection.sendall(modbus_response)

            # if it's not device enumeration, but it is valid modbus, pass it to the actual physical process simulation
            # and return that response to the client
            else:
                print("This is not device enumeration - sending to modbus server.")
                response_bytes = modbus_proxy_response(data)
                connection.sendall(response_bytes)

            break

    finally:
        connection.close()

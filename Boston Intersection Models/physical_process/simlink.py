import socket, time, json, _thread, struct
import parsers
import sanitizers
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# initialize the container states
containers = parsers.initialize_state()

REFLECTORS = {}

try:
    file = open('reflectors.json', 'r')
    REFLECTORS = json.loads(file.read())
    file.close()
except:
    print("No config file provided, defaulting to blank reflector config.")

LOG_TIME = time.time()
STANDBY = True

def exchange_plc_data():
    global containers
    global STANDBY
    raw_data = b''

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ('0.0.0.0', 8501)
    s.bind(server)

    # automatically proceed after 20 minutes
    counter = 0
    while STANDBY:
        print("Standing by..."+str(counter))
        time.sleep(1)
        counter += 1
        if counter > 1200:
            STANDBY = False

    counter = 0
    while True:
        for container in containers:
            # send data to the server
            s.sendto(parsers.c_to_payload(containers, container), (containers[container]['ip'], 6668))
            # listen for and print received data
            data, address = s.recvfrom(4096)
            if data != raw_data:
                raw_data = data
                counter+=1
                containers = parsers.update_plcdata(data, containers, container, LOG_TIME)

                # check for unsafe states after applying batch update
                sanitizers.get_unsafe_states(containers, LOG_TIME)

                # take care of the reflectors
                # {'parker_huntington': {'Offset_in': ['ruggles_huntington:Offset_in'], 'EW_Ped_Pressed': ['parker_huntington:EW_Vehical_Cnt']}}

                # update_single_state(containers, container, variable, value)
                for r_container in REFLECTORS:
                    for r_variable in REFLECTORS[r_container]:
                        for target in REFLECTORS[r_container][r_variable]:
                            new_value = parsers.get_coil(r_variable, r_container, containers)['value']
                            containers = parsers.update_single_state(containers, target.split(":")[0], target.split(":")[-1], new_value)

            # make individual state updates
            if container in REFLECTORS:
                for r_var in REFLECTORS[container]:
                    for source in REFLECTORS[container][r_var]:
                        new_value = parsers.get_coil(r_var, container, containers)['value']
                        containers = parsers.update_single_state(containers, source.split(":")[0], source.split(":")[0], new_value)

        time.sleep(.1)
    s.close()


##################################################################################
# everything below this line is for the REST API
##################################################################################
@app.route('/')
def check_reflectors():
    file = open("index.html", 'r')
    html = file.read()
    file.close()
    
    rows = []
    for container in containers:
        for var_type in containers[container]['state']:
            for coil in containers[container]['state'][var_type]:
                if 'raw' in coil:
                    coil_desc = coil['raw'].split(" ")[2].replace(":", "")
                    if len(coil['value']) == 1:
                        current_state = struct.unpack('<H', coil['value']+b'\x00')[0]
                    else:
                        current_state = struct.unpack('<H', coil['value'])[0]
                    rows.append("<tr><td>"+container+"</td><td>"+containers[container]['ip']+"</td><td>"+coil['varName']+"</td><td>"+coil['type']+"</td><td>"+coil_desc+"</td><td>"+str(current_state)+"</td><td>"+"<form action=\"reflector/"+container+"/"+coil['varName']+"\"><input type=\"submit\" value=\"Reflect This Coil"+"\" /></form>"+"</tr>")

    html = html.replace("TABLE_ROWS", "".join(rows))

    if len(REFLECTORS) > 0:
        th = '''
            <table>
            <tr>
            <th>Source Container</th><th>Source Variable</th><th>Target Container</th><th>Target Variable</th><th>Action</th>
            </tr>
            TABLE_ROWS
            </table>
            <form action="/export_config"><input type="submit" value="Export Config" /></form>
        '''
        rows = []
        for i in REFLECTORS:
            for socket in REFLECTORS[i]:
                for target in REFLECTORS[i][socket]:
                    button = "<form action=\"/remove/"+str(i)+"/"+socket+"/"+target.split(":")[0]+"/"+target.split(":")[1]+"\"><input type=\"submit\" value=\"Remove this reflection\"></form>"
                    rows.append("<tr><td>"+str(i)+"</td><td>"+socket+"</td><td>"+target.split(":")[0]+"</td><td>"+target.split(":")[1]+"</td><td>"+button+"</td></tr>")
        th = th.replace("TABLE_ROWS", "".join(rows))
        html = html.replace("No ports reflected.", th)

    # get the coil states for the containers
    # /get_container/<container>
    # Click <a href="/start">here</a> after all the PLCs are running.<br>
    container_links = []
    for c in containers:
        container_links.append("<a href=\"/get_container/"+c+"\">"+c+"</a>")

    html = html.replace("COIL_STATES", "<br>".join(container_links))

    return html


@app.route('/remove/<source_container>/<source_variable>/<target_container>/<target_variable>', methods = ['GET'])
def remove_reflector(source_container, source_variable, target_container, target_variable):
    global REFLECTORS
    print(REFLECTORS)
    # {'parker_huntington': {'Offset_in': ['ruggles_huntington:Offset_in'], 'EW_Ped_Pressed': ['parker_huntington:EW_Vehical_Cnt']}}
    index = REFLECTORS[source_container][source_variable].index(target_container+":"+target_variable)
    print(index)
    if index >= 0 and len(REFLECTORS[source_container][source_variable]) >= 1:
        print(REFLECTORS[source_container][source_variable])
        REFLECTORS[source_container][source_variable].pop(index)
        print(REFLECTORS[source_container][source_variable])
    return redirect(url_for('check_reflectors'))

@app.route('/reflector/<source_container>/<source_variable>', methods = ['GET', 'POST'])
def set_reflector(source_container, source_variable):
    if request.method == 'GET':
        # read the set reflector template
        file = open("set_reflector.html", 'r')
        html = file.read()
        file.close()
        var_type = parsers.get_coil(source_variable, source_container, containers)['type']
        coil = parsers.get_coil(source_variable, source_container, containers)['raw'].split()[2]
        val = parsers.get_coil(source_variable, source_container, containers)['value']
        if len(val) == 1:
            current_state = struct.unpack('<H', val+b'\x00')[0]
        else:
            current_state = struct.unpack('<H', val)[0]

        source = "<tr><td>"+source_container+"</td><td>"+source_variable+"</td><td>"+var_type+"</td><td>"+coil+"</td><td>"+str(current_state)+"</td></tr>"
        html = html.replace("TABLE_ROWS", source)

        rows = []
        for c in containers:
            for c_type in containers[c]['state']:
                for coil in containers[c]['state'][c_type]:
                    if 'raw' in coil and "%I" in coil['raw']:
                        rows.append("<option value=\""+c+":"+coil['varName']+"\" id=\"socket\">"+coil['varName']+" at "+c+"</option>")
        html = html.replace("DROPDOWN", "".join(rows))
        html = html.replace("INTERSECTION_VARS", source_container+"/"+source_variable)
        html = html.replace("RECEIVE_PORT", source_container+"/"+source_variable)

        return html

    else:
        # update the reflectors
        destination_coil = request.form['object']

        if source_container not in REFLECTORS:
            REFLECTORS[source_container] = {}
        if source_variable not in REFLECTORS[source_container]:
            REFLECTORS[source_container][source_variable] = []
        REFLECTORS[source_container][source_variable].append(destination_coil)

        return redirect(url_for('check_reflectors'))


@app.route('/export_config')
def export_config():
    with open('reflectors.json', 'w') as fp:
        json.dump(REFLECTORS, fp)
    return redirect(url_for('check_reflectors'))

@app.route('/get_containers')
def get_containers():
    print(containers)
    return json.dumps(containers)

@app.route('/get_container/<container>')
def get_container(container):
    if container not in containers:
        return "{'Status': 'No such container'}"

    rows = []
    for c_type in containers[container]['state']:
        row = [c_type]
        for value in containers[container]['state'][c_type]:
            row.append(str(value['value']))
        rows.append(row)

    css = '''
<!DOCTYPE html>
<html>
<head>
<style>
#coils {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#coils td, #customers th {
  border: 1px solid #ddd;
  padding: 8px;
}

#coils tr:nth-child(even){background-color: #f2f2f2;}

#coils tr:hover {background-color: #ddd;}

#coils th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}
</style>
</head>
'''


    html = "<table id=\"coils\"><tr><th>Coil Type</th>"
    for x in range(0, len(rows[0])-1):
        html = html + ("<th>Index"+str(x)+"</th>")
    html = html + "</tr><tr>"

    for row in rows:
        html = html + "<td>" + "</td><td>".join(row) + "</td></tr>"
    html = html + "</table>"


    print(containers[container])

    return css + html

@app.route('/start')
def start():
    global STANDBY
    STANDBY = False
    return redirect(url_for('check_reflectors'))

@app.route('/check_logs')
def check_logs():
    file = open(str(LOG_TIME)+"_update_log.tsv", 'r')
    lines = file.readlines()
    file.close()

    return "<br>".join(lines[::-1])

@app.route('/check_errors')
def check_errors():
    try:
        file = open(str(LOG_TIME)+"_error_log.tsv", 'r')
        lines = file.readlines()
        file.close()

        return "<br>".join(lines[::-1])
    except:
        return "No errors yet."

@app.route('/bad_states')
def bad_states():
    return json.dumps(sanitizers.UNDESIRED_STATES)

def run_server():
    app.run('0.0.0.0', port=8000)

def main():
    print("Starting logging thread...")
    _thread.start_new_thread(exchange_plc_data, ())
    print("OK")

    # run the webserver on it's own thread
    print("Running app...")
    _thread.start_new_thread( run_server, () )

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()

import intersection_template
import socket, time, _thread, struct

# change this to the ip where simlink is running,
# this is important for inputs like crosswalk button
# pushes and vehicles waiting at an intersection
SIMLINK_IP = 'localhost'

LOG_TIME = time.time()
LOGS = []

##############################################
# This is the dictionary that holds the state
# of each component in an intersection.  The
# names should be descriptive enough, but there
# is an additional description to make it clear.
#
# Naming convention follows this format:
# <intersection_direction/position_light_color>
##############################################

# this state maps one port to one light, it may be helpful
# for more specific error detection and precise control
'''
state = {
    ########################################
    # Intersection of Ruggles and Huntington
    #       intersection key == RH
    ########################################
    # Southbound Right Stoplight
    26013: ['RH_SR_S_Gre', False],
    26014: ['RH_SR_S_Yel', False],
    26015: ['RH_SR_S_Red', False],

    # Southbound Left Stoplight
    26016: ['RH_SL_S_Gre', False],
    26017: ['RH_SL_S_Yel', False],
    26018: ['RH_SL_S_Red', False],

    # Northbound Right Stoplight
    26001: ['RH_NR_S_Gre', False],
    26002: ['RH_NR_S_Yel', False],
    26003: ['RH_NR_S_Red', False],

    # Northbound Middle Stoplight
    26004: ['RH_NM_S_Gre', False],
    26005: ['RH_NM_S_Yel', False],
    26006: ['RH_NM_S_Red', False],

    # Northbound Left LeftTurnStoplight
    26007: ['RH_NL_LS_GreLeft', False],
    26008: ['RH_NL_LS_YeLeft', False],
    26009: ['RH_NL_LS_ReLeft', False],

    # Eastbound Solo Stoplight
    26010: ['RH_ES_S_Gre', False],
    26011: ['RH_ES_S_Yel', False],
    26012: ['RH_ES_S_Red', False],

    # Westbound Solo HybridLeftStoplight
    26019: ['RH_WS_HLS_Gre', False],
    26020: ['RH_WS_HLS_Yel', False],
    26021: ['RH_WS_HLS_Red', False],
    26022: ['RH_WS_HLS_YeLeft', False],
    26023: ['RH_WS_HLS_ReLeft', False],

    # South Crosswalk (Crossing Huntington)
    25003: ['RH_SR_Walk', False],
    25004: ['RH_SL_Walk', False],

    # North Crosswalk (Crossing Huntington)
    25005: ['RH_NR_Walk', False],
    25006: ['RH_NL_Walk', False],

    # East Crosswalk (Crossing Ruggles)
    25009: ['RH_ER_Walk', False],
    25010: ['RH_EL_Walk', False],

    # West Crosswalk (Crossing Ruggles)
    25007: ['RH_WR_Walk', False],
    25008: ['RH_WL_Walk', False],

    ########################################
    # Intersection of Parker and Huntington
    #       intersection key == PH
    ########################################
    # Southbound Right Stoplight
    26024: ['PH_SR_S_Gre', False],
    26025: ['PH_SR_S_Yel', False],
    26026: ['PH_SR_S_Red', False],

    # Southbound Middle Stoplight
    26027: ['PH_SM_S_Gre', False],
    26028: ['PH_SM_S_Yel', False],
    26029: ['PH_SM_S_Red', False],

    # Southbound Left LeftTurnStoplight
    26030: ['PH_SL_LS_GreLeft', False],
    26031: ['PH_SL_LS_YeLeft', False],
    26032: ['PH_SL_LS_ReLeft', False],

    # Northbound Right Stoplight
    26033: ['PH_NR_S_Gre', False],
    26034: ['PH_NR_S_Yel', False],
    26035: ['PH_NR_S_Red', False],

    # Northbound Left Stoplight
    26036: ['PH_NL_S_Gre', False],
    26037: ['PH_NL_S_Yel', False],
    26038: ['PH_NL_S_Red', False],

    # Eastbound Solo Stoplight
    26039: ['PH_ES_S_Gre', False],
    26040: ['PH_ES_S_Yel', False],
    26041: ['PH_ES_S_Red', False],

    # Westbound Right Stoplight
    26042: ['PH_WR_S_Gre', False],
    26043: ['PH_WR_S_Yel', False],
    26044: ['PH_WR_S_Red', False],

    # Westbound Left LeftTurnStoplight
    26045: ['PH_WL_LS_GreLeft', False],
    26046: ['PH_WL_LS_YeLeft', False],
    26047: ['PH_WL_LS_ReLeft', False],

    # South Crosswalk (Crossing Huntington)
    25011: ['PH_SR_Walk', False],
    25012: ['PH_SL_Walk', False],

    # North Crosswalk (Crossing Huntington)
    25013: ['PH_NR_Walk', False],
    25014: ['PH_NL_Walk', False],

    # East Crosswalk (Crossing Parker)
    25015: ['PH_ER_Walk', False],
    25016: ['PH_EL_Walk', False],

    # West Crosswalk (Crossing Parker)
    25017: ['PH_WR_Walk', False],
    25018: ['PH_WL_Walk', False],

    ########################################
    # Intersection of Forsyth and Huntington
    #      intersection key == FH
    ########################################
    # Southbound Right Stoplight
    26048: ['FH_SR_S_Gre', False],
    26049: ['FH_SR_S_Yel', False],
    26050: ['FH_SR_S_Red', False],

    # Southbound Left Stoplight
    26051: ['FH_SL_S_Gre', False],
    26052: ['FH_SL_S_Yel', False],
    26053: ['FH_SL_S_Red', False],

    # Northbound Right Stoplight
    26054: ['FH_NR_S_Gre', False],
    26055: ['FH_NR_S_Yel', False],
    26056: ['FH_NR_S_Red', False],

    # Northbound Left Stoplight
    26057: ['FH_NL_S_Gre', False],
    26058: ['FH_NL_S_Yel', False],
    26059: ['FH_NL_S_Red', False],

    # Eastbound Right Stoplight
    26060: ['FH_ER_S_Gre', False],
    26061: ['FH_ER_S_Yel', False],
    26062: ['FH_ER_S_Red', False],

    # Eastbound Left Stoplight
    26063: ['FH_EL_S_Gre', False],
    26064: ['FH_EL_S_Yel', False],
    26065: ['FH_EL_S_Red', False],

    # Westbound Right Stoplight
    26066: ['FH_WR_S_Gre', False],
    26067: ['FH_WR_S_Yel', False],
    26068: ['FH_WR_S_Red', False],

    # Westbound Left Stoplight
    26069: ['FH_WL_S_Gre', False],
    26070: ['FH_WL_S_Yel', False],
    26071: ['FH_WL_S_Red', False],

    # South Crosswalk (Crossing Huntington)
    25019: ['FH_SR_Walk', False],
    25020: ['FH_SL_Walk', False],

    # North Crosswalk (Crossing Huntington)
    25021: ['FH_NR_Walk', False],
    25022: ['FH_NL_Walk', False],

    # East Crosswalk (Crossing Forsyth)
    25023: ['FH_ER_Walk', False],
    25024: ['FH_EL_Walk', False],

    # West Crosswalk (Crossing Forsyth)
    25025: ['FH_WR_Walk', False],
    25026: ['FH_WL_Walk', False]

}
'''

STATE = {
    ########################################
    # Intersection of Ruggles and Huntington
    #       intersection key == RH
    ########################################
    # Southbound Right Stoplight
    26013: ['RH_SR_S_Gre', False],
    26014: ['RH_SR_S_Yel', False],
    26015: ['RH_SR_S_Red', False],

    # Southbound Left Stoplight
    26016: ['RH_SL_S_Gre', False],
    26017: ['RH_SL_S_Yel', False],
    26018: ['RH_SL_S_Red', False],

    # Northbound Right Stoplight
    26001: ['RH_NR_S_Gre', False],
    26002: ['RH_NR_S_Yel', False],
    26003: ['RH_NR_S_Red', False],

    # Northbound Middle Stoplight
    26004: ['RH_NM_S_Gre', False],
    26005: ['RH_NM_S_Yel', False],
    26006: ['RH_NM_S_Red', False],

    # Northbound Left LeftTurnStoplight
    26007: ['RH_NL_LS_GreLeft', False],
    26008: ['RH_NL_LS_YeLeft', False],
    26009: ['RH_NL_LS_ReLeft', False],

    # Eastbound Solo Stoplight
    26010: ['RH_ES_S_Gre', False],
    26011: ['RH_ES_S_Yel', False],
    26012: ['RH_ES_S_Red', False],

    # Westbound Solo HybridLeftStoplight
    26019: ['RH_WS_HLS_Gre', False],
    26020: ['RH_WS_HLS_Yel', False],
    26021: ['RH_WS_HLS_Red', False],
    26022: ['RH_WS_HLS_YeLeft', False],
    26023: ['RH_WS_HLS_ReLeft', False],

    # South Crosswalk (Crossing Huntington)
    25003: ['RH_SR_Walk', False],
    25004: ['RH_SL_Walk', False],

    # North Crosswalk (Crossing Huntington)
    25005: ['RH_NR_Walk', False],
    25006: ['RH_NL_Walk', False],

    # East Crosswalk (Crossing Ruggles)
    25009: ['RH_ER_Walk', False],
    25010: ['RH_EL_Walk', False],

    # West Crosswalk (Crossing Ruggles)
    25007: ['RH_WR_Walk', False],
    25008: ['RH_WL_Walk', False],

    ########################################
    # Intersection of Parker and Huntington
    #       intersection key == PH
    ########################################
    # North Green
    26024: ['PH_SR_S_Gre', 'PH_SM_S_Gre', False],
    # South Green
    26033: ['PH_NR_S_Gre', 'PH_NL_S_Gre', False],
    # East Green
    26042: ['PH_WR_S_Gre', False],
    # West Green
    26039: ['PH_ES_S_Gre', False],
    # North Yellow
    26025: ['PH_SR_S_Yel', 'PH_SM_S_Yel', False],
    # South Yellow
    26034: ['PH_NR_S_Yel', 'PH_NL_S_Yel', False],
    # East Yellow
    26043: ['PH_WR_S_Yel', False],
    # West Yellow
    26040: ['PH_ES_S_Yel', False],
    # North Red
    26026: ['PH_SR_S_Red', 'PH_SM_S_Red', False],
    # South Red
    26035: ['PH_NR_S_Red', 'PH_NL_S_Red', False],
    # East Red
    26044: ['PH_WR_S_Red', False],
    # West Red
    26041: ['PH_ES_S_Red', False],
    # North Left Yellow
    26031: ['PH_SL_LS_YeLeft', False],
    # East Left Yellow
    26046: ['PH_WL_LS_YeLeft', False],
    # North Left Green
    26030: ['PH_SL_LS_GreLeft', False],
    # East Left Green
    26045: ['PH_WL_LS_GreLeft', False],
    # North Left Red
    26032: ['PH_SL_LS_ReLeft', False],
    # East Left Red
    26047: ['PH_WL_LS_ReLeft', False],
    # North Pedestrian
    25011: ['PH_SR_Walk', 'PH_SL_Walk', False],
    # South Pedestrian
    25013: ['PH_NR_Walk', 'PH_NL_Walk', False],
    # East Pedestrian
    25015: ['PH_ER_Walk', 'PH_EL_Walk', False],
    # West Pedestrian
    25017: ['PH_WR_Walk', 'PH_WL_Walk', False],

    ########################################
    # Intersection of Forsyth and Huntington
    #      intersection key == FH
    ########################################
    # Southbound Right Stoplight
    26048: ['FH_SR_S_Gre', False],
    26049: ['FH_SR_S_Yel', False],
    26050: ['FH_SR_S_Red', False],

    # Southbound Left Stoplight
    26051: ['FH_SL_S_Gre', False],
    26052: ['FH_SL_S_Yel', False],
    26053: ['FH_SL_S_Red', False],

    # Northbound Right Stoplight
    26054: ['FH_NR_S_Gre', False],
    26055: ['FH_NR_S_Yel', False],
    26056: ['FH_NR_S_Red', False],

    # Northbound Left Stoplight
    26057: ['FH_NL_S_Gre', False],
    26058: ['FH_NL_S_Yel', False],
    26059: ['FH_NL_S_Red', False],

    # Eastbound Right Stoplight
    26060: ['FH_ER_S_Gre', False],
    26061: ['FH_ER_S_Yel', False],
    26062: ['FH_ER_S_Red', False],

    # Eastbound Left Stoplight
    26063: ['FH_EL_S_Gre', False],
    26064: ['FH_EL_S_Yel', False],
    26065: ['FH_EL_S_Red', False],

    # Westbound Right Stoplight
    26066: ['FH_WR_S_Gre', False],
    26067: ['FH_WR_S_Yel', False],
    26068: ['FH_WR_S_Red', False],

    # Westbound Left Stoplight
    26069: ['FH_WL_S_Gre', False],
    26070: ['FH_WL_S_Yel', False],
    26071: ['FH_WL_S_Red', False],

    # South Crosswalk (Crossing Huntington)
    25019: ['FH_SR_Walk', False],
    25020: ['FH_SL_Walk', False],

    # North Crosswalk (Crossing Huntington)
    25021: ['FH_NR_Walk', False],
    25022: ['FH_NL_Walk', False],

    # East Crosswalk (Crossing Forsyth)
    25023: ['FH_ER_Walk', False],
    25024: ['FH_EL_Walk', False],

    # West Crosswalk (Crossing Forsyth)
    25025: ['FH_WR_Walk', False],
    25026: ['FH_WL_Walk', False]

}




# just a function to draw an ascii representation of the intersection for
# easy understanding, nothing critical here
def draw_state():
    current = intersection_template.template

    state_reprs = {
        True : {
                'Gre' : "\33[92mO\33[0m\33[0m",
                'GreLeft' : "\33[92m<\33[0m\33[0m",
                'Red' : "\33[91mO\33[0m\33[0m",
                'ReLeft' : "\33[91m<\33[0m\33[0m",
                'Yel' : "\33[93mO\33[0m\33[0m",
                'YeLeft' : "\33[93m<\33[0m\33[0m",
                'Walk': "X"
            },
        False : {
                'Gre' : "\33[90mO\33[0m",
                'GreLeft' : "\33[90m<\33[0m",
                'Red' : "\33[90mO\33[0m",
                'ReLeft' : "\33[90m<\33[0m",
                'Yel' : "\33[90mO\33[0m",
                'YeLeft' : "\33[90m<\33[0m",
                'Walk': "\33[93mD\33[0m"
            }
    }

    # check each component in the state and make updates for display
    for key in STATE:
        for light in STATE[key][:-1]:
            replacement = state_reprs[STATE[key][-1]][light.split("_")[-1]]
            current = current.replace(light, replacement)


    print(current)

# listen for an incoming UDP packets, update that port's info in the state dict
# this is simple to overhaul if we use more complex structs
def start_coil(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('0.0.0.0', port)

    # make sure the port is actually available, if it isn't you either
    # need to redefine it in Simlink or kill the process using it
    try:
        sock.bind(server_address)
        print("Started listener on UDP "+str(port))
    except:
        print("Port is probably unavailable, either wait or stop the process using it.")
        return 1

    while True:
        # watch for packets from Simlink, update state as necessary
        data, address = sock.recvfrom(32)

        # parse the data and update the state accordingly
        if data and len(data)>1:
            # just look at the first two bytes, this should stop the problem
            # with routers adding random null bytes to the end
            log_entry = ""
            relevant = data[:2]
            log_entry = log_entry + str(time.time()-LOG_TIME)+"\t"+str(port)+"\t"+relevant.hex()+"\t"
            result = struct.unpack('>H', relevant)

            # just treat everything as a bool for now, parse more complex types in the future
            if result[0] > 0:
                log_entry = log_entry + str(STATE[port][-1])+"\t"
                STATE[port][-1] = True
                log_entry = log_entry + str(STATE[port][-1])+"\t"+str(STATE[port][0])+"\n"
            else:
                log_entry = log_entry + str(STATE[port][-1])+"\t"
                STATE[port][-1] = False
                log_entry = log_entry + str(STATE[port][-1])+"\t"+str(STATE[port][0])+"\n"

            # add the log entry to the log buffer
            LOGS.append(log_entry)

# additional error detection, this is still a TODO, but can be easily defined
# based on the STATE defined above after we make a decision about types in the ST
def detect_undesired_states():
    pass


# simulate button push for crosswalk or a vehicle sitting at a stoplight
# we just have to send a UDP to the correct Simlink port, the IP can be
# defined at the top of this file
def send_simlink_input(port):
    message = b'\x01\x00'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (SIMLINK_IP, port))

def main():
    # create a socket for each port
    for key in STATE:
        _thread.start_new_thread( start_coil, (key, ) )

    time.sleep(1)

    # print the state every so often
    while True:
        draw_state()

        # write log buffer to file, TODO find a prettier way to do this
        file = open(str(LOG_TIME)+'_stoplight_logs.tsv', 'a')
        while len(LOGS) > 1:
            file.write(LOGS[0])
            LOGS.pop(0)
        file.close()

        time.sleep(1)


if __name__ == "__main__":
    main()

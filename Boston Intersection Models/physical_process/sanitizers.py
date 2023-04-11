import struct, time

UNDESIRED_STATES = {}

def make_bool(b):
    return struct.unpack('?', b)[0]

# takes a digitalOut list and returns
# a stoplight dictionary
def c_type_to_dict(c_type):
    intersection = {}
    for coil in c_type:
        if 'varName' in coil:
            direction = coil['varName'].split("_")[0]
            color = coil['varName'].split("_")[-1]
            if direction not in intersection:
                intersection[direction] = {}
            intersection[direction][color] = make_bool(coil['value'])
    return intersection

# some helper functions for checking undesired state
def ew_green_yellow(intersection):
    '''Return true if there is a green or yellow true for east or west'''
    if intersection["E"]["G"]:
        return True
    if intersection["E"]["Y"]:
        return True
    if intersection["W"]["G"]:
        return True
    return intersection["W"]["Y"]

def ns_green_yellow(intersection):
    '''Return true if there is a green or yellow true for north or south'''
    if intersection["N"]["G"]:
        return True
    if intersection["N"]["Y"]:
        return True
    if intersection["S"]["G"]:
        return True
    return intersection["S"]["Y"]

def ew_pedestrian(intersection):
    if intersection["W"]["P"]:
        return True
    return intersection["E"]["P"]

def ns_pedestrian(intersection):
    if intersection["N"]["P"]:
        return True
    return intersection["S"]["P"]

def individual_light_conflict(light):
    if light["G"] and light["Y"]:
        return True
    if light["G"] and light["R"]:
        return True
    if light["Y"] and light["R"]:
        return True
    if light["LG"] and light["LY"]:
        return True
    if light["LG"] and light["LR"]:
        return True
    return light["LY"] and light["LR"]

def get_unsafe_states(containers, LOG_TIME):
    # only check physical process states at intersections
    for container in containers:
        if "huntington" in container:
            # lamp states are defined in digitalOut
            intersection = c_type_to_dict(containers[container]['state']['digitalOut'])
            # this check makes sure there are not conflicting green and yellow lights
            if ns_green_yellow(intersection) and ew_green_yellow(intersection):
                # unsafe state!
                index = len(UNDESIRED_STATES)
                UNDESIRED_STATES[index] = {}
                UNDESIRED_STATES[index]['ts'] = time.time()
                UNDESIRED_STATES[index]['message'] = "Unsafe/conflicting green/yellow lights at "+container
                UNDESIRED_STATES[index]['intersection'] = container
                UNDESIRED_STATES[index]['log_ts'] = LOG_TIME
                UNDESIRED_STATES[index]['state'] = intersection
                # give a more specific error about why something was unsafe: TODO
                # UNDESIRED_STATES[index]['struct'] = {}

            # this check makes sure that the intersection PLCs have the same offset as the field master


            # this check makes sure that incompatible lights at an intersection are not on
            for light in intersection:
                if individual_light_conflict(intersection[light]):
                    index = len(UNDESIRED_STATES)
                    UNDESIRED_STATES[index] = {}
                    UNDESIRED_STATES[index]['ts'] = time.time()
                    UNDESIRED_STATES[index]['message'] = "Unsafe/conflicting lamps on single light at "+container
                    UNDESIRED_STATES[index]['intersection'] = container
                    UNDESIRED_STATES[index]['log_ts'] = LOG_TIME
                    UNDESIRED_STATES[index]['state'] = intersection

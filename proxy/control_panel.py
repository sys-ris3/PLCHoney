from flask import Flask, redirect
import json, os, time


app = Flask(__name__)


PLC_PROFILE = 'plc_profiles.json'


homepage_html = '''
<!DOCTYPE html>
<html>
<head>
<style>
.tree li{
  display      : block;
}
table, th, td {
  border: 1px solid black;
}
</style>
</head>
<h2>Current PLC Profile</h2>
CURRENT_PROFILE
<h2>Select PLC Profile - PROFILE_COUNT Profiles Available</h2>
PROFILE_CONTENT
<h2>Scanning Activity - SCAN_COUNT Result(s)</h2>
<a href="/raw_scan_json">Download Raw Scan Data</a><br><br>
SCAN_CONTENT
</html>
'''


def load_scan_results():
    files = sorted(os.listdir('data'))[::-1]

    rows = [['Timestamp', 'Remote IP', 'Transaction ID', 'Payload Bytes']]

    for s in files:
        try:
            fstream = open(os.path.join('data', s), 'r')
            jdata = json.loads(fstream.read())
            fstream.close()
        except:
            continue

        row = []
        row.append(hr_time(jdata['timestamp']))
        row.append(jdata['remote_ip'])
        row.append(jdata['parsed_modbus']['transaction_identifier'])
        row.append(jdata['parsed_modbus']['payload_length'])
        rows.append(row)

    return rows



# the first entry in the 2d list is treated as the header
def list_to_table(title, l):
    # merge the cells of the title row
    table = "<table><tr><th style=\"text-align:center\" colspan=\""+str(len(l[0]))+"\">"+title+"</th></tr>"

    # add the column labels
    titles = "<tr>"
    for label in l[0]:
        titles += "<th>"+str(label)+"</th>"
    table += titles+"</tr>"

    # add in the rest of the columns
    data = ""
    for row in l[1:]:
        data += "<tr>"
        for value in row:
            data += "<td>"+str(value)+"</td>"
        data += "</tr>"
    table += data+"</table>"

    return table


def hr_time(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(epoch)))


def count_profiles():
    fstream = open(PLC_PROFILE, 'r')
    jdata = json.loads(fstream.read())
    fstream.close()
    return str(len(jdata))


def count_scans():
    if os.path.exists('data'):
        return len(os.listdir('data'))
    return 0

def get_honeypot_results():
    return


def profile_to_tree():
    fstream = open(PLC_PROFILE, 'r')
    jdata = json.loads(fstream.read())
    fstream.close()

    unique_byte_list = []
    master_profile_list = {}

    for x in range(0, len(jdata)):
        # every profile at least has a single object in the object list
        if len(jdata[x]['device_id_objects']) < 1:
            continue

        # no need to serve multiple instances of identical profiles
        if jdata[x]['response_bytes'] in unique_byte_list:
            continue
        unique_byte_list.append(jdata[x]['response_bytes'])


        # remove whitespace at the end, many responses contain several spaces after the vendor
        master_name = jdata[x]['device_id_objects'][0]['value'].strip()

        ######################################################################
        # VendorName
        ######################################################################
        # create an entry for the vendor name
        if master_name not in master_profile_list:
            master_profile_list[master_name] = {}

        # profiles for the current level, some responses only have a vendor name
        if len(jdata[x]['device_id_objects']) == 1:
            if 'UNSPECIFIED' not in master_profile_list[master_name]:
                master_profile_list[master_name]['UNSPECIFIED'] = {}

        ######################################################################
        # ProductCode
        ######################################################################
        if len(jdata[x]['device_id_objects']) > 1:
            master_product_code = jdata[x]['device_id_objects'][1]['value'].strip()
        else:
            master_product_code = 'UNSPECIFIED'

        if master_product_code not in master_profile_list[master_name]:
            master_profile_list[master_name][master_product_code] = {}

        ######################################################################
        # MajorMinorRevision
        ######################################################################
        if len(jdata[x]['device_id_objects']) > 2:
            master_version = jdata[x]['device_id_objects'][2]['value'].strip()
        else:
            master_version = 'UNSPECIFIED'

        if master_version not in master_profile_list[master_name][master_product_code]:
            master_profile_list[master_name][master_product_code][master_version] = []

        master_profile_list[master_name][master_product_code][master_version].append(str(x))

    # format the dict as a tree view html expandable list
    vendors = []
    for vendor in sorted(master_profile_list.keys()):
        product_code_list = []
        for product_code in master_profile_list[vendor]:
            mm_rev_list = []
            for mm_rev in master_profile_list[vendor][product_code]:
                setter_links = []
                for index in master_profile_list[vendor][product_code][mm_rev]:
                    setter_links.append("<a href=\"/set_profile/"+str(index)+"\"> Objects: "+str(len(jdata[x]['device_id_objects']))+"; Region: "+jdata[int(index)]['region']+" </a>")
                mm_rev_list.append("<details><summary>"+mm_rev+"</summary><ul>" + "</li><li>".join(setter_links) + "</ul></details>")

            bottom_level_list = "<ul><li>" + "</li><li>".join(mm_rev_list) + "</li></ul>"

            product_code_list.append("<li><details><summary>" + product_code + "</summary>" + bottom_level_list + "</details></li>")
        vendors.append("<li><details><summary>" + vendor + "</summary><ul>" + "".join(product_code_list) + "</ul></details></li>")

    return "<ul class=\"tree\">" + "".join(vendors) + "</ul>"


@app.route('/set_profile/<index>')
def set_profile(index):
    fstream = open(PLC_PROFILE, 'r')
    jdata = json.loads(fstream.read())
    fstream.close()

    # make sure we are working with an integer
    try:
        index_int = int(index)
    except:
        return "Route must be indexable integer!", 500

    # make sure the index actually exists
    try:
        profile = jdata[index_int]
    except:
        return "Index not present in profile database!", 500

    fstream = open('current_profile.json', 'w')
    fstream.write(json.dumps(profile))
    fstream.close()

    return redirect('/')


@app.route('/raw_scan_json')
def raw_scan_json():
    scan_data = []
    if os.path.exists == False:
        return json.dumps(scan_data)

    files = os.listdir('data')
    for f in files:
        try:
            fstream = open(os.path.join('data', f), 'r')
            jdata = json.loads(fstream.read())
            fstream.close()

            scan_data.append(jdata)
        except:
            continue
    return json.dumps(scan_data)


@app.route('/')
def main_page():
    # get the current profile
    current_profile = 'NONE'
    if os.path.exists('current_profile.json'):
        try:
            fstream = open("current_profile.json", 'r')
            jdata = json.loads(fstream.read())
            fstream.close()

            current_profile = "<strong>VendorName:</strong> "+jdata["device_id_objects"][0]["value"].strip()

            if len(jdata["device_id_objects"]) > 1:
                current_profile = current_profile + "<br><strong>ProductCode:</strong> "+jdata["device_id_objects"][1]["value"].strip()
            if len(jdata["device_id_objects"]) > 2:
                current_profile = current_profile + "<br><strong>MajorMinorRevision:</strong> "+jdata["device_id_objects"][2]["value"].strip()

        except:
            current_profile = 'ERROR READING PROFILE'

    # load the available profiles
    results = profile_to_tree()
    html = homepage_html.replace('PROFILE_CONTENT', results)

    html = html.replace("CURRENT_PROFILE", current_profile)
    html = html.replace("PROFILE_COUNT", count_profiles())

    # render the current scan results
    html = html.replace("SCAN_COUNT", str(count_scans()))
    table = list_to_table("Modbus Scanning Activity", load_scan_results())
    html = html.replace("SCAN_CONTENT", table)

    return html

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)

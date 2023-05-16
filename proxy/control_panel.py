from flask import Flask, redirect
import json, os


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
</style>
</head>
<h2>Current PLC Profile</h2>
CURRENT_PROFILE
<h2>Select PLC Profile</h2>
PROFILE_CONTENT
</html>
'''


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

    return html

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)

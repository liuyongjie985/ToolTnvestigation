########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import ssl
import json
import os
import traceback
import re
import requests

ssl._create_default_https_context = ssl._create_unverified_context

env = os.environ

headers = {
    # Request headers
    'app_id': env.get('APP_ID', 'yaminoryu_foxmail_com_02ed1f'),
    'app_key': env.get('APP_KEY', '3e3811ed4d0c948fdba9'),
    'Content-type': 'application/json'
}

params = urllib.parse.urlencode({})


def adjustTrace(json_object):
    new_object = {"x": [], "y": []}

    for x in json_object["strokes"]:
        x_list = []
        y_list = []
        for i, item in enumerate(x["points"].split(",")):
            if i % 2 == 0:
                x_list.append(int(float(item)))
            else:
                y_list.append(int(float(item)))
        assert len(x_list) == len(y_list)
        new_object["x"].append(x_list)
        new_object["y"].append(y_list)

    return {"strokes": {"strokes": new_object}}


def deal_single_file(parent, filename, error_file, result_file):
    try:
        path = os.path.join(parent, filename)
        test_str = json.load(
            open(path, "r"))

        print(str(test_str))

        new_trace = adjustTrace(test_str)

        r = requests.post("https://api.mathpix.com/v3/strokes",
                          data=json.dumps(new_trace), headers=headers, timeout=30)

        result = json.loads(r.text)
        print(result)
        result_file.write(filename)
        result_file.write("\n")
        result_file.write(json.dumps(result))
        result_file.write("\n")
        result_file.flush()

    except Exception as e:
        error_message = re.sub("\n+", "\t", traceback.format_exc())
        print(error_message)
        error_file.write(filename)
        error_file.write("\n")
        error_file.write(error_message)
        error_file.write("\n")
        error_file.flush()


####################################

FLAG = "yunbi"
input_file = "/Users/liuyongjie/Desktop/test_data/" + FLAG
error_file = open("mathpix_" + FLAG + "_error.txt", "w")
result_file = open("mathpix_" + FLAG + "_result.txt", "w")

if __name__ == "__main__":
    for parent, dirnames, filenames in os.walk(input_file, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if file_path[-5:] == ".json":
                deal_single_file(parent, filename, error_file, result_file)
error_file.close()
result_file.close()

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import ssl
import json
import os
import traceback
import re
import time

ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    # Request headers
    'x-ms-client-request-id': '1',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '0d6c433975e44841a122acfa3a49c918',
}

params = urllib.parse.urlencode({})


def deal_single_file(parent, filename, error_file, result_file):
    try:
        path = os.path.join(parent, filename)
        test_str = json.load(
            open(path, "r"))
        # test_str.pop("unit")
        test_str["language"] = "en-US"
        # print(str(test_str))
        conn = http.client.HTTPSConnection('nihao.cognitiveservices.azure.com')
        conn.request("PUT", "/inkrecognizer/v1.0-preview/recognize?%s" % params,
                     json.dumps(test_str).encode("utf-8"),
                     # "{\"version\":1,\"language\":\"en-US\",\"strokes\":[{\"id\":183,\"points\":\"11.89084,21.69333,11.84664,21.69333,11.74365,21.69333,11.58458,21.69333,11.3769,21.69333,11.13603,21.69333,10.91951,21.73753,10.70778,21.79632,10.53443,21.8966,10.40975,22.04479,10.33059,22.23934,10.28765,22.46819,10.27013,22.71949,10.26828,22.98349,10.2746,23.25317,10.28391,23.52744,10.29315,23.80157,10.34497,24.02904,10.45348,24.1945,10.66368,24.34503,10.9332,24.46251,11.27836,24.54349,11.64686,24.59245,12.00858,24.61708,12.34962,24.62536,12.66655,24.57985,12.91754,24.47099,13.09289,24.30136,13.20062,24.08598,13.25622,23.84014,13.2763,23.57667,13.27521,23.25736,13.26372,22.92023,13.24898,22.58729,13.19093,22.31304,13.07688,22.11477,12.91003,21.98819,12.65335,21.91897,12.35118,21.89021,12.03343,21.88656,11.76191,21.89608\",\"language\":\"en-US\"}]}",
                     headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        # print(data)
        result_file.write(filename)
        result_file.write("\n")
        result_file.write(data)
        result_file.write("\n")
        result_file.flush()
        conn.close()
    except Exception as e:
        error_message = re.sub("\n+", "\t", traceback.format_exc())
        # print(error_message)
        error_file.write(filename)
        error_file.write("\n")
        error_file.write(error_message)
        error_file.write("\n")
        error_file.flush()


def deal_fanti_file(parent, filename, error_file, result_file):
    try:
        path = os.path.join(parent, filename)
        test_str = json.load(open(path, "r"))

        result = []

        for x in test_str["events"]:

            assert len(x["x"]) == len(x["y"])
            temp_dict = {}
            temp_str = ""
            for i, c_x in enumerate(x["x"]):
                temp_str += str(x["x"][i]) + "," + str(x["y"][i])
                if i != len(x["x"]) - 1:
                    temp_str += ","
            temp_dict = {"points": temp_str, "id": len(result)}
            result.append(temp_dict)

        new_test_str = {"version": 1,
                        "unit": "mm",
                        "language": "zh-TW",
                        "strokes": result

                        }
        test_str = new_test_str
        test_str["language"] = "zh-TW"
        # print(str(test_str))
        conn = http.client.HTTPSConnection('nihao.cognitiveservices.azure.com')
        conn.request("PUT", "/inkrecognizer/v1.0-preview/recognize?%s" % params,
                     json.dumps(test_str).encode("utf-8"),
                     # "{\"version\":1,\"language\":\"en-US\",\"strokes\":[{\"id\":183,\"points\":\"11.89084,21.69333,11.84664,21.69333,11.74365,21.69333,11.58458,21.69333,11.3769,21.69333,11.13603,21.69333,10.91951,21.73753,10.70778,21.79632,10.53443,21.8966,10.40975,22.04479,10.33059,22.23934,10.28765,22.46819,10.27013,22.71949,10.26828,22.98349,10.2746,23.25317,10.28391,23.52744,10.29315,23.80157,10.34497,24.02904,10.45348,24.1945,10.66368,24.34503,10.9332,24.46251,11.27836,24.54349,11.64686,24.59245,12.00858,24.61708,12.34962,24.62536,12.66655,24.57985,12.91754,24.47099,13.09289,24.30136,13.20062,24.08598,13.25622,23.84014,13.2763,23.57667,13.27521,23.25736,13.26372,22.92023,13.24898,22.58729,13.19093,22.31304,13.07688,22.11477,12.91003,21.98819,12.65335,21.91897,12.35118,21.89021,12.03343,21.88656,11.76191,21.89608\",\"language\":\"en-US\"}]}",
                     headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        # print(data)
        result_file.write(filename)
        result_file.write("\n")
        result_file.write(data)
        result_file.write("\n")
        result_file.flush()
        conn.close()
    except Exception as e:
        error_message = re.sub("\n+", "\t", traceback.format_exc())
        # print(error_message)
        error_file.write(filename)
        error_file.write("\n")
        error_file.write(error_message)
        error_file.write("\n")
        error_file.flush()


####################################

FLAG = "ms_page"
# input_file = "./" + FLAG
input_path = "/Users/liuyongjie/Desktop/test_data/problem"
error_file = open(FLAG + "_en_error.txt", "w")
result_file = open(FLAG + "_en_result.txt", "w")
count = 0
if __name__ == "__main__":
    for parent, dirnames, filenames in os.walk(input_path, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if file_path[-5:] == ".json":
                print(file_path)
                start = time.time()
                # 中间是循环程序
                deal_fanti_file(parent, filename, error_file, result_file)
                end = time.time()
                print("Runtime is ：", end - start)
                if count % 5 == 0 and count != 0:
                    time.sleep(60)
                count += 1
error_file.close()
result_file.close()

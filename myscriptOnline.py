import os
import json
import requests
import hmac
import hashlib
import traceback
import re
import time


class PointEvent:
    x = 0.0
    y = 0.0
    eventType = None


def loadPointerEvents(json_object):
    result = []

    for x in json_object["strokes"]:
        x_list = []
        y_list = []
        if len(x["points"]) == 0:
            continue
        for i, item in enumerate(x["points"].split(",")):
            if i % 2 == 0:
                x_list.append(int(float(item)))
            else:
                y_list.append(int(float(item)))
        assert len(x_list) == len(y_list)

        pointevents = []

        for i, x in enumerate(x_list):
            a = PointEvent()
            a.x = x_list[i]
            a.y = y_list[i]
            if i == 0:
                a.eventType = "DOWN"
            elif i == len(x_list) - 1:
                a.eventType = "UP"
            else:
                a.eventType = "MOVE";
            pointevents.append(a);

        result.append(pointevents);
    return result


def loadYunbiPointerEvents(json_object):
    result = []

    for x in json_object["events"]:

        assert len(x["x"]) == len(x["y"])
        pointevents = []

        for i, c_x in enumerate(x["x"]):
            a = PointEvent()
            a.x = x["x"][i]
            a.y = x["y"][i]
            if i == 0:
                a.eventType = "DOWN"
            elif i == len(x["x"]) - 1:
                a.eventType = "UP"
            else:
                a.eventType = "MOVE"
            pointevents.append(a)

        result.append(pointevents)
    return result


FLAG = "ms_page"
# input_file = "/Users/liuyongjie/Desktop/test_data/" + FLAG
input_file = "/Users/liuyongjie/Desktop/test_data/problem"
error_file = open("myscript_" + FLAG + "_error.txt", "w")
result_file = open("myscript_" + FLAG + "_result.txt", "w")
count = 0

if __name__ == "__main__":
    for parent, dirnames, filenames in os.walk(input_file, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if file_path[-5:] == ".json":
                start = time.time()
                print(file_path)
                temp = json.load(open(file_path, "r"))
                bigPointerEvents = loadYunbiPointerEvents(temp)
                sign = 0

                # ==================================保证每个DOWN会有每个UP=====================================
                new_bigPointerEvents = []
                new_PointerEvents = []
                for i, x in enumerate(bigPointerEvents):
                    for j, y in enumerate(x):
                        now_iteration = y
                        if now_iteration.eventType == "DOWN":
                            sign -= 1
                            new_PointerEvents = []
                            new_PointerEvents.append(now_iteration)
                            if (sign != -1):
                                sign = -1
                        if now_iteration.eventType == "UP":
                            sign += 1
                            if sign == 0:
                                new_PointerEvents.append(now_iteration)
                                new_bigPointerEvents.append(new_PointerEvents)
                        if now_iteration.eventType == "MOVE":
                            if sign == -1:
                                new_PointerEvents.append(now_iteration)

                # =======================================================================

                changeContent = "\"components\": ["
                for i, stroke in enumerate(new_bigPointerEvents):
                    changeContent += "{\"y\":["
                    for j, p in enumerate(stroke):
                        changeContent += str(p.y)
                        changeContent += ","

                    changeContent = changeContent[0: len(changeContent) - 1]
                    changeContent += "],\"x\":["
                    for j, p in enumerate(stroke):
                        changeContent += str(p.x)
                        changeContent += ","
                    changeContent = changeContent[0: len(changeContent) - 1]
                    changeContent += "],\"type\": \"stroke\"},"

                changeContent = changeContent[0: len(changeContent) - 1]
                changeContent += "]}]"

                #                 发送请求

                recognitionCloudURL = "https://cloud.myscript.com"
                applicationKey = "4c379c73-99c0-4bfa-9f9d-50218f4b9a2f"
                hmacKey = "30de046c-df7c-4376-9641-488b2f93d4e4"
                textInput = "{\"inputUnits\": [{\"textInputType\": \"MULTI_LINE_TEXT\", " + changeContent + ", \"textParameter\": {\"contentTypes\": [\"text\"], \"textInputMode\": \"CURSIVE\", \"language\": \"zh_CN\"}}"
                in_textInput = textInput
                if not isinstance(in_textInput, bytes):  # Python 3
                    in_textInput = in_textInput.encode('latin1')
                in_c = applicationKey + hmacKey
                if not isinstance(in_c, bytes):  # Python 3
                    in_c = in_c.encode('latin1')
                computedHmac = hmac.new(in_c, in_textInput, digestmod=hashlib.sha512).hexdigest()

                headers = {
                    # Request headers
                    'Content-type': 'application/x-www-form-urlencoded',
                }

                FormData = {
                    'applicationKey': applicationKey,
                    "textInput": textInput,
                    "hmac": computedHmac
                }

                try:
                    end1 = time.time()

                    # 中间是循环程序
                    r = requests.post(recognitionCloudURL + "/api/v3.0/recognition/rest/text/doSimpleRecognition.json",
                                      data=FormData, headers=headers, timeout=30)
                    end2 = time.time()
                    print("single Runtime is ：", end2 - start)
                    print("response Runtime is ：", end2 - end1)
                except:
                    error_message = re.sub("\n+", "\t", traceback.format_exc())
                    print(error_message)
                    error_file.write(filename)
                    error_file.write("\n")
                    error_file.write(error_message)
                    error_file.write("\n")
                    error_file.flush()
                print(r.content.decode("utf-8"))

                result_file.write(filename)
                result_file.write("\n")
                result_file.write(r.content.decode("utf-8"))
                result_file.write("\n")
                result_file.flush()

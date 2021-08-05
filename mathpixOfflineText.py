#!/usr/bin/env python3
import os
import time
import base64
import requests
import json

#
# Simple example of calling Mathpix OCR with ../images/algebra.jpg.
#
# We use the default ocr (math-only) and a single return format, latex_simplified.
#
# If you expect the image to be math and want to examine the result
# as math then the return format should either be latex_simplified,
# asciimath, or mathml. If you want to see the text in the image then
# you should include 'ocr': ['math', 'text'] as an argument and
# the return format should be either text or latex_styled
# (depending on whether you want to use the result as a paragraph or an equation).


# input_path = "/Users/liuyongjie/Desktop/off_image_test_2"
# o = open("pull_pic_result.txt", "w")
# total = 0
# error = 0
# for parent, dirnames, filenames in os.walk(input_path, followlinks=True):
#     for filename in filenames:
#         file_path = os.path.join(parent, filename)
#         if file_path[-4:] == ".bmp":
#             print('文件名：%s' % filename)
#             print('文件完整路径：%s\n' % file_path)
#
#             if "error" in r:
#                 error += 1
#             else:
#                 o.write(filename)
#                 o.write("\t")
#                 o.write(r["latex_simplified"])
#                 o.write("\n")
#                 o.flush()
#             time.sleep(1)
#             total += 1
# o.close()


# put desired file path here
file_path = '/Users/liuyongjie/pycharm/conbinationData/mix_data/test_pic/combinated1_68-2-urs-phoneyd.2df74559cc864352a@163.com_0.json.jpg'
image_uri = "data:image/jpg;base64," + base64.b64encode(open(file_path, "rb").read()).decode()
r = requests.post("https://api.mathpix.com/v3/text",
                  data=json.dumps({'src': image_uri}),
                  headers={"app_id": "yaminoryu_foxmail_com_02ed1f", "app_key": "3e3811ed4d0c948fdba9",
                           "Content-type": "application/json"})
print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))

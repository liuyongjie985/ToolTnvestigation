#!/usr/bin/env python3
import os
import mathpix
import time
import traceback
import re

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


input_path = "/Users/liuyongjie/pycharm/math_mix_pic/"
error_file = open("mix_error.txt", "w")
result_file = open("mix_result.txt", "w")
total = 0
error = 0
for parent, dirnames, filenames in os.walk(input_path, followlinks=True):
    for filename in filenames:
        file_path = os.path.join(parent, filename)
        if file_path[-4:] == ".png":
            print('文件名：%s' % filename)
            print('文件完整路径：%s\n' % file_path)
            try:
                r = mathpix.latex({'src': mathpix.image_uri(file_path),
                                   'formats': ['latex_simplified'],
                                   "skip_recrop": True,
                                   "ocr": ["math", "text"]})
                if "error" in r:
                    error_file.write(filename)
                    error_file.write("\n")
                    error_file.write(str(r))
                    error_file.write("\n")
                    error_file.flush()
                else:
                    result_file.write(filename)
                    result_file.write("\n")
                    result_file.write(r["latex_simplified"])
                    result_file.write("\n")
                    result_file.flush()
                time.sleep(1)
                total += 1
            except:
                error_message = re.sub("\n+", "\t", traceback.format_exc())
                print(error_message)
                error_file.write(filename)
                error_file.write("\n")
                error_file.write(error_message)
                error_file.write("\n")
                error_file.flush()
result_file.close()

print("出错文件：", error)
print("总文件：", total)
print("错误率：", error / total)

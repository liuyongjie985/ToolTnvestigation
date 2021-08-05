import base64
import requests
import json
import os
import re
import time

if __name__ == "__main__":
    FLAG = "ms_page"
    # input_path = "/Users/liuyongjie/Desktop/test_data/problem"
    input_path = "/Users/liuyongjie/Desktop/test_data/" + FLAG + "_pic"
    TEXT = False
    if TEXT:
        output_path = "/Users/liuyongjie/Desktop/test_data/" + FLAG + "_pic_text_rest_result"
    else:
        output_path = "/Users/liuyongjie/Desktop/test_data/" + FLAG + "_pic_document_rest_result"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for parent, dirnames, filenames in os.walk(input_path, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if filename[-4:] == ".png" or filename[-4:] == ".jpg":
                image_uri = base64.b64encode(open(file_path, "rb").read()).decode()
                send_dict = {"requests": [
                    {
                        "image": {
                            "content": image_uri
                        },
                        "features": [
                            {
                                "type": "TEXT_DETECTION"
                            }
                        ],
                        "imageContext": {
                            "languageHints": ["en-US", "zh-Hans"]
                        },

                    }
                ]}
                temp_o = open(re.sub(".jpg", "", re.sub(".png", "", os.path.join(output_path, filename))) + ".result",
                              "w")
                start = time.time()
                r = requests.post(
                    "https://vision.googleapis.com/v1/images:annotate?key=AIzaSyA8H8KMr-qW9D_E1v_s8CppZhVA5dPuibI",
                    data=json.dumps(send_dict),
                    headers={"Content-type": "application/json"})
                end = time.time()
                print("耗时:" + str(end - start))
                temp_o.write("耗时:" + str(end - start) + "\n")

                response = json.loads(r.text)
                assert len(response["responses"]) == 1
                if not TEXT:

                    for page in response["responses"][0]["fullTextAnnotation"]["pages"]:
                        for block in page["blocks"]:
                            print(
                                '\nBlock confidence: {}\n'.format(
                                    block["confidence"] if "confidence" in block else "None"))
                            temp_o.write('\nBlock confidence: {}\n'.format(
                                block["confidence"] if "confidence" in block else "None") + "\n")
                            for paragraph in block["paragraphs"]:
                                print('Paragraph confidence: {}'.format(
                                    paragraph["confidence"] if "confidence" in paragraph else "None"))
                                temp_o.write('Paragraph confidence: {}'.format(
                                    paragraph["confidence"] if "confidence" in paragraph else "None") + "\n")
                                for word in paragraph["words"]:
                                    word_text = ''.join([
                                        symbol["text"] for symbol in word["symbols"]
                                    ])
                                    print('Word text: {} (confidence: {})'.format(
                                        word_text, word["confidence"] if "confidence" in word else "None"))
                                    temp_o.write('Word text: {} (confidence: {})'.format(
                                        word_text, word["confidence"] if "confidence" in word else "None") + "\n")
                                    for symbol in word["symbols"]:
                                        print('\tSymbol: {} (confidence: {})'.format(
                                            symbol["text"], symbol["confidence"] if "confidence" in symbol else "None"))
                                        temp_o.write('\tSymbol: {} (confidence: {})'.format(
                                            symbol["text"],
                                            symbol["confidence"] if "confidence" in symbol else "None") + "\n")
                else:
                    texts = response["responses"][0]["textAnnotations"]
                    print('Texts:')
                    temp_o.write("Texts:\n")

                    for text in texts:
                        print('\n"{}"'.format(text["description"]))
                        vertices = (['({},{})'.format(vertex["x"] if "x" in vertex else "None",
                                                      vertex["y"] if "y" in vertex else "None")
                                     for vertex in text["boundingPoly"]["vertices"]])

                        print('bounds: {}'.format(','.join(vertices)))
                        temp_o.write('\n"{}"'.format(text["description"]) + "\n")
                        temp_o.write('bounds: {}'.format(','.join(vertices)) + "\n")
                    temp_o.close()
                temp_o.close()
                if "error" in response["responses"][0]:
                    raise Exception(
                        '{}\nFor more info on error messages, check: '
                        'https://cloud.google.com/apis/design/errors'.format(
                            response["responses"][0]["error"]["message"]))

                # print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))

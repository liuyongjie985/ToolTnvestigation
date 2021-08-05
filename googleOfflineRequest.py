from google.cloud import vision
import io
import time
import os
import re


def detect_document(parent, filename, output_path):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()
    path = os.path.join(parent, filename)
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    temp_o = open(re.sub(".jpg", "", re.sub(".png", "", os.path.join(output_path, filename))) + ".result", "w")

    image = vision.types.Image(content=content)
    start = time.time()
    response = client.document_text_detection(image=image)
    end = time.time()
    print("耗时:" + str(end - start))
    temp_o.write("耗时:" + str(end - start) + "\n")
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))
            temp_o.write('\nBlock confidence: {}\n'.format(block.confidence) + "\n")
            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))
                temp_o.write('Paragraph confidence: {}'.format(
                    paragraph.confidence) + "\n")
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))
                    temp_o.write('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence) + "\n")
                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))
                        temp_o.write('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence) + "\n")
    temp_o.close()
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def detect_text(parent, filename, output_path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()
    path = os.path.join(parent, filename)
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    temp_o = open(re.sub(".jpg", "", re.sub(".png", "", os.path.join(output_path, filename))) + ".result", "w")
    start = time.time()
    response = client.text_detection(image=image)
    end = time.time()
    print("耗时:" + str(end - start))
    temp_o.write("耗时:" + str(end - start) + "\n")
    texts = response.text_annotations
    print('Texts:')
    temp_o.write("Texts:\n")

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
        temp_o.write('\n"{}"'.format(text.description) + "\n")
        temp_o.write('bounds: {}'.format(','.join(vertices)) + "\n")
    temp_o.close()
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


# input_path = "./lines_vis/0743D2C44A5C49BEAAA8F693E7ECC40B_109.json.jpg"
# detect_document(input_path)
# output_path = "/Users/liuyongjie/Desktop/shiqi_example/page_result"
#
# if not os.path.exists(output_path):
#     os.makedirs(output_path)
#
# detect_text("/Users/liuyongjie/Desktop/shiqi_example/", "0743D2C44A5C49BEAAA8F693E7ECC40B_109.json.jpg", output_path)
FLAG = "ms_page"
# input_path = "/Users/liuyongjie/Desktop/test_data/problem"
input_path = "/Users/liuyongjie/Desktop/test_data/" + FLAG + "_pic"
TEXT = False
if TEXT:
    output_path = "/Users/liuyongjie/Desktop/test_data/" + FLAG + "_pic_text_result"
else:
    output_path = "/Users/liuyongjie/Desktop/test_data/" + FLAG + "_pic_document_result"

if not os.path.exists(output_path):
    os.makedirs(output_path)

for parent, dirnames, filenames in os.walk(input_path, followlinks=True):
    for filename in filenames:
        file_path = os.path.join(parent, filename)
        if filename[-4:] == ".png" or filename[-4:] == ".jpg":
            if TEXT:
                detect_text(parent, filename, output_path)
            else:
                detect_document(parent, filename, output_path)

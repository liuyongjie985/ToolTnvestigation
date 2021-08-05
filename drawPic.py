import numpy as np
import cv2
import os
import json

'''
加载test_data里的数据，把ms_page渲染成图片

'''


def getFourDimension(traceid2xy):
    max_x = -1
    max_y = -1
    min_x = 99999999999
    min_y = 99999999999
    # print("修复涂改之后")
    for trace in traceid2xy:
        for i, xy in enumerate(trace):
            x = float(xy[0])
            y = float(xy[1])
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x
            if y > max_y:
                max_y = y
            if y < min_y:
                min_y = y
    return max_x, max_y, min_x, min_y


def scaleTrace(traceid2xy):
    max_x, max_y, min_x, min_y = getFourDimension(traceid2xy)
    origin_scale = (max_x - min_x) / (float(max_y - min_y) + 1e-8)
    print_traceid2xy, max_x, max_y, min_x, min_y = subScaleTrace(origin_scale, traceid2xy, max_x, max_y, min_x, min_y)
    return print_traceid2xy, max_x, max_y, min_x, min_y


def subScaleTrace(origin_scale, traceid2xy, max_x, max_y, min_x, min_y):
    # 长过长截
    while (max_x - min_x) > 2116:
        new_traceid2xy = []
        scale = 1.1
        max_x = -1
        max_y = -1
        min_x = 99999999999
        min_y = 99999999999

        for i, x in enumerate(traceid2xy):
            temp_list = []
            for j, y in enumerate(x):
                temp_list.append([y[0] / scale, y[1]])
                if y[0] / scale > max_x:
                    max_x = y[0] / scale
                if y[1] > max_y:
                    max_y = y[1]
                if y[0] / scale < min_x:
                    min_x = y[0] / scale
                if y[1] < min_y:
                    min_y = y[1]
            new_traceid2xy.append(temp_list)
        traceid2xy = new_traceid2xy
    # 长过短扩
    while (max_x - min_x) < 54:
        new_traceid2xy = []
        scale = 0.9
        max_x = -1
        max_y = -1
        min_x = 99999999999
        min_y = 99999999999

        for i, x in enumerate(traceid2xy):
            temp_list = []
            for j, y in enumerate(x):
                temp_list.append([y[0] / scale, y[1]])
                if y[0] / scale > max_x:
                    max_x = y[0] / scale
                if y[1] > max_y:
                    max_y = y[1]
                if y[0] / scale < min_x:
                    min_x = y[0] / scale
                if y[1] < min_y:
                    min_y = y[1]
            new_traceid2xy.append(temp_list)
        traceid2xy = new_traceid2xy
    # 高过长截
    while (max_y - min_y) > 481:
        new_traceid2xy = []
        scale = 1.1
        max_x = -1
        max_y = -1
        min_x = 99999999999
        min_y = 99999999999

        for i, x in enumerate(traceid2xy):
            temp_list = []
            for j, y in enumerate(x):
                temp_list.append([y[0], y[1] / scale])
                if y[0] > max_x:
                    max_x = y[0]
                if y[1] / scale > max_y:
                    max_y = y[1] / scale
                if y[0] < min_x:
                    min_x = y[0]
                if y[1] / scale < min_y:
                    min_y = y[1] / scale
            new_traceid2xy.append(temp_list)
        traceid2xy = new_traceid2xy

    # 高过短扩
    while (max_y - min_y) < 54:
        new_traceid2xy = []
        scale = 0.9
        max_x = -1
        max_y = -1
        min_x = 99999999999
        min_y = 99999999999

        for i, x in enumerate(traceid2xy):
            temp_list = []
            for j, y in enumerate(x):
                temp_list.append([y[0], y[1] / scale])
                if y[0] > max_x:
                    max_x = y[0]
                if y[1] / scale > max_y:
                    max_y = y[1] / scale
                if y[0] < min_x:
                    min_x = y[0]
                if y[1] / scale < min_y:
                    min_y = y[1] / scale
            new_traceid2xy.append(temp_list)
        traceid2xy = new_traceid2xy
    # 保证竖图要有以前竖，横图要有以前横
    # 如果原先是横图,将其长扩长
    if origin_scale > 1:
        pass
        while float(max_x - min_x) / (max_y - min_y) < origin_scale:
            new_traceid2xy = []
            scale = 0.9
            max_x = -1
            max_y = -1
            min_x = 99999999999
            min_y = 99999999999

            for i, x in enumerate(traceid2xy):
                temp_list = []
                for j, y in enumerate(x):
                    temp_list.append([y[0] / scale, y[1]])
                    if y[0] / scale > max_x:
                        max_x = y[0] / scale
                    if y[1] > max_y:
                        max_y = y[1]
                    if y[0] / scale < min_x:
                        min_x = y[0] / scale
                    if y[1] < min_y:
                        min_y = y[1]
                new_traceid2xy.append(temp_list)
            traceid2xy = new_traceid2xy
    else:
        # 如果原先是横图,将其高扩高
        while float(max_x - min_x) / (max_y - min_y) > origin_scale:
            new_traceid2xy = []
            scale = 0.9
            max_x = -1
            max_y = -1
            min_x = 99999999999
            min_y = 99999999999

            for i, x in enumerate(traceid2xy):
                temp_list = []
                for j, y in enumerate(x):
                    temp_list.append([y[0], y[1] / scale])
                    if y[0] > max_x:
                        max_x = y[0]
                    if y[1] / scale > max_y:
                        max_y = y[1] / scale
                    if y[0] < min_x:
                        min_x = y[0]
                    if y[1] / scale < min_y:
                        min_y = y[1] / scale
                new_traceid2xy.append(temp_list)
            traceid2xy = new_traceid2xy
            # 对于高度过于高的，缩放比例至1：1
        if (max_x - min_x) / (max_y - min_y) < 0.2:
            while (max_x - min_x) / (max_y - min_y) < 0.5:
                new_traceid2xy = []
                scale = 1.1
                max_x = -1
                max_y = -1
                min_x = 99999999999
                min_y = 99999999999

                for i, x in enumerate(traceid2xy):
                    temp_list = []
                    for j, y in enumerate(x):
                        temp_list.append([y[0], y[1] / scale])
                        if y[0] > max_x:
                            max_x = y[0]
                        if y[1] / scale > max_y:
                            max_y = y[1] / scale
                        if y[0] < min_x:
                            min_x = y[0]
                        if y[1] / scale < min_y:
                            min_y = y[1] / scale
                    new_traceid2xy.append(temp_list)
                traceid2xy = new_traceid2xy
    # # 对其大小也要限制,2009*183是作者最大的图，放缩到20kb
    # while (max_x - min_x) * (max_y - min_y) > 632 * 156 and (max_x - min_x) > 60 and (max_y - min_y) > 60:
    #     new_traceid2xy = []
    #     scale = 1.1
    #     max_x = -1
    #     max_y = -1
    #     min_x = 99999999999
    #     min_y = 99999999999
    #
    #     for i, x in enumerate(traceid2xy):
    #         temp_list = []
    #         for j, y in enumerate(x):
    #             temp_list.append([y[0] / scale, y[1] / scale])
    #             if y[0] / scale > max_x:
    #                 max_x = y[0] / scale
    #             if y[1] / scale > max_y:
    #                 max_y = y[1] / scale
    #             if y[0] / scale < min_x:
    #                 min_x = y[0] / scale
    #             if y[1] / scale < min_y:
    #                 min_y = y[1] / scale
    #         new_traceid2xy.append(temp_list)
    #     traceid2xy = new_traceid2xy

    return traceid2xy, max_x, max_y, min_x, min_y


# 输入是三维矩阵
# [ [[1,6],[5,7],[2,7],[9,0]],
#   [[1,6],[5,7],[2,7],[9,0]],
#   [[1,6],[5,7],[2,7],[9,0]] ]

def z_score(traceid2xy):
    u_x_numerator = 0
    u_x_denominator = 0
    u_y_numerator = 0
    u_y_denominator = 0
    for i, x in enumerate(traceid2xy):
        for j, y in enumerate(x):
            if j == 0:
                continue
            L = ((y[0] - x[j - 1][0]) ** 2 + (y[1] - x[j - 1][1]) ** 2) ** 0.5
            u_x_numerator += L * (y[0] + x[j - 1][0]) / 2
            u_x_denominator += L
            u_y_numerator += L * (y[1] + x[j - 1][1]) / 2
            u_y_denominator += L
    u_x = u_x_numerator / u_x_denominator
    u_y = u_y_numerator / u_y_denominator
    delta_x_numerator = 0
    delta_x_denominator = 0
    for i, x in enumerate(traceid2xy):
        for j, y in enumerate(x):
            if j == 0:
                continue
            L = ((y[0] - x[j - 1][0]) ** 2 + (y[1] - x[j - 1][1]) ** 2) ** 0.5
            delta_x_numerator += L / 3 * (
                    (y[0] - u_x) ** 2 + (x[j - 1][0] - u_x) ** 2 + (x[j - 1][0] - u_x) * (y[0] - u_x))
            delta_x_denominator += L

    delta_x = (delta_x_numerator / delta_x_denominator) ** 0.5

    new_traceid2xy = []
    count_x = 0
    count_y = 0
    count = 0
    for i, x in enumerate(traceid2xy):
        temp = []
        for j, y in enumerate(x):
            temp.append([(y[0] - u_x) / delta_x, (y[1] - u_y) / delta_x])
            count_x += (y[0] - u_x) / delta_x
            count_y += (y[1] - u_y) / delta_x
            count += 1
        new_traceid2xy.append(temp)
    avg_x = count_x / count
    avg_y = count_y / count
    return new_traceid2xy, avg_x, avg_y


'''
计算T_cos与T_dis，去除多余点，以每个笔画为单位
'''


def rve_duplicate(traceid2xy, T_dis, T_cos):
    count = 0
    for i, x in enumerate(traceid2xy):
        j = 0
        while j < len(x):
            if j == 0:
                # temp_list.append([x[j][0], x[j][1], x[j][2], x[j][3]])
                j += 1
                continue
            real_dis = ((x[j][0] - x[j - 1][0]) ** 2 + (x[j][1] - x[j - 1][1]) ** 2) ** 0.5
            if not real_dis < T_dis:
                # temp_list.append([x[j][0], x[j][1], x[j][2], x[j][3]])
                j += 1
            else:
                if j != len(x) - 1:
                    x.pop(j)
                else:
                    j += 1

                count += 1
    for i, x in enumerate(traceid2xy):
        j = 0
        while j < len(x):
            if j == 0 or j == len(x) - 1:
                j += 1
                continue
            if (((x[j][0] - x[j - 1][0]) ** 2 + (x[j][1] - x[j - 1][1]) ** 2) ** 0.5 * (
                    ((x[j + 1][0] - x[j][0]) ** 2 + (x[j + 1][1] - x[j][1]) ** 2) ** 0.5)) == 0:
                j += 1
                continue
            real_cos = abs(
                ((x[j][0] - x[j - 1][0]) * (x[j + 1][0] - x[j][0]) + (x[j][1] - x[j - 1][1]) * (
                        x[j + 1][1] - x[j][1])) / (
                        ((x[j][0] - x[j - 1][0]) ** 2 + (x[j][1] - x[j - 1][1]) ** 2) ** 0.5 * (
                        ((x[j + 1][0] - x[j][0]) ** 2 + (x[j + 1][1] - x[j][1]) ** 2) ** 0.5)))
            if not real_cos < T_cos:
                j += 1
            else:
                x.pop(j)
                count += 1
    return traceid2xy, count


'''
按照trace把公式图片画出来
'''

SCALE = 1


def drawPictureByTrace(traceid2xy, filename, pic_output_path, min_x, min_y, max_x, max_y):
    img_ = np.full((int((max_y - min_y) * SCALE) + 1, int((max_x - min_x) * SCALE) + 1, 3), (255, 255, 255), np.uint8)
    for i, x in enumerate(traceid2xy):
        for j, y in enumerate(x):
            if j == 0:
                continue

            cv2.line(img_, (
                int((x[j - 1][0] - min_x) + (SCALE - 1) / 2 * (max_x - min_x)),
                int(x[j - 1][1] - min_y + (SCALE - 1) / 2 * (max_y - min_y))),
                     (int(y[0] - min_x + (SCALE - 1) / 2 * (max_x - min_x)),
                      int(y[1] - min_y + (SCALE - 1) / 2 * (max_y - min_y))), (0, 0, 0), 2)

    cv2.imwrite(pic_output_path + "/" + filename + ".jpg", img_)
    print("save " + pic_output_path + "/" + filename + ".jpg")


if __name__ == "__main__":
    ZSCORE = False
    # FLAG = "ms_page"
    input_path = "/Users/liuyongjie/update/output_data/mix_data/on-ascii-test"
    pic_output_path = "/Users/liuyongjie/update/output_data/mix_data/on-ascii-test-pic"

    if not os.path.exists(pic_output_path):
        os.makedirs(pic_output_path)

    for parent, dirnames, filenames in os.walk(input_path, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            if file_path[-5:] == "ascii":
                temp = json.load(open(file_path, "r"))
                v = []

                for x in temp["strokes"]:
                    temp_list = []
                    if len(x["points"]) == 0:
                        continue
                    x_y_list = []
                    for i, item in enumerate(x["points"].split(",")):

                        if i % 2 == 0:
                            x_y_list.append(float(item))
                        else:
                            x_y_list.append(float(item))
                            assert len(x_y_list) == 2
                            temp_list.append(x_y_list)
                            x_y_list = []

                    v.append(temp_list)

                if ZSCORE:
                    traceid2xy, avg_x, avg_y = z_score(v)
                    traceid2xy, remove_point = rve_duplicate(traceid2xy, .017, -999999)
                    v = traceid2xy
                print_traceid2xy, temp_max_x, temp_max_y, temp_min_x, temp_min_y = scaleTrace(v)
                drawPictureByTrace(print_traceid2xy, filename[:-5],
                                   pic_output_path,
                                   temp_min_x, temp_min_y,
                                   temp_max_x,
                                   temp_max_y)

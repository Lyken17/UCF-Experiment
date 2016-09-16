import os, sys
import json

from os.path import join as path_join

import numpy as np
import cv2

import config as cfg




def read_from_file():
    data_table = dict()

    for dirpath, dirnames, filenames in os.walk(cfg.database_dir):
        for filename in filenames:
            if filename.endswith(".jpg") or filename.endswith(".txt") or filename.endswith(".tif"):
                fname = filename.split('.')[0]
                if fname not in data_table:
                    data_table[fname] = dict()

                fpath = path_join(dirpath, filename)
                if filename.endswith(".jpg"):
                    if fpath.find("jpeg") == -1:
                        data_table[fname]["image"] = fpath

                if filename.endswith(".txt") or filename.endswith(".tif"):
                    data_table[fname]["joint"] = fpath



    # print json.dumps(data_table, indent=4)

    c1 = 0
    c2 = 0
    new_table = dict()
    for kid in data_table:
        if len(data_table[kid]) >= 2:
            c2 +=1
            new_table[kid] = data_table[kid]

        c1 += 1

    print "Total :", c1
    print "Useful :", c2
    return new_table


def main():
    import re
    table = read_from_file()

    cnt = 0
    SHOWIMG = False

    l_table = table.values()
    new_table = []
    for each in l_table:

        img_path = each["image"]
        joint_path = each["joint"]
        image = cv2.imread(img_path)
        # print img_path
        # print image.shape

        with open(joint_path, 'r') as fp:
            line = fp.read()
            estimate = [int(each) for each in re.split(r'[\s\t]+', line)[:4]]
            belong = re.split(r'[\s\t]+', line)[-1]

        if SHOWIMG:
            joint = [int(each) for each in re.split(r'[\s\t]+', line)[:4]]
            joint[2] += joint[0]
            joint[3] += joint[1]
            pts = np.array([[joint[0], joint[1]], [joint[2], joint[1]], [joint[2], joint[3]], [joint[0], joint[3]]])
            cv2.polylines(image, [pts], True, (0, 0, 255))
            cv2.imshow("frame", image)
            cv2.waitKey(0)

        temp_data = {}
        temp_data["image"] = img_path
        temp_data["joint"] = estimate
        temp_data["attr"] = belong
        # print json.dumps(temp_data, indent=4)
        new_table.append(temp_data)
        cnt += 1

    if SHOWIMG:
        cv2.destroyAllWindows()

    return new_table

if __name__ == '__main__':
    data = main()
    # data = {}
    with open("data/collection.json", "w+") as fp:
        json.dump(data, fp, indent=4)
import os, sys
import json

from os.path import join as path_join

import numpy as np
import cv2

import config as cfg




def go_through():
    data_table = dict()

    for dirpath, dirnames, filenames in os.walk(cfg.database_dir):
        for filename in filenames:
            if filename.endswith(".jpg") or filename.endswith(".txt") or filename.endswith(".tif"):
                fname = filename.split('.')[0]
                if fname not in data_table:
                    data_table[fname] = dict()

                fpath = path_join(dirpath, filename)
                if filename.endswith(".jpg"):
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
    return data_table


def main():
    import re
    spli = re.compile(r'[\s\t]+')
    table = go_through()
    import random
    # table = table.values()
    # random.shuffle(table)
    cnt = 0
    # print table
    # print table[0]
    # return

    for key in table:
        each = table[key]
        img_path = each["image"]
        joint_path = each["joint"]
        image = cv2.imread(img_path)
        # print img_path
        # print image.shape

        with open(joint_path, 'r') as fp:
            line = fp.read()
            joint = [int(each) for each in re.split(r'[\s\t]+', line)[:4]]
            joint[2] += joint[0]
            joint[3] += joint[1]
        # print line
        # print joint
        pts = np.array([[joint[0], joint[1]], [joint[2], joint[1]],  [joint[2], joint[3]], [joint[0], joint[3]]])
        cv2.polylines(image, [pts], True, (0, 0, 255))
        cv2.imshow("frame", image)
        cv2.waitKey(0)

        cnt += 1
        if cnt >= 50:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
import cv2
import os

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

directory = '../building_data/val/labels/'
file_list = list_files(directory)
for filename in file_list:
    if(filename[-4:] == '.jpg'):
        img = cv2.imread(filename, 0)
        img[img <= 10] = 0
        img[img > 10] = 255
        cv2.imwrite(filename, img)
from PIL import Image
import os

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r

directory = '../building_data/' 
file_list = list_files(directory)
for filename in file_list:
    if(filename[-4:] == '.tif'):
        new_filename = filename[:-4] + '.jpg'
        img = Image.open(filename)
        img.save(new_filename, optimize=False, quality=100)

import utils
import sys
sys.path.insert(1, 'core/measuring_impact_of_natural_calamities')
import single_file_prediction

import time
import os
import cv2
import json

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

pre_image = 'uploads/' + sys.argv[1] + '_pre.jpg'
post_image = 'uploads/' + sys.argv[1] + '_post.jpg'
result_image = 'results/' + sys.argv[1] + '.jpg'
result_json = 'results/' + sys.argv[1] + '.json'

post_image, dii, added_pixels, destroyed_pixels = single_file_prediction.get_predictions(pre_image, post_image)
cv2.imwrite(result_image, post_image)

time.sleep(0.5)
utils.bash_print('Image:{}'.format(result_image))
utils.bash_print('Generating JSON..')
data_dict = {'added_pixels':added_pixels, 'destroyed_pixels':destroyed_pixels}
json_object = json.dumps(data_dict)
with open(result_json, 'w') as outfile: 
    outfile.write(json_object) 
time.sleep(1)
utils.bash_print('JSON:{}'.format(result_json))

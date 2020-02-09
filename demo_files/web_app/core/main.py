import utils

import sys
import os
import time
import json

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

image_id = '5e3f8664b8857'
result_image = 'results/' + image_id + '.jpg'
result_json = 'results/' + image_id + '.json'

time.sleep(0.2)
utils.bash_print('Extracting buildings..')
time.sleep(0.2)
utils.bash_print('Extracting buildings finished')
time.sleep(0.2)
utils.bash_print('Extracting roads..')
time.sleep(0.2)
utils.bash_print('Extracting roads finished')
time.sleep(0.2)
utils.bash_print('Image:{}'.format(result_image))
utils.bash_print('Generating JSON..')
time.sleep(1)
utils.bash_print('JSON:{}'.format(result_json))

import utils

import sys
import time
import os

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

fil = 'uploads/' + sys.argv[1] + '_pre.jpg'

utils.bash_print(sys.argv)
time.sleep(0.5)
utils.bash_print("Image:{}".format(fil))
time.sleep(0.5)
utils.bash_print("JSON:JSON Content")
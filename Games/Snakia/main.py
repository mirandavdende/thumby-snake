import os

os.chdir("/Games/Snakia")

import wrapper_thumby_color
from snakia import init, update

wrapper_thumby_color.run(wrapper_thumby_color, init, update, framerate=10)

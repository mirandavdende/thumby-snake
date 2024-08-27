import os

os.chdir("/Games/Snoke")

import thumbyColorWrapper
from snoke import init, update

thumbyColorWrapper.run(thumbyColorWrapper, init, update, framerate=10)

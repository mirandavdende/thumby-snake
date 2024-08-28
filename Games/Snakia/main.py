import os

os.chdir("/Games/Snakia")

import thumbyColorWrapper
from snakia import init, update

thumbyColorWrapper.run(thumbyColorWrapper, init, update, framerate=10)

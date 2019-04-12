# initalize the app module

import sys
import os.path as path

# add directory to system path for import access
sys.path.append(path.join(path.dirname(
    path.dirname(path.abspath(__file__))), '/app'))

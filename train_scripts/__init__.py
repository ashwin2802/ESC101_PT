# import all training scripts
from train_scripts import numpy_, tf_, torch_

# add directory to system path for import access
import sys
import os.path as path
sys.path.append(path.join(path.dirname(
    path.dirname(path.abspath(__file__))), '/train_scripts'))

# import all models
from models import rand, follower, tf_model, glitchy, numpy_model, torch_model

# add directory to system path for import access
import sys
import os.path as path
sys.path.append(path.join(path.dirname(path.abspath(__file__)), '/models'))

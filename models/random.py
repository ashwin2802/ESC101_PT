import os.path as path
from app import comp
from app import pong
import random


def make_prediction():
    move = random.randint(1, 100)
    if move % 3 == 1:
        pred = 1
    elif move % 3 == 0:
        pred = -1
    else:
        pred = 0
    # pong.debug(pred)
    return pred


def get_prediction():
    prediction = make_prediction()
    return prediction

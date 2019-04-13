# A model that just moves randomly

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


def get_prediction(side):
    prediction = make_prediction()
    return prediction

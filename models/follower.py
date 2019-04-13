# ball following model

import os.path as path
from app import data


def make_prediction(ball_x, ball_y, pad_x, pad_y):

    if(ball_y < pad_y + 40):
        # move up if ball is 40 pixels below pad's centre
        pred = 1
        return pred

    elif(ball_y > pad_y + 40):
        # move down if ball is 40 pixels above pad's centre
        pred = -1
        return pred

    else:
        # don't move at all
        pred = 0
        return pred


def get_prediction(side):

    # get ball and pad positions
    ball_x, ball_y, angle, v = data.get_ball_pos()
    if(side == "left"):
        pad_x, pad_y = data.get_pad_pos("left")
    elif(side == "right"):
        pad_x, pad_y = data.get_pad_pos("right")

    # make and return action
    prediction = make_prediction(ball_x, ball_y, pad_x, pad_y)
    return prediction

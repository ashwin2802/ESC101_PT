# ball following AI, but with laziness and random glitches

import random
import os.path as path
from app import data


def make_prediction(ball_x, ball_y, pad_x, pad_y):

    # define the glitch
    glitch = random.randint(1, 1000)

    if(ball_y < pad_y + 10):

        # move up if ball is 10 pixels below pad's centre
        pred = 1

        if(glitch % 10 == 0):
            # when glitched, move opposite
            return -pred
        else:
            return pred

    elif(ball_y > pad_y + 10):

        # move down if ball is 10 pixels above pad's centre
        pred = -1

        if(glitch % 10 == 0):
            # when glitched, move opposite
            return -pred
        else:
            return pred

    else:

        # else don't move at all
        pred = 0

        if(glitch % 10 == 0):
            # when glitched, randomly move up or down
            if(glitch % 2 == 0):
                return 1
            else:
                return -1
        else:
            return 0


def get_prediction(side):

    # get ball and pad positions
    ball_x, ball_y, angle, v = data.get_ball_pos()
    if(side == "left"):
        pad_x, pad_y = data.get_pad_pos("left")
    elif(side == "right"):
        pad_x, pad_y = data.get_pad_pos("right")

    # make and send prediction
    prediction = make_prediction(ball_x, ball_y, pad_x, pad_y)
    return prediction

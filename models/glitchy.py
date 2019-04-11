import random
import os.path as path
#from app import comp
#from app import pong
from app import data


def make_prediction(ball_x, ball_y, pad_x, pad_y):
    glitch = random.randint(1, 1000)
    # improve this a bit ?
    # works well, had to just place it out of the event loop
    # works too well maybe?
    if(ball_y < pad_y + 10):
        pred = 1
        # if(pad_y < 200):
        #   pred = -1
        # pong.debug(pred)
        if(glitch % 10 == 0):
            return -pred
        else:
            return pred
    elif(ball_y > pad_y + 10):
        pred = -1

        # if(pad_y > 600):
        #   pred = 1
        # pong.debug(pred)
        if(glitch % 10 == 0):
            return -pred
        else:
            return pred
    else:
        pred = 0
        # pong.debug(pred)
        if(glitch % 10 == 0):
            if(glitch % 2 == 0):
                return 1
            else:
                return -1
        else:
            return 0

# maybe rename this to send prediction?


def get_prediction(side):
    ball_x, ball_y, angle, v = data.get_ball_pos()
    if(side == "left"):
        pad_x, pad_y = data.get_pad_pos("left")
    elif(side == "right"):
        pad_x, pad_y = data.get_pad_pos("right")
    prediction = make_prediction(ball_x, ball_y, pad_x, pad_y)
    return prediction

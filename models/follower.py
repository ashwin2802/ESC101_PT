import os.path as path
#from app import comp
#from app import pong
from app import data


def make_prediction(ball_x, ball_y, pad_x, pad_y):
    # improve this a bit ?
    # works well, had to just place it out of the event loop
    # works too well maybe?
    if(ball_y < pad_y + 20):
        pred = 1
        # if(pad_y < 200):
        #   pred = -1
        # pong.debug(pred)
        return pred
    elif(ball_y > pad_y + 20):
        pred = -1
        # if(pad_y > 600):
        #   pred = 1
        # pong.debug(pred)
        return pred
    else:
        pred = 0
        # pong.debug(pred)
        return pred

# maybe rename this to send prediction?


def get_prediction(side):
    ball_x, ball_y, angle, v = data.get_ball_pos()
    if(side == "left"):
        pad_x, pad_y = data.get_pad_pos("left")
    elif(side == "right"):
        pad_x, pad_y = data.get_pad_pos("right")
    prediction = make_prediction(ball_x, ball_y, pad_x, pad_y)
    return prediction

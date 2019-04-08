import os.path as path
from app import comp
from app import pong


def get_ball_pos():
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/ball_pos.txt')
    with open(filepath, 'r') as f:
        data = f.readline()
        f.close()
    [x, y, angle, v] = data.split(',')
    # pong.debug(data)
    return int(x), int(y), int(angle), float(v)


def get_pad_pos():
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/pad_pos.txt')
    with open(filepath, 'r') as f:
        data = f.readline()
        f.close()
    [x, y] = data.split(',')
    # pong.debug(data)
    return int(x), int(y)


def make_prediction(ball_x, ball_y, pad_x, pad_y):
    if(ball_y < pad_y + 10):
        pred = 1
        if(pad_y < 200):
            pred = -1
        pong.debug(pred)
        return pred
    elif(ball_y > pad_y + 10):
        pred = -1
        if(pad_y > 600):
            pred = 1
        pong.debug(pred)
        return pred
    else:
        pred = 0
        pong.debug(pred)
        return pred

# maybe rename this to send prediction?


def get_prediction():
    ball_x, ball_y, angle, v = get_ball_pos()
    pad_x, pad_y = get_pad_pos()
    prediction = make_prediction(ball_x, ball_y, pad_x, pad_y)
    return prediction

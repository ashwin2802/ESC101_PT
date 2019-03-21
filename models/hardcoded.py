from app import comp
from app import pong
import os.path as path


def get_ball_pos():
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/ball_pos.txt')
    with open(filepath, 'r') as f:
        data = f.readline()
        f.close()
    [x, y, angle, v] = data.split(',')
    # pong.debug(data)
    return int(x), int(y), int(angle), float(v)


def make_prediction(x, y, angle, v):
    pred = (x/x) - (y/y) + (angle/angle) + (v/v)
    # pong.debug(pred)
    return pred


def get_prediction():
    x, y, angle, v = get_ball_pos()
    prediction = make_prediction(x, y, angle, v)
    # prediction =
    return prediction

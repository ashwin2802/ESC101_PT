import numpy as np
try:
    import cPickle as pickle
except:
    import pickle
from app import data

with open('weights/model.p', 'rb') as weights:
    model = pickle.load(weights)
    weights.close()
prev_frame = None
A = 80*80


def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))


def preproc(img):
    img = img.convert('L')
    img.thumbnail((80, 80))
    np_img = np.array(img)
    np_img[np_img != 0] = 1
    return np_img.astype(float).ravel()


def forward_pass(x):
    global model
    layer = np.dot(model['W1'], x)
    layer[layer < 0] = 0
    log_prob = np.dot(model['W2'], layer)
    prob = sigmoid(log_prob)
    return prob


def get_prediction(side):
    global prev_frame
    cur_frame = preproc(data.run_frame_load())
    inp = cur_frame - prev_frame if prev_frame is not None else np.zeros(A)
    prev_frame = cur_frame
    a_prob = forward_pass(inp)
    action = 1 if a_prob > 0.7 else -1
    # pong.debug(action)
    return action

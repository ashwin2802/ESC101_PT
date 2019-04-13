# numpy based RL model

import numpy as np
import pickle
from app import data

# import pre-trained model weights
try:
    model = pickle.load(open('weights/np/model1.p', 'rb'))
except:
    raise FileNotFoundError("Could not load model.")

# define variable to hold frame
prev_frame = None

# define number of pixels in input
A = 80*80

# returns sigmoid of x


def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

# preprocess image and convert to frame


def preproc(img):

    # convert RGB to grayscale
    img = img.convert('L')

    # compress image by a scale of 8
    img.thumbnail((80, 80))

    # convert to array
    np_img = np.array(img)

    # set all non-black pixels as 1
    np_img[np_img != 0] = 1

    # return linearized array of floats
    return np_img.astype(float).ravel()

# feed image through the network and return probability of going up


def forward_pass(x):
    global model

    # image after passing through hidden layer
    layer = np.dot(model['W1'], x)

    # ReLU activation
    layer[layer < 0] = 0

    # calculate the log probability
    log_prob = np.dot(model['W2'], layer)

    # sigmoid activation
    prob = sigmoid(log_prob)

    # return probability of going up
    return prob

# give prediction to interface


def get_prediction(side):
    global prev_frame

    # process current frame
    cur_frame = preproc(data.run_frame_load())

    # input difference frame into network
    inp = cur_frame - prev_frame if prev_frame is not None else np.zeros(A)

    # move frame ahead
    prev_frame = cur_frame

    # calculate up action probability by passing difference frame through network
    a_prob, _ = forward_pass(inp)

    # 70% threshold for confidence
    action = 1 if a_prob > 0.7 else -1
    return action

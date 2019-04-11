import numpy as np
from PIL import Image
try:
    import cPickle as pickle
except:
    import pickle
#import pygame
#import os.path as path
#from app import pong
from app import data

H = 200
batch_size = 5
learn_rate = 1e-4
gamma = 0.99
decay_rate = 0.99
resume = False
player_score = 0
self_score = 0

A = 80*80
if resume:
    with open('weights/model.p', 'rb') as weights:
        model = pickle.load(weights)
        weights.close()
else:
    model = {}
    model['W1'] = np.random.randn(H, A)/np.sqrt(A)
    model['W2'] = np.random.randn(H)/np.sqrt(H)

gradient_buf = {x: np.zeros_like(v) for x, v in model.items()}
RMSProp_mem = {y: np.zeros_like(w) for y, w in model.items()}


def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))


def preproc(img):
    img = img.convert('L')
    img.thumbnail((80, 80))
    np_img = np.array(img)
    np_img[np_img != 0] = 1
    return np_img.astype(float).ravel()


def discount_reward(r):
    global gamma
    discount_r = np.zeros_like(r)
    run_add = 0
    for x in reversed(range(0, r.size)):
        if (r[x] != 0):
            run_add = 0
        run_add = run_add*gamma + r[x]
        discount_r[x] = run_add
    return discount_r


def forward_pass(x):
    global model
    layer = np.dot(model['W1'], x)
    layer[layer < 0] = 0
    log_prob = np.dot(model['W2'], layer)
    prob = sigmoid(log_prob)
    return prob, layer


def backward_pass(ep_layers, ep_dlog_probs, ep_inps):
    global model
    dW2 = np.dot(ep_layers.T, ep_dlog_probs).ravel()
    dlayer = np.outer(ep_dlog_probs, model['W2'])
    dlayer[dlayer < 0] = 0
    dW1 = np.dot(dlayer.T, ep_inps)
    return {'W1': dW1, 'W2': dW2}


def get_reward():
    global self_score, player_score
    if(data.get_score("right") > self_score):
        self_score = data.get_score("right")
        return 1
    elif(data.get_score("left") > player_score):
        player_score = data.get_score("left")
        return -1
    else:
        return 0


def done():
    if(data.get_score("right") > 21 or data.get_score("left") > 21):
        return 1
    else:
        return 0


# give_action = False
prev_frame = None
inps, layers, dlog_probs, drs = [], [], [], []
run_reward = None
sum_reward = 0
ep_num = 0


def get_prediction(side):
    global prev_frame, inps, layers, dlog_probs, ep_num
    cur_frame = preproc(data.frame_load(ep_num))
    inp = cur_frame - prev_frame if prev_frame is not None else np.zeros(A)
    prev_frame = cur_frame
    a_prob, cur_layer = forward_pass(inp)
    action = 1 if np.random.uniform() < a_prob else -1
    inps.append(inp)
    layers.append(cur_layer)
    y = 1 if action == 1 else 0
    dlog_probs.append(y - a_prob)
    # pong.debug(action)
    return action


def update():
    global sum_reward, drs, inps, layers, dlog_probs, ep_num
    global gradient_buf, RMSProp_mem, run_reward, prev_frame
    global batch_size, decay_rate, self_score, player_score
    global model, learn_rate
    reward = get_reward()
    sum_reward += reward
    drs.append(reward)
    if done():
        ep_num += 1
        ep_inps = np.vstack(inps)
        ep_layers = np.vstack(layers)
        ep_dlog_probs = np.vstack(dlog_probs)
        ep_rewards = np.vstack(drs)
        inps, layers, dlog_probs, drs = [], [], [], []
        discounted_ep_rewards = discount_reward(ep_rewards).astype(float)
        discounted_ep_rewards -= np.mean(discounted_ep_rewards)
        discounted_ep_rewards /= np.std(discounted_ep_rewards)
        ep_dlog_probs *= discounted_ep_rewards
        grad = backward_pass(ep_layers, ep_dlog_probs, ep_inps)
        for x in model:
            gradient_buf[x] += grad[x]
        if ep_num % batch_size == 0:
            for x, y in model.items():
                g = gradient_buf[x]
                RMSProp_mem[x] = decay_rate * \
                    RMSProp_mem[x] + (1-decay_rate)*g**2
                model[x] += learn_rate*g/np.sqrt(RMSProp_mem[x]+1e-5)
                gradient_buf[x] = np.zeros_like(y)
        run_reward = sum_reward if run_reward is None else run_reward*0.99 + sum_reward*0.01
        data.update_log("Episode over. Resetting. Episode reward was " +
                        str(sum_reward)+". running mean: " + str(round(run_reward, 2)))
        if ep_num % 10 == 0:
            data.update_log("10 episodes done. Saving weights.")
            pickle.dump(model, open('weights/model.p', 'wb'))
        sum_reward = 0
        self_score = 0
        player_score = 0
        prev_frame = None

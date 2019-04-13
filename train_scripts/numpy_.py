# training script for numpy based model

from app import data
from app import torp
try:
    import numpy as np
except:
    data.write_numpy_log("Numpy not found.")
from PIL import Image
import pickle

# define hyperparameters
H = 200                 # no. of hidden neurons
batch_size = 5          # batch size for updating gradients
learn_rate = 1e-3       # learning rate for optimizer
gamma = 0.99            # gamma for discounted rewards
decay_rate = 0.99       # decay rate for optimizer
A = 80*80               # input pixels


# if training was interrupted or stopped, set this to true to restart
resume = False          # train from scratch

player_score = 0        # score of other pad
self_score = 0          # score of model's pad

# start logging by writing all hyperparameters
data.write_numpy_log("Hyperparameters - no. of layers = 1, no. of neurons = " + str(H) + ", batch size = " +
                     str(batch_size) + ", input size = " + str(A) + ", learning rate = " + str(learn_rate)+"\n")


if resume:

    # load saved weights
    with open('weights/np/model.p', 'rb') as weights:
        model = pickle.load(weights)
        weights.close()

    # update log
    data.update_numpy_log("Starting from previous checkpoint.\n")
else:

    # create new model
    model = {}

    # update log
    data.update_numpy_log("Training from scratch.\n")

    # random initialization of model weights
    model['W1'] = np.random.randn(H, A)/np.sqrt(A)
    model['W2'] = np.random.randn(H)/np.sqrt(H)

# gradient and optimizer memory variables
gradient_buf = {x: np.zeros_like(v) for x, v in model.items()}
RMSProp_mem = {y: np.zeros_like(w) for y, w in model.items()}


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

# calculate discounted rewards from set of obtained rewards


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

# update weights of the model


def backward_pass(ep_layers, ep_dlog_probs, ep_inps):
    global model
    dW2 = np.dot(ep_layers.T, ep_dlog_probs).ravel()
    dlayer = np.outer(ep_dlog_probs, model['W2'])
    dlayer[dlayer < 0] = 0
    dW1 = np.dot(dlayer.T, ep_inps)
    return {'W1': dW1, 'W2': dW2}

# get the reward according to set policy


def get_reward():
    global self_score, player_score

    # if other's score increases, -1
    if(data.get_score("right") > self_score):
        self_score = data.get_score("right")
        return 1

    # if our score increases, 1
    elif(data.get_score("left") > player_score):
        player_score = data.get_score("left")
        return -1

    # zero otherwise
    else:
        return 0

# condition for end of episode


def done():
    if(data.get_score("right") > 21 or data.get_score("left") > 21):
        return 1
    else:
        return 0


# storage variables for each episode
prev_frame = None           # previous frame
inps = []                   # episode inputs
layers = []                 # convoluted inputs
dlog_probs = []             # episode log probabilities
drs = []                    # episode rewards

run_reward = None           # running reward
reward_target = 5.0         # to stop training
sum_reward = 0              # total reward
ep_num = 0                  # episode number

# give prediction to interface


def get_prediction(side):
    global prev_frame, inps, layers, dlog_probs, ep_num

    # process current frame
    cur_frame = preproc(data.run_frame_load())

    # input difference frame into network
    inp = cur_frame - prev_frame if prev_frame is not None else np.zeros(A)

    # move frame ahead
    prev_frame = cur_frame

    # calculate up action probability by passing difference frame through network
    a_prob, cur_layer = forward_pass(inp)

    # 70% threshold for confidence
    action = 1 if a_prob > 0.7 else -1

    # store input, layer, log probability
    inps.append(inp)
    layers.append(cur_layer)
    y = 1 if action == 1 else 0
    dlog_probs.append(y - a_prob)

    return action

# update the network

def update():
    global sum_reward, drs, inps, layers, dlog_probs, ep_num
    global gradient_buf, RMSProp_mem, run_reward, prev_frame
    global batch_size, decay_rate, self_score, player_score
    global model, learn_rate, reward_target

    # obtain reward and store it
    reward = get_reward()
    sum_reward += reward
    drs.append(reward)

    # if epsiode is over
    if done():

        # increment episode_number
        ep_num += 1

        # stack all inputs, layers, rewards and log probabilities.
        ep_inps = np.vstack(inps)
        ep_layers = np.vstack(layers)
        ep_dlog_probs = np.vstack(dlog_probs)
        ep_rewards = np.vstack(drs)

        # clear storage
        inps, layers, dlog_probs, drs = [], [], [], []

        # calculate discounted rewards
        discounted_ep_rewards = discount_reward(ep_rewards).astype(float)
        discounted_ep_rewards -= np.mean(discounted_ep_rewards)
        discounted_ep_rewards /= np.std(discounted_ep_rewards)
        ep_dlog_probs *= discounted_ep_rewards

        # update gradients and store them
        grad = backward_pass(ep_layers, ep_dlog_probs, ep_inps)
        for x in model:
            gradient_buf[x] += grad[x]

        # every batch, update weights and store them
        if ep_num % batch_size == 0:
            for x, y in model.items():
                g = gradient_buf[x]
                RMSProp_mem[x] = decay_rate * \
                    RMSProp_mem[x] + (1-decay_rate)*g**2
                model[x] += learn_rate*g/np.sqrt(RMSProp_mem[x]+1e-5)
                gradient_buf[x] = np.zeros_like(y)

        # update running reward
        run_reward = sum_reward if run_reward is None else run_reward*0.99 + sum_reward*0.01

        # log end of episode
        data.update_numpy_log("Episode over. Resetting. Episode reward was " +
                              str(sum_reward)+". running mean: " + str(round(run_reward, 2)))

        # save every 2 batches / 10 episodes
        if ep_num % 10 == 0:
            data.update_numpy_log("10 episodes done. Saving weights.")
            pickle.dump(model, open('weights/np/model.p', 'wb'))

        # exit if target reward achieved
        if run_reward > reward_target:
            data.update_numpy_log("Running reward of" + str(run_reward) +
                                  "achieved. Saving weights and stopping training.")
            pickle.dump(model, open('weights/np/model.p', 'wb'))
            torp.menu.play()

        # empty all storages
        sum_reward = 0
        self_score = 0
        player_score = 0
        prev_frame = None


# save when exiting


def exit():
    global ep_num
    pickle.dump(model, open('weights/np/model.p', 'wb'))
    data.update_numpy_log("Training stopped after "+str(ep_num) +
                          " episodes. Target not achieved, saving model and exiting.\n")

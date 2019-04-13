# trainer script for the tensorflow model

from app import data
from PIL import Image
import numpy as np
try:
    import tensorflow as tf
except:
    print("Tensorflow not found.")
import pickle
import os.path as path

# if training was interrupted or is to be continued, set this to True
resume = False

# define hyperparameters
num_pixels = 6400
hidden_units = 200
batch_size = 10


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
    gamma = 0.99
    discount_r = np.zeros_like(r)
    run_add = 0
    for x in reversed(range(0, len(r))):
        if (r[x] != 0):
            run_add = 0
        run_add = run_add*gamma + r[x]
        discount_r[x] = run_add
    return discount_r


# create the neural network


def create_network(num_pixels, hidden_units):

    # input layer
    pixels = tf.placeholder(dtype=tf.float32, shape=(None, num_pixels))
    # action shape
    actions = tf.placeholder(dtype=tf.float32, shape=(None, 1))
    # reward shape
    rewards = tf.placeholder(dtype=tf.float32, shape=(None, 1))

    # set variable scope so that network doesn't run outside the session
    with tf.variable_scope('policy'):

        # first layer
        hidden = tf.layers.dense(pixels, hidden_units, activation=tf.nn.relu,
                                 kernel_initializer=tf.contrib.layers.xavier_initializer())

        # output log probabilities
        logits = tf.layers.dense(
            hidden, 1, activation=None, kernel_initializer=tf.contrib.layers.xavier_initializer())

        # output probability
        out = tf.sigmoid(logits, name="sigmoid")

        # calculate loss
        cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(
            labels=actions, logits=logits, name="cross_entropy")
        loss = tf.reduce_sum(tf.multiply(
            rewards, cross_entropy, name="rewards"))

    # set learning rate and decay rate for optimizer
    learn_rate = 1e-3
    decay_rate = 0.99

    # call optimizer to minimize loss
    optim = tf.train.RMSPropOptimizer(
        learn_rate, decay=decay_rate).minimize(loss)

    # create summary
    tf.summary.histogram("hidden_out", hidden)
    tf.summary.histogram("logits_out", logits)
    tf.summary.histogram("prob_out", out)
    merged = tf.summary.merge_all()

    # output network
    return pixels, actions, rewards, out, optim, merged


# reset the graph
tf.reset_default_graph()

# define directories to store logs and checkpoints
weights_dir = data.create_dir('weights/tf')
log_dir = data.create_dir('data/logs/tf')
checkpoint_dir = data.create_dir(weights_dir + '/checkpoints')

# create the network
pix_, action_, reward_, out_, opt_, merge_ = create_network(
    num_pixels, hidden_units)

# start a new session
sess = tf.Session()

# create saver object to save model at regular intervals
saver = tf.train.Saver(max_to_keep=20, keep_checkpoint_every_n_hours=1)

# create a writer object that stores logs
writer = tf.summary.FileWriter(log_dir+'/train', sess.graph)


# restore last checkpoint if training is to be resumed
if resume:
    data.write_tf_log("Resuming from latest saved checkpoint.\n")
    saver.restore(sess, tf.train.latest_checkpoint(checkpoint_dir))
else:
    # start a new session
    data.write_tf_log("Training from scratch.\n")
    sess.run(tf.global_variables_initializer())

# storage variables
prev_frame = None       # previous frame
xs = []                 # diff frames
ys = []                 # actions
ep_ws = []              # episode rewards
batch_ws = []           # batch rewards
step = pickle.load(open(weights_dir+'/step.p', 'rb')
                   ) if resume and path.exists(weights_dir+'/step.p') else 0   # batch number
ep_num = step*10        # episode number
mean_reward = -21.0     # running reward


# give prediction to interface


def get_prediction(side):
    global prev_frame, sess, out_, pix_

    # process current frame
    cur_frame = preproc(data.run_frame_load())

    # input difference frame into network
    x = cur_frame - \
        prev_frame if prev_frame is not None else np.zeros((num_pixels, ))

    # move frame ahead
    prev_frame = cur_frame

    # calculate probability
    tf_probs = sess.run(out_, feed_dict={pix_: x.reshape(-1, x.size)})

    # 70% threshold confidence
    action = 1 if tf_probs > 0.7 else -1
    return action

# obtain reward after action according to policy


def get_reward():
    ball_x, ball_y, angle, v = data.get_ball_pos()
    pad_x, pad_y = data.get_pad_pos("right")
    if ball_x > 600:
        if ball_y > pad_y - 40 and ball_y < pad_y + 40:
            return 1
        else:
            return -1
    else:
        return 0

# check if episode is over


def done():
    if(data.get_score("right") > 21 or data.get_score("left") > 21):
        return 1
    else:
        return 0

# update the network after performing action


def update():
    global ep_num, ep_ws, mean_reward, xs, ys, batch_ws, prev_frame
    global batch_size, checkpoint_dir, step, sess, weights_dir, saver, writer

    # get the reward
    reward = get_reward()

    # store reward
    ep_ws.append(reward)

    # if episode is over
    if done():

        # increment episode number
        ep_num += 1

        # calculate discounted rewards for episode
        discounted_epr = discount_reward(ep_ws).astype(float)
        discounted_epr -= np.mean(discounted_epr)
        discounted_epr /= np.mean(discounted_epr)

        # store discounted rewards
        batch_ws += discounted_epr.tolist()

        # calculate running reward
        mean_reward = 0.99*mean_reward + (1-0.99)*sum(ep_ws)

        # update log
        data.update_tf_log("episode: {}, reward: {}".format(
            ep_num, sum(ep_ws)))

        # update summary
        ep_sum = tf.Summary(value=[tf.Summary.Value(
            tag="running_reward", simple_value=mean_reward)])
        writer.add_summary(ep_sum, global_step=ep_num)

        # empty episode rewards
        ep_ws = []

        # if batch is over
        if ep_num % batch_size == 0:

            # increment batch number
            step += 1

            # stack all inputs
            exs = np.vstack(xs)

            # stack all actions
            eys = np.vstack(ys)

            # stack all rewards
            ews = np.vstack(batch_ws)

            # get number of frames in batch
            frame_size = len(xs)

            # empty storage
            xs = []
            ys = []
            batch_ws = []

            # number of frames to process at a time
            stride = 20000
            pos = 0

            # process all frames
            while True:

                # run through all frames
                end = frame_size if pos+stride >= frame_size else pos+stride
                batch_x = exs[pos::end]
                batch_y = eys[pos::end]
                batch_w = ews[pos::end]

                # run optimizer
                tf_opt, tf_summary = sess.run([opt_, merge_], feed_dict={
                    pix_: batch_x, action_: batch_y, reward_: batch_w})

                pos = end

                # stop when all frames are processed
                if pos >= frame_size:
                    batch_x = []
                    batch_y = []
                    batch_z = []
                    break

            # save the model
            saver.save(sess, checkpoint_dir+'/pg_{}.ckpt'.format(step))

            # update summary
            writer.add_summary(tf_summary, step)

            # save step number
            pickle.dump(step, open(weights_dir+'/step.p', 'wb+'))

            # update log
            data.update_tf_log("episode: {}, update step: {}, frame size: {}, reward: {}".format(
                ep_num, step, frame_size, round(mean_reward, 2)))

        # empty storage
        prev_frame = None

# save when exiting


def exit():
    global ep_num, weights_dir

    pickle.dump(step, open(weights_dir+'/step.p', 'wb+'))

    # update log
    data.update_numpy_log("Training stopped after "+str(ep_num) +
                          " episodes. Target not achieved, saving model and exiting.\n")

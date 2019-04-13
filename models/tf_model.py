# tensorflow based RL model

from app import data
from PIL import Image
import numpy as np
try:
    import tensorflow as tf
except:
    print("Tensorflow not found.")
import pickle

# define hyperparameters
num_pixels = 6400
hidden_units = 200
batch_size = 10

# set this to True for loading pre-trained model
resume = False

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

# create the network
pix_, action_, reward_, out_, opt_, merge_ = create_network(
    num_pixels, hidden_units)

# start a new session
sess = tf.Session()

# create saver object to save model at regular intervals
saver = tf.train.Saver(max_to_keep=20, keep_checkpoint_every_n_hours=1)

# define directories to store logs and checkpoints
weights_dir = data.create_dir('weights/tf')
log_dir = data.create_dir('data/logs/tf')
checkpoint_dir = data.create_dir(weights_dir + '/checkpoints')

# restore last checkpoint to load the model
if resume:
    saver.restore(sess, tf.train.latest_checkpoint(checkpoint_dir))

# set variable to store previous frame
prev_frame = None

# calculate action


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

from app import data
from PIL import Image
import numpy as np
try:
    import tensorflow as tf
    import keras
except:
    print("Tensorflow not found.")
import pickle

num_pixels = 6400
hidden_units = 200
batch_size = 10


def preproc(img):
    img = img.convert('L')
    img.thumbnail((80, 80))
    np_img = np.array(img)
    np_img[np_img != 0] = 1
    return np_img.astype(float).ravel()

def create_network(num_pixels, hidden_units):
    pixels = tf.placeholder(dtype=tf.float32, shape=(None, num_pixels))
    actions = tf.placeholder(dtype=tf.float32, shape=(None, 1))
    rewards = tf.placeholder(dtype=tf.float32, shape=(None, 1))

    with tf.variable_scope('policy'):
        hidden = keras.layers.dense(pixels, hidden_units, activation=tf.nn.relu,
                                 kernel_initializer=tf.contrib.layers.xavier_initializer())
        logits = keras.layers.dense(
            hidden, 1, activation=None, kernel_initializer=tf.contrib.layers.xavier_initializer())
        out = tf.sigmoid(logits, name="sigmoid")
        cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(
            labels=actions, logits=logits, name="cross_entropy")
        loss = tf.reduce_sum(tf.multiply(
            rewards, cross_entropy, name="rewards"))

    learn_rate = 1e-3
    decay_rate = 0.99
    optim = tf.train.RMSPropOptimizer(
        learn_rate, decay=decay_rate).minimize(loss)

    tf.summary.histogram("hidden_out", hidden)
    tf.summary.histogram("logits_out", logits)
    tf.summary.histogram("prob_out", out)
    merged = tf.summary.merge_all()

    return pixels, actions, rewards, out, optim, merged


tf.reset_default_graph()
pix_, action_, reward_, out_, opt_, merge_ = create_network(
    num_pixels, hidden_units)

sess = tf.Session()
saver = tf.train.Saver(max_to_keep=20, keep_checkpoint_every_n_hours=1)

weights_dir = data.create_dir('weights/tf')
checkpoint_dir = data.create_dir(log_dir + '/checkpoints')
saver.restore(sess, tf.train.latest_checkpoint(checkpoint_dir))
prev_frame = None


def get_prediction(side):
    global prev_frame, sess, out_, pix_
    cur_frame = preproc(data.run_frame_load())
    x = cur_frame - \
        prev_frame if prev_frame is not None else np.zeros((num_pixels, ))
    prev_frame = cur_frame
    tf_probs = sess.run(out_, feed_dict={pix_: x.reshape(-1, x.size)})
    action = 1 if np.random.uniform() < tf_probs[0, 0] else -1
    return action
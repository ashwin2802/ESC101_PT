from app import data
from PIL import Image
import numpy as np
try:
    import tensorflow as tf
except:
    print("Tensorflow not found.")
import pickle
import os.path as path

resume = True
num_pixels = 6400
hidden_units = 200
batch_size = 10


def preproc(img):
    img = img.convert('L')
    img.thumbnail((80, 80))
    np_img = np.array(img)
    np_img[np_img != 0] = 1
    return np_img.astype(float).ravel()


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


def create_network(num_pixels, hidden_units):
    pixels = tf.placeholder(dtype=tf.float32, shape=(None, num_pixels))
    actions = tf.placeholder(dtype=tf.float32, shape=(None, 1))
    rewards = tf.placeholder(dtype=tf.float32, shape=(None, 1))

    with tf.variable_scope('policy'):
        hidden = tf.layers.dense(pixels, hidden_units, activation=tf.nn.relu,
                                 kernel_initializer=tf.contrib.layers.xavier_initializer())
        logits = tf.layers.dense(
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
log_dir = data.create_dir('data/logs/tf')
weights_dir = data.create_dir('weights/tf')
checkpoint_dir = data.create_dir(log_dir + '/checkpoints')
writer = tf.summary.FileWriter(log_dir+'/train', sess.graph)

if resume:
    data.write_tf_log("Resuming from latest saved checkpoint.\n")
    saver.restore(sess, tf.train.latest_checkpoint(checkpoint_dir))
else:
    data.write_tf_log("Training from scratch.\n")
    sess.run(tf.global_variables_initializer())

prev_frame = None
xs = []
ys = []
ep_ws = []
batch_ws = []
step = pickle.load(open(weights_dir+'/step.p', 'rb')
                   ) if resume and path.exists(weights_dir+'/step.p') else 0
ep_num = step*10
mean_reward = -21.0


def get_prediction(side):
    global prev_frame, xs, ys, ep_num, sess, out_, pix_
    cur_frame = preproc(data.frame_load(ep_num))
    x = cur_frame - \
        prev_frame if prev_frame is not None else np.zeros((num_pixels, ))
    prev_frame = cur_frame
    tf_probs = sess.run(out_, feed_dict={pix_: x.reshape(-1, x.size)})
    action = 1 if np.random.uniform() < tf_probs[0, 0] else -1
    xs.append(x)
    ys.append(action)
    return action


def get_reward():
    ball_x, ball_y, angle, v = data.get_ball_pos()
    pad_x, pad_y = data.get_pad_pos("right")
    if ball_x > 600:
        if pad_y > ball_y - 40 and pad_y < ball_y + 40:
            return 1
        else:
            return -1
    else:
        return 0


def done():
    if(data.get_score("right") > 21 or data.get_score("left") > 21):
        return 1
    else:
        return 0


def update():
    global ep_num, ep_ws, mean_reward, xs, ys, batch_ws, prev_frame
    global batch_size, checkpoint_dir, step, sess, weights_dir
    reward = get_reward()
    ep_ws.append(reward)
    if done():
        ep_num += 1
        discounted_epr = discount_reward(ep_ws).astype(float)
        discounted_epr -= np.mean(discounted_epr)
        discounted_epr /= np.mean(discounted_epr)
        batch_ws += discounted_epr.tolist()
        mean_reward = 0.99*mean_reward + (1-0.99)*sum(ep_ws)
        data.update_tf_log("episode: {}, reward: {}".format(
            ep_num, sum(ep_ws)))
        ep_sum = tf.Summary(value=[tf.Summary.Value(
            tag="running_reward", simple_value=mean_reward)])
        writer.add_summary(ep_sum, global_step=ep_num)
        ep_ws = []
        if ep_num % batch_size == 0:
            step += 1
            exs = np.vstack(xs)
            eys = np.vstack(ys)
            ews = np.vstack(batch_ws)
            frame_size = len(xs)
            xs = []
            ys = []
            batch_ws = []
            stride = 20000
            pos = 0
            while True:
                end = frame_size if pos+stride >= frame_size else pos+stride
                batch_x = exs[pos::end]
                batch_y = eys[pos::end]
                batch_w = ews[pos::end]
                tf_opt, tf_summary = sess.run([opt_, merge_], feed_dict={
                    pix_: batch_x, action_: batch_y, reward_: batch_w})
                pos = end
                if pos >= frame_size:
                    break
            batch_x = []
            batch_y = []
            batch_z = []
            saver.save(sess, checkpoint_dir+'/pg_{}.ckpt'.format(step))
            writer.add_summary(tf_summary, step)
            pickle.dump(step, open(weights_dir+'/step.p', 'wb+'))
            data.update_tf_log("episode: {}, update step: {}, frame size: {}, reward: {}".format(
                ep_num, step, frame_size, round(mean_reward, 2)))
        prev_frame = None


def exit():
    global ep_num, weights_dir
    pickle.dump(step, open(weights_dir+'/step.p', 'wb+'))
    data.update_numpy_log("Training stopped after "+str(ep_num) +
                          " episodes. Target not achieved, saving model and exiting.\n")

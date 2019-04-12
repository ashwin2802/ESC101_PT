import math
import random
import numpy as np
from PIL import Image
from itertools import count
from collections import namedtuple
from app import data

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

Transition = namedtuple(
    'Transition', ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position+1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class Net(nn.Module):
    def __init__(self, h, w, outputs):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=5, stride=2)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, stride=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        self.bn3 = nn.BatchNorm2d(32)

        def conv2d_size_out(size, kernel_size=5, stride=2):
            return (size-(kernel_size-1)-1) // stride + 1
        convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(w)))
        convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(h)))
        linear_input_size = convw*convh*32
        self.head = nn.Linear(linear_input_size, outputs)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        return self.head(x.view(x.size(0), -1))


batch_size = 32
gamma = 0.99
target_update = 10
screen_height = 640
screen_width = 640
n_actions = 2
num_episode = 300
ep_num = 0
prev_frame = None
# state = None
# next_state = None
# action = 0

policy_net = Net(screen_height, screen_width, n_actions)
target_net = Net(screen_height, screen_width, n_actions)
target_net.load_state_dict(policy_net.state_dict())
optimizer = optim.RMSprop(policy_net.parameters())
init_memory = 10000
memory = ReplayMemory(init_memory*10)


def done():
    if(data.get_score("right") > 21 or data.get_score("left") > 21):
        return 1
    else:
        return 0


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


def optimize_model():
    global memory, batch_size, policy_net
    if len(memory) < batch_size:
        return
    transitions = memory.sample(batch_size)
    batch = Transitions(*zip(*transitions))
    actions = tuple(
        (map(lambda a: torch.tensor([[a]]), batch.action)))
    rewards = tuple(
        (map(lambda r: torch.tensor([r]), batch.reward)))
    non_final_mask = torch.tensor(tuple(
        map(lambda s: s is not None, batch.next_state)), dtype=torch.uint8)
    non_final_next_states = torch.cat(
        [s for s in batch.next_state if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(actions)
    reward_batch = torch.cat(rewards)
    state_action_values = policy_net(state_batch).gather(1, action_batch)
    next_state_values = torch.zeros(batch_size)
    next_state_value[non_final_mask] = target_net(
        non_final_next_states).max(1)[0].detach()
    expected_state_action_values = (next_state_values*gamma) + reward_batch
    loss = F.smooth_l1_loss(state_action_values,
                            expected_state_action_values.unsqueeze(1))
    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()


def get_state(frame):
    state = np.array(frame)
    state = state.transpose((2, 0, 1))
    state = torch.from_numpy(state)
    return state.unsqueeze(0)


def select_action(state):
    with torch.no_grad():
        return policy_net(state).max(1)[1].view(1, 1)


def get_prediction(side):
    global ep_num, prev_frame, policy_net, state
    cur_frame = data.frame_load(ep_num)
    cur_state = get_state(cur_frame)
    prev_state = get_state(prev_frame) if prev_frame is not None else None
    state = cur_state - prev_state if prev_state is not None else cur_state
    prev_frame = cur_frame
    action = select_action(state)


def update():
    global memory
    memory.push(state, action, next_state, reward)
    state = next_state

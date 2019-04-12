# file and data handling

import os.path as path
import os
from PIL import Image
from app import pong
import pygame
import shutil


def ball_pos(ball):
    # write ball data
    (angle, v) = ball.vector
    (x, y) = ball.rect.center
    data = (x, y, angle, v)
    result = ','.join(map(str, data))
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/ball_pos.txt')
    with open(filepath, 'w+') as f:
        f.write(result)
        f.close()


def get_ball_pos():
    # get ball data
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/ball_pos.txt')
    with open(filepath, 'r') as f:
        data = f.readline()
        f.close()
    [x, y, angle, v] = data.split(',')
    # pong.debug(data)
    return int(x), int(y), int(angle), float(v)


def pad_pos(computer, side):
    # write pad position
    (x, y) = computer.rect.center
    data = (x, y)
    result = ','.join(map(str, data))
    if(side == "left"):
        filepath = path.join(path.dirname(path.dirname(
            path.abspath(__file__))), 'data/pad_pos_left.txt')
    elif(side == "right"):
        filepath = path.join(path.dirname(path.dirname(
            path.abspath(__file__))), 'data/pad_pos_right.txt')
    with open(filepath, 'w+') as f:
        f.write(result)
        f.close()


def get_pad_pos(side):
    # get pad position
    if(side == "left"):
        filepath = path.join(path.dirname(path.dirname(
            path.abspath(__file__))), 'data/pad_pos_left.txt')
    elif(side == "right"):
        filepath = path.join(path.dirname(path.dirname(
            path.abspath(__file__))), 'data/pad_pos_right.txt')
    with open(filepath, 'r') as f:
        data = f.readline()
        f.close()
    [x, y] = data.split(',')
    return int(x), int(y)


def write_score(num, side):
    # write score of players
    game_num = get_num_games()
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/score_')
    with open(filepath+side+'.txt', 'w+') as f:
        f.write(str(num))
        f.close()


def get_score(side):
    # get score
    game_num = get_num_games()
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/score_')
    with open(filepath+side+'.txt', 'r') as f:
        score = f.readline()
        f.close()
    return int(score)


def model_write(name):
    # write model name to be trained
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/model_train.txt')
    with open(filepath, 'w+') as f:
        f.write(str(name))
        f.close()


def get_model():
    # get model name to be trained
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/model_train.txt')
    with open(filepath, 'r') as f:
        name = f.readline()
        f.close()
    return name


def score(num):
    # write winnner of game
    game_num = get_num_games()
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/result.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def get_win(game_num):
    # get winner of game
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/result.txt')
    with(open(filepath, 'r')) as f:
        win = f.readline()
        f.close()
    return win


def num_games(num):
    # write number of games played
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/num_games.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def get_num_games():
    # get number of games played
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/num_games.txt')
    with(open(filepath, 'r')) as f:
        num = f.readline()
        f.close()
    if(num == ""):
        return 0
    else:
        return int(num)


def frame(num):
    # write current frame number of episode
    game_num = get_num_games()
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/frame_num.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def get_frame_num(game_num):
    # get current frame number of episode
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num))
    if not path.exists(filepath):
        os.makedirs(filepath)
        open(filepath+'/frame_num.txt', 'w+').close()
    with(open(filepath+'/frame_num.txt', 'r')) as f:
        num = f.readline()
        # pong.debug(num)
        f.close()
    if(num == ""):
        return 0
    else:
        return int(num)


def scrot(screen):
    # take screenshot of current frame in training
    game_surface = pygame.Rect(0, 100, 640, 640)
    game_num = get_num_games()
    frame_num = get_frame_num(game_num)
    path = "data/train/game"+str(game_num)
    pygame.image.save(screen.subsurface(game_surface),
                      path+"/frame"+str(frame_num)+".jpg")
    frame(frame_num+1)


def frame_load(num):
    # load screenshot of current frame in training
    cur_frame_num = get_frame_num(num)-1
    filepath = path.join(path.dirname(path.dirname(path.abspath(
        __file__))), 'data/train/game'+str(num)+'/frame'+str(cur_frame_num)+'.jpg')
    return Image.open(filepath)


def run_frame(num):
    # write current frame number in interface
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/run'+'/run_frame.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def get_run_frame():
    # get current frame number in interface
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/run')
    # put this in all functions
    if not path.exists(filepath):
        os.makedirs(filepath)
        open(filepath+'/run_frame.txt', 'w+').close()
    with(open(filepath+'/run_frame.txt', 'r')) as f:
        num = f.readline()
        # pong.debug(num)
        f.close()
    if(num == ""):
        return 0
    else:
        return int(num)


def run_scrot(screen):
    # take screenshot of current frame in interface
    game_surface = pygame.Rect(0, 100, 640, 640)
    frame_num = get_run_frame()
    path = "data/run"
    pygame.image.save(screen.subsurface(game_surface),
                      path+"/frame"+str(frame_num)+".jpg")
    run_frame(frame_num+1)


def run_frame_load():
    # load screenshot of current frame in interface
    cur_frame_num = get_run_frame()-1
    filepath = path.join(path.dirname(path.dirname(path.abspath(
        __file__))), 'data/run/frame'+str(cur_frame_num)+'.jpg')
    return Image.open(filepath)


def create_dir(rel_path):
    # create dir of given path
    path_ = path.join(path.dirname(
        path.dirname(path.abspath(__file__))), rel_path)
    if not path.exists(path_):
        os.makedirs(path_)
    return path_


def write_numpy_log(message):
    # start numpy model training log with given message
    dirpath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), "data/logs/np")
    if not path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = dirpath+"/train_log.txt"
    with open(filepath, 'w+') as f:
        f.write(str(message)+"\n")
        f.close()


def update_numpy_log(message):
    # update numpy model training log with message
    dirpath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), "data/logs/np")
    if not path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = dirpath+"/train_log.txt"
    with open(filepath, 'a+') as f:
        f.write(str(message)+"\n")
        f.close()


def write_tf_log(message):
    # start tf training log with message
    dirpath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), "data/logs/tf")
    if not path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = dirpath+"/train_log.txt"
    with open(filepath, 'w+') as f:
        f.write(str(message)+"\n")
        f.close()


def update_tf_log(message):
    # update tf training log woith message
    dirpath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), "data/logs/tf")
    if not path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = dirpath+"/train_log.txt"
    with open(filepath, 'a+') as f:
        f.write(str(message)+"\n")
        f.close()


def remove_run():
    # clean screenshots in interface
    shutil.rmtree('data/run')


def remove_train():
    # clean screenshots in training
    shutil.rmtree('data/train')


def debug(var):
    # write variable to file, for debugging
    with open("debug.txt", "a") as f:
        f.write(str(var))
        f.write("\n")
        f.close()
    return

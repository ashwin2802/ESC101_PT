import os.path as path
import os
from PIL import Image
from app import pong
import pygame
import shutil
# from app import pong

# reorder these functions properly


def create_dir(rel_path):
    path_ = path.join(path.dirname(path.dirname(path.abspath(__file__))), rel_path)
    if not path.exists(path_):
        os.makedirs(path_)
    return path_


def debug(var):
    with open("debug.txt", "a") as f:
        f.write(str(var))
        f.write("\n")
        f.close()
    return


def num_games(num):
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/num_games.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def run_scrot(screen):
    game_surface = pygame.Rect(0, 100, 640, 640)
    frame_num = get_run_frame()
    path = "data/run"
    pygame.image.save(screen.subsurface(game_surface),
                      path+"/frame"+str(frame_num)+".jpg")
    run_frame(frame_num+1)


def run_frame(num):
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/run'+'/run_frame.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def get_run_frame():
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


def remove_run():
    shutil.rmtree('data/run')


def remove_train():
    shutil.rmtree('data/train')


def run_frame_load():
    cur_frame_num = get_run_frame()-1
    filepath = path.join(path.dirname(path.dirname(path.abspath(
        __file__))), 'data/run/frame'+str(cur_frame_num)+'.jpg')
    return Image.open(filepath)


def get_num_games():
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/num_games.txt')
    with(open(filepath, 'r')) as f:
        num = f.readline()
        f.close()
    if(num == ""):
        return 0
    else:
        return int(num)


def frame_load(num):
    cur_frame_num = get_frame_num(num)-1
    filepath = path.join(path.dirname(path.dirname(path.abspath(
        __file__))), 'data/train/game'+str(num)+'/frame'+str(cur_frame_num)+'.jpg')
    return Image.open(filepath)


def frame(num):
    game_num = get_num_games()
    # pong.debug(num)
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/frame_num.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def get_frame_num(game_num):
    #game_num = get_num_games()
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
    game_surface = pygame.Rect(0, 100, 640, 640)
    game_num = get_num_games()
    frame_num = get_frame_num(game_num)
    path = "data/train/game"+str(game_num)
    pygame.image.save(screen.subsurface(game_surface),
                      path+"/frame"+str(frame_num)+".jpg")
    frame(frame_num+1)


def score(num):
    game_num = get_num_games()
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/result.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def get_win(game_num):
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/result.txt')
    with(open(filepath, 'r')) as f:
        win = f.readline()
        f.close()
    return win


def ball_pos(ball):
    (angle, v) = ball.vector
    (x, y) = ball.rect.center
    data = (x, y, angle, v)
    result = ','.join(map(str, data))
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/ball_pos.txt')
    with open(filepath, 'w+') as f:
        f.write(result)
        f.close()


def pad_pos(computer, side):
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
    # pong.debug(data)
    return int(x), int(y)


def get_score(side):
    game_num = get_num_games()
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/score_')
    with open(filepath+side+'.txt', 'r') as f:
        score = f.readline()
        f.close()
    return int(score)


def update_numpy_log(message):
    dirpath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), "data/logs/np")
    if not path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = dirpath+"/train_log.txt"
    with open(filepath, 'a+') as f:
        f.write(str(message)+"\n")
        f.close()


def update_tf_log(message):
    dirpath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), "data/logs/tf")
    if not path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = dirpath+"/train_log.txt"
    with open(filepath, 'a+') as f:
        f.write(str(message)+"\n")
        f.close()


def write_tf_log(message):
    dirpath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), "data/logs/tf")
    if not path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = dirpath+"/train_log.txt"
    with open(filepath, 'w+') as f:
        f.write(str(message)+"\n")
        f.close()


def write_numpy_log(message):
    dirpath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), "data/logs/np")
    if not path.exists(dirpath):
        os.makedirs(dirpath)
    filepath = dirpath+"/train_log.txt"
    with open(filepath, 'w+') as f:
        f.write(str(message)+"\n")
        f.close()


def write_score(num, side):
    game_num = get_num_games()
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/score_')
    with open(filepath+side+'.txt', 'w+') as f:
        f.write(str(num))
        f.close()


def get_ball_pos():
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/ball_pos.txt')
    with open(filepath, 'r') as f:
        data = f.readline()
        f.close()
    [x, y, angle, v] = data.split(',')
    # pong.debug(data)
    return int(x), int(y), int(angle), float(v)

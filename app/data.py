import os.path as path
import os
from app import pong
import pygame
#from app import pong


def num_games(num):
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/num_games.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def get_num_games():
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/num_games.txt')
    with(open(filepath, 'r')) as f:
        num = f.readline()
        f.close()
    if(num==""):
        return 0
    else:
        return int(num)


def frame(num):
    game_num = get_num_games()
    # pong.debug(num)
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/train/game'+str(game_num)+'/frame_num.txt')
    with(open(filepath, 'w+')) as f:
        f.write(str(num))


def get_frame_num():
    game_num = get_num_games()
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
    game_surface = pygame.Rect(0, 100, 600, 600)
    game_num = get_num_games()
    frame_num = get_frame_num()
    path = "data/train/game"+str(game_num)
    pygame.image.save(screen.subsurface(game_surface),
                      path+"/frame"+str(frame_num)+".jpg")
    frame(frame_num+1)


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


def get_ball_pos():
    filepath = path.join(path.dirname(path.dirname(
        path.abspath(__file__))), 'data/ball_pos.txt')
    with open(filepath, 'r') as f:
        data = f.readline()
        f.close()
    [x, y, angle, v] = data.split(',')
    # pong.debug(data)
    return int(x), int(y), int(angle), float(v)

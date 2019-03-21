import math
import random
import pygame
import importlib
import app
#from app import models


def debug(var):
    with open("debug.txt", "a") as f:
        f.write(str(var))
        f.write("\n")
        f.close()
    return


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 10
        self.height = 10
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill([255, 255, 255])
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.area = pygame.Rect(0, 100, 800, 600)
        self.hit = 0
        self.vector = self.reset()

    def reset(self):
        init_angle = random.randrange(30, 45)
        if random.randrange(2) == 0:
            init_angle = -init_angle
        if random.randrange(2) == 0:
            init_angle += 180
        self.rect.x = random.randrange(200, 600)
        self.rect.y = random.randrange(200, 400)
        return (init_angle, 5.0)

    def calcnewpos(self, rect, vector):
        (angle, v) = vector
        (dx, dy) = (int(v*math.cos(math.radians(angle))),
                    int(v*math.sin(math.radians(angle))))
        return rect.move(dx, dy)

    def update(self, player1, player2):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if (tr and tl) or (br and bl):
                (angle, v) = self.vector
                angle = -angle
                self.vector = (angle, v)
            if tl and bl:
                player2.score += 1
                v = 5
                self.vector = self.reset()
            if tr and br:
                player1.score += 1
                v = 5
                self.vector = self.reset()
        else:
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                (angle, v) = self.vector
                angle = int(math.degrees(math.pi - math.radians(angle)))
                self.vector = (angle, v)
                self.hit = not self.hit
            elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                (angle, v) = self.vector
                angle = int(math.degrees(math.pi - math.radians(angle)))
                self.vector = (angle, v)
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit


class FastBall(Ball):
    def __init__(self):
        super().__init__()

    def update(self, player1, player2):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if (tr and tl) or (br and bl):
                (angle, v) = self.vector
                angle = -angle
                if v < 10:
                    v *= 1.02
                self.vector = (angle, v)
            if tl and bl:
                player2.score += 1
                v = 5
                self.vector = self.reset()
            if tr and br:
                player1.score += 1
                v = 5
                self.vector = self.reset()
        else:
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                (angle, v) = self.vector
                angle = int(math.degrees(math.pi - math.radians(angle)))
                if v < 2*player1.speed:
                    v *= 1.07
                self.vector = (angle, v)
                self.hit = not self.hit
            elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                (angle, v) = self.vector
                angle = int(math.degrees(math.pi - math.radians(angle)))
                if v < player2.speed:
                    v *= 1.07
                self.vector = (angle, v)
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit


class Pad(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.image = pygame.Surface([15, 75])
        self.image.fill([255, 255, 255])
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.area = pygame.Rect(0, 100, 800, 600)
        self.side = side
        self.speed = 10
        self.state = "still"
        self.reset()
        self.score = 0

    def reset(self):
        self.state = "still"
        self.movepos = [0, 0]
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        elif self.side == "right":
            self.rect.midright = self.area.midright

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveup(self):
        self.movepos[1] -= self.speed
        self.state = "moveup"

    def movedown(self):
        self.movepos[1] += self.speed
        self.state = "movedown"


class AI(Pad):
    def __init__(self, diff):
        super().__init__("right")
        self.name = self.model_select(diff)
        temp = importlib.import_module('models')
        self.model = getattr(temp, self.name)

    def predict(self):
        return self.model.get_prediction()

    def model_select(self, diff):
        if(diff == "Effortless"):
            return "hardcoded"

import math
import random
import pygame


def debug(var):
    with open("output.txt", "a") as f:
        f.write(str(var))
        f.write("\n")
        f.close()
    return


def model_select(diff):
    if(diff == "Effortless"):
        model = ""


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 10
        self.height = 10
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill([255, 255, 255])
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        #self.vector = (0.0, 5)
        self.hit = 0
        self.vector = self.reset()

    def reset(self):
        # self.vector = (0.0, 5)
        # why block multiples of 11?
        init_angle = random.randrange(-45, 45)
        if(not (init_angle % 11)):
            init_angle -= 1
        if random.randrange(2) == 0:
            init_angle = -init_angle
        if random.randrange(2) == 0:
            init_angle += 180
            if(not (init_angle % 11)):
                init_angle += 1
        self.rect.x = random.randrange(200, 600)
        self.rect.y = random.randrange(200, 400)
        return (init_angle, 5)
        # debug(self.vector[1])
        # debug("\n")
        #self.vector = (34.0, 5)

    def calcnewpos(self, rect, vector):
        (angle, v) = vector
        (dx, dy) = (v*math.cos(angle), v*math.sin(angle))
        return rect.move(dx, dy)

    def update(self, player1, player2):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        #(angle, v) = self.vector
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
                #angle = math.pi - angle
                player2.score += 1
                v = 5
                # scope error here
                self.vector = self.reset()
            if tr and br:
                #angle = math.pi - angle
                player1.score += 1
                v = 5
                self.vector = self.reset()
        else:
            #player1.rect.inflate(-3, -3)
            #player2.rect.inflate(-3, -3)
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                (angle, v) = self.vector
                angle = math.pi - angle
                if v < player1.speed:
                    v *= 1.05
                self.vector = (angle, v)
                self.hit = not self.hit
            elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                (angle, v) = self.vector
                angle = math.pi - angle
                if v < player2.speed:
                    v *= 1.08
                self.vector = (angle, v)
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit
        #self.vector = (angle, v)


class Pad(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.image = pygame.Surface([15, 75])
        self.image.fill([255, 255, 255])
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
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
        self.model = model_select(diff)

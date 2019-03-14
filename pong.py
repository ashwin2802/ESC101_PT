import math
import random
import pygame


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
        # self.x = 0
        # self.y = 0
        self.vector = (0.0, 0)
        self.hit = 0
        self.reset()

    def reset(self):
        self.rect.x = random.randrange(200, 600)
        self.rect.y = random.randrange(200, 400)
        self.vector = (math.radians(random.randrange(-45, 45)), 5)
        if random.randrange(2) == 0:
            (angle, v) = self.vector
            angle += 180
            self.vector = (angle, v)

    def calcnewpos(self, rect, vector):
        (angle, v) = vector
        (dx, dy) = (v*math.cos(angle), v*math.sin(angle))
        return rect.move(dx, dy)

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, v) = self.vector
        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if (tr and tl) or (br and bl):
                angle = -angle
            if tl and bl:
                angle = math.pi - angle
                player2.score += 1
                self.reset()
            if tr and br:
                angle = math.pi - angle
                player1.score += 1
                self.reset()
        else:
            player1.rect.inflate(-3, -3)
            player2.rect.inflate(-3, -3)
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit
        self.vector = (angle, v)


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


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pong")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)

    global player1
    global player2
    player1 = Pad("left")
    player2 = Pad("right")
    ball = Ball()
    players = pygame.sprite.RenderPlain((player1, player2))
    balls = pygame.sprite.RenderPlain(ball)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    game_over = False

    while 1:
        clock.tick(60)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1.moveup()
                if event.key == pygame.K_s:
                    player1.movedown()
                if event.key == pygame.K_UP:
                    player2.moveup()
                if event.key == pygame.K_DOWN:
                    player2.movedown()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1.movepos = [0, 0]
                    player1.state = "still"
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2.movepos = [0, 0]
                    player2.state = "still"
        if abs(player1.score-player2.score) > 3:
            game_over = True

        if game_over:
            text = font.render("Game Over", 1, (200, 200, 200))
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 50
            screen.blit(text, textpos)

        scoreprint = "P1: " + str(player1.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (200, 0)
        screen.blit(text, textpos)

        scoreprint = "P2: " + str(player2.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (600, 0)
        screen.blit(text, textpos)

        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        screen.blit(background, player2.rect, player2.rect)
        balls.update()
        players.update()
        balls.draw(screen)
        players.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()

import pygame
# change the name of this module
from app import players as p
import thorpy
from app import pong


def buttons(screen):
    again = thorpy.make_button("Play Again", func=more)
    leave = thorpy.make_button("Exit", func=thorpy.functions.quit_func)
    again.surface = screen
    leave.surface = screen
    box = thorpy.Box.make([again, leave])
    box.fit_children((30, 30))
    box.center()
    box.set_main_color((0, 0, 0, 0))
    menu = thorpy.Menu(box)
    menu.play()


def more():
    p.menu.play()


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 740))
    pygame.display.set_caption("Pong")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)

    global player1
    global player2
    player1 = pong.Pad("left")
    player2 = pong.Pad("right")
    ball = pong.FastBall()
    players = pygame.sprite.RenderPlain((player1, player2))
    balls = pygame.sprite.RenderPlain(ball)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    game_over = False

    while 1:
        # fix intialized angle of the ball
        # add function to change the angle of the ball on reflection
        # this was probably the diff function
        # diff function glitches, implement a new one
        # do we need the diff and speed ups? See original pong
        clock.tick(60)
        screen.fill((0, 0, 0))
        #  fix ball movement when the button is held for a long time
        pygame.key.set_repeat(100, 100)
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
            textpos.top = 150
            screen.blit(text, textpos)
            win_mess = "Player 1 wins!" if (
                player1.score > player2.score) else "Player 2 wins!"
            win_text = font.render(win_mess, 1, (200, 200, 200))
            winpos = win_text.get_rect(centerx=background.get_width()/2)
            winpos.top = 250
            screen.blit(win_text, winpos)
            buttons(screen)

        scoreprint = "P1: " + str(player1.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (100, 40)
        screen.blit(text, textpos)
        # five pixels unaccounted for somewhere, pad cant access them
        pygame.draw.line(screen, (255, 255, 255), (0, 95), (800, 95), 10)
        scoreprint = "P2: " + str(player2.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (300, 40)
        screen.blit(text, textpos)

        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        screen.blit(background, player2.rect, player2.rect)
        ball.update(player1, player2)
        players.update()
        balls.draw(screen)
        players.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()

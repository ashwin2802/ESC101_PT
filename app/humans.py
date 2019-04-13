# 2 player interface

import pygame
# change the name of this module
from app import players as p
import thorpy
from app import pong


def buttons(screen):
    # display for when the game gets over
    again = thorpy.make_button("Play Again", func=more)
    leave = thorpy.make_button("Exit", func=thorpy.functions.quit_func)

    # set screen attributes so that buttons display on same screen
    again.surface = screen
    leave.surface = screen

    # make a box containing the buttons
    box = thorpy.Box.make([again, leave])
    box.fit_children((30, 30))
    box.center()
    # black box
    box.set_main_color((0, 0, 0, 0))

    # add the box to the screen
    menu = thorpy.Menu(box)
    menu.play()


def more():
    # continue playing, goes back to the player selection window
    p.menu.play()


def main():
    # initialize pygame
    pygame.init()

    # create screen and background
    screen = pygame.display.set_mode((640, 740))
    pygame.display.set_caption("Pong")
    background = pygame.Surface(screen.get_size())

    # ensure background is of proper format (?) and set font
    background = background.convert()
    background.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)

    # create two keyboard-controllable Pads
    player1 = pong.Pad("left")
    player2 = pong.Pad("right")

    # create a ball
    ball = pong.FastBall()

    # group the pads
    players = pygame.sprite.RenderPlain((player1, player2))

    # group the ball
    balls = pygame.sprite.RenderPlain(ball)

    # add objects to the background
    screen.blit(background, (0, 0))

    # update the display
    pygame.display.flip()

    # set clock
    clock = pygame.time.Clock()

    # game isn't over yet
    game_over = False

    # control loop
    while 1:

        # set frame rate
        clock.tick(60)
        # black screen
        screen.fill((0, 0, 0))
        #  set repeat rate for keys, press event registers in intervals of 100 ms only
        pygame.key.set_repeat(100, 100)

        # event loop
        for event in pygame.event.get():

            # exit on quit event
            if event.type == pygame.QUIT:
                buttons(screen)

            # key is pressed
            elif event.type == pygame.KEYDOWN:

                # move the left pad if w or s is pressed
                if event.key == pygame.K_w:
                    player1.moveup()
                if event.key == pygame.K_s:
                    player1.movedown()

                # move the right pad if down or up arrow key is pressed
                if event.key == pygame.K_UP:
                    player2.moveup()
                if event.key == pygame.K_DOWN:
                    player2.movedown()

            # pressed key is released
            elif event.type == pygame.KEYUP:

                # stop moving left pad when w or s is released
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1.movepos = [0, 0]
                    player1.state = "still"

                # stop moving right pad when up or down arrow key is released
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2.movepos = [0, 0]
                    player2.state = "still"

        # game is over when one player reaches 21
        if player1.score >= 21 or player2.score >= 21:
            game_over = True

        # when game finishes
        if game_over:

            # create text
            text = font.render("Game Over", 1, (200, 200, 200))
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 150

            # show text on screen
            screen.blit(text, textpos)

            # create win message
            win_mess = "Player 1 wins!" if (
                player1.score > player2.score) else "Player 2 wins!"
            win_text = font.render(win_mess, 1, (200, 200, 200))
            winpos = win_text.get_rect(centerx=background.get_width()/2)
            winpos.top = 250

            # show win message on screen
            screen.blit(win_text, winpos)

            # show the continue and exit buttons
            more()

        # display live score for left pad
        scoreprint = "P1: " + str(player1.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (100, 40)
        screen.blit(text, textpos)

        # display live score for right pad
        scoreprint = "P2: " + str(player2.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (460, 40)
        screen.blit(text, textpos)

        # separate scoreboard and game area
        pygame.draw.line(screen, (255, 255, 255), (0, 95), (800, 95), 10)

        # show ball and pads on the background
        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        screen.blit(background, player2.rect, player2.rect)

        # call the updates
        ball.update(player1, player2)
        players.update()

        # draw the objects onto the screen
        balls.draw(screen)
        players.draw(screen)

        # update display
        pygame.display.flip()


if __name__ == '__main__':
    main()

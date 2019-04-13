# user vs computer interface

import pygame
from app import diff, data, pong
import thorpy


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
    # continue playing, goes back to the difficulty selection window
    diff.menu.play()


def main(lvl):
    # initialize pygame
    pygame.init()

    # create screen and background
    screen = pygame.display.set_mode((640, 740))
    pygame.display.set_caption("Pong")
    background = pygame.Surface(screen.get_size())

    # ensure background is of proper format (?) and set font
    background = background.convert()
    background.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)

    # create a keyboard-controlled pad
    player1 = pong.Pad("left")

    # create an AI pad of selected difficulty
    computer = pong.AI(lvl, "right")

    # create a ball
    ball = pong.Ball()

    # group the pads
    players = pygame.sprite.RenderPlain((player1, computer))

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
        #  set repeat rate for keys,
        #  press events register in intervals of 100 ms only
        pygame.key.set_repeat(100, 100)

        # display live score for user
        scoreprint = "You: " + str(player1.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (100, 40)
        screen.blit(text, textpos)

        # display live score for AI
        scoreprint = "Computer: " + str(computer.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (300, 40)
        screen.blit(text, textpos)

        # separate scoreboard and game area
        pygame.draw.line(screen, (255, 255, 255), (0, 95), (800, 95), 10)

        # show ball and pads on the background
        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        screen.blit(background, computer.rect, computer.rect)

        # store ball and pad positions
        data.ball_pos(ball)
        data.pad_pos(computer, "right")
        data.pad_pos(player1, "left")

        if(lvl == 'Hard' or lvl == "Expert" or lvl == "Legendary"):
            # take a screenshot of the screen for these levels
            data.run_scrot(screen)

        # get prediction from the AI
        action = computer.predict()

        # move the right pad based on AI's prediction
        if action == -1:
            computer.movedown()
        elif action == 1:
            computer.moveup()
        elif action == 0:
            computer.movepos = [0, 0]
            computer.state = "still"

        # event loop
        for event in pygame.event.get():
            # exit on quit event
            if event.type == pygame.QUIT:
                buttons(screen)

            # handle key events for user pad
            # key is pressed
            elif event.type == pygame.KEYDOWN:
                # move the left pad if w or s is pressed
                if event.key == pygame.K_w:
                    player1.moveup()
                if event.key == pygame.K_s:
                    player1.movedown()

            # pressed key is released
            elif event.type == pygame.KEYUP:

                # stop moving left pad when w or s is released
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1.movepos = [0, 0]
                    player1.state = "still"

        # game is over when one player reaches 21
        if player1.score >= 21 or computer.score >= 21:
            game_over = True

        # when game is over
        if game_over:

            # clean screenshots
            if(lvl == "Hard" or lvl == "Expert" or lvl == "Legendary"):
                data.remove_run()

            # create text
            text = font.render("Game Over", 1, (200, 200, 200))
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 150

            # show text on screen
            screen.blit(text, textpos)

            # create win message
            win_mess = "You win!" if (
                player1.score > computer.score) else "You lose!"
            win_text = font.render(win_mess, 1, (200, 200, 200))
            winpos = win_text.get_rect(centerx=background.get_width()/2)
            winpos.top = 250

            # show win message on screen
            screen.blit(win_text, winpos)

            # show the continue and exit buttons
            buttons(screen)

        # call the updates
        ball.update(player1, computer)
        players.update()

        # draw obkects onto the screen
        balls.draw(screen)
        players.draw(screen)

        # update the display
        pygame.display.flip()


if __name__ == "__main__":
    main(lvl=diff.sel_diff)

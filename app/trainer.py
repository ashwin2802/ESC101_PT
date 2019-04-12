# training interface

import pygame
from train_scripts import numpy_, tf_, torch_
from app import data, pong, agent


def main(exec_):
    # initialize pygame
    pygame.init()

    # create screen and background
    screen = pygame.display.set_mode((640, 740))
    pygame.display.set_caption("Pong")
    background = pygame.Surface(screen.get_size())

    # ensure background is black and of proper format (?)
    background = background.convert()
    background.fill((0, 0, 0))

    # get the model that is to be trained
    model = data.get_model()

    # set Font
    font = pygame.font.Font(None, 36)

    # if user chose to train themself, create a keyboard-controlled pad
    if(exec_ == "Human"):
        computer1 = pong.Pad("left")

    # if user chose to train model with AI, create a ball-following pad
    elif(exec_ == "AI"):
        computer1 = pong.AI("Normal", "left")

    # create pad controlled by model
    computer2 = pong.AI("Train "+str(model), "right")

    # create ball
    ball = pong.Ball()

    # group the pads
    players = pygame.sprite.RenderPlain((computer1, computer2))

    # group the ball
    balls = pygame.sprite.RenderPlain(ball)

    # add objects to the background
    screen.blit(background, (0, 0))

    # update the display
    pygame.display.flip()

    # set the clock
    clock = pygame.time.Clock()

    # game isn't over
    game_over = False

    # control loop
    while 1:
        # set frame rate
        clock.tick(60)

        # set black screen
        screen.fill((0, 0, 0))

        #  set repeat rate for keys, press event registers in intervals of 100 ms only
        pygame.key.set_repeat(100, 100)

        # display live score for left pad
        scoreprint = "1: " + str(computer1.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (100, 40)
        screen.blit(text, textpos)

        # display live score for right pad
        scoreprint = "2: " + str(computer2.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (300, 40)
        screen.blit(text, textpos)

        # separate scoreboard and game area
        pygame.draw.line(screen, (255, 255, 255), (0, 95), (800, 95), 5)

        # show ball and pads on the background
        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, computer1.rect, computer1.rect)
        screen.blit(background, computer2.rect, computer2.rect)

        # take screenshot of game area
        data.scrot(screen)

        # save ball and pad positions
        data.ball_pos(ball)
        data.pad_pos(computer1, "left")
        data.pad_pos(computer2, "right")

        # if left pad is AI, get prediction
        if(exec_ == "AI"):
            action1 = computer1.predict()

        # get prediction from right pad
        action2 = computer2.predict()

        # if left pad is AI, move based on prediction
        if(exec_ == "AI"):
            if action1 == -1:
                computer1.movedown()
            elif action1 == 1:
                computer1.moveup()
            elif action1 == 0:
                computer1.movepos = [0, 0]
                computer1.state = "still"

        # move right pad based on prediction
        if action2 == -1:
            computer2.movedown()
        elif action2 == 1:
            computer2.moveup()
        elif action2 == 0:
            computer2.movepos = [0, 0]
            computer2.state = "still"

        # store score
        data.write_score(computer1.score, "left")
        data.write_score(computer2.score, "right")

        # update the model
        if(model == "Numpy"):
            numpy_.update()
        if(model == "TF"):
            tf_.update()
        if(model == "Torch"):
            torch_.update()

        # event loop
        for event in pygame.event.get():
            # save and clean on quit
            if event.type == pygame.QUIT:
                if(model == "Numpy"):
                    numpy_.exit()
                if(model == "TF"):
                    tf_.exit()
                if(model == "Torch"):
                    torch_.exit()
                data.remove_train()
                return

            # if left pad is keyboard-controlled, handle key events
            if(exec_ == "Human"):
                # key is pressed
                if event.type == pygame.KEYDOWN:
                    # move the left pad if w or s is pressed
                    if event.key == pygame.K_w:
                        computer1.moveup()
                    if event.key == pygame.K_s:
                        computer2.movedown()

                # key is released
                elif event.type == pygame.KEYUP:
                    # stop moving left pad when w or s is released
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player1.movepos = [0, 0]
                        player1.state = "still"

        # game over when one pad reaches 21 or more score
        if computer1.score > 21 or computer2.score > 21:
            game_over = True

        # when the game is over
        if game_over:
            # get number of games played till now
            games_played = data.get_num_games()
            # store winner
            if(computer1.score > 21):
                data.score(1)
            else:
                data.score(2)

            # increment and store num of games played
            data.num_games(games_played+1)

            # call interface again. start a new game
            main(exec_)

        # call the updates
        ball.update(computer1, computer2)
        players.update()

        # draw the objects onto the screen
        balls.draw(screen)
        players.draw(screen)

        # update the display
        pygame.display.flip()


if __name__ == "__main__":
    main(agent.agent_)

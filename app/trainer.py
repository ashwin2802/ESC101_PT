import pygame
from train_scripts import numpy_, tf_, torch_
from app import data, pong, modtra
#import thorpy


def main(model):
    pygame.init()
    screen = pygame.display.set_mode((640, 740))
    pygame.display.set_caption("Pong")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)

    global computer1
    global computer2

    computer1 = pong.AI("Normal", "left")
    computer2 = pong.AI("Train "+str(model), "right")
    ball = pong.Ball()
    players = pygame.sprite.RenderPlain((computer1, computer2))
    balls = pygame.sprite.RenderPlain(ball)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    game_over = False

    while 1:
        clock.tick(60)
        screen.fill((0, 0, 0))
        pygame.key.set_repeat(100, 100)

        scoreprint = "1: " + str(computer1.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (100, 40)
        screen.blit(text, textpos)

        scoreprint = "2: " + str(computer2.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (300, 40)
        screen.blit(text, textpos)
        # five pixels unaccounted for somewhere, pad cant access them
        pygame.draw.line(screen, (255, 255, 255), (0, 95), (800, 95), 5)
        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, computer1.rect, computer1.rect)
        screen.blit(background, computer2.rect, computer2.rect)

        data.scrot(screen)
        data.ball_pos(ball)
        data.pad_pos(computer1, "left")
        data.pad_pos(computer2, "right")

        action1 = computer1.predict()
        action2 = computer2.predict()
        if action1 == -1:
            computer1.movedown()
        elif action1 == 1:
            computer1.moveup()
        elif action1 == 0:
            computer1.movepos = [0, 0]
            computer1.state = "still"
        if action2 == -1:
            computer2.movedown()
        elif action2 == 1:
            computer2.moveup()
        elif action2 == 0:
            computer2.movepos = [0, 0]
            computer2.state = "still"
        data.write_score(computer1.score, "left")
        data.write_score(computer2.score, "right")
        if(model == "Numpy"):
            numpy_.update()
        if(model == "TF"):
            tf_.update()
        if(model == "Torch"):
            torch_.update()
        # pong.debug(game_over)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if(model == "Numpy"):
                    numpy_.exit()
                if(model == "TF"):
                    tf_.exit()
                if(model == "Torch"):
                    torch_.exit()
                data.remove_train()
                return
        # pong.debug(computer1.score)
        # pong.debug(computer2.score)
        if computer1.score > 21 or computer2.score > 21:
            game_over = True

        if game_over:
            games_played = data.get_num_games()
            if(computer1.score > 21):
                data.score(1)
            else:
                data.score(2)
            data.num_games(games_played+1)
            main(model)

        ball.update(computer1, computer2)
        players.update()
        balls.draw(screen)
        players.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main(modtra.model)

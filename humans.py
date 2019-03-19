import pygame
import players
#import over
import pong


def _quit():
    players.menu.play()


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
    player1 = pong.Pad("left")
    player2 = pong.Pad("right")
    ball = pong.Ball()
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
                _quit()
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
            ball.vector = (0.0, 0)
            text = font.render("Game Over", 1, (200, 200, 200))
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 50
            screen.blit(text, textpos)
            over.main()

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
        ball.update(player1, player2
                    )
        players.update()
        balls.draw(screen)
        players.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()

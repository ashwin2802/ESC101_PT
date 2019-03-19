import thorpy
import players
import pygame


def spacedown(event):
    players.menu.play()


def main():
    space = thorpy.Reaction(reacts_to=pygame.KEYDOWN,
                            reac_func=spacedown, event_args={"key": pygame.K_SPACE})
    application = thorpy.Application((800, 600), "Pong")
    title = thorpy.make_text(text="PONG", font_size=50, font_color=(255, 0, 0))
    instr_text = "Press Space to Continue"
    instr = thorpy.make_text(
        text=instr_text, font_size=30, font_color=(0, 255, 0))
    elements = [title, instr]
    box = thorpy.Box.make(elements=elements)
    box.fit_children(margins=(30, 30))
    box.center()
    box.set_main_color((220, 220, 220, 180))
    background = thorpy.Background.make(
        color=(0, 0, 0), elements=[box])
    background.add_reaction(space)
    menu = thorpy.Menu(background)
    menu.play()
    background.blit()
    background.update()
    application.quit()


if __name__ == '__main__':
    main()

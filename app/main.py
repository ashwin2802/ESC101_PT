# main application screen

import thorpy
from app import players
import pygame


def spacedown(event):
    # executes the next screen when space is pressed
    # players.menu.play()
    players.menu.play()


def main():

    # create a reaction that calls the function when space is pressed
    space = thorpy.Reaction(reacts_to=pygame.KEYDOWN,
                            reac_func=spacedown, event_args={"key": pygame.K_SPACE})

    # initialize the window
    application = thorpy.Application((640, 740), "Pong")

    # create all elements
    title = thorpy.make_text(text="PONG", font_size=50, font_color=(255, 0, 0))
    instr_text = "Press Space to Play"
    instr = thorpy.make_text(
        text=instr_text, font_size=30, font_color=(0, 255, 0))
    elements = [title, instr]

    # make a box to add the elements
    box = thorpy.Box.make(elements=elements)
    box.fit_children(margins=(30, 30))
    box.center()
    box.set_main_color((220, 220, 220, 180))

    # generate background and add element box to it
    background = thorpy.Background.make(
        color=(0, 0, 0), elements=[box])

    # add reaction to window
    background.add_reaction(space)
    menu = thorpy.Menu(background)

    # activate the objects
    menu.play()

    # display the background on the window
    background.blit()

    # refresh to check for key events
    background.update()

    # exit the application once focus from child window returns
    application.quit()


if __name__ == '__main__':
    main()

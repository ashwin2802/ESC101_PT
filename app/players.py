from app import diff, humans
import thorpy
import pygame


def player():
    humans.main()


def computer():
    diff.menu.play()


application = thorpy.Application((800, 600), "Players")
instr_text = "Play versus:"
instr = thorpy.make_text(
    text=instr_text, font_size=50, font_color=(0, 255, 0))
human = thorpy.make_button("Human", func=player)
comp = thorpy.make_button("Computer", func=computer)
elements = [instr, human, comp]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])
menu = thorpy.Menu(background)

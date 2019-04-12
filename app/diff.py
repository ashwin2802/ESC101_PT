import thorpy
from app import comp


def lvl1():
    sel_diff = "Effortless"
    comp.main(sel_diff)


def lvl2():
    sel_diff = "Easy"
    comp.main(sel_diff)


def lvl3():
    sel_diff = "Normal"
    comp.main(sel_diff)


def lvl4():
    sel_diff = "Hard"
    comp.main(sel_diff)


def lvl5():
    sel_diff = "Expert"
    comp.main(sel_diff)


def lvl6():
    sel_diff = "Legendary"
    comp.main(sel_diff)


# make a training interface that gives the option of train with AI or human


application = thorpy.Application((640, 740), "Level")
instr_text = "Select Difficulty"
instr = thorpy.make_text(
    text=instr_text, font_size=50, font_color=(0, 255, 0))
level_1 = thorpy.make_button("Effortless", func=lvl1)
level_2 = thorpy.make_button("Easy", func=lvl2)
level_3 = thorpy.make_button("Normal", func=lvl3)
level_4 = thorpy.make_button("Hard", func=lvl4)
level_5 = thorpy.make_button("Expert", func=lvl5)
level_6 = thorpy.make_button("Legendary", func=lvl6)
elements = [instr, level_1, level_2, level_3, level_4, level_5, level_6]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])
menu = thorpy.Menu(background)

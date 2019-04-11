import thorpy
from app import comp, trainer


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


def lvl0():
    trainer.main()


application = thorpy.Application((800, 600), "Level")
instr_text = "Select Difficulty"
instr = thorpy.make_text(
    text=instr_text, font_size=50, font_color=(0, 255, 0))
level_0 = thorpy.make_button("Train", func=lvl0)
level_1 = thorpy.make_button("Effortless", func=lvl1)
level_2 = thorpy.make_button("Easy", func=lvl2)
level_3 = thorpy.make_button("Normal", func=lvl3)
level_4 = thorpy.make_button("Hard", func=lvl4)
elements = [instr, level_0, level_1, level_2, level_3, level_4]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])
menu = thorpy.Menu(background)

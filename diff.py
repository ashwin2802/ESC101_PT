import thorpy
import comp


def lvl1():
    comp.main("Effortless")


def lvl2():
    comp.main("Easy")


application = thorpy.Application((800, 600), "Level")
instr_text = "Select Difficulty"
instr = thorpy.make_text(
    text=instr_text, font_size=50, font_color=(0, 255, 0))
level_1 = thorpy.make_button("Effortless", func=lvl1)
level_2 = thorpy.make_button("Easy", func=lvl2)
elements = [instr, level_1, level_2]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])
menu = thorpy.Menu(background)

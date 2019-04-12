import thorpy
from app import modtra, diff


def train():
    modtra.menu.play()


def play():
    diff.menu.play()


application = thorpy.Application((640, 740), "T or P")
instr_text = "Train Models or Play?"
instr = thorpy.make_text(
    text=instr_text, font_size=50, font_color=(0, 255, 0))
sel_train = thorpy.make_button("Train", func=train)
sel_play = thorpy.make_button("Play", func=play)
elements = [instr, sel_train, sel_play]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])
menu = thorpy.Menu(background)

# choose whether to train or play with the AI

import thorpy
from app import modtra, diff


def train():
    # executes next screen if user wants to train models
    modtra.menu.play()


def play():
    # executes diffculty select screen if user wants to play with AI
    diff.menu.play()


# create the application
application = thorpy.Application((640, 740), "Pong")

# create text element
instr_text = "Train Models or Play?\n"
instr = thorpy.make_text(
    text=instr_text, font_size=50, font_color=(0, 255, 0))

# create buttons
sel_train = thorpy.make_button("Train", func=train)
sel_play = thorpy.make_button("Play", func=play)

# add elements to box
elements = [instr, sel_train, sel_play]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))

# add elements to background
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])
menu = thorpy.Menu(background)

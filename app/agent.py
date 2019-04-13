# choose whether to train or play with the AI

import thorpy
from app import trainer


def self_():
    # executes trainer with one keyboard-controllable pad and one AI pad
    agent_ = "Human"
    trainer.main(agent_)


def game():
    # executes trainer with both AI pads
    agent_ = "AI"
    trainer.main(agent_)


# create the application
application = thorpy.Application((640, 740), "Pong")

# create text element
instr_text = "Train Models with AI or with Player?\n"
instr = thorpy.make_text(
    text=instr_text, font_size=30, font_color=(0, 255, 0))

# create buttons
sel_self = thorpy.make_button("AI", func=game)
sel_game = thorpy.make_button("Player", func=self_)

# add elements to box
elements = [instr, sel_self, sel_game]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))

# add elements to background
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])
menu = thorpy.Menu(background)

# screen for selecting number of players

from app import humans, torp
import thorpy


def player():
    # executes the 2 player interface when the button is pressed
    humans.main()


def computer():
    # executes next screen when the button is pressed
    torp.menu.play()


# create application
application = thorpy.Application((640, 740), "Pong")

# create text elements
instr_text = "Choose Opponent:"
instr = thorpy.make_text(
    text=instr_text, font_size=50, font_color=(50, 100, 50))

# create buttons
human = thorpy.make_button("Player", func=player)
comp = thorpy.make_button("Computer", func=computer)

# make a box and add all elements
elements = [instr, human, comp]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))

# add box to the background
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])

# add escape function
background.add_reaction(esc)

menu = thorpy.Menu(background)

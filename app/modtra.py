import thorpy
from app import agent, data


def train0():
    # remember model choice
    data.model_write("Numpy")
    # execute next screen
    agent.menu.play()


def train1():
    # remember model choice
    data.model_write("TF")
    # execute next screen
    agent.menu.play()


# def train2():
#     # remember model choice
#     data.model_write("Torch")
#     # execute next screen
#     agent.menu.play()


# create application
application = thorpy.Application((640, 740), "Pong")

# create text elements
instr_text = "Select Model\n"
instr = thorpy.make_text(
    text=instr_text, font_size=50, font_color=(0, 255, 0))

# create buttons
train_0 = thorpy.make_button("Train Numpy", func=train0)
train_1 = thorpy.make_button("Train TF", func=train1)
# train_2 = thorpy.make_button("Train Torch", func=train2)

# add elements to box
elements = [instr, train_0, train_1]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))

# add box to background
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])
menu = thorpy.Menu(background)

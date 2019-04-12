import thorpy
from app import trainer


def train0():
    model = "Numpy"
    trainer.main(model)


def train1():
    model = "TF"
    trainer.main(model)


def train2():
    model = "Torch"
    trainer.main(model)


application = thorpy.Application((640, 740), "Model")
instr_text = "Select Model"
instr = thorpy.make_text(
    text=instr_text, font_size=50, font_color=(0, 255, 0))
train_0 = thorpy.make_button("Train Numpy", func=train0)
train_1 = thorpy.make_button("Train TF", func=train1)
train_2 = thorpy.make_button("Train Torch", func=train2)
elements = [instr, train_0, train_1, train_2]
box = thorpy.Box.make(elements)
box.fit_children((30, 30))
box.center()
box.set_main_color((220, 220, 220, 180))
background = thorpy.Background.make(color=(0, 0, 0), elements=[box])
menu = thorpy.Menu(background)


train_0 = thorpy.make_button("Train Numpy", func=train0)
train_1 = thorpy.make_button("Train TF", func=train1)
train_2 = thorpy.make_button("Train Torch", func=train2)

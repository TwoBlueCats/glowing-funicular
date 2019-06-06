import typing
from typing import Optional, Callable
from PIL import Image, ImageTk
import tkinter as tk
from defs import *

root: Optional[tk.Tk] = None
bg_canvas: Optional[tk.Label] = None
label_items: typing.List[tk.Label] = []
image_ref: Optional[tk.Image] = None
running: Optional[Callable[[], None]] = None
item_binds: typing.Dict[tk.Misc, typing.Set[str]] = dict()


def __addBind(item: tk.Misc, seq: str, func: Callable[[tk.Event], None], *args, **kwargs) -> None:
    item.bind(seq, func)
    item_binds[item].add(seq)


def __clearBind(item: tk.Misc):
    for sequence in item_binds[item]:
        item.unbind(sequence)
    item_binds[item].clear()


def __destroy(item: tk.Misc):
    item_binds.pop(item)
    for child in item.winfo_children():
        __destroy(child)
    item.destroy()


def destroyEvent(event: tk.Event):
    global root
    if root:
        __destroy(root)
    root = None


def init() -> None:
    global root
    global bg_canvas
    global label_items

    root = tk.Tk()
    item_binds[root] = set()
    root.title("Glowing funicular")

    bg_canvas = tk.Canvas()
    item_binds[bg_canvas] = set()
    bg_canvas.pack(side='top', fill='both', expand='yes')

    for item in label_items:
        item.destroy()
    label_items = []


def setBgImage(image_name: str) -> None:
    global root
    global bg_canvas
    global image_ref

    __destroy(bg_canvas)

    img = Image.open(image_name)
    img = img.resize((w, h), Image.ANTIALIAS)
    image_ref = ImageTk.PhotoImage(img)

    root.geometry("%dx%d" % (w, h))

    bg_canvas = tk.Canvas(width=w, height=h, bg='black')
    item_binds[bg_canvas] = set()
    bg_canvas.create_image(0, 0, image=image_ref, anchor='nw')
    bg_canvas.pack(side='top', fill='both', expand='yes')

    bg_canvas.update_idletasks()
    root.update_idletasks()


def addText(text: str, x: int, y: int, color="black"):
    global label_items
    bg_canvas.create_text(x, y, text=text, fill=color, anchor='nw')


def addTextCenter(text: str, line: int, color="black"):
    if line < 0:
        line -= 1
        line = lineCnt + line
    x_pos = CenterX(text) * charSize

    addText(text, x_pos, line * charSize, color=color)


def addGameBind(sequence: str, func: Callable[[tk.Event], None], *args, **kwargs) -> None:
    global root
    __addBind(root, sequence, func, *args, **kwargs)


def gameClearBinds():
    global root
    __clearBind(root)


def setRunningFunc(to_run: Optional[Callable[[], None]] = None):
    global running
    running = to_run


def start() -> None:
    global root
    if running:
        root.after(100, running)
    root.mainloop()
    print("Mainloop ended")


def after(delay, func, *args, **kwargs):
    global root
    root.after(delay, func, *args, **kwargs)

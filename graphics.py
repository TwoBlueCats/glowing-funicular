import typing
from PIL import Image, ImageTk
import tkinter as tk
from defs import *

root: tk.Tk = None
bg_canvas: tk.Label = None
label_items: typing.List[tk.Label] = []
imgae_ref: tk.Image = None



def skipEvents(event : tk.Event):
    pass
    
def init() -> None:
    global root
    global bg_canvas
    global label_items

    root = tk.Tk()
    root.title("Glowing funicular")

    bg_canvas = tk.Canvas()
    bg_canvas.pack(side='top', fill='both', expand='yes')
    
    for item in label_items:
        item.destroy()
    label_items = []


def setBgImage(image_name: str) -> None:
    global root
    global bg_canvas
    global imgae_ref

    bg_canvas.destroy()
    
    img = Image.open(image_name)
    img = img.resize((w,h), Image.ANTIALIAS)
    imgae_ref = ImageTk.PhotoImage(img)
    
    print(image_name, w, h)

    root.geometry("%dx%d" % (w, h))

    bg_canvas = tk.Canvas(width=w, height=h, bg='black')

    bg_canvas.create_image(0, 0, image=imgae_ref, anchor='nw')
    bg_canvas.pack(side='top', fill='both', expand='yes')
    
    bg_canvas.update_idletasks()
    root.update_idletasks()

def addText(text: str, x: int, y: int, color="black") -> tk.Label:
    global label_items
    print(x, y, text)
    item = bg_canvas.create_text(x, y, text=text, fill=color, anchor='nw')
    label_items.append(item)
    return item

def addTextCenter(text: str, line: int, color="black") -> tk.Label:
    if line < 0:
        line -= 1
        line = lineCnt + line
        
    x_pos = w // 2 - len(text) // 2 * charSize
    
    addText(text, x_pos, line * charSize, color=color)

def DisplyTitle() -> None:
    setBgImage("./images/title.png")
    addTextCenter("Copyright (C) 2019, by Anikushin Anton", -2, color="yellow")

def start() -> None:
    global root
    root.mainloop()
    print("Mainloop ended")


def testFunc():
    init()
    setBgImage("./images/title.png")
    
    addTextCenter("Dungeon funicular", 0, color="red")
    addTextCenter("Dungeon funicular", -3, color="red")
    
    start()

def __main():
    init()
    DisplyTitle()
    start()
    
if __name__ == "__main__":
    __main()

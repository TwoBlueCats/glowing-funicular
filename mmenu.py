from enum import Enum
import graphics
from defs import *

MMenuItems = ["New Game    ",
              "Load Game   ",
              "Instructions",
              "Quit        "
              ]
mid_x = CenterX(sorted(MMenuItems, key=lambda x: -len(x))[0])
mid_y = CenterY(len(MMenuItems) * 2)


def GetMenuItem(item: str) -> int:
    return MMenuItems.index(item)


def DrawMenu(id_x: int = 0, x=mid_x, y=mid_y):
    def change(text, flag):
        if flag:
            pass
            # text = "->" + text + "<-"
        return text

    colors = ["gray", "white"]
    for i in range(len(MMenuItems)):
        print(i)
        graphics.addTextCenter(change(MMenuItems[i], i == id_x), y, color=colors[i == id_x])
        y += 2
    return


def MainMenu():
    graphics.setBgImage("./images/mainback.bmp")

    mtitle = "Dungeon of funicular v." + str(version)
    tx = CenterX(mtitle) * charSize
    ty = 10 * charSize
    graphics.addText(mtitle, tx + 1, ty + 1, color="black")
    graphics.addText(mtitle, tx, ty, color="yellow")

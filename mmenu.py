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
    colors = ["gray", "white"]
    graphics.deleteAllText()
    for i in range(len(MMenuItems)):
        graphics.addTextCenter(MMenuItems[i], y, color=colors[i == id_x])
        y += 2

    mtitle = "Dungeon of funicular v." + str(version)
    tx = CenterX(mtitle) * charSize
    ty = 10 * charSize
    graphics.addTextShadow(mtitle, tx, ty, color="yellow")

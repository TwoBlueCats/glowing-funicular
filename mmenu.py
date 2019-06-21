from enum import Enum
import graphics
from defs import *
from typing import Tuple

MMenuItems: Tuple[str, str, str, str] = ("New Game    ",
                                         "Load Game   ",
                                         "Instructions",
                                         "Quit        "
                                         )

mid_x: int = CenterX(sorted(MMenuItems, key=lambda x: -len(x))[0])
mid_y: int = CenterY(len(MMenuItems) * 2)


def GetMenuItem(item: str) -> int:
    return MMenuItems.index(item)


def DrawMenu(id_x: int = 0, x: int = mid_x, y: int = mid_y) -> None:
    colors = ["gray", "white"]
    graphics.deleteAllText()
    for i in range(len(MMenuItems)):
        graphics.addTextShadow(MMenuItems[i], x * charSize, y * charSize, color=colors[i == id_x])
        y += 2

    mtitle = "Dungeon of funicular v." + str(version)
    tx = CenterX(mtitle) * charSize
    ty = 10 * charSize
    graphics.addTextShadow(mtitle, tx, ty, color="yellow")

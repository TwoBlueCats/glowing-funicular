import typing
from typing import List
import tkinter as tk

import graphics
import mmenu


def DisplayBindFunc(ev: tk.Event):
    print(ev)
    graphics.after(10, MainMenu)


def MainMenuBindFunc(ev: tk.Event, id_x: List[int]) -> None:
    sym = ev.__getattribute__("keysym")

    if sym == "Return":
        if id_x == 0:
            pass  # new game
        elif id_x == 1:
            pass  # load game
        elif id_x == 2:
            pass  # instructions
        elif id_x == 3:
            graphics.destroyEvent(ev)
        graphics.after(10, nextFunc)

    if sym == "Up":
        id_x[0] = (id_x[0] - 1) % 4
        graphics.after(1, mmenu.DrawMenu, id_x[0])
    if sym == "Down":
        id_x[0] = (id_x[0] + 1) % 4
        graphics.after(1, mmenu.DrawMenu, id_x[0])


def nextFunc():
    print("next function here")
    graphics.destroyEvent(tk.Event())


def DisplyTitle() -> None:
    graphics.setBgImage("./images/title.bmp")
    graphics.addTextCenter("Copyright (C) 2019, by Anikushin Anton", -2, color="yellow")

    done = False
    graphics.addGameBind("<Escape>", graphics.destroyEvent)
    graphics.addGameBind("<Key>", DisplayBindFunc)


def MainMenu():
    graphics.gameClearBinds()
    id_x = [0]
    mmenu.MainMenu()
    mmenu.DrawMenu(id_x=id_x[0])

    graphics.addGameBind("<Escape>", graphics.destroyEvent)
    graphics.addGameBind("<Key>", lambda e: MainMenuBindFunc(e, id_x))


graphics.init()
graphics.setRunningFunc(DisplyTitle)
graphics.start()

import typing
from typing import List
import tkinter as tk

import graphics
import mmenu
import character
from wrapper import MutableWrapper

person: MutableWrapper = MutableWrapper()


def addGenerationPromt() -> None:
    prompt = "Press <r> to roll again, <enter> to accept, <esc> to exit to menu."
    tx, ty = graphics.CenterX(prompt) * graphics.charSize, (graphics.lineCnt - 7) * graphics.charSize
    graphics.addTextShadow(prompt, tx, ty)


def DisplayBindFunc(ev: tk.Event) -> None:
    print(ev)
    graphics.after(10, MainMenu)


def MainMenuBindFunc(ev: tk.Event, id_x: MutableWrapper) -> None:
    sym: str = ev.__getattribute__("keysym")
    print(sym, ev)
    if sym == "Return":
        if id_x == 0:
            graphics.after(10, CharacterGeneration)
        elif id_x == 1:
            pass  # load game
        elif id_x == 2:
            pass  # instructions
        elif id_x == 3:
            print(id_x)
            graphics.destroyEvent(ev)
        return

    if sym == "Up":
        id_x[0] = (id_x[0] - 1) % 4
        graphics.after(1, mmenu.DrawMenu, id_x.value)
    if sym == "Down":
        id_x[0] = (id_x[0] + 1) % 4
        graphics.after(1, mmenu.DrawMenu, id_x.value)


def CharacterGenerationBindFunc(ev: tk.Event, char: character.Character) -> None:
    sym: str = ev.__getattribute__("keysym")

    if sym.lower() == "r":
        char.SelfRegenerate()
        graphics.deleteAllText()
        graphics.after(1, char.PrintStats)
        graphics.after(1, addGenerationPromt)
    if sym == "Return":
        pass  # all is done
        graphics.after(1, nextFunc)
    if sym == "Escape":
        graphics.after(1, MainMenu)


def nextFunc() -> None:
    print("next function here")
    graphics.destroyEvent(tk.Event())


def DisplyTitle() -> None:
    graphics.gameClearBinds()
    graphics.setBgImage("./images/title.bmp")
    graphics.addTextCenter("Copyright (C) 2019, by Anikushin Anton", -2, color="yellow")

    graphics.addGameBind("<Escape>", graphics.destroyEvent)
    graphics.addGameBind("<Key>", DisplayBindFunc)


def MainMenu() -> None:
    graphics.gameClearBinds()
    graphics.setBgImage("./images/mainback.bmp")

    id_x: MutableWrapper = MutableWrapper(0)
    mmenu.DrawMenu(id_x=id_x.value)

    graphics.addGameBind("<Escape>", graphics.destroyEvent)
    graphics.addGameBind("<Key>", lambda e: MainMenuBindFunc(e, id_x))


def CharacterGeneration() -> None:
    global person
    graphics.gameClearBinds()
    graphics.setBgImage("./images/charback.bmp")

    if person:
        del person.value

    person.value = character.Character()

    name: str = "Great Tester"
    # print(tx, len(prompt), graphics.colsCnt, graphics.w)
    person.SetName(name)
    person.SelfRegenerate()

    addGenerationPromt()
    person.PrintStats()

    graphics.addGameBind("<Key>", lambda e: CharacterGenerationBindFunc(e, person))


graphics.init()
graphics.setRunningFunc(DisplyTitle)
graphics.start()

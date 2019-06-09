import typing
from typing import List, Tuple
import random

import graphics
from defs import *


class CharacterInfo:
    def __init__(self):
        self.name: str = ""
        self.strength: List[int] = [0, 0]
        self.stamina: List[int] = [0, 0]
        self.dexterity: List[int] = [0, 0]
        self.agility: List[int] = [0, 0]
        self.intelligence: List[int] = [0, 0]

        self.currHp: int = 0
        self.maxHp: int = 0

        self.unarmed_combat: List[int] = [0, 0]
        self.armed_combat: List[int] = [0, 0]
        self.projectile_combat: List[int] = [0, 0]
        self.magic_combat: List[int] = [0, 0]
        self.combat_defense: List[int] = [0, 0]
        self.magic_defense: List[int] = [0, 0]

        self.currXp: int = 0
        self.totXp: int = 0
        self.currGold: int = 0
        self.totGold: int = 0

        self.loc_x: int = 0
        self.loc_y: int = 0

    @property
    def str(self):
        return self.strength[0]

    @property
    def sta(self):
        return self.stamina[0]

    @property
    def dex(self):
        return self.dexterity[0]

    @property
    def agi(self):
        return self.agility[0]

    @property
    def int(self):
        return self.intelligence[0]

    @property
    def unarmed(self):
        return self.unarmed_combat[0]

    @property
    def armed(self):
        return self.armed_combat[0]

    @property
    def projectile(self):
        return self.projectile_combat[0]

    @property
    def magic(self):
        return self.magic_combat[0]

    @property
    def defense(self):
        return self.combat_defense[0]

    @property
    def mag_def(self):
        return self.magic_defense[0]


class Character:
    def __init__(self):
        self._info = CharacterInfo()

    def PrintStats(self, back: bool = False):
        if back:
            graphics.setBgImage("./images/charback.bmp")
        local_title = f"{self._info.name.strip()}: Attributes and Skills"
        row = 8
        ty = row * charSize
        tx = CenterX(local_title) * charSize
        graphics.addTextShadow(local_title, tx, ty)

        tx = 70
        row += 4
        messages: List[str] = []
        messages += [f"Strength:       {self._info.str}"]
        messages += [f"Stamina:        {self._info.sta}"]
        messages += [f"Dexterity:      {self._info.dex}"]
        messages += [f"Agility:        {self._info.agi}"]
        messages += [f"Intelligence:   {self._info.int}"]
        messages += [f"Hit Points:     {self._info.currHp}"]

        messages += [f"Unarmed Combat:      {self._info.unarmed}"]
        messages += [f"Armed Combat:        {self._info.armed}"]
        messages += [f"Projectile Combat:   {self._info.projectile}"]
        messages += [f"Magic Combat:        {self._info.magic}"]
        messages += [f"Combat Defense:      {self._info.defense}"]
        messages += [f"Magic Defense:       {self._info.mag_def}"]

        messages += [f"Experience:   {self._info.currXp}"]
        messages += [f"Gold:         {self._info.currGold}"]

        for mes in messages:
            ty = row * charSize
            graphics.addTextShadow(mes, tx, ty)
            row += 2
            row += mes.startswith("Hit")
            row += mes.startswith("Magic Defense")

    def SetName(self, name):
        self._info.name = name

    def SelfRegenerate(self):
        self._info.strength[0] = random.randint(1, 20)
        self._info.stamina[0] = random.randint(1, 20)
        self._info.dexterity[0] = random.randint(1, 20)
        self._info.agility[0] = random.randint(1, 20)
        self._info.intelligence[0] = random.randint(1, 20)

        self._info.currHp = self._info.str + self._info.sta
        self._info.maxHp = self._info.currHp

        self._info.unarmed_combat[0] = self._info.str + self._info.agi
        self._info.armed_combat[0] = self._info.str + self._info.dex
        self._info.projectile_combat[0] = self._info.dex + self._info.int
        self._info.magic_combat[0] = self._info.int + self._info.sta
        self._info.combat_defense[0] = self._info.str + self._info.agi
        self._info.magic_defense[0] = self._info.agi + self._info.int

        self._info.currXp = random.randint(100, 200)
        self._info.totXp = self._info.currXp

        self._info.currGold = random.randint(50, 100)
        self._info.totGold = self._info.currGold

        self._info.loc_x = 0
        self._info.loc_y = 0

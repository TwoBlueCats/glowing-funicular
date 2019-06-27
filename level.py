import typing
from typing import Optional, List, Tuple
import random
from defs import *
import character
import enum
import graphics


class TerraType(enum.IntEnum):
    floor = 0
    wall = 1
    door_open = 2
    door_closed = 3
    stair_up = 4
    stair_down = 5

    @classmethod
    def get(cls, val):
        for tr in cls:
            if tr.value == val:
                return tr


class Coordinates:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y


class RoomDimension:
    def __init__(self, wi: int = 0, he: int = 0, c: Optional[Coordinates] = None):
        self.width: int = wi
        self.height: int = he
        if not c:
            c = Coordinates()
        self.coord: Coordinates = c


class RoomType:
    def __init__(self, wi: int = 0, he: int = 0):
        self.room_dim: RoomDimension = RoomDimension(wi, he)
        self.top_left: Coordinates = Coordinates()
        self.bot_right: Coordinates = Coordinates()


class CellType:
    def __init__(self):
        self.coord: Coordinates = Coordinates()
        self.room_id: int = empty_cell


class MapInfo:
    def __init__(self):
        self.terr_id: TerraType = TerraType.floor
        self.has_monster: bool = False
        self.monster_id: int = -1
        self.has_item: bool = False
        self.visible: bool = False
        self.seen: bool = False


class LevelInfo:
    def __init__(self):
        self.level_num: int = 1
        self.map: List[List[MapInfo]] = [[]]

    def resize(self, n: int, m: int) -> None:
        if len(self.map) != 0:
            raise ValueError("Resize not empty level")

        for i in range(n):
            self.map.append([])
            for j in range(m):
                self.map[i].append(MapInfo())
                self.map[i][j].terr_id = TerraType.wall

    def clear(self) -> None:
        self.map = []

    def set_level(self, level: int) -> None:
        self.level_num = level

    def __getitem__(self, item) -> List[MapInfo]:
        return self.map[item]

    def __setitem__(self, key, value) -> None:
        self.map[key] = value

    def __len__(self):
        return len(self.map)

    def __str__(self) -> str:
        text = f"Level id: {self.level_num}"
        lines: List[str] = []
        for line in self.map:
            lines.append("".join(
                '#' if item.terr_id == TerraType.wall else 'D' if item.terr_id == TerraType.door_closed else '.' for
                item in line))
        return "\n".join([text] + lines)


class Level:
    def __init__(self, person: Optional[character.Character] = None):
        self._char: Optional[character.Character] = person
        self._room_nums: int = 0
        self._rooms: List[RoomType] = []
        self._grid: List[List[CellType]] = []
        self._info: LevelInfo = LevelInfo()
        self._blocking_tiles: List[TerraType] = [TerraType.wall, TerraType.door_closed, ]
        self._label_map: List[List[graphics.LABEL]] = []

    def GenerateDungeonLevel(self) -> "Level":
        self._info.clear()
        self._info.resize(map_w, map_h)
        self._InitGrid()
        self._DrawMapToArray()
        return self

    def _InitGrid(self):
        self._room_nums = random.randint(min_room_num, max_room_num)
        for i in range(self._room_nums):
            wi = random.randint(min_room_size, max_room_size)
            he = random.randint(min_room_size, max_room_size)
            new_room = RoomType(wi, he)
            self._rooms.append(new_room)

        for i in range(gw):
            self._grid.append([])
            for j in range(gh):
                cell = CellType()
                cell.coord.x = 1 + cell_size * i
                cell.coord.y = 1 + cell_size * j
                self._grid[-1].append(cell)

        for i in range(self._room_nums):
            x = random.randint(0, gw - 1)
            y = random.randint(0, gh - 1)
            while self._grid[x][y].room_id != -1:
                x = random.randint(0, gw - 1)
                y = random.randint(0, gh - 1)

            self._rooms[i].room_dim.coord.x = self._grid[x][y].coord.x + (self._rooms[i].room_dim.width // 2)
            self._rooms[i].room_dim.coord.y = self._grid[x][y].coord.y + (self._rooms[i].room_dim.height // 2)
            # Set the room rect
            self._rooms[i].top_left.x = self._grid[x][y].coord.x
            self._rooms[i].top_left.y = self._grid[x][y].coord.y
            self._rooms[i].bot_right.x = self._grid[x][y].coord.x + self._rooms[i].room_dim.width
            self._rooms[i].bot_right.y = self._grid[x][y].coord.y + self._rooms[i].room_dim.height
            self._grid[x][y].room_id = i

    def _DrawMapToArray(self):
        for x in range(self._rooms[0].top_left.x + 1, self._rooms[0].bot_right.x):
            for y in range(self._rooms[0].top_left.y + 1, self._rooms[0].bot_right.y):
                self._info[x][y].terr_id = TerraType.floor

        for i in range(1, self._room_nums):
            for x in range(self._rooms[i].top_left.x + 1, self._rooms[i].bot_right.x):
                for y in range(self._rooms[i].top_left.y + 1, self._rooms[i].bot_right.y):
                    self._info[x][y].terr_id = TerraType.floor
            self._ConnectRooms(i, i - 1)
        self._AddDoors()

        x: int = self._rooms[1].room_dim.coord.x + self._rooms[1].room_dim.width // 2
        y: int = self._rooms[1].room_dim.coord.y + self._rooms[1].room_dim.height // 2
        self._char.loc_x = x - 1
        self._char.loc_y = y - 1
        self._info[self._char.loc_x][self._char.loc_y].terr_id = TerraType.stair_up
        x: int = self._rooms[-1].room_dim.coord.x + self._rooms[-1].room_dim.width // 2
        y: int = self._rooms[-1].room_dim.coord.y + self._rooms[-1].room_dim.height // 2
        self._info[x - 1][y - 1].terr_id = TerraType.stair_down  # TODO battery item here

    def _ConnectRooms(self, cur: int, prev: int):
        cur_cell: Coordinates = self._rooms[cur].room_dim.coord
        prev_cell: Coordinates = self._rooms[prev].room_dim.coord

        dx = 1 if cur_cell.x < prev_cell.x else -1

        was_wall = False
        x = cur_cell.x
        for x_in in irange(cur_cell.x + dx, prev_cell.x, dx):
            if self._info[x_in][cur_cell.y].terr_id == TerraType.wall:
                was_wall = True
            if self._info[x_in][cur_cell.y].terr_id == TerraType.floor and was_wall:
                return
            self._info[x_in][cur_cell.y].terr_id = TerraType.floor
            x = x_in

        dy = 1 if cur_cell.y < prev_cell.y else -1
        was_wall = False
        for y in irange(cur_cell.y + dy, prev_cell.y, dy):
            if self._info[x][y].terr_id == TerraType.wall:
                was_wall = True
            if self._info[x][y].terr_id == TerraType.floor and was_wall:
                return
            self._info[x][y].terr_id = TerraType.floor

    def _AddDoors(self):
        for i in range(self._room_nums):
            self._AddDoor(i)

    def _AddDoor(self, index: int):
        for col in irange(self._rooms[index].top_left.x, self._rooms[index].bot_right.x):
            dd1 = self._rooms[index].top_left.y
            dd2 = self._rooms[index].bot_right.y
            if self._info[col][dd1].terr_id == TerraType.floor:
                self._info[col][dd1].terr_id = TerraType.door_closed
            if self._info[col][dd2].terr_id == TerraType.floor:
                self._info[col][dd2].terr_id = TerraType.door_closed

        for row in irange(self._rooms[index].top_left.y, self._rooms[index].bot_right.y):
            dd1 = self._rooms[index].top_left.x
            dd2 = self._rooms[index].bot_right.x
            if self._info[dd1][row].terr_id == TerraType.floor:
                self._info[dd1][row].terr_id = TerraType.door_closed
            if self._info[dd2][row].terr_id == TerraType.floor:
                self._info[dd2][row].terr_id = TerraType.door_closed

    def _CalcLOS(self):
        for i in range(map_w):
            for j in range(map_h):
                self._info[i][j].visible = False
        v: int = view_w // 2
        h: int = view_h // 2

        x1: int = max(self._char.loc_x - v, 1)
        y1: int = max(self._char.loc_y - h, 1)

        x2: int = min(self._char.loc_x + v, map_w - 1)
        y2: int = min(self._char.loc_y + h, map_h - 1)

        for x in irange(x1, x2):
            for y in irange(y1, y2):
                if not self._info[x][y].visible:
                    if self._CanSee(x, y):
                        self._info[x][y].visible = True
                        self._info[x][y].seen = True

        for i in irange(x1, x2):
            for j in irange(y1, y2):
                if self._IsBlocking(i, j) and not self._info[i][j].visible:
                    x, y = i, j - 1
                    if 0 <= x <= map_w and 0 <= y <= map_h:
                        if self._info[x][y].terr_id == TerraType.floor and self._info[x][y].visible:
                            self._info[i][j].visible = True
                            self._info[i][j].seen = True

    def _CanSee(self, x: int, y: int) -> bool:
        dist = Distance((x, y), self._char.loc)

        answer = False
        if dist <= view_h:
            answer = self._LineOfSight((x, y), self._char.loc)
        return answer

    def _LineOfSight(self, fr: Tuple[int, int], to: Tuple[int, int]) -> bool:
        dx = abs(fr[0] - to[0])
        dy = abs(fr[1] - to[1])
        mi = min(dx, dy)
        ma = max(dx, dy)

        numtiles = ma + 1
        d = 2 * mi - ma
        dinc1 = mi << 1
        dinc2 = (mi - ma) << 1
        xinc1 = dx == ma
        yinc1 = dy == ma
        xinc2 = yinc2 = 1

        if fr[0] > to[0]:
            xinc1 *= -1
            xinc2 *= -1
        if fr[1] > to[1]:
            yinc1 *= -1
            yinc2 *= -1

        x, y = fr
        for _ in irange(2, numtiles):
            if self._IsBlocking(x, y):
                return False
            if d < 0:
                d += dinc1
                x += xinc1
                y += yinc1
            else:
                d += dinc2
                x += xinc2
                y += yinc2
        return True

    def _IsBlocking(self, x: int, y: int) -> bool:
        terra = self._info[x][y].terr_id
        if self._info[x][y].has_monster:
            return True
        return terra in self._blocking_tiles

    def _CheckLabels(self):
        try:
            self._label_map[0][0]["text"]
        except Exception as err:
            del self._label_map
            self._label_map = []
            for x in range(view_w):
                self._label_map.append([])
                for y in range(view_h):
                    self._label_map[-1].append(graphics.addText("", (y + 1) * charSize, (x + 1) * charSize))

    def _DrawMapFromCoords(self, i: int, j: int):
        self._CheckLabels()
        for x in range(view_w):
            for y in range(view_h):
                pass

    def DrawMap(self):
        self._CalcLOS()

        i: int = self._char.loc_x - view_w // 2
        j: int = self._char.loc_y - view_h // 2
        i = max(0, min(i, map_w - 1))
        j = max(0, min(j, map_h - 1))

        self._DrawMapFromCoords(i, j)


if __name__ == "__main__":
    Level(character.Character()).GenerateDungeonLevel()

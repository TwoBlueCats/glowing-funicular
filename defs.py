import typing

""" Global """
width: int = 680  # 850
height: int = 480  # 600

charSize: int = 8
lineCnt: int = height // charSize
colsCnt: int = width // charSize

version: str = "0.0.0"

""" Map """
max_room_size: int = 6
min_room_size: int = 4
max_room_num: int = 5
min_room_num: int = 4

view_w: int = 40
view_h: int = 55

empty_cell: int = -1  # fake room index

map_w: int = 64 - 8
map_h: int = 64 - 8

cell_size: int = 8

gw: int = map_w // cell_size  # grid_w
gh: int = map_h // cell_size  # grid_h


def CenterX(text: str) -> int:
    return colsCnt // 2 - len(text) // 2


def CenterY(n: int) -> int:
    return lineCnt // 2 - n // 2


def irange(a: int, b: typing.Optional[int] = None, c: typing.Optional[int] = None):
    if b is None:
        return range(a + 1)
    if c is None:
        return range(a, b + 1)
    if c > 0:
        b += 1
    else:
        b -= 1
    return range(a, b, c)


def Distance(a: typing.Tuple[int, int], b: typing.Tuple[int, int]) -> int:
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return (dx + dy + max(dx, dy)) // 2

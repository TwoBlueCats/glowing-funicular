import typing

w: int = 680   # 850
h: int = 480   # 600

charSize: int = 8
lineCnt: int = h // charSize
colsCnt: int = w // charSize

version: str = "0.0.0"


def CenterX(text: str) -> int:
    return colsCnt // 2 - len(text) // 2


def CenterY(n: int) -> int:
    return lineCnt // 2 - n // 2

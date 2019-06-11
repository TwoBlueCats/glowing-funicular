import typing

# w, h = 680, 480
w: int = 850
h: int = 600
charSize: int = 8
lineCnt: int = h // charSize
colsCnt: int = w // charSize

version: str = "0.0.0"


def CenterX(text: str) -> int:
    return colsCnt // 2 - len(text) // 2


def CenterY(n: int) -> int:
    return lineCnt // 2 - n // 2

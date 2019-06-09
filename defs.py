w, h = 680, 480
charSize = 8
lineCnt = h // charSize
colsCnt = w // charSize


def CenterX(text: str) -> int:
    return colsCnt // 2 - len(text) // 2


def CenterY(n: int) -> int:
    return lineCnt // 2 - n // 2


version = "0.0.0"

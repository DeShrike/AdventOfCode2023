from math import gcd
from typing import Iterator

def modify_bit(self, number: int, bit: int, value: int) -> int:
    m = 1 << bit
    return (number & ~m) | ((value << bit) & m)

def lcm(a: int, b: int) -> int:
    """
    Calculate the LCM of 2 numbers.
    """
    return abs(a * b) // gcd(a, b)

def terminal_size() -> tuple[int, int]:
    import fcntl, struct, termios
    return struct.unpack('HHHH', fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0)))[:2]

def sumrange(c: int) -> int:
    """
    Calculate 1 + 2 + 3 + 4 + ... + c
    """
    return c * (c + 1) / 2

def dirange(start: int, end: int = None, step: int = 1) -> Iterator[int]:
    """
    Directional, inclusive range. This range function is an inclusive version of
    :class:`range` that figures out the correct step direction to make sure that it goes
    from `start` to `end`, even if `end` is before `start`.
    >>> dirange(2, -2)
    [2, 1, 0, -1, -2]
    >>> dirange(-2)
    [0, -1, -2]
    >>> dirange(2)
    [0, 1, 2]
    """
    assert step > 0
    if end is None:
        start, end = 0, start

    if end >= start:
        yield from range(start, end + 1, step)
    else:
        yield from range(start, end - 1, -step)

def isingrid(x: int, y: int, width: int, height: int) -> bool:
    """
    Returns True if position (x, y) is inside a grid with size (width, height).
    """
    return x >= 0 and x < width and y >= 0 and y < height

def neighbours8(x: int, y: int, size: tuple[int, int] = None) -> Iterator[tuple[int, int]]:
    """
    Returns the 8 neighbours of a cell in a 2D grid.
    """
    dirs = [(1, 0), (1, 1), (0, 1), (-1, 1),(-1, 0), (-1, -1), (0, -1), (1, -1)]
    for dir in dirs:
        xx = x + dir[0]
        yy = y + dir[1]
        if size != None and not isingrid(xx, yy, size[0], size[1]):
            continue
        yield (xx, yy)
 
def neighbours4(x: int, y: int, size: tuple[int, int] = None) -> Iterator[tuple[int, int]]:
    """
    Return the 4 neighbours in cardinal directions of a cell in a 2D grid.
    """
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for dir in dirs:
        xx = x + dir[0]
        yy = y + dir[1]
        if size != None and not isingrid(xx, yy, size[0], size[1]):
            continue
        yield (xx, yy)

def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    """
    Calculate the Manhattan distance between 2 points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def isbetween(v: int, a: int, b: int) -> bool:
    """
    Check if v is between a and b, exclusive.
    """
    if a > b: a, b = b, a
    return a < v < b

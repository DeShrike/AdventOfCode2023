from math import gcd
import fcntl, struct, termios

def modify_bit(self, number:int, bit: int, value: int) -> int:
	m = 1 << bit
	return (number & ~m) | ((value << bit) & m)

def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)

def terminal_size():
    return struct.unpack('HHHH', fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0)))[:2]

def sumrange(c:int) -> int:
    """
    Calculate 1 + 2 + 3 + 4 + ... + c
    """
    return c * (c + 1) / 2

def dirange(start, end=None, step:int=1):
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

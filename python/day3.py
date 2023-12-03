from aoc import Aoc
from utilities import isingrid, dirange
import sys

# Day 3
# https://adventofcode.com/2023

class Number():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.number = ""
        self.symbols = []

    def __repr__(self):
        return f"{self.number} ({self.x},{self.y}) {self.symbols}"


class Day3Solution(Aoc):

    def Run(self):
        self.StartDay(3, "Gear Ratios")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(3)

        goal = self.TestDataA()
        self.PartA()
        self.Assert(self.GetAnswerA(), goal)

        goal = self.TestDataB()
        self.PartB()
        self.Assert(self.GetAnswerB(), goal)

    def TestDataA(self):
        self.inputdata.clear()
        testdata = \
        """
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 4361

    def TestDataB(self):
        self.inputdata.clear()
        self.TestDataA()
        return 467835

    def Neighbours(self, x: int, y: int, l: int, w: int, h: int):
        for yy in dirange(y - 1, y + 1):
            for xx in dirange(x - 1, x + l):
                if isingrid(xx, yy, w, h):
                    yield xx, yy

    def ParseInput(self):
        numbers = []
        gears = {}
        w = len(self.inputdata[0])
        h = len(self.inputdata)
        n = None
        for y in range(h):
            for x in range(w):
                if self.inputdata[y][x].isdigit():
                    if n is None:
                        n = Number(x, y)
                        numbers.append(n)
                    n.number += self.inputdata[y][x]
                else:
                    if n is not None:
                        n = None

        for num in numbers:
            for nx, ny in self.Neighbours(num.x, num.y, len(num.number), w, h):
                if self.inputdata[ny][nx] != "." and not self.inputdata[ny][nx].isdigit():
                    num.symbols.append(self.inputdata[ny][nx])
                    if self.inputdata[ny][nx] == "*":
                        if (nx, ny) in gears:
                            gears[(nx, ny)].append(int(num.number))
                        else:
                            gears[(nx, ny)] = [int(num.number)]

        return numbers, gears

    def PartA(self):
        self.StartPartA()

        numbers, _ = self.ParseInput()
        answer = sum([int(n.number) for n in numbers if len(n.symbols) > 0])

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        _, gears = self.ParseInput()
        answer = sum([g[0] * g[1] for g in gears.values() if len(g) == 2])

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day3Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


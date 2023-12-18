from aoc import Aoc
from canvas import Canvas
from utilities import neighbours8
import re
import sys

# Day 18
# https://adventofcode.com/2023

class Dig():
    def __init__(self, line: str) -> None:
        rx = re.compile("^(?P<dir>[RDLU]) (?P<dist>[0-9]*) \(#(?P<r>[a-f0-9]{2})(?P<g>[a-f0-9]{2})(?P<b>[a-f0-9]{2})\)$")
        match = rx.search(line)
        if match:
            self.dir = match["dir"]
            self.dist = int(match["dist"])
            self.r = int("0x" + match["r"], 16)
            self.g = int("0x" + match["g"], 16)
            self.b = int("0x" + match["b"], 16)
        else:
            raise Exception("Parse Failed: " + line)

    def __str__(self) -> str:
        return f"{self.dir} {self.dist} {self.r} {self.g} {self.b}"

    def GetPositions(self, pos):
        dirs = { "R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1) }
        for i in range(self.dist):
            yield (pos[0] + (i + 1) * dirs[self.dir][0], pos[1] + (i + 1) * dirs[self.dir][1])

class Day18Solution(Aoc):

    def Run(self):
        self.StartDay(18, "Lavaduct Lagoon")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(18)

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
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 62

    def TestDataB(self):
        self.inputdata.clear()
        # self.TestDataA()    # If test data is same as test data for part A
        testdata = \
        """
        1000
        2000
        3000
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return None

    def ParseInput(self):
        # rx = re.compile("^(?P<from>[A-Z0-9]{3}) = \((?P<left>[A-Z0-9]{3}), (?P<right>[A-Z0-9]{3})\)$")
        # match = rx.search(line)
        # pos = match["from"]

        data = []
        for line in self.inputdata:
            data.append(Dig(line))

        return data

    def CreatePng(self, grid, pngname: str) -> None:
        w = len(grid[0])
        h = len(grid)
        boxsize = 5
        canvas = Canvas(w * boxsize, h * boxsize)

        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c is not None:
                    canvas.set_big_pixel(x * boxsize, y * boxsize, c, boxsize)

        print(f"Saving {pngname}")
        canvas.save_PNG(pngname)

    def FindExtent(self, digs):
        maxx = -1_000_000
        maxy = -1_000_000
        minx = 1_000_000
        miny = 1_000_000
        current = (0, 0)
        for dig in digs:
            for pos in dig.GetPositions(current):
                current = pos
                maxx = max(maxx, current[0])
                maxy = max(maxy, current[1])
                minx = min(minx, current[0])
                miny = min(miny, current[1])
        w = maxx - minx + 1 + 2
        h = maxy - miny + 1 + 2
        ox = -minx + 1
        oy = -miny + 1
        return w, h, ox, oy
    
    def Floodfill(self, grid):
        h = len(grid)
        w = len(grid[0])
        q = [(0, 0)]
        while len(q) > 0:
            current = q.pop()
            for n in neighbours8(current[0], current[1], (w, h)):
                if grid[n[1]][n[0]] == None:
                    grid[n[1]][n[0]] = (0, 0, 0)
                    q.append(n)

    def PartA(self):
        self.StartPartA()

        digs = self.ParseInput()

        answer = None

        w, h, ox, oy = self.FindExtent(digs)
        grid = [[None for x in range(w)] for y in range(h)]

        current = (0, 0)
        for dig in digs:
            for pos in dig.GetPositions(current):
                current = pos
                x = current[0] + ox
                y = current[1] + oy
                grid[y][x] = (dig.r, dig.g, dig.b)

        self.Floodfill(grid)

        answer = sum([len([True for c in row if c != (0, 0, 0)]) for row in grid])

        self.CreatePng(grid, "day18a.png")

        # Add solution here

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        #data = self.ParseInput()
        answer = None

        # Add solution here

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day18Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


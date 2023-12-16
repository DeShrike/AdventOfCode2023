from aoc import Aoc
from utilities import isingrid
from canvas import Canvas
import sys

# Day 16
# https://adventofcode.com/2023

bloks = {
    "|": [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    "-": [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    "/": [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ],
    "\\": [
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
    ],
    ".": [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    "+": [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    "H": [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    "V": [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
}

boxsize = 5


class Beam():
    directions = [(1,0), (0, 1), (-1, 0), (0, -1) ]
    vertical = [1, 3]
    horizontal = [0, 2]

    def __init__(self, x: int, y: int, direction: int) ->None:
        self.x = x
        self.y = y
        self.ox = x
        self.oy = y
        self.direction = direction
        self.active = True

    def __str__(self) -> str:
        dir = [">", "v", "<", "^"][self.direction]
        return f"({self.x},{self.y} {dir} {'active' if self.active else 'done  '})"

    def Move(self, w: int, h: int, grid, path: list[tuple[int, int]]):
        self.x += Beam.directions[self.direction][0]
        self.y += Beam.directions[self.direction][1]

        if not isingrid(self.x, self.y, w, h):
            self.active = False
            return None
        path.append((self.x, self.y))

        c = grid[self.y][self.x]
        if c == "|":
            if self.direction in Beam.vertical:
                return None
            self.direction = (self.direction + 1) % 4
            newbeam = Beam(self.x, self.y, (self.direction + 2) % 4)
            return newbeam

        if c == "-":
            if self.direction in Beam.horizontal:
                return None
            self.direction = (self.direction + 1) % 4
            newbeam = Beam(self.x, self.y, (self.direction + 2) % 4)
            return newbeam
            
        if c == "/":
            if self.direction in Beam.vertical:
                self.direction = (self.direction + 1) % 4
            else:
                self.direction = (self.direction - 1) % 4

        if c == "\\":
            if self.direction in Beam.vertical:
                self.direction = (self.direction - 1) % 4
            else:
                self.direction = (self.direction + 1) % 4

        if c == ".":
            if self.direction in Beam.horizontal:
                grid[self.y][self.x] = "H"
            if self.direction in Beam.vertical:
                grid[self.y][self.x] = "V"
        elif c == "V":
            if self.direction in Beam.horizontal:
                grid[self.y][self.x] = "+"
        elif c == "H":
            if self.direction in Beam.vertical:
                grid[self.y][self.x] = "+"

        return None

class Day16Solution(Aoc):

    def Run(self):
        self.StartDay(16, "The Floor Will Be Lava")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(16)

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
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\\
        ..../.\\\\..
        .-.-/..|..
        .|....-|.\\
        ..//.|....
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 46

    def TestDataB(self):
        self.TestDataA()
        return 51

    def DrawBlok(self, canvas: Canvas, x: int, y: int, bloksize: int, symbol: str, color = (0, 0, 0)) -> None:
        b = bloks[symbol]
        xx = x * bloksize * 5
        yy = y * bloksize * 5
        for yyy, row in enumerate(b):
            for xxx, c in enumerate(row):
                if c == 1:
                    canvas.set_big_pixel(xx + xxx * bloksize, yy + yyy * bloksize, color, bloksize)

    def ParseInput(self):
        data = []
        for line in self.inputdata:
            data.append([c for c in line])

        return data

    def FindEnergized(self, grid, startx: int, starty: int, startdir: int) -> list[tuple[int, int]]:
        path = []
        w = len(grid[0])
        h = len(grid)
        beams = [ Beam(startx, starty, startdir) ]

        while True:
            beam = next(filter(lambda b: b.active, beams), None)
            if beam is None:
                break
            newbeam = beam.Move(w, h, grid, path)
            if newbeam is not None:
                if not any([b for b in beams if b.ox == newbeam.ox and b.oy == newbeam.oy]):
                    beams.append(newbeam)
                else:
                    beam.active = False
                    newbeam = None
            # self.PrintGrid(grid, path)
            # print(beam)
            # if newbeam is not None: print(newbeam)
            # a = input()

        return path

    def PrintGrid(self, grid, path) -> None:
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c in ["/", "-", "|", "\\"]:
                    print(c, end="")
                elif (x, y) in path:
                    print("#", end="")
                else:
                    print(".", end="")
            print("")

    def CreatePng(self, grid, pngname: str) -> None:
        w = len(grid[0])
        h = len(grid)
        canvas = Canvas(w * boxsize * 5, h * boxsize * 5)

        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                xx = x * 3 + 1
                yy = y * 3 + 1
                if c in ["V", "H", "+"]:
                    color = (255, 0, 0)
                else:
                    color = (255, 255, 255)
                self.DrawBlok(canvas, x, y, boxsize, c, color)

        print(f"Saving {pngname}")
        canvas.save_PNG(pngname)

    def PartA(self):
        self.StartPartA()

        grid = self.ParseInput()
        path = self.FindEnergized(grid, -1, 0, 0)
        answer = len(set(path))

        self.CreatePng(grid, "day16a.png")

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        tests = []  # [(startx, starty, count, direction), ...]
        grid = self.ParseInput()
        w = len(grid[0])
        h = len(grid)
        for x in range(w):
            grid = self.ParseInput()
            path = self.FindEnergized(grid, x, -1, 1)
            count = len(set(path))
            tests.append((x, -1, count, 1))

            grid = self.ParseInput()
            path = self.FindEnergized(grid, x, h, 3)
            count = len(set(path))
            tests.append((x, h, count, 3))

        for y in range(h):
            grid = self.ParseInput()
            path = self.FindEnergized(grid, -1, y, 0)
            count = len(set(path))
            tests.append((-1, y, count, 0))

            grid = self.ParseInput()
            path = self.FindEnergized(grid, w, y, 2)
            count = len(set(path))
            tests.append((w, y, count, 2))

        tests.sort(key=lambda t: t[2])
        answer = tests[-1][2]

        grid = self.ParseInput()
        path = self.FindEnergized(grid, tests[-1][0], tests[-1][1], tests[-1][3])
        count = len(set(path))
        self.CreatePng(grid, "day16b.png")

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day16Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


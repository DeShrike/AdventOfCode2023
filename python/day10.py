from aoc import Aoc
from utilities import isingrid, neighbours8
from canvas import Canvas
import sys

# Day 10
# https://adventofcode.com/2023

bloks = {
    "|": [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ],
    "-": [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    "F": [
        [0, 0, 0],
        [0, 1, 1],
        [0, 1, 0],
    ],
    "L": [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ],
    "7": [
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
    ],
    "J": [
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0],
    ],
    ".": [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
}

connections = {
    (1, 0):  { 
        "-": ["-", "J", "7"],
        "|": [],
        "7": [],
        "J": [],
        "F": ["-", "J", "7"],
        "L": ["-", "J", "7"],
    },
    (-1, 0):  { 
        "-": ["-", "L", "F"],
        "|": [],
        "7": ["-", "L", "F"],
        "J": ["-", "L", "F"],
        "F": [],
        "L": [],
    },
    (0, -1):  { 
        "-": [],
        "|": ["|", "F", "7"],
        "7": [],
        "J": ["|", "F", "7"],
        "F": [],
        "L": ["|", "F", "7"],
    },
    (0, 1):  { 
        "-": [],
        "|": ["|", "J", "L"],
        "7": ["|", "J", "L"],
        "J": [],
        "F": ["|", "J", "L"],
        "L": []
    },
}

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

boxsize = 5

class Day10Solution(Aoc):

    def Run(self):
        self.StartDay(10, "Pipe Maze")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(10)

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
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 8

    def TestDataB(self):
        self.inputdata.clear()
        testdata = \
        """
        .F----7F7F7F7F-7....
        .|F--7||||||||FJ....
        .||.FJ||||||||L7....
        FJL7L7LJLJ||LJ.L-7..
        L--J.L7...LJS7F-7L7.
        ....F-J..F7FJ|L7L7L7
        ....L7.F7||L7|.L7L7|
        .....|FJLJ|FJ|F7|.LJ
        ....FJL-7.||.||||...
        ....L---J.LJ.LJLJ...
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 8

    def ParseInput(self):
        w = len(self.inputdata[0])
        h = len(self.inputdata)
        pos = None
        grid = []
        for y, line in enumerate(self.inputdata):
            row = []
            grid.append(row)
            for x, c in enumerate(line):
                row.append(c)
                if c == "S":
                    pos = (x, y)

        left = right = up = down = None

        xx = pos[0] + 1
        yy = pos[1] + 0
        if isingrid(xx, yy, w, h):
            right = grid[yy][xx]
        xx = pos[0] - 1
        yy = pos[1] + 0
        if isingrid(xx, yy, w, h):
            left = grid[yy][xx]
        xx = pos[0] + 0
        yy = pos[1] + 1
        if isingrid(xx, yy, w, h):
            down = grid[yy][xx]
        xx = pos[0] + 0
        yy = pos[1] - 1
        if isingrid(xx, yy, w, h):
            up = grid[yy][xx]

        possibilities = []
        if up in ["7","F","|"]:
            possibilities.append(["|","L","J"])
        if down in ["|","L","J"]:
            possibilities.append(["7","F","|"])
        if right in ["-","7","J"]:
            possibilities.append(["F","L","-"])
        if left in ["-","L","F"]:
            possibilities.append(["-","7","J"])

        s = set(possibilities[0]).intersection(set(possibilities[1]))
        grid[pos[1]][pos[0]] = list(s)[0]
        return (w, h), pos, grid

    def DrawBlok(self, canvas: Canvas, x: int, y: int, bloksize: int, symbol: str, color = (0, 0, 255)) -> None:
        b = bloks[symbol]
        xx = x * bloksize * 3
        yy = y * bloksize * 3
        for yyy, row in enumerate(b):
            for xxx, c in enumerate(row):
                if c == 1:
                    canvas.set_big_pixel(xx + xxx * bloksize, yy + yyy * bloksize, color, bloksize)

    def CalculatePath(self, size, startpos, grid):
        pos = list(startpos)
        dix = 0
        lastdix = None
        path = []
        canvas = Canvas(size[0] * boxsize * 3, size[1] * boxsize * 3)
        while True:
            while True:
                xx = pos[0] + dirs[dix][0]
                yy = pos[1] + dirs[dix][1]
                if isingrid(xx, yy, size[0], size[1]) and lastdix != dix:
                    c = grid[pos[1]][pos[0]]
                    n = grid[yy][xx]
                    if n in connections[dirs[dix]][c]:
                        pos = (xx, yy)
                        lastdix = (dix + 2) % 4
                        dix = (dix + 1) % 4
                        break
                dix = (dix + 1) % 4
            self.DrawBlok(canvas, pos[0], pos[1], boxsize, grid[pos[1]][pos[0]])
            path.append(pos)
            
            if pos == startpos:
                break

        return canvas, path

    def Floodfill(self, grid):
        h = len(grid)
        w = len(grid[0])

        q = [(0, 0)]
        while len(q) > 0:
            current = q.pop()
            for n in neighbours8(current[0], current[1], (w, h)):
                if grid[n[1]][n[0]] == 0:
                    grid[n[1]][n[0]] = 2
                    q.append(n)

    def PartA(self):
        self.StartPartA()

        size, startpos, grid = self.ParseInput()
        canvas, path = self.CalculatePath(size, startpos, grid)

        pngname = "day10a.png"
        print(f"Saving {pngname}")
        canvas.save_PNG(pngname)

        answer = len(path) // 2
        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        size, startpos, grid = self.ParseInput()
        canvas, path = self.CalculatePath(size, startpos, grid)

        newgrid = [[0 for _ in range(size[0] * 3)] for _ in range(size[1] * 3)]
        for pos in path:
            x = pos[0]
            y = pos[1]
            c = grid[y][x]
            b = bloks[c]
            for yy, row in enumerate(b):
                for xx, cc in enumerate(row):
                    if cc == 1:
                        newgrid[y * 3 + yy][x * 3 + xx] = 1


        self.Floodfill(newgrid)

        for y in range(size[1]):
            for x in range(size[0]):
                xx = x * 3 + 1
                yy = y * 3 + 1
                if newgrid[yy][xx] == 2:
                    grid[y][x] == 2

        answer = 0
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                xx = x * 3 + 1
                yy = y * 3 + 1
                if newgrid[yy][xx] == 0:
                    answer += 1
                    self.DrawBlok(canvas, x, y, boxsize, ".", (0, 255, 0))
                elif newgrid[yy][xx] == 2:
                    self.DrawBlok(canvas, x, y, boxsize, ".", (255, 0, 0))

        pngname = "day10b.png"
        print(f"Saving {pngname}")
        canvas.save_PNG(pngname)

        # Attempt 1: 610 is too high
        # Attempt 2: 357 is correct

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day10Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


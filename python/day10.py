from aoc import Aoc
from utilities import isingrid
import itertools
import math
import re
import sys

# Day 10
# https://adventofcode.com/2023


connections = {
    (1, 0): ("-", "J", "7"),
    (-1, 0): ("-", "L", "F"),
    (0, 1): ("|", "L", "J"),
    (0, -1): ("|", "7", "F")
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

        testdatax = \
        """
        -L|F7
        7S-7|
        L|7||
        -L-J|
        L|-JF
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 8

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
    
    def PartA(self):
        self.StartPartA()

        answer = 0
        size, startpos, grid = self.ParseInput()
        pos = list(startpos)
        dix = 0
        lastdix = None
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
            answer += 1
            if pos == startpos:
                break

        answer = answer // 2

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        # Add solution here

        answer = None

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day10Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


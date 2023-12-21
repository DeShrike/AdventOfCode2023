from aoc import Aoc
from utilities import neighbours4
import itertools
import sys

# Day 21
# https://adventofcode.com/2023

class Day21Solution(Aoc):

    def Run(self):
        self.StartDay(21, "Step Counter")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(21)

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
        ...........
        .....###.#.
        .###.##..#.
        ..#.#...#..
        ....#.#....
        .##..S####.
        .##..#...#.
        .......##..
        .##.#.####.
        .##..##.##.
        ...........
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 42

    def TestDataB(self):
        self.TestDataA()
        return None

    def ParseInput(self):
        start = None
        data = []
        for y, line in enumerate(self.inputdata):
            if "S" in line:
                start = (line.index("S"), y)
            data.append([c for c in line])

        return data, start

    def Walk(self, grid, start):
        w = len(grid[0])
        h = len(grid)
        newgrid = [[0 for _ in range(w)] for _ in range(h)]
        q = [start]
        while len(q) > 0:
            current = q.pop(0)
            d = newgrid[current[1]][current[0]]
            for n in neighbours4(*current, (w, h)):
                if grid[n[1]][n[0]] == "#":
                    continue
                if newgrid[n[1]][n[0]] != 0:
                    continue
                newgrid[n[1]][n[0]] = d + 1
                q.append(n)
        return newgrid

    def PartA(self):
        self.StartPartA()

        grid, start = self.ParseInput()
        newgrid = self.Walk(grid, start)

        answer = 0
        for row in newgrid:
            for c in row:
                if c > 64 or c == 0 or c % 2 == 1:
                    pass
                else:
                    answer += 1

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        steps = 26_501_365
        grid, start = self.ParseInput()




        answer = None
        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day21Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


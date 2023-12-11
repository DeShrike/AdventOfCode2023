from aoc import Aoc
from utilities import dirange, manhattan_distance
import itertools
import sys

# Day 11
# https://adventofcode.com/2023

class Day11Solution(Aoc):

    def Run(self):
        self.StartDay(11, "Cosmic Expansion")
        self.ReadInput()
        self.expand_by = 1_000_000
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(11)

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
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 374

    def TestDataB(self):
        self.inputdata.clear()
        self.expand_by = 100
        self.TestDataA()
        return 8410

    def ParseInput(self):
        grid = []
        for line in self.inputdata:
            grid.append([c for c in line])
        return grid

    def Expand(self, grid):
        hgrid = []
        r = c = 0
        for line in grid:
            hgrid.append(line)
            if all([c == "." for c in line]):
                r = r + 1
                hgrid.append(line[:])

        for x in dirange(len(hgrid[0]) - 1, 0):
            if all([row[x] == "." for row in hgrid]):
                c = c + 1
                for row in hgrid:
                    row.insert(x, ".")
        print(f"Extra rows: {r}  Extra columns: {c}")
        return hgrid

    def FindEmpty(self, grid):
        erows = []
        ecols = []
        for y, line in enumerate(grid):
            if all([c == "." for c in line]):
                erows.append(y)

        for x in range(len(grid[0])):
            if all([row[x] == "." for row in grid]):
                ecols.append(x)
        return erows, ecols

    def isbetween(self, v: int, a: int, b: int) -> bool:
        if a > b: a, b = b, a
        return a < v < b
    
    def FindGalaxies(self, grid):
        galaxies = []
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == "#":
                    galaxies.append((x, y))
        return galaxies

    def PartA(self):
        self.StartPartA()

        universe = self.ParseInput()
        universe = self.Expand(universe)
        galaxies = self.FindGalaxies(universe)

        answer = 0
        for c in itertools.combinations(galaxies, 2):
            answer += manhattan_distance(c[0], c[1])

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        universe = self.ParseInput()
        erows, ecols = self.FindEmpty(universe)
        galaxies = self.FindGalaxies(universe)
        print(ecols)
        print(erows)
        # print(galaxies)

        answer = 0
        for c in itertools.combinations(galaxies, 2):
            dist = manhattan_distance(c[0], c[1])
            er = len([v for v in erows if self.isbetween(v, c[0][1], c[1][1])])
            ec = len([v for v in ecols if self.isbetween(v, c[0][0], c[1][0])])

            # print(ecols)
            # print(erows)
            # print(f" X: {c[0][0]} -> {c[1][0]}    Y: {c[0][1]} -> {c[1][1]} ")
            # print("ec", ec)
            # print("er", er)
            # a = input()
            answer += dist + er * (self.expand_by - 1) + ec * (self.expand_by - 1)

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day11Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


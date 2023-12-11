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
        grid = []
        for line in self.inputdata:
            grid.append([c for c in line])
        return grid

    def Expand(self, grid):
        hgrid = []
        for line in grid:
            hgrid.append(line)
            if all([c == "." for c in line]):
                hgrid.append(line[:])

        for x in dirange(len(hgrid[0]) - 1, 0):
            if all([row[x] == "." for row in hgrid]):
                for row in hgrid:
                    row.insert(x, ".")
        return hgrid

    def PartA(self):
        self.StartPartA()

        universe = self.ParseInput()
        universe = self.Expand(universe)

        galaxies = []
        for y, row in enumerate(universe):
            for x, c in enumerate(row):
                if c == "#":
                    galaxies.append((x, y))

        answer = 0
        for c in itertools.combinations(galaxies, 2):
            answer += manhattan_distance(c[0], c[1])

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        # Add solution here

        answer = None

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day11Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


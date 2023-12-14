from aoc import Aoc
import itertools
import math
import re
import sys

# Day 14
# https://adventofcode.com/2023

class Day14Solution(Aoc):

    def Run(self):
        self.StartDay(14, "Parabolic Reflector Dish")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(14)

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
        O....#....
        O.OO#....#
        .....##...
        OO.#O....O
        .O.....O#.
        O.#..O.#.#
        ..O..#O..O
        .......O..
        #....###..
        #OO..#....
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 136

    def TestDataB(self):
        self.TestDataA()
        return 64

    def ParseInput(self):
        data = []
        for line in self.inputdata:
            data.append([ch for ch in line])

        return data

    def SlideUpAndCalcLoad(self, grid, x: int) -> int:
        h = len(grid)
        moved = True
        while moved:
            moved = False
            for y in range(1, h):
                if grid[y][x] == "O" and grid[y - 1][x] == ".":
                    moved = True
                    grid[y][x], grid[y - 1][x] = grid[y - 1][x], grid[y][x]
        load = 0
        for y in range(0, h):
            if grid[y][x] == "O":
                load += (h - y)

        return load

    def PartA(self):
        self.StartPartA()

        data = self.ParseInput()

        answer = 0
        cols = len(data[0])
        for x in range(cols):
            answer += self.SlideUpAndCalcLoad(data, x)
        for r in data:
            print(r)

        # Add solution here

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        # data = self.ParseInput()
        answer = None

        # Add solution here

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day14Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


from aoc import Aoc
from utilities import dirange
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

        # goal = self.TestDataB()
        # self.PartB()
        # self.Assert(self.GetAnswerB(), goal)

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

    def SlideUp(self, grid, x: int) -> None:
        h = len(grid)
        moved = True
        while moved:
            moved = False
            for y in range(1, h):
                if grid[y][x] == "O" and grid[y - 1][x] == ".":
                    moved = True
                    grid[y][x], grid[y - 1][x] = grid[y - 1][x], grid[y][x]

    def SlideLeft(self, grid, y: int) -> None:
        w = len(grid[0])
        moved = True
        while moved:
            moved = False
            for x in range(1, w):
                if grid[y][x] == "O" and grid[y][x - 1] == ".":
                    moved = True
                    grid[y][x], grid[y][x - 1] = grid[y][x - 1], grid[y][x]

    def SlideDown(self, grid, x: int) -> None:
        h = len(grid)
        moved = True
        while moved:
            moved = False
            for y in dirange(h - 2, 0):
                if grid[y][x] == "O" and grid[y + 1][x] == ".":
                    moved = True
                    grid[y][x], grid[y + 1][x] = grid[y + 1][x], grid[y][x]

    def SlideRight(self, grid, y: int) -> None:
        w = len(grid[0])
        moved = True
        while moved:
            moved = False
            for x in dirange(w - 2, 0):
                if grid[y][x] == "O" and grid[y][x + 1] == ".":
                    moved = True
                    grid[y][x], grid[y][x + 1] = grid[y][x + 1], grid[y][x]

    def CalcLoad(self, grid) -> int:
        h = len(grid)
        w = len(grid[0])
        load = 0
        for x in range(w):
            for y in range(0, h):
                if grid[y][x] == "O":
                    load += (h - y)

        return load

    def PartA(self):
        self.StartPartA()

        data = self.ParseInput()

        cols = len(data[0])
        for x in range(cols):
            self.SlideUp(data, x)

        answer = self.CalcLoad(data)

        self.ShowAnswer(answer)

    def DoCycle(self, data) -> None:
        cols = len(data[0])
        rows = len(data)
        for x in range(cols):
            self.SlideUp(data, x)

        for y in range(rows):
            self.SlideLeft(data, y)

        for x in range(cols):
            self.SlideDown(data, x)

        for y in range(rows):
            self.SlideRight(data, y)

    def Cycle(self, list):
        shortest = [] 
        if len(list) <= 1: 
            return list
        if len(set(list)) == len(list): 
            return list
        for x in range(len(list)):
            if list[0:x] == list[x:2 * x]:
                shortest = list[0:x]
        return shortest 

    def PartB(self):
        self.StartPartB()

        data = self.ParseInput()
        prefix = 0
        cycle = 1
        count = 1_000_000_000

        loads = []
        for i in range(1000):
            self.DoCycle(data)
            load = self.CalcLoad(data)
            loads.append(load)

        for i in range(1000):
            s = self.Cycle(loads[i:])
            if len(s) > 0:
                print(f"Prefix: {i}  cycle: {len(s)}")
                prefix = i
                cycle = len(s)
                break

        data = self.ParseInput()    # reset

        for i in range(prefix):
            self.DoCycle(data)

        # This part can be improved ;)
        i = prefix
        while i + cycle < count:
            i += cycle

        while i < count:
            self.DoCycle(data)
            i += 1

        # Attempt 1: 90575 is too high
        # Attempt 2: 90551 is correct

        answer = self.CalcLoad(data)

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day14Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


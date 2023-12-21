from aoc import Aoc
from utilities import neighbours4
from typing import Iterator
import itertools
import sys

# Day 21
# https://adventofcode.com/2023

class Grid():
    def __init__(self, grid, pos: tuple[int, int], maxsteps: int, addoutofbound) -> None:
        self.pos = pos
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.q = []
        self.solved = False
        self.start = None
        self.maxsteps = maxsteps
        self.count = 0
        self.addoutofbound = addoutofbound
        self.newgrid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        # print(f"Created {self.pos}")

    def Neighbours(self, x: int, y: int) -> Iterator[tuple[int, int]]:
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dir in dirs:
            xx = x + dir[0]
            yy = y + dir[1]
            yield (xx, yy)

    def AddNumber(self, x: int, y: int, val: int) -> None:
        if self.grid[y][x] == "#":
            return
        if self.newgrid[y][x] != 0:
            return
        if val > self.maxsteps + 1:
            return
        else:
            self.newgrid[y][x] = val
            self.q.append((x, y))

    def Walk(self):
        print(f"Starting Walk {self.pos}")
        # a = input()
        if len(self.q) == 0 and self.start is not None:
            self.q.append(self.start)
        while len(self.q) > 0:
            current = self.q.pop(0)
            d = self.newgrid[current[1]][current[0]]
            for n in self.Neighbours(*current):
                if n[0] < 0:
                    # Left
                    self.addoutofbound(*n, d + 1)
                    continue
                if n[1] < 0:
                    # Up
                    self.addoutofbound(*n, d + 1)
                    continue
                if n[0] >= self.width:
                    # Right
                    self.addoutofbound(*n, d + 1)
                    continue
                if n[1] >= self.height:
                    # Down
                    self.addoutofbound(*n, d + 1)
                    continue

                if self.grid[n[1]][n[0]] == "#":
                    continue
                if self.newgrid[n[1]][n[0]] != 0:
                    continue
                if d + 1 > self.maxsteps + 1:
                    continue
                else:
                    self.newgrid[n[1]][n[0]] = d + 1
                    self.q.append(n)
        rem = (self.maxsteps + 1) % 2
        for row in self.newgrid:
            for c in row:
                if c > self.maxsteps or c == 0 or c % 2 == rem:
                    pass
                else:
                    self.count += 1
        

class Part2Solver():
    def __init__(self, grid, start, maxsteps: int) -> None:
        self.grid = grid
        self.start = start
        self.width = len(grid[0])
        self.height = len(grid)
        self.grids: list[Grid] = []
        self.maxsteps = maxsteps
        self.total = 0
        self.currentg = None
        self.done = []

    def FindGrid(self, pos: tuple[int, int]):
        for grid in self.grids:
            if grid.pos == pos:
                return grid
        return None
    
    def AddOutOfBound(self, x: int, y: int, val: int):
        # print(f"OOB: {x},{y}  {val}     ({self.width}x{self.height})")
        if x < 0:
            dst = (self.currentg.pos[0] - 1, self.currentg.pos[1])
            newx = self.width - 1
            newy = y
        if y < 0:
            dst = (self.currentg.pos[0], self.currentg.pos[1] - 1)
            newx = x
            newy = self.height - 1
        if x >= self.width:
            dst = (self.currentg.pos[0] + 1, self.currentg.pos[1])
            newx = 0
            newy = y
        if y >= self.height:
            dst = (self.currentg.pos[0], self.currentg.pos[1] + 1)
            newx = x
            newy = 0
        if dst in self.done:
            return
        if dst is None:
            print(f"{x},{y}  val={val}  ")
            a = input()
        # print(f" > {dst}  - {newx},{newy}")
        g = self.FindGrid(dst)
        if g is None:
            g = Grid(self.grid, dst, self.maxsteps, self.AddOutOfBound)
            self.grids.append(g)
        g.AddNumber(newx, newy, val)
        # a = input()

    def Solve(self) -> int:
        g = Grid(self.grid, (0, 0), self.maxsteps, self.AddOutOfBound)
        g.start = self.start
        self.grids.append(g)
        while len(self.grids) > 0:
            self.currentg = self.grids.pop(0)
            print(f"{len(self.grids)} ", end="")
            self.currentg.Walk()
            self.done.append(self.currentg.pos)
            self.total += self.currentg.count
            self.currentg = None

        return self.total

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
            row = [c for c in line]
            if "S" in line:
                start = (line.index("S"), y)
                row[start[0]] = "."
            data.append(row)

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
        steps = 1000
        grid, start = self.ParseInput()
        solver = Part2Solver(grid, start, steps)
        answer = solver.Solve()

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day21Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


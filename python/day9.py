from aoc import Aoc
from utilities import dirange
import sys

# Day 9
# https://adventofcode.com/2023

class Day9Solution(Aoc):

    def Run(self):
        self.StartDay(9, "Mirage Maintenance")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(9)

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
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 114

    def TestDataB(self):
        self.TestDataA()
        return 2

    def ParseInput(self):
        rows = []
        for line in self.inputdata:
            row = list(map(int, [n for n in line.split(" ")]))
            rows.append(row)
        return rows

    def Reduce(self, row):
        r = [row]
        current = row[:]
        while any([x != 0 for x in current]):
            new = []
            for ix in range(1, len(current)):
                new.append(current[ix] - current[ix - 1])
            r.append(new)
            current = new
        return r

    def Extrapolate(self, reduced):
        reduced[-1].append(0)
        for ix in dirange(len(reduced) - 2, 0):
            reduced[ix].append(reduced[ix + 1][-1] + reduced[ix][-1])

    def Prepolate(self, reduced):
        reduced[-1].insert(0, 0)
        for ix in dirange(len(reduced) - 2, 0):
            reduced[ix].insert(0, reduced[ix][0] - reduced[ix + 1][0])

    def PartA(self):
        self.StartPartA()

        answer = 0

        rows = self.ParseInput()
        for row in rows:
            reduced = self.Reduce(row)
            self.Extrapolate(reduced)
            answer += reduced[0][-1]

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        answer = 0

        rows = self.ParseInput()
        for row in rows:
            reduced = self.Reduce(row)
            self.Prepolate(reduced)
            answer += reduced[0][0]

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day9Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


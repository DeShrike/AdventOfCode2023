from aoc import Aoc
from collections import Counter
from utilities import dirange
import re
import itertools
import math
import sys

# Day 13
# https://adventofcode.com/2023

class Day13Solution(Aoc):

    def Run(self):
        self.StartDay(13, "Point of Incidence")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(13)

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
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.

        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 405

    def TestDataB(self):
        self.TestDataA()
        return 400

    def ParseInput(self):
        data = []
        pattern = []
        data.append(pattern)
        for line in self.inputdata:
            if line == "":
                pattern = []
                data.append(pattern)
            else:
                pattern.append(line)

        return data

    def CountDiff(self, line1: list[str], line2: list[str]) -> int:
        return len([0 for c1, c2 in zip(line1, line2) if c1 != c2])

    def TryReflect(self, pattern, fixdiff: bool = False) -> int:
        h = len(pattern)
        w = len(pattern[0])

        for ix in range(h - 1):
            if fixdiff:
                if pattern[ix] != pattern[ix + 1]:
                    if self.CountDiff(pattern[ix], pattern[ix + 1]) == 1:
                        print(pattern[ix], pattern[ix + 1])
                        pattern[ix] = pattern[ix + 1][:]
                        print("fixed")
            if pattern[ix] == pattern[ix + 1]:
                rix = ix
                bad = False
                for l in dirange(ix, 0):
                    rix += 1
                    if l < 0 or rix >= h:
                        break
                    if pattern[l] != pattern[rix]:
                        if fixdiff:
                            if self.CountDiff(pattern[l], pattern[rix]) == 1:
                                print(pattern[l], pattern[rix])
                                pattern[l] = pattern[rix][:]
                                print("fixed")
                        else:
                            bad = True
                            break
                if not bad:
                    return ix + 1

        return None

    def Reflect(self, pattern, fixdiff: bool = False) -> int:
        result = self.TryReflect(pattern, fixdiff)
        if result is None:
            pattern_t = [list(x) for x in zip(*pattern)]
            result = self.TryReflect(pattern_t, fixdiff)
        else:
            result *= 100
        return result

    def PartA(self):
        self.StartPartA()

        answer = 0
        data = self.ParseInput()
        for pattern in data:
            answer += self.Reflect(pattern)
        
        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        answer = 0
        data = self.ParseInput()
        for pattern in data:
            answer += self.Reflect(pattern, True)
            # a = input()

        # Attempt 1: 39597 is too high

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day13Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


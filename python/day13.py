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

    def TryReflect(self, pattern) -> int:
        h = len(pattern)
        w = len(pattern[0])
        for ix in range(h - 1):
            if pattern[ix] == pattern[ix + 1]:
                rix = ix
                bad = False
                for l in dirange(ix, 0):
                    rix += 1
                    if l < 0 or rix >= h:
                        break
                    if pattern[l] != pattern[rix]:
                        bad = True
                        break
                if not bad:
                    return ix + 1

        return None

    def TryFixAndReflect(self, pattern) -> list[int]:
        h = len(pattern)
        w = len(pattern[0])
        results = []

        for ix in range(h - 1):
            if pattern[ix] != pattern[ix + 1]:
                if self.CountDiff(pattern[ix], pattern[ix + 1]) == 1:
                    pattern[ix] = pattern[ix + 1][:]
            if pattern[ix] == pattern[ix + 1]:
                rix = ix
                bad = False
                for l in dirange(ix, 0):
                    rix += 1
                    if l < 0 or rix >= h:
                        break
                    if pattern[l] != pattern[rix]:
                        if self.CountDiff(pattern[l], pattern[rix]) == 1:
                            pattern[l] = pattern[rix][:]
                    if pattern[l] != pattern[rix]:
                        bad = True
                        break
                if not bad:
                    results.append(ix + 1)

        return results

    def Reflect(self, pattern) -> int:
        result = self.TryReflect(pattern)
        if result is None:
            pattern_t = [list(x) for x in zip(*pattern)]
            result = self.TryReflect(pattern_t)
        else:
            result *= 100
        return result

    def FindAllReflections(self, pattern) -> int:
        reflections = []
        result = self.TryFixAndReflect(pattern)
        reflections += [r * 100 for r in result]
        pattern_t = [list(x) for x in zip(*pattern)]
        result = self.TryFixAndReflect(pattern_t)
        reflections += result
        return reflections

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
            normal = self.Reflect(pattern)
            reflections = self.FindAllReflections(pattern)
            reflections.remove(normal)
            # print(normal, reflections)
            answer += reflections[0]

        # Attempt 1: 39597 is too high
        # Attempt 2: 36755 is correct
        
        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day13Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


from aoc import Aoc
import itertools
import math
import re
import sys

# Day 15
# https://adventofcode.com/2023

class Day15Solution(Aoc):

    def Run(self):
        self.StartDay(15, "Lens Library")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(15)

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
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 1320

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
        data = self.inputdata[0].split(",")
        return data

    def Hash(self, step: str) -> int:
        h = 0
        for c in step:
            h = h + ord(c)
            h *= 17
            h = h % 256
        return h

    def PartA(self):
        self.StartPartA()

        steps = self.ParseInput()
        answer = sum([self.Hash(step) for step in steps])

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        data = self.ParseInput()
        answer = None

        # Add solution here

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day15Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


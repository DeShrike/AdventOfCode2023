from aoc import Aoc
from collections import Counter
import re
import itertools
import math
import sys

# Day 12
# https://adventofcode.com/2023

class Day12Solution(Aoc):

    def Run(self):
        self.StartDay(12, "Hot Springs")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(12)

        # goal = self.TestDataA()
        # self.PartA()
        # self.Assert(self.GetAnswerA(), goal)

        goal = self.TestDataB()
        self.PartB()
        self.Assert(self.GetAnswerB(), goal)

    def TestDataA(self):
        self.inputdata.clear()
        testdata = \
        """
        ???.### 1,1,3
        .??..??...?##. 1,1,3
        ?#?#?#?#?#?#?#? 1,3,1,6
        ????.#...#... 4,1,1
        ????.######..#####. 1,6,5
        ?###???????? 3,2,1
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 21

    def TestDataB(self):
        self.TestDataA()
        return 525152

    def ParseInput(self):
        data = []
        for line in self.inputdata:
            parts = line.split(" ")
            data.append((parts[0], list(map(int,parts[1].split(",")))))

        return data

    def CheckValid(self, v: str, nums: list[int]) -> bool:
        v2 = v.replace("..", ".")
        v2 = v2.replace("..", ".")
        v2 = v2.replace("..", ".")
        v2 = v2.replace("..", ".")
        v2 = v2.replace("..", ".")
        cc = [len(v4) for v4 in v2.strip(".").split(".")]
        return cc == nums
    
    def SetBits(self, bits: int, record: str) -> str:
        news = ""
        b = 0
        for c in record:
            if c == "?":
                if bits & (1 << b) == 0:
                    news += "."
                else:
                    news += "#"
                b += 1 
            else:
                news += c
        return news

    def Expand(self, data) -> tuple[str, list[int]]:
        news = data[0] + "?" + data[0] + "?" + data[0] + "?" + data[0] + "?" + data[0]
        newnumbers = data[1] * 5
        return news, newnumbers

    def CountPosibilities(self, s: str, num:int) -> int:
        c = 0
        bits = Counter(s)["?"]
        print(f"{s} -> {bits} bit   ", end="")
        for i in range(2 ** bits):
            news = self.SetBits(i, s)
            if self.CheckValid(news, [num]):
                c += 1
        print(f" --> {c}")
        return c
    
    def SolveExpanded(self, record: str, nums: list[int]) -> int:
        r = "^[\.\?]*?"
        for ix, n in enumerate(nums):
            r += "([\?#]{" + str(n) + "}?)"
            # r += "([\?#]{" + str(n) + "," + str(n + 20) + "}?)"
            if ix < len(nums) - 1:
                r += "[\.\?]+?"
            else:
                r += "[\.\?]*?"
        r += "$"
        print(r)
        rx = re.compile(r)
        match = rx.search(record)

        for groupNum in range(1, len(match.groups()) + 1):
            print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

        t = 1
        # for s, n in zip(g, nums):
        #     t *= self.CountPosibilities(s, n)
        # print("T: ", t)
        a = input()
        return t

    def PartA(self):
        self.StartPartA()

        data = self.ParseInput()
        answer = 0
        for d in data:
            s = d[0]
            bits = Counter(s)["?"]
            # print(f"{s} -> {bits} bit")
            for i in range(2 ** bits):
                news = self.SetBits(i, s)
                if self.CheckValid(news, d[1]):
                    answer += 1

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        data = self.ParseInput()
        answer = 0
        for d in data:
            record, nums = self.Expand(d)
            print(record, nums)
            answer += self.SolveExpanded(record, nums)

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day12Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


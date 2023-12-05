from aoc import Aoc
import itertools
import math
import re
import sys

# Day 5
# https://adventofcode.com/2023

class Mapping():
    def __init__(self, name: str):
        self.name = name
        self.parts = []     # [(dst, src, len), ...]

    def map(self, seed: int) -> int:
        for part in self.parts:
            dst = part[0]
            src = part[1]
            l = part[2]
            if src <= seed <= src + l - 1:
                seed = (seed - src) + dst
                break
        return seed


class Day5Solution(Aoc):

    def Run(self):
        self.StartDay(5, "If You Give A Seed A Fertilizer")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(5)

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
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 35

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
        mappings = []
        seeds = None
        mapping = None
        for line in self.inputdata:
            if line == "":
                continue
            elif line[:6] == "seeds:":
                seeds = [int(s) for s in line[7:].split(" ")]
            elif line[-1] == ":":
                mapping = Mapping(line[0:-1])
                mappings.append(mapping)
            else:
                parts = [int(p) for p in line.split(" ")]
                mapping.parts.append((parts[0], parts[1], parts[2]))

        return seeds, mappings

    def Map(self, seed: int, mappings) -> int:
        # print(f"Van {seed} ", end="")
        for mapping in mappings:
            seed = mapping.map(seed)
            # print(f"{mapping.name} -> {seed}");
        # print(f"naar {seed}")

        return seed

    def PartA(self):
        self.StartPartA()

        seeds, mappings = self.ParseInput()
        print(seeds)
        mapped = [self.Map(seed, mappings) for seed in seeds]
        print(mapped)

        answer = min(mapped)

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        # Add solution here

        answer = None

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day5Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


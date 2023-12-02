from aoc import Aoc
import itertools
import math
import re
import sys

# Day 2
# https://adventofcode.com/2023

class Game():
    def __init__(self, line: str):
        self.sets = []      # [(red, green, blue), ...]
        parts = line.split(":")
        self.id = int(parts[0][5:])
        parts = parts[1].split(";")
        for s in parts:
            cubes = s.split(",")
            r = 0
            g = 0
            b = 0
            for c in cubes:
                c = c.strip()
                count = int(c[:c.index(" ")])
                if "red" in c:
                    r = count
                if "green" in c:
                    g = count
                if "blue" in c:
                    b = count
            self.sets.append((r, g, b))

    def NotMoreThan(self, count, ix) -> bool:
        for s in self.sets:
            if s[ix] > count:
                return False

        return True

    def CalcPower(self) -> int:
        r = max([s[0] for s in self.sets])
        g = max([s[1] for s in self.sets])
        b = max([s[2] for s in self.sets])
        return r *g * b


class Day2Solution(Aoc):

    def Run(self):
        self.StartDay(2, "Cube Conundrum")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(2)

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
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 8

    def TestDataB(self):
        self.inputdata.clear()
        self.TestDataA()
        return 2286

    def ParseInput(self):
        games = []
        for line in self.inputdata:
            games.append(Game(line))
        return games

    def PartA(self):
        self.StartPartA()

        answer = 0
        games = self.ParseInput()
        for game in games:
            if game.NotMoreThan(12, 0) and game.NotMoreThan(13, 1) and game.NotMoreThan(14, 2):
                answer += game.id

        # Attempt 1: 1715 is too low
        # Attempt 2: 2061 is correct

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        answer = 0
        games = self.ParseInput()
        for game in games:
            answer += game.CalcPower()

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day2Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


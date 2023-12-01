from aoc import Aoc
import itertools
import math
import re
import sys

# Day 1
# https://adventofcode.com/2023

class Day1Solution(Aoc):

    def Run(self):
        self.StartDay(1, "Trebuchet?!")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(1)

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
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 142

    def TestDataB(self):
        self.inputdata.clear()
        testdata = \
        """
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 281

    def ReplaceWords(self, line: str) -> str:
        words = ["????", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        result = ""
        ix = 0
        while ix < len(line):
            foundw = False
            for wix, word in enumerate(words):
                if line[ix:ix + len(word)] == word:
                    result += str(wix)
                    foundw = True
                    ix += len(word)
                    break
            if foundw == False:
                result += line[ix]
                ix += 1

        result2 = ""
        ix = len(line) -1
        while ix >= 0:
            foundw = False
            for wix, word in enumerate(words):
                if line[ix:ix + len(word)] == word:
                    result2 = str(wix) + result2
                    foundw = True
                    ix -= 1
                    break
            if foundw == False:
                result2 = line[ix] + result2
                ix -= 1
        # print(result, result2)
        # a = input()
        return result + result2

    def PartA(self):
        self.StartPartA()

        answer = 0
        for line in self.inputdata:
            newline = [ch for ch in line if ord(ch) >= 48 and ord(ch) <= 57]
            answer += int(newline[0] + newline[-1])

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        answer = 0
        for line in self.inputdata:
            # print(line)
            newline = self.ReplaceWords(line)
            # print(newline)
            # a = input()
            # print("")
            newline2 = [ch for ch in newline if ord(ch) >= 48 and ord(ch) <= 57]
            answer += int(newline2[0] + newline2[-1])

        # Attempt 1: 54978 is too low

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day1Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


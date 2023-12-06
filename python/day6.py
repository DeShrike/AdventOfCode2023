from aoc import Aoc
import sys

# Day 6
# https://adventofcode.com/2023

class Day6Solution(Aoc):

    def Run(self):
        self.StartDay(6, "Wait For It")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(6)

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
        Time:      7  15   30
        Distance:  9  40  200
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 288

    def TestDataB(self):
        self.inputdata.clear()
        self.TestDataA()
        return 71503

    def PartA(self):
        self.StartPartA()

        times = list(map(int, self.inputdata[0][10:].strip().split()))
        dists = list(map(int, self.inputdata[1][10:].strip().split()))

        print(times)
        print(dists)

        answer = 1
        for ix in range(len(times)):
            bettercount = 0
            for t in range(times[ix] + 1):
                if (times[ix] - t) * t > dists[ix]:
                    bettercount += 1
            answer *= bettercount

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        time = int(self.inputdata[0][10:].replace(" ", ""))
        dist = int(self.inputdata[1][10:].replace(" ", ""))

        print(time)
        print(dist)

        bettercount = 0
        for t in range(time + 1):
            if (time - t) * t > dist:
                bettercount += 1
        answer = bettercount

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day6Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


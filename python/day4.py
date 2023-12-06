from aoc import Aoc
from utilities import dirange
import sys

# Day 4
# https://adventofcode.com/2023

class Day4Solution(Aoc):

    def Run(self):
        self.StartDay(4, "Scratchcards")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(4)

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
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 13

    def TestDataB(self):
        self.TestDataA()
        return 30

    def ParseInput(self):
        cards = []      # [(id, winning, have), ...]
        for line in self.inputdata:
            parts = line.split(":")
            id = int(parts[0][5:])
            parts = parts[1].split("|")
            winning = [int(n.strip()) for n in parts[0].replace("  ", " ").strip().split(" ")]
            having = [int(n.strip()) for n in parts[1].replace("  ", " ").strip().split(" ")]
            cards.append((id, winning, having))
        return cards

    def CalcScore(self, card) -> int:
        same = set(card[2]).intersection(set(card[1]))
        return 2 ** (len(same) - 1) if len(same) > 0 else 0

    def PartA(self):
        self.StartPartA()

        cards = self.ParseInput()
        answer = sum([self.CalcScore(card) for card in cards])

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        cards = self.ParseInput()
        counts = [1 for _ in range(len(cards))]
        for ix, card in enumerate(cards):
            same = set(card[2]).intersection(set(card[1]))
            if len(same) > 0:
                for a in dirange(ix + 1, ix + len(same)):
                    counts[a] += counts[ix]

        answer = sum(counts)

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day4Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


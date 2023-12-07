from aoc import Aoc
from enum import IntEnum
import itertools
import math
import re
import sys

# Day 7
# https://adventofcode.com/2023

class HandType(IntEnum):
    FiveOfAKind = 1,
    FourOfAKind = 2,
    FullHouse = 3,
    ThreeOfAKind = 4,
    TwoPair = 5,
    OnePair = 6,
    HighCard = 7


class Hand():
    ranks = list(reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]))

    def __init__(self, cards: str):
        self.cards = cards

    def handtype(self) -> HandType:
        o = list(sorted([self.cards.count(x) for x in set(self.cards)], reverse=True))
        if len(o) == 5:
           return HandType.HighCard
        elif len(o) == 4:
            return HandType.OnePair
        elif len(o) == 1:
            return HandType.FiveOfAKind
        elif len(o) == 2 and o[0] == 4:
            return HandType.FourOfAKind
        elif len(o) == 2 and o[0] == 3:
            return HandType.FullHouse
        elif len(o) == 3 and o[0]== 3:
            return HandType.ThreeOfAKind
        elif len(o) == 3 and o[0]== 2 and o[1]== 2:
            return HandType.TwoPair
    
        return None
    
    def __gt__(self, other):
        t = self.handtype()
        o = other.handtype()
        if t == o:
            for ct, co in zip(self.cards, other.cards):
                if ct != co:
                    return Hand.ranks.index(ct) > Hand.ranks.index(co)
        return t < o

class Day7Solution(Aoc):

    def Run(self):
        self.StartDay(7, "Camel Cards")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(7)

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
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 6440

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

    def SortHands(self, hands):
        # Slow bubblesort
        swapped = True
        while swapped:
            swapped = False
            for ix in range(len(hands) - 1):
                if hands[ix][0] > hands[ix + 1][0]:
                    hands[ix], hands[ix + 1] = hands[ix + 1], hands[ix]
                    swapped = True

    def ParseInput(self):
        cards = []  # [(hand, bid), ...]
        for line in self.inputdata:
            hand, bid = line.split(" ")
            cards.append((Hand(hand), int(bid)))
        return cards

    def PartA(self):
        self.StartPartA()

        answer = 0
        hands = self.ParseInput()
        self.SortHands(hands)
        for ix, hand in enumerate(hands):
            answer += (ix + 1) * hand[1]        


        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        # Add solution here

        answer = None

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day7Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


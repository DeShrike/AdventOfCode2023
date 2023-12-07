from aoc import Aoc
from enum import IntEnum
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
    ranksA = list(reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]))
    ranksB = list(reversed(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]))

    def __init__(self, cards: str, part: str = "A"):
        self.cards = cards
        self.originalcards = cards
        self.part = part

    def UpgradeJoker(self):
        if "J" not in self.cards:
            return
        
        bestcard = None
        current, bestrank = self.cards, self.handtypeof(self.cards)
        for r in Hand.ranksB:
            new = current.replace("J", r)
            newrank = self.handtypeof(new)
            if newrank < bestrank:
                bestcard = r
                bestrank = newrank
        if bestcard:
            self.cards = self.cards.replace("J", bestcard)

    def handtypeof(self, cards: str) -> HandType:
        o = list(sorted([cards.count(x) for x in set(cards)], reverse=True))
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

    def handtype(self) -> HandType:
        if self.part == "B":
            self.UpgradeJoker()
        return self.handtypeof(self.cards)
        
    def __gt__(self, other):
        t = self.handtype()
        o = other.handtype()
        if t == o:
            for ct, co in zip(self.originalcards, other.originalcards):
                if ct != co:
                    if self.part == "A":
                        return Hand.ranksA.index(ct) > Hand.ranksA.index(co)
                    else:
                        return Hand.ranksB.index(ct) > Hand.ranksB.index(co)
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
        self.TestDataA()
        return 5905

    def SortHands(self, hands):
        # Slow bubblesort
        swapped = True
        while swapped:
            swapped = False
            for ix in range(len(hands) - 1):
                if hands[ix][0] > hands[ix + 1][0]:
                    hands[ix], hands[ix + 1] = hands[ix + 1], hands[ix]
                    swapped = True

    def ParseInput(self, part: str = "A"):
        cards = []  # [(hand, bid), ...]
        for line in self.inputdata:
            hand, bid = line.split(" ")
            cards.append((Hand(hand, part), int(bid)))
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

        answer = 0
        hands = self.ParseInput("B")
        self.SortHands(hands)
        for ix, hand in enumerate(hands):
            answer += (ix + 1) * hand[1]        

        # Attempt 1: 253720086 is too low
        # Attempt 2: 254115617 is correct

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day7Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


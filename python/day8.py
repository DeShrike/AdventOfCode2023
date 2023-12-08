from aoc import Aoc
from utilities import lcm
import re
import sys

# Day 8
# https://adventofcode.com/2023

class Day8Solution(Aoc):

    def Run(self):
        self.StartDay(8, "Haunted Wasteland")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(8)

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
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 6

    def TestDataB(self):
        self.inputdata.clear()
        testdata = \
        """
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 6

    def ParseInput(self):
        instr = self.inputdata[0]
        rx = re.compile("^(?P<from>[A-Z0-9]{3}) = \((?P<left>[A-Z0-9]{3}), (?P<right>[A-Z0-9]{3})\)$")
        nodes = {}
        for line in self.inputdata[2:]:
            match = rx.search(line)
            if match:
                pos = match["from"]
                left = match["left"]
                right = match["right"]
                nodes[pos] = (left, right)
            else:
                print(f"Bad line: {line}")
        return instr, nodes

    def CalcSteps(self, pos: str, end, instr, nodes) -> int:
        ix = 0
        count = 0
        while (pos != "ZZZ" and end == "ZZZ") or (pos[2] != "Z" and end != "ZZZ"):
            node = nodes[pos]
            pos = node[0] if instr[ix] == "L" else node[1]
            count += 1
            ix = (ix + 1) % len(instr)
        return count
    
    def PartA(self):
        self.StartPartA()

        instr, nodes = self.ParseInput()
        answer = self.CalcSteps("AAA", "ZZZ", instr, nodes)
        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        instr, nodes = self.ParseInput()
        starts = [k for k in nodes.keys() if k[2] == "A"]
        print(starts)
        counts = [self.CalcSteps(start, "??Z", instr, nodes) for start in starts]
        print(counts)

        answer = counts[0]
        for c in counts[1:]:
            answer = lcm(answer, c)

        # Attempt 1: 1815232161643 is too low
        # Attempt 2: 13268366086992805522755101 is too high
        # Attempt 3: 513710701744969 is too high
        # Attempt 4: 25828479029 is wrong
        # Attempt 5: 7309459565207 is correct

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day8Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.4


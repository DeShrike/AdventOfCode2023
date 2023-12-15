from aoc import Aoc
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
        self.TestDataA()
        return 145

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
        boxes = [[] for _ in range(256)]
        for step in data:
            if step[-1] == "-":
                label = step[:-1]
                hash = self.Hash(label)
                for b in boxes[hash]:
                    if b[1] == label:
                        boxes[hash].remove(b)
                        break
            else:
                label, strength = step.split("=")
                hash = self.Hash(label)
                found = False
                for lix, l in enumerate(boxes[hash]):
                    if l[1] == label:
                        boxes[hash][lix] = (step, label, strength)
                        found = True
                        break
                if not found:
                    boxes[hash].append((step, label, strength))

            # for bix, b in enumerate(boxes):
            #     if len(b) > 0:
            #         print(f"Box {bix}: ", end="")
            #         for l in b:
            #             print(f"[{l[1]} {l[2]}]", end=" ")
            #         print("")
            # a = input()

        answer = 0
        for bix, box in enumerate(boxes):
            for lix, l in enumerate(box):
                answer += ((bix + 1) * (lix + 1)) * int(l[2])

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day15Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


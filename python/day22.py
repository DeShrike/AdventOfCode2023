from aoc import Aoc
from utilities import dirange
import re
import sys

# Day 22
# https://adventofcode.com/2023

class Brick():
    def __init__(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.gone = False
        self.Calc()

    def Calc(self) -> None:
        self.points = self.GetPoints()

    def GetPoints(self):
        points = []
        for x in dirange(self.x1, self.x2):
            for y in dirange(self.y1, self.y2):
                for z in dirange(self.z1, self.z2):
                    points.append((x, y, z))
        return set(points)


class Day22Solution(Aoc):

    def Run(self):
        self.StartDay(22, "Sand Slabs")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(22)

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
        1,0,1~1,2,1
        0,0,2~2,0,2
        0,2,3~2,2,3
        0,0,4~0,2,4
        2,0,5~2,2,5
        0,1,6~2,1,6
        1,1,8~1,1,9
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 5

    def TestDataB(self):
        self.TestDataA()
        return 7

    def ParseInput(self):
        rx = re.compile("^(?P<x1>[0-9]*),(?P<y1>[0-9]*),(?P<z1>[0-9]*)~(?P<x2>[0-9]*),(?P<y2>[0-9]*),(?P<z2>[0-9]*)$")
        bricks = []
        for line in self.inputdata:
            match = rx.search(line)
            if match:
                x1 = int(match["x1"])
                y1 = int(match["y1"])
                z1 = int(match["z1"])
                x2 = int(match["x2"])
                y2 = int(match["y2"])
                z2 = int(match["z2"])
                b = Brick(x1, y1, z1, x2, y2, z2)
                bricks.append(b)
            else:
                print("No match", line)
        return bricks

    def GetPoints(self, brick: Brick, offset: int = 0):
        points = []
        for x in dirange(brick.x1, brick.x2):
            for y in dirange(brick.y1, brick.y2):
                for z in dirange(brick.z1, brick.z2):
                    points.append((x, y, z + offset))
        return points
    
    def CanDrop(self, ix: int, bricks: list[Brick]) -> bool:
        b = bricks[ix]
        if b.z1 == 1 or b.z2 == 1:
            return False
        points = set(self.GetPoints(b, -1))
        can = True
        for i, bb in enumerate(bricks):
            if i == ix: 
                continue
            if bb.gone:
                continue
            if len(points.intersection(bb.points)) != 0:
                can = False
                break
        return can

    def TryDrop(self, bricks: list[Brick], dodrop: bool = True) -> bool:
        for ix in range(len(bricks)):
            if bricks[ix].gone:
                continue
            dropped = False
            while self.CanDrop(ix, bricks):
                dropped = True
                if dodrop:
                    bricks[ix].z1 -= 1
                    bricks[ix].z2 -= 1
                    bricks[ix].Calc()
                else:
                    return True
            if dropped:
                return True            
        return False

    def PartA(self):
        self.StartPartA()

        bricks = self.ParseInput()
        bricks.sort(key=lambda b: b.z1 if b.z1 < b.z2 else b.z2)

        print("This will take a few minutes")
        print("Initial Drops")
        dropped = True
        while dropped:
            dropped = self.TryDrop(bricks)

        print("Calculating")
        answer = 0
        for brick in bricks:
            canremove = True
            brick.gone = True
            if self.TryDrop(bricks, False):
                canremove = False
            if canremove:
                answer += 1
            brick.gone = False

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        bricks = self.ParseInput()
        bricks.sort(key=lambda b: b.z1 if b.z1 < b.z2 else b.z2)

        print("This will take a few minutes")
        print("Initial Drops")
        dropped = True
        while dropped:
            dropped = self.TryDrop(bricks)

        print("Calculating")
        answer = 0
        for brick in bricks:
            aantal = 0
            for b in bricks:
                b.gone = False
            brick.gone = True
            for ix, bb in enumerate(bricks):
                if bb.gone:
                    continue
                if self.CanDrop(ix, bricks):
                    bb.gone = True
                    aantal += 1

            answer += aantal

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day22Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


from aoc import Aoc
import itertools
import math
import re
import sys

# Day 19
# https://adventofcode.com/2023


class Workflow():
    def __init__(self, line: str) -> None:
        rx = re.compile("^(?P<name>[a-z]*){(?P<rules>.*)}$")
        rx2 = re.compile("^(?P<xmas>[xmas])(?P<op>[\<\>])(?P<val>[0-9]*):(?P<dest>[ARa-z]*)$")
        match = rx.search(line)
        if match:
            self.conditions = []
            self.name = match["name"]
            rules = match["rules"]
            parts = rules.split(",")
            for part in parts:
                match = rx2.search(part)
                if match:
                    xmas = match["xmas"]
                    op = match["op"]
                    val = int(match["val"])
                    dest = match["dest"]
                    self.conditions.append((xmas, op, val, dest))
                else:
                    self.conditions.append((None, None, None, part))

    def __str__(self) -> str:
        s = f"{self.name} = "
        for con in self.conditions:
            if con[0] is None:
                s += f"{con[3]}|"
            else:
                s += f" {con[0]}{con[1]}{con[2]}:{con[3]} |"
        return s

class Part():
    def __init__(self, line: str) -> None:
        self.accepted = False
        self.rejected = False
        rx = re.compile("^{x=(?P<x>[0-9]*),m=(?P<m>[0-9]*),a=(?P<a>[0-9]*),s=(?P<s>[0-9]*)}$")
        match = rx.search(line)
        if match:
            self.x = int(match["x"])
            self.m = int(match["m"])
            self.a = int(match["a"])
            self.s = int(match["s"])

            self.rating = self.x + self.m + self.a + self.s
        else:
            print("No Match")
            print(line)

    def Eval(self, xmas: str, op: str, val: int) -> bool:
        r = self.x
        if xmas == "m":
            r = self.m
        elif xmas == "a":
            r = self.a
        elif xmas == "s":
            r = self.s
        if op == "<":
            return r < val
        else:
            return r > val

    def __str__(self) -> str:
        status = "Accepted" if self.accepted else ("Rejected" if self.rejected else "")
        return f"x={self.x},m={self.m},a={self.a},s={self.s}  {status}"


class Node():
    def __init__(self, wf: Workflow) -> None:
        self.rx = (0, 4000)
        self.rm = (0, 4000)
        self.ra = (0, 4000)
        self.rs = (0, 4000)
        self.parent = None
        self.children = []
        self.name = wf.name
        self.wf = wf


class Day19Solution(Aoc):

    def Run(self):
        self.StartDay(19, "Aplenty")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(19)

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
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}

        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 19114

    def TestDataB(self):
        self.TestDataA()
        return 167409079868000

    def ParseInput(self):
        workflows = {}
        parts = []
        inparts = False
        for line in self.inputdata:
            if line == "":
                inparts = True
                continue
            if inparts:
                parts.append(Part(line))
            else:
                wf = Workflow(line)
                workflows[wf.name] = wf

        return workflows, parts

    def Evaluate(self, part: Part, workflows: dict[Workflow]) -> None:
        cond = "in"
        while not part.accepted and not part.rejected:
            wf = workflows[cond]
            for con in wf.conditions:
                if con[0] is None:
                    cond = con[3]
                    if cond == "A":
                        part.accepted = True
                    elif cond == "R":
                        part.rejected = True
                    break
                else:
                    if part.Eval(con[0], con[1], con[2]):
                        cond = con[3]
                        if cond == "A":
                            part.accepted = True
                        elif cond == "R":
                            part.rejected = True
                        break
            
    def PartA(self):
        self.StartPartA()

        workflows, parts = self.ParseInput()
        # for part in parts:
        #     print(part)
        # for k, workflow in workflows.items():
        #     print(k, workflow)

        for part in parts:
            self.Evaluate(part, workflows)

        # for part in parts:
        #     print(part)

        answer = sum([p.rating for p in parts if p.accepted])

        self.ShowAnswer(answer)

    def AddChildren(self, node: Node, workflows: dict[Workflow]) -> None:
        pass
    
    def PartB(self):
        self.StartPartB()

        workflows, _ = self.ParseInput()
        answer = None

        wf = workflows["in"]
        tree = Node(wf)
        self.AddChildren(tree, workflows)

        # Add solution here

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day19Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


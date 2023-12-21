from aoc import Aoc
import itertools
import math
import re
import sys

# Day 20
# https://adventofcode.com/2023

class Module():
    def __init__(self, name: str, typ: str) -> None:
        self.name = name
        self.typ = typ
        self.flipflop = typ == "%"
        self.conjunction = typ == "&"
        self.state = False
        self.srcs = {}
        self.gotlowpulse = False

    def __str__(self) -> str:
        return f"{self.typ} {self.name}"

    def addsrc(self, src: str) -> None:
        self.srcs[src] = False

    def pulse(self, src: str, val: int):
        if val == 0:
            self.gotlowpulse = True
        if self.flipflop:
            if val == 0:
                self.state = not self.state
                return int(self.state)
        elif self.conjunction:
            self.srcs[src] = val
            # print(f"{self.name} states: {self.srcs}")
            if all([v for k, v in self.srcs.items()]):
                return 0
            else:
                return 1
        else:
            return val


class Config():
    def __init__(self, name: str, line: str) -> None:
        self.name = name
        if line != "":
            self.destinations = [s.strip() for s in line.split(",")]
        else:
            self.destinations = []

    def __str__(self) -> str:
        return f"{self.name} -> {', '.join(self.destinations)}"


class Day20Solution(Aoc):

    def Run(self):
        self.StartDay(20, "Pulse Propagation")
        self.ReadInput()
        self.PartA()
        self.PartB()

    def Test(self):
        self.StartDay(20)

        goal = self.TestDataA()
        self.PartA()
        self.Assert(self.GetAnswerA(), goal)

    def TestDataA(self):
        self.inputdata.clear()
        testdata = \
        """
        broadcaster -> a
        %a -> inv, con
        &inv -> b
        %b -> con
        &con -> output
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return 11687500

    def TestDataB(self):
        self.inputdata.clear()
        testdata = \
        """
        """
        self.inputdata = [line.strip() for line in testdata.strip().split("\n")]
        return None

    def ParseInput(self):
        rx = re.compile("^(?P<from>.*) -> (?P<to>.*)$")
        modules = {}
        configs = {}
        for line in self.inputdata:
            match = rx.search(line)
            if match:
                van = match["from"]
                naar = match["to"]

                if van == "broadcaster" or van == "button":
                    name = van
                    typ = None
                else:
                    name = van[1:]
                    typ = van[0]
                modules[name] = Module(name, typ)
                configs[name] = Config(name, naar)

        newconfigs = {}
        for k, config in configs.items():
            for dst in config.destinations:
                if dst not in modules:
                    modules[dst] = Module(dst, None)
                if dst not in configs:
                    newconfigs[dst] = Config(dst, "")

        for k, new in newconfigs.items():
            configs[k] = new

        configs["button"] = Config("button", "broadcaster")

        for km, m in modules.items():
            if not m.conjunction:
                continue
            for kc, c in configs.items():
                if m.name in c.destinations:
                    m.addsrc(c.name)

        return configs, modules

    def Push(self) -> None:
        self.Q = [("button", 0)]
        while len(self.Q) > 0:
            src, val = self.Q.pop(0)
            config = self.configs[src]
            for dst in config.destinations:
                if val == 0:
                    self.lows += 1
                else:
                    self.highs += 1

                # print(f"{src}  {'-high-' if val == 1 else '-low-'} -> {dst}")
                pulse = self.modules[dst].pulse(src, val)
                if pulse is not None:
                    self.Q.append((dst, pulse))

    def PartA(self):
        self.StartPartA()

        self.configs, self.modules = self.ParseInput()
        self.highs = 0
        self.lows = 0
        for _ in range(1000):
            self.Push()

        answer = self.highs * self.lows

        self.ShowAnswer(answer)

    def PartB(self):
        self.StartPartB()

        self.configs, self.modules = self.ParseInput()

        flipflops = [mod for k, mod in self.modules.items() if mod.flipflop]
        flipflops.sort(key=lambda f: f.name)

        rx = self.modules["rx"]
        answer = 0
        while True:
            answer += 1
            if answer % 10_000 == 0:
                print(answer)
            self.Push()

            # for f  in flipflops:
            #     print("1" if f.state else "0", end="")
            # print("\r", end="", flush=True)

            if rx.gotlowpulse:
                break

        self.ShowAnswer(answer)


if __name__ == "__main__":
    solution = Day20Solution()
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        solution.Test()
    else:
        solution.Run()

# Template Version 1.5


import time
import os
from sys import platform, stdout

class Ansi():
    Reversed =      u"\u001b[7m"
    Underline =     u"\u001b[4m"
    SlowBlink =     u"\u001b[5m"
    Reset =         u"\u001b[0m"

    ClearScreen =   u"\u001b[2J"
    ClearLine =     u"\u001b[2K"

    StoreCursor =   u"\u001b[s"
    RestoreCursor = u"\u001b[u"

    HideCursor =    u"\u001b[?25l"
    ShowCursor =    u"\u001b[?25h"

    Black =         u"\u001b[30m"
    Red =           u"\u001b[31m"
    Green =         u"\u001b[32m"
    Yellow =        u"\u001b[33m"
    Blue =          u"\u001b[34m"
    Magenta =       u"\u001b[35m"
    Cyan =          u"\u001b[36m"
    White =         u"\u001b[37m"

    BrightBlack =   u"\u001b[30;1m"
    BrightRed =     u"\u001b[31;1m"
    BrightGreen =   u"\u001b[32;1m"
    BrightYellow =  u"\u001b[33;1m"
    BrightBlue =    u"\u001b[34;1m"
    BrightMagenta = u"\u001b[35;1m"
    BrightCyan =    u"\u001b[36;1m"
    BrightWhite =   u"\u001b[37;1m"

    BlackBackground =   u"\u001b[40m"
    RedBackground =     u"\u001b[41m"
    GreenBackground =   u"\u001b[42m"
    YellowBackground =  u"\u001b[43m"
    BlueBackground =    u"\u001b[44m"
    MagentaBackground = u"\u001b[45m"
    CyanBackground =    u"\u001b[46m"
    WhiteBackground =   u"\u001b[47m"

class Aoc():

    def __init__(self):
        self._day = 0
        self._start = 0
        self._end = 0
        self._part = 0
        self.inputdata = []
        self.AnswerA = None
        self.AnswerB = None

    def StartDay(self, day:int, title:str = "AOC") -> None:
        self._day = day
        self.title = title
        print(f"{Ansi.BlueBackground} {Ansi.White}Day {Ansi.BrightMagenta}{self._day}{Ansi.White} - {Ansi.Red}{self.title} {Ansi.Reset}")

    def ReadInput(self):
        self.inputdata.clear()
        if os.path.isfile(self.input_filename()) == False:
            print(f"{Ansi.BrightRed}File {self.input_filename()} not found{Ansi.Reset}")
            return

        file = open(self.input_filename(), "r")
        for line in file:
            self.inputdata.append(line.rstrip())
        file.close()

    def input_filename(self):
        return f"../input/input-day{self._day}.txt"

    def StartPartA(self):
        print("")
        print(f"{Ansi.Underline}{Ansi.BrightWhite}Part {Ansi.BrightCyan}A{Ansi.Reset}")
        self._start = time.perf_counter()
        self._part = 1

    def StartPartB(self):
        print("")
        print(f"{Ansi.Underline}{Ansi.BrightWhite}Part {Ansi.BrightCyan}B{Ansi.Reset}")
        self._start = time.perf_counter()
        self._part = 2

    def ShowAnswer(self, result):
        if self._part == 1:
            self.AnswerA = result
        else:
            self.AnswerB = result

        self._end = time.perf_counter()
        ellapsed = self._end - self._start
        print(f"Answer: {Ansi.BrightGreen}{result}{Ansi.Reset} | Took {Ansi.BrightMagenta}{ellapsed:.5f}{Ansi.Reset} seconds")
        print("")

    def GetAnswerA(self):
        return self.AnswerA

    def GetAnswerB(self):
        return self.AnswerB

    def MoveCursor(self, column: int, line: int) -> str:
        return u"\u001b[%d;%dH" % (line, column)

    def MoveCursorUp(self, lines: int) -> str:
        return u"\u001b[%dA" % lines

    def Flush(self):
        stdout.flush()

    def Assert(self, answer, goal):
        try:
            assert answer == goal
            print(f"{Ansi.GreenBackground}{Ansi.Black}OK{Ansi.Reset}")
            print("")
        except AssertionError as e:
            print(f"{Ansi.RedBackground}{Ansi.BrightWhite}Test Failed{Ansi.Reset} {Ansi.BrightRed}{answer}{Ansi.Reset} is not equal to {Ansi.BrightGreen}{goal}{Ansi.Reset}")
            print("")
        else:
            pass
        finally:
            pass

if platform == "win32":
    import msvcrt, ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

## Main

if __name__ == "__main__":
    aoc = Aoc()
    aoc.StartPartA()
    time.sleep(1)
    aoc.ShowAnswer(42)
    aoc.StartPartB()
    time.sleep(0.4)
    aoc.ShowAnswer(80085)

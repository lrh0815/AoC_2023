from aoc_helper.AoCHelper import *
import re
from dataclasses import dataclass
from icecream import ic
from collections import deque
from rich import print
from rich.progress import track
from rich.status import Status


class DaySolver(PuzzleSolver):
    def __init__(self):
        PuzzleSolver.__init__(self, 2023, x, None, None, True)

    def solve_a(self, input: list[str]):
        return None

    def solve_b(self, input: list[str]):
        return None


example_input1 = """""".splitlines()

example_input2 = """""".splitlines()

if __name__ == "__main__":
    AoCHelper(DaySolver())\
        .test()\
        .test_with('a', example_input1, None)\
        .test_with('b', example_input2, None)\
        .solve().submit()

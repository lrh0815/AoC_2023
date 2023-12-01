from aocd.models import Puzzle
from colorama import Fore
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


def chunk_input(input, size):
    for i in range(0, len(input), size):
        yield input[i:i+size]


def sign(n):
    if n < 0:
        return -1
    elif n > 0:
        return 1
    else:
        0


@dataclass(frozen=True,)
class Point(object):
    x: int
    y: int
    z: Optional[int] = 0

    def __add__(self, o):
        if type(o) is Point:
            return Point(self.x + o.x, self.y+o.y, self.z+o.z)
        if type(o) is tuple:
            if len(o) == 2:
                return Point(self.x + o[0], self.y+o[1])
            if len(o) == 3:
                return Point(self.x + o[0], self.y+o[1], self.z+o[2])


class Grid(object):
    def __init__(self, default_value=None):
        self.default_value = default_value
        self.__grid = {}

    def set(self, point: Point, value):
        self.__grid[point] = value

    def reset(self, point: Point):
        return self.__grid.pop(point, self.default_value)

    def get(self, point: Point):
        return self.__grid.get(point, self.default_value)
    
    def is_set(self, point: Point):
        return point in self.__grid.keys()

    @property
    def min_x(self) -> int:
        return min([k.x for k in self.__grid.keys()])

    @property
    def max_x(self) -> int:
        return max([k.x for k in self.__grid.keys()])

    @property
    def min_y(self) -> int:
        return min([k.y for k in self.__grid.keys()])

    @property
    def max_y(self) -> int:
        return max([k.y for k in self.__grid.keys()])

    @property
    def min_z(self) -> int:
        return min([k.z for k in self.__grid.keys()])

    @property
    def max_z(self) -> int:
        return max([k.z for k in self.__grid.keys()])

    def all_set_points(self) -> list[Point]:
        return [p for p in self.__grid.keys()]

    def contains(self, point: Point):
        return self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y and self.min_z <= point.z <= self.max_z

    def print_grid(self, min_x=None, max_x=None, min_y=None, max_y=None, min_z=None, max_z=None, reverse_y=False):
        min_x = self.min_x if min_x == None else min_x
        max_x = self.max_x if max_x == None else max_x
        min_y = self.min_y if min_y == None else min_y
        max_y = self.max_y if max_y == None else max_y
        min_z = self.min_z if min_z == None else min_z
        max_z = self.max_z if max_z == None else max_z
        for z in range(min_z, max_z+1):
            print(f"z = {z}")
            print("    ", end="")
            for x in range(min_x, max_x + 1, 2):
                if x >= 100:
                    print(f"{(x//100)%10}", end=" ")
                else:
                    print(" ", end=" ")
            print()
            print("    ", end="")
            for x in range(min_x, max_x + 1, 2):
                if x >= 10:
                    print(f"{(x//10)%10}", end=" ")
                else:
                    print(" ", end=" ")
            print()
            print("    ", end="")
            for x in range(min_x, max_x + 1, 2):
                print(f"{x%10}", end=" ")
            print()
            print("    ", end="")
            for x in range(min_x, max_x + 1, 2):
                print(f"|", end=" ")

            if reverse_y:
                y_range = range(min_y, max_y + 1)
            else:
                y_range = range(max_y, min_y - 1, -1)
            for y in y_range:
                print()
                print(f"{y:3} ", end="")
                for x in range(min_x, max_x + 1):
                    print(self.get(Point(x, y, z)), end="")

            print()
            print("    ", end="")
            for x in range(min_x, max_x + 1, 2):
                print(f"|", end=" ")
            print()
            print("    ", end="")
            for x in range(min_x, max_x + 1, 2):
                if x >= 100:
                    print(f"{(x//100)%10}", end=" ")
                else:
                    print("|", end=" ")
            print()
            print("    ", end="")
            for x in range(min_x, max_x + 1, 2):
                if x >= 10:
                    print(f"{(x//10)%10}", end=" ")
                else:
                    print("|", end=" ")
            print()
            print("    ", end="")
            for x in range(min_x, max_x + 1, 2):
                print(f"{x%10}", end=" ")
            print()


class PuzzleSolver(ABC):
    def __init__(self, year: int, day: int, example_answer_a, example_answer_b, do_submit: bool):
        self.year = year
        self.day = day
        self.example_answers = {'a': example_answer_a, 'b': example_answer_b}
        self.solvers = {'a': self.solve_a, 'b': self.solve_b}
        self.do_submit = do_submit

    @abstractmethod
    def solve_a(self, input: list[str]):
        pass

    @abstractmethod
    def solve_b(self, input: list[str]):
        pass


class AoCHelper(object):

    def __init__(self, puzzle_solver: PuzzleSolver):
        self.puzzle = Puzzle(puzzle_solver.year, puzzle_solver.day)
        self.puzzle_solver = puzzle_solver
        self.test_results = {'a': None, 'b': None}
        self.solutions = {'a': None, 'b': None}
        self.submitters = {'a': self.__submit_a, 'b': self.__submit_b}

    def print_input(self):
        print(self.puzzle.input_data)
        return self

    def print_example_input(self):
        print(self.puzzle.example_data)
        return self

    def __get_parts(self, part):
        if part == None:
            parts = ['a', 'b']
        else:
            parts = [part]
        return parts

    def test_with(self, part, input: list[str], expected_answer):
        print()
        self.__test_for_part(part, input, expected_answer)
        return self

    def test(self, part=None):
        print()
        input = self.puzzle.example_data.splitlines()
        for part in self.__get_parts(part):
            self.__test_for_part(part, input, self.puzzle_solver.example_answers[part])
        return self

    def __test_for_part(self, part, input, expected_answer):
        print(f'Test {part}: ')
        result = self.__test(self.puzzle_solver.solvers[part], input, expected_answer)
        if self.test_results[part] == None:
            self.test_results[part] = result
        else:
            self.test_results[part] = self.test_results[part] and result

    def __test(self, solver, input, expected_answer):
        if solver != None and expected_answer != None:
            answer = solver(input)
            if answer == expected_answer:
                print(Fore.GREEN + 'PASSED' + Fore.RESET)
                return True
            else:
                print(Fore.RED + 'FAILED' + Fore.RESET +
                      f' (expected {expected_answer} but was {answer})')
                return False
        else:
            print(Fore.YELLOW + 'IGNORED' + Fore.RESET)
            return None

    def solve(self, part=None):
        print()
        for part in self.__get_parts(part):
            self.solutions[part] = self.__solve_for_part(part)
        return self

    def __solve_for_part(self, part):
        print(f'Solve {part}: ')
        return self.__solve(self.test_results[part], self.puzzle_solver.solvers[part])

    def __solve(self, test_result: bool, solver):
        if test_result == False:
            print(Fore.RED + 'test failed' + Fore.RESET)
        elif test_result == None:
            print(Fore.YELLOW + 'not tested' + Fore.RESET)
        elif solver == None:
            print(Fore.YELLOW + 'no solver' + Fore.RESET)
        else:
            answer = solver(self.puzzle.input_data.splitlines())
            print(f'{answer}')
            return answer
        return None

    def submit(self, part=None):
        print()
        for part in self.__get_parts(part):
            self.__submit_for_part(part)
        return self

    def __submit_for_part(self, part):
        print(f'Submit {part}: ', end='')
        self.__submit(self.solutions[part], self.submitters[part])

    def __submit(self, solution, submitter):
        if solution == None:
            print(Fore.RED + 'not solved')
        elif self.puzzle_solver.do_submit == True:
            print(solution)
            submitter(solution)
        else:
            print(f'{solution} ' + Fore.CYAN + 'not submitted')

    def __submit_a(self, solution):
        self.puzzle.answer_a = solution

    def __submit_b(self, solution):
        self.puzzle.answer_b = solution

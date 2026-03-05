from abc import ABC, abstractmethod

class Solver(ABC):
    def __init__(self, args):
        pass

    @abstractmethod
    def solve(self, inst, args, output_filename):
        pass

    @abstractmethod
    def solve_all(self, insts, args, output_filename):
        pass

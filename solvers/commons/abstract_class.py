from abc import ABC, abstractmethod

class Solver(ABC):
    def __init__(self, args):
        pass

    @abstractmethod
    def solve(self, inst, args, individual):
        pass

    @abstractmethod
    def solve_all(self, insts, args, individual):
        pass

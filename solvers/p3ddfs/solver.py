import multiprocessing as mp
import subprocess

from solvers.commons.postprocessing import print_results, store_results, extract_results
from solvers.commons.abstract_class import Solver

allowed_braching_rules = [
    "dantzig",
    "dantzig_mvar"
]

class P3DDFS_solver(Solver):
    def __init__(self, args):
        self.output_filename = p3ddfs_parse_args(args)

    def solve(self, inst, args, individual = ""):
        """
        Solve a single optimization instance using P3D-DFS solver.

        The generation of the instance to solve is managed by the solver itself.
        Other parameters allow to configure the solver.

        Optionally prints and/or saves results according to the user arguments.
        """
        results = subprocess.run(
            [
                "./main_knapsack.out",
                "--mode", "sequential",
                "--ub", "dantzig_mvar",
                "--lb", "inf",
                "--mvar", str(args.nv),
                "--ind", individual,
                "--n", str(inst.n),
                "--r", str(inst.r),
                "--t", str(inst.t),
                "--id", str(inst.i)
            ],
            capture_output=True,
            text=True,
            cwd="solvers/p3ddfs/"
        )

        instancename = inst.get_name()

        if not args.no_output:
            print_results('p3ddfs', instancename, results.stdout, args.check_output)
        if args.save_output:
            store_results('p3ddfs', instancename, results.stdout, self.output_filename, args.check_output)

    def solve_all(self, insts, args, individual = ""):
        """
        Solve a series of optimization instances using P3D-DFS solver.

        This method relies on the 'solve' method, and allows parallel solving.
        """
        if args.parmode:
            args_list = [(inst, args) for inst in insts]
            with mp.Pool(processes=mp.cpu_count()) as pool:
                pool.starmap(self.solve, args_list)
        else:
            for inst in insts:
                self.solve(inst, args, individual)

def p3ddfs_parse_args(args):
    """
    Parse user arguments to generate P3D-DFS parameters and outputs.
    """
    if args.timelimit is not None:
        # NOTE: timelimit not yet implemented in P3D-DFS solver
        pass

    branch_rule = allowed_braching_rules[args.b]

    if branch_rule == "dantzig_mvar":
        output_filename = f"p3ddfs_knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}_{args.nv}.txt"
    else:
        output_filename = f"p3ddfs_knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}.txt"

    return output_filename

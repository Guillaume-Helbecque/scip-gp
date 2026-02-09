from instances.generate_instances import compile_generator, clean_files, instance

from solvers.scip.solver import scip_parse_args, scip_solve_instance, scip_solve_all_instances
from solvers.scip.util import extract_results

from solvers.p3ddfs.solver import p3ddfs_solve_instance, p3ddfs_solve_all_instances

from genetic_programming.gp_engine import run_gp
from genetic_programming.util import print_gp_convergence, save_logbook, load_logbook

from utils.argument_parser import parser

import os

try:
    # Standard case when running from a .py file
    work_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Fallback for interactive environments
    import inspect
    frame = inspect.currentframe()
    filename = inspect.getfile(frame)
    work_dir = os.path.dirname(os.path.abspath(filename))

os.chdir(work_dir)

if __name__ == '__main__':
    args = parser.parse_args()

    if args.solver == 'scip':
        compile_generator()
        param_dict, output_filename = scip_parse_args(args)

        if args.solve_all:
            # Solve all instances in series (`S` in total)
            insts = [instance(args.n, args.t, args.r, i) for i in range(1, args.s+1)]
            scip_solve_all_instances(insts, args, param_dict, output_filename)
            print("All instances completed successfully.")
        else:
            # Solve only the instance given by `-i`
            inst = instance(args.n, args.t, args.r, args.i)
            scip_solve_instance(inst, args, param_dict, output_filename)
            print("The instance completed successfully.")

    elif args.solver == 'p3d-dfs':
        if args.solve_all:
            # Solve all instances in series (`S` in total)
            insts = [instance(args.n, args.t, args.r, i) for i in range(1, args.s+1)]
            p3ddfs_solve_all_instances(insts, args, "output_filename")
            print("All instances completed successfully.")
        else:
            # Solve only the instance given by `-i`
            inst = instance(args.n, args.t, args.r, args.i)
            p3ddfs_solve_instance(inst, args, "output_filename")
            print("The instance completed successfully.")

    # pop, logbook, hof = run_gp()
    #
    # for ind in hof:
    #     print(ind)
    #
    # save_logbook(logbook, "logbook.txt")
    # print_gp_convergence(logbook)

    clean_files()

from instances.generate_instances import compile_generator, clean_files

from scip_solver.solver import parse_args, solve_instance, solve_all_instances
from scip_solver.util import extract_results

from genetic_programming.gp_engine import run_gp
from genetic_programming.util import print_gp_convergence

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
    compile_generator()
    args, param_dict, output_filename = parse_args()

    if args.solve_all:
        # Solve all instances in series (`S` in total)
        solve_all_instances(args, param_dict, output_filename)
        print("All instances completed successfully.")
    else:
        # Solve only the instance given by `-i`
        solve_instance(args, args.i, param_dict, output_filename)
        print("The instance completed successfully.")
    pop, logbook, hof = run_gp()

    for ind in hof:
        print(ind)

    print_gp_convergence(logbook)

    clean_files()

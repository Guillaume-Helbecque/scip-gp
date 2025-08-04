from instances.generate_instances import compile_generator, clean_files
from scip_solver.solver import parse_args, solve_instance, solve_all_instances

import os

try:
    work_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
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
    else:
        # Solve only the instance given by `-i`
        solve_instance(args, args.i, param_dict, output_filename)

    clean_files()

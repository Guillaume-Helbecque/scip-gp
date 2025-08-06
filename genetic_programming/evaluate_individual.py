from deap import gp
from scip_solver.solver import parse_args, solve_all_instances
from scip_solver.util import extract_results

def evaluate(individual, pset):
    """
    TODO
    """
    print(individual)
    func = gp.compile(individual, pset)
    args, param_dict, output_filename = parse_args()
    args.no_output=True
    args.save_output=True
    output_filename += "_" + str(individual)
    solve_all_instances(args, param_dict, output_filename, func)
    mean_time, mean_gap, mean_nodes = extract_results(output_filename, args.check_output, False)

    if args.timelimit is not None:
        return mean_gap,
    else:
        return mean_time,

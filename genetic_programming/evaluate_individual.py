from scip_solver.solver import parse_args, solve_all_instances
from scip_solver.util import extract_results

from instances.instance_sets import determine_training_set

from deap import gp

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
    # NOTE: the instance set could be given as an argument to evaluate
    instance_set = determine_training_set()
    # TODO: implement a function that solves the given set of instances
    solve_all_instances(args, param_dict, output_filename, func)
    mean_time, mean_gap, mean_nodes = extract_results(output_filename, args.check_output, False)

    if args.timelimit is not None:
        return mean_gap,
    else:
        return mean_time,

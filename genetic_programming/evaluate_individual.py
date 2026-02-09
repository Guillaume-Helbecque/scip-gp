from solvers.scip.solver import scip_parse_args, scip_solve_all_instances
from solvers.scip.util import extract_results

from instances.instance_sets import determine_training_set

from utils.argument_parser import parser

from deap import gp

def evaluate(individual, pset):
    """
    TODO
    """
    print(individual)
    func = gp.compile(individual, pset)
    args = parser.parse_args()
    param_dict, output_filename = scip_parse_args(args)
    args.no_output=True
    args.save_output=True
    output_filename += "_" + str(individual)
    # NOTE: the instance set could be given as an argument to evaluate
    instance_set = determine_training_set()
    solve_all_instances(instance_set, args, param_dict, output_filename, func)
    mean_time, mean_gap, mean_nodes = extract_results(output_filename, args.check_output, False)

    if args.timelimit is not None:
        return mean_gap,
    else:
        return mean_time,

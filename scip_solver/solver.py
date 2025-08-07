from instances.generate_instances import generate_instance
from scip_solver.custom_branching.StrongBranchingRule import StrongBranchingRule
from scip_solver.custom_branching.StrongMultiBranchingRule import StrongMultiBranchingRule
from scip_solver.custom_branching.StrongMultiBranchingRule_gp import StrongMultiBranchingRule_gp
from scip_solver.util import parser, print_results, store_results, extract_results
from scip_solver.generate_model import create_model

from pyscipopt import Model, SCIP_PARAMSETTING
import multiprocessing as mp

# NOTE: the following function is only available on POSIX systems.
mp.set_start_method("fork", force=True)
global_func = None

allowed_braching_rules = [
    "default",
    "customStrongBranching",
    "customStrongMultiBranching",
    "customStrongMultiBranching_gp"
]

def parse_args():
    """
    TODO
    """
    args = parser.parse_args()

    param_dict = {
        "nodeselection/dfs/stdpriority": 1073741823,
        "misc/usesymmetry": 5,
    }

    if args.timelimit is not None:
        param_dict.update({"limits/time": args.timelimit})

    # if args.parmode: print(f"Number of CPU: {mp.cpu_count()}\n")

    branch_rule = allowed_braching_rules[args.b]

    if branch_rule == "customStrongMultiBranching":
        output_filename = f"knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}_{args.nv}.txt"
    else:
        output_filename = f"knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}.txt"

    return args, param_dict, output_filename

def setBranchingRule(scip, branch_id, num_vars, function):
    """
    Configure and set the SCIP branching rule.

    The branching rule is chosen based on the `-b` option.
    Supported rules include:
      - "default": SCIP default strong branching rule.
      - "customStrongBranching": User-defined strong branching rule.
      - "customStrongMultiBranching": User-defined multi-variable strong branching rule.
    """
    branch_rule = allowed_braching_rules[branch_id]

    match branch_rule:
        case "default":
            scip.setParam("branching/fullstrong/priority", 536870911)
        case "customStrongBranching":
            custom_branch_rule = StrongBranchingRule(scip)
            scip.includeBranchrule(custom_branch_rule, "", "",
                priority=536870911, maxdepth=-1, maxbounddist=1)
        case "customStrongMultiBranching":
            custom_branch_rule = StrongMultiBranchingRule(scip, num_vars)
            scip.includeBranchrule(custom_branch_rule, "", "",
                priority=536870911, maxdepth=-1, maxbounddist=1)
        case "customStrongMultiBranching_gp":
            custom_branch_rule = StrongMultiBranchingRule_gp(scip, function)
            scip.includeBranchrule(custom_branch_rule, "", "",
                priority=536870911, maxdepth=-1, maxbounddist=1)

def solve_instance(inst, args, param_dict, output_filename, function = lambda x,y: 1):
    """
    Solve a single optimization instance using SCIP.

    This function generates an instance based on given parameters,
    creates the corresponding SCIP model, applies configuration parameters,
    and runs the optimization.

    Optionally prints and/or saves results according to the user arguments.
    """
    if args.parmode:
        global global_func
        function = global_func

    instancename = generate_instance(inst, args.s)
    scip = create_model(instancename)
    scip.setParams(param_dict)
    scip.setHeuristics(SCIP_PARAMSETTING.OFF)
    scip.setPresolve(SCIP_PARAMSETTING.OFF)
    scip.setSeparating(SCIP_PARAMSETTING.OFF)
    scip.hideOutput()
    setBranchingRule(scip, args.b, args.nv, function)
    scip.optimize()

    if not args.no_output:
        print_results(instancename, scip, args.check_output)
    if args.save_output:
        store_results(instancename, scip, output_filename, args.check_output)

def solve_all_instances(insts, args, param_dict, output_filename, function = lambda x,y: 1):
    """
    TODO
    """
    if args.parmode:
        global global_func
        global_func = function

        args_list = [(inst, args, param_dict, output_filename) for inst in insts]
        with mp.Pool(processes=mp.cpu_count()) as pool:
            pool.starmap(solve_instance, args_list)
    else:
        for inst in insts:
            solve_instance(inst, args, param_dict, output_filename, function)

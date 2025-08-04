from instances.generate_instances import generate_instance
from scip_solver.custom_branching.StrongBranchingRule import StrongBranchingRule
from scip_solver.custom_branching.StrongMultiBranchingRule import StrongMultiBranchingRule
from scip_solver.util import parser, print_results, store_results, extract_results
from scip_solver.generate_model import create_model

from pyscipopt import Model, SCIP_PARAMSETTING
import multiprocessing as mp

allowed_braching_rules = [
    "default",
    "customStrongBranching",
    "customStrongMultiBranching",
]

def parse_args():
    args = parser.parse_args()

    param_dict = {
        "nodeselection/dfs/stdpriority": 1073741823,
        "limits/time": args.timelimit,
        "misc/usesymmetry": 5,
    }

    if args.parmode: print(f"Number of CPU: {mp.cpu_count()}\n")

    branch_rule = allowed_braching_rules[args.b]

    if branch_rule == "customStrongMultiBranching":
        output_filename = f"knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}_{args.nv}.txt"
    else:
        output_filename = f"knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}.txt"

    return args, param_dict, output_filename

def setBranchingRule(scip, branch_id, num_vars):
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

def solve_instance(args, id, param_dict, output_filename):
    """
    Solve a single optimization instance using SCIP.

    This function generates an instance based on given parameters,
    creates the corresponding SCIP model, applies configuration parameters,
    and runs the optimization.

    Optionally prints and/or saves results according to the user arguments.
    """
    instancename = generate_instance(args.n, args.t, args.r, id, args.s)
    scip = create_model(instancename)
    scip.setParams(param_dict)
    scip.setHeuristics(SCIP_PARAMSETTING.OFF)
    scip.setPresolve(SCIP_PARAMSETTING.OFF)
    scip.setSeparating(SCIP_PARAMSETTING.OFF)
    scip.hideOutput()
    setBranchingRule(scip, args.b, args.nv)
    scip.optimize()

    if not args.no_output:
        print_results(instancename, scip, args.check_output)
    if args.save_output:
        store_results(instancename, scip, output_filename, args.check_output)
    if not args.solve_all:
        print("The instance completed successfully.")

def solve_all_instances(args, param_dict, output_filename):

    if args.parmode:
        args_list = [(args, id, param_dict, output_filename) for id in range(1, args.s+1)]
        with mp.Pool(processes=mp.cpu_count()) as pool:
            pool.starmap(solve_instance, args_list)
    else:
        for id in range(1, args.s+1):
            solve_instance(args, id, param_dict, output_filename)

    print("All instances completed successfully.")

import os
import multiprocessing as mp

print("Number of CPU : ", mp.cpu_count())

try:
    work_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    import inspect
    frame = inspect.currentframe()
    filename = inspect.getfile(frame)
    work_dir = os.path.dirname(os.path.abspath(filename))

os.chdir(work_dir)

from instances.generate_instances import compile_generator, generate_instance, clean_files
from branching.StrongBranchingRule import StrongBranchingRule
from branching.StrongMultiBranchingRule import StrongMultiBranchingRule
from model.generate_model import create_model
from util import parser, print_results, store_results, extract_results

from pyscipopt import Model, SCIP_PARAMSETTING

## Configuration

allowed_braching_rules = [
    "default",
    "customStrongBranching",
    "customStrongMultiBranching",
]

args = parser.parse_args()

branch_rule = allowed_braching_rules[args.b]

if branch_rule == "customStrongMultiBranching":
    output_filename = f"knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}_{args.nv}.txt"
else:
    output_filename = f"knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}.txt"

param_dict = {
    "nodeselection/dfs/stdpriority": 1073741823,
    "limits/time": args.timelimit,
    "misc/usesymmetry": 5,
}

def setBranchingRule(scip):
    """
    Configure and set the SCIP branching rule.

    The branching rule is chosen based on the `-b` option.
    Supported rules include:
      - "default": SCIP default strong branching rule.
      - "customStrongBranching": User-defined strong branching rule.
      - "customStrongMultiBranching": User-defined multi-variable strong branching rule.
    """
    match branch_rule:
        case "default":
            scip.setParam("branching/fullstrong/priority", 536870911)
        case "customStrongBranching":
            custom_branch_rule = StrongBranchingRule(scip)
            scip.includeBranchrule(custom_branch_rule, "", "",
                priority=536870911, maxdepth=-1, maxbounddist=1)
        case "customStrongMultiBranching":
            custom_branch_rule = StrongMultiBranchingRule(scip, args.nv)
            scip.includeBranchrule(custom_branch_rule, "", "",
                priority=536870911, maxdepth=-1, maxbounddist=1)

## SCIP solving

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
    setBranchingRule(scip)
    scip.optimize()

    if not args.no_output:
        print_results(instancename, scip)
    if args.save_output:
        store_results(instancename, scip, output_filename)

if __name__ == '__main__':
    compile_generator()

    if args.solve_all:
        # Solve all instances in series (`S` in total)
        if args.parmode:
            args_list = [(args, id, param_dict, output_filename) for id in range(1, args.s + 1)]
            with mp.Pool(processes=mp.cpu_count()) as pool:
                pool.starmap(solve_instance, args_list)
        else:
            for id in range(1, args.s+1):
                solve_instance(args, id, param_dict, output_filename)
    else:
        # Solve only the instance given by `-i`
        solve_instance(args, args.i, param_dict, output_filename)

    clean_files()
    print("All instances completed successfully.")

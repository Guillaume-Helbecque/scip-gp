import os

try:
    work_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    import inspect
    frame = inspect.currentframe()
    filename = inspect.getfile(frame)
    work_dir = os.path.dirname(os.path.abspath(filename))

os.chdir(work_dir)

from instances.generate_instances import generate_instance, clean_files
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
    output_filename = f"knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}_{args.nvar}.txt"
else:
    output_filename = f"knapPI_{args.t}_{args.n}_{args.r}_{branch_rule}.txt"

param_dict = {
    "nodeselection/dfs/stdpriority": 1073741823,
    "limits/time": args.timelimit,
    "misc/usesymmetry": 5,
}

def setBranchingRule(scip):
    """
    Sets the SCIP branching rule based on the `branch_rule` option.
    """
    match branch_rule:
        case "default":
            scip.setParam("branching/fullstrong/priority", 536870911)
        case "customStrongBranching":
            custom_branch_rule = StrongBranchingRule(scip)
            scip.includeBranchrule(custom_branch_rule, "", "",
                priority=536870911, maxdepth=-1, maxbounddist=1)
        case "customStrongMultiBranching":
            custom_branch_rule = StrongMultiBranchingRule(scip, args.nvar)
            scip.includeBranchrule(custom_branch_rule, "", "",
                priority=536870911, maxdepth=-1, maxbounddist=1)

## SCIP solving

if args.solve_all:
    # Solve all instances in series (`S` in total)
    for id in range(1, args.s+1):
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
else:
    # Solve only instance `id`
    instancename = generate_instance(args.n, args.t, args.r, args.i, args.s)
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

clean_files()

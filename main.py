import os
os.chdir("/home/ghelbecq/Bureau/scip-rl/")

from instances.generate_instances import generate_instance, clean_files
from model.generate_model import create_model
from util import print_results, store_results

from pyscipopt import Model, SCIP_PARAMSETTING

# TODO:
#     - Improve the way we navigate between directories

## Global parameters

save_output = False
solve_all   = False

n = 100
type = 11
r = 1000
S = 100
id = 1

## SCIP solving

param_dict = {
    "nodeselection/dfs/stdpriority": 1073741823,
    "branching/fullstrong/priority": 536870911,
}

if solve_all:
    # Solve all instances in series (`S` in total)
    for id in range(1, S+1):
        instancename = generate_instance(n, type, r, id, S)
        scip = create_model(instancename)
        scip.setParams(param_dict)
        scip.setHeuristics(SCIP_PARAMSETTING.OFF)
        scip.setPresolve(SCIP_PARAMSETTING.OFF)
        scip.hideOutput()
        scip.optimize()
        print_results(instancename, scip)
        if save_output:
            store_results(instancename, scip, "test_output.txt")
else:
    # Solve only instance `id`
    instancename = generate_instance(n, type, r, id, S)
    scip = create_model(instancename)
    scip.setParams(param_dict)
    scip.setHeuristics(SCIP_PARAMSETTING.OFF)
    scip.setPresolve(SCIP_PARAMSETTING.OFF)
    scip.hideOutput()
    scip.optimize()
    print_results(instancename, scip)
    if save_output:
        store_results(instancename, scip, "test_output.txt")

clean_files()

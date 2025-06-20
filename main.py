import os
os.chdir("/home/ghelbecq/Bureau/scip-rl/")

from instances.generate_instances import generate_instance
from model.generate_model import create_model
from util import print_results

from pyscipopt import Model, SCIP_PARAMSETTING

n = 5000
type = 9
r = 100000
id = 17

param_dict = {
    "nodeselection/dfs/stdpriority": 1073741823,
}

filename = generate_instance(n, type, r, id)
scip = create_model(filename)
scip.setParams(param_dict)
scip.setHeuristics(SCIP_PARAMSETTING.OFF)
scip.setPresolve(SCIP_PARAMSETTING.OFF)
scip.hideOutput()
scip.optimize()
print_results(scip)

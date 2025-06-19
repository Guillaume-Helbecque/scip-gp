import os
from pyscipopt import Model, quicksum

def extract_data(filename):
    """
    Extracts instance data contained inside a file.
    """
    os.chdir("/home/ghelbecq/Bureau/scip-rl/instances/")

    with open(filename, 'r') as f:
        lines = f.readlines()

    n = int(lines[0].strip())

    p = []
    w = []
    for line in lines[1:n+1]:
        _, profit, weight = map(int, line.strip().split())
        p.append(profit)
        w.append(weight)

    c = int(lines[n+1].strip())

    return n, c, p, w

def create_model(n, c, p, w):
    """
    Create a SCIP model based on the given instance data.
    """
    model = Model()

    # Create binary decision variables
    x = {}
    for i in range(n):
        x[i] = model.addVar(vtype="B", name=f"x_{i}")

    # Add the capacity constraint
    model.addCons(quicksum(w[i] * x[i] for i in range(n)) <= c, "capacity")

    # Set the objective
    model.setObjective(quicksum(p[i] * x[i] for i in range(n)), sense="maximize")

    return model

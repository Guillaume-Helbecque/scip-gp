import os
from pyscipopt import Model, quicksum

def _extract_data(filename):
    """
    Extract instance data from a given file for a knapsack problem.

    The file format is expected as follows:
    - First line: integer `n` representing the number of items.
    - Next `n` lines: each containing three integers (index, profit, weight).
    - The line after these `n` lines: integer `c` representing the knapsack capacity.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    n = int(lines[0].strip())

    p = []
    w = []
    for line in lines[1:n+1]:
        _, profit, weight = map(int, line.strip().split())
        p.append(profit)
        w.append(weight)

    # c = int(lines[n+1].strip())
    c = lines[n+1].strip()

    return n, c, p, w

def _sort_data(n, weights, profits):
    """
    TODO
    """
    ratios = [profits[i] / weights[i] for i in range(n)]

    for i in range(n):
        max_ratio = max(ratios[i:])
        max_idx = ratios.index(max_ratio, i)
        ratios[i], ratios[max_idx] = ratios[max_idx], ratios[i]
        weights[i], weights[max_idx] = weights[max_idx], weights[i]
        profits[i], profits[max_idx] = profits[max_idx], profits[i]

def create_model(filename):
    """
    Build a SCIP optimization model for the knapsack problem from an instance file.
    """
    n, c, p, w = _extract_data(os.path.join("instances", filename))
    _sort_data(n, w, p)

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

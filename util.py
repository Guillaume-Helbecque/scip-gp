def print_results(model):
    """
    Defines a custom output for SCIP solver.
    """
    print("SCIP Status       :", model.getStatus())
    print("Solving Time (sec):", model.getSolvingTime())
    print("Solving Nodes     :", model.getNNodes())
    print("Primal Bound      :", model.getObjVal())
    print("Solution(s) found :", model.getNSolsFound())

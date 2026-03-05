import re
import os

def get_solving_time(solver, results):
    if solver == 'scip':
        return results.getSolvingTime()
    elif solver == 'p3ddfs':
        m = re.search(r"Elapsed time:\s*([0-9.]+)\s*\[s\]", results)
        return float(m.group(1))

def get_number_nodes(solver, results):
    if solver == 'scip':
        return results.getNNodes()
    elif solver == 'p3ddfs':
        m = re.search(r"Size of the explored tree:\s*([0-9]+)", results)
        return int(m.group(1))

def get_optimal_found(solver, results):
    if solver == 'scip':
        return results.getObjVal()
    elif solver == 'p3ddfs':
        m = re.search(r"Optimum found:\s*([0-9]+(?:\.[0-9]+)?)", results)
        return float(m.group(1))

def get_number_solutions(solver, results):
    if solver == 'scip':
        return results.getNSolsFound()
    elif solver == 'p3ddfs':
        m = re.search(r"Number of optimal solutions:\s*([0-9]+)", results)
        return int(m.group(1))

def get_status(solver, results):
    if solver == 'scip':
        return results.getStatus()
    elif solver == 'p3ddfs':
        return "not yet implemented"

def get_optimality_gap(solver, results):
    if solver == 'scip':
        return results.getGap()
    elif solver == 'p3ddfs':
        return "not yet implemented"

def print_results(solver, instancename, results, check):
    """
    Print summary results from a B&B model optimization to standard output.
    """
    instancename = os.path.splitext(instancename)[0]

    print("Instance          :", instancename)
    print("B&B Solver        :", solver)
    print("B&B Status        :", get_status(solver, results))
    print("Solving Time (sec):", get_solving_time(solver, results))
    print("Gap               :", get_optimality_gap(solver, results))
    print("Solving Nodes     :", get_number_nodes(solver, results))
    if get_number_solutions(solver, results):
        print("Objective value   :", get_optimal_found(solver, results))
        print("Solutions found   :", get_number_solutions(solver, results))
    # if check:
    #     # NOTE: 'check' disabled for now
    #     c = _check_results(instancename, model)
    #     if get_status(solver, results) == "optimal":
    #         if c: print("Check             : Success")
    #         elif (c == False): print("Check             : Fail")
    #         else: print("Check             : None")
    #     else:
    #         print("Check             : None")
    print("")

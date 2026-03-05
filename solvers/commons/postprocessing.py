import re
import os
import pandas as pd

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
        # NOTE: workaround since no status in P3D-DFS yet
        if get_number_solutions(solver, results):
            return 'optimal'
        else:
            return 'timelimit'

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

    if check:
        c = _check_results(instancename, solver, results)
        if get_status(solver, results) == "optimal":
            if c: print("Check             : Success")
            elif (c == False): print("Check             : Fail")
            else: print("Check             : None")
        else:
            print("Check             : None")

def store_results(solver, instancename, results, filename, check):
    """
    Append optimization results from a B&B model to an output file.

    Creates the output directory if it does not exist. Writes a header line
    if the file is new. Each call appends a line with instance results.
    """
    os.makedirs("outputs", exist_ok=True)

    instancename = os.path.splitext(instancename)[0]
    filename = os.path.join("outputs", filename)

    header = (
        f"{'Instance':<26}"
        f"{'B&B Status':<12}"
        f"{'Solving Time (sec)':<20}"
        f"{'Gap':<8}"
        f"{'Solving Nodes':<15}"
        f"{'Objective value':<17}"
        f"{'Solutions found':<15}"
    )

    if check:
        c = _check_results(instancename, solver, results)
        # NOTE: Nested f-strings allowed from Python 3.12+
        # header += f"{f'{'Check':<7}':>9}"
        formatted = f"{'Check':<7}"
        header += f"{formatted:>9}"

    header += "\n"

    # Write header if file does not exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(header)

    # Append a new data line
    with open(filename, "a") as f:
        # NOTE: By default, SCIP returns gap=1e+20 if no solution is found
        # NOTE: gap not yet implemented for P3D-DFS solver
        if solver == 'p3ddfs':
            gap = 0
        elif solver == 'scip':
            gap = get_optimality_gap(solver, results)
        gap_str = f"{'1e+20':<8}" if gap == 1e20 else f"{gap:<8.4f}"

        f.write(
            f"{instancename:<26}"
            f"{get_status(solver, results):<12}"
            f"{get_solving_time(solver, results):<20.4f}"
            f"{gap_str}"
            f"{get_number_nodes(solver, results):<15}"
        )

        if get_number_solutions(solver, results):
            f.write(
                f"{get_optimal_found(solver, results):<17.1f}"
                f"{get_number_solutions(solver, results):<15}"
            )
        else:
            f.write(
                f"{'':<17}"
                f"{'':<15}"
            )

        if check:
            if get_status(solver, results) == "optimal":
                # NOTE: Nested f-strings allowed from Python 3.12+
                if c:
                    formatted = f"{'Success':<7}"
                    f.write(f"{formatted:>9}")
                elif (c == False):
                    formatted = f"{'Fail':<7}"
                    f.write(f"{formatted:>9}")
                else:
                    formatted = f"{'None':<7}"
                    f.write(f"{formatted:>9}")

            else:
                formatted = f"{'None':<7}"
                f.write(f"{formatted:>9}")

        f.write("\n")

def extract_results(filename, check, show_output=True):
    """
    Load and summarize results from an output file containing SCIP results.
    """
    columns=[
        "Instance",
        "B&B_Status",
        "Solving_Time",
        "Gap",
        "Solving_Nodes",
        "Objective value",
        "Solutions_found"
    ]

    if check:
        columns.append("Check")

    data = pd.read_csv(
        os.path.join("outputs", filename),
        sep=r'\s+',
        skiprows=1,
        header=None,
        names=columns
    )

    mean_time = data["Solving_Time"].mean()
    mean_gap = data["Gap"].mean()
    mean_nodes = data["Solving_Nodes"].mean()

    if show_output:
        print("RESULTS FOR: ", filename)
        print("Average solving time:", mean_time)
        print("Average gap:", mean_gap)
        print("Average number of nodes:", mean_nodes)
        print(data["SCIP_Status"].value_counts())
        if check:
            if (data["Check"] == "Fail").any():
                print("ERROR - At least one check failed")
            else:
                print("All checks passed")
        print("")

    return mean_time, mean_gap, mean_nodes

def _check_results(instancename, solver, results):
    """
    Check whether the solution found for a given instance matches the known
    optimal value.
    """
    path = os.path.join("instances", "knapPI_optimal.txt")

    if get_number_solutions(solver, results):
        optimal_found = int(get_optimal_found(solver, results))

        with open(path, 'r') as f:
            for line in f:
                inst, val = line.strip().split()
                if inst == instancename:
                    if int(val) == optimal_found:
                        return True
                    else:
                        return False

        return None

    else:
        return None

import os
import argparse
import pandas as pd

## Arguments parser

parser = argparse.ArgumentParser(prog='main.py')

# Instance
parser.add_argument('-n', type=int, default=100, help='number of items')
parser.add_argument('-t', type=int, default=11,
    choices = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16], help='instance type')
parser.add_argument('-r', type=int, default=1000, help='range of coefficients')
parser.add_argument('-s', type=int, default=100,
    help='number of instances in series')
parser.add_argument('-i', type=int, default=1, help='instance index')

# Solver
parser.add_argument('--timelimit', type=int,
    help='time limit for SCIP solving (seconds)')
parser.add_argument('-b', type=int, default=1, choices = [0,1,2,3],
    help='branching rule index')
parser.add_argument('--nv', type=int, default=1, help='size of branching set')
parser.add_argument('--parmode', action='store_true', help='Enable parallel mode (only if --solve-all)')

# Outputs
parser.add_argument('--no-output', action='store_true', help='Disable output')
parser.add_argument('--save-output', action='store_true',
    help='save output in a file')
parser.add_argument('--solve-all', action='store_true',
    help='solve all instances in series')
parser.add_argument('--check-output', action='store_true',
    help='Check whether the SCIP solution matches the known optimal one, if one exists')

## Misc

def print_results(instancename, model, check):
    """
    Print summary results from a SCIP model optimization to standard output.
    """
    instancename = os.path.splitext(instancename)[0]

    print("Instance          :", instancename)
    print("SCIP Status       :", model.getStatus())
    print("Solving Time (sec):", model.getSolvingTime())
    print("Gap               :", model.getGap())
    print("Solving Nodes     :", model.getNNodes())
    if model.getNSolsFound() > 0:
        print("Objective value   :", model.getObjVal())
        print("Solutions found   :", model.getNSolsFound())
    if check:
        c = _check_results(instancename, model)
        if model.getStatus() == "optimal":
            if c: print("Check             : Success")
            elif (c == False): print("Check             : Fail")
            else: print("Check             : None")
        else:
            print("Check             : None")
    print("")

def store_results(instancename, model, filename, check):
    """
    Append optimization results from a SCIP model to an output file.

    Creates the output directory if it does not exist. Writes a header line
    if the file is new. Each call appends a line with instance results.
    """
    os.makedirs("outputs", exist_ok=True)

    instancename = os.path.splitext(instancename)[0]
    filename = os.path.join("outputs", filename)

    header = (
        f"{'Instance':<26}"
        f"{'SCIP Status':<13}"
        f"{'Solving Time (sec)':<20}"
        f"{'Gap':<8}"
        f"{'Solving Nodes':<15}"
        f"{'Objective value':<17}"
        f"{'Solutions found':<15}"
    )

    if check:
        c = _check_results(instancename, model)
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
        gap = model.getGap()
        gap_str = f"{'1e+20':<8}" if gap == 1e20 else f"{gap:<8.4f}"

        f.write(
            f"{instancename:<26}"
            f"{model.getStatus():<13}"
            f"{model.getSolvingTime():<20.4f}"
            f"{gap_str}"
            f"{model.getNNodes():<15}"
        )

        if model.getNSolsFound() > 0:
            f.write(
                f"{model.getObjVal():<17.1f}"
                f"{model.getNSolsFound():<15}"
            )
        else:
            f.write(
                f"{'':<17}"
                f"{'':<15}"
            )

        if check:
            if model.getStatus() == "optimal":
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
        "SCIP_Status",
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

def _check_results(instancename, model):
    """
    TODO
    """
    instance = os.path.splitext(instancename)[0]
    path = os.path.join("instances", "knapPI_optimal.txt")

    if model.getNSolsFound() > 0:
        scip_optimal = int(model.getObjVal())

        with open(path, 'r') as f:
            for line in f:
                inst, val = line.strip().split()
                if inst == instance:
                    if int(val) == scip_optimal:
                        return True
                    else:
                        return False

        return None

    else:
        return None

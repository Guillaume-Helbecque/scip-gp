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
parser.add_argument('--timelimit', type=int, default=1e+20,
    help='time limit for SCIP solving (seconds)')
parser.add_argument('-b', type=int, default=1, choices = [0,1,2],
    help='branching rule index')
parser.add_argument('--nv', type=int, default=1, help='size of branching set')
parser.add_argument('--parmode', action='store_true', help='Enable parallel mode')

# Outputs
parser.add_argument('--no-output', action='store_true', help='Disable output')
parser.add_argument('--save-output', action='store_true',
    help='save output in a file')
parser.add_argument('--solve-all', action='store_true',
    help='solve all instances in series')

## Misc

def print_results(instancename, model):
    """
    Print summary results from a SCIP model optimization to standard output.
    """
    instancename = os.path.splitext(instancename)[0]

    print("Instance          :", instancename)
    print("SCIP Status       :", model.getStatus())
    print("Solving Time (sec):", model.getSolvingTime())
    print("Solving Nodes     :", model.getNNodes())
    if model.getNSolsFound() > 0:
        print("Objective value   :", model.getObjVal())
        print("Solutions found   :", model.getNSolsFound(),"\n")

def store_results(instancename, model, filename):
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
        f"{'Solving Nodes':<15}"
        f"{'Objective value':<17}"
        f"{'Solutions found':<15}\n"
    )

    # Write header if file does not exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(header)

    # Append a new data line
    with open(filename, "a") as f:
        f.write(
            f"{instancename:<26}"
            f"{model.getStatus():<13}"
            f"{model.getSolvingTime():<20.4f}"
            f"{model.getNNodes():<15}"
        )
        if model.getNSolsFound() > 0:
            f.write(
                f"{model.getObjVal():<17.1f}"
                f"{model.getNSolsFound():<15}"
            )
        f.write("\n")

def extract_results(filename):
    """
    Load and summarize results from an output file containing SCIP results.
    """
    data = pd.read_csv(
        os.path.join("outputs", filename),
        sep=r'\s+',
        skiprows=1,
        header=None,
        names=[
            "Instance",
            "SCIP_Status",
            "Solving_Time",
            "Solving_Nodes",
            "Objective value",
            "Solutions_found"
        ]
    )

    print("RESULTS FOR: ", filename)
    print("Average solving time:", data["Solving_Time"].mean())
    print("Average number of nodes:", data["Solving_Nodes"].mean())
    print(data["SCIP_Status"].value_counts())
    print("\n")

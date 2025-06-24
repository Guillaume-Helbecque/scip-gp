import os

def print_results(instancename, model):
    """
    Defines a custom output for SCIP solver.
    """
    instancename = os.path.splitext(instancename)[0]

    print("Instance          :", instancename)
    print("SCIP Status       :", model.getStatus())
    print("Solving Time (sec):", model.getSolvingTime())
    print("Solving Nodes     :", model.getNNodes())
    if model.getNSolsFound() > 0:
        print("Primal Bound      :", model.getObjVal())
        print("Solutions found   :", model.getNSolsFound(),"\n")

def store_results(instancename, model, filename):
    """
    Stores a custom output for SCIP solver in a file.
    """
    os.makedirs("/home/ghelbecq/Bureau/scip-rl/outputs/", exist_ok=True)
    os.chdir("/home/ghelbecq/Bureau/scip-rl/outputs/")

    instancename = os.path.splitext(instancename)[0]

    header = (
        f"{'Instance':<26}"
        f"{'SCIP Status':<13}"
        f"{'Solving Time (sec)':<20}"
        f"{'Solving Nodes':<15}"
        f"{'Primal Bound':<14}"
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
                f"{model.getObjVal():<14.1f}"
                f"{model.getNSolsFound():<15}"
            )
        f.write("\n")

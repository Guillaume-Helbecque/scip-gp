import os
import glob
import subprocess

def compile_generator():
    """
    Compile the C program 'genhard.c' into an executable 'genhard.out' inside the
    'instances' directory.

    The resulting executable is used to generate knapsack problem instances.
    """
    binary_path = os.path.join("instances", "genhard.out")

    if not os.path.exists(binary_path):
        subprocess.run(
            ["gcc", "genhard.c", "-lm", "-o", "genhard.out"],
            cwd="instances"
        )

def generate_instance(n, t, r, i, S=100):
    """
    Generate a knapsack problem instance file by invoking the compiled C generator.

    The function calls the 'genhard.out' executable with parameters corresponding to:
        - n: Number of items in the instance.
        - t: Instance type identifier.
        - r: Range of the coefficients.
        - i: Index of the instance within the series.
        - S: Total number of instances in the series (default is 100).

    The generator writes the instance to a file named according to the pattern
    "knapPI_<t>_<n>_<r>_<i>.txt" inside the 'instances' folder. The exact filename
    is returned by the generator's standard output.
    """
    result = subprocess.run(
        ["./genhard.out", str(n), str(r), str(t), str(i), str(S)],
        capture_output=True,
        text=True,
        cwd="instances"
    )
    return result.stdout.strip()

def clean_files():
    """
    Remove the compiled executable and all generated knapsack instance files.
    """
    binary_path = os.path.join("instances", "genhard.out")
    files_path = os.path.join("instances", "knapPI_*.txt")

    if os.path.exists(binary_path):
        os.remove(binary_path)

    for instance_file in glob.glob(files_path):
        os.remove(instance_file)

import os
import glob
import subprocess

def _compile_generator():
    """
    Compiles the C file 'genhard.c' using gcc to produce 'genhard.out',
    only if 'genhard.out' does not already exist.
    """
    binary_path = os.path.join("instances", "genhard.out")

    if not os.path.exists(binary_path):
        subprocess.run(
            ["gcc", "genhard.c", "-lm", "-o", "genhard.out"],
            cwd="instances"
        )

def generate_instance(n, t, r, i, S=100):
    """
    Generates a file named "knapPI_%t_%n_%r_%i.txt" containing the data of the
    knapsack instance. This function calls the C generator of Pisinger, that is
    assumed to be already compiled. The parameters are:
        - n: number of items
        - t: type of instance
        - r: range of data
        - i: index of instance
        - S: number of instances in the series
    The file name is returned.
    """
    _compile_generator()
    result = subprocess.run(
        ["./genhard.out", str(n), str(r), str(t), str(i), str(S)],
        capture_output=True,
        text=True,
        cwd="instances"
    )
    return result.stdout.strip()

def clean_files():
    """
    Clean the generated files (genhard.out and knapPI_*.txt).
    """
    binary_path = os.path.join("instances", "genhard.out")
    files_path = os.path.join("instances", "knapPI_*.txt")

    if os.path.exists(binary_path):
        os.remove(binary_path)

    for instance_file in glob.glob(files_path):
        os.remove(instance_file)

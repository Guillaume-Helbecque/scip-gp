import os
import subprocess

os.chdir("/home/ghelbecq/Bureau/scip-rl/instances/")

def compile_generator():
    """
    Compiles the C file 'genhard.c' using gcc to produce 'genhard.out'.
    """
    os.chdir("/home/ghelbecq/Bureau/scip-rl/instances/")
    subprocess.run(["gcc", "genhard.c", "-lm", "-o", "genhard.out"])

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
    """
    os.chdir("/home/ghelbecq/Bureau/scip-rl/instances/")
    subprocess.run(["./genhard.out", str(n), str(r), str(t), str(i), str(S)])

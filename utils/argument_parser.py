import argparse

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
parser.add_argument('--solver', type=str, default='scip', choices = ['scip'], help='B&B solver')
parser.add_argument('--timelimit', type=int,
    help='time limit for solver (seconds)')
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
    help='Check whether the best solution found matches the known optimal one, if one exists')

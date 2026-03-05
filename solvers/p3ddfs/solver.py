import multiprocessing as mp
import subprocess

from solvers.commons.postprocessing import print_results

def p3ddfs_solve_instance(inst, args, output_filename, individual = ""):
    """
    TODO
    """
    results = subprocess.run(
        [
            "./main_knapsack.out",
            "--mode", "sequential",
            "--ub", "dantzig_mvar",
            "--lb", "inf",
            "--mvar", str(args.nv),
            "--ind", individual,
            "--n", str(inst.n),
            "--r", str(inst.r),
            "--t", str(inst.t),
            "--id", str(inst.i)
        ],
        capture_output=True,
        text=True,
        cwd="solvers/p3ddfs/"
    )

    instancename = inst.get_name()

    if not args.no_output:
        print_results('p3ddfs', instancename, results.stdout, args.check_output)

def p3ddfs_solve_all_instances(insts, args, output_filename, individual = ""):
    """
    TODO
    """
    if args.parmode:
        args_list = [(inst, args, output_filename) for inst in insts]
        with mp.Pool(processes=mp.cpu_count()) as pool:
            pool.starmap(p3ddfs_solve_instance, args_list)
    else:
        for inst in insts:
            p3ddfs_solve_instance(inst, args, output_filename, individual)

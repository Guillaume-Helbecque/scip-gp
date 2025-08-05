# NOTE: The following three lines are necessary to specify that scip-rl is the
# root directory from which modules are searched. This is only needed when
# executing gp_engine.py as a main file.
# TODO: Can I avoid this somehow?
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evaluate_individual import evaluate
from gp_parameters import primitives
import numpy

from deap import base, creator, gp, tools, algorithms

def run_gp(initial_pop=50, mate=0.9, mutate=0.1, nb_gen=20):
    """
    TODO
    """
    # Create fitness and individual
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

    pset = gp.PrimitiveSet("main", arity=4) # TODO: arity to determine

    for p in primitives.values():
        pset.addPrimitive(p[0], p[1])

    pset.renameArguments(ARG0="x")
    pset.renameArguments(ARG1="y")
    pset.renameArguments(ARG2="z")
    pset.renameArguments(ARG3="t")

    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Create evolutionary tools
    toolbox.register("evaluate", evaluate, pset=pset)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("mutate", gp.mutNodeReplacement, pset=pset)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Compile statistics
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # Launch evolutionary algorithm
    pop_init = toolbox.population(n=initial_pop)
    pop, logbook = algorithms.eaSimple(pop_init, toolbox, cxpb=mate, mutpb=mutate,
        ngen=nb_gen, stats=stats)

    return pop, logbook

if __name__ == "__main__":
    run_gp()

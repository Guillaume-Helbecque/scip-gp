import operator
import numpy

from deap import base, creator, gp, tools, algorithms

# create fitness (-1.0 means minimization)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# create individual (as arithmetic expression)
pset = gp.PrimitiveSet("main", arity=4)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
# TODO: add division, but which one?
pset.addPrimitive(operator.lt, 2)
pset.addPrimitive(operator.gt, 2)
pset.addPrimitive(operator.eq, 2)

# rename arguments
pset.renameArguments(ARG0="x")
pset.renameArguments(ARG1="y")
pset.renameArguments(ARG2="z")
pset.renameArguments(ARG3="t")

creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

toolbox = base.Toolbox()
# create individual
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
# create population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    # this function should evaluate individual using SCIP solver
    return 1.0,

# create mutation, crossover, evaluation, and selection operators
toolbox.register("evaluate", evaluate)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("mutate", gp.mutNodeReplacement, pset=pset)
toolbox.register("select", tools.selTournament, tournsize=3)

# compile statistics
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

# launch evolutionary algorithm
pop_init = toolbox.population(n=100)

pop, logbook = algorithms.eaSimple(pop_init, toolbox, cxpb=0.9, mutpb=0.1, ngen=20, stats=stats)

from deap import gp

# Dummy evaluation for testing
def evaluate(individual, pset):
    function = gp.compile(individual, pset)
    # TODO: this function should evaluate individual using SCIP solver
    return function(0,1,2,3),

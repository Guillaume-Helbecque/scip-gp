import operator
import numpy
import re

from deap import base, creator, gp, tools, algorithms

operations = {
    'add': operator.add,
    'mul': operator.mul,
    'sub': operator.sub,
    # 'protectedDiv': protectedDiv,
    'lt': operator.lt,
    'gt': operator.gt,
    'eq': operator.eq
}

def run_gp(initial_pop=50, mate=0.9, mutate=0.1, nb_gen=20):
    # Create fitness and individual
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

    pset = gp.PrimitiveSet("main", arity=4) # TODO: arity to determine
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    # TODO: add division, but which one?
    pset.addPrimitive(operator.lt, 2)
    pset.addPrimitive(operator.gt, 2)
    pset.addPrimitive(operator.eq, 2)

    pset.renameArguments(ARG0="x")
    pset.renameArguments(ARG1="y")
    pset.renameArguments(ARG2="z")
    pset.renameArguments(ARG3="t")

    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Dummy evaluation for testing
    def evaluate(individual):
        print(str(individual))
        print("x=0, y=1, z=2, t=3")
        print(comp_policy_as_a_function(str(individual),0,1,2,3))
        print()
        # TODO: this function should evaluate individual using SCIP solver
        return 1.0,

    # Create evolutionary tools
    toolbox.register("evaluate", evaluate)
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

def comp_policy_as_a_function(comp_policy, x, y, z, t):
    delimiters = ["(", ",", " ", ")"]
    #string = self.comp_policy
    context = {
            'x': x,
            'y': y,
            'z': z,
            't': t,
        }
    return evaluate_expression(comp_policy, context)

def parse_args(args, context):
    # Split arguments considering nested functions
    args_list = []
    nested = 0
    last_split = 0
    for i, char in enumerate(args):
        if char == '(':
            nested += 1
        elif char == ')':
            nested -= 1
        elif char == ',' and nested == 0:
            args_list.append(args[last_split:i].strip())
            last_split = i + 1
    args_list.append(args[last_split:].strip())
    return [evaluate_expression(arg, context) for arg in args_list]

def evaluate_expression(expr, context):
    expr = expr.strip()
    # Regex to match outermost function calls
    func_pattern = r'^(\w+)\((.*)\)$'
    match = re.match(func_pattern, expr)
    if match:
        func_name, args_str = match.groups()
        if func_name in operations:
            args = parse_args(args_str, context)
            return operations[func_name](*args)
        else:
            raise ValueError(f"Unsupported function '{func_name}'")
    else:
        try:
            return float(expr)
        except ValueError:
            return context[expr]

if __name__ == "__main__":
    run_gp()

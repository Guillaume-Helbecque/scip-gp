from gp_parameters import primitives
import re

# Dummy evaluation for testing
def evaluate(individual):
    print(str(individual))
    print("x=0, y=1, z=2, t=3")
    print(comp_policy_as_a_function(str(individual),0,1,2,3))
    print()
    # TODO: this function should evaluate individual using SCIP solver
    return 1.0,

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
        if func_name in primitives:
            args = parse_args(args_str, context)
            return primitives[func_name](*args)
        else:
            raise ValueError(f"Unsupported function '{func_name}'")
    else:
        try:
            return float(expr)
        except ValueError:
            return context[expr]

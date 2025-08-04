import operator

def protecteddiv(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 1

def if_then_else(input, output1, output2):
    return output1 if input else output2

# TODO: add if_then_else to primitives. How to specify arity in dict?
primitives = {
    'add': operator.add,
    'sub': operator.sub,
    'mul': operator.mul,
    # 'truediv': operator.truediv,
    # 'floordiv': operator.floordiv,
    'protecteddiv': protecteddiv,
    # 'pow': operator.pow,
    # 'mod': operator.mod,
    # 'neg': operator.neg,
    # 'pos': operator.pos,
    # 'lt': operator.lt,
    # 'le': operator.le,
    # 'eq': operator.eq,
    # 'ne': operator.ne,
    # 'ge': operator.ge,
    # 'gt': operator.gt
}

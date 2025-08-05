import operator

def protecteddiv(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 1

def if_then_else(input, output1, output2):
    return output1 if input else output2

primitives = {
    'add': (operator.add, 2),
    'sub': (operator.sub, 2),
    'mul': (operator.mul, 2),
    # 'truediv': (operator.truediv, 2),
    # 'floordiv': (operator.floordiv, 2),
    'protecteddiv': (protecteddiv, 2),
    # 'pow': (operator.pow, 2),
    # 'mod': (operator.mod, 2),
    # 'neg': (operator.neg, 2),
    # 'pos': (operator.pos, 2),
    # 'lt': (operator.lt, 2),
    # 'le': (operator.le, 2),
    # 'eq': (operator.eq, 2),
    # 'ne': (operator.ne, 2),
    # 'ge': (operator.ge, 2),
    # 'gt': (operator.gt, 2),
    # 'if_then_else', (if_then_else, 3)
}

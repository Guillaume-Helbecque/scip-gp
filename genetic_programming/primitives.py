import operator

def protecteddiv(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 1

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

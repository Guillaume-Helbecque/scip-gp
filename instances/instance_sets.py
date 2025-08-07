from instances.generate_instances import instance
from itertools import product
import random

# TODO: add seed and randomly select a subset of instances
def determine_training_set():
    """
    Generates a full set of training instances and returns a list of tuples, where
    each tuple represents an instance defined by:
    (size, correlation, range of data, instance_id)
    """
    n = [50]
    t = [11]
    r = [1000]
    i = list(range(1, 101))

    training_instances_params = list(product(n, t, r, i))
    training_instances = [instance(*params) for params in training_instances_params]

    return training_instances

def determine_test_set():
    """
    Generates a full set of test instances and returns a list of tuples, where
    each tuple represents an instance defined by:
    (size, correlation, range of data, instance_id)
    """
    n = [100]
    t = [11]
    r = [1000]
    i = list(range(1, 101))

    test_instances_params = list(product(n, t, r, i))
    test_instances = [instance(*params) for params in test_instances_params]

    return test_instances

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
    corr = [11]
    range = [1000]
    instance_ids = list(range(1, 101))

    training_instances = list(product(n, corr, range, instance_ids))

    return training_instances

def determine_test_set():
    """
    Generates a full set of test instances and returns a list of tuples, where
    each tuple represents an instance defined by:
    (size, correlation, range of data, instance_id)
    """
    n = [100]
    corr = [11]
    range = [1000]
    instance_ids = list(range(1, 101))

    test_instances = list(product(n, corr, range, instance_ids))

    return test_instances

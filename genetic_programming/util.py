import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pickle
import math

def save_logbook(logbook, filename="logbook.txt"):
    """
    Save a DEAP logbook to a text file using pickle serialization.
    """
    with open(filename, "wb") as f:
        pickle.dump(logbook, f)

def load_logbook(filename="logbook.txt"):
    """
    Load a DEAP logbook from a text file.
    """
    with open(filename, "rb") as f:
        logbook = pickle.load(f)

    return logbook

def print_gp_convergence(logbook):
    """
    Plot the convergence curve of a genetic programming algorithm, showing the
    minimum fitness per generation.
    """
    gens = logbook.select("gen")
    fit_mins = logbook.select("min")

    fig, ax1 = plt.subplots()
    ax1.plot(gens, fit_mins, "b-", label="Minimum Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness")
    ax1.legend()

    # Bound axes
    y_max = math.ceil(max(fit_mins) * 10) / 10
    if y_max == 0: y_max = 0.1
    ax1.set_ylim(0, y_max)
    ax1.set_xlim(0, gens[-1])

    # Set x-axis to only show integer ticks
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.show()

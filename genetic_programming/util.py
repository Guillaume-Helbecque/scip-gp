import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

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

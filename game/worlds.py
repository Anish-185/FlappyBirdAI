import numpy as np
from game import engine as E
from ga import evolve as G

WORLDS = {"standard": (200.0, 400.0), "hard": (150.0, 450.0)}

def table(world, n=G.N_SEEDS):
    lo, hi = WORLDS[world]
    t = np.empty((n, E.N_PIPES))
    for s in range(n):
        t[s] = np.random.default_rng(s).uniform(lo, hi, E.N_PIPES)
    return t

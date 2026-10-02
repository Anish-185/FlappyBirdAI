"""Headless Flappy-Bird simulator, compiled with numba.

The GA never touches this file's internals: it only calls `eval_batch`,
which maps (genomes, world seeds) -> per-episode statistics.
"""
import math
import numpy as np
from numba import njit

# ---- physics / geometry (frozen for every experiment) -----------------------
GRAVITY, FLAP_V, MAX_V = 0.45, -7.5, 11.0
GAP, SPACING, SPEED = 130.0, 200.0, 3.0
H, BIRD_X, HALF, PIPE_W = 600.0, 80.0, 12.0, 52.0
FIRST_X, START_Y = 300.0, 300.0
GAP_LO, GAP_HI = 150.0, 450.0          # range of gap centres
N_PIPES = 300                           # pipes precomputed per seed
GENOME_SIZE = 43                        # 5-6-1 MLP
TRUNC, GROUND, CEIL, PIPE = 0, 1, 2, 3  # death causes
# result columns
R_FRAMES, R_PIPES, R_DEATH, R_FLAPS, R_PROX = 0, 1, 2, 3, 4


def make_table(n_seeds):
    """gap-centre table; row s is the (deterministic) world for seed s."""
    t = np.empty((n_seeds, N_PIPES))
    for s in range(n_seeds):
        t[s] = np.random.default_rng(s).uniform(GAP_LO, GAP_HI, N_PIPES)
    return t


@njit(cache=True)
def _episode(g, gaps, max_frames, mode, rec, ty, res):
    y = START_Y
    v = 0.0
    nxt = 0
    pipes = 0
    flaps = 0
    prox = 0.0
    sampled = -1
    death = TRUNC
    frames = max_frames
    hg = GAP / 2.0
    for t in range(max_frames):
        px = FIRST_X + SPACING * nxt - SPEED * t
        while px + PIPE_W < BIRD_X - HALF:          # pipe fully behind the bird
            nxt += 1
            pipes += 1
            px = FIRST_X + SPACING * nxt - SPEED * t
        c = gaps[nxt]
        if mode == 0:                               # 5-6-1 MLP, tanh hidden
            o0 = (y - 300.0) / 300.0
            o1 = v / MAX_V
            o2 = (px - BIRD_X) / SPACING
            o3 = (c - hg - y) / 300.0
            o4 = (c + hg - y) / 300.0
            z = g[42]
            for j in range(6):
                s = (g[30 + j] + o0 * g[j] + o1 * g[6 + j] + o2 * g[12 + j]
                     + o3 * g[18 + j] + o4 * g[24 + j])
                z += math.tanh(s) * g[36 + j]
            flap = z > 0.0                          # == sigmoid(z) > 0.5
        else:                                       # 2-gene threshold rule
            flap = (y - c) / 50.0 + g[1] * v / 5.0 > g[0]
        if flap:
            v = FLAP_V
            flaps += 1
        v = min(v + GRAVITY, MAX_V)
        y += v
        if rec:
            ty[t] = y
        px1 = FIRST_X + SPACING * nxt - SPEED * (t + 1)
        if sampled != nxt and px1 <= BIRD_X + HALF:  # pipe face reaches bird
            err = abs(y - c)
            prox += max(0.0, 1.0 - err / hg)
            sampled = nxt
        if y - HALF < 0.0:
            death = CEIL
            frames = t + 1
            break
        if y + HALF > H:
            death = GROUND
            frames = t + 1
            break
        if px1 < BIRD_X + HALF and px1 + PIPE_W > BIRD_X - HALF:
            if y - HALF < c - hg or y + HALF > c + hg:
                death = PIPE
                frames = t + 1
                break
    res[0] = frames
    res[1] = pipes
    res[2] = death
    res[3] = flaps
    res[4] = prox


@njit(cache=True)
def eval_batch(pop, seeds, table, max_frames, mode):
    """-> array (N, K, 5): frames, pipes, death, flaps, proximity."""
    N = pop.shape[0]
    K = seeds.shape[0]
    out = np.empty((N, K, 5))
    dummy = np.empty(1)
    res = np.empty(5)
    for i in range(N):
        for k in range(K):
            _episode(pop[i], table[seeds[k]], max_frames, mode, False, dummy, res)
            for m in range(5):
                out[i, k, m] = res[m]
    return out


def trace(genome, seed, table, max_frames, mode=0):
    """Return (y[t], result) for plotting one episode."""
    ty = np.zeros(max_frames)
    res = np.empty(5)
    _episode(genome, table[seed], max_frames, mode, True, ty, res)
    return ty[: int(res[0])], res

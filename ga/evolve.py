"""Generational genetic algorithm with interchangeable operators.

Everything here is game-agnostic except `fitness_from_stats`, which turns the
simulator's per-episode statistics into a scalar.
"""
import time
from dataclasses import dataclass, field, asdict
import numpy as np
from game import engine as E

LO, HI = -3.0, 3.0


@dataclass
class Config:
    # population / budget
    pop: int = 50
    gens: int = 100
    elite: int = 2
    # operators
    selection: str = "tournament"      # roulette | tournament | rank
    k: int = 3                         # tournament size
    crossover: str = "uniform"         # none | single | uniform | arithmetic
    p_cross: float = 0.85
    mutation: str = "gaussian"         # gaussian | reset | annealed
    m_rate: float = 0.10
    m_sigma: float = 0.30
    s0: float = 0.60                   # annealed sigma: s0 -> s1
    s1: float = 0.05
    # diversity maintenance
    immigrants: float = 0.0            # fraction of population replaced by random genomes
    sharing: float = 0.0               # fitness-sharing radius (0 = off)
    # evaluation
    fitness: int = 2                   # 0 frames | 1 pipes+frames | 2 shaped
    aggregate: str = "min"             # min | mean
    K: int = 3                         # seeds per individual per generation
    train_pool: int = 10               # seeds 0..pool-1 (resampled each generation)
    max_frames: int = 10000
    mode: int = 0                      # 0 = MLP, 1 = 2-gene rule
    # weights of the shaped fitness
    w_pipes: float = 1000.0
    w_frames: float = 1.0
    w_prox: float = 50.0
    ceil_pen: float = 300.0


VAL_SEEDS = np.arange(1000, 1006)      # never used for selection
TEST_SEEDS = np.arange(2000, 2030)     # only used once, on the final champion
TRAIN_OFFSET = 5000                    # training seeds live at 5000.. so pool size can vary freely
N_SEEDS = 5000 + 1000 + 10


def fitness_from_stats(out, cfg):
    """out: (N,K,5) -> fitness (N,)."""
    frames, pipes = out[:, :, 0], out[:, :, 1]
    death, prox = out[:, :, 2], out[:, :, 4]
    if cfg.fitness == 0:
        f = frames
    elif cfg.fitness == 1:
        f = cfg.w_pipes * pipes + cfg.w_frames * frames
    else:
        f = (cfg.w_pipes * pipes + cfg.w_frames * frames + cfg.w_prox * prox
             - cfg.ceil_pen * (death == E.CEIL))
    return f.min(axis=1) if cfg.aggregate == "min" else f.mean(axis=1)


# ------------------------------------------------------------------ operators
def select(pop, fit, rng, cfg, n):
    N = len(pop)
    if cfg.selection == "tournament":
        idx = rng.integers(0, N, (n, cfg.k))
        return idx[np.arange(n), np.argmax(fit[idx], axis=1)]
    if cfg.selection == "roulette":
        f = fit - fit.min() + 1e-9
        return rng.choice(N, size=n, p=f / f.sum())
    if cfg.selection == "rank":
        sp = 1.7
        r = np.empty(N)
        r[np.argsort(fit)] = np.arange(N)            # 0 = worst
        p = (2 - sp + 2 * (sp - 1) * r / (N - 1)) / N
        return rng.choice(N, size=n, p=p / p.sum())
    raise ValueError(cfg.selection)


def cross(a, b, rng, cfg):
    M, L = a.shape
    if cfg.crossover == "none":
        child = a.copy()
    elif cfg.crossover == "single":
        c = rng.integers(1, L, (M, 1))
        child = np.where(np.arange(L)[None, :] < c, a, b)
    elif cfg.crossover == "uniform":
        child = np.where(rng.random((M, L)) < 0.5, a, b)
    elif cfg.crossover == "arithmetic":
        al = rng.random((M, 1))
        child = al * a + (1 - al) * b
    else:
        raise ValueError(cfg.crossover)
    skip = rng.random(M) >= cfg.p_cross               # no crossover -> copy parent a
    child[skip] = a[skip]
    return child


def mutate(x, rng, cfg, gen):
    mask = rng.random(x.shape) < cfg.m_rate
    if cfg.mutation == "reset":
        noise = rng.uniform(LO, HI, x.shape)
        out = np.where(mask, noise, x)
    else:
        sigma = cfg.m_sigma
        if cfg.mutation == "annealed":
            sigma = cfg.s0 * (cfg.s1 / cfg.s0) ** (gen / max(cfg.gens - 1, 1))
        out = x + mask * rng.normal(0.0, sigma, x.shape)
    return np.clip(out, LO, HI)


def diversity(pop):
    """mean pairwise Euclidean distance between genomes."""
    sq = (pop ** 2).sum(1)
    d2 = sq[:, None] + sq[None, :] - 2 * pop @ pop.T
    n = len(pop)
    return float(np.sqrt(np.maximum(d2, 0)).sum() / (n * (n - 1)))


def shared(pop, fit, radius):
    sq = (pop ** 2).sum(1)
    d = np.sqrt(np.maximum(sq[:, None] + sq[None, :] - 2 * pop @ pop.T, 0))
    sh = np.where(d < radius, 1 - d / radius, 0.0)
    f = fit - fit.min() + 1.0
    return f / sh.sum(1)


# ------------------------------------------------------------------ main loop
def run(cfg, seed, table, n_records=50):
    """One independent GA run.  Returns (per-generation records, champion, test dict)."""
    rng = np.random.default_rng(10_000 + seed)
    L = E.GENOME_SIZE if cfg.mode == 0 else 2
    pop = rng.uniform(-1, 1, (cfg.pop, L))
    train = TRAIN_OFFSET + np.arange(cfg.train_pool)
    K = min(cfg.K, cfg.train_pool)
    recs, evals = [], 0
    every = max(1, cfg.gens // n_records)
    for gen in range(cfg.gens):
        seeds = rng.choice(train, size=K, replace=False)
        out = E.eval_batch(pop, seeds, table, cfg.max_frames, cfg.mode)
        fit = fitness_from_stats(out, cfg)
        evals += cfg.pop * K
        order = np.argsort(-fit)
        best = pop[order[0]]
        if gen % every == 0 or gen == cfg.gens - 1:
          v = E.eval_batch(best[None, :], VAL_SEEDS, table, cfg.max_frames, cfg.mode)[0]
          recs.append(dict(
            gen=gen, evals=evals, best=fit[order[0]], mean=fit.mean(), worst=fit.min(),
            div=diversity(pop),
            val_pipes=v[:, 1].mean(), val_surv=(v[:, 2] == E.TRUNC).mean(),
            frac_ceil=float((out[:, :, 2] == E.CEIL).any(1).mean()),
            best_flap_rate=float(v[:, 3].sum() / v[:, 0].sum()),
          ))
        if gen == cfg.gens - 1:
            break
        # ---- next generation
        sel_fit = shared(pop, fit, cfg.sharing) if cfg.sharing > 0 else fit
        n_new = cfg.pop - cfg.elite
        a = pop[select(pop, sel_fit, rng, cfg, n_new)]
        b = pop[select(pop, sel_fit, rng, cfg, n_new)]
        kids = mutate(cross(a, b, rng, cfg), rng, cfg, gen)
        n_imm = int(round(cfg.immigrants * cfg.pop))
        if n_imm > 0:
            kids[-n_imm:] = rng.uniform(-1, 1, (n_imm, L))
        pop = np.vstack([pop[order[: cfg.elite]].copy(), kids])
    champ = best                                      # best of the final generation
    t = E.eval_batch(champ[None, :], TEST_SEEDS, table, cfg.max_frames, cfg.mode)[0]
    test = dict(test_pipes=t[:, 1].mean(), test_surv=(t[:, 2] == E.TRUNC).mean(),
                test_all=float((t[:, 2] == E.TRUNC).all()))
    return recs, champ, test

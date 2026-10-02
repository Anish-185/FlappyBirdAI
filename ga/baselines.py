"""Non-GA search baselines evaluated under exactly the same protocol/budget."""
import numpy as np
from game import engine as E
from ga import evolve as G


def _rec(gen, evals, fit, pop_like, best, cfg, table):
    v = E.eval_batch(best[None, :], G.VAL_SEEDS, table, cfg.max_frames, cfg.mode)[0]
    return dict(gen=gen, evals=evals, best=float(fit.max()), mean=float(fit.mean()),
                worst=float(fit.min()), div=float("nan"),
                val_pipes=v[:, 1].mean(), val_surv=(v[:, 2] == E.TRUNC).mean(),
                frac_ceil=float("nan"), best_flap_rate=float(v[:, 3].sum() / v[:, 0].sum()))


def _test(champ, cfg, table):
    t = E.eval_batch(champ[None, :], G.TEST_SEEDS, table, cfg.max_frames, cfg.mode)[0]
    return dict(test_pipes=t[:, 1].mean(), test_surv=(t[:, 2] == E.TRUNC).mean(),
                test_all=float((t[:, 2] == E.TRUNC).all()))


def run_random(cfg, seed, table):
    """Random search: sample `pop` fresh genomes per 'generation'; champion = best
    fitness ever observed (each genome scored on its generation's K seeds)."""
    rng = np.random.default_rng(10_000 + seed)
    L = E.GENOME_SIZE
    train = G.TRAIN_OFFSET + np.arange(cfg.train_pool)
    best, best_f, recs, evals = None, -np.inf, [], 0
    for gen in range(cfg.gens):
        pop = rng.uniform(-1, 1, (cfg.pop, L))
        seeds = rng.choice(train, size=cfg.K, replace=False)
        fit = G.fitness_from_stats(E.eval_batch(pop, seeds, table, cfg.max_frames, 0), cfg)
        evals += cfg.pop * cfg.K
        i = int(np.argmax(fit))
        if fit[i] > best_f:
            best, best_f = pop[i].copy(), fit[i]
        recs.append(_rec(gen, evals, fit, pop, best, cfg, table))
    return recs, best, _test(best, cfg, table)


def run_hillclimb(cfg, seed, table):
    """(1+1)-ES: mutate, compare parent and child on the SAME fresh K seeds, keep the
    child if it is at least as good.  Budget-matched to the GA (2K episodes/step)."""
    rng = np.random.default_rng(10_000 + seed)
    L = E.GENOME_SIZE
    train = G.TRAIN_OFFSET + np.arange(cfg.train_pool)
    x = rng.uniform(-1, 1, L)
    steps = cfg.pop * cfg.gens // 2                # (pop*K*gens) / (2K)
    log_every = cfg.pop // 2                       # one record per GA-generation of budget
    recs, evals = [], 0
    for it in range(steps):
        y = G.mutate(x[None, :], rng, cfg, 0)[0]
        seeds = rng.choice(train, size=cfg.K, replace=False)
        fit = G.fitness_from_stats(E.eval_batch(np.stack([x, y]), seeds, table, cfg.max_frames, 0), cfg)
        evals += 2 * cfg.K
        if fit[1] >= fit[0]:
            x = y
        if (it + 1) % log_every == 0:
            recs.append(_rec(len(recs), evals, fit, None, x, cfg, table))
    return recs, x, _test(x, cfg, table)

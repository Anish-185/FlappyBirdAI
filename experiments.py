"""Runs every experiment in the paper.  Results -> logs/<cond>.pkl (resumable)."""
import os, sys, time, pickle, itertools
import numpy as np
from game import worlds
from ga import evolve as G, baselines as B

SEEDS = list(range(100, 112))          # 12 reported runs (pilot runs used 0-5, 900-905)
BUDGET = 15000                          # baseline evaluation budget: 50 * 3 * 100


def gens_for(pop, K):
    return BUDGET // (pop * K)


C = {}                                   # name -> (world, kwargs, seeds, kind)
def add(name, world="hard", seeds=SEEDS, kind="ga", **kw):
    C[name] = (world, kw, seeds, kind)

# ===== primary testbed: the "hard" world (gap centres ~ U(150,450)) ==========
add("base")
# --- Study A: selection
add("sel_roulette", selection="roulette")
add("sel_tour2", k=2)
add("sel_tour5", k=5)
add("sel_rank", selection="rank")
# --- Study B: crossover
add("cx_none", crossover="none")
add("cx_single", crossover="single")
add("cx_arith", crossover="arithmetic")
# --- reference searchers at equal evaluation budget
add("rs", kind="random")
add("hc", kind="hill")
add("rule_ga", mode=1)
# --- Study E: fitness design, noise handling, generalisation
add("fit_frames", fitness=0)
add("fit_pipes", fitness=1)
add("agg_mean", aggregate="mean")
add("K1", K=1, gens=gens_for(50, 1))
add("K5", K=5, gens=gens_for(50, 5))
add("pool_1", train_pool=1, gens=gens_for(50, 1))   # K collapses to 1 -> 300 gens
for pool in (3, 100):
    add(f"pool_{pool}", train_pool=pool)
# --- Study D: population size (equal budget) and elitism
for pop in (20, 100, 200):
    add(f"pop_{pop}", pop=pop, gens=gens_for(pop, 3))
for e in (0, 1, 5, 10):
    add(f"elite_{e}", elite=e)
# --- Study F: diversity
IND = dict(selection="tournament", k=7, m_rate=0.01, m_sigma=0.1, elite=10, pop=30,
           gens=BUDGET // (30 * 3))
add("div_ctrl", **IND)
for r in (1.0, 2.0, 3.0, 4.0):
    add(f"div_share{r:.0f}", sharing=r, **IND)
add("div_imm10", immigrants=0.10, **IND)
add("div_imm20", immigrants=0.20, **IND)
# --- Study C: mutation (rate x sigma grid, n=6) + schedule + operator
add("mut_annealed", mutation="annealed")
add("mut_reset", mutation="reset", m_rate=0.05)
for r, s_ in itertools.product([0.02, 0.05, 0.10, 0.20, 0.40], [0.05, 0.15, 0.30, 0.60]):
    if (r, s_) != (0.10, 0.30):
        add(f"mut_r{r:.2f}_s{s_:.2f}", seeds=SEEDS[:6], m_rate=r, m_sigma=s_)
# ===== "standard" world (gap centres ~ U(200,400)): ceiling-effect check ========
add("std_base", world="standard")
add("std_rs", world="standard", kind="random")
add("std_hc", world="standard", kind="hill")
add("std_rule_ga", world="standard", mode=1)
add("std_sel_roulette", world="standard", selection="roulette")
add("std_cx_none", world="standard", crossover="none")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    tables = {w: worlds.table(w) for w in worlds.WORLDS}
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    budget_s = next((float(a.split("=")[1]) for a in sys.argv[1:] if a.startswith("--secs=")), 1e9)
    only = args or list(C)
    t0 = time.time()
    for i, name in enumerate(only):
        path = f"logs/{name}.pkl"
        if os.path.exists(path):
            continue
        world, kw, seeds, kind = C[name]
        cfg = G.Config(**kw)
        runs = []
        for s in seeds:
            fn = {"ga": G.run, "random": B.run_random, "hill": B.run_hillclimb}[kind]
            recs, champ, test = fn(cfg, s, tables[world])
            runs.append(dict(seed=s, recs=recs, champ=champ, test=test))
        pickle.dump(dict(name=name, world=world, cfg=cfg.__dict__, kind=kind, runs=runs), open(path, "wb"))
        done = len([p for p in os.listdir("logs") if p.endswith(".pkl")])
        with open("logs/progress.txt", "a") as f:
            f.write(f"{time.time()-t0:7.0f}s  [{done}/{len(C)}] {name}\n")
        if time.time() - t0 > budget_s:
            print("time budget reached"); break

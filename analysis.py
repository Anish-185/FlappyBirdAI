"""Load logs -> metrics, statistics (Mann-Whitney U + Cliff's delta + Holm), results.pkl"""
import glob, os, pickle, itertools
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

from game import engine as E, worlds
from ga import evolve as G

BUDGET = 15000
THRESH = 50                      # "competent" = validation mean >= 50 pipes


def load():
    runs, gens, conds = [], [], {}
    for f in sorted(glob.glob("logs/*.pkl")):
        d = pickle.load(open(f, "rb"))
        name = d["name"]
        conds[name] = dict(world=d["world"], cfg=d["cfg"], kind=d["kind"])
        for r in d["runs"]:
            df = pd.DataFrame(r["recs"])
            ev, v = df["evals"].to_numpy(), df["val_pipes"].to_numpy()
            grid = np.linspace(BUDGET / 100, BUDGET, 100)
            idx = np.searchsorted(ev, grid, side="right") - 1
            curve = np.where(idx >= 0, v[np.clip(idx, 0, None)], 0.0)
            hit = np.where(v >= THRESH)[0]
            runs.append(dict(
                cond=name, world=d["world"], seed=r["seed"], **r["test"],
                final_val=float(v[-1]), last10_val=float(v[-10:].mean()),
                auc=float(curve.mean()) if ev[-1] >= BUDGET * 0.99 else np.nan,
                e50=float(ev[hit[0]]) if len(hit) else np.nan,
                reach50=float(len(hit) > 0),
                final_div=float(df["div"].iloc[-1]),
                champ=r["champ"]))
            df["cond"], df["seed"] = name, r["seed"]
            gens.append(df)
    return pd.DataFrame(runs), pd.concat(gens, ignore_index=True), conds


def cliffs_delta(x, y):
    x, y = np.asarray(x), np.asarray(y)
    gt = (x[:, None] > y[None, :]).sum()
    lt = (x[:, None] < y[None, :]).sum()
    return (gt - lt) / (len(x) * len(y))


def holm(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    m = len(p)
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj


def summarize(runs, names, ref, metric="test_pipes", labels=None):
    """One row per condition; delta/p are versus `ref` (Holm-corrected within the table)."""
    rows = []
    r0 = runs[runs.cond == ref][metric].dropna().to_numpy()
    pv = []
    for n in names:
        x = runs[runs.cond == n][metric].dropna().to_numpy()
        if len(x) == 0:
            continue
        row = dict(cond=n, label=(labels or {}).get(n, n), n=len(x),
                   median=np.median(x), q1=np.percentile(x, 25), q3=np.percentile(x, 75),
                   mean=x.mean(), sd=x.std(ddof=1) if len(x) > 1 else 0.0,
                   surv=runs[runs.cond == n]["test_surv"].mean(),
                   robust=runs[runs.cond == n]["test_all"].mean(),
                   auc=runs[runs.cond == n]["auc"].mean(),
                   reach50=runs[runs.cond == n]["reach50"].mean(),
                   e50=runs[runs.cond == n]["e50"].median(),
                   div=runs[runs.cond == n]["final_div"].mean())
        if n != ref and len(x) > 1 and len(r0) > 1:
            u = mannwhitneyu(x, r0, alternative="two-sided")
            row["delta"], row["p"] = cliffs_delta(x, r0), u.pvalue
            pv.append(u.pvalue)
        else:
            row["delta"], row["p"] = np.nan, np.nan
        rows.append(row)
    df = pd.DataFrame(rows)
    mask = df["p"].notna()
    if mask.any():
        df.loc[mask, "p_holm"] = holm(df.loc[mask, "p"].to_numpy())
    else:
        df["p_holm"] = np.nan
    return df


def best_rule(world, tables):
    """Grid-search the best hand-tuned 2-gene rule on training seeds; report on test seeds."""
    tr = G.TRAIN_OFFSET + np.arange(20)
    best = (-1, None)
    for a in np.linspace(-1, 1.5, 26):
        for b in np.linspace(0, 3, 31):
            r = E.eval_batch(np.array([[a, b]]), tr, tables[world], 10000, 1)[0]
            if r[:, 1].mean() > best[0]:
                best = (r[:, 1].mean(), np.array([a, b]))
    t = E.eval_batch(best[1][None, :], G.TEST_SEEDS, tables[world], 10000, 1)[0]
    return dict(a=best[1][0], b=best[1][1], test_pipes=t[:, 1].mean(), test_surv=(t[:, 2] == 0).mean())


def train_performance(runs, tables, pools):
    """Champion performance on the *training* seeds it was selected on (for the overfitting study)."""
    out = {}
    for name, pool in pools.items():
        sub = runs[runs.cond == name]
        if sub.empty:
            continue
        w = sub.world.iloc[0]
        seeds = G.TRAIN_OFFSET + np.arange(pool)
        vals = []
        for g in sub["champ"]:
            r = E.eval_batch(g[None, :], seeds, tables[w], 10000, 0)[0]
            vals.append(r[:, 1].mean())
        out[name] = np.array(vals)
    return out


if __name__ == "__main__":
    tables = {w: worlds.table(w) for w in worlds.WORLDS}
    runs, gens, conds = load()
    print(len(runs), "runs from", runs.cond.nunique(), "conditions")
    res = dict(runs=runs.drop(columns=["champ"]), gens=gens, conds=conds)
    res["rule"] = {w: best_rule(w, tables) for w in worlds.WORLDS}
    print(res["rule"])
    P = {}
    def S(key, names, ref, **kw):
        names = [n for n in names if n in set(runs.cond)]
        if ref in names:
            P[key] = summarize(runs, names, ref, **kw)
    S("methods", ["base", "hc", "rs", "rule_ga"], "base")
    S("selection", ["sel_tour2", "base", "sel_tour5", "sel_roulette", "sel_rank"], "base")
    S("crossover", ["cx_none", "cx_single", "base", "cx_arith"], "base")
    S("mutation_named", ["base", "mut_annealed", "mut_reset"], "base")
    S("popsize", ["pop_20", "base", "pop_100", "pop_200"], "base")
    S("elitism", ["elite_0", "elite_1", "base", "elite_5", "elite_10"], "base")
    S("fitness", ["fit_frames", "fit_pipes", "base"], "base")
    S("evalproto", ["K1", "agg_mean", "base", "K5"], "base")
    S("pool", ["pool_1", "pool_3", "base", "pool_100"], "base")
    S("diversity", ["div_ctrl", "div_share1", "div_share2", "div_share3", "div_share4", "div_imm10", "div_imm20"], "div_ctrl")
    S("standard", ["std_base", "std_sel_roulette", "std_cx_none", "std_hc", "std_rs", "std_rule_ga"], "std_base")
    res["tables"] = P
    # mutation grid
    grid = {}
    for r in [0.02, 0.05, 0.10, 0.20, 0.40]:
        for s in [0.05, 0.15, 0.30, 0.60]:
            n = "base" if (r, s) == (0.10, 0.30) else f"mut_r{r:.2f}_s{s:.2f}"
            x = runs[runs.cond == n]["test_pipes"]
            if len(x):
                grid[(r, s)] = (x.median(), x.mean(), len(x))
    res["mut_grid"] = grid
    res["train_perf"] = train_performance(
        runs, tables, {"pool_1": 1, "pool_3": 3, "base": 10, "pool_100": 100})
    # counts for text
    res["tables_keys"] = list(P)
    pickle.dump(res, open("results.pkl", "wb"))
    for k, v in P.items():
        print("\n==", k)
        print(v[["label", "n", "median", "q1", "q3", "mean", "surv", "delta", "p", "p_holm", "auc", "e50", "reach50"]].round(3).to_string(index=False))

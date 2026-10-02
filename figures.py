"""All figures for the paper -> figures/*.png"""
import pickle, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

from game import engine as E, worlds
from ga import evolve as G
import analysis as A

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Liberation Serif", "DejaVu Serif"],
    "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8, "legend.fontsize": 7,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.spines.top": False,
    "axes.spines.right": False, "axes.linewidth": 0.7, "lines.linewidth": 1.3,
    "savefig.dpi": 300, "figure.dpi": 100, "mathtext.fontset": "stix",
})
OI = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#7a7a7a", "#000000"]
OUT = "figures"
os.makedirs(OUT, exist_ok=True)
CAP = 149


def panel(ax, s):
    ax.text(-0.02, 1.06, s, transform=ax.transAxes, fontsize=9, fontweight="bold", va="bottom", ha="right")


def have(gens, *names):
    s = set(gens.cond.unique())
    return all(n in s for n in names)


def curve(ax, gens, cond, x="gen", y="val_pipes", color="k", label=None, band=True, lw=1.4):
    d = gens[gens.cond == cond]
    piv = d.pivot(index=x if x == "gen" else "gen", columns="seed", values=y)
    xs = d[d.seed == d.seed.iloc[0]].sort_values("gen")[x].to_numpy()
    med = piv.median(axis=1).to_numpy()
    if band:
        ax.fill_between(xs, piv.quantile(0.25, axis=1), piv.quantile(0.75, axis=1),
                        color=color, alpha=0.16, lw=0)
    ax.plot(xs, med, color=color, lw=lw, label=label)


def boxstrip(ax, runs, names, labels, colors=None, metric="test_pipes", ylim=(0, 155), rot=0, cap=True):
    data = [runs[runs.cond == n][metric].to_numpy() for n in names]
    colors = colors or [OI[i % len(OI)] for i in range(len(names))]
    bp = ax.boxplot(data, positions=range(len(names)), widths=0.55, showfliers=False,
                    patch_artist=True, medianprops=dict(color="k", lw=1.2),
                    whiskerprops=dict(lw=0.7), capprops=dict(lw=0.7), boxprops=dict(lw=0.7))
    rng = np.random.default_rng(0)
    for i, (d, c, b) in enumerate(zip(data, colors, bp["boxes"])):
        b.set_facecolor(c); b.set_alpha(0.28)
        ax.scatter(i + rng.uniform(-0.17, 0.17, len(d)), d, s=6, color=c, alpha=0.85, lw=0, zorder=3)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(labels, rotation=rot, ha="right" if rot else "center")
    if ylim:
        ax.set_ylim(*ylim)
    if cap and metric == "test_pipes":
        ax.axhline(CAP, color="0.5", lw=0.6, ls=":")
    ax.set_ylabel("champion test pipes" if metric == "test_pipes" else metric)


# ------------------------------------------------------------------ Fig 1
def fig_setup():
    fig = plt.figure(figsize=(6.5, 2.7))
    ax = fig.add_axes([0.02, 0.06, 0.52, 0.86])
    ax.set_xlim(0, 620); ax.set_ylim(600, -20); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 620, 600, fill=False, lw=0.8, ec="0.4"))
    for px, c in [(300, 300), (500, 430)]:
        ax.add_patch(Rectangle((px, 0), 52, c - 65, fc="0.72", ec="0.35", lw=0.8))
        ax.add_patch(Rectangle((px, c + 65), 52, 600 - c - 65, fc="0.72", ec="0.35", lw=0.8))
    by = 300
    ax.add_patch(Rectangle((80 - 12, by - 12), 24, 24, fc=OI[4], ec="k", lw=0.8))
    # horizontal distance to the next pipe
    ax.annotate("", xy=(298, by), xytext=(94, by), arrowprops=dict(arrowstyle="<->", lw=0.8, color=OI[0]))
    ax.text(196, by - 10, r"$dx$", color=OI[0], ha="center", fontsize=8)
    # signed offsets to the gap edges, drawn inside the gap so nothing crosses
    xg = 326
    ax.annotate("", xy=(xg, 235), xytext=(xg, by), arrowprops=dict(arrowstyle="<->", lw=0.8, color=OI[1]))
    ax.text(xg + 6, 262, r"$\Delta_{top}$", color=OI[1], ha="left", va="center", fontsize=8)
    ax.annotate("", xy=(xg, 365), xytext=(xg, by), arrowprops=dict(arrowstyle="<->", lw=0.8, color=OI[2]))
    ax.text(xg + 6, 338, r"$\Delta_{bot}$", color=OI[2], ha="left", va="center", fontsize=8)
    ax.plot([300, 352], [235, 235], color="0.35", lw=0.5, ls=":")
    ax.plot([300, 352], [365, 365], color="0.35", lw=0.5, ls=":")
    # velocity and altitude
    ax.annotate("", xy=(80, 352), xytext=(80, 322), arrowprops=dict(arrowstyle="->", lw=1.0, color="k"))
    ax.text(90, 344, r"$v$", fontsize=8, va="center")
    ax.annotate("", xy=(44, by), xytext=(44, 0), arrowprops=dict(arrowstyle="->", lw=0.7, color="0.45"))
    ax.text(36, 150, r"$y$", fontsize=8, ha="right", va="center", color="0.3")
    ax.text(310, 588, "pipes scroll left at 3 px/frame; spacing 200 px, gap 130 px",
            fontsize=6.5, color="0.25", va="bottom", ha="center")
    ax.text(8, -8, "ceiling: lethal", fontsize=6.5, color="0.3")
    ax.text(8, 596, "ground: lethal", fontsize=6.5, color="0.3", va="top")
    ax.text(0.0, 1.0, "(a)", transform=ax.transAxes, fontweight="bold", fontsize=9, va="bottom")

    ax2 = fig.add_axes([0.57, 0.04, 0.42, 0.90]); ax2.axis("off"); ax2.set_xlim(0, 10); ax2.set_ylim(0, 10)
    xi, xh, xo = 1.8, 5.2, 8.6
    yi = np.linspace(8.6, 1.9, 5); yh = np.linspace(9.0, 1.4, 6)
    for a in yi:
        for b in yh:
            ax2.plot([xi, xh], [a, b], color="0.82", lw=0.4, zorder=1)
    for b in yh:
        ax2.plot([xh, xo], [b, 5.2], color="0.82", lw=0.4, zorder=1)
    ax2.scatter([xi] * 5, yi, s=48, color=OI[0], zorder=3)
    ax2.scatter([xh] * 6, yh, s=48, color=OI[1], zorder=3)
    ax2.scatter([xo], [5.2], s=60, color=OI[2], zorder=3)
    for a, l in zip(yi, [r"$y$", r"$v$", r"$dx$", r"$\Delta_{top}$", r"$\Delta_{bot}$"]):
        ax2.text(xi - 0.35, a, l, ha="right", va="center", fontsize=7.5)
    ax2.text(xi, 9.7, "input (5)", ha="center", fontsize=7); ax2.text(xh, 10.0, "hidden (6, tanh)", ha="center", fontsize=7)
    ax2.text(xo, 6.2, "output (1)", ha="center", fontsize=7); ax2.text(xo, 4.3, "flap iff\n$z>0$", ha="center", va="top", fontsize=7)
    ax2.text(5.2, 0.35, "genome: 30 + 6 + 6 + 1 = 43 real genes", ha="center", fontsize=7, color="0.25")
    ax2.text(0.0, 1.0, "(b)", transform=ax2.transAxes, fontweight="bold", fontsize=9, va="bottom")
    fig.savefig(f"{OUT}/fig_setup.png")
    plt.close(fig)


# ------------------------------------------------------------------ Fig 2
def fig_baseline(gens):
    if not have(gens, "base"):
        return
    fig, axs = plt.subplots(1, 3, figsize=(6.5, 2.2))
    d = gens[gens.cond == "base"]
    ax = axs[0]
    for s, g in d.groupby("seed"):
        ax.plot(g.gen, g.val_pipes, color=OI[0], alpha=0.16, lw=0.6)
    curve(ax, gens, "base", color=OI[0], band=False, lw=1.8)
    ax.set_xlabel("generation"); ax.set_ylabel("validation pipes (best individual)"); ax.set_ylim(0, 155); panel(ax, "(a)")
    ax = axs[1]
    curve(ax, gens, "base", y="div", color=OI[1]); ax.set_xlabel("generation"); ax.set_ylabel("genome diversity"); ax.set_ylim(0, 6); panel(ax, "(b)")
    ax = axs[2]
    curve(ax, gens, "base", y="frac_ceil", color=OI[3], label="pop. dying at ceiling")
    curve(ax, gens, "base", y="best_flap_rate", color=OI[2], label="flap rate of best")
    ax.set_xlabel("generation"); ax.set_ylabel("fraction"); ax.set_ylim(0, 1.02); ax.legend(frameon=False, loc="upper right"); panel(ax, "(c)")
    fig.tight_layout(w_pad=1.0)
    fig.savefig(f"{OUT}/fig_baseline.png"); plt.close(fig)


# ------------------------------------------------------------------ Fig 3
def fig_methods(runs, gens, rule):
    if not have(gens, "base", "hc", "rs"):
        return
    fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.4), gridspec_kw=dict(width_ratios=[1.25, 1]))
    ax = axs[0]
    curve(ax, gens, "base", x="evals", color=OI[0], label="GA (baseline)")
    curve(ax, gens, "hc", x="evals", color=OI[1], label=r"(1+1) hill climber")
    curve(ax, gens, "rs", x="evals", color=OI[2], label="random search")
    ax.axhline(rule["hard"]["test_pipes"], color="0.4", ls="--", lw=0.8)
    ax.text(14600, rule["hard"]["test_pipes"] + 4, "best hand-tuned 2-gene rule", fontsize=6.5, color="0.3", ha="right")
    ax.set_xlabel("episode evaluations"); ax.set_ylabel("validation pipes"); ax.set_ylim(0, 155)
    ax.legend(frameon=False, loc="upper left", fontsize=6.8); panel(ax, "(a)")
    ax = axs[1]
    names = [n for n in ["base", "hc", "rs", "rule_ga"] if n in set(runs.cond)]
    lab = {"base": "GA\n(MLP)", "hc": "hill\nclimber", "rs": "random\nsearch", "rule_ga": "GA\n(2-gene)"}
    boxstrip(ax, runs, names, [lab[n] for n in names], [OI[0], OI[1], OI[2], OI[3]])
    ax.axhline(rule["hard"]["test_pipes"], color="0.4", ls="--", lw=0.8); panel(ax, "(b)")
    fig.tight_layout(w_pad=1.2)
    fig.savefig(f"{OUT}/fig_methods.png"); plt.close(fig)


# ------------------------------------------------------------------ Fig 4/5
def fig_pair(runs, gens, names, labels, fname, xcol="gen", colors=None, xlabel="generation", legloc="lower right"):
    names = [n for n in names if n in set(runs.cond)]
    if len(names) < 2:
        return
    colors = colors or OI
    fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.4), gridspec_kw=dict(width_ratios=[1.15, 1]))
    ax = axs[0]
    for i, n in enumerate(names):
        curve(ax, gens, n, x=xcol, color=colors[i % len(colors)], label=labels[n], band=False)
    ax.set_xlabel(xlabel); ax.set_ylabel("validation pipes (median of runs)"); ax.set_ylim(0, 155)
    ax.legend(frameon=False, loc=legloc); panel(ax, "(a)")
    ax = axs[1]
    boxstrip(ax, runs, names, [labels[n] for n in names], [colors[i % len(colors)] for i in range(len(names))], rot=25)
    panel(ax, "(b)")
    fig.tight_layout(w_pad=1.2)
    fig.savefig(f"{OUT}/{fname}.png"); plt.close(fig)


# ------------------------------------------------------------------ Fig 6
def fig_mutation(runs, res):
    grid = res["mut_grid"]
    if len(grid) < 10:
        return
    rates = [0.02, 0.05, 0.10, 0.20, 0.40]; sigmas = [0.05, 0.15, 0.30, 0.60]
    M = np.full((len(rates), len(sigmas)), np.nan)
    for i, r in enumerate(rates):
        for j, s in enumerate(sigmas):
            if (r, s) in grid:
                M[i, j] = grid[(r, s)][0]
    fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.5), gridspec_kw=dict(width_ratios=[1.05, 1]))
    ax = axs[0]
    im = ax.imshow(M, cmap="viridis", vmin=0, vmax=max(100, np.nanmax(M)), aspect="auto", origin="lower")
    for i in range(len(rates)):
        for j in range(len(sigmas)):
            if not np.isnan(M[i, j]):
                ax.text(j, i, f"{M[i, j]:.0f}", ha="center", va="center", fontsize=7.5,
                        color="w" if M[i, j] < 0.6 * np.nanmax(M) else "k")
    ax.set_xticks(range(4)); ax.set_xticklabels(sigmas); ax.set_yticks(range(5)); ax.set_yticklabels(rates)
    ax.set_xlabel(r"mutation step size $\sigma$"); ax.set_ylabel("per-gene mutation rate")
    ax.add_patch(Rectangle((1.5, 1.5), 1, 1, fill=False, ec="w", lw=1.4))
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03); cb.set_label("median champion test pipes", fontsize=7)
    cb.ax.tick_params(labelsize=6.5); panel(ax, "(a)")
    ax = axs[1]
    names = [n for n in ["base", "mut_annealed", "mut_reset"] if n in set(runs.cond)]
    lab = {"base": "Gaussian\nconstant", "mut_annealed": "Gaussian\nannealed", "mut_reset": "uniform\nreset"}
    boxstrip(ax, runs, names, [lab[n] for n in names], [OI[0], OI[2], OI[3]]); panel(ax, "(b)")
    fig.tight_layout(w_pad=1.2)
    fig.savefig(f"{OUT}/fig_mutation.png"); plt.close(fig)


# ------------------------------------------------------------------ Fig 7
def fig_popelite(runs):
    fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.3), gridspec_kw=dict(width_ratios=[1, 1.15]))
    names = [n for n in ["pop_20", "base", "pop_100", "pop_200"] if n in set(runs.cond)]
    lab = {"pop_20": "20\n(250 gen)", "base": "50\n(100 gen)", "pop_100": "100\n(50 gen)", "pop_200": "200\n(25 gen)"}
    if names:
        boxstrip(axs[0], runs, names, [lab[n] for n in names], OI[:4]); axs[0].set_xlabel("population size (generations)"); panel(axs[0], "(a)")
    names = [n for n in ["elite_0", "elite_1", "base", "elite_5", "elite_10"] if n in set(runs.cond)]
    lab = {"elite_0": "0", "elite_1": "1", "base": "2", "elite_5": "5", "elite_10": "10"}
    if names:
        boxstrip(axs[1], runs, names, [lab[n] for n in names], OI[:5]); axs[1].set_xlabel("number of elites (population 50)"); panel(axs[1], "(b)")
    fig.tight_layout(w_pad=1.2)
    fig.savefig(f"{OUT}/fig_popelite.png"); plt.close(fig)


# ------------------------------------------------------------------ Fig 8
def fig_noise(runs, res):
    fig, axs = plt.subplots(1, 3, figsize=(6.5, 2.4), gridspec_kw=dict(width_ratios=[0.8, 1.15, 1.15]))
    names = [n for n in ["fit_frames", "fit_pipes", "base"] if n in set(runs.cond)]
    lab = {"fit_frames": "frames\nonly", "fit_pipes": "pipes +\nframes", "base": "shaped\n(default)"}
    if names:
        boxstrip(axs[0], runs, names, [lab[n] for n in names], [OI[1], OI[2], OI[0]]); panel(axs[0], "(a)")
    names = [n for n in ["K1", "agg_mean", "base", "K5"] if n in set(runs.cond)]
    lab = {"K1": "1 seed\n(300 gen)", "agg_mean": "3 seeds\nmean", "base": "3 seeds\nmin", "K5": "5 seeds\nmin (60 gen)"}
    if names:
        boxstrip(axs[1], runs, names, [lab[n] for n in names], [OI[1], OI[3], OI[0], OI[2]]); panel(axs[1], "(b)")
    ax = axs[2]
    tp = res["train_perf"]
    order = [("pool_1", 1), ("pool_3", 3), ("base", 10), ("pool_100", 100)]
    order = [(n, p) for n, p in order if n in tp]
    if order:
        xs = np.arange(len(order))
        tr = [tp[n] for n, _ in order]
        te = [runs[runs.cond == n].test_pipes.to_numpy() for n, _ in order]
        for i in range(len(order)):
            ax.scatter(np.full(len(tr[i]), i - 0.16) + np.random.default_rng(i).uniform(-0.08, 0.08, len(tr[i])), tr[i], s=6, color=OI[4], alpha=0.8, lw=0)
            ax.scatter(np.full(len(te[i]), i + 0.16) + np.random.default_rng(i + 9).uniform(-0.08, 0.08, len(te[i])), te[i], s=6, color=OI[0], alpha=0.8, lw=0)
        ax.plot(xs - 0.16, [np.mean(t) for t in tr], color=OI[4], lw=1.3, marker="_", ms=9, label="training seeds")
        ax.plot(xs + 0.16, [np.mean(t) for t in te], color=OI[0], lw=1.3, marker="_", ms=9, label="unseen seeds")
        ax.set_xticks(xs); ax.set_xticklabels([str(p) for _, p in order]); ax.set_xlabel("training-seed pool size")
        ax.set_ylabel("champion pipes"); ax.set_ylim(0, 155); ax.legend(frameon=False, loc="lower right"); panel(ax, "(c)")
    fig.tight_layout(w_pad=1.0)
    fig.savefig(f"{OUT}/fig_noise.png"); plt.close(fig)


# ------------------------------------------------------------------ Fig 9
def fig_diversity(runs, gens):
    if not have(gens, "div_ctrl"):
        return
    fig, axs = plt.subplots(1, 3, figsize=(6.5, 2.3), gridspec_kw=dict(width_ratios=[1, 1, 1.05]))
    cols = {"base": OI[6], "div_ctrl": OI[1], "div_share3": OI[0], "div_imm10": OI[2]}
    labs = {"base": "baseline setting", "div_ctrl": "greedy setting", "div_share3": "+ sharing (r=3)", "div_imm10": "+ immigrants 10%"}
    for i, key in enumerate(["div", "val_pipes"]):
        ax = axs[i]
        for n in ["base", "div_ctrl", "div_share3", "div_imm10"]:
            if have(gens, n):
                curve(ax, gens, n, x="evals", y=key, color=cols[n], label=labs[n], band=(n != "base"))
        ax.set_xlabel("episode evaluations")
        ax.set_ylabel("genome diversity" if key == "div" else "validation pipes")
        if key == "val_pipes":
            ax.set_ylim(0, 155)
        else:
            ax.set_yscale("log"); ax.set_ylim(0.03, 8)
        panel(ax, "(a)" if i == 0 else "(b)")
    axs[0].legend(frameon=False, loc="upper right", fontsize=6.2)
    names = [n for n in ["div_ctrl", "div_share1", "div_share2", "div_share3", "div_share4", "div_imm10", "div_imm20"] if n in set(runs.cond)]
    lab = {"div_ctrl": "none", "div_share1": "share\nr=1", "div_share2": "r=2", "div_share3": "r=3", "div_share4": "r=4", "div_imm10": "imm.\n10%", "div_imm20": "20%"}
    boxstrip(axs[2], runs, names, [lab[n] for n in names], [OI[1]] + [OI[0]] * 4 + [OI[2]] * 2)
    panel(axs[2], "(c)")
    fig.tight_layout(w_pad=1.0)
    fig.savefig(f"{OUT}/fig_diversity.png"); plt.close(fig)


# ------------------------------------------------------------------ Fig 10
def fig_traces(runs, res, tables):
    sub = runs[runs.cond == "base"]
    if sub.empty:
        return
    pk = pickle.load(open("logs/base.pkl", "rb"))
    champs = {r["seed"]: r["champ"] for r in pk["runs"]}
    med_seed = sub.iloc[(sub.test_pipes - sub.test_pipes.median()).abs().argsort().iloc[0]].seed
    champ = champs[int(med_seed)]
    tab = tables["hard"]
    # exactly reproduce generation 0 of the SAME logged run (same RNG stream as ga.evolve.run)
    r0 = np.random.default_rng(10_000 + int(med_seed))
    cfg0 = G.Config()
    pop0 = r0.uniform(-1, 1, (cfg0.pop, 43))
    sd0 = r0.choice(G.TRAIN_OFFSET + np.arange(cfg0.train_pool), size=cfg0.K, replace=False)
    fit0 = G.fitness_from_stats(E.eval_batch(pop0, sd0, tab, cfg0.max_frames, 0), cfg0)
    rand_best = pop0[int(np.argmax(fit0))]
    fig, axs = plt.subplots(3, 1, figsize=(6.5, 4.6), sharex=False)
    T = 620
    specs = [("generation 0: fittest of the 50 random initial networks", rand_best, 2000),
             ("evolved champion (median run), unseen seed A", champ, 2000),
             ("evolved champion (median run), unseen seed B", champ, 2004)]
    for k, (ax, (title, g, seed)) in enumerate(zip(axs, specs)):
        ty, r = E.trace(g, seed, tab, T, 0)
        gaps = tab[seed]
        for i in range(12):
            t0 = (E.FIRST_X + E.SPACING * i - (E.BIRD_X + E.HALF)) / E.SPEED
            t1 = (E.FIRST_X + E.SPACING * i + E.PIPE_W - (E.BIRD_X - E.HALF)) / E.SPEED
            c = gaps[i]
            ax.add_patch(Rectangle((t0, 0), t1 - t0, c - E.GAP / 2, fc="0.65", ec="none"))
            ax.add_patch(Rectangle((t0, c + E.GAP / 2), t1 - t0, 600 - c - E.GAP / 2, fc="0.65", ec="none"))
        ax.plot(np.arange(1, len(ty) + 1), ty, color=OI[0], lw=1.1)
        if int(r[2]) != E.TRUNC and len(ty) < T:
            ax.scatter([len(ty)], [ty[-1]], marker="x", color=OI[1], s=26, zorder=5, lw=1.4)
            cause = {1: "ground", 2: "ceiling", 3: "pipe"}[int(r[2])]
            ax.text(len(ty) + 6, ty[-1], f"dies ({cause})", color=OI[1], fontsize=7, va="center")
        ax.set_ylim(600, 0); ax.set_xlim(0, T); ax.set_ylabel("height $y$")
        ax.set_title(title, loc="left", fontsize=8)
        if k == 2:
            ax.set_xlabel("frame")
    fig.tight_layout(h_pad=0.8)
    fig.savefig(f"{OUT}/fig_traces.png"); plt.close(fig)


# ------------------------------------------------------------------ Fig 11
def fig_rule_landscape(tables):
    world = "hard"
    tab = tables[world]
    aa = np.linspace(-1.3, 1.6, 59); bb = np.linspace(-1.2, 2.2, 55)
    seeds = G.TRAIN_OFFSET + np.arange(5)
    Z = np.zeros((len(bb), len(aa)))
    for j, b in enumerate(bb):
        pop = np.stack([aa, np.full_like(aa, b)], 1)
        Z[j] = E.eval_batch(pop, seeds, tab, 10000, 1)[:, :, 1].mean(1)
    cfg = G.Config(mode=1, gens=20)
    rng = np.random.default_rng(10_100)
    pop = rng.uniform(-1, 1, (cfg.pop, 2)); train = G.TRAIN_OFFSET + np.arange(cfg.train_pool)
    snaps = {}
    for gen in range(cfg.gens):
        sd = rng.choice(train, size=3, replace=False)
        fit = G.fitness_from_stats(E.eval_batch(pop, sd, tab, cfg.max_frames, 1), cfg)
        if gen in (0, 4, 19):
            snaps[gen] = pop.copy()
        order = np.argsort(-fit)
        a = pop[G.select(pop, fit, rng, cfg, cfg.pop - cfg.elite)]; b = pop[G.select(pop, fit, rng, cfg, cfg.pop - cfg.elite)]
        kids = G.mutate(G.cross(a, b, rng, cfg), rng, cfg, gen)
        pop = np.vstack([pop[order[:cfg.elite]].copy(), kids])
    fig, ax = plt.subplots(1, 1, figsize=(3.6, 2.9))
    im = ax.imshow(Z, origin="lower", extent=[aa[0], aa[-1], bb[0], bb[-1]], aspect="auto", cmap="viridis")
    for (gen, P), c, mk in zip(snaps.items(), ["w", OI[4], OI[1]], ["o", "s", "^"]):
        ax.scatter(P[:, 0], P[:, 1], s=13, facecolor=c, edgecolor="k", lw=0.4, marker=mk, label=f"generation {gen}", zorder=3)
    ax.set_xlabel(r"gene 0: threshold $a$"); ax.set_ylabel(r"gene 1: velocity gain $b$")
    ax.legend(frameon=True, fontsize=6.5, loc="upper left", framealpha=0.9)
    cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03); cb.set_label("mean pipes cleared", fontsize=7); cb.ax.tick_params(labelsize=6.5)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig_landscape.png"); plt.close(fig)
    return Z.max()


if __name__ == "__main__":
    tables = {w: worlds.table(w) for w in worlds.WORLDS}
    res = pickle.load(open("results.pkl", "rb"))
    runs, gens, rule = res["runs"], res["gens"], res["rule"]
    fig_setup(); fig_baseline(gens); fig_methods(runs, gens, rule)
    fig_pair(runs, gens, ["sel_tour2", "base", "sel_tour5", "sel_roulette", "sel_rank"],
             {"sel_tour2": "tournament k=2", "base": "tournament k=3", "sel_tour5": "tournament k=5",
              "sel_roulette": "roulette", "sel_rank": "linear rank"}, "fig_selection", legloc="upper left")
    fig_pair(runs, gens, ["cx_none", "cx_single", "base", "cx_arith"],
             {"cx_none": "none", "cx_single": "single-point", "base": "uniform", "cx_arith": "arithmetic"}, "fig_crossover")
    fig_mutation(runs, res); fig_popelite(runs); fig_noise(runs, res); fig_diversity(runs, gens)
    fig_traces(runs, res, tables); print("landscape max", fig_rule_landscape(tables))
    print(sorted(os.listdir(OUT)))

# Neuroevolution of a Flappy Bird Controller

Code, logs and figures for the paper *Neuroevolution of a Flappy Bird Controller:
An Empirical Study of Genetic Operators, Evaluation Noise and Generalisation*.

Every number in the paper is regenerated from this directory by the commands below.

## Contents

    game/engine.py     numba-compiled simulator; eval_batch() is the only entry point the GA uses
    game/worlds.py     the two environments (hard = U(150,450), standard = U(200,400))
    ga/evolve.py       Config, genetic operators, diversity metric, one GA run
    ga/baselines.py    random search and the (1+1) hill climber, budget-matched
    experiments.py     all 60 conditions; resumable, writes logs/<cond>.pkl
    analysis.py        metrics, Mann-Whitney U, Cliff's delta, Holm correction -> results.pkl
    figures.py         all 11 figures -> figures/*.png
    paperlib.py        typesetting helpers
    paper_content.py   the paper text
    build_paper.py     builds the PDF
    play.py            pygame viewer for an evolved champion on the unseen test levels
    logs/              60 pickles, 606 runs (raw per-generation records + champion genomes)

## Reproducing

    pip install numpy scipy pandas matplotlib numba reportlab pillow
    python experiments.py            # ~50 min on one core; resumable, skips finished conditions
    python experiments.py --secs=200 # or run in time-boxed batches
    python analysis.py               # prints every statistical table, writes results.pkl
    python figures.py                # writes figures/
    python build_paper.py            # writes the PDF
    python play.py [condition]       # watch the best champion fly (pip install pygame-ce); SPACE next level, UP/DOWN speed

## Protocol

Budget is 15,000 episode evaluations for every condition; generation counts are
adjusted so that N x K x G is constant. Three disjoint level-seed pools are used:
training seeds (5000+) drive selection, validation seeds (1000-1005) are for
learning curves only, and test seeds (2000-2029) are touched once by the final
champion. Pilot experiments used algorithm seeds 0-5 and 900-905; all reported
runs use seeds 100-111, so no condition was tuned on the data it is reported on.

## Headline results (hard environment, median pipes on 30 unseen levels)

    GA, 43-gene network      91.3      beats random search, delta = -0.90, p_holm = 0.001
    (1+1) hill climber       61.7      not distinguishable from the GA (p_holm = 0.60)
    GA, 2-gene rule          84.2      not distinguishable from the GA (p_holm = 0.60)
    random search             9.5
    training on 1 level      54.2      vs 91.3 on 10 levels, delta = -0.89, p_holm = 0.001
    greedy config            25.2      diversity collapses 5.34 -> 0.12
      + fitness sharing r=3  80.6      delta = 0.71, p_holm = 0.021

No selection scheme, crossover operator or mutation setting produced a difference
that survived Holm correction.

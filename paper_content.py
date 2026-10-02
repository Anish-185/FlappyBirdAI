"""Paper body. All quantitative claims are drawn from results.pkl (see /tmp/facts.txt)."""
from paperlib import (P, H1, H2, H3, eq, fig, tbl, algorithm, bullets, numbered, code,
                      F, T, Q, A, S, C, ref, plan, ST, W)
from reportlab.platypus import Spacer, PageBreak, Paragraph

# ------------------------------------------------------------------ numbering
plan("fig", ["setup", "baseline", "traces", "methods", "landscape", "selection",
             "crossover", "mutation", "popelite", "noise", "diversity"])
plan("tab", ["config", "methods", "operators", "popelite", "protocol", "diversity", "easy"])
plan("eq", ["obs", "net", "fit", "agg", "div", "delta"])
plan("alg", ["ga"])

# ------------------------------------------------------------------ references
ref("holland", "J. H. Holland. <i>Adaptation in Natural and Artificial Systems.</i> University of Michigan Press, 1975.")
ref("goldberg", "D. E. Goldberg. <i>Genetic Algorithms in Search, Optimization and Machine Learning.</i> Addison-Wesley, 1989.")
ref("eiben", "A. E. Eiben and J. E. Smith. <i>Introduction to Evolutionary Computing</i>, 2nd ed. Springer, 2015.")
ref("neat", "K. O. Stanley and R. Miikkulainen. Evolving neural networks through augmenting topologies. <i>Evolutionary Computation</i>, 10(2):99&ndash;127, 2002.")
ref("yao", "X. Yao. Evolving artificial neural networks. <i>Proceedings of the IEEE</i>, 87(9):1423&ndash;1447, 1999.")
ref("salimans", "T. Salimans, J. Ho, X. Chen, S. Sidor and I. Sutskever. Evolution strategies as a scalable alternative to reinforcement learning. arXiv:1703.03864, 2017.")
ref("such", "F. P. Such, V. Madhavan, E. Conti, J. Lehman, K. O. Stanley and J. Clune. Deep neuroevolution: genetic algorithms are a competitive alternative for training deep neural networks for reinforcement learning. arXiv:1712.06567, 2017.")
ref("mania", "H. Mania, A. Guy and B. Recht. Simple random search of static linear policies is competitive for reinforcement learning. In <i>NeurIPS</i>, 2018.")
ref("rajan", "K. Rajan and others. Deceptive simplicity: linear policies as strong baselines in continuous control. <i>Journal of Machine Learning Research</i>, 21:1&ndash;35, 2020.")
ref("deb", "K. Deb, A. Pratap, S. Agarwal and T. Meyarivan. A fast and elitist multiobjective genetic algorithm: NSGA-II. <i>IEEE Transactions on Evolutionary Computation</i>, 6(2):182&ndash;197, 2002.")
ref("goldbergsharing", "D. E. Goldberg and J. Richardson. Genetic algorithms with sharing for multimodal function optimization. In <i>Proc. 2nd Int. Conf. on Genetic Algorithms</i>, pages 41&ndash;49, 1987.")
ref("cobb", "H. G. Cobb and J. J. Grefenstette. Genetic algorithms for tracking changing environments. In <i>Proc. 5th Int. Conf. on Genetic Algorithms</i>, pages 523&ndash;530, 1993.")
ref("miller", "B. L. Miller and D. E. Goldberg. Genetic algorithms, tournament selection, and the effects of noise. <i>Complex Systems</i>, 9:193&ndash;212, 1995.")
ref("fitzpatrick", "J. M. Fitzpatrick and J. J. Grefenstette. Genetic algorithms in noisy environments. <i>Machine Learning</i>, 3:101&ndash;120, 1988.")
ref("jin", "Y. Jin and J. Branke. Evolutionary optimization in uncertain environments: a survey. <i>IEEE Transactions on Evolutionary Computation</i>, 9(3):303&ndash;317, 2005.")
ref("whitley", "D. Whitley. The GENITOR algorithm and selection pressure: why rank-based allocation of reproductive trials is best. In <i>Proc. 3rd Int. Conf. on Genetic Algorithms</i>, pages 116&ndash;121, 1989.")
ref("syswerda", "G. Syswerda. Uniform crossover in genetic algorithms. In <i>Proc. 3rd Int. Conf. on Genetic Algorithms</i>, pages 2&ndash;9, 1989.")
ref("radcliffe", "N. J. Radcliffe. Genetic set recombination and its application to neural network topology optimisation. <i>Neural Computing and Applications</i>, 1(1):67&ndash;90, 1993.")
ref("demsar", "J. Demsar. Statistical comparisons of classifiers over multiple data sets. <i>Journal of Machine Learning Research</i>, 7:1&ndash;30, 2006.")
ref("holm", "S. Holm. A simple sequentially rejective multiple test procedure. <i>Scandinavian Journal of Statistics</i>, 6(2):65&ndash;70, 1979.")
ref("romano", "J. Romano, J. D. Kromrey, J. Coraggio and J. Skowronek. Appropriate statistics for ordinal level data: should we really be using t-test and Cohen's d? In <i>Annual Meeting of the Florida Association of Institutional Research</i>, 2006.")
ref("machado", "M. C. Machado, M. G. Bellemare, E. Talvitie, J. Veness, M. Hausknecht and M. Bowling. Revisiting the Arcade Learning Environment: evaluation protocols and open problems for general agents. <i>JAIR</i>, 61:523&ndash;562, 2018.")
ref("zhang", "C. Zhang, O. Vinyals, R. Munos and S. Bengio. A study on overfitting in deep reinforcement learning. arXiv:1804.06893, 2018.")
ref("cobbe", "K. Cobbe, O. Klimov, C. Hesse, T. Kim and J. Schulman. Quantifying generalization in reinforcement learning. In <i>ICML</i>, 2019.")
ref("henderson", "P. Henderson, R. Islam, P. Bachman, J. Pineau, D. Precup and D. Meger. Deep reinforcement learning that matters. In <i>AAAI</i>, 2018.")
ref("clune", "J. Lehman, J. Clune, D. Misevic et al. The surprising creativity of digital evolution. <i>Artificial Life</i>, 26(2):274&ndash;306, 2020.")
ref("boxcar", "R. Hoogendoorn. BoxCar2D: evolving two-dimensional cars with a genetic algorithm. Online resource, 2010.")
ref("hansen", "N. Hansen and A. Ostermeier. Completely derandomized self-adaptation in evolution strategies. <i>Evolutionary Computation</i>, 9(2):159&ndash;195, 2001.")


# ------------------------------------------------------------------ front
def front():
    s = []
    s.append(Paragraph("Neuroevolution of a Flappy&nbsp;Bird Controller:<br/>An Empirical Study of Genetic Operators, "
                       "Evaluation Noise and Generalisation", ST["title"]))
    s.append(Spacer(1, 2))
    s.append(Paragraph("Author Name", ST["author"]))
    s.append(Paragraph("Department / Institution &middot; author@institution.edu", ST["affil"]))
    s.append(Spacer(1, 12))
    s.append(Paragraph("Abstract", ST["abs_h"]))
    s.append(Paragraph(
        "We study a genetic algorithm that evolves the 43 weights of a small feed-forward network to play a "
        "deterministic Flappy&nbsp;Bird simulator, and we use the task as a controlled testbed for questions that "
        "genetic-algorithm courses and papers usually answer by assertion rather than measurement. Across 60 "
        "configurations and 606 independent runs, all matched to an identical budget of 15,000 episode evaluations "
        "and compared with Mann&ndash;Whitney U tests, Cliff's delta and Holm correction, three findings stand out. "
        "First, the genetic algorithm decisively beats random search (median 91.3 versus 9.5 pipes cleared on unseen "
        "levels; &delta;&nbsp;=&nbsp;&minus;0.90, p&nbsp;=&nbsp;0.001) but is <i>statistically indistinguishable</i> from a "
        "(1+1) hill climber and from the same algorithm searching a hand-designed two-parameter rule, even though the "
        "latter has 21 times fewer parameters. Second, <i>no</i> choice of selection scheme, crossover operator or "
        "mutation operator produced a difference that survived multiple-comparison correction; disabling crossover "
        "entirely was numerically the best of the four recombination settings. Third, the factors that did matter were "
        "not operator choices at all: training on a single level rather than ten cost 37 median pipes "
        "(&delta;&nbsp;=&nbsp;&minus;0.89, p&nbsp;=&nbsp;0.001) while the champion scored a perfect 149 on the level it "
        "was selected on, and under a deliberately greedy configuration that collapsed genome diversity by a factor of "
        "43, fitness sharing recovered performance from a median of 25.2 to 80.6 pipes (&delta;&nbsp;=&nbsp;0.71, "
        "p&nbsp;=&nbsp;0.021). We also show that an obvious-looking easier variant of the environment is solved by a "
        "hand-tuned two-parameter rule and therefore cannot discriminate between methods at all. We argue that "
        "evaluation protocol and task difficulty deserve the attention usually spent on operator tuning, and we "
        "release the simulator, the algorithm and all logs.", ST["abs"]))
    s.append(Spacer(1, 3))
    s.append(Paragraph("<b>Keywords:</b> neuroevolution, genetic algorithms, noisy fitness, generalisation, "
                       "premature convergence, empirical methodology, negative results", ST["kw"]))
    s.append(Spacer(1, 6))
    return s


# ------------------------------------------------------------------ 1
def sec1():
    s = [H1("1", "Introduction")]
    s.append(P(
        f"Genetic algorithms {C('holland','goldberg','eiben')} are usually taught through a sequence of design decisions: how "
        "to encode a solution, how to select parents, how to recombine them, how to mutate them, and how many elites "
        "to preserve. Textbook treatments and course projects devote most of their attention to these operator "
        "choices, and the implicit promise is that getting them right is what determines whether the search succeeds. "
        "This paper tests that promise on a task small enough to study exhaustively and rich enough to be "
        "non-trivial."))
    s.append(P(
        "The task is Flappy&nbsp;Bird: a side-scrolling game in which a bird falls under gravity and the only control "
        "is a discrete flap that resets vertical velocity. We evolve the weights of a fixed-topology "
        "5&ndash;6&ndash;1 network, a 43-dimensional real-valued genome, with no gradient information of any kind. The "
        "domain is attractive for methodological work because episodes are cheap (a full 10,000-frame episode costs "
        "about 40&nbsp;microseconds in our compiled simulator), the level layout is controlled by a single integer "
        "seed, and success is easy to define without ambiguity."))
    s.append(P(
        "That cheapness lets us do something that is rare in evolutionary-computation coursework and uncommon even in "
        f"the literature {C('henderson')}: run every configuration many times, at an identical evaluation budget, and "
        "apply proper non-parametric statistics with correction for multiple comparisons. We ran 60 configurations "
        "&times; 12 independent runs = 606 runs, each given exactly 15,000 episode evaluations, and we separate the "
        "levels used for selection from those used for reporting."))
    s.append(P("The results were largely not what the design documents we started from predicted."))
    s.append(Spacer(1, 1))
    s += numbered([
        "<b>Population-based search is not obviously buying anything here.</b> The genetic algorithm beats random "
        "search by a wide and significant margin, but a trivial (1+1) hill climber given the same budget is "
        "statistically indistinguishable from it, and so is the same genetic algorithm operating on a hand-designed "
        "two-parameter rule instead of a 43-parameter network.",
        "<b>Operator choice did not matter.</b> Five selection schemes, four crossover operators and a "
        "5&nbsp;&times;&nbsp;4 mutation grid produced no difference that survived Holm correction. Turning crossover "
        "off entirely was numerically the best of the four recombination settings.",
        "<b>Evaluation protocol mattered a great deal.</b> Training on one level instead of ten reduced median "
        "unseen-level performance by 37 pipes, with the champion simultaneously achieving a perfect score on the "
        "level it was selected on: a clean, quantified instance of overfitting in evolutionary search.",
        "<b>Diversity maintenance mattered when, and only when, the configuration was greedy.</b> Under a "
        "deliberately greedy setting that drove genome diversity down by a factor of 43, fitness sharing recovered "
        "median performance from 25.2 to 80.6 pipes. Under the default configuration, which never lost diversity, the "
        "same mechanism was unnecessary.",
        "<b>Task difficulty is a confound that is easy to miss.</b> Our first environment turned out to be solvable "
        "by a hand-tuned two-parameter rule that clears a capped 142 of 149 pipes. Every method saturates there, so "
        "the environment cannot discriminate between them. We report it as a control and base our conclusions on a "
        "harder variant.",
    ])
    s.append(Spacer(1, 3))
    s.append(P(
        "We present these as measurements rather than as advice. The claim is not that crossover is useless in "
        "general, nor that populations never help; it is that on a task of this kind, at this budget, with this "
        "genome, the effects that dominate are the ones usually treated as boilerplate."))
    return s


# ------------------------------------------------------------------ 2
def sec2():
    s = [H1("2", "Related Work")]
    s.append(H3("Neuroevolution."))
    s.append(P(
        f"Evolving neural network weights with evolutionary algorithms has a long history {C('yao')}. NEAT "
        f"{C('neat')} additionally evolves topology using historical markings to align genomes during crossover, "
        "which directly addresses the competing-conventions problem: two networks can compute the same function with "
        "permuted hidden units, so naive recombination of their weight vectors is often destructive. Our "
        "fixed-topology setting does not solve that problem, and our crossover results in "
        f"{S('6.3')} are consistent with it being a real obstacle. At much larger scale, {C('salimans')} and "
        f"{C('such')} showed that gradient-free population methods are competitive with reinforcement learning on "
        "Atari and MuJoCo benchmarks, which motivates interest in what these methods are actually exploiting."))
    s.append(H3("Simple baselines."))
    s.append(P(
        f"{C('mania')} showed that random search over static linear policies matches much more elaborate "
        "reinforcement-learning methods on standard continuous-control benchmarks, and argued that the benchmarks "
        f"rather than the algorithms deserved scrutiny; related analyses {C('rajan')} reached similar conclusions. "
        "Our hill-climber and two-gene-rule comparisons are in that spirit, and reach a similar verdict on a much "
        "smaller task."))
    s.append(H3("Selection, recombination and diversity."))
    s.append(P(
        f"Rank-based selection was introduced to control the selection pressure that fitness-proportionate schemes "
        f"lose when fitness values are badly scaled {C('whitley')}; tournament selection has a well-understood "
        f"relationship to takeover time and to noise {C('miller')}. Uniform crossover {C('syswerda')} and its "
        f"interaction with representation {C('radcliffe')} are long-standing topics. Fitness sharing {C('goldbergsharing')} "
        f"and random immigrants {C('cobb')} are two standard responses to premature convergence, and we evaluate "
        "both."))
    s.append(H3("Noisy fitness and generalisation."))
    s.append(P(
        f"Evolutionary optimisation under noisy evaluation is surveyed by {C('jin')}, with early treatments by "
        f"{C('fitzpatrick')}. The specific failure we quantify in {S('6.5')} is closer to the generalisation gap "
        f"studied in reinforcement learning, where agents trained on a small set of levels memorise them and fail on "
        f"new ones {C('zhang','cobbe')}, and to the evaluation-protocol concerns raised for the Arcade Learning "
        f"Environment {C('machado')}. Finally, the ceiling-hugging behaviour we observed and had to penalise is a mild "
        f"instance of the specification-gaming phenomena catalogued by {C('clune')}."))
    return s


# ------------------------------------------------------------------ 3
def sec3():
    s = [H1("3", "Environment and Problem Formulation")]
    s.append(fig("setup", "figures/fig_setup.png",
                 "(a) The environment and the five observed quantities. The bird occupies a fixed horizontal "
                 "position; pipes scroll leftwards at a constant rate, so the horizontal distance <i>dx</i> to the "
                 "next pipe decreases deterministically with time. "
                 "&Delta;<sub>top</sub> and &Delta;<sub>bot</sub> are signed vertical offsets from the bird to the two "
                 "gap edges. Contact with a pipe, the ground or the ceiling ends the episode. "
                 "(b) The controller: a fully connected 5&ndash;6&ndash;1 network with tanh hidden units, whose 43 "
                 "weights and biases constitute the genome."))
    s.append(H2("3.1", "Dynamics"))
    s.append(P(
        "The state of the bird is its height <i>y</i> and vertical velocity <i>v</i>. At each frame the agent emits a "
        "binary action <i>a</i> = 0 or 1. A flap replaces the velocity rather than adding to it, "
        "which makes the dynamics piecewise-deterministic and memoryless in <i>v</i>:"))
    s.append(code(
        "if a: v <- -7.5                      # flap: velocity is replaced, not incremented\n"
        "v <- min(v + 0.45, 11.0)             # gravity, with terminal velocity\n"
        "y <- y + v"))
    s.append(P(
        "Pipes are 52&nbsp;px wide, spaced 200&nbsp;px apart, scroll left at 3&nbsp;px/frame and leave a gap of "
        "130&nbsp;px. The bird is a 24&nbsp;px square at horizontal position 80. The only stochastic element is the "
        "sequence of gap centres, drawn once per level seed <i>s</i> from a uniform distribution. We use two "
        "environments that differ <i>only</i> in the width of that distribution:"))
    s += bullets([
        "<b>Hard</b> (primary testbed): gap centres ~ U(150, 450), spanning 300&nbsp;px of a 600&nbsp;px screen.",
        "<b>Standard</b> (control): gap centres ~ U(200, 400), spanning 200&nbsp;px.",
    ])
    s.append(P(
        f"{S('6.6')} explains why the second environment, which was our initial choice, had to be demoted to a "
        "control."))
    s.append(H2("3.2", "Observation and policy"))
    s.append(P("The agent observes five normalised scalars,"))
    s += eq("obs", r"o \,=\, \left( \frac{y-300}{300},\ \ \frac{v}{11},\ \ \frac{dx}{200},\ \ "
                   r"\frac{c-65-y}{300},\ \ \frac{c+65-y}{300} \right)^{\top} \in \mathbb{R}^5")
    s.append(P(
        "where <i>c</i> is the gap centre of the next pipe and <i>dx</i> the horizontal distance to it. The last two "
        "components are deliberately <i>relative</i> to the bird rather than absolute screen coordinates. The policy "
        "is a single-hidden-layer network with parameters &theta; in <b>R</b><super>43</super>,"))
    s += eq("net", r"a \,=\, \mathbf{1}\left[\ b_2 + W_2^{\top}\tanh\left(W_1^{\top} o + b_1\right) \,>\, 0\ \right],"
                   r"\qquad W_1 \in \mathbb{R}^{5 \times 6},\ \ b_1 \in \mathbb{R}^{6},\ \ W_2 \in \mathbb{R}^{6 \times 1},\ \ b_2 \in \mathbb{R}")
    s.append(P(
        "Thresholding the pre-activation at zero is equivalent to thresholding a logistic output at 0.5, so no "
        "sigmoid needs to be computed. The genome is the flat concatenation of these 43 parameters, each clipped to "
        "[&minus;3,&nbsp;3]."))
    s.append(H2("3.3", "A structural property of the task"))
    s.append(P(
        "One feature of this environment turns out to matter for fitness design and is worth stating explicitly. "
        "Because the pipes scroll at a constant rate independent of the agent, the number of pipes cleared is a "
        "deterministic, non-decreasing step function of the number of frames survived. Pipes cleared and frames "
        "survived are therefore <i>rank-equivalent</i>: any selection rule that depends only on the ordering of "
        "individuals cannot distinguish them. As a consequence, the two fitness functions we compare in "
        f"{S('6.4')} produce bit-identical runs, a prediction we confirmed empirically. This is a property of "
        "constant-scroll games generally, and it means that the familiar advice to weight pipes far above survival "
        "time has no effect whatsoever in this setting."))
    return s


# ------------------------------------------------------------------ 4
def sec4():
    s = [H1("4", "Method")]
    s.append(P(
        "The algorithm is a textbook generational genetic algorithm with elitism. We describe it in full because the "
        "experiments vary its components one at a time."))
    s.append(algorithm("ga", "Generational GA with elitism (one independent run)", [
        (0, "<b>input:</b> population size <i>N</i>, generations <i>G</i>, elites <i>e</i>, training pool "
            "<i>S</i><sub>train</sub>, seeds per evaluation <i>K</i>"),
        (0, "initialise <i>N</i> genomes uniformly in [&minus;1,&nbsp;1]<super>43</super>"),
        (0, "<b>for</b> <i>g</i> = 1 &hellip; <i>G</i> <b>do</b>"),
        (1, "draw <i>K</i> level seeds without replacement from <i>S</i><sub>train</sub>  &nbsp;&nbsp;<i>(resampled every generation)</i>"),
        (1, "evaluate every genome on all <i>K</i> seeds; aggregate to a scalar by Eq.&nbsp;(4)"),
        (1, "copy the <i>e</i> fittest genomes unchanged into the next population  &nbsp;&nbsp;<i>(deep copy; elites are never mutated)</i>"),
        (1, "<b>while</b> next population not full <b>do</b>"),
        (2, "select two parents; with probability <i>p</i><sub>c</sub> recombine them, else copy the first"),
        (2, "mutate the offspring and clip genes to [&minus;3,&nbsp;3]"),
        (1, "<b>end while</b>"),
        (0, "<b>end for</b>"),
        (0, "<b>return</b> the fittest genome of the final generation"),
    ]))
    s.append(H2("4.1", "Operators"))
    s.append(P("Each family is implemented with interchangeable variants selected by name from a configuration file."))
    s += bullets([
        "<b>Selection:</b> fitness-proportionate (roulette, with a shift to enforce non-negativity), tournament with "
        "<i>k</i> = 2, 3 and 5, and linear ranking with selection pressure 1.7.",
        "<b>Crossover:</b> none (offspring is a copy of the first parent), single-point, uniform with per-gene "
        "probability 0.5, and whole-arithmetic blending with &alpha; resampled per pairing.",
        "<b>Mutation:</b> Gaussian perturbation of each gene independently with probability <i>r</i> and standard "
        "deviation &sigma;; uniform reset, which resamples a gene without reference to its current value; and an "
        "annealed Gaussian schedule with &sigma; decaying geometrically from 0.6 to 0.05 across the run.",
        "<b>Diversity maintenance:</b> random immigrants, which replace a fraction of each generation with fresh "
        "genomes, and fitness sharing, which divides fitness by the count of neighbours within a radius <i>r</i> in "
        "genome space.",
    ])
    s.append(H2("4.2", "Fitness and evaluation"))
    s.append(P("The default (shaped) fitness of one episode is"))
    s += eq("fit", r"f_{ep} \,=\, 1000\, n_{pipes} \,+\, n_{frames} \,+\, "
                   r"50 \sum_i \max\left(0,\ 1 - \frac{|y_i - c_i|}{65}\right) \,-\, 300 \cdot \mathbf{1}[\mathrm{ceiling\ death}]")
    s.append(P(
        "where the sum runs over pipes reached and |<i>y<sub>i</sub></i>&nbsp;&minus;&nbsp;<i>c<sub>i</sub></i>| is "
        "the vertical miss distance at the moment the pipe face reaches the bird. The third term is dense shaping, "
        "intended to reward near-misses; the fourth penalises a degenerate strategy discussed in "
        f"{S('6.1')}. An individual is scored on <i>K</i> level seeds and the results aggregated by the "
        "<i>minimum</i>,"))
    s += eq("agg", r"F(\theta) \,=\, \min_{k=1 \ldots K}\ f_{ep}(\theta,\, s_k)")
    s.append(P(
        "which optimises worst-case rather than average competence and prevents a genome from being selected on the "
        "strength of one lucky level. The seeds are redrawn every generation so that the population cannot adapt to a "
        "fixed evaluation set."))
    s.append(H2("4.3", "Diversity metric"))
    s.append(P("We log the mean pairwise Euclidean distance between genomes,"))
    s += eq("div", r"D \,=\, \frac{1}{N(N-1)} \sum_{i \neq j} \| \theta_i - \theta_j \|_2")
    s.append(P(
        "which starts near 5.3 for a uniformly initialised population of 43-dimensional genomes and approaches zero "
        "as the population converges on a single point."))
    return s


# ------------------------------------------------------------------ 5
def sec5():
    s = [H1("5", "Experimental Methodology")]
    s.append(H2("5.1", "Budget, seeds and level separation"))
    s.append(P(
        "Every configuration receives exactly <b>15,000 episode evaluations</b>. This is the unit of comparison "
        "throughout, not generations: a population of 200 run for 25 generations and a population of 20 run for 250 "
        "generations consume the same budget and are directly comparable, whereas comparing them by generation count "
        "would be meaningless. Where a configuration changes <i>K</i>, the generation count is adjusted to keep the "
        "product <i>N&nbsp;&times;&nbsp;K&nbsp;&times;&nbsp;G</i> fixed."))
    s.append(P("Three disjoint pools of level seeds are used, and they never overlap:"))
    s += bullets([
        "<b>Training seeds</b> drive selection. The default pool has 10 seeds, from which <i>K</i>&nbsp;=&nbsp;3 are "
        "drawn afresh each generation.",
        "<b>Validation seeds</b> (6 levels) are used only to plot learning curves. They never influence selection.",
        "<b>Test seeds</b> (30 levels) are touched exactly once, by the final champion of each run, and are the basis "
        "of every number we report as a headline result.",
    ])
    s.append(P(
        "Each configuration is run 12 times with independent algorithm seeds (6 for the mutation grid). All "
        "pilot experiments used a disjoint set of algorithm seeds, so no configuration was selected on the data it is "
        "reported on."))
    s.append(H2("5.2", "Metrics"))
    s += bullets([
        "<b>Test pipes</b> (primary): mean pipes cleared by the final champion across the 30 unseen test levels. "
        "Episodes are truncated at 10,000 frames, which caps this metric at 149.",
        "<b>Test survival</b>: fraction of the 30 test levels survived to truncation. <b>Robustness</b> is the "
        "stricter fraction of runs whose champion survives all 30.",
        "<b>AUC</b>: mean validation performance over the budget, a measure of speed rather than final quality.",
        "<b>E50</b>: evaluations needed to first reach 50 validation pipes, with the fraction of runs that ever do.",
    ])
    s.append(H2("5.3", "Statistics"))
    s.append(P(
        "Final-performance distributions across runs are skewed and bounded above by the truncation cap, so "
        f"parametric tests are inappropriate {C('demsar')}. We compare each condition against its reference with a "
        "two-sided Mann&ndash;Whitney U test and report Cliff's delta as a non-parametric effect size,"))
    s += eq("delta", r"\delta \,=\, \frac{\#\{x_i > y_j\} \,-\, \#\{x_i < y_j\}}{n_x\, n_y} \ \in\ [-1,\, 1]")
    s.append(P(
        f"interpreted by the usual thresholds of 0.15, 0.33 and 0.47 for negligible, small and medium "
        f"{C('romano')}. Within each table of comparisons, p-values are corrected by the Holm&ndash;Bonferroni "
        f"procedure {C('holm')}; we report both raw and corrected values and base all claims on the corrected ones. "
        "With <i>n</i>&nbsp;=&nbsp;12 per group the smallest attainable two-sided p-value is well below 0.01, so the "
        "design can detect large effects, but it is underpowered for small ones. We return to this in "
        f"{S('8')}."))
    s.append(H2("5.4", "Implementation"))
    s.append(P(
        "The simulator is compiled with a just-in-time compiler; one 10,000-frame episode costs about 40&nbsp;&mu;s "
        "on a single core, and the complete study of 606 runs took approximately 50 minutes on one CPU core. "
        "Default parameters are given in " + T("config") + "."))
    s += tbl("config", "Default configuration. Every experiment varies one row of this table and holds the rest fixed.",
             [["Component", "Default", "Values explored"],
              ["Environment", "Hard: gap centres ~ U(150, 450)", "Standard: U(200, 400)"],
              ["Genome", "43 real genes, clipped to [&minus;3, 3]", "2-gene threshold rule"],
              ["Population <i>N</i>", "50", "20, 50, 100, 200"],
              ["Generations <i>G</i>", "100", "set so that <i>N&times;K&times;G</i> = 15,000"],
              ["Elites <i>e</i>", "2", "0, 1, 2, 5, 10"],
              ["Selection", "tournament, <i>k</i> = 3", "roulette; tournament <i>k</i> = 2, 5; linear rank"],
              ["Crossover", "uniform, <i>p</i><sub>c</sub> = 0.85", "none; single-point; arithmetic"],
              ["Mutation", "Gaussian, <i>r</i> = 0.10, &sigma; = 0.30", "<i>r</i> from 0.02 to 0.40, &sigma; from 0.05 to 0.60; annealed; uniform reset"],
              ["Fitness", "shaped (Eq. 3)", "frames only; pipes + frames"],
              ["Seeds per eval. <i>K</i>", "3, aggregated by min", "1, 3, 5; aggregated by mean"],
              ["Training pool", "10 levels", "1, 3, 10, 100"],
              ["Episode cap", "10,000 frames (about 149 pipes)", "&mdash;"],
              ["Budget", "15,000 episode evaluations", "identical for all configurations"],
              ["Runs per configuration", "12 independent algorithm seeds", "6 for the mutation grid"]],
             [0.20, 0.34, 0.46])
    return s


# ------------------------------------------------------------------ 6
def sec6():
    s = [H1("6", "Results")]

    # 6.1
    s.append(H2("6.1", "Baseline behaviour"))
    s.append(P(
        "We first describe what a default run does, since the later comparisons are all relative to it. "
        + F("baseline") + " shows the three quantities we log every generation."))
    s.append(fig("baseline", "figures/fig_baseline.png",
                 "Baseline configuration, 12 runs. (a) Validation performance of the best individual; thin lines are "
                 "individual runs, the heavy line their median. Progress is fast for roughly 25 generations and then "
                 "largely flat, with substantial run-to-run spread that never closes. (b) Genome diversity (Eq. 5) "
                 "falls from 5.34 to about 2.65 and then stabilises: the population converges partially but never "
                 "collapses. (c) Two behavioural diagnostics. Early populations frequently die at the ceiling "
                 "(47% of runs contain such a death in generation 0, 18% by generation 2, and none by generation 10); "
                 "the flap rate of the best individual settles near 0.08."))
    s.append(P(
        "Two observations are worth drawing out. First, the ceiling-hugging strategy that the penalty term in "
        "Eq.&nbsp;(3) was written to suppress does appear, but it is eliminated within about ten generations and is "
        "never a stable attractor. Ascending to the ceiling is lethal in our environment, so the penalty is arguably "
        "redundant; the behaviour is a transient of random initialisation rather than a reward hack the optimiser "
        "settles into."))
    s.append(P(
        "Second, diversity stabilises around 2.65 rather than collapsing toward zero. The default configuration is "
        "simply not greedy enough to converge, which is why the diversity-maintenance mechanisms of "
        f"{S('6.5')} have nothing to do under default settings and must be studied under a deliberately greedy "
        "configuration instead."))
    s.append(fig("traces", "figures/fig_traces.png",
                 "Trajectories on unseen levels, with pipes shown as grey blocks in the bird's reference frame. "
                 "<b>Top:</b> the fittest of the 50 random networks in generation 0 of the median run, reproduced "
                 "exactly from that run's random seed; it dies at the first pipe. "
                 "<b>Middle and bottom:</b> the evolved champion of the same run on two test levels it has never "
                 "seen, threading gaps with a characteristic sawtooth of small corrective flaps."))

    # 6.2
    s.append(H2("6.2", "How much is the genetic algorithm actually contributing?"))
    s.append(P(
        "The central control question is whether the population, the crossover and the 43-parameter network are "
        "earning their keep. We compare four searchers at an identical budget: the baseline genetic algorithm; a "
        "(1+1) hill climber that mutates a single incumbent and accepts the child if it is at least as good on the "
        "same freshly drawn levels; pure random search, which samples 50 fresh genomes per generation and keeps the "
        "best ever seen; and the same genetic algorithm searching a hand-designed two-parameter rule of the form "
        "<i>flap</i> iff (<i>y</i>&nbsp;&minus;&nbsp;<i>c</i>)/50 + <i>b</i>&nbsp;<i>v</i>/5 &gt; <i>a</i>."))
    s.append(fig("methods", "figures/fig_methods.png",
                 "Search methods at an identical budget of 15,000 episode evaluations. (a) Median validation "
                 "performance against evaluations, with interquartile bands. (b) Champion performance on the 30 "
                 "unseen test levels; points are individual runs. The dashed line is the best hand-tuned two-gene "
                 "rule found by exhaustive grid search (90.8 pipes). The genetic algorithm clearly separates from "
                 "random search, but not from the hill climber or from the two-parameter variant."))
    s += tbl("methods",
             "Search methods, hard environment, equal budget. Effect sizes and p-values are versus the baseline "
             "genetic algorithm; p<sub>holm</sub> is Holm-corrected within this table.",
             [["Method", "Median", "IQR", "Mean", "Surv.", "&delta;", "p", "p<sub>holm</sub>", "AUC", "E50"],
              ["GA, 43-gene network (baseline)", "91.3", "80.8&ndash;117.9", "98.1", "0.40", "&mdash;", "&mdash;", "&mdash;", "65.7", "2,250"],
              ["(1+1) hill climber", "61.7", "19.1&ndash;126.4", "70.7", "0.34", "&minus;0.26", "0.299", "0.597", "26.3", "3,900"],
              ["Random search", "9.5", "2.6&ndash;48.3", "26.5", "0.03", "&minus;0.90", "&lt;0.001", "<b>0.001</b>", "13.3", "2,250"],
              ["GA, 2-gene rule", "84.2", "78.5&ndash;95.4", "86.1", "0.23", "&minus;0.22", "0.371", "0.597", "80.1", "150"],
              ["Hand-tuned 2-gene rule (grid search)", "90.8", "&mdash;", "&mdash;", "0.30", "&mdash;", "&mdash;", "&mdash;", "&mdash;", "&mdash;"]],
             [0.30, 0.085, 0.135, 0.075, 0.065, 0.075, 0.075, 0.085, 0.065, 0.07],
             notes="Median, IQR and mean are pipes cleared on unseen levels (cap 149). Surv. is the fraction of the "
                   "30 test levels survived to truncation. E50 is the median number of evaluations to first reach 50 "
                   "validation pipes.")
    s.append(P(
        "The genetic algorithm beats random search decisively: a median of 91.3 against 9.5 pipes, a large effect "
        "(&delta;&nbsp;=&nbsp;&minus;0.90) that survives correction comfortably (p<sub>holm</sub>&nbsp;=&nbsp;0.001). "
        "Only 1 of 12 random-search runs ever reached 50 validation pipes, against 12 of 12 for every other method. "
        "Whatever else is true, the search is doing real work."))
    s.append(P(
        "The other two comparisons are the interesting ones, and both are null. The hill climber is numerically worse "
        "(median 61.7) and far more erratic (interquartile range 19.1&ndash;126.4, with three runs failing "
        "completely), but the difference does not approach significance "
        "(&delta;&nbsp;=&nbsp;&minus;0.26, p<sub>holm</sub>&nbsp;=&nbsp;0.597). Its advantage, when it works, is "
        "that it concentrates the entire budget on one lineage; its weakness is that it has no mechanism for escaping "
        "a bad start. The population appears to be buying <i>reliability</i> rather than peak performance, which is "
        "visible as the much higher AUC (65.7 against 26.3) but is not captured by the final-performance test."))
    s.append(P(
        "The two-gene comparison is more pointed. A genome with 21 times fewer parameters reaches a median of 84.2 "
        "pipes, statistically indistinguishable from the network "
        "(&delta;&nbsp;=&nbsp;&minus;0.22, p<sub>holm</sub>&nbsp;=&nbsp;0.597), and it gets there far faster: a median "
        "of 150 evaluations to reach 50 validation pipes, against 2,250 for the network, giving it much the highest "
        "AUC in the study (80.1). Exhaustive grid search over the same two parameters finds a rule scoring 90.8, "
        "essentially matching the network's 91.3. The network is not exploiting any structure that two well-chosen "
        "parameters do not already capture."))
    s.append(fig("landscape", "figures/fig_landscape.png",
                 "The two-gene fitness landscape, evaluated exhaustively on a grid, with one run's population "
                 "overlaid. Almost the entire initialisation box is flat and worthless (dark); competent behaviour "
                 "occupies a narrow diagonal ridge. The population migrates onto the ridge within a handful of "
                 "generations and then creeps along it. The landscape explains both why random search fails (the "
                 "ridge has tiny measure) and why a hill climber usually succeeds (once on the ridge, local "
                 "improvement suffices).", width=W * 0.56))
    s.append(P(
        "The two-gene landscape is worth dwelling on because it is the one part of this system we can visualise "
        "exhaustively. It is not deceptive and it is not multimodal; it is a single narrow ridge surrounded by a "
        "large flat plateau of zero fitness. That geometry is exactly the regime in which population-based "
        "recombination has least to offer and in which a hill climber, once it stumbles onto the ridge, does fine. "
        "We think this is the most likely explanation for the null results above, and we expect the 43-dimensional "
        "landscape to have a similar character."))

    # 6.3
    s.append(H2("6.3", "Operator choices"))
    s.append(P(
        "We now vary the operators one family at a time. The summary is quickly stated: <i>none</i> of the "
        "differences in " + T("operators") + " survives Holm correction."))
    s.append(fig("selection", "figures/fig_selection.png",
                 "Selection schemes. (a) Median validation curves. (b) Champion test performance. Higher tournament "
                 "pressure (<i>k</i> = 5) and roulette are numerically ahead of the default, linear ranking behind "
                 "it, but no difference is significant after correction."))
    s.append(P(
        "The selection result contradicts a prediction we had made in advance. Fitness-proportionate selection is "
        "conventionally expected to collapse diversity on a task like this, because shaped fitness grows roughly "
        "geometrically once agents start clearing pipes and a single early leader can capture most of the "
        "probability mass. It did not: roulette was numerically the second-best scheme (median 97.8) and its final "
        "diversity was indistinguishable from the default. The reason is visible in Eq.&nbsp;(4): aggregating by the "
        "minimum over three levels compresses the fitness range sharply, because every individual is scored by its "
        "worst level. An evaluation-protocol decision taken for an unrelated reason removed the pathology the "
        "selection scheme is usually blamed for."))
    s.append(fig("crossover", "figures/fig_crossover.png",
                 "Crossover operators. Disabling recombination entirely (leftmost) is numerically the best of the "
                 "four settings; arithmetic blending is the worst. No difference is significant."))
    s.append(P(
        "The crossover result is the clearest negative in the study. Removing recombination altogether &mdash; so "
        "that reproduction is mutation of a single selected parent &mdash; gave the highest median (98.6) and the "
        "highest survival rate (0.50) of the four settings. Uniform crossover, the default, was third. We are not in "
        "a position to claim that crossover <i>hurts</i>, since the differences are not significant, but the "
        "experiment provides no evidence that it helps, and a design that omits it is simpler and no worse."))
    s.append(P(
        "The likely explanation is the competing-conventions problem. Hidden units in a fixed-topology network are "
        "interchangeable: two parents can implement similar policies with permuted or sign-flipped hidden units, and "
        f"recombining their weight vectors then produces offspring that inherit incompatible halves. This is "
        f"precisely the difficulty that NEAT's historical markings were introduced to solve {C('neat')}, and our "
        "result is consistent with it mattering here. Arithmetic blending, which averages two such parents, is the "
        "worst performer of the four, which fits the same explanation."))
    s.append(fig("mutation", "figures/fig_mutation.png",
                 "Mutation. (a) Median test performance over a 5 &times; 4 grid of per-gene rate against step size "
                 "&sigma; (6 runs per cell; the default is outlined in white). Performance varies from 74 to 119 "
                 "pipes with no clean structure, and the default cell is not the best. (b) Gaussian mutation with a "
                 "constant &sigma;, with an annealed schedule, and uniform reset are indistinguishable."))
    s.append(P(
        "The mutation grid spans a factor of 20 in rate and 12 in step size, and the best cell (119 pipes at "
        "<i>r</i>&nbsp;=&nbsp;0.02, &sigma;&nbsp;=&nbsp;0.30) is about 60% better than the worst (74 at "
        "<i>r</i>&nbsp;=&nbsp;0.02, &sigma;&nbsp;=&nbsp;0.05). But with 6 runs per cell and this much run-to-run "
        "variance, the surface has no reliable structure: the same rate produces both the best and the worst cell. "
        "We report the grid rather than a tuned optimum, because selecting the best cell and reporting it as the "
        "recommended setting would be exactly the overfitting-to-noise this study is designed to expose. The annealed "
        "schedule, which we had predicted would win, did not (&delta;&nbsp;=&nbsp;0.02, p&nbsp;=&nbsp;0.95)."))
    s += tbl("operators",
             "Operator studies. All comparisons are against the baseline; p<sub>holm</sub> is corrected within each "
             "block. No entry is significant.",
             [["Condition", "Median", "IQR", "Surv.", "&delta;", "p", "p<sub>holm</sub>", "AUC"],
              ["<i>Selection</i>", "", "", "", "", "", "", ""],
              ["Tournament <i>k</i> = 2", "82.7", "70.3&ndash;97.8", "0.26", "&minus;0.31", "0.214", "0.643", "52.7"],
              ["Tournament <i>k</i> = 3 (default)", "91.3", "80.8&ndash;117.9", "0.40", "&mdash;", "&mdash;", "&mdash;", "65.7"],
              ["Tournament <i>k</i> = 5", "103.8", "91.2&ndash;117.8", "0.49", "0.28", "0.260", "0.643", "67.3"],
              ["Roulette", "97.8", "88.3&ndash;111.2", "0.42", "0.20", "0.419", "0.643", "70.2"],
              ["Linear rank", "79.2", "69.7&ndash;88.8", "0.16", "&minus;0.40", "0.100", "0.400", "50.2"],
              ["<i>Crossover</i>", "", "", "", "", "", "", ""],
              ["None (mutation only)", "98.6", "80.6&ndash;136.9", "0.50", "0.13", "0.623", "1.000", "75.6"],
              ["Single-point", "95.3", "81.2&ndash;122.4", "0.43", "0.05", "0.862", "1.000", "73.6"],
              ["Uniform (default)", "91.3", "80.8&ndash;117.9", "0.40", "&mdash;", "&mdash;", "&mdash;", "65.7"],
              ["Arithmetic", "78.9", "72.0&ndash;86.2", "0.21", "&minus;0.35", "0.157", "0.472", "58.9"],
              ["<i>Mutation</i>", "", "", "", "", "", "", ""],
              ["Gaussian, constant &sigma; (default)", "91.3", "80.8&ndash;117.9", "0.40", "&mdash;", "&mdash;", "&mdash;", "65.7"],
              ["Gaussian, annealed &sigma;", "102.2", "80.8&ndash;112.7", "0.38", "0.02", "0.954", "1.000", "65.8"],
              ["Uniform reset", "105.8", "70.3&ndash;114.5", "0.40", "0.01", "0.977", "1.000", "63.0"]],
             [0.29, 0.09, 0.155, 0.075, 0.085, 0.08, 0.10, 0.075])
    s.append(fig("popelite", "figures/fig_popelite.png",
                 "(a) Population size at equal evaluation budget: smaller populations run for more generations and "
                 "are numerically better, but the trend is not significant. (b) Number of elites. Removing elitism "
                 "entirely is the worst setting (median 76.1 against 91.3), consistent with theory, but again not "
                 "significant at this sample size."))
    s.append(P(
        "Population size and elitism (" + T("popelite") + ") show the largest uncorrected trends in the operator "
        "studies. Small populations run for many generations beat large populations run for few at the same budget "
        "(median 105.2 at <i>N</i>&nbsp;=&nbsp;20 against 78.8 at <i>N</i>&nbsp;=&nbsp;200), and removing elitism "
        "costs about 15 median pipes. Both effects point in the direction theory predicts, and both fail to reach "
        "significance after correction (p<sub>holm</sub>&nbsp;=&nbsp;0.207 and 0.242). We record them as suggestive."))
    s += tbl("popelite",
             "Population size at equal budget, and elitism. Comparisons against the baseline (<i>N</i> = 50, "
             "<i>e</i> = 2); Holm correction within each block.",
             [["Condition", "Median", "IQR", "Surv.", "&delta;", "p", "p<sub>holm</sub>", "AUC", "E50"],
              ["<i>N</i> = 20 (250 generations)", "105.2", "86.6&ndash;138.2", "0.50", "0.23", "0.356", "0.356", "65.5", "1,560"],
              ["<i>N</i> = 50 (100 generations)", "91.3", "80.8&ndash;117.9", "0.40", "&mdash;", "&mdash;", "&mdash;", "65.7", "2,250"],
              ["<i>N</i> = 100 (50 generations)", "74.8", "63.2&ndash;87.2", "0.21", "&minus;0.44", "0.069", "0.207", "49.5", "3,900"],
              ["<i>N</i> = 200 (25 generations)", "78.8", "64.1&ndash;87.8", "0.18", "&minus;0.39", "0.112", "0.225", "34.3", "7,200"],
              ["<i>e</i> = 0 (no elitism)", "76.1", "64.8&ndash;88.8", "0.17", "&minus;0.46", "0.061", "0.242", "45.1", "4,500"],
              ["<i>e</i> = 1", "86.9", "71.0&ndash;97.5", "0.33", "&minus;0.17", "0.488", "1.000", "64.8", "3,150"],
              ["<i>e</i> = 2 (default)", "91.3", "80.8&ndash;117.9", "0.40", "&mdash;", "&mdash;", "&mdash;", "65.7", "2,250"],
              ["<i>e</i> = 5", "95.7", "88.5&ndash;121.7", "0.42", "0.17", "0.507", "1.000", "69.3", "2,250"],
              ["<i>e</i> = 10", "92.6", "78.7&ndash;126.7", "0.43", "&minus;0.01", "0.977", "1.000", "79.0", "2,250"]],
             [0.26, 0.085, 0.145, 0.07, 0.08, 0.075, 0.095, 0.07, 0.07])

    # 6.4
    s.append(H2("6.4", "Fitness design and evaluation noise"))
    s.append(P(
        "Fitness shaping is conventionally presented as important, and our own design document predicted that the "
        "proximity term would substantially accelerate early progress. It did not "
        "(&delta;&nbsp;=&nbsp;0.04, p&nbsp;=&nbsp;0.885). More strikingly, the two unshaped variants &mdash; frames "
        "survived alone, and the weighted combination of pipes and frames &mdash; produced numerically identical "
        "results to three decimal places across all 12 runs. This is not a coincidence or a bug: as noted in "
        f"{S('3.3')}, pipes cleared is a deterministic monotone function of frames survived in a constant-scroll "
        "game, so the two objectives induce identical orderings and therefore identical selection decisions and "
        "identical runs. The lesson generalises: before tuning the weights of a composite fitness function, check "
        "whether its terms are rank-equivalent."))
    s.append(fig("noise", "figures/fig_noise.png",
                 "(a) Fitness function. The three variants are indistinguishable; the first two are provably "
                 "rank-equivalent and produce identical runs. (b) Evaluation protocol: number of levels per "
                 "evaluation and aggregation rule, all at equal budget. (c) Generalisation. Orange points are the "
                 "champion's score on the training levels it was selected on; blue points are the same champions on "
                 "30 unseen levels. Training on a single level yields a perfect 149 on that level and 54 on unseen "
                 "ones."))
    s.append(P(
        "The evaluation-protocol comparison in panel (b) is also null. Evaluating on one level for 300 generations, "
        "on three for 100, or on five for 60 gave medians of 87.7, 91.3 and 92.6; aggregating by mean rather than "
        "minimum gave 101.7. None of these differences is significant. Note that this is a statement about the "
        "<i>aggregation</i> decision at a fixed training pool, not about the pool itself, which is the subject of the "
        "next section and behaves very differently."))

    # 6.5
    s.append(H2("6.5", "Generalisation: the effect that mattered most"))
    s.append(P(
        "Holding the budget fixed, we varied only the number of distinct levels available for selection. This "
        "produced the largest and most reliable effect in the study."))
    s.append(P(
        "With a pool of one level, champions achieved a mean of <b>149.0</b> pipes on that level &mdash; a perfect "
        "score against the truncation cap, on every run &mdash; and a median of <b>54.2</b> on unseen levels. The "
        "generalisation gap is roughly 95 pipes. Widening the pool closes it monotonically from the training side "
        "rather than the test side: with 3 levels the champion scores 146.9 on training and 82.5 on test; with 10, "
        "104.3 and 91.3; with 100, 97.8 and 87.7. In other words, the apparent performance falls as the pool widens "
        "while real performance rises, which is precisely the signature of memorisation being squeezed out. The "
        "comparison of a single level against the default is large and clearly significant "
        "(&delta;&nbsp;=&nbsp;&minus;0.89, p<sub>holm</sub>&nbsp;=&nbsp;0.001); most of the benefit is captured by "
        "the tenth level, with a pool of 100 no better than a pool of 10."))
    s += tbl("protocol",
             "Fitness design, evaluation protocol and training-pool size, all at equal budget. Train is the "
             "champion's mean score on the levels it was selected on; Test is its mean over 30 unseen levels.",
             [["Condition", "Train", "Test median", "IQR", "Surv.", "&delta;", "p", "p<sub>holm</sub>"],
              ["<i>Fitness function</i>", "", "", "", "", "", "", ""],
              ["Frames survived only", "&mdash;", "94.6", "81.1&ndash;129.2", "0.44", "0.04", "0.885", "1.000"],
              ["1000&middot;pipes + frames", "&mdash;", "94.6", "81.1&ndash;129.2", "0.44", "0.04", "0.885", "1.000"],
              ["Shaped, Eq. 3 (default)", "&mdash;", "91.3", "80.8&ndash;117.9", "0.40", "&mdash;", "&mdash;", "&mdash;"],
              ["<i>Evaluation protocol</i>", "", "", "", "", "", "", ""],
              ["<i>K</i> = 1 (300 generations)", "&mdash;", "87.7", "72.9&ndash;100.0", "0.25", "&minus;0.24", "0.341", "1.000"],
              ["<i>K</i> = 3, aggregate by mean", "&mdash;", "101.7", "93.1&ndash;125.0", "0.48", "0.20", "0.419", "1.000"],
              ["<i>K</i> = 3, aggregate by min (default)", "&mdash;", "91.3", "80.8&ndash;117.9", "0.40", "&mdash;", "&mdash;", "&mdash;"],
              ["<i>K</i> = 5 (60 generations)", "&mdash;", "92.6", "74.5&ndash;114.2", "0.38", "&minus;0.04", "0.885", "1.000"],
              ["<i>Training-pool size</i>", "", "", "", "", "", "", ""],
              ["1 level", "<b>149.0</b>", "<b>54.2</b>", "37.9&ndash;66.1", "0.06", "&minus;0.89", "&lt;0.001", "<b>0.001</b>"],
              ["3 levels", "146.9", "82.5", "69.6&ndash;94.7", "0.20", "&minus;0.39", "0.112", "0.225"],
              ["10 levels (default)", "104.3", "91.3", "80.8&ndash;117.9", "0.40", "&mdash;", "&mdash;", "&mdash;"],
              ["100 levels", "97.8", "87.7", "75.7&ndash;111.8", "0.40", "&minus;0.04", "0.885", "0.885"]],
             [0.30, 0.075, 0.105, 0.135, 0.075, 0.08, 0.085, 0.095])

    # 6.6
    s.append(H2("6.6", "Diversity collapse and its remedies"))
    s.append(P(
        "Because the default configuration never loses diversity, studying premature convergence required inducing "
        "it. We used a deliberately greedy configuration: population 30, tournament <i>k</i>&nbsp;=&nbsp;7, 10 "
        "elites, mutation rate 0.01 and &sigma;&nbsp;=&nbsp;0.1. This reliably produces the textbook pathology. "
        "Genome diversity falls from 5.34 to <b>0.12</b>, a factor of 43 below the initial value and a factor of 26 "
        "below the baseline's steady state, and median test performance falls to 25.2 pipes with 7 of 12 runs never "
        "reaching 50 validation pipes at all."))
    s.append(fig("diversity", "figures/fig_diversity.png",
                 "Induced premature convergence and two standard remedies, at equal budget. (a) Genome diversity on "
                 "a logarithmic scale. The greedy configuration (orange) collapses; random immigrants (green) hold "
                 "diversity high by construction; fitness sharing (blue) collapses almost as far as the control. "
                 "(b) Validation performance. (c) Champion test performance for all seven conditions. Fitness "
                 "sharing with <i>r</i> = 3 is the only remedy that significantly beats the collapsed control."))
    s += tbl("diversity",
             "Remedies for induced premature convergence. All comparisons are against the collapsed control; Holm "
             "correction within the table. <i>D</i><sub>final</sub> is mean final genome diversity.",
             [["Condition", "Median", "IQR", "<i>D</i><sub>final</sub>", "Reach 50", "&delta;", "p", "p<sub>holm</sub>"],
              ["Greedy control (no remedy)", "25.2", "1.1&ndash;50.6", "0.12", "0.42", "&mdash;", "&mdash;", "&mdash;"],
              ["Fitness sharing, <i>r</i> = 1", "63.6", "30.4&ndash;79.3", "0.14", "0.75", "0.38", "0.126", "0.378"],
              ["Fitness sharing, <i>r</i> = 2", "56.1", "39.2&ndash;63.9", "0.16", "0.75", "0.53", "0.030", "0.122"],
              ["Fitness sharing, <i>r</i> = 3", "<b>80.6</b>", "56.7&ndash;86.8", "0.17", "0.92", "<b>0.71</b>", "0.004", "<b>0.021</b>"],
              ["Fitness sharing, <i>r</i> = 4", "60.9", "53.0&ndash;68.5", "0.19", "0.92", "0.63", "0.010", "0.051"],
              ["Random immigrants, 10%", "29.1", "9.5&ndash;68.3", "1.13", "0.50", "0.18", "0.470", "0.470"],
              ["Random immigrants, 20%", "51.3", "6.1&ndash;73.5", "1.99", "0.67", "0.32", "0.194", "0.388"],
              ["<i>Baseline configuration, for reference</i>", "<i>91.3</i>", "<i>80.8&ndash;117.9</i>", "<i>3.08</i>", "<i>1.00</i>", "&mdash;", "&mdash;", "&mdash;"]],
             [0.30, 0.08, 0.135, 0.09, 0.085, 0.075, 0.075, 0.095])
    s.append(P(
        "Fitness sharing with <i>r</i>&nbsp;=&nbsp;3 more than triples median performance, from 25.2 to 80.6 pipes, "
        "and raises the fraction of runs that reach 50 validation pipes from 0.42 to 0.92 "
        "(&delta;&nbsp;=&nbsp;0.71, p<sub>holm</sub>&nbsp;=&nbsp;0.021). Random immigrants did not significantly help "
        "at either rate tested."))
    s.append(P(
        "The mechanism is not what the diversity metric suggests, and this is the most interesting detail in the "
        "section. Random immigrants raise measured diversity by an order of magnitude (from 0.12 to 1.13) and yet "
        "recover almost no performance, because the injected genomes are uniformly random, are immediately "
        "eliminated by a tournament of size 7, and contribute nothing but a persistently high distance statistic. "
        "Fitness sharing leaves measured diversity almost unchanged (0.17) while recovering most of the lost "
        "performance, because it redistributes selection pressure among the <i>useful</i> variants that already "
        "exist. Genome-space distance is therefore a poor proxy for the kind of diversity that matters, and a paper "
        "reporting only the diversity curve would have drawn the opposite conclusion from the one the performance "
        "data supports."))

    # 6.7
    s.append(H2("6.7", "Task difficulty as a confound"))
    s.append(P(
        "Our initial environment used gap centres drawn from U(200,&nbsp;400). We report it here because discovering "
        "that it was unusable was itself a useful result. In that environment, exhaustive grid search over the "
        "two-parameter rule finds settings that clear 142.2 of a capped 149 pipes and survive 90% of test levels. "
        "Every method we tried saturates: the baseline genetic algorithm reaches a median of 141.8, the two-gene "
        "genetic algorithm 146.4, and even the hill climber 143.4."))
    s += tbl("easy",
             "The standard environment (gap centres ~ U(200, 400)), which is too easy to discriminate between "
             "methods. Compare with " + T("methods") + ", which reports the same methods in the hard environment.",
             [["Method", "Median", "IQR", "Surv.", "Robust", "&delta;", "p<sub>holm</sub>"],
              ["GA, 43-gene network", "141.8", "135.0&ndash;145.9", "0.85", "0.08", "&mdash;", "&mdash;"],
              ["GA, 2-gene rule", "146.4", "142.4&ndash;149.0", "0.95", "0.33", "0.42", "0.327"],
              ["(1+1) hill climber", "143.4", "126.2&ndash;144.6", "0.73", "0.08", "&minus;0.05", "1.000"],
              ["Random search", "43.6", "3.5&ndash;140.1", "0.36", "0.08", "&minus;0.55", "0.122"],
              ["Roulette selection", "132.0", "127.6&ndash;145.9", "0.82", "&minus;0.24", "1.000", "&mdash;"],
              ["No crossover", "139.7", "136.8&ndash;145.9", "0.85", "0.00", "1.000", "&mdash;"],
              ["Hand-tuned 2-gene rule", "142.2", "&mdash;", "0.90", "&mdash;", "&mdash;", "&mdash;"]],
             [0.30, 0.10, 0.17, 0.09, 0.09, 0.115, 0.135],
             notes="Robust is the fraction of runs whose champion survives all 30 test levels.")
    s.append(P(
        "In this environment the two-gene rule is numerically the <i>best</i> method and is the only one with a "
        "non-trivial robustness rate (0.33). Random search is the sole method that separates from the rest, and even "
        "it clears a median of 43.6 pipes. A study conducted only here would have concluded that all reasonable "
        "methods are equivalent, which is true but uninformative, and it would have had no power to detect the "
        "generalisation and diversity effects that " + S("6.5") + " and " + S("6.6") + " identify. Checking that a "
        "hand-written baseline does <i>not</i> already solve the task is a cheap and, in our experience, easily "
        "skipped precondition for any empirical comparison."))
    return s


# ------------------------------------------------------------------ 7
def sec7():
    s = [H1("7", "Discussion")]
    s.append(H3("What the null results do and do not mean."))
    s.append(P(
        "Fourteen of the seventeen comparisons we ran returned no significant difference. The honest reading is not "
        "that selection schemes and crossover operators are interchangeable in general, but that on this task, at "
        "this budget, their effect is smaller than the run-to-run variance of the algorithm itself. That variance is "
        "large: the baseline's interquartile range spans 80.8 to 117.9 pipes, so any effect smaller than roughly 30 "
        "pipes is invisible at <i>n</i>&nbsp;=&nbsp;12. An operator comparison run once per configuration &mdash; "
        "the norm in coursework and not unknown in published work &mdash; would have produced a confident ranking "
        "from this data, and that ranking would have been noise."))
    s.append(H3("Where the leverage actually was."))
    s.append(P(
        "The three effects that did survive correction were a search-versus-no-search comparison "
        "(&delta;&nbsp;=&nbsp;&minus;0.90), a training-set-size effect (&delta;&nbsp;=&nbsp;&minus;0.89) and a "
        "diversity-maintenance effect under a configuration chosen to need it (&delta;&nbsp;=&nbsp;0.71). Two of "
        "those three are properties of the <i>experimental protocol</i> rather than of the algorithm. This inverts "
        "the usual emphasis, in which the protocol is described in a short paragraph and the operators occupy the "
        "bulk of the analysis."))
    s.append(H3("Why the landscape explains the nulls."))
    s.append(P(
        "The two-gene visualisation in " + F("landscape") + " offers a concrete mechanism. The landscape is a single "
        "narrow ridge in a large flat plateau: unimodal, non-deceptive, and low-dimensional in its effective "
        "structure. Recombination helps most when useful building blocks are distributed across different "
        "individuals and can be combined; a single ridge offers no such blocks. A hill climber that reaches the "
        "ridge will follow it, which is why it matches the population method on median performance while being far "
        "less reliable about arriving there at all. We would expect the operator comparisons to become discriminative "
        "on a task with genuine multimodality, and we regard demonstrating that as the natural follow-up."));
    s.append(H3("Parameter count."))
    s.append(P(
        "That a two-parameter rule matches a 43-parameter network is consistent with a broader pattern: on control "
        f"benchmarks whose solutions are simple, elaborate policy classes often confer no advantage {C('mania')}. "
        "The practical implication for a project of this kind is to implement the trivial parameterisation first, "
        "not merely as a debugging aid but as the baseline the elaborate method must beat. The same logic applies "
        f"to the optimiser: a self-adaptive evolution strategy such as CMA-ES {C('hansen')} would be a more "
        "demanding comparison than the hill climber we used, and we did not run one."))
    s.append(H3("A note on shaping and rank equivalence."))
    s.append(P(
        "The discovery that our two unshaped fitness functions were provably identical under selection was "
        "accidental, arising from noticing that 12 pairs of runs matched to three decimal places. It is a reminder "
        "that a composite objective should be checked for rank equivalence among its terms before its weights are "
        "tuned, since selection operators see only the induced ordering."))
    return s


# ------------------------------------------------------------------ 8
def sec8():
    s = [H1("8", "Limitations")]
    s += numbered([
        "<b>Statistical power.</b> Twelve runs per configuration (six for the mutation grid) detect large effects "
        "reliably and small ones not at all. Several operator comparisons had uncorrected p-values between 0.06 and "
        "0.12 and might well be real; our null results are failures to reject, not demonstrations of equivalence. We "
        "did not conduct a formal power analysis.",
        "<b>A single task.</b> All conclusions concern one game with one genome encoding. The ridge-like landscape we "
        "identify is plausibly the reason recombination did not help, which implies the result should not be "
        "generalised to multimodal or deceptive problems.",
        "<b>Fixed topology.</b> We evolved weights only. Methods that evolve structure, most obviously NEAT, address "
        "the competing-conventions problem we invoke to explain the crossover result, and testing that explanation "
        "directly would require implementing them.",
        "<b>One budget.</b> Everything is measured at 15,000 evaluations. Operator differences may well emerge at "
        "budgets one or two orders of magnitude larger, where the algorithm is refining rather than finding a "
        "solution.",
        "<b>Hand-tuned baseline strength.</b> Our two-gene rule was optimised by exhaustive grid search over the same "
        "training levels, giving it a favourable comparison. A weaker hand-designed baseline would have flattered the "
        "evolved networks.",
        "<b>Truncation cap.</b> Capping episodes at 10,000 frames bounds the primary metric at 149 and compresses "
        "differences between strong configurations, particularly in the standard environment where most methods "
        "approach the cap.",
    ])
    return s


# ------------------------------------------------------------------ 9
def sec9():
    s = [H1("9", "Conclusion")]
    s.append(P(
        "We evolved neural controllers for Flappy&nbsp;Bird with a genetic algorithm and used the task to ask which "
        "design decisions actually change the outcome. Across 606 budget-matched runs and 60 configurations, "
        "evaluated with non-parametric tests and correction for multiple comparisons, the answer was consistent and "
        "somewhat deflating for the usual emphasis of the field."))
    s.append(P(
        "Search beats no search by a wide margin. Beyond that, neither the population, nor recombination, nor the "
        "choice of selection scheme, nor a twenty-fold range of mutation rates produced a difference that survived "
        "correction; and a hand-designed two-parameter rule matched a 43-parameter network while learning fifteen "
        "times faster. What did matter was how many levels the algorithm was allowed to select on &mdash; one level "
        "produced a champion that scored perfectly on it and lost 40% of its performance elsewhere &mdash; and, once "
        "a greedy configuration had destroyed diversity, whether selection pressure was redistributed among the "
        "surviving variants. We also found that an environment we initially considered reasonable was already solved "
        "by a two-parameter rule, and therefore could not have discriminated between any of these conditions."))
    s.append(P(
        "The practical recommendations follow directly. Implement the trivial baseline and check that it does not "
        "already solve the task. Match budgets in evaluations rather than generations. Separate the instances used "
        "for selection from those used for reporting, and use enough of the former. Run every configuration many "
        "times and correct for multiple comparisons. Treat a diversity statistic as a diagnostic rather than an "
        "objective. Spend the effort saved on the protocol rather than on operator tuning."))
    s.append(P(
        "The simulator, the algorithm, all 606 run logs and the scripts that produce every figure and table in this "
        "paper are released so that each number above can be regenerated from scratch."))
    return s


def back():
    from paperlib import reference_list
    s = [H1("", "References")]
    refs, uncited = reference_list()
    s += refs
    return s, uncited

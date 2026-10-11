---
updated: 2026-10-11
status: draft
key_papers:
  - key: judson1992teaching
    note: Proposes learning control. A closed loop between experiment and an evolutionary algorithm finds laser pulses without a model.
  - key: nelder1965simplex
    note: The Nelder–Mead simplex method, the direct-search workhorse of CRAB and of many closed-loop experiments.
  - key: hansen2001cmaes
    note: CMA-ES, a robust evolution strategy that adapts its search distribution; well suited to noisy, rugged objectives.
  - key: zahedinejad2014evolutionary
    note: Shows greedy, local optimization getting trapped on fast gates (a qutrit phase gate, a CNOT) and an evolutionary algorithm succeeding.
software:
  - name: pycma
    url: https://github.com/CMA-ES/pycma
    note: reference Python implementation of CMA-ES
  - name: NLopt
    url: https://github.com/stevengj/nlopt
    note: library of local and global derivative-free optimizers
  - name: QuOCS
    url: https://github.com/Quantum-OCS/QuOCS
    note: dCRAB with Nelder–Mead or CMA-ES, for simulations and experiments
---

**Gradient-free optimizers** need only the *value* of the figure of merit, never its derivative. They are the
natural choice when gradients are unavailable or unreliable. Examples: the fidelity is measured on an experiment
and is noisy, the simulation is a black box, or the objective is not differentiable. They are also useful when the
landscape is rugged enough that local gradient methods get stuck. The price is poor scaling with the number of
parameters, so they are usually combined with a compact pulse description such as [[crab|CRAB]].

## The main families

- **Direct search — Nelder–Mead.** A simplex of $n+1$ points in parameter space is reflected, expanded and
  contracted towards better values [@nelder1965simplex]. Simple, with few settings, and effective for up to a few tens
  of parameters. It is the classic partner of [[crab|CRAB]] [@caneva2011crab].
- **Evolution strategies — CMA-ES.** Candidates are sampled from a multivariate Gaussian whose mean and covariance
  matrix adapt to the landscape [@hansen2001cmaes]. CMA-ES learns correlations between parameters and copes well with
  noise and rugged landscapes.
- **Genetic and evolutionary algorithms.** Populations of pulses are recombined and mutated. They were used in the
  first proposal of *learning control*, in which an algorithm drives a laser experiment directly
  [@judson1992teaching]. For fast gates where greedy algorithms are trapped — a qutrit phase gate and a CNOT — an
  evolutionary algorithm has been shown to succeed [@zahedinejad2014evolutionary].
- **Surrogate-based optimization.** Bayesian optimization and other machine-learning surrogates build a model of the
  landscape from few, expensive evaluations, for example to optimize ultracold-atom experiments online
  [@wigley2016fast]; see [[machine-learning-control]].

## Where they shine

- **Closed-loop experiments.** Optimizing directly on the device sidesteps model errors. Examples include tuning
  superconducting-qubit gates with randomized-benchmarking fidelities as the objective [@kelly2014orbit], and
  refining model-based optimal pulses in the laboratory (ad-HOC) [@egger2014adhoc]. See [[closed-loop]].
- **Black-box simulations** whose gradients are unavailable, for example tensor-network or mean-field dynamics in
  [[many-body-control]].
- **Global exploration.** Population methods can escape local optima that trap greedy methods. Even human
  intuition, collected through a citizen-science game, has been used to seed optimizers in such landscapes
  [@sorensen2016speedlimit].

## Limitations

- The number of evaluations needed grows quickly with the number of parameters, so the pulse description must stay
  compact (a few to a few dozen parameters).
- With cheap exact gradients, gradient-based methods ([[grape|GRAPE]], [[goat|GOAT]] with
  [[second-order-methods|L-BFGS]]) almost always converge in far fewer evaluations.
- "Global" methods such as genetic algorithms or CMA-ES explore more widely, but give no guarantee of finding the global
  optimum. For a certified global optimum, see [[polynomial-optimization|QCPOP]].

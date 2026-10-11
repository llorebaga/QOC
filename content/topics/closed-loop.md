---
updated: 2026-10-11
status: draft
key_papers:
  - key: judson1992teaching
    note: Proposes learning control. Let an algorithm "teach" the laser by optimizing directly on the experiment, without a model.
  - key: egger2014adhoc
    note: Ad-HOC. Optimize on a model first, then refine on the device with a gradient-free method, combining the strengths of both.
  - key: kelly2014orbit
    note: Closed-loop gate tuning on superconducting qubits with randomized benchmarking as the objective.
  - key: li2017hybrid
    note: A hybrid scheme in which the quantum device itself evaluates the fidelity and its gradient for a classical optimizer.
  - key: sauvage2020poor
    note: Bayesian optimization that finds optimal controls even with large shot noise, down to single-shot measurements.
software:
  - name: QuOCS
    url: https://github.com/Quantum-OCS/QuOCS
    note: optimal control suite designed to talk to experiments (dCRAB, Nelder–Mead, CMA-ES, gradients)
  - name: C3
    url: https://github.com/q-optimize/c3
    note: integrates open-loop optimization, closed-loop calibration and model learning
---

Even the best model of a quantum device is imperfect. Unknown couplings, pulse distortions and drifting parameters make
pulses optimized on a computer underperform on hardware. **Closed-loop** (or *in situ*) optimization removes the model
from the loop. An optimizer proposes a control, the **experiment** measures how well it works, and the result guides
the next proposal. Introduced in chemistry as *learning control* [@judson1992teaching], it is now routine for calibrating
gates in quantum processors.

## The loop

1. Propose controls $u$ (often in a compact parametrization — a few amplitudes, phases, or [[crab|CRAB]]
   coefficients).
2. Run the experiment and estimate a figure of merit $\hat J(u)$ — a state population, a randomized-benchmarking
   fidelity, a sensing signal.
3. Update $u$ with an optimizer that tolerates noisy estimates, and repeat.

The figure of merit is noisy, since every estimate comes from finitely many shots, and expensive, since every
evaluation costs experimental time. This shapes the choice of optimizer and of objective.

## Gradient-free closed loops

The classic choice is a [[gradient-free|gradient-free]] method: genetic algorithms, Nelder–Mead or CMA-ES.

- **Chemistry.** Feedback-optimized, phase-shaped femtosecond pulses steered the branching ratio of chemical reactions
  [@assion1998chemical]; see [[molecules]].
- **Superconducting qubits.** Nelder–Mead with randomized benchmarking as the objective tunes single- and two-qubit gates
  and identifies crosstalk [@kelly2014orbit]. "Restless" measurements, which skip the wait for qubit relaxation,
  speed up the tune-up tenfold, reaching 0.999 average Clifford fidelity in about a minute [@rol2017restless].
  Optimizing every sample of the waveform in closed loop produced a 4.16 ns gate with 0.044 % leakage
  [@werninghaus2021leakage].
- **Spins and atoms.** Autonomous closed-loop calibration of NV-centre spin operations [@frank2017autonomous], online
  optimization of ultracold-atom experiments with machine-learning surrogates [@wigley2016fast], and remote
  optimization involving citizen scientists [@heck2018remote].

## Hybrid: model first, device second

Pure closed-loop optimization from scratch is slow. **Ad-HOC** first optimizes on a model with gradients, then refines
the near-optimal pulse on the device with a gradient-free search. In typical solid-state settings this improved gate
fidelities by an order of magnitude [@egger2014adhoc]. Starting from a good model-based guess, and optimizing only the
few parameters that matter, is the most common practical strategy.

## Gradients from the device

Gradients can also be measured. In a hybrid quantum–classical scheme, the quantum system evaluates the fitness and its
gradient while a classical computer updates the controls. This was demonstrated on a seven-qubit NMR processor
[@li2017hybrid]. Measured gradients (and finite differences) have been compared with open-loop optimization in a
solid-state two-qubit system [@feng2018closedloop]. A 12-qubit processor has been used to optimize its own control
sequence with measurement-based feedback, correcting unknown imperfections [@lu2017bootstrapping]. More generally, a
quantum simulator can learn its own gates in situ. This avoids both an accurate model and a classical computer more
powerful than the simulator, with evidence of polynomial scaling up to nine qubits [@dive2018insitu].

## Coping with noisy, expensive evaluations

- **Stochastic optimization.** Algorithms built on direct fidelity estimation need only a constant number of
  experiments per iteration, independent of the number of control parameters. They are robust to statistical and
  technical noise [@ferrie2015insitu].
- **Bayesian optimization** builds a surrogate model of the landscape and chooses the most informative next
  experiment. It finds optimal controls even with very few shots per setting, down to single-shot measurements
  [@sauvage2020poor]; see [[machine-learning-control]].
- **Cheap, sensitive objectives.** Randomized benchmarking, restless measurements and error-amplifying sequences make
  each evaluation fast and sensitive to small errors.

## Closed loop versus model learning

Closed-loop optimization treats the device as a black box. The alternative is to *learn* a better model from data and
optimize on it ([[model-learning]]). The two combine naturally: identify, optimize, verify, refine
[@wittler2021c3]. Re-optimizing continuously over a short horizon leads to model-predictive control
([[lyapunov-control]]).

## Strengths and limitations

**Strengths**

- Accounts for everything the model misses: distortions, crosstalk, unknown couplings.
- Simple to set up on top of existing calibration routines.

**Limitations**

- Every evaluation costs experimental time, and shot noise limits precision.
- Scales poorly with the number of parameters unless gradients or surrogate models are used.
- Results are specific to the device and can drift, so periodic re-calibration is needed.

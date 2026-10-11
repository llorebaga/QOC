---
updated: 2026-10-12
status: draft
key_papers:
  - key: koch2016open
    note: Review of optimal control for open quantum systems — tools, achievements, and the limits set by decoherence.
  - key: schulteherbruggen2011dissipative
    note: Gate optimization that exploits known relaxation rates, and when it beats simply going as fast as possible.
  - key: goerz2014dissipative
    note: Optimizing a gate in an open system needs only three propagated states, independent of the Hilbert-space dimension.
  - key: reich2015nonmarkovianity
    note: Non-Markovian back-flow of amplitude and phase can be exploited to perform control tasks impossible in Markovian settings.
  - key: breuer2016nonmarkovian
    note: The standard colloquium on non-Markovian open-system dynamics.
software:
  - name: Quandary
    url: https://github.com/llnl/quandary
    note: high-performance optimal control of open quantum systems (C++, MPI)
  - name: krotov / Krotov.jl
    url: https://github.com/qucontrol/krotov
    note: Krotov's method for Lindblad dynamics
---

No quantum system is perfectly isolated. Coupling to an environment causes **decoherence and dissipation**: loss of
phase information, relaxation of populations and leakage of entanglement. **Open-system control** asks how to
reach targets despite this, and sometimes *because* of it. It also changes what control can do. Hamiltonian controls
alone can never purify a mixed state, while engineered dissipation and measurement can.

## Dynamics

For weak, memoryless coupling the density matrix obeys a master equation of Gorini–Kossakowski–Sudarshan–Lindblad
(GKSL) form [@gorini1976semigroups; @lindblad1976generators],

$$\dot\rho = -\frac{i}{\hbar}\big[H(t), \rho\big] + \sum_k \gamma_k\Big(L_k\rho L_k^\dagger - \tfrac12\big\{L_k^\dagger L_k, \rho\big\}\Big),$$

with jump operators $L_k$ and rates $\gamma_k$. When the environment has memory, the dynamics is **non-Markovian**:
information flows back from the environment, and time-local Lindblad forms no longer suffice
[@breuer2016nonmarkovian].

## Optimal control with dissipation

- **Fighting decoherence.** Optimal control finds pulses that complete a task before decoherence takes over, or that
  steer through weakly decaying subspaces. When the relaxation rates are known, exploiting them can beat simply
  minimizing time [@schulteherbruggen2011dissipative]. Robust gates for interacting qubits have been optimized in both
  Markovian and non-Markovian environments [@floether2012robust].
- **Numerics in Liouville space.** Density matrices have $d^2$ entries and superoperators act on them, so open-system
  control is expensive. For gates, three well-chosen states suffice instead of a full Liouville-space basis
  [@goerz2014dissipative]. Quantum trajectories with automatic differentiation reduce cost further
  [@abdelhafez2019trajectories]. Distributed-memory codes target larger open systems [@gunther2021quandary]. See
  [[propagation-methods]] and [[problem-formulation]].
- **Time-optimal control with relaxation.** Even a single dissipative spin has optimal solutions with singular arcs,
  realized experimentally in NMR [@lapert2010singular]; see [[geometric-control]].

## Using the environment

Dissipation is not only an enemy:

- **Cooling and reset.** Optimal control of relaxing systems can speed up or slow down their approach to the steady
  state [@mukherjee2013relaxation]. It has also been used to design laser cooling of internal molecular degrees of
  freedom [@bartana1997cooling]. For qubit reset under non-Markovian dynamics, initial system–environment correlations
  allow faster reset and smaller errors [@basilewitsch2017correlations].
- **Non-Markovian back-flow.** Amplitude and phase returning from the environment can be exploited to perform control
  tasks that would be impossible with a memoryless bath [@reich2015nonmarkovianity].
- **Incoherent control.** A suitably prepared, time-dependent environment can itself be the control that steers a
  system to its target [@pechen2006environment].
- **Engineered dissipation.** Designing the coupling to an environment so that the target is the steady state is the
  subject of [[reservoir-engineering]].

## Limits

Controllability notions change for open systems [@altafini2012modeling]; see [[controllability]]. Speed limits must be
generalized to non-unitary dynamics; see [[quantum-speed-limits]]. A review of the tools, achievements and
limitations of open-system optimal control is [@koch2016open]. Measurement adds another resource, real-time
information; see [[feedback-control]].

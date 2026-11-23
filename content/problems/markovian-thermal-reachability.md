---
title: Reachable states of controlled Markovian systems coupled to a thermal bath
question: >-
  Given an $n$-level quantum system ($n \ge 3$) with full unitary control and switchable Markovian coupling to a
  thermal bath at finite temperature $0 < T < \infty$, what is an exact, verifiable characterization of the set of
  reachable density matrices — including states with coherence?
status: partial
topics: [open-system-control, controllability, quantum-thermodynamics]
posed_by:
  - key: koch2022roadmap
    where: Section 2.2.2 and Section 2.3. Generalizing reachability results for open systems coupled to a finite-temperature
      bath from diagonal toy models ($d$-majorization) to general quantum states ($D$-majorization and Markovian
      Lie-semigroup orbits) is stated as a key open goal.
  - key: vomende2020dmajorization
    where: Section 1, Section 3.1 and Section 4 (arXiv:2003.04164v5). Characterizing the reachable set for
      $0 < T < \infty$, finding simple verifiable conditions for $D$-majorization in $n \ge 3$, and extending
      Markovian thermal reachability beyond diagonal states are posed as open problems.
  - key: lostaglio2022continuous
    where: Section II.B and Section IX. Having solved Markovian thermal reachability for diagonal (energy-incoherent)
      states via continuous thermomajorization, extending the framework to coherent states and time-dependent driving
      while preserving Markovianity is left open.
added: 2026-11-23
updated: 2026-11-23
review: draft
---

## Statement

Consider an $n$-level [[open-system-control|open quantum system]] with Hamiltonian $H_S$ and full coherent control
(the control Hamiltonians $H_1, \dots, H_m$ generate all of $\mathfrak{su}(n)$), coupled via a switchable rate
$\gamma(t) \ge 0$ to a Markovian thermal bath at temperature $T > 0$:

$$\dot\rho(t) = -i\Big[H_S + \sum_{j=1}^{m} u_j(t)\,H_j,\; \rho(t)\Big] - \gamma(t)\,\Gamma_T\big(\rho(t)\big),
\qquad \rho(0) = \rho_0,$$

where the Gorini–Kossakowski–Sudarshan–Lindblad (GKLS) dissipator $\Gamma_T$ has the thermal Gibbs state
$D = \rho_{\mathrm{Gibbs}} = e^{-H_S/T} / \mathrm{Tr}(e^{-H_S/T}) > 0$ as its unique fixed point
[@dirr2019reachable; @vomende2020dmajorization].

Let $\mathfrak{reach}(\rho_0)$ denote the closure of the set of density matrices reachable from $\rho_0$ under all
piecewise-constant coherent controls $u_j$ and $\gamma(t) \ge 0$. A natural outer bound is the set of states
**$D$-majorized** by $\rho_0$, written $\rho \prec_D \rho_0$, meaning there exists a completely positive
trace-preserving (CPTP) map $\Phi$ with $\Phi(\rho_0) = \rho$ and $\Phi(D) = D$ [@vomende2020dmajorization].

**Question.** For finite temperature $0 < T < \infty$ and dimension $n \ge 3$, what is an explicit, computable
characterization of:

1. the reachable set $\mathfrak{reach}(\rho_0)$ for general (non-diagonal) density matrices $\rho_0$, and
2. the matrix $D$-majorization relation $\rho \prec_D \rho_0$ — as well as the exact gap between general
   Gibbs-preserving maps, thermal operations, and time-dependent Markovian (CP-divisible) dynamics?

## Why it matters

In closed systems, [[controllability|controllability]] is governed by Lie groups and unitary orbits preserve the
spectrum of $\rho$. In [[open-system-control|open systems]], dissipation breaks unitarity and the reachable set becomes
a Lie-semigroup orbit [@dirr2009semigroup; @koch2016open]. Knowing which states can be reached from $\rho_0$ with a
given thermal bath sets the fundamental limits of dissipative state preparation, cooling, and finite-time
[[quantum-thermodynamics|quantum thermodynamics]] — telling an optimal-control algorithm whether a target state is
physically attainable before optimization begins [@koch2022roadmap; @vomende2020dmajorization].

## Known results

**The two temperature extremes are settled.** With full coherent control and switchable coupling $\gamma(t) \ge 0$, if
the bath is at zero temperature ($T = 0$), *every* density matrix is approximately reachable from every initial state
[@dirr2019reachable; @koch2022roadmap]. At infinite temperature ($T = \infty$), the dissipator is unital ($D = I/n$),
and reachability is governed by classical majorization of eigenvalue spectra [@dirr2019reachable;
@vomende2020dmajorization].

**Qubits ($n = 2$).** For a two-level system, $D$-majorization has an exact, easily verifiable trace-norm
characterization: $\rho \prec_D \rho_0$ holds if and only if $\|\rho - tD\|_1 \le \|\rho_0 - tD\|_1$ for all
$t \in \mathbb{R}$ (equivalently, via a finite set of trace-norm and generalized-fidelity inequalities)
[@vomende2020dmajorization].

**Diagonal states and Markovian thermal processes.** Restricting to states diagonal in the energy eigenbasis reduces
$D$-majorization to vector $d$-majorization (thermomajorization), which forms a convex polytope and yields outer bounds
for diagonal toy models [@dirr2019reachable; @vomende2020dmajorization]. Crucially, not every thermomajorized state is
reachable by a continuous Markovian master equation: Lostaglio and Korzekwa introduced *continuous thermomajorization*,
giving necessary and sufficient conditions — plus a finite algorithm and universal two-level elementary thermalization
controls — for exact reachability of diagonal states under Markovian thermal processes [@lostaglio2022continuous].

**Obstructions for $n \ge 3$ with coherence.** Beyond two levels, the trace-norm criterion for $D$-majorization fails
because of the counterexample of Heinosaari et al. to the higher-dimensional Alberti–Uhlmann theorem (which separates
positive from completely positive Gibbs-preserving maps) [@heinosaari2012extending; @vomende2020dmajorization].
Furthermore, when coherence is present, the three natural thermodynamic channel classes separate strictly:
$\mathsf{TO} \subsetneq \mathsf{EnTO} \subsetneq Q_D$ (thermal operations, covariant Gibbs-preserving maps, and all
Gibbs-preserving CPTP maps), with strict inclusions already for $n = 3$ [@faist2015gibbs; @ding2021gap;
@vomende2020dmajorization].

## Status

**Partial progress.** The problem is solved at $T = 0$ and $T = \infty$ [@dirr2019reachable], for matrix
$D$-majorization of qubits [@vomende2020dmajorization], and for diagonal states under Markovian thermal processes
[@lostaglio2022continuous]. Characterizing the exact Markovian reachable set — and finding a simple verifiable test for
matrix $D$-majorization — for general coherent states of $n \ge 3$ levels at finite temperature $0 < T < \infty$
remains open [@koch2022roadmap; @vomende2020dmajorization; @lostaglio2022continuous].

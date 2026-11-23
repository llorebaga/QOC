---
title: Structure of time-optimal schedules in quantum annealing and QAOA
question: >-
  When minimizing a problem Hamiltonian's energy over fixed total time $T$ by interpolating between a driver $B$ and a
  problem Hamiltonian $C$, when are optimal schedules purely bang-bang versus hybrid bang-anneal-bang, are singular
  arcs always smooth, and do boundary bangs disappear in Markovian open systems?
status: partial
topics: [variational-algorithms, pmp, geometric-control, open-system-control]
posed_by:
  - key: brady2021annealing
    where: Introduction and discussion. Shows that Pontryagin's maximum principle generally permits singular
      ("annealing") arcs between initial and final bangs ("bang-anneal-bang"), leaving open when purely bang-bang
      (QAOA) versus hybrid schedules are optimal.
  - key: venuti2021optimal
    where: Sections IV.B, V.C, VI and VII (Phys. Rev. Applied 16, 054023). Explicitly leaves open (i) sufficient
      conditions for the active time constraint $\lambda > 0$, (ii) continuity and smoothness of the optimal control on
      singular arcs, and (iii) conjectures that in open systems coupled to an infinite-dimensional Markovian bath,
      boundary bangs vanish and pure continuous annealing schedules are optimal.
added: 2026-11-23
updated: 2026-11-23
review: draft
---

## Statement

Consider the canonical quantum optimization control problem interpolating between a driver Hamiltonian $B$ and a
problem Hamiltonian $C$ over a fixed duration $T > 0$:

$$H(t) = \big(1 - s(t)\big)\,B + s(t)\,C, \qquad s(t) \in [0, 1], \qquad t \in [0, T],$$

starting from the ground state $\rho_0$ of $B$, with the objective of minimizing the final problem energy
$J[s] = \mathrm{Tr}\big[C\,\rho(T)\big]$ [@yang2017pmpvqa; @brady2021annealing; @venuti2021optimal]. A **bang-bang**
schedule takes only the extremal values $s(t) \in \{0, 1\}$ (corresponding to the
[[variational-algorithms|Quantum Approximate Optimization Algorithm]], QAOA), whereas a continuous schedule
$s(t) \in (0, 1)$ corresponds to quantum annealing (QA).

Because $s(t)$ enters the dynamics linearly, [[pmp|Pontryagin's maximum principle]] (PMP) implies that an optimal
schedule consists of bang arcs ($s \in \{0,1\}$ where the switching function $\Phi(t) \neq 0$) and **singular arcs**
($0 < s(t) < 1$ on intervals where $\Phi(t) \equiv 0$) [@brady2021annealing; @venuti2021optimal]. In the open-system
version, $\dot\rho = \mathcal{L}_s(\rho)$ includes a Markovian or non-Markovian dissipator coupled to a bath
[@venuti2021optimal].

**Questions.**

1. *Active time constraint:* What are sharp sufficient conditions ensuring that the PMP time multiplier satisfies
   $\lambda > 0$ (strictly decreasing optimal cost with $T$) for sufficiently small $T$, which guarantees initial and
   final bang arcs in closed systems [@venuti2021optimal]?
2. *Regularity of singular arcs:* Is the optimal control $s^*(t)$ always continuous (or smooth) along singular arcs, or
   can singularities and infinitely rapid switching (chattering) occur [@venuti2021optimal; @robin2022chattering]?
3. *Open-system conjecture:* For an open quantum system coupled to an infinite-dimensional Markovian bath, do boundary
   bangs ($s(0) = 0$ and $s(T) = 1$) cease to be optimal, so that pure continuous annealing schedules are optimal
   [@venuti2021optimal]?

## Why it matters

QAOA and quantum annealing are the two leading paradigms for near-term quantum optimization, yet they represent opposite
extremes of the same optimal-control problem. Determining the exact structure of time-optimal schedules settles whether
discrete gate-based pulses or continuous analog ramps — or a hybrid of both — extract the best performance from a given
coherence budget, and reveals how [[open-system-control|decoherence]] reshapes optimal protocols on noisy hardware
[@brady2021annealing; @venuti2021optimal].

## Known results

**The bang-bang claim and its refinement.** Applying PMP to the closed-system energy minimization problem, Yang et al.
argued that optimal schedules are strictly bang-bang, lending theoretical support to QAOA over continuous annealing
[@yang2017pmpvqa]; Bapat and Jordan also analysed bang-bang optimality in comparison with adiabatic evolution
[@bapat2019bang]. Brady et al. subsequently showed that singular arcs cannot be ruled out in general: under an active
time constraint ($T$ below the minimum time to reach the ground state), optimal protocols start with a bang at $s = 0$
and end with a bang at $s = 1$, but generically follow a smooth singular ("anneal") arc in between — a
**bang-anneal-bang** schedule — and numerical tests on transverse-field Ising models show that finite-depth QAOA
effectively Trotterizes this annealing segment [@brady2021annealing].

**Exact density-matrix PMP and single-spin proof.** Campos Venuti, D'Alessandro and Lidar reformulated the problem in
density-matrix space and sharpened the bang-anneal-bang theorem [@venuti2021optimal]. They proved that for a single
spin-$1/2$ in a closed system, the optimal schedule is strictly bang-bang (a single switch from $s = 0$ to $s = 1$), and
gave a counterexample showing that $T < T_c$ (total time below the exact ground-state reachability time) is necessary
but *not* sufficient for the active time constraint $\lambda > 0$ [@venuti2021optimal].

**Open systems.** For a system coupled to a *finite-dimensional* bath, Campos Venuti et al. proved sufficient
conditions under which bang-anneal, anneal-bang, or bang-anneal-bang schedules remain optimal [@venuti2021optimal]. For
an infinite-dimensional bath described by an adiabatic Redfield master equation, the proof of an initial bang breaks
down, and in the fully Markovian limit neither an initial nor a final bang could be established — motivating their
conjecture that continuous annealing is optimal in Markovian open systems [@venuti2021optimal].

**Chattering in quantum optimal control.** Separately, Robin, Boscain, Sigalotti and Sugny proved that the Fuller
chattering phenomenon (infinitely many bang switches accumulating in finite time onto a singular arc) *can* occur in
quantum optimal control — demonstrating it in a dissipative three-level system [@robin2022chattering] — underscoring
that regularity of singular-to-bang transitions cannot be taken for granted without proof.

## Status

**Partial progress.** The general closed-system structure (bang-anneal-bang with boundary bangs whenever $\lambda > 0$)
is established [@brady2021annealing; @venuti2021optimal], and the single-qubit closed case is completely solved
[@venuti2021optimal]. However, sufficient conditions for $\lambda > 0$, a general proof of continuity or absence of
chattering on singular arcs, a classification of multi-qubit Hamiltonians that admit purely bang-bang optima, and the
conjecture that Markovian open-system optimal schedules are purely continuous all remain open [@venuti2021optimal].

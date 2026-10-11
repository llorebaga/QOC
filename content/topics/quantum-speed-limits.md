---
updated: 2026-10-11
status: draft
key_papers:
  - key: mandelstam1991uncertainty
    note: The original time–energy bound (1945, reprinted) — evolution to an orthogonal state takes at least πħ/(2ΔE).
  - key: margolus1998maximum
    note: A second, independent bound, set by the mean energy above the ground state rather than the energy spread.
  - key: deffner2017review
    note: The standard review — Mandelstam–Tamm and Margolus–Levitin, open systems, and the connection to optimal control.
  - key: caneva2009qsl
    note: Shows that optimal control reaches the quantum speed limit in paradigmatic cases, connecting the two fields.
  - key: bukov2019geometric
    note: With only local controls, many-body state preparation obeys a geometric speed limit that can be exponentially longer than Mandelstam–Tamm.
---

How fast can a quantum system evolve? **Quantum speed limits** (QSLs) are lower bounds on the time needed to go from
one state to another, set by the energy available to the dynamics. In quantum control they appear in two ways:
as fundamental limits that no pulse can beat, and, through the closely related **minimal control time**, as
the shortest duration at which a given control problem becomes solvable. Below that time no optimizer can reach
unit fidelity, and close to it optimization becomes hard.

## The two classic bounds

For a system with time-independent Hamiltonian $H$, starting in $|\psi_0\rangle$, let $\tau_\perp$ be the time to
reach an orthogonal state. Two bounds hold:

$$\tau_\perp \;\ge\; \frac{\pi\hbar}{2\,\Delta E} \qquad\text{(Mandelstam–Tamm)}, \qquad\qquad
\tau_\perp \;\ge\; \frac{\pi\hbar}{2\,\big(\langle E\rangle - E_0\big)} \qquad\text{(Margolus–Levitin)},$$

where $\Delta E$ is the energy uncertainty and $\langle E \rangle - E_0$ the mean energy above the ground state
[@mandelstam1991uncertainty; @margolus1998maximum]. Both hold at once, so the larger of the two is the relevant bound.
This unified bound is tight: for any values of $\Delta E$ and $\langle E\rangle - E_0$ there are states that approach
it arbitrarily closely [@levitin2009unified].

The Mandelstam–Tamm bound has a geometric meaning. The state moves through projective Hilbert space at speed
$\Delta E/\hbar$, as measured by the Fubini–Study metric [@anandan1990geometry]. Since the distance to a target is
the angle $\arccos|\langle\psi_0|\psi_{\rm tgt}\rangle|$,

$$\tau \;\ge\; \frac{\hbar\,\arccos\big|\langle \psi_0 | \psi_{\rm tgt}\rangle\big|}{\Delta E}$$

for any target, not only orthogonal ones. For time-dependent Hamiltonians, the same argument holds with $\Delta E$
replaced by its time average along the path.

## Generalizations

- **Open systems.** Speed limits have been derived for non-unitary dynamics. They are based on the quantum Fisher
  information [@taddei2013physical], on the Lindblad generator in a Mandelstam–Tamm-like form [@delcampo2013open],
  and on operator norms of the generator in a Margolus–Levitin-like form. In the last case, non-Markovian effects can
  *speed up* the evolution [@deffner2013nonmarkovian].
- **Other geometries.** Every valid measure of distinguishability between quantum states gives a speed limit,
  and the choice can be made to tighten the bound [@pires2016generalized].
- **Classical systems.** Speed limits are not uniquely quantum: equivalent bounds exist for classical dynamics in phase
  space [@shanahan2018classical].
- **Experiments.** The crossover between the Mandelstam–Tamm and Margolus–Levitin regimes has been observed with
  atoms in a multilevel system, using fast matter-wave interferometry [@ness2021crossover].

A comprehensive review groups these results into a *geometric* approach (distinguishability of states) and a
*minimal-time* approach (control theory) [@deffner2017review].

## Speed limits in optimal control

The bounds above refer to a *given* Hamiltonian. A control problem asks something different: the **minimal control
time** to reach a target when the Hamiltonian can be shaped within constraints. The textbook QSLs usually say little
about this time, and bounds adapted to control are needed [@poggi2019geometric]:

- **Optimal control finds the limit.** Scanning the duration $T$ with an optimizer shows a sharp threshold. Above a
  minimal time unit fidelity is reached, below it is not, and in paradigmatic cases this threshold coincides with the
  speed limit allowed by the dynamics [@caneva2009qsl].
- **Drift and amplitude bounds.** For a closed system, the minimal time for a target gate can be bounded from below
  in terms of the gate, the strength of the drift and the maximal control amplitude. For a single qubit this bound
  describes the numerical minimal times remarkably well [@arenz2017drift].
- **Exact minimal times.** For a driven two-level system, the minimal time and the optimal protocol are known exactly
  [@hegerfeldt2013qsl]. [[geometric-control|Geometric control]] gives exact minimal times more generally for small
  systems.

## Many-body systems

In interacting systems, locality matters. Information propagates at a finite speed — the Lieb–Robinson bound
[@lieb1972finite] — so transferring a state along a chain takes a time that grows with its length. Optimal control can
drive an excitation along a spin chain at this maximal propagation rate [@murphy2010chain]. When only *local*
controls are available, state preparation obeys a geometric speed limit set by the quantum geometric tensor. In
glassy or chaotic systems it can be exponentially larger than the Mandelstam–Tamm time [@bukov2019geometric]. The
quantum speed limit of atom transport has even been explored with a citizen-science game [@sorensen2016speedlimit].

## Why it matters

- **Coherence budgets.** Faster operations accumulate less decoherence, so the minimal time is a design target for
  gates and state preparation; see [[gate-synthesis]] and [[state-preparation]].
- **Optimization difficulty.** Near the minimal time, the [[control-landscapes|control landscape]] becomes rugged
  and even glassy, so optimizers need more restarts or global methods.
- **Resources.** How the minimal time depends on bandwidth and on the number of control parameters is the subject of
  [[control-complexity]].

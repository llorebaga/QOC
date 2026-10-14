---
title: Time-optimal cooling of two qubits through one decay channel
question: >-
  Two qubits, only one of which decays, are cooled using arbitrarily fast unitary control. Can every achievable rate
  of change of the eigenvalues of the state be obtained, up to convex combinations, by simply permuting the eigenbasis?
  If so, the time-optimal cooling protocol for this system is known explicitly.
status: open
topics: [open-system-control, quantum-thermodynamics, quantum-speed-limits]
posed_by:
  - key: malvetti2024cooling
    where: Conjecture 6.3 (arXiv:2403.05285), supported by a partial proof and numerical evidence; the time-optimal
      cooling procedure derived in Section VIII for this system assumes the conjecture.
added: 2026-10-14
updated: 2026-10-14
review: draft
---

## Statement

**The system.** A Markovian system on $\mathbb C^n$ evolves under a Lindblad equation with jump operators $V_k$, and
the control Hamiltonians generate all of $\mathfrak{su}(n)$ with unbounded amplitudes — *fast unitary control*. The
unitary orbit can then be crossed instantly, and what matters is the spectrum
$\lambda \in \Delta^{n-1}$ (the probability simplex) of the state. It obeys the **reduced control system**

$$\dot\lambda = -L_U\,\lambda, \qquad -L_U = J(U) - \mathrm{diag}\big(J(U)^{\top} e\big), \qquad
J(U)_{ij} = \sum_k \big|\langle i|\,U^{*} V_k U\,|j\rangle\big|^2,$$

where the control is the unitary $U(t)$ that sets the eigenbasis relative to the dissipation, and
$e = (1,\dots,1)$. The reduced and the full systems have the same reachable sets up to unitary orbits
[@malvetti2025reachability; @malvetti2024cooling].

Let $\mathrm{derv}(\lambda) = \{-L_U\lambda : U \in SU(n)\}$ be the set of achievable derivatives at $\lambda$. The
system is called **quasi-classical** if, for every $\lambda$, these derivatives lie in the convex hull of the ones
obtained with permutation matrices,

$$\mathrm{derv}(\lambda) \subseteq P(\lambda) := \mathrm{conv}\{-L_P\,\lambda : P \in S_n\},$$

so that, up to convexification, the optimal control only ever needs to permute the eigenbasis.

**Conjecture** (Malvetti). For two qubits ($n = 4$) with the single jump operator $V = \sigma^- \otimes \mathbb 1$ —
decay of the first qubit only — and every $\lambda \in \Delta^3$,

$$\mathrm{conv}\big(\mathrm{derv}(\lambda)\big) = P(\lambda).$$

That is, this "spin–spin" system is quasi-classical [@malvetti2024cooling].

## Why it matters

Cooling, or resetting, a register quickly is a basic task of every quantum device. When only part of a system is
coupled to a cold bath, the rest can be cooled only by moving entropy towards the dissipative part with coherent
control, and the fastest way to do so is a question of time-optimal [[open-system-control|open-system control]]. With
fast unitary control, the reduction to the eigenvalues turns it into a finite-dimensional problem on the simplex. If
the system is quasi-classical, the controls can be restricted to permutations, and time-optimal cooling becomes an
explicitly solvable problem; this two-qubit system is described as a first approximation of the ubiquitous spin–boson
system [@malvetti2024cooling]. See also [[quantum-thermodynamics]].

## Known results

**General framework.** Reachability, coolability and stabilizability of Markovian systems with fast unitary control
can be studied on the reduced system; coolability has a simple necessary and sufficient characterization
[@malvetti2025reachability; @malvetti2024cooling].

**Solved cases.** Provably time-optimal cooling protocols have been derived for rank-one qubit systems and for the
inverted $\Lambda$ ("V") system on a qutrit. The V system is quasi-classical, whereas the rank-one qubit systems are
not [@malvetti2024cooling]. Time-optimal cooling and heating controls of a Markovian qubit are worked out in
[@malvetti2024qubit].

**The conjecture.** One inclusion is trivial: $P(\lambda) \subseteq \mathrm{conv}(\mathrm{derv}(\lambda))$. For
regular $\lambda$, $P(\lambda)$ is a polytope with 12 vertices and 8 facets: four hexagonal facets, which are easily
shown to bound $\mathrm{derv}(\lambda)$, and four triangular ones, for which only numerical evidence is available. A
slightly larger bound on the achievable derivatives is proved. Assuming the conjecture, the time-optimal
cooling procedure for this system follows explicitly [@malvetti2024cooling].

## Status

**Open.** The conjecture is stated in the 2024 paper with numerical evidence, and the optimal cooling result for the
two-qubit system is conditional on it. Its arXiv version has not been revised, and we have found no later work that
proves or refutes it. If you know of one, please tell us.

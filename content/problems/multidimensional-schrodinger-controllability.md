---
title: Exact controllability of the multidimensional bilinear Schrödinger equation
question: >-
  For a quantum particle in a bounded domain $\Omega \subset \mathbb{R}^d$ with $d \ge 2$, driven by a scalar
  time-dependent field, is the bilinear Schrödinger equation locally or globally *exactly* controllable in finite time
  in a suitable Sobolev space?
status: open
topics: [controllability, bosonic-control, molecules]
posed_by:
  - key: beauchard2015encyclopedia
    where: Section "Open Problems" (discussion of Theorem 1). Exact controllability in finite time for $d \ge 2$ is
      stated as an open problem; the authors conjecture that in $d \ge 3$ (or with continuous spectrum) local exact
      controllability with $L^2$-bounded controls fails because the Dirichlet–Laplacian eigenvalues violate the spectral
      gap condition.
  - key: duca2022nls
    where: Introduction. Notes that while local exact controllability is established in 1D, exact controllability in the
      multidimensional case remains an open problem.
  - key: koch2022roadmap
    where: Section 2.2.4 and Section 2.3. Highlights controllability of infinite-dimensional Schrödinger PDEs — in
      particular beyond 1D and with degenerate or continuous spectra — as a central open challenge.
added: 2026-11-23
updated: 2026-11-23
review: draft
---

## Statement

Let $\Omega \subset \mathbb{R}^d$ be a bounded domain with smooth boundary (for instance, a $d$-dimensional box), and
consider the bilinear controlled Schrödinger equation

$$i\,\partial_t \psi(t,x) = \big(-\Delta + V(x) - u(t)\,\mu(x)\big)\psi(t,x), \qquad x \in \Omega, \quad \psi|_{\partial\Omega} = 0,$$

where $\psi(t,\cdot)$ evolves on the unit sphere $\mathcal{S}$ of $L^2(\Omega, \mathbb{C})$, $V$ and $\mu$ are real
potentials, and $u : [0,T] \to \mathbb{R}$ is a real-valued control field.

The system is **locally exactly controllable** around an eigenstate $\phi_1$ in a functional space $X \subset
L^2(\Omega)$ at time $T > 0$ if every target state $\psi_f \in \mathcal{S} \cap X$ sufficiently close to $\phi_1$
(up to the free evolution phase) can be reached *exactly* at time $T$ by an admissible control $u \in U([0,T])$; it is
**globally exactly controllable** in $X$ if every pair $\psi_0, \psi_f \in \mathcal{S} \cap X$ can be connected in
finite time.

**Question.** For dimension $d \ge 2$, does there exist a functional space $X$ (such as a Sobolev space $H^s$) and a
control space $U$ in which the bilinear Schrödinger equation is locally — or globally — exactly controllable in finite
time? In particular, is the conjecture of Beauchard and Rouchon true: that in $d \ge 3$ (or in the presence of
continuous spectrum), local exact controllability fails for $L^2$-bounded controls [@beauchard2015encyclopedia]?

## Why it matters

Finite-dimensional [[controllability|quantum controllability]] is governed by a simple algebraic criterion — the Lie
algebra rank condition — and exact and approximate controllability coincide. In infinite dimensions (particles in
potentials, [[molecules|molecular wavepackets]], or [[bosonic-control|continuous-variable modes]]), this equivalence
breaks down dramatically. Ball, Marsden and Slemrod proved in 1982 that exact controllability on the full $L^2$ sphere
with locally integrable controls is impossible [@ball1982bilinear]. Knowing whether exact steering is nevertheless
possible in smoother Sobolev spaces in two and three spatial dimensions — and what regularity of controls it demands —
is the core mathematical question of PDE-based quantum control [@beauchard2015encyclopedia; @glaser2015training;
@koch2022roadmap].

## Known results

**No exact controllability in $L^2$.** By the Ball–Marsden–Slemrod obstruction, for any bounded multiplication operator
$\mu$ and controls $u \in L^1_{\mathrm{loc}}$, the reachable set from any initial state has empty interior in $L^2$
(in fact it is a countable union of compact subsets), ruling out exact controllability in $L^2$ [@ball1982bilinear].

**1D finite-time exact controllability is solved.** For a particle in a 1D infinite potential well $\Omega = (0,1)$,
Beauchard bypassed the Ball–Marsden–Slemrod obstruction by working in higher Sobolev regularity, proving local exact
controllability around eigenstates in $H^7$ via Nash–Moser techniques [@beauchard2005local]. Beauchard and Laurent
simplified the proof using the classical inverse mapping theorem and established local exact controllability in $H^3$
(with $u \in L^2$) for both linear and nonlinear 1D Schrödinger equations [@beauchard2010local]; combining this with
global approximate controllability in Sobolev norms [@nersesyan2010global] yields *global* exact controllability in
finite time in 1D. Local exact controllability in $H^1$ for suitable 1D settings — including discontinuous potentials
and periodic boundary conditions with a magnetic field — was established more recently [@boussaid2025h1].

**Multidimensional approximate and infinite-time results.** For any dimension $d \ge 1$ and generic smooth potentials
$(V,\mu)$, Nersesyan proved global *approximate* controllability in every Sobolev norm $H^s$ [@nersesyan2010global].
Moreover, Nersesyan and Nersisyan proved global *exact* controllability in *infinite* time ($t \to \infty$) for 1D and
multidimensional Schrödinger equations [@nersesyan2012infinite; @beauchard2015encyclopedia].

**Why 1D methods fail in $d \ge 2$.** The 1D local exact controllability proofs linearize around an eigenstate and solve
a trigonometric moment problem via Ingham's inequality, which requires a uniform spectral gap between consecutive
eigenvalues of $-\Delta + V$ [@beauchard2010local; @beauchard2015encyclopedia]. By Weyl's law, the eigenvalues of the
Dirichlet Laplacian grow as $k^{2/d}$: the gap grows linearly in $d = 1$, stays constant on average in $d = 2$, and
closes as $k \to \infty$ for $d \ge 3$, breaking the moment-problem approach [@beauchard2015encyclopedia].

## Status

**Open.** In one dimension, both local and global finite-time exact controllability in Sobolev spaces are well
established [@beauchard2005local; @beauchard2010local; @nersesyan2010global; @boussaid2025h1]. In dimensions $d \ge 2$,
only global approximate controllability [@nersesyan2010global] and infinite-time exact controllability
[@nersesyan2012infinite] are known; finite-time exact controllability remains open, and the conjecture of Beauchard
and Rouchon on its failure for $L^2$-bounded controls in $d \ge 3$ is neither proved nor refuted
[@beauchard2015encyclopedia; @duca2022nls].

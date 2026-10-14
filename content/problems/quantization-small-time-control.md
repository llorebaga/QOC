---
title: Does a classical speed limit survive quantization?
question: >-
  If a classical particle driven by a controlled potential cannot be steered across its phase space in arbitrarily
  short time, is the corresponding Schrödinger equation also not controllable in arbitrarily short time?
status: partial
topics: [quantum-speed-limits, controllability]
posed_by:
  - key: beschastnyi2021obstruction
    where: Conjecture 1, stated in the introduction, together with the definitions of the classical and quantum
      controllability diameters.
  - key: koch2022roadmap
    where: Section 2.3, "Quantum speed limit". Which properties of an infinite-dimensional system imply that it has
      no speed limit, and whether a speed limit passes through quantization, are listed as open.
added: 2026-10-14
updated: 2026-10-14
review: draft
---

## Statement

Let $M$ be a connected, complete Riemannian manifold, and consider the controlled Schrödinger equation and its
classical counterpart [@beschastnyi2021obstruction]

$$i\,\partial_t\psi = \Big(-\tfrac12\Delta + V(x) + u(t)\,W(x)\Big)\psi, \qquad \psi \in L^2(M),$$

$$H(t,\xi) = \tfrac12\lVert p\rVert^2 + V(x) + u(t)\,W(x), \qquad \xi = (p,x) \in T^*M,$$

with real potentials $V, W$ such that $-\tfrac12\Delta + V + uW$ is essentially self-adjoint for every $u \in \mathbb R$,
and piecewise-constant controls $u$. Let $\mathcal A^q_T(\psi_0)$ be the set of states reachable from $\psi_0$ in time
at most $T$, and $\mathcal A^c_T(\xi_0)$ the same for the classical system. The **controllability diameters** are

$$T_q = \sup_{\psi_0}\, \inf\Big\{T \ge 0 : \overline{\mathcal A^q_T(\psi_0)} = S(M)\Big\},$$

$$T_c = \inf\Big\{T \ge 0 : \exists\, \Omega \subset T^*M \text{ dense},\ \forall \xi_0 \in \Omega:\
\overline{\mathcal A^c_T(\xi_0)} = T^*M\Big\},$$

where $S(M)$ is the unit sphere of $L^2(M)$. A system is *small-time controllable* when its diameter is zero.

**Conjecture** (Beschastnyi, Boscain, Sigalotti). For every Hamiltonian of this form,
$$T_c > 0 \;\Longrightarrow\; T_q > 0.$$

In words: the quantum effects that come from the non-locality of the Schrödinger equation have a limited effect at
small times.

## Why it matters

A positive controllability diameter is a [[quantum-speed-limits|speed limit]] for control: no field, however
strong, can perform every task faster. In finite dimension $n > 1$ there always is one: for $i\dot\psi = (A + u(t)B)\psi$,
the overlap of the state with an eigenvector of $B$ cannot change faster than $\lVert A\rVert$ allows, so $T_q > 0$
[@agrachev2017timezero; @beschastnyi2021obstruction]. In infinite dimensions the drift is unbounded and this
argument fails, so whether a speed limit exists becomes a real question — important whenever a system must be
controlled much faster than it decoheres [@beschastnyi2021obstruction]. A semiclassical criterion would let one
decide it from classical mechanics.

The conjecture goes in one direction only. The converse is false: the harmonic oscillator driven by an electric
field is controllable as a classical system but not approximately controllable as a quantum one; and tunnelling can
make a quantum system controllable when its classical counterpart is not [@beschastnyi2021obstruction].

## Known results

**Quantum speed limits proved directly.** For a particle in a controlled electric field, Gaussian wave packets stay
localized along classical trajectories for a time that does not depend on the control, which forces $T_q > 0$
[@beauchard2014minimal; @beauchard2018minimal].

**The conjecture in a class of systems.** If $M = N_1 \times N_2$ and, on an open subset $\Omega \subset N_1$, the
control potential $W$ does not depend on the $N_1$ coordinate and the $N_1$-gradient of $V$ is bounded by a Lipschitz
function, then $T_c > 0$ — and the quantum system also has $T_q > 0$. The simplest case is a $W$ that is constant on an
open set, where the classical dynamics does not feel the control. The quantum proof uses the WKB method to show that
tunnelling cannot empty such a region in arbitrarily small time [@beschastnyi2021obstruction].

**Systems without a speed limit.** Small-time controllability is possible in infinite dimensions. An early example
was given for a fractional Schrödinger-type equation [@boussaid2012smalltime] (see the discussion in
[@beschastnyi2021obstruction]). Small-time control of phases was proved for nonlinear Schrödinger equations on tori
[@duca2024sobolev] and on $\mathbb R^N$ with electromagnetic controls [@duca2025smalltime], and small-time control
between particular eigenfunctions on closed manifolds, with an application to rotating linear molecules
[@chambrion2023smalltime]. The first bilinear Schrödinger equations that are globally approximately controllable in
arbitrarily small time have two controls, one of them on the frequency of a quadratic potential
[@beauchard2026examples]. A second method, based on controlling flows of diffeomorphisms, covers equations on tori
and on $\mathbb R^d$ [@beauchard2025diffeomorphisms] and extends to a logarithmic nonlinear Schrödinger equation
[@beauchard2026logarithmic]. These results use several controls, while the conjecture is stated for one.

## Status

**Partial progress.** The conjecture is proved for the class of systems above and open in general. Its authors note
that most questions about small-time controllability are open [@beschastnyi2021obstruction], and more recent work
calls the characterization of small-time controllable bilinear Schrödinger equations an ambitious open problem
[@beauchard2025diffeomorphisms].

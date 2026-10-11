---
updated: 2026-10-11
status: draft
key_papers:
  - key: boscain2021pmp
    note: A tutorial introduction to the maximum principle for quantum physicists — normal, abnormal and singular extremals, existence, and worked quantum examples.
  - key: agrachev2004geometric
    note: The geometric-control textbook treatment of the maximum principle on manifolds and Lie groups.
  - key: lapert2010singular
    note: Singular extremals in the time-optimal control of a dissipative spin-1/2 particle, with an NMR experiment.
  - key: brady2021annealing
    note: Applies the maximum principle to quantum annealing and QAOA and finds bang–anneal–bang optimal protocols, not pure bang-bang.
---

**Pontryagin's maximum principle** (PMP), formulated in the 1950s for engineering problems, gives the *necessary
conditions* that an optimal control must satisfy. It turns an optimization over functions into a boundary-value problem
for the state and an auxiliary **co-state**, together with a pointwise maximization condition on the control. In
quantum control it plays two roles. It yields exact optimal solutions for small systems, and it underlies the
numerical gradient methods used for large ones. A tutorial written for quantum physicists is
[@boscain2021pmp]; the geometric theory is developed in [@agrachev2004geometric].

## Statement

Consider a system $\dot x = f(x, u)$ with controls $u(t) \in \mathcal U$, and a cost

$$C[u] = \varphi\big(x(T)\big) + \int_0^T f^0\big(x(t), u(t)\big)\,dt$$

to be minimized. Define the **pseudo-Hamiltonian**

$$\mathcal H(x, p, p^0, u) = \langle p, f(x, u)\rangle + p^0 f^0(x, u).$$

!!! note "Maximum principle"
    If $u^*$ is optimal with trajectory $x^*$, there exist a constant $p^0 \le 0$ and a co-state $p(t)$, not both zero,
    such that

    - $\dot x = \partial\mathcal H/\partial p$ and $\dot p = -\partial\mathcal H/\partial x$;
    - for almost every $t$, $u^*(t)$ **maximizes** $\mathcal H\big(x^*(t), p(t), p^0, v\big)$ over $v \in \mathcal U$;
    - boundary (transversality) conditions hold, e.g. $p(T) = p^0\,\nabla\varphi\big(x(T)\big)$ when the final state is free;
      and if the final time is free, $\mathcal H = 0$ along the optimal trajectory.

Trajectories satisfying these conditions are **extremals**. They are called *normal* if $p^0 \neq 0$ (normalized to
$p^0 = -1$) and *abnormal* if $p^0 = 0$. The principle only gives candidates: an extremal need not be optimal, and
optimality must be checked separately.

## Quantum form

For a closed system $|\dot\psi\rangle = -iH(u)|\psi\rangle$ with $H(u) = H_0 + \sum_k u_k H_k$, the co-state is a
wavefunction $|\chi(t)\rangle$ and the pseudo-Hamiltonian reads

$$\mathcal H = \mathrm{Re}\,\big\langle \chi \big|\, {-i}H(u)\, \big|\psi\big\rangle + p^0 f^0 .$$

Its equation of motion $\dot p = -\partial\mathcal H/\partial x$ is again the Schrödinger equation,
$|\dot\chi\rangle = -iH(u)|\chi\rangle$, solved backward from a final condition set by the figure of merit. The way
the controls enter is summarized by the **switching functions**

$$\Phi_k(t) = \frac{\partial \mathcal H}{\partial u_k} - p^0\frac{\partial f^0}{\partial u_k}
= \mathrm{Im}\,\big\langle \chi(t) \big| H_k \big| \psi(t) \big\rangle .$$

Two cases recur:

- **Energy-penalized, unbounded controls**, $f^0 = \tfrac12\sum_k u_k^2$ with $p^0 = -1$. Maximization gives
  $u_k(t) = \Phi_k(t) = \mathrm{Im}\langle\chi(t)|H_k|\psi(t)\rangle$. This is the structure of the updates of
  [[krotov|Krotov's method]] and of the gradient in [[grape|GRAPE]]: numerical methods solve these conditions
  iteratively.
- **Bounded controls, time-optimal problems**, $|u_k| \le u_{\max}$ and $f^0 = 1$. $\mathcal H$ is linear in $u$, so
  $u_k(t) = u_{\max}\,\mathrm{sign}\,\Phi_k(t)$ wherever $\Phi_k \neq 0$ — **bang-bang** control. If $\Phi_k$ vanishes
  on a whole interval, the arc is **singular** and the control is found by differentiating $\Phi_k$ until $u$
  appears.

## What it has revealed

- **Exact optimal protocols for two- and three-level systems**, e.g. for laser-driven population transfer
  [@boscain2002laser] and for time-optimal single-qubit operations [@garon2013su2]; see [[geometric-control]].
- **Singular arcs are physical.** In the time-optimal control of a dissipative spin-1/2, the optimal solution contains
  singular arcs, and it has been realized experimentally in NMR [@lapert2010singular].
- **Bang-bang versus smooth.** The maximum principle has been used to argue that optimal variational protocols for
  fixed total time have bang-bang form, supporting the structure of QAOA [@yang2017pmpvqa]. A later analysis showed
  that generic optimal protocols are bang–anneal–bang — pulsed at the beginning and end with a smooth, singular
  annealing segment in between [@brady2021annealing]. See [[variational-algorithms]].
- **Minimal times.** Free-final-time problems, with the condition $\mathcal H = 0$, give minimal control times —
  control-based [[quantum-speed-limits|quantum speed limits]] — which are known exactly for driven two-level systems
  [@hegerfeldt2013qsl; @garon2013su2].

## Practical notes

- **Shooting.** Solving the boundary-value problem by guessing the initial co-state and integrating forward
  ("shooting") works for low-dimensional systems. Larger problems are solved by gradient iterations ([[grape]],
  [[krotov]]), which converge towards normal extremals.
- **Existence matters.** The principle assumes that an optimum exists. With unbounded controls, or without
  penalties, it may not — the infimum can be approached without being reached.
- **Sufficiency.** Second-order conditions, or a direct comparison of all extremals, are needed to confirm optimality.
  [[control-landscapes|Landscape]] analysis studies the same critical points from a global point of view.

---
title: Does provable absence of barren plateaus imply classical simulability?
question: >-
  In parameterized quantum circuits and variational optimal control, does every natural ansatz whose loss landscape is
  provably free of barren plateaus also admit an efficient classical simulation (at least after polynomial-size data
  acquisition from a quantum device)?
status: open
topics: [variational-algorithms, control-landscapes, controllability]
posed_by:
  - key: cerezo2025simulability
    where: Title question and Section II, Eq. (5) ($\overline{\mathrm{BP}} \overset{?}{\subset} \mathrm{CSIM}$ or
      $\mathrm{QESIM}$). The Perspective collects case-by-case evidence that known mechanisms for provably avoiding
      barren plateaus confine the dynamics to polynomially sized, classically simulable subspaces.
added: 2026-11-23
updated: 2026-11-23
review: draft
---

## Statement

Consider a parameterized unitary $U(\boldsymbol{\theta}) = \prod_{l=1}^{L} \exp(-i \theta_l H_l)$ acting on $n$
qubits — which describes both a variational quantum circuit and a discretized piecewise-constant
[[variational-algorithms|quantum optimal control]] pulse — together with an initial state $\rho$, a Hermitian
observable $O$, and the loss function

$$\ell_{\boldsymbol{\theta}}(\rho, O) = \mathrm{Tr}\!\big[U(\boldsymbol{\theta})\,\rho\,U(\boldsymbol{\theta})^\dagger\,O\big].$$

Given a distribution $\mathcal{P}$ over parameters $\boldsymbol{\theta}$, the problem family exhibits a **barren
plateau** if the variance $\mathrm{Var}_{\boldsymbol{\theta}\sim\mathcal{P}}[\ell_{\boldsymbol{\theta}}(\rho, O)]$
decays exponentially with $n$ (typically $O(b^{-n})$ for some $b > 1$); otherwise, when the variance decays at most
polynomially in $n$, it belongs to the barren-plateau-free class $\overline{\mathrm{BP}}$ [@cerezo2025simulability].

Let $\mathrm{CSIM}$ denote the class of loss functions that can be estimated to inverse-polynomial precision by a
classical algorithm in $\mathrm{poly}(n)$ time (with high probability over $\boldsymbol{\theta}\sim\mathcal{P}$), and
let $\mathrm{QESIM}$ denote the broader class that is classically simulable after an initial polynomial-size
classical data-acquisition phase on a quantum device [@cerezo2025simulability].

**Question.** For physically realistic, continuous parameter distributions $\mathcal{P}$, does provable absence of
barren plateaus imply classical simulability — that is,

$$\overline{\mathrm{BP}} \;\overset{?}{\subset}\; \mathrm{CSIM} \qquad \text{or} \qquad \overline{\mathrm{BP}} \;\overset{?}{\subset}\; \mathrm{QESIM}?$$

## Why it matters

In finite-dimensional [[controllability|quantum controllability]], the dynamical Lie algebra $\mathfrak{g}$ generated
by the control Hamiltonians $\{iH_l\}$ determines the reachable unitary manifold. For deep parameterized circuits and
variational control ansätze, the same algebra governs trainability: an exponentially large $\mathfrak{g}$ gives high
expressivity but concentrates gradients exponentially around zero, creating barren plateaus [@larocca2022barren;
@ragone2024lie; @fontana2024adjoint]. If every structural mechanism that provably avoids barren plateaus also enables
efficient classical simulation, then provably trainable variational quantum algorithms cannot deliver a superpolynomial
quantum advantage in the optimization stage — forcing a rethinking of how [[control-landscapes|control landscapes]]
and quantum hardware should be used together [@cerezo2025simulability].

## Known results

**Lie-algebraic theory of barren plateaus.** Building on the control-theoretic diagnosis of barren plateaus via the
dynamical Lie algebra [@larocca2022barren], Ragone et al. and Fontana et al. derived exact variance formulas showing
that, for deep circuits whose generators form a Lie algebra $\mathfrak{g}$ and observables in $i\mathfrak{g}$, the
loss variance scales inversely with $\dim(\mathfrak{g})$ [@ragone2024lie; @fontana2024adjoint]. Avoiding barren
plateaus in this regime therefore requires $\dim(\mathfrak{g}) \in O(\mathrm{poly}(n))$.

**Classical simulation of BP-free families.** Whenever $\dim(\mathfrak{g})$ grows polynomially in $n$ and the relevant
observable or state projects onto $i\mathfrak{g}$, the dynamics can be simulated classically in the adjoint
representation ($\mathfrak{g}$-sim) in polynomial time [@goh2025gsim]. Cerezo et al. extended this observation across
the other major provably barren-plateau-free architectures — shallow hardware-efficient circuits, matchgate and
symmetry-equivariant ansätze, small-angle initializations, and certain non-unital noisy circuits — showing that each
restricts the effective dynamics to a polynomially sized subspace and falls into $\mathrm{CSIM}$ or $\mathrm{QESIM}$
[@cerezo2025simulability]. In particular, quantum convolutional neural networks (QCNNs), long viewed as a leading
barren-plateau-free architecture, were shown to be effectively classically simulable on average [@bermejo2026qcnn].

**Caveats and boundary cases.** Strictly speaking, $\overline{\mathrm{BP}} \neq \mathrm{QESIM}$ if arbitrary
*discrete* parameter distributions are permitted: Cerezo et al. construct a contrived circuit encoding a classically
hard Boolean function (such as discrete logarithm) over discrete angles $\theta_i \in \{0, \pi/2, \pi, 3\pi/2, 2\pi\}$
that avoids concentration yet is not in $\mathrm{QESIM}$ (while the continuous-angle variant becomes average-case
simulable) [@cerezo2025simulability]. More recently, Meyer et al. studied local landscape patches near Clifford
circuits using Taylor surrogates, proving the existence of regimes where gradients decay only polynomially while
standard Taylor surrogation scales superpolynomially [@meyer2026surrogation].

## Status

**Open.** Every widely studied family of variational circuits with an unconditional proof of barren-plateau absence
over standard continuous parameter distributions has so far been shown to admit classical simulation (with or without
quantum data acquisition) [@cerezo2025simulability; @goh2025gsim; @bermejo2026qcnn]. However, there is no general
theorem proving $\overline{\mathrm{BP}} \subset \mathrm{QESIM}$ for continuous ansätze, and no uncontrived
continuous-parameter counterexample with a provable quantum advantage has been established; smart initializations,
structured warm-start patches [@meyer2026surrogation], and heuristic regimes remain active areas of investigation.

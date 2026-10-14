---
title: Ensemble controllability with a single control beyond two-level systems
question: >-
  A continuum of qubits whose resonance frequencies are known only up to an interval can be steered simultaneously,
  to any family of target gates, by one real-valued control field. Does the same hold for systems with more than two
  levels?
status: open
topics: [robust-optimal-control, controllability, adiabatic-passage]
posed_by:
  - key: koch2022roadmap
    where: Section 2.3, "Simultaneous controllability". Whether single-control ensemble controllability, known for a
      qubit with a dispersion in the Larmor frequency, extends beyond two-level systems is called an important open
      problem.
  - key: robin2022ensemble
    where: Discussion after the main approximation theorem (Remark 6 of arXiv:2003.05831). The authors expect their
      techniques to apply to systems with more levels, but note that the extension does not seem trivial.
added: 2026-10-14
updated: 2026-10-14
review: draft
---

## Statement

**The two-level result.** Consider the ensemble of qubits

$$i\,\frac{d}{dt}M(\alpha,\delta,t) = \big((E+\alpha)\,\sigma_z + \delta\,u(t)\,\sigma_x\big)\,M(\alpha,\delta,t),
\qquad M(\alpha,\delta,0) = I_2,$$

with $E > 0$, an unknown detuning $\alpha \in [v_0, v_1]$ ($v_0 < 0 < v_1$), an unknown coupling strength
$\delta \in [\delta_m, \delta_M]$ ($0 < \delta_m \le \delta_M$), and **one** real control
$u \in L^\infty([0,T],[-K,K])$, the same for every member of the ensemble. Robin, Augier, Boscain and Sigalotti
proved that if $3(E + v_0) > E + v_1$, then for every continuous target $M_F$ from the parameter set to $SU(2)$, every
$\varepsilon > 0$ and every $K > 0$ there are $T$ and $u$ with
$\max_{\alpha,\delta}\lVert M(\alpha,\delta,T) - M_F(\alpha,\delta)\rVert < \varepsilon$ — approximate ensemble
controllability in $C^0$ [@robin2022ensemble].

**Question.** Consider a family of $N$-level systems, $N \ge 3$,

$$i\,\frac{d}{dt}M(\theta,t) = \big(H_0(\theta) + u(t)\,H_1(\theta)\big)\,M(\theta,t), \qquad M(\theta,0) = I_N,$$

with parameters $\theta$ in a compact set $K$ containing a continuum of values (for example, a dispersion of the
transition frequencies) and a single real control $u$. Under which conditions on $H_0(\theta)$ and $H_1(\theta)$ is
this ensemble approximately controllable in $C^0(K, SU(N))$? In particular, do multilevel analogues of the qubit
result hold?

## Why it matters

Ensemble controllability is the mathematical basis of [[robust-optimal-control|robust control]]: one pulse that works
for every value of an unknown or inhomogeneous parameter, without feedback. Most experiments drive a system with a
single real field, but the classical ensemble results use two independent controls (the two quadratures of the
field), and the step from two controls to one is not innocent: the rotating-wave approximation that turns one real
field into two effective controls interacts with the adiabatic approximation that gives robustness
[@robin2022ensemble; @koch2022roadmap]. Multilevel systems — atoms with several relevant levels, qudits,
molecules — are where robust pulses are increasingly needed.

## Known results

**Two controls.** For the Bloch equations with dispersion in the Larmor frequency and in the field amplitude,
ensembles are approximately controllable with two controls [@li2006ensemble; @li2009bloch]. Controllability questions
for Bloch ensembles and other systems with continuous spectrum were also analysed by Beauchard, Coron and Rouchon
[@beauchard2010bloch].

**Finitely many parameter values.** If the parameter takes only finitely many values, simultaneous controllability
of systems on $SU(N)$ has been characterized by Lie-algebraic conditions (see the review in [@koch2022roadmap]). The
difficulty of the problem above is the continuum of values.

**General Lie-algebraic results.** Lie-algebraic methods give ensemble controllability for classes of
control-affine systems [@agrachev2016ensemble], and every semisimple Lie algebra admits parameter-dependent control
Hamiltonians for which approximate ensemble controllability holds — but in general with many controls
[@chen2019ensemble; @koch2022roadmap].

**Adiabatic methods.** With two controls, robustness can be traced to conical intersections of the eigenvalues,
which an [[adiabatic-passage|adiabatic]] path can follow for every value of the parameter [@augier2018adiabatic].

**One control, one qubit.** The theorem above is obtained by justifying rigorously the cascade of the rotating-wave
and adiabatic approximations with high-order averaging; the condition $3(E + v_0) > E + v_1$ keeps characteristic
frequencies from overlapping [@robin2022ensemble].

## Status

**Open.** The single-control result is proved for two-level systems only. The 2022 roadmap calls the extension an
important open problem [@koch2022roadmap], and we have not found a result that settles it for $N \ge 3$. If you know
of one, please tell us.

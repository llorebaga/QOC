---
title: Maximum speed-up of qudit purification by measurement-based feedback
question: >-
  Under continuous weak measurement of an angular-momentum component $J_z$ on a $D$-dimensional qudit, with unitary
  feedback keeping the state's eigenbasis unbiased relative to $J_z$, does the maximum purification speed-up scale as
  $O(D)$ or $O(D^2)$?
status: solved
topics: [feedback-control, state-preparation, quantum-speed-limits]
posed_by:
  - key: combes2010unbiased
    where: Section VII, "Discussion" (Phys. Rev. A 82, 022307). After bounding the unbiased-basis purification
      speed-up of a $D$-dimensional qudit by $\frac{2}{3}(D+1) \le S \le D^2/2$, the authors explicitly state that it
      remains an open question whether the actual achievable speed-up is $O(D)$ or $O(D^2)$.
added: 2026-11-23
updated: 2026-11-23
review: draft
---

## Statement

Consider a $D$-dimensional quantum system (a qudit with spin $J = (D-1)/2$) subject to a continuous, quantum-limited
weak measurement of the angular-momentum observable $J_z$ at rate $\gamma$, together with arbitrarily fast unitary
[[feedback-control|measurement-based feedback]] $H(t)$ conditioned on the measurement record [@combes2006rapid;
@combes2010unbiased]. In the absence of feedback, the mean linear impurity $L(t) = \mathbb{E}[1 - \mathrm{Tr}\,\rho(t)^2]$
decays exponentially at long times as $e^{-r_0 t}$ (with $r_0 = 2\gamma$).

In an **unbiased-basis (UBB) feedback** protocol, the controller rotates $\rho(t)$ at every instant so that its
eigenbasis is mutually unbiased with respect to the eigenbasis of $J_z$ (making all measurement outcomes equally
informative, in analogy with Jacobs' single-qubit protocol) [@jacobs2003purification; @combes2006rapid]. The asymptotic
**purification speed-up** $S$ is the ratio of the exponential decay rate of the mean impurity under feedback to that
without feedback (equivalently, the factor by which the time to reach a target high mean purity is reduced).

**Question.** Within the rigorous bounds $\frac{2}{3}(D+1) \le S \le \frac{1}{2}D^2$ established in
[@combes2010unbiased], what is the optimal asymptotic scaling of $S$ with dimension $D$ — is it $O(D)$ or $O(D^2)$?

## Why it matters

Rapid [[state-preparation|state purification]] (initialization) is a basic primitive for quantum computing and sensing
when thermal cooling is slow. For a single qubit ($D = 2$), Jacobs showed that continuous feedback keeping the Bloch
vector orthogonal to the measurement axis doubles the average purification rate ($S = 2$), a purely quantum effect
relying on coherent superpositions [@jacobs2003purification], though Wiseman and Ralph pointed out that the choice of
figure of merit — mean purity at fixed time versus mean time to reach a target purity — reverses the optimal strategy
[@wiseman2006rapid]. In higher dimensions $D$, knowing whether coherent feedback can achieve a quadratic $O(D^2)$
speed-up — or only the $O(D)$ scaling already attainable without feedback by random open-loop unitaries
[@combes2010random] — tests the true power of real-time quantum feedback [@combes2010unbiased; @combes2011maximum].

## Known results

**Single-qubit baseline and qudit bounds.** Jacobs introduced the unbiased-basis feedback protocol for a qubit,
achieving $S = 2$ [@jacobs2003purification]. Combes and Jacobs generalized the protocol to $D$-dimensional qudits and
derived the lower bound $S \ge \frac{2}{3}(D+1)$ for an averaged UBB strategy [@combes2006rapid]. Combes, Wiseman,
Jacobs and O'Connor rigorously re-derived this lower bound, proved the upper bound $S \le D^2/2$ for *any* UBB feedback
protocol on a qudit, and showed that for $n$ independent qubit measurements on an $n$-qubit register the speed-up is
at most $2n$ [@combes2010unbiased]. Meanwhile, Combes, Wiseman and Scott proved that open-loop random unitaries (no
feedback) already achieve $S \sim \frac{2}{3}D$, sharpening the question of whether UBB feedback can beat linear
scaling [@combes2010random].

**Resolution: $O(D^2)$ is achievable, but complementarity alone is not enough.** Combes and Wiseman resolved the
question completely [@combes2011maximum]. First, they showed a sharp surprise: merely keeping the state's eigenbasis
unbiased (complementary) relative to $J_z$ does *not* guarantee even $O(D)$ scaling — poorly chosen unbiased bases yield
a speed-up of only $S = 2$ (correcting the interpretation of the earlier averaged lower bound). Second, they
constructed an explicit locally optimal UBB feedback protocol based on the quantum Fourier transform (QFT) that
achieves $S \approx 0.2\,D^2$ analytically — attaining the optimal $O(D^2)$ scaling, with nearly deterministic
information gain — and provided numerical evidence that optimal unbiased bases saturate the upper bound $S = D^2/2$ for
even $D$ [@combes2011maximum].

## Status

**Solved.** The optimal purification speed-up of a continuously monitored $D$-dimensional qudit under unbiased-basis
feedback scales as $\Theta(D^2)$: bounded above by $D^2/2$ [@combes2010unbiased] and achieved up to a constant factor
($\approx 0.2\,D^2$) by an explicit QFT-based feedback protocol [@combes2011maximum].

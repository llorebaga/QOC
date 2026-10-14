---
title: How many pulses does universal dynamical decoupling of a qubit need?
question: >-
  To cancel an arbitrary interaction between a qubit and its environment up to order $K$ in the total time, with
  ideal instantaneous pulses, are about $K^2$ pulses necessary — as for quadratic dynamical decoupling — or do
  $O(K)$ pulses suffice?
status: open
topics: [dynamical-decoupling, open-system-control]
posed_by:
  - key: west2010qdd
    where: Introduction and conclusions. Exhaustive numerical searches for orders 2, 3 and 4 find optimal sequences
      only two pulses shorter than the quadratic construction, and the authors state their belief that the
      construction is very nearly optimal.
added: 2026-10-14
updated: 2026-10-14
review: draft
---

## Statement

A qubit coupled to a bath evolves under the most general Hamiltonian

$$H = I \otimes B_I + X \otimes B_X + Y \otimes B_Y + Z \otimes B_Z,$$

with arbitrary bounded bath operators $B_\alpha$ ($B_I$ is the bath's own Hamiltonian). A dynamical decoupling
sequence applies ideal, instantaneous $\pi$ pulses about the $x$ and $z$ axes at chosen times in $[0, T]$. It
achieves **order $K$** if the resulting evolution, in the toggling frame, contains no term that couples qubit and bath
up to order $T^K$ — for every choice of the $B_\alpha$, and to all orders in the coupling strength
[@west2010qdd; @kuo2011qdd].

Let $N(K)$ be the smallest number of pulses that achieves order $K$.

**Question.** How does $N(K)$ grow? Is $N(K) = \Theta(K^2)$, as the quadratic construction suggests, or is
$N(K) = O(K)$?

## Why it matters

[[dynamical-decoupling|Dynamical decoupling]] is the cheapest way to protect idle qubits and is used routinely on
current processors. Each pulse costs time and adds pulse errors, so the number of pulses needed for a given order of
protection decides how far high-order schemes are useful in practice. The question is also a clean test of what
optimal control can achieve with the simplest possible controls: a finite set of instantaneous rotations.

## Known results

**One error axis.** For pure dephasing, or for pure relaxation, Uhrig's sequence reaches order $K$ with $K$ pulses
[@uhrig2007keeping], and no sequence does it with fewer [@yang2008udd; @west2010qdd]. Since general noise contains
these cases, $N(K) \ge K$; a self-contained proof of this lower bound is given in [@kim2026weakcoupling].

**Quadratic dynamical decoupling (QDD).** Nesting a Uhrig sequence about one axis inside a Uhrig sequence about an
orthogonal axis cancels general decoherence to order $K$ with $(K+1)^2$ pulse intervals, so $N(K) = O(K^2)$
[@west2010qdd]. Concatenated decoupling, the first scheme to reach arbitrary order, needs a number of pulses that
grows exponentially with $K$ [@khodjasteh2005cdd; @kim2026weakcoupling]. The universality of QDD was proved first for
even inner order [@wang2011nested] and then for all inner and outer orders [@kuo2011qdd], with rigorous performance
bounds for bounded baths [@xia2011bounds].

**Small orders.** Exhaustive numerical searches give optimal sequences of 7, 14 and 23 pulses for orders 2, 3 and 4 —
that is, $(K+1)^2 - 2$, differing from QDD by at most two pulses [@west2010qdd].

**Weak coupling.** If only the terms *linear* in the coupling strength $J$ must vanish through order $K$, then $O(K)$
pulses suffice — at most $3K$ for a single qubit — and linear scaling is optimal. The construction maps pulse
scheduling to the continuous necklace-splitting problem. Its error is $O(JT^{K+1}) + O(J^2T^2)$, so it beats QDD
when the coupling is weak; outside that regime QDD, which also cancels higher orders in $J$, can perform better
[@kim2026weakcoupling].

## Status

**Open.** For decoupling to all orders in the coupling, the best known sequences use $\Theta(K^2)$ pulses and the best
lower bound is $K$. The small-order searches and the conjecture of near-optimality point to quadratic growth, but no
lower bound beyond linear is known, and we have not found a construction with $o(K^2)$ pulses. If you know one,
please tell us. The asymptotic form of the question is our formulation of the near-optimality conjecture of West,
Fong and Lidar.

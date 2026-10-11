---
updated: 2026-10-12
status: draft
key_papers:
  - key: rabitz2004landscape
    note: The landscape conjecture. Under mild assumptions, the optimal-control landscape for transition probabilities has no local traps — only global optima and saddles.
  - key: chakrabarti2007landscapes
    note: A comprehensive review of quantum control landscapes — kinematic and dynamical pictures, critical-point structure, consequences for optimization.
  - key: pechen2011traps
    note: A counterexample. Special (singular) critical points can create traps in the dynamical landscape, shown for a three-level system.
  - key: russell2017trapfree
    note: Proves that almost all closed, finite-dimensional systems have trap-free landscapes, and clarifies when singular controls can and cannot cause traps.
  - key: riviello2015severe
    note: How constraints on the number of controls, the duration and the field strength create artificial traps in practice.
---

The **control landscape** is the figure of merit viewed as a function of the controls,
$u(\cdot) \mapsto J[u]$ — an extremely high-dimensional surface over the space of all pulses. Its shape decides how
hard an optimization is. If every local optimum is also a global one, any local method such as [[grape|GRAPE]] or
[[krotov|Krotov]] will succeed from almost any starting point. If there are **traps** — local optima that are not
global — the optimizer can get stuck. A central, and at first surprising, result of the field is that for many
quantum control problems the landscape is **trap-free**. This explains why optimal control works so well in practice.

## Kinematic and dynamical landscapes

The map from controls to the figure of merit can be split into two steps:

$$u(\cdot)\;\xrightarrow{\;\text{dynamics}\;}\;U(T)\;\xrightarrow{\;\text{kinematics}\;}\;J\big(U(T)\big).$$

The **kinematic landscape** $J(U)$ is a function on the unitary group, for example the transition probability
$|\langle f|U|i\rangle|^2$ or an expectation value $\mathrm{Tr}\big(O\,U\rho U^\dagger\big)$. Its critical points can be
classified completely: they are global maxima, global minima and saddles, with no local optima [@ho2006easy]. The
**dynamical landscape** $J[u]$ inherits this structure if the first map is well behaved
[@rabitz2004landscape; @chakrabarti2007landscapes].

!!! note "When is the landscape trap-free?"
    Three assumptions guarantee that there are no traps [@riviello2015severe]:

    1. the system is [[controllability|controllable]];
    2. the map from controls to $U(T)$ is *locally surjective* — its Jacobian has full rank at the critical points;
    3. the controls are *unconstrained*.

## Traps: where the assumptions fail

**Singular controls.** Where the Jacobian loses rank — at *singular* controls, the singular extremals of
[[pmp|Pontryagin's maximum principle]] — the kinematic argument does not apply. A three-level example shows that such
points can indeed be traps [@pechen2011traps], and the assumptions of landscape analysis have been examined critically
[@defouquieres2013landscapes]. A later geometric analysis proved that *almost all* closed, finite-dimensional systems
are nonetheless trap-free in a broad class of situations, including qubit evolutions in quantum computing. Being
singular is not by itself enough for a control to stop an optimization [@russell2017trapfree].

**Constraints.** The practically most important source of traps is the third assumption. Real optimizations restrict
the controls:

- **few parameters** — a truncated basis, as in [[crab|CRAB]], or a coarse time grid;
- **short durations** — close to the minimal time;
- **bounded amplitudes or bandwidth.**

Simulations show that such constraints can create *artificial* traps, severe enough to prevent successful
optimization [@riviello2015severe]. The minimum number of controls needed for a high yield depends on the number of
accessible states [@moore2012constrained]. Even a two-level system develops a rich landscape structure when the total
time approaches the speed limit [@larocca2018twolevel].

**Near the minimal time.** In many-body state preparation, the landscape changes character as the protocol duration
decreases. A glass-like transition appears: an exponential number of near-optimal solutions separated by barriers,
with the true optimum exponentially hard to find [@bukov2018phases; @day2019glassy]. See [[quantum-speed-limits]] and
[[many-body-control]].

## What it means for optimization

- **Why local methods usually work.** With enough control freedom and enough time, a gradient method from a random
  start reaches a global optimum. This is the common experience with GRAPE and Krotov.
- **When to expect trouble.** Few parameters, short times, strong bounds: use restarts, continuation in time or
  parameters, or methods that escape false traps. dCRAB changes its basis to reach the trap-free landscape
  [@rach2015dcrab]; global methods find the best solution of the constrained problem directly
  ([[polynomial-optimization|QCPOP]], [[gradient-free]]).
- **Beyond quantum control.** The same questions — how controllability shapes the landscape — decide the trainability of
  variational quantum algorithms, where the dimension of the dynamical Lie algebra determines whether gradients vanish
  (barren plateaus) [@larocca2022barren]. See [[variational-algorithms]].

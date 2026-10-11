---
updated: 2026-10-11
status: draft
key_papers:
  - key: haeberlen1968averaging
    note: Average Hamiltonian theory — coherent averaging by periodic pulse sequences, the NMR origin of Hamiltonian engineering.
  - key: goldman2014periodically
    note: Effective Hamiltonians of periodically driven systems and how to engineer gauge fields with them.
  - key: bukov2015highfrequency
    note: The high-frequency expansion in depth — when the Floquet Hamiltonian differs from the time average, stroboscopic versus non-stroboscopic dynamics.
  - key: choi2020robust
    note: A framework for designing periodic pulse sequences that engineer robust target Hamiltonians in strongly interacting spin systems.
  - key: abanin2017prethermal
    note: Rigorous bounds showing that heating of driven many-body systems is exponentially slow in the drive frequency — the basis of long-lived Floquet engineering.
---

**Floquet engineering** uses **periodic driving** to give a quantum system an effective Hamiltonian it does not
naturally have. Examples: suppressing unwanted interactions, creating new couplings, or synthesizing gauge fields and
topological bands. Pulse sequences in NMR, dynamical decoupling, parametric gates in superconducting circuits and
shaken optical lattices are all instances of the same idea. Optimal control extends it by optimizing the drive
waveform itself.

## Floquet theory in brief

For a Hamiltonian with period $T$, $H(t+T) = H(t)$, the evolution operator can be written as

$$U(t, 0) = P(t)\,e^{-iH_F t/\hbar}, \qquad P(t + T) = P(t),$$

with a time-independent **Floquet Hamiltonian** $H_F$ and a periodic *micromotion* $P(t)$ [@shirley1965floquet].
Observed stroboscopically, at $t = nT$, the system evolves as if under $H_F$ alone. Floquet engineering means choosing
the drive so that $H_F$ is the Hamiltonian one wants.

## The high-frequency (Magnus) expansion

When the drive is fast compared with the system's own dynamics, $H_F$ is computed order by order (with $\hbar = 1$):

$$H_F = \underbrace{\frac{1}{T}\int_0^T H(t)\,dt}_{H^{(0)}}
\;+\; \underbrace{\frac{1}{2iT}\int_0^T\!dt_1\int_0^{t_1}\!dt_2\,\big[H(t_1), H(t_2)\big]}_{H^{(1)}} \;+\;\dots$$

The leading term is the time average. In magnetic resonance this is **average Hamiltonian theory**
[@haeberlen1968averaging], which explains, for example, how the WAHUHA sequence averages away dipolar couplings to
give high-resolution NMR in solids [@waugh1968wahuha]. The higher-order terms matter. In several important classes of
protocols — the Kapitza pendulum, artificial magnetic fields for neutral atoms, Floquet Chern insulators — the
infinite-frequency Floquet Hamiltonian differs from the simple average [@bukov2015highfrequency;
@goldman2014periodically]. Decoupling sequences are the special case where the target average is zero; see
[[dynamical-decoupling]].

## Where it is used

- **Ultracold atoms in shaken lattices.** Periodic modulation renormalizes tunnelling, creates artificial gauge fields
  and topological bands [@eckardt2017colloquium]. A notable example is the realization of the topological Haldane model
  with fermions in a modulated honeycomb lattice [@jotzu2014haldane]. See [[cold-atoms]].
- **Interacting spins.** Global periodic pulse sequences engineer target many-body Hamiltonians that are robust against
  disorder, unwanted interactions and pulse imperfections [@choi2020robust]. With Rydberg atoms, the type of spin
  Hamiltonian itself can be changed by driving [@geier2021floquet]. See [[spins]] and [[neutral-atoms]].
- **Superconducting circuits.** Modulating qubit frequencies activates selective *parametric* couplings, giving a
  universal gate set on fixed-coupling hardware [@reagor2018parametric]. See [[superconducting]].
- **Quantum materials.** Light-driven band structures and phases — "Floquet engineering of quantum materials"
  [@oka2019floquet].
- **Counterdiabatic driving.** Approximate counterdiabatic terms, built as nested commutators, can be realized with
  periodic driving using only the available controls [@claeys2019floquetcd]; see [[shortcuts-to-adiabaticity]].

## Heating and its limits

Interacting many-body systems absorb energy from a periodic drive. For generic systems at finite drive period, the
long-time state is featureless, equivalent to infinite temperature [@dalessio2014heating]. Fortunately, heating is
exponentially slow in the drive frequency. A long-lived *prethermal* regime exists in which the engineered Floquet
Hamiltonian governs the dynamics [@abanin2017prethermal]. Choosing the drive frequency is therefore a trade-off:
high enough to suppress heating and higher-order corrections, low enough to stay within the available bandwidth and
avoid exciting other levels.

## Floquet engineering and optimal control

Floquet engineering is usually analytic: choose a drive and compute $H_F$. Optimal control turns it around. It
searches for the drive *waveform* that produces a target Floquet Hamiltonian or a target quasi-energy band structure,
for example to manipulate the Floquet bands of a two-dimensional material [@castro2023floquetoct]. Robustness to
pulse errors can be built into the same optimization; see [[robust-optimal-control]].

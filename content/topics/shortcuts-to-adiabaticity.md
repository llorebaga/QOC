---
updated: 2026-10-12
status: draft
key_papers:
  - key: guery2019sta
    note: The comprehensive review — concepts, methods (counterdiabatic driving, invariants, fast-forward), and applications across atomic, molecular and many-body physics.
  - key: demirplak2003adiabatic
    note: Introduces counterdiabatic control fields that make population transfer exactly adiabatic at any speed.
  - key: berry2009transitionless
    note: Transitionless quantum driving — the general formula for the Hamiltonian that drives a system exactly along its instantaneous eigenstates.
  - key: chen2010cooling
    note: Invariant-based inverse engineering for fast frictionless cooling in harmonic traps — the paper that named "shortcuts to adiabaticity".
  - key: sels2017local
    note: Local, approximate counterdiabatic driving from a variational principle — the route to shortcuts in complex many-body systems.
---

Adiabatic processes are robust: if a Hamiltonian changes slowly enough, a system follows its instantaneous eigenstate
and ends up exactly where intended. But "slowly enough" can be too slow for the available coherence time.
**Shortcuts to adiabaticity** (STA) reach the same final state as a perfectly adiabatic process in a *finite*,
short time, by designing the Hamiltonian so that the excitations created along the way are cancelled or undone
[@guery2019sta; @torrontegui2013sta]. Most shortcuts are analytic or semi-analytic, which makes them a natural
partner and starting point for numerical optimal control.

## The adiabatic starting point

For a Hamiltonian $H_0(\lambda(t))$ with instantaneous eigenstates $|n(t)\rangle$, the adiabatic theorem
[@born1928adiabatensatz; @kato1950adiabatic] guarantees that a system starting in $|n(0)\rangle$ stays in
$|n(t)\rangle$ (up to a phase) if the rate of change is small compared with the energy gaps. Shortcuts remove the
need for slowness in three main ways.

## Counterdiabatic (transitionless) driving

Add a term that exactly cancels the non-adiabatic couplings. With

$$H(t) = H_0(t) + H_1(t), \qquad
H_1(t) = i\hbar \sum_n \Big( |\partial_t n\rangle\langle n| - \langle n|\partial_t n\rangle\, |n\rangle\langle n| \Big),$$

the system follows the eigenstates of $H_0$ exactly, at any speed [@demirplak2003adiabatic; @berry2009transitionless].
Equivalently $H_1 = \dot\lambda\,\mathcal A_\lambda$, where $\mathcal A_\lambda$ is the *adiabatic gauge potential*
[@kolodrubetz2017geometry].

For a two-level system $H_0 = \tfrac{\hbar}{2}\big(\Delta(t)\,\sigma_z + \Omega(t)\,\sigma_x\big)$ — a Landau–Zener sweep —
the counterdiabatic term is a field along $\sigma_y$, $H_1 = \tfrac{\hbar}{2}\,\Omega_a(t)\,\sigma_y$, with
$\Omega_a = (\dot\Omega\Delta - \Omega\dot\Delta)/(\Omega^2 + \Delta^2)$ (up to sign conventions). It has been realized
with Bose–Einstein condensates in optical lattices [@bason2012driving] and with a single NV-centre spin
[@zhang2013assisted].

The difficulty is that $H_1$ requires knowledge of all eigenstates and, in many-body systems, typically involves
non-local, many-body terms that cannot be implemented. Two ideas address this:

- **Experimentally realizable protocols** for single-particle, many-body and non-linear systems that do not need the
  spectrum as input, applied for example to fast decompression of condensates [@delcampo2013counterdiabatic];
- **Local counterdiabatic driving**, which approximates the gauge potential variationally with the terms that are
  actually available [@sels2017local], or as a series of nested commutators realized by periodic driving
  [@claeys2019floquetcd]. See [[floquet-engineering]].

## Invariant-based inverse engineering

A Lewis–Riesenfeld invariant $I(t)$ satisfies $\partial_t I + \tfrac{1}{i\hbar}[I, H] = 0$, and the eigenstates of
$I(t)$, with suitable phases, solve the Schrödinger equation exactly [@lewis1969invariant]. One *designs* $I(t)$ to
commute with $H$ at the initial and final times, then inverts it to find the Hamiltonian that realizes it. Applied to
expanding a harmonic trap, this gives frictionless cooling in a time much shorter than adiabatic expansion. The trap
may transiently become expulsive, and the cooling times are shorter than those of bang-bang optimal control restricted
to real trap frequencies [@chen2010cooling]. Formulated as a time-optimal control problem, the minimal-time solution
is itself bang-bang [@stefanatos2010frictionless]; see [[geometric-control]].

## Fast-forward

The fast-forward approach derives driving potentials that reproduce, in any desired short time, the result of a slow
adiabatic process — transport, splitting or squeezing of a wavefunction — up to a global phase
[@masuda2010fastforward].

## In quantum computing

Counterdiabatic terms can be added to digitized adiabatic algorithms, improving fidelity with shallow circuits on
current hardware [@hegade2021digitized]. Adding non-stoquastic counterdiabatic terms to adiabatic optimization for Ising
spin glasses has been proposed to give a polynomial enhancement over standard adiabatic optimization
[@hegade2022dcqo]. See [[variational-algorithms]].

## Costs and limits

Shortcuts are not free. There is a rigorous trade-off between speed and the energetic cost of the counterdiabatic
field. Instantaneous driving would need infinite cost, and the spectral gap governs both the speed limit and the cost
[@campbell2017tradeoff]; see [[quantum-speed-limits]]. Different shortcuts to the same target also differ in their
sensitivity to noise and systematic errors, and the most robust one can be selected
[@ruschhaupt2012robust]; see [[robust-optimal-control]].

## Shortcuts and optimal control

The two approaches are complementary. Shortcuts provide interpretable, analytic protocols and good initial guesses.
Optimal control can then add constraints (bounded amplitudes, limited couplings), robustness, or push towards the
minimal time. In thermodynamics, shortcuts suppress the "quantum friction" of finite-time cycles; see
[[quantum-thermodynamics]]. Applications span [[cold-atoms|cold-atom transport and cooling]],
[[adiabatic-passage|population transfer]], and [[state-preparation]].

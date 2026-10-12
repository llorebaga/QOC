---
updated: 2026-10-12
status: draft
key_papers:
  - key: doria2011crab
    note: Optimal control of a many-body system simulated with time-dependent DMRG — the paper that introduced CRAB.
  - key: caneva2011speeding
    note: Optimized crossing of a quantum phase transition, with a minimal time set by the smallest spectral gap.
  - key: lloyd2014information
    note: How many control parameters a many-body problem needs, and why efficiently simulable dynamics is efficiently controllable.
  - key: rosi2013fast
    note: Closed-loop optimal control of ultracold atoms in an optical lattice, including the superfluid–Mott-insulator crossing.
  - key: omran2019cat
    note: GHZ states of up to 20 Rydberg atoms, prepared with optimal control of the many-body system.
---

**Many-body optimal control** deals with systems of many interacting particles: spin chains, atoms in optical
lattices, Rydberg arrays, Bose–Einstein condensates. The tasks are the same as elsewhere — prepare a state, cross a
phase transition quickly, transfer an excitation, implement an evolution — but two features change the problem. The
Hilbert space grows exponentially with the number of particles, so the dynamics can rarely be simulated exactly. And
the controls are usually few, global fields (a lattice depth, a laser detuning, a Rabi frequency) acting on all
particles at once.

## What makes it hard

- **Simulation.** Exact propagation, and with it [[grape|GRAPE]]-type gradients, is limited to a few tens of
  spins. Larger systems need approximate dynamics: tensor networks in one dimension — matrix product states, the
  time-evolving block decimation [@vidal2004tebd] and time-dependent DMRG [@schollwock2011dmrg] — or mean-field
  descriptions, such as the Gross–Pitaevskii equation for condensates [@hohenester2007bec; @jager2014bec].
  See [[propagation-methods]].
- **Reachability.** Global controls respect the symmetries of the system, which restrict what can be reached
  [@zeier2011symmetry]. Conversely, acting on a small part can be enough. Heisenberg chains, for instance, are fully
  controllable by operating on one spin at their end [@burgarth2009local]. See [[controllability]].
- **Time.** Correlations spread at a finite speed in lattice systems [@lieb1972finite], and transfers along chains
  have a minimal time [@murphy2010chain]. Crossing a quantum phase transition without creating defects takes at
  least a time of order $\pi/\Delta$, where $\Delta$ is the minimal spectral gap. The optimal dynamics reaching this
  bound is not adiabatic [@caneva2011speeding]. See [[quantum-speed-limits]].

## How few parameters suffice

States that local Hamiltonians can reach in polynomial time fill an exponentially small part of Hilbert space.
The number of control parameters a problem needs is set by the dimension of that reachable set, not of the full
space. When the dynamics has an efficient classical description, such as slightly entangled one-dimensional
dynamics, the control problem can be solved efficiently [@lloyd2014information]. Conserved quantities shrink the
manifold further [@caneva2014complexity]. See [[control-complexity]].

This is why compact parametrizations work so well here. [[crab|CRAB]] was introduced precisely to control a
many-body system simulated with time-dependent DMRG [@doria2011crab]. Optimizing a handful of coefficients keeps
the number of expensive simulations small, and dCRAB removes the traps that a truncated basis introduces
[@rach2015dcrab; @muller2022decade].

## Methods in use

- **Open-loop optimization on approximate models**: CRAB/dCRAB with tensor networks [@doria2011crab], and GRAPE
  or Krotov with the Gross–Pitaevskii equation [@jager2014bec].
- **Closed-loop optimization** on the experiment itself, which removes the need to simulate the dynamics at all
  [@rosi2013fast; @heck2018remote]. See [[closed-loop]].
- **Counterdiabatic and variational driving**, which approximates the adiabatic gauge potential with local terms
  [@sels2017local]. See [[shortcuts-to-adiabaticity]].
- **Reinforcement learning**, which also showed that many-body state preparation has distinct "phases" of control,
  set by the protocol duration [@bukov2018phases], including a glassy phase with many near-optimal protocols
  [@day2019glassy]. See [[machine-learning-control]].

## In experiments

- **Optical lattices.** Closed-loop optimization of atom loading and of the superfluid–Mott-insulator crossing
  improved the result and sped up the process more than threefold compared with adiabatic ramps [@rosi2013fast].
  Optimal transformations were computed and verified experimentally for the motional states of a condensate and for a
  phase-transition crossing in small lattice systems, and they proved robust to temperature and atom-number
  fluctuations [@vanfrank2016complex].
- **Rydberg arrays.** Optimal control protocols were proposed for ordered many-body ground states and GHZ states of
  Rydberg lattice gases [@cui2017rydberg]. Experimentally, GHZ states of up to 20 atoms were created by engineering
  the energy spectrum and using optimal control of the many-body system [@omran2019cat]. See [[neutral-atoms]].

## Connections

Many-body control meets quantum computing in [[variational-algorithms]], where QAOA and quantum annealing are
control protocols for spin Hamiltonians. It is also the natural setting for [[state-preparation]] on
[[cold-atoms|cold-atom]] and [[neutral-atoms|Rydberg]] simulators.

## Limitations

- Optimal controls are only as good as the approximate model used to find them: truncation errors in a tensor network
  or the breakdown of mean-field theory can be mistaken for good performance.
- Tensor-network methods are efficient only while entanglement stays low, which fast, strongly driven protocols
  can violate. Two-dimensional systems remain hard.
- Global controls cannot correct local imperfections, such as disorder or inhomogeneous couplings, without help.

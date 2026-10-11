---
updated: 2026-10-12
status: draft
key_papers:
  - key: poyatos1996reservoir
    note: Proposes quantum reservoir engineering — designing the environment of laser-cooled trapped ions to prepare and protect quantum states.
  - key: verstraete2009dissipation
    note: Shows that dissipation alone can drive universal quantum computation and the preparation of complex many-body states.
  - key: ticozzi2010stabilizing
    note: Any generic quantum state can be stabilized by constructively designing a Lindblad generator.
  - key: shankar2013autonomous
    note: Autonomous stabilization of a Bell state of two superconducting qubits by engineered dissipation, without measurement-based feedback.
  - key: harrington2022engineered
    note: A modern review of engineered dissipation for measurement, state preparation and stabilization in quantum information science.
---

**Reservoir engineering** turns dissipation from a problem into a tool. Instead of shielding a system from its
environment, one *designs* the coupling to an engineered environment so that the dynamics relaxes the system into a
desired state, and keeps it there. Because the target is an attractor of the dynamics, it is reached from any
initial state and recovered after perturbations, without measurement or active feedback.

## The idea

For Lindblad dynamics, $\dot\rho = \mathcal L(\rho)$, the long-time state is a steady state, $\mathcal L(\rho_{ss}) = 0$.
If the jump operators $L_k$ and the Hamiltonian are designed so that a target pure state $|\psi\rangle$ is a **dark
state** — annihilated by every $L_k$ and an eigenstate of $H$ — and the dynamics has no other steady state, every
initial state converges to $|\psi\rangle$. This makes dissipation a deterministic, self-correcting preparation
protocol. The approach was proposed for trapped ions, whose motion can be laser-cooled into an engineered bath
[@poyatos1996reservoir].

## How far it reaches

- **Many-body states.** Any pure multipartite state can be prepared as the unique steady state of a suitable
  dissipative process [@kraus2008markov]. Driven, dissipative cold-atom systems can be steered into given many-body
  states and phases [@diehl2008driven].
- **Computation.** Dissipation alone can perform universal quantum computation and prepare complex states such as
  ground states of frustration-free Hamiltonians [@verstraete2009dissipation].
- **Control theory.** For Markovian dynamics, the invariance and attractivity of subspaces have been characterized
  [@ticozzi2008markovian]. Any generic state can be made globally asymptotically stable by constructively designing
  the Lindblad generator [@ticozzi2010stabilizing].

## In experiments

- **Atomic ensembles.** Engineered dissipation generated steady-state entanglement between two macroscopic atomic
  ensembles at room temperature, maintained for 0.04 s [@krauter2011dissipation].
- **Trapped ions.** An open-system quantum simulator with up to five qubits implemented engineered dissipative
  dynamics [@barreiro2011opensim]. Unitary operations combined with engineered dissipation produced and stabilized an
  approximate Bell state [@lin2013dissipative].
- **Superconducting circuits.** Tailoring the microwave noise in a cavity relaxes a qubit to an arbitrary chosen
  superposition [@murch2012bath]. Two qubits were autonomously stabilized in a Bell state [@shankar2013autonomous].
  Engineered two-photon loss confines a cavity field to the manifold of cat states [@leghtas2015twophoton], the basis of
  dissipatively protected cat qubits [@mirrahimi2014cat]. See [[bosonic-control]] and [[error-correction]].

Reviews cover engineered dissipation across quantum information science [@harrington2022engineered] and as a resource
in superconducting circuits [@kapit2017upside].

## Reservoir engineering and control

Reservoir engineering is control at the level of the *generator* of the dynamics: drives, couplings and auxiliary
lossy modes are chosen to shape $\mathcal L$. Optimal control can design those drives, or speed up the convergence to
the steady state; see [[open-system-control]]. Compared with [[feedback-control|measurement-based feedback]],
autonomous schemes need no fast classical processing. Feeding quantum outputs back coherently — see
[[linear-quantum-systems]] — sits in between. The same ideas underpin autonomous quantum error correction
[@kerckhoff2010memory].

## Limitations

- Engineering the right jump operators needs strong, well-controlled couplings to auxiliary dissipative modes.
- Steady states are reached only asymptotically, and the convergence rate (the dissipative gap) can be small, especially
  in many-body systems.
- Unwanted, natural dissipation competes with the engineered one and limits the attainable fidelity.

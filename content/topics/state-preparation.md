---
updated: 2026-10-12
status: draft
key_papers:
  - key: tannor1985control
    note: Steering molecular wave packets with timed pulses to select the outcome of a chemical reaction — an origin of state-to-state control.
  - key: bergmann1998coherent
    note: Review of STIRAP and related adiabatic methods for complete, robust population transfer.
  - key: caneva2009qsl
    note: Optimal control reaches the target state exactly down to a minimal time that coincides with the quantum speed limit.
  - key: christandl2004perfect
    note: Spin networks with fixed, engineered couplings that transfer any state perfectly, without switching.
  - key: cirac1997network
    note: Transfer between distant atoms by shaping the emitted photon so that it is absorbed with unit probability.
  - key: kraus2008markov
    note: Any pure entangled state can be prepared as the unique steady state of an engineered dissipative process.
---

**State preparation** drives a quantum system from a known initial state into a target state: a superposition, an
entangled state of many qubits, the ground state of a many-body Hamiltonian, a Fock or cat state of an oscillator.
**State transfer** moves an unknown state from one place to another, along a chain or between distant nodes. These
were the first problems of quantum control, in the steering of molecular wave packets to select chemical products
[@tannor1985control; @kosloff1989wavepacket; @rabitz2000whither]. They remain the most common ones outside gate
design.

## The problem

For pure states, the objective is the overlap $F = |\langle\psi_\mathrm{target}|\psi(T)\rangle|^2$. It involves one
state rather than a full unitary, so it is cheaper to compute and needs fewer control resources. Its
[[control-landscapes|landscape]] is generically free of traps when the system is controllable. For mixed or open
systems, the objective becomes a distance between density matrices or the expectation of a projector. See
[[problem-formulation]]. The minimal duration is set by the speed limit, and an optimizer scanning the duration
finds it as the time below which the target can no longer be reached [@caneva2009qsl].

## Routes to a target state

- **Adiabatic following.** Slowly changing the Hamiltonian keeps the system in an eigenstate that connects the
  initial and target states. STIRAP and rapid adiabatic passage transfer population completely and robustly
  [@bergmann1998coherent; @vitanov2017stirap]. Adiabatic quantum computation prepares ground states of problem
  Hamiltonians the same way [@albash2018aqc]. See [[adiabatic-passage]].
- **Shortcuts.** Shortcuts to adiabaticity reach the same final state in a finite time [@guery2019sta], for example
  cooling atoms in harmonic traps fast and without final excitation [@chen2010cooling]. See
  [[shortcuts-to-adiabaticity]].
- **Optimal control.** Numerical optimization handles the cases without analytic solutions, from single qubits to
  many-body states [@doria2011crab; @omran2019cat]. See [[grape]], [[crab]] and [[many-body-control]].
- **Constructive sequences.** For an oscillator coupled to a qubit, any state can be built step by step
  [@law1996arbitrary], as done for arbitrary superpositions of photon numbers [@hofheinz2009synthesizing]. See
  [[bosonic-control]].
- **Circuits.** Entangling gates build GHZ states. In 14 trapped ions, their coherence decayed with the square of the
  number of qubits, as expected for correlated phase noise [@monz2011fourteen].
- **Dissipation.** Any pure multipartite state can be the unique steady state of an engineered dissipative process,
  reached from any initial state [@kraus2008markov; @verstraete2009dissipation]. See [[reservoir-engineering]].
- **Measurement and feedback.** Real-time feedback prepared and stabilized photon-number states in a cavity
  [@sayrin2011photon]. See [[feedback-control]].

## State transfer

- **Along spin chains.** Even an unmodulated Heisenberg chain transmits a qubit with better-than-classical fidelity
  over tens of spins [@bose2003chain]. With engineered but fixed couplings, the transfer is perfect over any length
  of chain [@christandl2004perfect]. With time-dependent control, the transfer can run at the speed limit
  [@murphy2010chain], and control at one end of the chain can be enough [@burgarth2009local].
- **Between distant nodes.** In a quantum network, a laser pulse can map an atom's state onto a time-symmetric photon
  that a second atom absorbs with unit probability [@cirac1997network]. The microwave version transferred states
  deterministically between superconducting qubits on separate chips [@kurpiers2018transfer].

## Cooling and initialization

Preparing a pure state from a thermal one requires removing entropy, so it needs dissipation or measurement. Optimal
control has been used to design laser cooling of internal molecular degrees of freedom [@bartana1997cooling]. The
third law limits how fast this can go: for general cooling processes, the attainable temperature scales as an inverse
power of the cooling time [@masanes2017thirdlaw]. Fast, unconditional reset of qubits is part of
[[error-correction]] [@magnard2018reset]; see also [[quantum-thermodynamics]].

## In experiments

- **Cold atoms.** Closed-loop optimization sped up atom loading into optical lattices and the crossing of the
  superfluid–Mott-insulator transition more than threefold [@rosi2013fast]. With condensates in optical lattices,
  both a protocol at the speed limit and a robust superadiabatic (transitionless) protocol were realized
  [@bason2012driving]. See [[cold-atoms]].
- **Rydberg arrays.** Optimal control prepared GHZ states of up to 20 atoms [@omran2019cat]. See [[neutral-atoms]].
- **Citizen science.** In a game based on moving atoms with optical tweezers, players found good solutions in
  regimes where purely numerical optimization struggled [@sorensen2016speedlimit].

## Limitations

- Verifying a large entangled state is hard: tomography scales exponentially, and witnesses or fidelity estimates
  replace it.
- A state-to-state solution works only for the initial state it was designed for, while a gate works for all
  inputs. Errors in the initial state propagate.
- Many optimal solutions exist for the same target, and the choice between them should be based on robustness rather
  than nominal fidelity alone.

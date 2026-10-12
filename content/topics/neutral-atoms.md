---
updated: 2026-10-12
status: draft
key_papers:
  - key: jaksch2000rydberg
    note: Proposes fast neutral-atom gates using strong dipole–dipole interactions between Rydberg states — the blockade mechanism.
  - key: saffman2010rydberg
    note: Review of quantum information with Rydberg atoms.
  - key: browaeys2020rydberg
    note: Review of many-body physics with individually controlled Rydberg atoms in tweezer arrays.
  - key: jandura2022timeoptimal
    note: Time-optimal CZ and CCZ pulses for Rydberg atoms, found with optimal control.
  - key: evered2023parallel
    note: 99.5% two-qubit gates on up to 60 atoms in parallel, using single-pulse gates based on optimal control.
  - key: omran2019cat
    note: GHZ states of up to 20 atoms prepared with optimal control of the many-body system.
software:
  - name: Pulser
    url: https://github.com/pasqal-io/Pulser
    note: pulse sequences for neutral-atom arrays, digital and analog, with emulation
---

**Neutral-atom arrays** hold single atoms in optical tweezers and make them interact by exciting them to Rydberg
states, whose strong dipole–dipole interaction blocks double excitation within a few micrometres
[@jaksch2000rydberg; @saffman2010rydberg]. Arrays of hundreds of atoms in arbitrary geometries serve both as analog
quantum simulators and as gate-based processors [@browaeys2020rydberg]. The atoms are identical and the qubits
long-lived. The controls are lasers, often applied globally, and tweezers that can rearrange and move the atoms.

## Building the array

Tweezers are loaded randomly. Imaging and moving the atoms one by one then assembles defect-free arrays in one and
two dimensions [@endres2016arrays; @barredo2016assembler]. Coherent transport of entangled atoms between zones gives
the processor dynamic, non-local connectivity [@bluvstein2022transport].

## Gates

- **Blockade gates.** In the blockade regime, only one atom of a pair can be excited, so the laser pulse acquires a
  phase that depends on both atoms. A CZ gate can be driven by a global pulse that needs no single-site addressing
  [@levine2019parallel].
- **Optimal control.** Shaped, analytic DRAG-type pulses reduce leakage and improve Rydberg-gate fidelity
  [@theis2016rydberg]. Numerical and semi-analytic optimal control found the time-optimal CZ and CCZ pulses,
  smooth and with only a few parameters [@jandura2022timeoptimal]. Fast single-pulse gates of this kind, together
  with dark states that reduce scattering, gave 99.5% fidelity on up to 60 atoms in parallel
  [@evered2023parallel]. See [[gate-synthesis]].
- **Algorithms and logical qubits.** Arrays with individually addressed beams have run multi-qubit algorithms
  [@graham2022multiqubit]. Logical-level control in a zoned architecture has operated up to 280 physical qubits
  [@bluvstein2024logical]. See [[error-correction]].

## Analog control of many-body states

As simulators, Rydberg arrays implement Ising-type spin models with tunable interactions. Ordered phases were prepared
in a 51-atom array [@bernien2017probing], and antiferromagnets in two dimensions with hundreds of atoms
[@scholl2021antiferromagnets], by sweeping the laser detuning. Optimal control prepared GHZ states of up to 20 atoms
[@omran2019cat], following theory proposals for Rydberg lattices [@cui2017rydberg]. For the maximum-independent-set
problem on up to 289 atoms, variational algorithms were optimized in closed loop on the hardware [@ebadi2022mis].
See [[many-body-control]], [[variational-algorithms]] and [[closed-loop]].

## Programming

Pulse-level software such as Pulser expresses analog and digital sequences for neutral-atom devices
[@silverio2022pulser]. See [[pulse-level-compilation]].

## Limitations

- Rydberg states decay and are sensitive to stray electric fields, and laser phase and intensity noise limit gate
  fidelity.
- Atoms are lost and heated, and both need to be detected and replaced during long computations.
- Global control is easy, but local control needs extra beams or light shifts, which bring crosstalk.

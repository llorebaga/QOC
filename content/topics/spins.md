---
updated: 2026-10-12
status: draft
key_papers:
  - key: khaneja2005grape
    note: GRAPE, introduced for designing NMR pulse sequences in coupled spin systems.
  - key: vandersypen2005nmr
    note: Review of the NMR pulse and tomography techniques that served as the first quantum-computing testbed.
  - key: glaser1998unitary
    note: Unitary bounds on spin transformations and pulse sequences that maximize signal in coherent spectroscopy.
  - key: dolde2014entanglement
    note: Optimal control of two NV centres, with high-fidelity single-spin gates and entanglement between them.
  - key: cerfontaine2020closedloop
    note: Optimized, closed-loop-tuned exchange gates for singlet–triplet qubits in GaAs at 99.5% fidelity.
  - key: burkard2023spin
    note: Review of semiconductor spin qubits — single spins, donors, singlet–triplet and exchange-only qubits.
software:
  - name: Spinach
    url: https://github.com/IlyaKuprov/Spinach
    note: spin dynamics simulation for magnetic resonance, with optimal control (GRAPE) built in
---

**Spin systems** are where quantum control became an engineering discipline. In nuclear magnetic resonance (NMR),
electron spin resonance (ESR/EPR) and MRI, radio-frequency and microwave pulses have manipulated spins for decades.
Echoes, composite pulses and adiabatic sweeps all come from this tradition [@hahn1950echo; @levitt1986composite;
@garwood2001sweep]. Today the family also includes solid-state spins: colour centres such as the nitrogen-vacancy
(NV) centre in diamond, and electron spins in semiconductor quantum dots and donors.

## Magnetic resonance

- **The first quantum processors.** NMR provided the earliest testbed for quantum algorithms, with up to seven
  qubits, and developed many of the pulse and tomography techniques other platforms now use [@vandersypen2005nmr].
- **Bounds and optimal sequences.** Unitary dynamics bounds how much signal any pulse sequence can transfer between
  spin states, and optimal sequences reach those bounds [@glaser1998unitary]. Time-optimal control of coupled spins
  was solved with geometric methods [@khaneja2001timeoptimal]. See [[geometric-control]].
- **GRAPE and broadband pulses.** GRAPE was introduced to design NMR pulse sequences [@khaneja2005grape]. Optimal
  control gives excitation and inversion pulses that work over wide ranges of frequency offsets and field strengths
  [@skinner2003broadband; @kobzar2004broadband]. Shaped optimal-control pulses also increased the excitation
  bandwidth in pulsed EPR [@spindler2012epr]. See [[grape]] and [[robust-optimal-control]].
- **Imaging.** Pulse design for MRI was among the first engineering applications of optimal control
  [@conolly1986mri].

## NV centres and other colour centres

The NV centre has a spin that can be initialized and read out optically at room temperature
[@doherty2013nv]. It is a leading platform for nanoscale sensing [@taylor2008magnetometer; @degen2017sensing].
Control tasks include:

- **Gates and entanglement.** Optimal control of two nearby NV centres gave single-spin gates with fidelity of about
  0.99 and, combined with decoupling, entanglement between them [@dolde2014entanglement].
- **Nuclear spins.** Decoupling sequences on the electron spin select and control individual weakly coupled
  $^{13}$C nuclear spins [@taminiau2012nuclear].
- **Robust sensing.** Smooth optimal control made wide-field magnetometry robust to inhomogeneous control amplitudes
  and detunings [@nobauer2015magnetometry]. A cost function built for sensing improved sensitivity to time-varying
  fields [@poggiali2018sensing]. See [[quantum-sensing]] and the review [@rembold2020nvsensing].

## Semiconductor spin qubits

Electron spins in quantum dots are controlled electrically, through gate voltages that tune tunnelling and
exchange, or with microwaves [@loss1998dots; @burkard2023spin]. Coherent manipulation of two coupled spins
established singlet–triplet qubits [@petta2005coherent]. Exchange-based gates require pulse optimization against
charge noise, nuclear-spin noise and leakage. With careful pulse optimization and closed-loop tuning, single-qubit
gates of singlet–triplet qubits in GaAs reached 99.5% fidelity with 0.13% leakage [@cerfontaine2020closedloop].
Silicon processors have crossed the surface-code threshold, with all gate fidelities above 99.5%
[@xue2022threshold]. See [[gate-synthesis]] and [[closed-loop]].

## Limitations

- In ensembles, inhomogeneity of fields and couplings is unavoidable, so robustness costs pulse length.
- Solid-state spins see spin baths and charge noise that are partly non-Markovian; see [[dynamical-decoupling]] and
  [[filter-functions]].
- Electrical control of quantum dots relies on accurate, device-specific models of gate voltages and couplings.

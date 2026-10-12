---
updated: 2026-10-12
status: draft
key_papers:
  - key: koch2007transmon
    note: The transmon — a charge-insensitive Cooper-pair box, and the most widely used superconducting qubit.
  - key: blais2021cqed
    note: Comprehensive review of circuit quantum electrodynamics, the framework for controlling and reading out superconducting qubits.
  - key: motzoi2009drag
    note: DRAG pulse shaping against leakage in weakly anharmonic qubits — the standard single-qubit pulse.
  - key: krantz2019guide
    note: An engineer's guide to superconducting qubits, including their control and readout.
  - key: rol2019netzero
    note: A fast CZ gate with a bipolar flux pulse that suppresses leakage by interference and tolerates line distortion.
  - key: werninghaus2021leakage
    note: Fast single-qubit gates with reduced leakage, found by optimal control and refined on the device.
---

**Superconducting circuits** are electrical circuits of Josephson junctions, capacitors and inductors that behave
as artificial atoms at millikelvin temperatures. They are controlled with microwave pulses and baseband flux pulses,
and read out through coupled microwave resonators, an architecture known as circuit QED [@blais2021cqed]. Coherent
control of a superconducting circuit was first shown with a Cooper-pair box driven by a voltage pulse
[@nakamura1999cooperpair]. Today the platform runs some of the largest quantum processors, and it shapes much of
current pulse-design practice [@krantz2019guide; @kjaergaard2020superconducting].

## The control problem

- **Weak anharmonicity.** The transmon trades anharmonicity for insensitivity to charge noise [@koch2007transmon].
  Its levels are almost equally spaced, so fast pulses leak into the second excited state. Leakage and the phase
  errors that come with it set the speed limit of single-qubit gates. DRAG [@motzoi2009drag], numerically optimized
  pulses [@werninghaus2021leakage] and virtual $Z$ gates [@mckay2017virtualz] are the standard remedies. See
  [[drag]].
- **Other circuits.** The fluxonium has a much larger anharmonicity and long coherence times
  [@manucharyan2009fluxonium; @nguyen2019fluxonium]. Its gates face a different trade-off: lower qubit frequencies
  and more complex level structures.
- **Many controls, one chip.** Qubits are coupled by fixed capacitors, tunable couplers or shared resonators. This
  brings frequency crowding, crosstalk and parasitic $ZZ$ interactions, which pulses must avoid or cancel
  [@theis2016crowded; @sung2021coupler]. See [[gate-synthesis]].
- **Signal distortion.** Control pulses pass through cables, filters and attenuators that distort them. Distortions
  can be measured with the qubit itself and pre-compensated [@gustavsson2013distortions; @jerger2019vna;
  @rol2020distortion]. See [[model-learning]] and [[control-hardware]].

## Entangling gates

- **Microwave-only gates.** The cross-resonance gate drives one fixed-frequency qubit at the frequency of its
  neighbour [@rigetti2010crossresonance]. Calibrating its full Hamiltonian and cancelling the unwanted terms raised
  its fidelity above 99% [@sheldon2016crossresonance].
- **Flux-pulsed gates.** Tuning frequencies with flux brings $|11\rangle$ close to $|02\rangle$ and accumulates a
  conditional phase. Shaping the flux pulse with optimal window functions makes the interaction adiabatic and fast
  [@martinis2014adiabatic], and gates of this type reached the surface-code threshold [@barends2014threshold]. A
  bipolar ("net-zero") flux pulse suppresses leakage by interference, includes an echo, and is robust to slow
  distortions in the flux line [@rol2019netzero].
- **Couplers and parametric drives.** Tunable couplers designed beyond the dispersive approximation gave CZ and
  $ZZ$-free iSWAP gates at 99.76% and 99.87% [@sung2021coupler]. Modulating a qubit frequency activates parametric
  entangling gates [@reagor2018parametric].

## Readout, reset and bosonic modes

Dispersive readout reached 98.25% fidelity in 48 ns [@walter2017readout]. Shaped measurement pulses empty the readout
resonator quickly [@mcclure2016reset], and microwave-driven protocols reset a qubit in under 500 ns
[@magnard2018reset]. See [[error-correction]]. High-quality microwave cavities coupled to transmons host bosonic
qubits controlled by numerically optimized pulses or gate sequences [@heeres2017logical; @eickbusch2022ecd]. See
[[bosonic-control]].

## Optimal control in practice

Superconducting devices are a natural target for model-based optimal control, since their Hamiltonians are known from
circuit theory. Pulses are optimized on a model and then refined on the device, with randomized benchmarking as the
cost [@kelly2014orbit], by hybrid schemes [@egger2014adhoc] or with integrated calibration and characterization tools
[@wittler2021c3]. See [[grape]], [[closed-loop]] and [[pulse-level-compilation]].

## Limitations

- Device parameters drift and vary between fabrication runs, so every pulse needs calibration and recalibration.
- Two-level-system defects and other coupling to the environment change in time and are hard to model.
- Wiring and heat load from many control lines limit how far the architecture scales; see [[control-hardware]].

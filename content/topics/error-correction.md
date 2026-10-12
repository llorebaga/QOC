---
updated: 2026-10-12
status: draft
key_papers:
  - key: terhal2015memories
    note: Review of quantum error correction for quantum memories, from stabilizer codes to topological order.
  - key: fowler2012surface
    note: The surface code as an architecture — the gates, measurements and cycle times it needs.
  - key: google2025threshold
    note: Surface-code memories below threshold, with real-time decoding, on superconducting qubits.
  - key: mcewen2021leakage
    note: Leakage creates correlated errors in error correction; a dedicated reset protocol removes them.
  - key: rosenblum2018faulttolerant
    note: Error detection designed so that ancilla errors do not spread to the logical qubit.
  - key: kosut2008robustqec
    note: Encoding and recovery optimized by semidefinite programming, robust to uncertainty in the noise.
---

**Quantum error correction** (QEC) protects quantum information by encoding it redundantly, repeatedly measuring
error syndromes and correcting the errors they reveal [@shor1995scheme; @steane1996codes; @terhal2015memories]. It
works only if the physical operations are good enough, below the code's threshold, and if errors stay local and
uncorrelated. Every QEC cycle is a sequence of control tasks — entangling gates, measurements, resets, real-time
decisions — so the quality of control decides whether encoding helps at all.

## The control stack of a QEC cycle

- **Gates.** The surface code needs only nearest-neighbour gates and tolerates errors near 1% per step
  [@fowler2012surface]. Superconducting and neutral-atom processors have reached this regime
  [@barends2014threshold; @evered2023parallel]. See [[gate-synthesis]].
- **Measurement.** Syndrome readout must be fast and accurate, and must not disturb neighbouring qubits. Careful
  design of superconducting dispersive readout reached 98.25% fidelity in 48 ns [@walter2017readout]. Five qubits
  were read out in one multiplexed channel with 80 ns pulses [@heinsoo2018readout]. Shaped measurement pulses empty
  the readout resonator quickly so that the next cycle can start [@mcclure2016reset].
- **Reset.** Ancillas must return to the ground state after each measurement. An all-microwave protocol resets a
  transmon in under 500 ns with 0.2% residual excitation, without feedback [@magnard2018reset].
- **Leakage.** Population in non-computational levels is long-lived and mobile, which makes errors correlated in
  space and time. A reset protocol that removes leakage from all relevant levels lowered logical error rates and
  stabilized their suppression with system size [@mcewen2021leakage]. See [[drag]].
- **Real-time decoding.** Corrections must be decided faster than errors accumulate. Increasing the surface-code
  distance first improved logical performance modestly [@google2023scaling]. Later, distance-5 and distance-7
  memories ran below threshold, suppressing the logical error by a factor of 2.14 per distance step and outliving
  their best physical qubit, with a real-time decoder [@google2025threshold]. Reconfigurable atom arrays have run
  logical circuits with up to 280 physical qubits [@bluvstein2024logical]. See [[control-hardware]].

## Optimizing codes and recoveries

Standard codes correct a fixed set of errors exactly. If the noise is known, encoding and recovery can be optimized
for it, as a control problem on quantum channels. Iterative algorithms find optimal encodings and decodings for a
given channel [@reimpell2005iterative]. The optimal recovery for a given code is a semidefinite program
[@fletcher2007recovery]. Optimizing encoding and recovery together can make them robust to uncertainty in the
noise [@kosut2008robustqec]. See [[polynomial-optimization]] for related convex methods.

QEC can also be continuous. Weak measurements and Hamiltonian feedback protect states between discrete correction
cycles [@ahn2002continuous]. Reinforcement learning can discover feedback strategies of this kind
[@fosel2018feedback], and a learning agent has acted in real time on a superconducting qubit
[@reuer2023realtime]. See [[feedback-control]] and [[machine-learning-control]].

## Fault-tolerant operations

The ancillas used to detect errors are often noisier than the encoded qubit, and their errors must not spread to it.

- Error detection can be made fault-tolerant to ancilla errors by using higher ancilla levels
  [@rosenblum2018faulttolerant]. Gates can be made error-transparent, keeping the device's tolerance to errors
  that occur before or during them [@kapit2018transparent]. On a cavity-encoded qubit, ancilla-induced errors were
  corrected in real time during the gate [@reinhold2020errorcorrected].
- Noise bias is a resource. Cat qubits stabilized by two-photon dissipation show an exponential suppression of bit
  flips as the cat grows, at the price of a linear increase of phase flips [@lescanne2020bitflips]. Bias-preserving
  CX gates on such qubits raise the fault-tolerance threshold and reduce overhead [@puri2020biaspreserving].

## Bosonic codes

A single oscillator can host an error-correctable qubit: cat codes [@mirrahimi2014cat; @ofek2016qec] or grid
(GKP) codes [@gottesman2001gkp; @campagneibarcq2020gkp]. A GKP memory with parameters tuned by reinforcement learning
outlived the best of its physical components by a factor of 2.27 [@sivak2023beyond]. Logical operations on such codes
are designed by numerical optimal control of the cavity–ancilla system [@heeres2017logical] or built from sequences of
simpler operations [@eickbusch2022ecd]. See
[[bosonic-control]] and [[reservoir-engineering]].

## Limitations

- Physical gate fidelities are a proxy. What matters is the logical error rate, which depends on correlations,
  leakage and the decoder, and these are rarely part of the control objective.
- A large code needs thousands of calibrated pulses that drift. Calibration and recalibration have to be automated.
- Feedback latency is set by electronics and decoders, not by the quantum hardware alone.

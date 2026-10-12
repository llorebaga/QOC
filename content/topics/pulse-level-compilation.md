---
updated: 2026-10-12
status: draft
key_papers:
  - key: shi2019aggregated
    note: Aggregates circuit instructions into multi-qubit blocks and compiles each block into a custom optimal-control pulse.
  - key: gokhale2019partial
    note: Partial compilation — pre-computes optimal pulses for fixed blocks so that variational algorithms are not slowed by compilation.
  - key: earnest2021pulseefficient
    note: Pulse-efficient transpilation, which scales calibrated cross-resonance pulses instead of decomposing into CNOTs.
  - key: alexander2020qiskitpulse
    note: Qiskit Pulse — pulse-level programming of cloud quantum computers (since removed from Qiskit).
  - key: cross2022openqasm3
    note: OpenQASM 3, an assembly language with real-time control flow and pulse-level calibration descriptions.
software:
  - name: Pulser
    url: https://github.com/pasqal-io/Pulser
    note: pulse-level and analog programming of neutral-atom devices, with a QuTiP-based emulator
  - name: qutip-qip
    url: https://github.com/qutip/qutip-qip
    note: compiles circuits to pulses on simulated processors and simulates them with noise
---

**Pulse-level compilation** turns a quantum program into the control signals that run it. A standard compiler maps
a circuit onto native gates and replaces each gate with a pulse from a calibrated library. Pulse-level compilation
breaks that abstraction where it pays off. It optimizes pulses for whole blocks of gates, reshapes calibrated
pulses to implement gates the library lacks, or lets programs specify pulses directly. The goal is the same as in
[[gate-synthesis]] — shorter, more accurate operations — but applied across a whole program.

## The standard pipeline

A circuit is decomposed into native gates, mapped and routed onto the device's connectivity, and scheduled as a
sequence of pulses. Some operations cost nothing: $Z$ rotations can be implemented "virtually" as phase changes of
later drives [@mckay2017virtualz]. Calibration keeps the library accurate, and closed-loop tune-up can use
randomized benchmarking as its cost [@kelly2014orbit] or fit a device model along the way [@wittler2021c3]. See
[[closed-loop]] and [[model-learning]].

## Compiling blocks with optimal control

- **Aggregated instructions.** The gate set is an artificial boundary: a block of gates on a few qubits can be
  implemented by one pulse much shorter than the sum of its gates. Aggregating instructions into blocks of up to 10
  qubits and compiling each block with optimal control reduced program latency [@shi2019aggregated]. See
  [[grape]].
- **Compilation latency.** Optimal-control compilation is slow, which is a problem when compilation and execution
  alternate, as in [[variational-algorithms]]. Partial compilation pre-computes pulses for the parameter-independent
  blocks, giving pulse speed-ups of 1.5–3× at a small fraction of the compilation cost [@gokhale2019partial].
  Static pre-compilation combined with accelerated dynamic compilation reduces it further [@cheng2020accqoc]. GPUs and
  automatic differentiation speed up the underlying optimization [@leung2017gpu].

## Compiling from calibrated pulses

Full optimal control needs an accurate model of the device. A lighter approach starts from the existing
calibrations. Building pulses from calibrated gates rather than by optimal control gave 1.6× lower error rates and
2× faster execution on IBM devices [@gokhale2020openpulse]. Scaling calibrated cross-resonance pulses exposes a
continuous family of two-qubit gates. Combined with a Cartan decomposition of SU(4), this reduced the error of
arbitrary two-qubit gates by up to 50% and shortened QAOA schedules by up to 52%, with no extra calibration
[@earnest2021pulseefficient].

## Pulse-level programming

- **Interfaces.** OpenPulse specified how pulse schedules are sent to cloud hardware [@mckay2018openpulse]. Qiskit
  Pulse implemented it, from calibrating cross-resonance gates to Hamiltonian characterization through the cloud
  [@alexander2020qiskitpulse]. Qiskit deprecated its pulse module in version 1.3 (November 2024) and removed it in
  version 2.0 (March 2025). OpenQASM 3 adds real-time control flow and lets programs describe operations at several
  levels, down to calibrations [@cross2022openqasm3].
- **Analog and neutral-atom devices.** Pulser programs neutral-atom arrays at the pulse level, in digital and analog
  modes [@silverio2022pulser].
- **Simulation.** Circuits can be compiled to pulses on simulated processors and run with realistic noise
  [@li2022qutipqip].
- **Variational algorithms at the pulse level.** Pulses themselves can be the variational parameters, as in ctrl-VQE
  [@meitei2021ctrlvqe] or adjoint-based pulse optimization for neutral-atom hardware [@dekeijzer2023pulsevqoc]. See
  [[variational-algorithms]].

## The trade-off

Gates are an abstraction that pays for itself. They are calibrated once, benchmarked individually, portable across
devices, and come with the simple error models that error correction relies on. Pulse-level compilation gains time
and fidelity by giving some of this up. Its pulses are device-specific, harder to benchmark and only as good as the
model or calibration behind them.

## Limitations

- Custom block pulses are hard to characterize: randomized benchmarking applies to gate sets, not to one-off blocks.
- Calibrations drift, and every additional pulse type adds to the calibration burden. See [[control-hardware]].
- Access to pulse-level control depends on the hardware provider and can change, as the removal of Qiskit Pulse
  showed.

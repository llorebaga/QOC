---
updated: 2026-10-11
status: draft
key_papers:
  - key: granade2012robust
    note: Online Bayesian Hamiltonian learning with sequential Monte Carlo and adaptive experiment design, robust to drifting parameters and unknown noise.
  - key: burgarth2012identification
    note: A general framework for quantum system identification — what can be learned in principle from a given experiment.
  - key: rol2020distortion
    note: Cryoscope. Measuring and correcting on-chip distortion of control pulses directly with the qubit.
  - key: wittler2021c3
    note: An integrated workflow — optimal control, calibration and model learning — applied to superconducting qubits.
  - key: genois2025ocml
    note: Optimal control on a model learned by physics-inspired machine learning from experimental data.
---

Model-based optimal control is only as good as the model. To apply open-loop optimized pulses, one must know the
Hamiltonian parameters, the noise and dissipation, and the **distortions** the control electronics impose on the pulses.
**System identification** — learning this model from data — closes the gap between the simulated and the real device.
It is the model-based counterpart of [[closed-loop|closed-loop optimization]]: instead of optimizing blindly on the
device, learn a better model, then optimize on it.

## What there is to learn

- **Hamiltonian parameters** — frequencies, couplings, anharmonicities, cross-talk.
- **Noise and dissipation** — decay and dephasing rates, Lindblad operators, noise spectra.
- **The control chain** — transfer functions of cables and filters, amplifier non-linearities, timing offsets.

## Learning Hamiltonians

- **Bayesian inference** treats the unknown parameters as random variables and updates their distribution after each
  measurement. With sequential Monte Carlo and adaptive experiment design, it can run *online*, track parameters that
  change between experiments, and tolerate unknown noise [@granade2012robust].
- **Quantum-assisted learning.** A trusted quantum simulator can learn the Hamiltonian of a larger, untrusted one
  [@wiebe2014hamiltonian]. A photonic quantum simulator has been used this way to learn the Hamiltonian of an NV-centre
  spin [@wang2017experimental].
- **Learning the model itself.** An automated, machine-learning agent can propose and test *candidate Hamiltonians*, not
  only their parameters, and identify which interactions are present [@gentile2021learning].
- **Time traces.** Ideas from linear systems theory reconstruct Hamiltonian parameters from time records of a few
  observables [@zhang2014timetraces].
- **Many-body systems.** Local Hamiltonians can be recovered from local measurements, with resources that scale
  linearly with system size [@bairey2019local]. Polynomially many local measurements on thermal states suffice to learn
  an interacting Hamiltonian accurately [@anshu2021sample].

What can be learned is limited in principle. Controllable closed systems, for instance, can be identified only up to a
unitary change of basis, and prior knowledge or particular measurements can help [@burgarth2012identification].

## Learning noise and dissipation

Lindblad tomography reconstructs both the Hamiltonian and the Lindblad operators of a multi-qubit processor
[@samach2022lindblad]. Learning the most accurate Markovian model from time-series data can be cast as a polynomial
optimization and solved globally [@popovych2022identification]; see [[polynomial-optimization]]. Noise *spectra* are
measured with tailored pulse sequences; see [[filter-functions]].

## Learning the control chain

Pulses arrive distorted. On superconducting processors, the step response of flux-control lines has been measured
with the qubit itself (Cryoscope) and compensated by real-time digital filters [@rol2020distortion]. A qubit can also act
as a vector network analyzer, measuring a control line's transfer function in the frequency domain and improving
entangling gates [@jerger2019vna]. Once known, distortions are built into the optimization; see
[[pulse-parametrization]] and [[control-hardware]].

## Machine learning and digital twins

Physics-inspired ("quantum-tailored") machine-learning models can be trained on experimental data to characterize a
superconducting qubit [@genois2021mlchar]. Optimizing controls on such a learned model yields pulses tailored to the actual
device, including spurious modes and distortions [@genois2025ocml]. Integrated toolsets cycle between optimal control,
calibration and model refinement [@wittler2021c3].

## Verifying the result

Learned models and optimized operations must be validated. Characterization and benchmarking methods — randomized
benchmarking, process and gate-set tomography — quantify how well the operations work [@eisert2020certification].
Gate-set tomography, for example, can certify errors below rigorous fault-tolerance thresholds
[@blumekohout2017gst]. See [[problem-formulation]].

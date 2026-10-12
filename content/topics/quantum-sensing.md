---
updated: 2026-10-12
status: draft
key_papers:
  - key: braunstein1994statistical
    note: The quantum Fisher information as a statistical distance — the basis of the quantum Cramér–Rao bound.
  - key: degen2017sensing
    note: Review of quantum sensing, with the control sequences used by spin and atomic sensors.
  - key: demkowicz2012elusive
    note: Under generic decoherence, the quantum advantage in metrology shrinks asymptotically to a constant factor.
  - key: pang2017adaptive
    note: For time-dependent signals, control is generally needed to reach the optimal Fisher information — and can beat the usual time scaling.
  - key: poggiali2018sensing
    note: Optimal control with a cost function built for sensing, demonstrated on an NV centre.
  - key: zhou2018heisenberg
    note: When and how quantum error correction restores Heisenberg-limited sensing under Markovian noise.
---

**Quantum sensing** estimates a parameter — a magnetic field, a frequency, a phase, a force — from its effect on
a quantum system. Control enters at every stage: preparing a sensitive probe state, shaping its evolution so that
it picks up the signal and rejects noise, and choosing the measurements. The tasks span magnetometry with spins,
atomic clocks and interferometers, and optical phase estimation [@degen2017sensing; @giovannetti2011advances].

## The figure of merit

For $\nu$ repetitions, the error of any unbiased estimator of a parameter $\omega$ obeys the quantum Cramér–Rao bound
$\Delta\omega \ge 1/\sqrt{\nu F_Q}$, where $F_Q$ is the quantum Fisher information of the final state
[@braunstein1994statistical]. $F_Q$ is the natural objective for control. With $N$ independent probes, the error
scales as $1/\sqrt N$, the standard quantum limit. Entangled probes can reach the Heisenberg scaling $1/N$ in the
ideal case [@giovannetti2011advances]. Collective states of atomic ensembles, such as spin-squeezed states, are the
best-developed route to this enhancement [@pezze2018ensembles]. Preparing them is a [[state-preparation]] problem.

## Shaping the evolution

- **Filtering the signal.** Pulse sequences make a sensor respond to fields at selected frequencies while averaging
  out noise. The same sequences that protect a qubit act as frequency filters ([[filter-functions]]
  [@cywinski2008dephasing]). This turns spins into lock-in detectors of oscillating fields: nanoscale magnetometers
  based on NV centres in diamond [@taylor2008magnetometer], sensors of individual weakly coupled nuclear spins
  [@taminiau2012nuclear], and noise spectrometers [@alvarez2011spectrum]. See [[dynamical-decoupling]].
- **Control raises the bound.** Usually the dynamics is taken as fixed and only the probe state and measurement are
  optimized. Adding controls during the evolution raises the attainable precision, beyond the limits the coherence
  time imposes on standard schemes [@liu2017estimation]. Optimal feedback controls restore the expectation that a
  longer sensing time gives better precision [@yuan2015feedback]. For time-dependent Hamiltonians, the optimal
  control is generally adaptive. For a qubit in a rotating field, it gives a $T^4$ scaling of the Fisher information
  in the rotation frequency, beyond the usual $T^2$ [@pang2017adaptive].
- **Optimal control built for sensing.** Standard gate or state fidelities are the wrong cost here. A sensing cost
  function accounts for both the unknown field and the noise. Optimized with it, controls on an NV centre improved
  the sensitivity to a broad set of time-varying fields [@poggiali2018sensing]. Optimal control for NV-centre sensing
  has been reviewed in [@rembold2020nvsensing]. See [[spins]].

## Adaptive measurements

Choosing each measurement based on earlier outcomes is feedback control of the estimation. Adaptive phase
measurements of optical modes beat non-adaptive ones [@wiseman1995adaptive]. With adaptive, multi-pass protocols,
phase estimation reached Heisenberg-limited scaling without entangled states [@higgins2007heisenberg]. See
[[feedback-control]].

## Noise and the Heisenberg limit

- **Decoherence caps the gain.** For generic noise, such as dephasing, depolarization or loss, the asymptotic quantum
  advantage reduces to a constant factor rather than a change of scaling
  [@escher2011noisy; @demkowicz2012elusive]. In the presence of noise, entangled strategies and ancillas do help,
  unlike in the noiseless case [@demkowicz2014noise].
- **Error correction can restore it.** If the noise and the signal act differently, error correction can suppress
  the noise without erasing the signal and restore Heisenberg scaling
  [@kessler2014qecmetrology; @dur2014qecmetrology]. For Markovian noise there is a necessary and sufficient condition
  for this, and the optimal code follows from a semidefinite program [@zhou2018heisenberg]. See
  [[error-correction]].

## Limitations

- The quantum Cramér–Rao bound is asymptotic in the number of repetitions. Few-shot and prior-dependent problems
  need Bayesian figures of merit.
- Control pulses have their own errors and bandwidth limits, which add noise and distort the filter.
- Optimizing for a signal requires a model of it, and a sensor tuned for one signal can be worse for others.

---
updated: 2026-10-12
status: draft
key_papers:
  - key: palao2003unitary
    note: Optimal control for unitary transformations — the phase-insensitive gate objective used ever since.
  - key: zhang2003geometric
    note: The geometry of two-qubit gates up to local operations (the Weyl chamber) and a criterion for perfect entanglers.
  - key: motzoi2009drag
    note: DRAG — pulse shaping that suppresses leakage and phase errors in weakly anharmonic qubits.
  - key: molmer1999entanglement
    note: The Mølmer–Sørensen gate, which entangles trapped ions without full control of their motion.
  - key: jandura2022timeoptimal
    note: Time-optimal CZ and CCZ gates for Rydberg atoms, found by optimal control; the basis of later record-fidelity experiments.
  - key: kelly2014orbit
    note: Closed-loop gate optimization with randomized benchmarking as the cost function.
---

**Gate synthesis** designs the controls that make a quantum device implement a target unitary — a single-qubit
rotation, an entangling two-qubit gate, a multi-qubit or qudit operation — with an error small enough for
computation. The fault-tolerance threshold of the surface code is about 1% error per operation
[@barends2014threshold], and practical overheads need errors well below it. Gate synthesis is the most common task in quantum optimal control and the main driver of
its methods.

## The problem

- **Objective.** The standard figure of merit compares the achieved evolution with the target, ignoring a global
  phase, $F = |\mathrm{Tr}(U_\mathrm{target}^\dagger U(T))|^2/d^2$ [@palao2003unitary]. Average gate fidelities
  follow from it [@nielsen2002fidelity; @pedersen2007fidelity]. When the device has more levels than the
  computational space, $U(T)$ is projected onto that space, so population lost from it lowers $F$. With dissipation,
  the objective is defined on the dynamical map [@goerz2014dissipative]. See [[problem-formulation]].
- **Targets up to local operations.** For entangling gates, often only the nonlocal part matters. Two-qubit gates up
  to single-qubit operations form a tetrahedron (the Weyl chamber), and exactly half of the nonlocal gates are
  perfect entanglers [@zhang2003geometric]. One can optimize for *any* perfect entangler rather than a specific gate
  [@watts2015perfect].
- **Existence and time.** [[controllability|Controllability]] guarantees that a solution exists for long enough
  times. [[quantum-speed-limits|Speed limits]] and [[geometric-control]] set how short it can be. Building blocks of
  quantum algorithms can be synthesized directly, which can be faster than a decomposition into elementary gates
  [@schulteherbruggen2005synthesis]. Globally optimal solutions can be certified with
  [[polynomial-optimization]] [@baladagaggioli2025gates].

## The errors control must handle

- **Leakage.** Weakly anharmonic qubits such as transmons leak into higher levels when driven fast. DRAG removes
  leakage and phase errors to leading order [@motzoi2009drag]. Leakage can be measured and suppressed
  [@chen2016leakage], and numerically optimized pulses reduce it further in fast gates [@werninghaus2021leakage].
  Virtual $Z$ gates, implemented as phase changes of later drives, correct rotation errors at no cost in time
  [@mckay2017virtualz]. See [[drag]].
- **Crosstalk.** Crosstalk covers many physical effects that make an operation on some qubits depend on others. It
  can be defined rigorously and detected operationally [@sarovar2020crosstalk]. Control can address it: analytic
  pulses drive simultaneous gates in frequency-crowded systems [@theis2016crowded], an extra drive tone cancels
  unwanted terms of the cross-resonance interaction [@sheldon2016crossresonance], and coupler controls designed
  beyond the dispersive approximation remove leakage to the coupler and parasitic $ZZ$ terms [@sung2021coupler].
- **Decoherence.** Shorter gates lose less coherence, which is why time-optimal solutions matter. Open-system
  optimization takes the loss into account directly; see [[open-system-control]].
- **Model errors.** Pulses optimized on an imperfect model are refined on the device, with randomized benchmarking
  as the cost [@kelly2014orbit] or by hybrid model-based and closed-loop schemes [@egger2014adhoc]. See
  [[closed-loop]] and [[robust-optimal-control]].

## Entangling gates on different platforms

- **Superconducting qubits.** The cross-resonance gate entangles fixed-frequency qubits with microwaves alone
  [@rigetti2010crossresonance]. Its fidelity rose above 99% once its full Hamiltonian was calibrated and the unwanted
  terms cancelled [@sheldon2016crossresonance]. Alternatives include parametrically activated gates
  [@reagor2018parametric] and tunable couplers, which reached 99.76% for CZ and 99.87% for iSWAP [@sung2021coupler].
  See [[superconducting]].
- **Trapped ions.** The Mølmer–Sørensen gate works even with ions in thermal motion [@molmer1999entanglement]. In
  long chains, many motional modes take part, and optimally shaped, segmented pulses control the coupling to all of
  them [@choi2014multimode]. Laser-driven gates have reached 99.9% for two qubits and single-qubit errors of a few
  $10^{-5}$ [@ballance2016hyperfine; @gaebler2016universal]. See [[trapped-ions]].
- **Neutral atoms.** The Rydberg blockade gives fast entangling gates [@jaksch2000rydberg]. A CZ gate driven by a
  global laser pulse avoids single-site addressing [@levine2019parallel]. Optimal control found time-optimal CZ and
  CCZ pulses with only a few parameters [@jandura2022timeoptimal]. Single-pulse gates of this kind reached 99.5%
  fidelity on up to 60 atoms in parallel [@evered2023parallel]. See [[neutral-atoms]].
- **Qudits.** Using more than two levels per carrier, a trapped-ion processor achieved universal control of qudits
  with up to seven levels [@ringbauer2022qudit].

## Measuring success

Gate errors near $10^{-4}$ cannot be resolved by process tomography, which is itself limited by state-preparation
and measurement errors. Randomized benchmarking measures the average error of long random sequences instead
[@knill2008benchmarking; @magesan2011benchmarking]. Gate set tomography gives a self-consistent model of all the
operations [@blumekohout2017gst]. See [[model-learning]].

## Limitations

- An isolated gate's fidelity is not its performance in a circuit. Crosstalk, spectator qubits, drift and
  non-Markovian noise appear only in context.
- Pulses that exploit fine details of a model can be fragile, so robustness has to be traded against speed.
- Calibration drifts, and keeping many optimized pulses calibrated on a large device is an engineering problem in
  its own right. See [[pulse-level-compilation]].

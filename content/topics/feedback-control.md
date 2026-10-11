---
updated: 2026-10-12
status: draft
key_papers:
  - key: wiseman2009book
    note: The textbook on quantum measurement and control — continuous measurement, filtering and feedback.
  - key: wiseman1993homodyne
    note: Quantum theory of optical feedback based on homodyne detection — the foundation of Markovian (direct) feedback.
  - key: doherty1999estimation
    note: Feedback based on continuous state estimation, closely analogous to classical LQG control.
  - key: sayrin2011photon
    note: Real-time quantum feedback prepares and stabilizes photon-number states of a microwave cavity.
  - key: zhang2017feedback
    note: A broad review of quantum feedback — theory, experiments and applications.
---

**Measurement-based feedback** steers a quantum system using information gained *while* it evolves. A measurement
record is processed in real time, often into an estimate of the quantum state, and the controls are adjusted
accordingly. This lets control react to stochastic events: random measurement back-action, noise, errors. Open-loop
pulses cannot do that. It is the quantum analogue of classical feedback control, with one essential difference:
measuring disturbs the system.

## Continuous measurement and quantum filtering

Under continuous weak measurement — for example homodyne detection of a field leaking from a cavity — the state
conditioned on the measurement record evolves stochastically. In one common form,

$$d\rho = -i[H,\rho]\,dt + \mathcal D[c]\rho\,dt + \sqrt{\eta}\,\mathcal H[c]\rho\,dW,$$

where $c$ is the measurement operator, $\mathcal D[c]\rho = c\rho c^\dagger - \tfrac12\{c^\dagger c, \rho\}$ the
dissipator, $\mathcal H[c]\rho = c\rho + \rho c^\dagger - \mathrm{Tr}\big[(c + c^\dagger)\rho\big]\rho$ the measurement
back-action, $\eta$ the detection efficiency and $dW$ the innovation of the measured current [@wiseman2009book]. The
mathematically rigorous form of this state estimation is **quantum filtering** [@belavkin1992filtering;
@bouten2007filtering].

## Feedback strategies

- **Markovian (direct) feedback.** The measured current is fed back directly as a control Hamiltonian, without
  explicit state estimation [@wiseman1993homodyne].
- **Estimation-based (Bayesian) feedback.** The full conditional state is tracked and the control is a function of it.
  For linear systems this is closely analogous to classical linear-quadratic-Gaussian (LQG) control
  [@doherty1999estimation]. Global stabilization of states using filters and geometric control is analysed in
  [@mirrahimi2007stabilizing]; see [[lyapunov-control]].
- **Measurement as the control.** Slowly varying the measured observable drags the state along its eigenstate through the
  quantum Zeno effect. This has been demonstrated with a superconducting qubit [@hacohengourgy2018zeno] and optimized
  as a control protocol [@lewalle2024zeno].
- **Learned policies.** Reinforcement learning discovers feedback strategies from data, including error correction and
  real-time feedback on FPGAs [@fosel2018feedback; @reuer2023realtime]. Feedback-GRAPE optimizes
  measurement-conditioned strategies by gradients [@porotti2023grapefeedback]. See [[machine-learning-control]].

## Landmark experiments

- **Cavity QED.** Real-time feedback prepared and stabilized photon-number (Fock) states of a microwave cavity
  [@sayrin2011photon].
- **Superconducting qubits.** Continuous weak measurement and feedback stabilized Rabi oscillations
  [@vijay2012rabi]. Parity measurement plus feedback created deterministic entanglement between two qubits
  [@riste2013entanglement]. Real-time error correction extended the lifetime of a bosonic qubit
  [@ofek2016qec]; see [[error-correction]].
- **Mechanical motion.** Measurement-based control has cooled and controlled the motion of mechanical resonators
  [@rossi2018mechanical]. Real-time optimal control — Kalman filtering plus optimal feedback — has controlled the
  quantum trajectory of a levitated nanoparticle at room temperature [@magrini2021mechanical].

## Measurement versus coherent feedback

Instead of measuring, the output of a system can be processed by another *quantum* system and fed back coherently,
avoiding measurement back-action [@lloyd2000coherent]. When each approach is better is a question of linear
systems theory; see [[linear-quantum-systems]]. Autonomous stabilization by engineered dissipation is the limit with no
processing at all; see [[reservoir-engineering]].

## Practical constraints

- **Latency.** The loop must be much faster than the system's dynamics and decoherence, which drives the use of FPGAs
  and dedicated control hardware; see [[control-hardware]].
- **Efficiency.** Lost measurement information (finite $\eta$) adds noise that feedback cannot remove.
- **Model accuracy.** State estimation requires a good model of the measurement and the dynamics; see
  [[model-learning]].

Uses include state stabilization, cooling, error correction and adaptive sensing ([[quantum-sensing]]).

---
updated: 2026-10-12
status: draft
key_papers:
  - key: farhi2014qaoa
    note: Introduces QAOA — alternating cost and mixer Hamiltonians, with the switching times optimized classically.
  - key: peruzzo2014vqe
    note: Introduces the variational quantum eigensolver, demonstrated on a photonic processor.
  - key: yang2017pmpvqa
    note: Applies Pontryagin's principle to variational algorithms and argues for bang-bang (QAOA-like) protocols.
  - key: magann2021pulses
    note: Perspective that puts variational algorithms and optimal control in one hierarchy of variational optimization, from circuits to pulses.
  - key: larocca2022barren
    note: Uses the dynamical Lie algebra, a controllability tool, to diagnose barren plateaus.
  - key: cerezo2021vqa
    note: Broad review of variational quantum algorithms, their applications and their trainability problems.
software:
  - name: PennyLane
    url: https://github.com/PennyLaneAI/pennylane
    note: differentiable variational circuits, including pulse-level programs with parametrized Hamiltonians
---

A **variational quantum algorithm** (VQA) runs a parametrized evolution $U(\boldsymbol\theta)$ on a quantum device,
measures a cost such as an energy $C(\boldsymbol\theta) = \langle\psi_0|U^\dagger(\boldsymbol\theta)\,H\,
U(\boldsymbol\theta)|\psi_0\rangle$, and updates the parameters with a classical optimizer
[@cerezo2021vqa; @bharti2022nisq]. The best-known examples are the variational quantum eigensolver (VQE)
[@peruzzo2014vqe] and the quantum approximate optimization algorithm (QAOA) [@farhi2014qaoa]. Read as control
problems, the parameters are controls, the cost is a figure of merit, and the hybrid loop is
[[closed-loop|closed-loop optimization]] on hardware. VQAs and optimal control are variational optimization at two
levels of abstraction, circuits and pulses. Results move between them in both directions [@magann2021pulses].

## QAOA is bang-bang control

QAOA applies $p$ alternating layers,

$$
|\psi(\boldsymbol\gamma, \boldsymbol\beta)\rangle = e^{-i\beta_p H_M} e^{-i\gamma_p H_C} \cdots
e^{-i\beta_1 H_M} e^{-i\gamma_1 H_C}\, |\psi_0\rangle ,
$$

where $H_C$ encodes the cost function and $H_M$ is a "mixer" [@farhi2014qaoa]. This is the evolution under
$H(t) = u(t) H_C + [1-u(t)] H_M$ with a control $u(t) \in \{0, 1\}$ that alternates between its two values in $2p$
segments, whose durations $\gamma_k, \beta_k$ are the parameters. In other words, it is bang-bang control. Three control-theoretic results frame it:

- **Optimal protocols.** Pontryagin's principle has been used to argue that the optimal protocols at fixed total time
  are bang-bang [@yang2017pmpvqa]. A later analysis found that generic optimal protocols are bang–anneal–bang, with a
  smooth annealing segment between pulsed ends [@brady2021annealing]. See [[pmp]].
- **Annealing and beyond.** A smooth $u(t)$ that varies slowly is quantum annealing [@kadowaki1998annealing] and
  adiabatic quantum computation [@albash2018aqc], which QAOA can approximate at large depth. Optimized QAOA can also
  learn *non-adiabatic* mechanisms that get around the small spectral gaps where annealing fails [@zhou2020qaoa].
- **Universality.** Whether alternating two fixed Hamiltonians generates every unitary is a
  [[controllability]] question. For one-dimensional cost Hamiltonians with nearest-neighbour $ZZ$ terms, the precise
  conditions for universality have been proven [@morales2020universality].

## Landscapes and trainability

- **Barren plateaus.** For a wide class of randomly initialized circuits, the gradient is exponentially small in the
  number of qubits [@mcclean2018barren]. The dynamical Lie algebra of the circuit's generators, the same object that
  decides controllability, controls the variance of the cost [@larocca2022barren]. A general Lie-algebraic theory
  gives this variance exactly for deep circuits and unifies the known sources of barren plateaus: expressiveness,
  entangled inputs, local observables and noise [@ragone2024lie]. Full controllability and trainability therefore
  pull in opposite directions.
- **Overparametrization.** Above a critical number of parameters, bounded by the dimension of that Lie algebra,
  spurious local minima start to disappear and training becomes much easier [@larocca2023overparametrization].
  Problem-inspired ansätze such as the Hamiltonian variational ansatz show mild barren plateaus and become almost trap
  free when overparametrized [@wiersema2020hva]. This is the circuit counterpart of the trap-free
  [[control-landscapes]] of optimal control.

## From circuits to pulses, and back

- **Gradients from measurements.** The parameter-shift rule obtains exact gradients from the same circuit run at
  shifted parameters [@mitarai2018circuit; @schuld2019gradients]. A stochastic version extends it to general
  parametrized evolutions, such as pulse amplitudes [@banchi2021stochastic]. These are hardware-ready gradient
  estimators of the kind [[closed-loop]] control needs.
- **Optimizing pulses directly.** In ctrl-VQE, the pulse shapes of the device, not gate angles, are the variational
  parameters. In simulations of molecules on transmons, this shortened the state-preparation time by roughly three
  orders of magnitude [@meitei2021ctrlvqe]. See [[pulse-level-compilation]].
- **Ansätze from control.** Hardware-efficient ansätze use the device's native interactions [@kandala2017hardware].
  Ansätze inspired by optimal control add symmetry-breaking terms that improve convergence, for example for the
  Fermi–Hubbard model [@choquette2021ocvqa]. Counterdiabatic terms enrich QAOA layers [@chandarana2022dcqaoa] (see
  [[shortcuts-to-adiabaticity]]). Digital–analog schemes combine single-qubit gates with an always-on analog Ising
  interaction [@parrarodriguez2020digitalanalog].
- **No optimizer at all.** Lyapunov control gives FALQON, where each layer's parameters are fixed by measurements on
  the previous layers [@magann2022falqon; @magann2022lyapunovqaoa]. See [[lyapunov-control]].

## What each field brings

Optimal control brings controllability and Lie-algebra tools, landscape theory, [[quantum-speed-limits]] and
[[robust-optimal-control|robustness]], and the lesson that enough control resources (parameters, time) make
optimization easy [@magann2021pulses]. Variational algorithms bring gradient estimation from measurements,
optimizers that cope with shot noise, and a precise theory of when the cost concentrates. Both use the same
mathematics for problems on [[many-body-control|many-body]] Hamiltonians.

## Limitations

- Every cost evaluation is a finite-shot estimate. Gradients below the shot-noise level cannot be resolved, which
  turns barren plateaus into a practical limit.
- Hardware noise flattens landscapes as well and biases the cost.
- Pulse-level ansätze optimized in simulation need an accurate device model. Without one, they must be optimized on
  the hardware, with every evaluation costing measurements.

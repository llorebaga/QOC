---
updated: 2026-10-11
status: draft
key_papers:
  - key: bukov2018phases
    note: Deep reinforcement learning reaches optimal-control performance in many-body state preparation, and reveals a glass-like transition in the space of protocols.
  - key: fosel2018feedback
    note: A neural-network agent discovers complete quantum-error-correction strategies with measurement feedback, from scratch.
  - key: niu2019universal
    note: Deep reinforcement learning for fast, leakage- and noise-robust two-qubit gates, by training with control noise.
  - key: baum2021drl
    note: Reinforcement learning on a real superconducting processor designs an error-robust universal gate set without a Hamiltonian model.
  - key: duncan2025taming
    note: A pedagogical tutorial bringing together shortcuts to adiabaticity, optimal control and machine-learning-based control.
software:
  - name: JAX
    url: https://github.com/jax-ml/jax
    note: differentiable simulation for model-based learning of controllers
---

**Machine learning** offers two things to quantum control. One is new ways to *search*: reinforcement-learning agents,
neural-network controllers, Bayesian surrogates and tree-search methods. The other is new ways to *adapt*: control
policies that react to measurement outcomes in real time, learned from simulation or directly from the experiment.
Since the late 2010s these approaches have matched optimal control on standard tasks. They are especially valuable
where classical optimal control struggles: feedback, model-free learning on hardware, and discrete or rugged control
problems.

## Reinforcement learning in a nutshell

In **reinforcement learning** (RL), an *agent* repeatedly chooses an *action* (the next piece of the control pulse, a
gate, a measurement), observes the result, and receives a *reward* (a fidelity, a measurement outcome). It improves a
*policy* to maximize the expected total reward. Two features make RL attractive here:

- **Model-free learning.** The agent needs only rewards, so it can learn on the device itself, without a Hamiltonian;
- **Policies, not pulses.** The agent learns a rule that maps observations to actions, so it can react to
  measurement outcomes, which is exactly what [[feedback-control|feedback]] requires.

## What has been shown

- **State preparation.** Deep RL finds driving protocols in non-integrable many-body systems with performance
  comparable to optimal-control methods. It also exposed a spin-glass-like transition in the space of protocols as a
  function of duration [@bukov2018phases]; see [[control-landscapes]]. A comparative study found that deep Q-learning and
  policy-gradient methods outperform the other methods tested when the controls are discretized
  [@zhang2019whenrl].
- **Gates.** Agents trained with control noise in the simulation produce fast two-qubit gates that are robust to
  leakage and stochastic errors [@niu2019universal]. Deep Q-networks have been applied to single- and two-qubit gate
  control [@an2019drlgate]. Machine-learning-based optimizers design high-fidelity single-shot three-qubit gates
  [@zahedinejad2016threequbit]. On a real superconducting processor, RL designed an error-robust universal gate set
  without a model of the Hamiltonian, controls or noise [@baum2021drl]. See [[gate-synthesis]].
- **Transport.** Deep RL found control sequences for transporting a state through quantum dots that outperform the
  standard counterintuitive adiabatic sequence, including under detuning, dephasing and losses
  [@porotti2019transport].
- **Feedback and error correction.** A neural-network agent discovered complete quantum-error-correction strategies
  that adapt to measurement outcomes [@fosel2018feedback]. An agent running as a sub-microsecond-latency neural network
  on an FPGA has performed real-time feedback, initializing a superconducting qubit and trained only from measurements
  [@reuer2023realtime]. See [[error-correction]] and [[control-hardware]].
- **Model-free control of oscillators.** Circuit-based RL agents learn to prepare non-classical states of an oscillator
  coupled to an ancilla, using rewards built from experimentally available measurements [@sivak2022modelfree]; see
  [[bosonic-control]].

## Beyond reinforcement learning

- **Bayesian optimization** builds a probabilistic surrogate of the landscape. It suits expensive, noisy experiments —
  for example preparing GHZ states in Rydberg arrays [@mukherjee2020bayesian], optimizing with very few shots
  [@sauvage2020poor], or optimizing ultracold-atom experiments online [@wigley2016fast]. See [[closed-loop]].
- **Deep exploration.** An AlphaZero-style combination of neural networks and tree search explores rugged landscapes
  without good initial guesses [@dalgaard2020alphazero].
- **Differentiable controllers.** When a model is available, a neural-network controller can be trained by
  differentiating through the dynamics — model-based RL [@schafer2020differentiable]. *Feedback-GRAPE* borrows RL ideas
  to optimize measurement-conditioned strategies while still taking gradients through the quantum dynamics
  [@porotti2023grapefeedback]. See [[autodiff-control]].

## When to use what

- **Known model, open-loop task.** Gradient-based optimal control ([[grape|GRAPE]], [[goat|GOAT]]) is usually far more
  sample-efficient than RL.
- **Feedback, adaptivity, discrete actions, or learning on hardware.** RL and related methods come into their own.
- **Expensive, noisy experiments with few parameters.** Bayesian optimization.

Tutorials introduce optimal control and RL side by side [@giannelli2022tutorial; @duncan2025taming], and a broad
review covers machine learning across quantum technologies [@krenn2023ai].

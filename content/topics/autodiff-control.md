---
updated: 2026-10-11
status: draft
key_papers:
  - key: leung2017gpu
    note: Brings automatic differentiation and GPUs to quantum optimal control — arbitrary combinations of cost terms without deriving gradients by hand.
  - key: abdelhafez2019trajectories
    note: Automatic differentiation through quantum trajectories, making gradient-based control of open systems scalable.
  - key: schafer2020differentiable
    note: Differentiable programming for quantum control — a neural-network agent maps the system state to the control and is trained by differentiating through the equations of motion.
  - key: goerz2022semiad
    note: Semi-automatic differentiation. Analytic gradients for the dynamics, automatic differentiation only for the functional, avoiding the memory and run-time overhead of full AD.
software:
  - name: JAX
    url: https://github.com/jax-ml/jax
    note: automatic differentiation and GPU/TPU compilation for Python
  - name: dynamiqs
    url: https://github.com/dynamiqs/dynamiqs
    note: GPU-accelerated, differentiable simulation of quantum systems (JAX)
  - name: qutip-qoc (JOPT)
    url: https://github.com/qutip/qutip-qoc
    note: optimization of JAX-defined controls with automatic differentiation
  - name: QuantumControl.jl
    url: https://github.com/JuliaQuantumControl/QuantumControl.jl
    note: Julia framework; supports semi-automatic differentiation of arbitrary functionals
---

**Automatic differentiation** (AD) computes exact derivatives of a program by applying the chain rule to every
elementary operation it performs. In quantum control, this means the gradient of *any* figure of merit — a
fidelity plus leakage penalties, a robustness average, a measure of entanglement — can be obtained without deriving
it by hand. Since the late 2010s, AD frameworks built for machine learning (TensorFlow, PyTorch, JAX, Julia's
Zygote and Enzyme) have become a standard tool for pulse optimization, often on GPUs [@leung2017gpu].

## The idea

A simulation of controlled dynamics is a long chain of differentiable operations: build the Hamiltonian from the
control parameters, propagate, evaluate the cost. AD differentiates such chains in one of two modes:

- **Forward mode** carries derivatives along with the values. Its cost grows with the number of *inputs*, so it
  suits a few control parameters ([[goat|GOAT]] is forward-mode differentiation of the Schrödinger equation).
- **Reverse mode** (back-propagation) records the computation and then sweeps backwards. It gives the gradient of
  one scalar output with respect to *all* inputs at a cost of a small multiple of one evaluation, independent of the
  number of parameters.

[[grape|GRAPE]]'s backward propagation is exactly reverse-mode differentiation, derived by hand for one specific
cost function. AD generalizes it: change the cost, add constraints or penalties, make the Hamiltonian depend
non-linearly on the controls — and the gradient follows automatically.

## What it enabled

- **Composite cost functions.** Fidelity, leakage to non-computational levels, pulse smoothness, power and
  occupation of forbidden states can be combined freely and weighted, with GPU acceleration [@leung2017gpu].
- **Open systems at scale.** Differentiating through stochastic quantum trajectories instead of the full density
  matrix avoids the $d^2$ growth of Liouville space [@abdelhafez2019trajectories]; see [[open-system-control]].
- **Differentiable programming.** A neural-network agent that maps the current state to the control can be trained
  by differentiating through both the network and the equations of motion. This model-based alternative to
  reinforcement learning has been demonstrated for robust state preparation [@schafer2020differentiable]; see
  [[machine-learning-control]].
- **Integrated device workflows.** Toolsets combine gradient-based pulse optimization with calibration and model
  learning on real hardware [@wittler2021c3; @ball2021software]; see [[model-learning]].

## Caveats

- **Memory.** Reverse mode stores intermediate results. For long time grids or large systems this can exceed memory;
  checkpointing trades extra computation for memory. **Semi-automatic differentiation** uses the analytic GRAPE-type
  gradient for the dynamics and AD only for the final functional. This removes most of the memory and run-time overhead
  of full AD while still allowing practically any functional, including non-analytic ones such as the gate concurrence
  [@goerz2022semiad].
- **Matrix functions.** Gradients through matrix exponentials, eigendecompositions and complex arithmetic must be
  supported correctly by the framework. Degenerate eigenvalues are a classic source of numerical trouble; see
  [[propagation-methods]].
- **Discretize-then-differentiate.** AD returns the exact gradient of the *discretized* simulation. With adaptive ODE
  solvers this can differ from the gradient of the continuous problem, and adjoint-ODE methods offer an alternative.
- **Optimizers.** AD supplies gradients; convergence still depends on the optimizer. Quasi-Newton methods suit
  smooth deterministic costs ([[second-order-methods]]); stochastic optimizers such as Adam suit noisy or sampled
  costs.

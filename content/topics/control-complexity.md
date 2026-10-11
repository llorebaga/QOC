---
updated: 2026-10-11
status: draft
key_papers:
  - key: lloyd2014information
    note: The number of control parameters needed is bounded by the size of the set of states reachable in polynomial time; also gives a bandwidth–time bound and the role of entanglement.
  - key: poulin2011illusion
    note: States reachable by local Hamiltonians in polynomial time fill an exponentially small part of Hilbert space — the "convenient illusion" that makes many-body control tractable.
  - key: caneva2014complexity
    note: A lower bound on the control complexity of many-body dynamics in terms of the dimension of the manifold supporting it, and the role of integrability.
  - key: muller2022noisybounds
    note: Information–time bounds for control in the presence of noise, and how the achievable accuracy scales with it.
---

A quantum system of $n$ qubits has a Hilbert space of dimension $2^n$. Naively, controlling it would need an
exponential number of control parameters and exponentially long pulses. Yet optimal control routinely prepares
many-body states with a few dozen parameters. **Control complexity** explains why, and asks what resources a control
task really needs: how many parameters, how much bandwidth, how much time, and how much classical information.

## The illusion of Hilbert space

Physical dynamics cannot explore all of Hilbert space. States that local, time-dependent Hamiltonians can generate
in a time polynomial in the system size occupy an *exponentially small* volume of it. The overwhelming majority of
states can only be produced after an exponentially long time [@poulin2011illusion]. Control problems of physical
interest therefore live on a much smaller manifold than the full space.

## How many parameters are needed?

The size of the space of control parameters needed to solve a control problem — for pure states, mixed states or
unitaries — is polynomially bounded by the size of the set of states reachable in polynomial time
[@lloyd2014information]. Two consequences:

- **Few parameters can be enough.** If the dynamics has an efficient classical description — for example
  one-dimensional, slightly entangled dynamics — the control problem can be solved efficiently to finite precision
  [@lloyd2014information]. This underlies the success of compact parametrizations such as [[crab|CRAB]] and of
  tensor-network-based [[many-body-control]].
- **The dimension of the dynamics sets the cost.** The control complexity of a many-body evolution is bounded from
  below by the dimension of the manifold that supports it. This makes the role of integrability explicit: conserved
  quantities confine the dynamics to smaller manifolds [@caneva2014complexity]. With partial control of the Hamiltonian, arbitrary many-body evolutions
  can even be reversed, in a way much more robust to noise than standard time-reversal procedures
  [@caneva2014complexity].

Simulations of constrained problems tell the same story from the optimizer's side. The minimum number of controls that
ensures a high yield depends on the number of accessible energy levels [@moore2012constrained]. With too few control
variables the landscape develops traps [@riviello2015severe]; see [[control-landscapes]].

## Bandwidth and time

Time and bandwidth trade off against each other. Lloyd and Montangero give a bound on the minimal time of a control
process for a given control bandwidth, a continuous analogue of the Solovay–Kitaev theorem [@lloyd2014information].
Minimal times scale with the inverse of the bandwidth, a scaling that optimization in a basis of Slepian functions
reaches for entangling two-qubit gates [@lucarelli2018grafs]. See [[quantum-speed-limits]] and
[[pulse-parametrization]].

## Noise and information

Control fields carry information, and noise degrades it. Information–time bounds quantify how well a system can be
controlled under arbitrary noise sources. They agree with standard decoherence formulas and predict how the
achievable accuracy scales with the noise, which has been tested numerically with dCRAB
[@muller2022noisybounds]. See [[robust-optimal-control]] and [[open-system-control]].

## Related notions of complexity

- **Geometric (circuit) complexity.** The number of gates needed for a unitary can be cast as a geodesic length in
  a suitably weighted geometry on the unitary group [@nielsen2006geometry]; see [[geometric-control]].
- **Computational complexity.** Deciding whether a control task is possible at all is undecidable for digitized
  controls on a Turing machine [@bondar2020uncomputability]. In the real-number model of computation, the polynomial
  formulation of [[polynomial-optimization|QCPOP]] makes optimal control computable [@bondar2025qcpop].
- **Algebraic complexity.** The dimension of the [[controllability|dynamical Lie algebra]] determines whether
  gradients of variational circuits vanish exponentially (barren plateaus) [@larocca2022barren]. It is a measure of
  how "large" the controlled dynamics is; see [[variational-algorithms]].

## Practical lessons

- Start with a compact, physically motivated parametrization and add parameters only until fidelity saturates.
- If a problem needs an exponential number of parameters, it is probably asking for a state that the dynamics cannot
  reach in reasonable time.
- Low entanglement in the controlled dynamics is a resource: it makes both simulation and control efficient.

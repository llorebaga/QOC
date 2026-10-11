---
updated: 2026-10-12
status: draft
key_papers:
  - key: gardiner1985inputoutput
    note: Input–output theory — how damped quantum systems couple to propagating fields, via quantum stochastic differential equations and the master equation.
  - key: gough2009series
    note: The series product. An algebra for connecting quantum systems in feedforward and feedback networks, the core of the SLH framework.
  - key: james2008hinf
    note: H-infinity control for linear quantum stochastic systems, including controllers that are themselves quantum (coherent feedback).
  - key: mabuchi2008compensator
    note: An experimental coherent-feedback controller — all-optical disturbance rejection with a tailored dynamic compensator.
  - key: combes2017slh
    note: A review of the SLH framework for modeling quantum input–output networks.
---

Many quantum devices are networks: cavities, waveguides, beam splitters, amplifiers and atoms connected by propagating
fields. **Linear quantum systems theory** describes such networks with the tools of systems engineering — state-space
models, transfer functions, interconnections — while respecting quantum mechanics. Its most distinctive idea is
**coherent feedback**. The output field of a system is processed by another *quantum* system and fed back, with no
measurement in the loop.

## Input–output and quantum stochastic models

A system coupled to a field is modelled by quantum stochastic differential equations: the field acts as quantum noise
driving the system, and the system modifies the outgoing field [@hudson1984ito; @gardiner1985inputoutput]. In the
**SLH framework**, each component is described by a triple $(S, L, H)$: a scattering matrix for the fields, coupling
operators to the fields, and an internal Hamiltonian. Networks are assembled with the *series* and *concatenation*
products [@gough2009series; @combes2017slh].

When the dynamics is linear in the quadratures $x$ — cavities, beam splitters, parametric amplifiers, squeezers —
the model takes the familiar engineering form

$$dx = A\,x\,dt + B\,dw, \qquad dy = C\,x\,dt + D\,dw,$$

with the field noise $dw$ as input and the output field $dy$. Quantum mechanics enters through **physical
realizability** conditions that constrain $(A, B, C, D)$ so that commutation relations are preserved
[@petersen2016linear; @nurdin2017linear].

## Control design

- **H-infinity control.** Robust controllers that bound the effect of disturbances can be designed for linear quantum
  systems, including controllers that are themselves quantum [@james2008hinf].
- **Coherent LQG.** The linear-quadratic-Gaussian problem can be formulated with a quantum controller and fully quantum
  plant outputs [@nurdin2009lqg].
- **Experiments.** An all-optical coherent-feedback controller with a dynamic compensator achieved about 7 dB of
  broadband disturbance rejection on an optical ring resonator [@mabuchi2008compensator]. Coherent feedback enhanced
  optical squeezing, with time delays and losses limiting the benefit [@iida2012squeezing].

## Coherent versus measurement-based feedback

Which is better depends on the task. In some settings all-optical and electro-optical feedback give identical effects
on the controlled cavity [@wiseman1994alloptical]. Coherent feedback, in principle, avoids measurement back-action
[@lloyd2000coherent]. For cooling optical and optomechanical resonators, coherent schemes can outperform the best
measurement-based LQG schemes in the quantum regime, because the coherent controller can process non-commuting output
quadratures simultaneously [@hamerly2012cooling]. A systematic comparison within linear systems theory maps out
where each approach is advantageous [@yamamoto2014coherent]. See [[feedback-control]].

## Why it matters

- **Modular design.** Photonic and microwave circuits can be designed like classical networks, with component models
  that compose correctly; see [[photonics]].
- **Autonomous error correction.** Coherent feedback can replace measurement and classical processing entirely — for
  example in photonic-circuit quantum memories with embedded control [@kerckhoff2010memory]; see [[error-correction]]
  and [[reservoir-engineering]].
- **Bosonic modes.** Linear systems theory is the natural language for Gaussian control of oscillators, while
  non-Gaussian control needs nonlinear elements; see [[bosonic-control]].

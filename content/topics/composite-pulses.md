---
updated: 2026-10-12
status: draft
key_papers:
  - key: levitt1986composite
    note: The classic review of composite pulses in NMR — the principles, families and limits of the technique.
  - key: wimperis1994bb1
    note: Introduces broadband, narrowband and passband composite pulses, including BB1, still the standard correction for amplitude errors.
  - key: cummins2003corpse
    note: Brings composite rotations to quantum computing — BB1, CORPSE and SCROFULOUS families for amplitude and off-resonance errors.
  - key: brown2004arbitrarily
    note: Composite sequences that cancel systematic errors to arbitrary order, without knowing the size of the error.
  - key: merrill2014compensating
    note: A review of compensating pulse sequences for quantum computation.
software:
  - name: Q-CTRL Open Controls
    url: https://github.com/qctrl/open-controls
    note: open-source library of composite-pulse and dynamical-decoupling sequences
---

A **composite pulse** replaces a single rotation by a short sequence of rotations about different axes, chosen so that
**systematic errors cancel**. An amplitude miscalibration or a detuning then barely affects the final operation,
and the sequence works without knowing how large the error is. Composite pulses were developed in NMR in the late
1970s and 1980s [@levitt1979inversion; @levitt1986composite]. Today they are routine in trapped ions, neutral atoms,
spins and superconducting qubits as a simple, analytic form of [[robust-optimal-control|robust control]].

## The idea

Write $\theta_\phi$ for a rotation by angle $\theta$ about an axis at angle $\phi$ in the $xy$-plane. Two systematic
errors dominate:

- **Pulse-length (amplitude) errors** — every rotation angle is scaled, $\theta \to \theta(1+\epsilon)$;
- **Off-resonance errors** — a detuning tilts the rotation axis out of the $xy$-plane.

A composite pulse chooses angles and phases so that the leading error terms of the individual rotations cancel in the
product. The first example — inverting a spin with $90_x\,180_y\,90_x$ instead of $180_x$ — is far less sensitive to
amplitude errors than a single pulse [@levitt1979inversion].

## Classic sequences

**BB1** corrects amplitude errors [@wimperis1994bb1]. A target rotation $\theta_0$ is complemented by

$$\theta_0 \;\cdot\; \pi_{\phi}\; 2\pi_{3\phi}\; \pi_{\phi}, \qquad \phi = \arccos\!\Big(-\frac{\theta}{4\pi}\Big),$$

which leaves an error of order $\epsilon^3$ for any initial state. The correction block can be placed before, after,
or in the middle of the main pulse.

**CORPSE** corrects off-resonance errors and **SCROFULOUS** amplitude errors. Together with BB1, these families were
introduced to quantum computing as fully compensating rotations, which work for any input state
[@cummins2003corpse].

**Arbitrary order.** Systematic constructions cancel errors to any order $\epsilon^n$, independently of the initial
state and without knowing $\epsilon$ [@brown2004arbitrarily]. Short sequences tailored to a single gate — for example
robust NOT gates — trade generality for duration [@jones2013robustnot].

## Point-to-point versus universal

Some composite pulses only need to work for one initial state, such as inversion from $|0\rangle$ to $|1\rangle$.
These *point-to-point* pulses can be shorter and more robust. *Universal* (fully compensating) rotations must work for
every input state, which quantum gates require. Mixing the two up is a common source of disappointing results.

## Beyond hard pulses

- **Smooth composite pulses.** Sequences of shaped instead of rectangular pulses keep robustness while reducing
  bandwidth [@torosov2011smooth]. A single shaped pulse with a time-dependent phase can be viewed as the continuous
  limit of a composite sequence [@daems2013singleshot].
- **Robust dynamical decoupling.** Composite-pulse ideas make decoupling sequences robust to their own pulse errors. In
  universally robust sequences the number of pulses grows only linearly with the order of compensation
  [@genov2017decoupling]; see [[dynamical-decoupling]].
- **Numerical design.** Optimizing a pulse over a range of error parameters ([[robust-optimal-control]]) can be seen as
  an unrestricted search for "composite" solutions. It often finds shorter or more robust pulses than analytic families,
  at the cost of interpretability.

## Strengths and limitations

**Strengths**

- Analytic, simple to implement and calibrate, independent of the size of the error.
- Robust for any initial state (universal sequences), compatible with standard hardware.

**Limitations**

- Longer than a single pulse, so more exposed to decoherence and time-dependent noise; see [[filter-functions]].
- Each family targets specific error types. Simultaneous robustness against several errors needs longer sequences or
  numerical design.

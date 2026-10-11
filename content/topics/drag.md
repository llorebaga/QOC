---
updated: 2026-10-11
status: draft
key_papers:
  - key: motzoi2009drag
    note: Introduces DRAG — a derivative-shaped quadrature component that removes leakage and phase errors in weakly anharmonic qubits.
  - key: gambetta2011analytic
    note: The systematic theory behind DRAG — a family of analytic solutions from an adiabatic expansion, generalizing to several leakage transitions.
  - key: chow2010optimized
    note: Early experimental demonstration on transmons, correcting the phase error from higher levels with a quadrature derivative pulse.
  - key: chen2016leakage
    note: Measures and suppresses leakage with refined DRAG and detuning, reaching errors below 10⁻³ and leakage at the 10⁻⁵ level.
  - key: motzoi2013frequency
    note: Generalizes derivative-based suppression to crosstalk, ladder transitions and sidebands — frequency-selective analytic pulse design.
software:
  - name: qutip-qoc
    url: https://github.com/qutip/qutip-qoc
    note: GOAT/JOPT can optimize DRAG-type analytic pulse families
---

**DRAG** — *Derivative Removal by Adiabatic Gate* — is an analytic pulse-shaping technique for qubits that are only
weakly separated from other levels. Superconducting transmons are the prime example. Adding a component proportional
to the **time derivative** of the pulse envelope, in the out-of-phase (quadrature) channel, removes to leading order
both **leakage** out of the qubit subspace and the associated **phase errors**. Introduced by Motzoi, Gambetta,
Rebentrost and Wilhelm [@motzoi2009drag], it is part of the standard single-qubit gate on most superconducting
processors.

## The problem: weak anharmonicity

A transmon is essentially an anharmonic oscillator [@koch2007transmon]. Its qubit transition $0\leftrightarrow1$ and
its leakage transition $1\leftrightarrow2$ differ only by the anharmonicity $\Delta/2\pi$, typically a few hundred MHz.
A fast pulse has a broad spectrum. If it is short compared with $1/|\Delta|$, part of its spectral weight drives the
$1\leftrightarrow2$ transition, causing **leakage** to $|2\rangle$. The virtual coupling to $|2\rangle$ also shifts
the qubit levels (an AC Stark shift), causing **phase errors**. Without correction, this sets a lower bound on gate
duration [@krantz2019guide]; see [[superconducting]].

## The DRAG solution

Drive the qubit with an in-phase envelope $\Omega_x(t)$ and add a quadrature component proportional to its
derivative,

$$\Omega_y(t) = -\beta\,\frac{\dot\Omega_x(t)}{\Delta},$$

where $\beta$ is of order one at leading order and is calibrated in practice. A time-dependent detuning compensates
the remaining Stark shift. In the frequency domain, the derivative term reshapes the spectrum so that it cancels the
drive at the leakage transition. In the time domain, it is the first correction of an adiabatic expansion in a frame
that removes the coupling to $|2\rangle$ [@motzoi2009drag]. The general theory gives a whole *family* of analytic
solutions, from which one can choose what is practical, and extends to several leakage transitions
[@gambetta2011analytic].

## In experiments

- **Phase-error correction.** A derivative pulse on the quadrature channel removes the phase error caused by higher
  levels, enabling few-nanosecond single-qubit gates [@chow2010optimized]. A simplified "half-derivative" variant,
  calibrated with error-amplifying sequences, reduced phase errors several-fold together with leakage
  [@lucero2010phase].
- **Leakage at the $10^{-5}$ level.** Refining DRAG with a pulse detuning gives gate errors consistently below
  $10^{-3}$ and leakage rates around $10^{-5}$. Much of the remaining leakage then comes from incoherent heating
  [@chen2016leakage].
- **Beyond DRAG.** Closed-loop optimization of every sample of the waveform has produced a 4.16 ns single-qubit
  pulse with 99.76 % fidelity and 0.044 % leakage, faster than DRAG allows [@werninghaus2021leakage]; see
  [[closed-loop]].

## Generalizations

The same derivative-based idea suppresses other unwanted, off-resonant transitions: drive crosstalk onto neighbouring
qubits, additional ladder transitions, and sidebands of the drive [@motzoi2013frequency]. In frequency-crowded
multi-qubit (qutrit) systems, analytic few-parameter pulses with DRAG-like and composite features achieve simultaneous
gates with errors below $10^{-4}$ [@theis2016crowded]. See [[gate-synthesis]].

## DRAG and numerical optimal control

DRAG is a compact, interpretable [[pulse-parametrization|pulse family]]. It is often the starting point for numerical
methods: [[goat|GOAT]] can optimize its few parameters exactly, and [[grape|GRAPE]] can refine it with filtering for
rapidly varying Hamiltonians [@motzoi2011rapid]. Numerically optimized pulses that penalize leakage typically contain
similar quadrature components; see [[problem-formulation]].

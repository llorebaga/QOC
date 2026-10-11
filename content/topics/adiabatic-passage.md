---
updated: 2026-10-11
status: draft
key_papers:
  - key: gaubatz1990stirap
    note: Introduces STIRAP — population transfer through a lossy intermediate level with partially overlapping, counterintuitively ordered pulses.
  - key: bergmann1998coherent
    note: The classic review of coherent population transfer by adiabatic passage in atoms and molecules.
  - key: vitanov2017stirap
    note: A comprehensive review of STIRAP and its extensions across physics, chemistry and quantum technology.
  - key: garwood2001sweep
    note: Adiabatic, frequency-swept pulses in magnetic resonance — broadband and insensitive to field inhomogeneity.
  - key: albash2018aqc
    note: Adiabatic quantum computation — the adiabatic theorem as a model of computation.
---

**Adiabatic passage** transfers population between quantum states by changing the Hamiltonian slowly, so that
the system follows an instantaneous eigenstate from the initial to the target state. Its great strength is
**robustness**. The result does not depend on the precise pulse area, timing or amplitude — only on the change being
slow enough and on the eigenstate connecting the right endpoints. Rapid adiabatic passage in two-level systems and
stimulated Raman adiabatic passage (STIRAP) in three-level systems are workhorses of atomic, molecular and
magnetic-resonance physics, and of quantum technologies.

## The adiabatic theorem

If $H(t)$ changes slowly compared with the energy gap separating an eigenstate from the rest of the spectrum, a system
prepared in that eigenstate remains in it [@born1928adiabatensatz; @kato1950adiabatic]. Adiabatic passage chooses
$H(t)$ so that the relevant eigenstate *is* the initial state at the start and the target state at the end.

## Rapid adiabatic passage (two levels)

Sweep the detuning of a drive through resonance,
$H(t) = \tfrac{\hbar}{2}\big(\Delta(t)\,\sigma_z + \Omega(t)\,\sigma_x\big)$, from large negative to large positive
$\Delta$. The instantaneous eigenstates rotate from $|0\rangle$ to $|1\rangle$, so a slow sweep inverts the
population. The Landau–Zener formula quantifies "slow" [@zener1932crossing]. For a linear sweep $\Delta = \alpha t$
with constant coupling $\Omega$, the probability of a *diabatic* transition (failure) is

$$P_{\rm dia} = \exp\!\Big(-\frac{\pi\,\Omega^2}{2\,|\alpha|}\Big),$$

exponentially small for slow sweeps. In NMR and MRI, frequency-swept adiabatic pulses invert spins uniformly over large
bandwidths, despite inhomogeneous radio-frequency fields [@garwood2001sweep]; see [[spins]].

## STIRAP (three levels)

To transfer population from $|1\rangle$ to $|3\rangle$ via a lossy intermediate state $|2\rangle$, use a *pump* field
$\Omega_P$ on $1\leftrightarrow2$ and a *Stokes* field $\Omega_S$ on $2\leftrightarrow3$. On two-photon resonance the
Hamiltonian has a **dark state**

$$|D\rangle = \cos\theta\,|1\rangle - \sin\theta\,|3\rangle, \qquad \tan\theta = \frac{\Omega_P(t)}{\Omega_S(t)},$$

with no component on $|2\rangle$. Applying the Stokes pulse *before* the pump — the "counterintuitive" order — rotates
$\theta$ from $0$ to $\pi/2$, and the population moves from $|1\rangle$ to $|3\rangle$ without ever occupying the
lossy intermediate level [@gaubatz1990stirap]. The transfer is robust provided the pulses are adiabatic, typically
requiring a pulse area well above $\pi$ (a common rule of thumb is $\Omega_{\rm rms}T \gtrsim 10$).
STIRAP is used for molecules, atoms, ions, solid-state spins and superconducting circuits — for example across the
three lowest levels of a transmon [@kumar2016scstirap] — and has many extensions to multi-level systems
[@bergmann1998coherent; @vitanov2001adiabatic; @vitanov2017stirap].

## Adiabatic quantum computation

In adiabatic quantum computing, the ground state of a simple Hamiltonian is slowly deformed into the ground state of a
problem Hamiltonian that encodes the answer [@albash2018aqc]. The run time is set by the minimum gap. Adapting the
speed locally to the gap, rather than sweeping at a constant rate, recovers the quadratic Grover speed-up for
unstructured search [@roland2002search]. See [[variational-algorithms]].

## Making it faster

The weakness of adiabatic passage is its duration, which competes with decoherence. Ways to speed it up:

- **[[shortcuts-to-adiabaticity|Shortcuts to adiabaticity]]** add counterdiabatic corrections or use invariants to
  reach the adiabatic result in finite time;
- **dressed-state schemes** harness non-adiabatic transitions with corrections that require no extra couplings,
  while minimizing population in the intermediate level of STIRAP [@baksic2016dressed];
- **optimal control** shapes the pulses for a given duration and error budget, often starting from an adiabatic
  protocol. Robustness can be kept by optimizing over parameter ensembles; see [[robust-optimal-control]].

## Strengths and limitations

**Strengths**

- Insensitive to pulse area, amplitude and exact timing; broadband.
- STIRAP avoids populating lossy intermediate states.

**Limitations**

- Slow: needs large pulse areas and long durations.
- Sensitive to two-photon detuning (STIRAP) and to decoherence during the long passage.
- Phases of the final state are less robust than populations, which matters for gates.

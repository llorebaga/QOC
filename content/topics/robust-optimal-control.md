---
updated: 2026-10-11
status: draft
key_papers:
  - key: skinner2003broadband
    note: Optimal control for broadband NMR excitation pulses — the template for optimizing a pulse over a whole range of offsets at once.
  - key: li2006ensemble
    note: Ensemble controllability. When can a single field steer a continuum of systems with different parameters simultaneously?
  - key: kosut2013sequential
    note: Worst-case robust gate design with limited amplitude and bandwidth, and the trade-off between robustness and pulse energy.
  - key: vandamme2017robust
    note: Exact robust optimal pulses for two-level systems from the maximum principle, order by order in the error.
  - key: poggi2024universal
    note: Pulses robust to any systematic error class, through the fidelity susceptibility — equivalent to building a unitary 1-design.
software:
  - name: qutip-qoc
    url: https://github.com/qutip/qutip-qoc
    note: GRAPE/GOAT/CRAB with user-defined (e.g. ensemble-averaged) objectives
  - name: QuOCS
    url: https://github.com/Quantum-OCS/QuOCS
    note: dCRAB and gradient methods, including robust optimization over parameter sets
---

A pulse that is optimal for one precisely known Hamiltonian can fail badly when the real system differs slightly:
a detuning, a miscalibrated amplitude, a spread of couplings across an ensemble. **Robust optimal control** designs
pulses that work well over a whole *range* of parameters at once. It is essential in practice. Magnetic-resonance
pulses must cover an entire spectrum of chemical shifts and inhomogeneous fields, and quantum gates must tolerate drifts
and calibration errors.

## Formulating robustness

Let the Hamiltonian depend on uncertain parameters $\boldsymbol\delta$ — a detuning $\Delta$, an amplitude error
$\epsilon$ —

$$H(t; \boldsymbol\delta) = H_0(\boldsymbol\delta) + \sum_k \big(1 + \epsilon\big)\,u_k(t)\,H_k ,$$

so that each value of $\boldsymbol\delta$ gives a fidelity $F(\boldsymbol\delta)$. Three formulations are common.

**Ensemble average.** Maximize the average over a distribution of parameters, approximated by sampling:

$$\bar F = \int p(\boldsymbol\delta)\,F(\boldsymbol\delta)\,d\boldsymbol\delta \;\approx\; \sum_{j} w_j\,F(\boldsymbol\delta_j).$$

The gradient of $\bar F$ is the weighted average of the gradients for each sample, so [[grape|GRAPE]],
[[krotov|Krotov]] or [[goat|GOAT]] apply directly. This is how broadband NMR pulses were designed
[@skinner2003broadband] and how their physical limits were explored [@kobzar2004broadband]. Sampling-based learning
control trains on a set of sampled ensemble members and then tests the result on new ones [@chen2014sampling].

**Worst case.** Maximize $\min_{\boldsymbol\delta} F(\boldsymbol\delta)$ over the uncertainty set. This gives guarantees
rather than averages, and makes trade-offs explicit — for example between worst-case gate fidelity and pulse energy
under amplitude and bandwidth limits [@kosut2013sequential].

**Sensitivity (order by order).** Expand around the nominal point and cancel the leading derivatives,

$$F(\delta) = F(0) + \delta\,\partial_\delta F + \tfrac12 \delta^2\,\partial_\delta^2 F + \dots ,
\qquad \partial_\delta F = \dots = \partial_\delta^N F = 0 ,$$

making the pulse robust to $N$th order. For two-level systems, the maximum principle gives exact time- and
energy-optimal robust pulses order by order. The control landscape of a pulse robust to $N$th order has dimension at
most $2N$, an estimate of its complexity [@vandamme2017robust]. Expressing the leading error through the *fidelity
susceptibility* in superoperator form gives pulses robust to *any* class of systematic errors. This turns out to be
equivalent to making the sequence of unitaries mimic the first moments of the Haar distribution, i.e. a unitary 1-design
[@poggi2024universal].

## Ensemble controllability

A more fundamental question is whether *one* field can steer a whole continuum of systems with different parameters
to the same target, for example spins with a spread of Larmor frequencies or Rabi amplitudes. The theory of ensemble
controllability answers it for Bloch equations [@li2006ensemble; @li2009bloch]. It explains why broadband and
amplitude-robust pulses exist, and how much time they need.

## Analytic and geometric routes to robustness

Robustness can also be built in by construction:

- **[[composite-pulses|Composite pulses]]** cancel systematic errors with sequences of simple rotations. Smooth,
  single-shot shaped pulses generalize them to a continuous time-dependent phase [@daems2013singleshot].
- **Robust [[shortcuts-to-adiabaticity|shortcuts to adiabaticity]].** Invariant-based engineering can be chosen to be
  optimally robust, with different optimal protocols for amplitude noise and for systematic errors
  [@ruschhaupt2012robust].
- **Inverse geometric optimization** derives robust optimal fields by optimizing trajectories in the space of dynamical
  variables and inverting the dynamics [@dridi2020inverse].
- **Space curves.** Error-correcting evolutions correspond to closed geometric curves, which gives access to the global
  space of dynamically corrected gates [@barnes2022spacecurves].

## Static versus time-dependent errors

The methods above target *quasi-static* uncertainty: parameters that are unknown but constant during a pulse. For noise
that fluctuates *during* the pulse, the relevant tool is the frequency-domain description of
[[filter-functions|filter functions]], with [[dynamical-decoupling|dynamical decoupling]] as its simplest instance.
Both kinds of robustness can be optimized together.

## Practical notes

- **Robustness costs time and energy.** Robust pulses are longer or stronger than nominal ones. The trade-off should be
  explored explicitly [@kosut2013sequential].
- **Sample wisely.** A few well-placed samples (e.g. Gauss–Hermite points of the expected distribution) often suffice
  for averages. Worst-case formulations need samples at the edges of the uncertainty set.
- **Use the right model.** Robust optimization is only as good as the error model; see [[model-learning]] for learning
  it from the device.

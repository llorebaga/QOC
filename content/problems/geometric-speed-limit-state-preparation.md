---
title: The Bukov–Sels–Polkovnikov geometric speed limit for accessible state preparation
question: >-
  For a quantum system steered with unit fidelity between ground states of a restricted family of accessible
  Hamiltonians $H(\lambda)$, is the time-integrated energy standard deviation always bounded below by the geodesic
  distance inside the ground-state manifold?
status: solved
topics: [quantum-speed-limits, many-body-control, shortcuts-to-adiabaticity, state-preparation]
posed_by:
  - key: bukov2019geometric
    where: Section II, Eqs. (2) and (6). Formulates the geometric bound conjecture relating the Fubini–Study length of
      any unit-fidelity dynamical state path to the geodesic length in the accessible eigenstate manifold, with
      analytical and numerical evidence in few-level and many-body models.
  - key: koch2022roadmap
    where: Section 2.2.6, "Quantum speed limit". Highlights the diverging geodesic length under local controls as a key
      challenge for many-body speed limits.
added: 2026-11-23
updated: 2026-11-23
review: draft
---

## Statement

Consider a family of accessible Hamiltonians $\{H(\lambda)\}_{\lambda \in \Lambda}$ ($\Lambda \subset \mathbb{R}^p$)
with non-degenerate ground states $|\psi_0(\lambda)\rangle$, forming the **ground-state manifold**
$\mathcal{M}_0 = \{|\psi_0(\lambda)\rangle : \lambda \in \Lambda\}$ equipped with the induced Fubini–Study metric

$$g_{\mu\nu}(\lambda) = \mathrm{Re}\Big[\langle \partial_\mu \psi_0 | \partial_\nu \psi_0 \rangle - \langle \partial_\mu \psi_0 | \psi_0 \rangle \langle \psi_0 | \partial_\nu \psi_0 \rangle\Big].$$

Suppose a time-dependent protocol $\lambda(t) \in \Lambda$ steers the Schrödinger evolution
$i\,\partial_t|\psi(t)\rangle = H(\lambda(t))|\psi(t)\rangle$ from $|\psi(0)\rangle = |\psi_0(\lambda_i)\rangle$ to
$|\psi(T)\rangle = |\psi_0(\lambda_*)\rangle$ with unit fidelity (a "fast-forward" protocol). By the Anandan–Aharonov
relation, the Fubini–Study length of the dynamical state trajectory equals the time-integrated energy standard
deviation [@anandan1990geometry]:

$$l_E\big[|\psi(t)\rangle\big] = \int_0^T \sqrt{\delta E^2(t)}\,dt, \qquad
\delta E^2(t) = \langle\psi(t)|H(\lambda(t))^2|\psi(t)\rangle - \langle\psi(t)|H(\lambda(t))|\psi(t)\rangle^2.$$

**Conjecture** (Bukov, Sels, Polkovnikov). For every unit-fidelity state-preparation protocol $H(\lambda(t))$ within
the accessible control space $\Lambda$,

$$l_E\big[|\psi(t)\rangle\big] \;\ge\; d_{\mathcal{M}_0}\big(|\psi_i\rangle, |\psi_*\rangle\big)
\;=\; \min_{\lambda(\cdot)\subset\Lambda} \int \sqrt{g_{\mu\nu}\,d\lambda^\mu d\lambda^\nu},$$

which by Cauchy–Schwarz implies the geometric [[quantum-speed-limits|quantum speed limit]]
$T_{\mathrm{QSL}} \ge d_{\mathcal{M}_0} / \sqrt{\overline{\delta E^2}}$ [@bukov2019geometric].

## Why it matters

Standard [[quantum-speed-limits|quantum speed limits]] such as Mandelstam–Tamm assume unconstrained access to all
Hamiltonians on Hilbert space. In [[many-body-control|many-body systems]] of size $L$, the energy variance grows as
$\sqrt{L}$ while the Fubini–Study angle between states is at most $\pi/2$, making the unconstrained bound vanish in the
thermodynamic limit even when local control is exponentially hard [@bukov2019geometric]. The conjecture promised a
universal, control-restricted speed limit governed solely by the adiabatic quantum geometry of $\mathcal{M}_0$: if
true, any non-equilibrium optimal protocol would remain fundamentally bounded by the adiabatic geodesic length,
implying exponentially long [[state-preparation|state-preparation]] times in glassy or chaotic many-body systems
[@bukov2019geometric; @koch2022roadmap].

## Known results

**Adiabatic and counterdiabatic saturation.** Along any sufficiently slow (adiabatic) path, adiabatic perturbation
theory shows $l_E = l_g + O(\dot\lambda^2)$, so the inequality holds perturbatively and is saturated in the adiabatic
limit [@bukov2019geometric]. For [[shortcuts-to-adiabaticity|counterdiabatic driving]]
$H_{\mathrm{CD}}(t) = H(\lambda(t)) + \dot\lambda\,\mathcal{A}_\lambda$, the state never leaves $\mathcal{M}_0$ and the
equality $l_E = l_g$ holds exactly at arbitrary speed [@funo2017universal; @bukov2019geometric]. Bukov, Sels and
Polkovnikov also verified the inequality analytically in two- and three-level models and numerically in non-integrable
spin chains and an SYK model [@bukov2019geometric].

**Sufficient geometric condition.** Goll and Jonsson observed that the dynamical trajectory $|\psi(t)\rangle$ generally
leaves $\mathcal{M}_0$ while remaining inside the larger orbit $\mathcal{O}_{|\psi_i\rangle}$ of all states dynamically
reachable under $H(\Lambda)$. Consequently, the conjecture is guaranteed to hold whenever $\mathcal{M}_0$ contains a
shortest geodesic of $\mathcal{O}_{|\psi_i\rangle}$ connecting $|\psi_i\rangle$ and $|\psi_*\rangle$ — in particular
when $\mathcal{M}_0$ is a flat (zero extrinsic curvature) submanifold of $\mathcal{O}_{|\psi_i\rangle}$, which covers
all linearly controlled qubits [@goll2026curved].

**Refutation via extrinsic curvature.** Goll and Jonsson disproved the conjecture in general by showing that whenever
$\mathcal{M}_0$ has non-zero *extrinsic curvature* inside $\mathcal{O}_{|\psi_i\rangle}$, dynamical trajectories can
cut through $\mathcal{O}_{|\psi_i\rangle}$ along paths shorter than $d_{\mathcal{M}_0}$ [@goll2026curved]. They
constructed explicit unit-fidelity counterexamples with $l_E < d_{\mathcal{M}_0}$ in four systems:

- a qubit whose accessible Hamiltonians trace a non-equatorial circle on the Bloch sphere ($\theta \neq \pi/2$);
- a harmonic oscillator with linearly shifted quadratures along a semicircular control path ($l_E = 2 < d_{\mathcal{M}_0} = \pi$);
- a squeezed harmonic oscillator at fixed squeezing parameter $r$; and
- a **linearly controlled qutrit** $H(\lambda) = H_0 + \lambda K$ (matching the linear control form tested in
  [@bukov2019geometric]), where constant evolution under $H_0$ for $T = \pi/\omega$ maps $|\psi_0(-\lambda_*)\rangle$
  to $|\psi_0(\lambda_*)\rangle$ with $l_E < d_{\mathcal{M}_0}$ for $a > 1$ and sufficiently large $|\lambda_*|$
  [@goll2026curved].

## Status

**Solved (refuted).** The Bukov–Sels–Polkovnikov conjecture does not hold in general — not even for linearly
controlled finite-dimensional Hamiltonians $H(\lambda) = H_0 + \lambda K$ — because extrinsic curvature of the
ground-state manifold inside the dynamically reachable orbit allows shorter unit-fidelity paths [@goll2026curved].
Follow-up questions remain open, including whether non-zero extrinsic curvature always guarantees a counterexample and
how to bound the gap between geodesics in $\mathcal{M}_0$ and $\mathcal{O}_{|\psi_i\rangle}$ to obtain valid
control-restricted speed limits [@goll2026curved].

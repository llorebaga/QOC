---
updated: 2026-10-12
status: draft
key_papers:
  - key: kosloff2013thermodynamics
    note: Quantum thermodynamics from the dynamics of open quantum systems — the foundation of finite-time quantum thermodynamics.
  - key: rezek2006irreversible
    note: The quantum Otto engine with oscillators — "quantum friction" from non-commuting Hamiltonians, and optimal power.
  - key: delcampo2014superadiabatic
    note: Shortcuts to adiabaticity give engine cycles with finite power and no friction.
  - key: scandi2019length
    note: Thermodynamic length for Lindblad dynamics; minimal-dissipation protocols are geodesics.
  - key: binder2015quantacell
    note: Optimal charging of quantum batteries in finite time, and the power advantage of global operations.
  - key: rossnagel2016singleatom
    note: A heat engine whose working medium is a single trapped ion.
---

**Quantum thermodynamics** studies heat, work and entropy at the scale of single quantum systems. Its devices — heat
engines, refrigerators, batteries — are driven by time-dependent controls: a trap frequency that is compressed and
expanded, couplings to hot and cold baths switched on and off, a field that charges a battery. Choosing these
controls is an optimal control problem with thermodynamic objectives: extracted work, power, efficiency, entropy
production, or the size of fluctuations [@kosloff2013thermodynamics; @vinjanampathy2016thermodynamics].

## Engines as control problems

- **Origins.** A three-level maser can be viewed as a heat engine, with an efficiency bounded by Carnot's
  [@scovil1959maser]. Open quantum systems driven by external fields and coupled to baths give a general model of
  heat engines [@alicki1979engine].
- **The Otto cycle.** In the quantum Otto cycle, a working medium (often a harmonic oscillator) is compressed and
  expanded by changing its Hamiltonian, and thermalized with two baths in between. When the Hamiltonian does not
  commute with itself at different times, fast strokes create excitations that cost work. This irreversible loss of
  power, called "quantum friction", is of quantum origin [@rezek2006irreversible]. At high temperature and in the
  quasistatic regime, the efficiency at maximum power coincides with the Curzon–Ahlborn value of endoreversible
  engines [@rezek2006irreversible; @curzon1975efficiency]. The harmonic Otto cycle has been reviewed in
  [@kosloff2017otto].
- **Experiments.** A single ion in a tapered Paul trap, coupled to engineered laser reservoirs, was proposed as a
  heat engine [@abah2012singleion] and then realized [@rossnagel2016singleatom]. With NV centres in diamond, two
  predicted effects of coherence in the working medium were observed: more power than an equivalent classical engine
  at small engine action, and the thermodynamic equivalence of different engine types [@klatzow2019engines].

## Shortcuts against friction

[[shortcuts-to-adiabaticity|Shortcuts to adiabaticity]] make the compression and expansion strokes fast without
final excitations. This gives engine cycles that produce finite power with no friction
[@delcampo2014superadiabatic]. It also raises power and efficiency and suppresses work fluctuations
[@deng2013boosting]. The shortcut fields are not free: the energetic cost of counterdiabatic driving grows as the
duration shrinks [@campbell2017tradeoff]. Whether that cost is counted decides whether a shortcut pays off.

## Optimal finite-time cycles

- **Thermodynamic length.** For slow driving, the dissipated availability is governed by a metric on the space of
  equilibrium states, the thermodynamic length [@salamon1983length]. For Lindblad dynamics, minimal-dissipation
  protocols are geodesics of a corresponding metric [@scandi2019length]. Perturbation theory for slowly driven master
  equations gives the efficiency at maximum power of finite-time Carnot engines [@cavina2017slow]. See
  [[geometric-control]].
- **Optimal cycles.** For low-dissipation Carnot engines, the optimal strategy is to run small cycles around a
  working point. The best point does not depend on how power and efficiency are weighted. Many-body working media
  can reach Carnot efficiency at finite power per constituent in the thermodynamic limit
  [@abiuso2020lowdissipation].
- **Several objectives.** Power, efficiency and stability cannot all be maximized at once. Reinforcement learning has
  found the Pareto-optimal cycles of a quantum-dot engine, revealing abrupt changes in the optimal cycle shape
  [@erdman2023pareto]. See [[machine-learning-control]].

## Batteries

A quantum battery stores energy that can later be extracted as work. Entangling operations can extract more work
from many copies than independent ones [@alicki2013batteries]. For charging in finite time, optimal protocols exist
analytically for a qubit. Global operations on $N$ qubits give an $N$-fold advantage in power per qubit, which
numerical optimal control confirms [@binder2015quantacell]. This collective advantage is bounded when only $k$
batteries interact at a time [@campaioli2017charging].

## Feedback and fundamental limits

- **Feedback.** With measurement and feedback, a Maxwell's demon, the extractable work can exceed the free-energy
  difference by an amount set by the mutual information between system and controller. The second law is restored
  once the cost of information processing is included [@sagawa2008feedback]. See [[feedback-control]].
- **Cooling.** The third law limits how fast a system can be cooled. The attainable temperature scales as an inverse
  power of the cooling time [@masanes2017thirdlaw]. Cooling and reset are also [[state-preparation]] and
  [[open-system-control]] problems.

## Limitations

- Definitions of work and heat are not unique when the system is strongly coupled to its baths or carries
  coherences, so results depend on the chosen definition.
- Weak-coupling Markovian master equations, the usual models, can break down for fast strokes and fast switching of
  bath couplings.
- The energy and entropy cost of the controller itself is often left out, although it can dominate at small scales.

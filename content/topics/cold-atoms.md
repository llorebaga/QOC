---
updated: 2026-10-12
status: draft
key_papers:
  - key: bloch2008manybody
    note: Review of many-body physics with ultracold gases, from optical lattices to strongly interacting Fermi gases.
  - key: hohenester2007bec
    note: Optimal control of Bose–Einstein condensates in microtraps with the Gross–Pitaevskii equation.
  - key: schaff2010fast
    note: Invariant-based shortcut to adiabaticity demonstrated by decompressing a cold-atom cloud 37 times faster.
  - key: rosi2013fast
    note: Closed-loop optimal control of the superfluid–Mott-insulator crossing in an optical lattice.
  - key: vanfrank2016complex
    note: Optimal control computed and verified for condensate motional states and phase-transition crossings.
  - key: weidner2018shaken
    note: Shaken-lattice interferometry, with beam splitters found by closed-loop dCRAB optimization.
---

**Ultracold atoms** are neutral atoms cooled to nanokelvin temperatures, as Bose–Einstein condensates or degenerate
Fermi gases, and held in magnetic traps, atom chips or optical lattices [@bloch2008manybody]. The controls are the
trapping potentials themselves: their depth, position, shape and time dependence, plus laser and radio-frequency
couplings between internal states. Control tasks include moving and splitting clouds, preparing motional and
many-body states, and building the beam splitters and mirrors of atom interferometers.

## Transport, compression and splitting

- **Moving atoms.** Transport with optical tweezers on the timescale of a trap period leaves no centre-of-mass
  excitation for a discrete set of durations, set by the Fourier transform of the velocity profile
  [@couvert2008transport].
- **Shortcuts to adiabaticity.** Engineered trap trajectories based on invariants of motion decompressed a cold cloud
  by a factor of 15 in 35 ms, 37 times faster than a linear ramp [@schaff2010fast]. They also worked for an
  interacting, finite-temperature condensate [@schaff2011bec]. See [[shortcuts-to-adiabaticity]].
- **Splitting condensates.** Optimal control of the splitting of a condensate in a double well increases number
  squeezing, which helps interferometry [@grond2009squeezing]. On an atom chip, optimally controlled excitation of a
  condensate's vibrational state produced correlated twin-atom beams [@bucker2011twin].

## Mean-field and many-body control

For condensates, the Gross–Pitaevskii equation is a tractable model for gradient-based optimization. It has been
used to design control of condensates in microtraps that remains good when the computed controls are distorted by
filters [@hohenester2007bec], and to compare GRAPE and Krotov [@jager2014bec]. In optical lattices, the
superfluid–Mott-insulator transition [@greiner2002mott] is the standard control target. Optimal crossings were first
designed with tensor networks [@doria2011crab]. Experimentally, closed-loop optimization sped up loading and crossing
more than threefold [@rosi2013fast]. Optimal transformations proved robust to temperature and atom-number
fluctuations [@vanfrank2016complex]. See [[many-body-control]] and [[crab]].

## Motional states and interferometry

Shaking an optical lattice in position turns the lattice into a control knob for momentum states. Optimal control
transferred a condensate into single or multiple momentum states with controlled relative phases
[@dupont2021lattice]. Closed-loop dCRAB optimization of the shaking built a beam splitter and complete
interferometers [@weidner2018shaken]. In light-pulse atom interferometry [@cronin2009interferometry], GRAPE-designed
mirror pulses are robust to the spread of velocities, intensities and Zeeman states in the cloud
[@saywell2018mirror]. See [[quantum-sensing]] and [[robust-optimal-control]].

## Learning and citizen science

Cold-atom experiments are slow to simulate but quick to repeat, which makes them natural targets for optimization on
the experiment. Machine learning has optimized the production of condensates [@wigley2016fast], and experts and
citizen scientists have optimized it remotely [@heck2018remote]. See [[closed-loop]] and
[[machine-learning-control]].

## Limitations

- Interactions, finite temperature and imperfect potentials make accurate models hard. Mean-field descriptions fail
  for strongly correlated states.
- Each experimental run takes seconds, and the measurements are usually destructive, which limits how many cost
  evaluations closed-loop optimization can afford.
- Calibration of potentials (atom-chip currents, lattice depths) drifts between runs.

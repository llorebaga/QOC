---
updated: 2026-10-12
status: draft
key_papers:
  - key: cirac1995ions
    note: The first proposal for quantum computing with trapped ions, using their shared motion as a bus.
  - key: leibfried2003ions
    note: Review of the quantum dynamics and laser control of single trapped ions.
  - key: molmer1999entanglement
    note: The Mølmer–Sørensen gate, insensitive to the ions' thermal motion — the standard entangling gate.
  - key: choi2014multimode
    note: Optimally shaped pulses that control many motional modes for entangling gates in a five-ion chain.
  - key: schafer2018fast
    note: Entangling gates faster than the trap period, driven by amplitude-shaped laser pulses.
  - key: walther2012transport
    note: Optimized fast transport of a ground-state-cooled ion over many wavefunction widths in a few trap periods.
---

**Trapped ions** are charged atoms held in electromagnetic traps and controlled with lasers or microwaves
[@leibfried2003ions; @bruzewicz2019ions]. Qubits are stored in long-lived hyperfine or optical levels, and ions in
the same trap interact through their shared vibrational modes. This was the basis of the first proposal for a quantum
computer [@cirac1995ions]. Ions combine excellent coherence and very high gate fidelities with comparatively slow
gates, which makes control of the motion the central problem.

## Single-qubit control

Laser- and microwave-driven single-qubit gates reach errors of a few $10^{-5}$ [@gaebler2016universal;
@ballance2016hyperfine]. Microwave near fields can also couple to the motion, which allows laser-free entangling
gates [@ospelkaus2011microwave]. Composite and robust pulses suppress amplitude and frequency errors; see
[[composite-pulses]] and [[robust-optimal-control]].

## Entangling gates through the motion

- **Spin-dependent forces.** The Mølmer–Sørensen gate uses a bichromatic field that entangles the ions' internal
  states through virtual excitation of the motion. The motion need not be fully controlled, so it works even with
  ions in thermal motion [@molmer1999entanglement; @sorensen2000thermal]. Laser-driven gates based on
  spin-dependent forces have reached 99.9% fidelity [@ballance2016hyperfine].
- **Many modes.** At the end of the gate, the ions must be disentangled from every motional mode, and longer chains
  have more modes to close. Optimally shaped, segmented pulses address this in a five-ion chain
  [@choi2014multimode]. Frequency modulation of the driving force suppresses residual spin–motion entanglement and is
  robust to frequency drifts [@leung2018robust]. Discrete phase shifts can decouple several modes and suppress drive
  fluctuations [@green2015phasemodulated]. Multitone drives give gates robust to several error sources
  [@shapira2018robust]. See [[gate-synthesis]].
- **Beyond the trap period.** Standard gates are slow compared with the motional frequencies. Amplitude-shaped laser
  pulses that drive the motion along designed trajectories gave entangling gates far faster than this limit
  [@schafer2018fast].

## Shuttling

A scalable architecture moves ions between zones for storage, gates and readout [@kielpinski2002architecture]. The
"quantum CCD" architecture has been realized in practice [@pino2021qccd]. Transport must be fast and must leave the
ion's motion unexcited. Ions have been moved over hundreds of micrometres in 5 to 16 trap periods, gaining only about
0.1 motional quanta [@walther2012transport; @bowler2012transport], and ion chains have been split
[@bowler2012transport]. Shuttling is a control problem in its own right. Numerical optimization, invariant-based
inverse engineering and geometric optimal control each work best in different regimes of length and time
[@furst2014transport]. See [[shortcuts-to-adiabaticity]].

## Ions as a testbed

Ion motion is a clean harmonic oscillator, used to encode error-correctable grid states [@fluhmann2019gkp] (see
[[bosonic-control]]). Engineered laser dissipation implements open-system dynamics [@barreiro2011opensim;
@lin2013dissipative] (see [[reservoir-engineering]]), and a single ion has served as a heat engine
[@rossnagel2016singleatom] (see [[quantum-thermodynamics]]). GHZ states of 14 ions revealed how correlated noise
limits large entangled states [@monz2011fourteen]. Ions also host qudits with up to seven levels
[@ringbauer2022qudit].

## Limitations

- Gates are slow compared with solid-state platforms, and speeding them up excites the motion.
- Long chains have dense motional spectra, which makes gates harder to design and more sensitive to drifts.
- Laser intensity and phase noise, beam pointing and heating of the motion limit fidelities.

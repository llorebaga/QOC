---
updated: 2026-10-12
status: draft
key_papers:
  - key: cirac1997network
    note: Shaped laser pulses map an atom's state onto a photon that a distant atom absorbs with unit probability.
  - key: reck1994unitary
    note: Any discrete unitary on optical modes can be built from beam splitters and phase shifters.
  - key: novikova2007storage
    note: Optimal input pulse shapes for light storage, found by time reversal and demonstrated in warm vapour.
  - key: aspelmeyer2014optomechanics
    note: Review of cavity optomechanics — radiation-pressure coupling, cooling and quantum control of motion.
  - key: magrini2021mechanical
    note: Measurement-based optimal feedback cools a levitated nanoparticle to its motional ground state at room temperature.
  - key: kok2007linear
    note: Review of linear-optical quantum computing with photonic qubits.
---

**Photonic and optomechanical systems** cover the control of light and of the mechanical motion it couples to:
single-photon sources, optical circuits, cavities, quantum memories and mechanical resonators. Photons rarely
interact, which makes them excellent carriers of quantum information but hard to process. Much of the control
therefore acts on the matter that emits, stores or scatters light, or on the classical settings of optical circuits.

## Shaping photons

- **Emission and absorption.** Shaping the drive of an atom in a cavity sets the temporal shape of the emitted
  photon. A time-symmetric photon can be absorbed by a second atom with unit probability [@cirac1997network]. An
  atom–cavity system driven by an adiabatic Raman transition emits single photons on demand [@kuhn2002photon]. The
  microwave counterpart transferred states between superconducting qubits on different chips
  [@kurpiers2018transfer]. See [[state-preparation]].
- **Storage.** Electromagnetically induced transparency maps a light pulse onto a collective atomic excitation, the
  dark-state polariton, by turning a control field down [@fleischhauer2000polaritons]. The retrieval efficiency of
  storage in an atomic ensemble is set by its optical depth or cooperativity, whatever the technique, and optimal
  storage strategies follow from this [@gorshkov2007storage]. Time reversal gives optimal input pulse shapes, as
  demonstrated in warm rubidium vapour [@novikova2007storage].
- **Quantum dots.** Semiconductor quantum dots in photonic nanostructures are bright single-photon sources whose
  emission can be engineered [@lodahl2015dots].

## Optical circuits

Any unitary on $N$ optical modes can be decomposed into beam splitters and phase shifters [@reck1994unitary]. A
different mesh design needs half the physical footprint and is more tolerant of losses
[@clements2016interferometers].
Reconfigurable integrated circuits implement universal linear optics on chip [@carolan2015universal]. With single
photons, detectors and feed-forward, linear optics is enough for scalable quantum computation [@knill2001klm;
@kok2007linear]. Setting the phases of such circuits is a static control and calibration problem. Continuous-variable
optics with squeezing and nonlinearities is covered in [[bosonic-control]] and [[linear-quantum-systems]].

## Optomechanics

Radiation pressure couples light to the motion of mechanical resonators [@aspelmeyer2014optomechanics].
Sideband cooling brought micromechanical and nanomechanical oscillators to their quantum ground state
[@teufel2011groundstate; @chan2011groundstate]. Optically levitated nanoparticles have been cooled to the ground
state with a cavity [@delic2020levitated], and with measurement-based feedback, both at room temperature
[@magrini2021mechanical] and in cryogenic free space [@tebbenjohanns2021levitated]. Measurement-based control has
also cooled membrane resonators [@rossi2018mechanical]. See [[feedback-control]] and [[open-system-control]].

## Limitations

- Photon loss is the dominant error, and loss in sources, circuits and detectors compounds.
- Probabilistic sources and gates need multiplexing or feed-forward, which require fast, low-latency control.
- Mechanical resonators couple strongly to their thermal environment, so control must outpace thermal decoherence.

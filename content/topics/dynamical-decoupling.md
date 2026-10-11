---
updated: 2026-10-11
status: draft
key_papers:
  - key: hahn1950echo
    note: The spin echo. A single refocusing pulse undoes the dephasing caused by static inhomogeneities — the seed of all decoupling.
  - key: viola1999decoupling
    note: Dynamical decoupling of open quantum systems — averaging away unknown system–environment couplings while keeping control over the system.
  - key: uhrig2007keeping
    note: UDD. Optimized, non-equidistant π-pulse timings that suppress dephasing to high order.
  - key: biercuk2009memory
    note: Experimental demonstration with trapped ions of large error suppression by optimized decoupling sequences, in a model quantum memory.
  - key: ezzell2023survey
    note: A survey of 60 decoupling sequences on superconducting devices, and what works in practice.
software:
  - name: Q-CTRL Open Controls
    url: https://github.com/qctrl/open-controls
    note: library of standard decoupling sequences (CPMG, XY, UDD, CDD, …)
---

**Dynamical decoupling** (DD) protects a quantum system from its environment by applying a sequence of fast
pulses that repeatedly flip it, so that the unwanted system–environment interaction averages to zero. It needs no
extra qubits, no measurements and no detailed model of the noise. This makes it the simplest and cheapest
error-suppression method available, and a building block of quantum memories, gates and sensors.

## From spin echoes to decoupling

**The spin echo.** Spins precessing at slightly different frequencies dephase. A single $\pi$ pulse at time $\tau$
reverses their relative phases, and at $2\tau$ they refocus [@hahn1950echo]. Static inhomogeneity is undone exactly.

**CPMG.** Repeating the echo — $\pi$ pulses at times $\tau, 3\tau, 5\tau, \dots$ — also suppresses slowly *fluctuating*
noise [@carr1954diffusion]. With the refocusing pulses phase-shifted by $90^\circ$ relative to the initial excitation,
the sequence becomes robust to pulse imperfections for the relevant initial state [@meiboom1958modified].

**Decoupling open quantum systems.** Viola and Lloyd showed that repeated flipping ("quantum bang-bang control")
suppresses decoherence caused by a quantum environment, provided the pulse interval is short compared with the
environment's correlation time [@viola1998suppression]. More generally, cycling through a group of operations
$\{g_j\}$ replaces the system–bath Hamiltonian by its group average,

$$H_{SB} \;\longrightarrow\; \bar H_{SB} = \frac{1}{|G|}\sum_{j} g_j^\dagger\, H_{SB}\, g_j ,$$

which vanishes for a suitably chosen group — to lowest order in the average-Hamiltonian (Magnus) expansion. This
filters out *unknown* couplings while preserving control over the system [@viola1999decoupling]; see
[[floquet-engineering]].

## Sequence families

| Sequence | Idea | Notes |
|---|---|---|
| Spin echo / CPMG | equally spaced π pulses about one axis | Simple; CPMG is robust for states along the pulse axis |
| XY-4, XY-8, XY-16 | alternate pulses about $x$ and $y$ | Compensates pulse errors for arbitrary states [@gullion1990xy] |
| UDD | π pulses at $t_j = T\sin^2\!\big(\tfrac{\pi j}{2(n+1)}\big)$ | Optimized timings, high-order suppression of dephasing [@uhrig2007keeping] |
| CDD | recursively concatenated sequences | Error suppression improves with concatenation level [@khodjasteh2005cdd] |
| Universally robust (UR) | phases chosen as in composite pulses | Robust to pulse errors to arbitrary order, any pulse shape [@genov2017decoupling] |

Real pulses have errors, and in long sequences these accumulate. They can even exceed the effect of the environment,
which is why robust sequences matter in practice [@souza2012robust]. A broad review covers decoupling together with
decoherence-free subspaces and noiseless subsystems [@lidar2014review].

## In experiments

- **Trapped ions.** Optimized sequences strongly suppressed qubit errors in a model quantum memory
  [@biercuk2009memory].
- **Solid-state spins.** Decoupling a single NV-centre spin from its spin bath extended its coherence time for arbitrary
  states up to 25-fold [@delange2010universal].
- **Superconducting qubits.** A survey of 60 sequences from 10 families on cloud devices found that high-order
  universally robust and quadratic DD sequences performed best overall. Basic sequences such as CPMG and XY-4 could
  nearly match them once the pulse interval was optimized [@ezzell2023survey].

## Decoupling as filtering

In the frequency domain, a decoupling sequence acts as a **filter** on the noise spectrum. The coherence decays
according to the overlap of the noise power spectral density with a filter function determined by the pulse timings
[@cywinski2008dephasing]. This viewpoint explains why different sequences suit different noise spectra. Run in
reverse, it turns decoupling into a spectrometer for the noise itself; see [[filter-functions]].

## Beyond memory

- **Protected gates.** Decoupling can be merged with gate operations to build dynamically error-corrected gates with
  bounded-strength controls [@khodjasteh2009gates]; see [[gate-synthesis]].
- **Sensing.** The same sequences turn a qubit into a narrow-band detector of oscillating signals, a workhorse of
  quantum sensing with spins [@degen2017sensing]; see [[quantum-sensing]].

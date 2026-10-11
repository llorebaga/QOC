---
updated: 2026-10-11
status: draft
key_papers:
  - key: kofman2001universal
    note: A universal formula for decay under modulation — the decay rate is the overlap of the bath's coupling spectrum with the spectrum of the control.
  - key: green2013universal
    note: Generalized filter functions for arbitrary single-qubit control with noise along all axes, from time-domain control matrices.
  - key: pazsilva2014transfer
    note: A general transfer-function framework. A finite set of fundamental filter functions defines a filtering order distinct from the Magnus order.
  - key: soare2014filtering
    note: Experimental demonstration with trapped ions of noise filtering by designed control, including band-selective filters.
  - key: hangleiter2021filter
    note: Filter functions for complete quantum processes of gate sequences, with a composition rule and an open-source package.
software:
  - name: filter_functions
    url: https://github.com/qutech/filter_functions
    note: efficient computation of generalized filter functions and quantum processes (Python)
---

Many quantum devices are limited by noise that **fluctuates in time** — $1/f$ charge or flux noise, magnetic-field
fluctuations, laser phase noise. Its effect depends on how the noise spectrum overlaps with the "spectrum" of the
control. **Filter functions** make this precise. To leading order, the error of an operation is the integral of the
noise power spectral density multiplied by a filter function that depends only on the control. This gives a
transparent, frequency-domain way to evaluate, compare and *design* pulses for time-dependent noise.

## The idea

Consider a qubit with weak classical noise, $H(t) = H_c(t) + \beta(t)\,\sigma_z$, where $\beta(t)$ is a stationary
Gaussian process with power spectral density $S(\omega)$. To leading order in the noise, the average error of the
controlled evolution takes the form

$$1 - \bar F \;\approx\; \frac{1}{2\pi}\int_{-\infty}^{\infty} S(\omega)\,F_c(\omega)\,d\omega ,$$

where the **filter function** $F_c(\omega)$ depends only on the control $H_c(t)$ (normalization conventions differ
between papers). A good control makes $F_c(\omega)$ small wherever $S(\omega)$ is large.

For pure dephasing under a sequence of instantaneous $\pi$ pulses, the filter function is the squared Fourier
transform of the *switching function* $f(t) = \pm 1$, which changes sign at every pulse:

$$F_c(\omega) \;\propto\; \Big|\int_0^T f(t)\,e^{i\omega t}\,dt\Big|^2 .$$

A free evolution passes low frequencies ($F_c$ peaks at $\omega = 0$); a spin echo or CPMG sequence suppresses them
and moves the sensitivity to a band near $\omega \approx \pi/\tau_p$, where $\tau_p$ is the spacing between pulses. This explains how [[dynamical-decoupling|dynamical decoupling]]
works and why the best sequence depends on the noise spectrum [@cywinski2008dephasing]. Kofman and Kurizki gave the
general form of this idea for decay into a continuum: the modified decay rate is the overlap of the bath spectrum with
the spectrum of the modulation [@kofman2001universal].

## Filter functions for arbitrary gates

Decoupling sequences ideally do nothing. Gates rotate the qubit, so noise along one axis turns into errors along
others. Generalized filter functions handle this. They are built from *control matrices* that track how each noise
axis is transformed by the control, and they cover arbitrary piecewise-constant pulses with noise along all axes
[@green2012filtering; @green2013universal]. A transfer-function framework shows how arbitrary filter functions are
assembled from a finite, computable set of fundamental ones. It also defines a *filtering order*, which captures
features of error suppression that differ from the order of cancellation in the Magnus expansion
[@pazsilva2014transfer]. The formalism also extends to complete quantum processes of gate sequences, with a simple
rule for composing them [@hangleiter2021filter].

## Designing pulses with filter functions

Because the error is an explicit functional of the control, filter functions can be used as objectives. Examples:

- **Walsh-synthesized gates.** Amplitude and phase modulations built from Walsh functions are optimized to minimize
  the filter function in chosen bands [@ball2015walsh].
- **Experimental noise filtering.** Designed controls suppress noise in selected frequency bands, which has been
  demonstrated in trapped ions [@soare2014filtering].
- **Combined robustness.** Filter-function objectives for time-dependent noise can be optimized together with
  sensitivity to static errors; see [[robust-optimal-control]].

## Noise spectroscopy

The relation can also be inverted. Applying sequences with known, narrow-band filter functions and measuring the
resulting decay **reconstructs the noise spectrum** $S(\omega)$. This has been done in NMR
[@alvarez2011spectrum], in superconducting flux qubits [@bylander2011spectroscopy] and, with multi-pulse frequency
combs, for non-Gaussian noise [@norris2016nongaussian]. A known spectrum then feeds back into better control design;
see [[model-learning]] and [[quantum-sensing]].

## Limitations

- **Leading order.** The standard formulas assume weak noise. Strong noise needs higher-order terms or full simulation.
- **Classical, Gaussian noise.** Most results treat classical, stationary Gaussian noise. Quantum or non-Gaussian
  environments require extensions [@norris2016nongaussian].
- **Correlations across gates.** Noise correlated over many gates breaks the assumption that errors of successive
  operations are independent. Process-level filter functions address this [@hangleiter2021filter].

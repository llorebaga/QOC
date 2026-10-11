---
updated: 2026-10-11
status: draft
key_papers:
  - key: motzoi2011rapid
    note: Optimal control with rapidly varying Hamiltonians and filtered controls, accounting for the bandwidth of the electronics.
  - key: hincks2015nonlinear
    note: Includes distortions of the control hardware, including non-linear ones, in the optimization through the chain rule.
  - key: lucarelli2018grafs
    note: Pulses in a basis of Slepian functions, connecting the time–bandwidth product to the minimal control time.
  - key: petersson2022bsplines
    note: B-splines with carrier waves — a compact, smooth parametrization designed for superconducting qudits.
software:
  - name: Juqbox.jl
    url: https://github.com/LLNL/Juqbox.jl
    note: B-spline control parametrization (Julia)
  - name: QuOCS
    url: https://github.com/Quantum-OCS/QuOCS
    note: Fourier, Chebyshev, sigmoid, sinc and piecewise bases
---

Before a pulse can be optimized it must be **described by finitely many numbers**. The choice of that
description — the *parametrization* — and the way experimental limits are imposed on it often decide whether an
optimized pulse works in the laboratory at all. A pulse that reaches 99.999 % fidelity in simulation but needs
infinite bandwidth, or exceeds the amplifier's range, is of little use.

## Common parametrizations

| Parametrization | Typical method | Parameters | Character |
|---|---|---|---|
| Piecewise constant | [[grape|GRAPE]] | one per time slice and control (hundreds–thousands) | maximally flexible; no built-in smoothness |
| Truncated randomized Fourier basis | [[crab|CRAB / dCRAB]] | a few to tens of coefficients | smooth, bandwidth-limited by construction |
| Slepian (prolate spheroidal) functions | GRAFS | tens | optimal concentration in a given bandwidth [@lucarelli2018grafs] |
| B-splines (with carrier waves) | Juqbox | tens–hundreds | smooth, local support, efficient for multi-level systems [@petersson2022bsplines] |
| Analytic shapes (Gaussian, DRAG, …) | [[goat|GOAT]] | a handful | physically interpretable, hardware-native [@machnes2018goat; @skinner2010analytic] |
| Polynomial / power series | [[polynomial-optimization|QCPOP]] | a few | makes the problem polynomial for global optimization |

Analytic corrections such as [[drag|DRAG]] [@motzoi2009drag] are themselves parametrizations: a few well-chosen
terms that remove a specific error.

How many parameters are actually needed? An information-theoretic argument relates the minimal number of
independent control parameters to the dimension of the set of states the dynamics can reach in the available
time [@lloyd2014information]. Bandwidth and duration are linked: for a fixed bandwidth there is a minimal time to
reach a target [@lucarelli2018grafs]. See [[control-complexity]] and [[quantum-speed-limits]].

## Imposing experimental constraints

- **Amplitude.** Hard bounds through bound-constrained optimizers (L-BFGS-B), through a smooth mapping such as
  $u = u_{\max}\tanh(v)$ that makes the problem unconstrained, or through penalties. Plain clipping after each step is
  simple but can stall the optimizer.
- **Smoothness and bandwidth.** Penalize derivatives, e.g. $\lambda \int_0^T \dot u(t)^2\,dt$; optimize on a
  coarse grid and interpolate; or use a smooth basis with limited frequency content (CRAB, splines, Slepians).
- **Transfer functions.** Cables, filters and amplifiers distort the programmed pulse. If the distortion is a linear
  filter with impulse response $h(t)$, the field seen by the system is the convolution
  $u_{\rm act}(t) = \int h(t-\tau)\,u(\tau)\,d\tau$. Optimizing *through* this map — by the chain rule — yields pulses
  that are correct after distortion [@motzoi2011rapid]. The same works for non-linear hardware responses
  [@hincks2015nonlinear].
- **Boundary conditions.** Pulses usually must start and end at zero. Shape functions that vanish at $t=0$ and
  $t=T$ do this automatically — Krotov's update shape $S(t)$ ([[krotov]]) or CRAB's boundary factor $\lambda(t)$
  ([[crab]]).
- **Energy and power.** A fluence penalty $\lambda \int u(t)^2\,dt$ limits heating and drive-induced errors.
- **Sampling.** Arbitrary waveform generators output samples at a fixed rate. Matching the control grid to it, and
  using a finer grid for simulation, avoids aliasing between model and hardware; see [[control-hardware]].

## Choosing a parametrization

- **Exploration and benchmarks:** piecewise constant with GRAPE — maximal freedom shows what is possible in
  principle.
- **Experiments:** a compact, smooth basis with the hardware constraints built in, so the result can be transferred to
  the device and recalibrated in closed loop ([[closed-loop]]).
- **Robustness:** fewer parameters are easier to calibrate, while extra freedom can be spent on making the pulse robust
  ([[robust-optimal-control]]).

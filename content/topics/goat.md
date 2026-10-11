---
updated: 2026-10-11
status: draft
key_papers:
  - key: machnes2018goat
    note: Introduces GOAT — exact gradients for arbitrary analytic pulse shapes by propagating the derivatives of the evolution along with the evolution itself.
  - key: lucarelli2018grafs
    note: GRAFS, a related approach that optimizes smooth pulses in a basis of Slepian functions, and connects bandwidth to minimal control time.
  - key: wittler2021c3
    note: C3, a toolset that optimizes analytic pulse parametrizations with automatic differentiation and combines it with calibration and model learning on real devices.
software:
  - name: qutip-qoc
    url: https://github.com/qutip/qutip-qoc
    note: an extended GOAT implementation (and JOPT, its JAX/automatic-differentiation counterpart)
  - name: C3
    url: https://github.com/q-optimize/c3
    note: control, calibration and characterization toolset (TensorFlow)
---

**GOAT** — *Gradient Optimization of Analytic conTrols* — computes exact gradients of the fidelity with respect to
the parameters of *any* smooth, analytically defined pulse shape. Machnes, Assémat, Tannor and Wilhelm introduced it
to optimize controls for practical qubits [@machnes2018goat]: Gaussian or DRAG-like envelopes, sums of Fourier
components, pulses passed through a filter — whatever the hardware naturally produces. It avoids the
piecewise-constant approximation of [[grape|GRAPE]] entirely.

## The idea

Let the controls depend on a set of parameters $\boldsymbol{\alpha}$ through known functions,

$$H(\boldsymbol{\alpha}, t) = H_0 + \sum_k c_k(\boldsymbol{\alpha}, t)\, H_k ,$$

for example $c(\boldsymbol\alpha, t) = \alpha_1 \exp[-(t-\alpha_2)^2/\alpha_3^2]\cos(\alpha_4 t)$. Differentiating
the Schrödinger equation $\partial_t U = -iHU$ with respect to a parameter $\alpha_j$ gives an equation for the
derivative of the propagator,

$$\partial_t\big(\partial_{\alpha_j} U\big) = -i\,\big(\partial_{\alpha_j} H\big)\,U - i\,H\,\big(\partial_{\alpha_j} U\big),
\qquad \partial_{\alpha_j} H = \sum_k \frac{\partial c_k}{\partial \alpha_j}\,H_k .$$

GOAT integrates this together with the evolution as one coupled linear system,

$$\frac{\partial}{\partial t}\begin{pmatrix} U \\ \partial_{\alpha_j} U \end{pmatrix}
= -i \begin{pmatrix} H & 0 \\ \partial_{\alpha_j} H & H \end{pmatrix}
\begin{pmatrix} U \\ \partial_{\alpha_j} U \end{pmatrix},
\qquad U(0) = \mathbb{1},\;\; \partial_{\alpha_j} U(0) = 0,$$

using a standard high-accuracy ODE solver with error control. At the final time, $U(T)$ and all
$\partial_{\alpha_j} U(T)$ are known, so the gradient of any figure of merit follows directly. For the gate
fidelity $g = \frac{1}{d}\,\big|\mathrm{Tr}(U_{\rm tgt}^\dagger U(T))\big|$, for example,

$$\frac{\partial g}{\partial \alpha_j} = \frac{1}{d}\,\mathrm{Re}\!\left[
\frac{\mathrm{Tr}\big(U_{\rm tgt}^\dagger U(T)\big)^{*}}{\big|\mathrm{Tr}\big(U_{\rm tgt}^\dagger U(T)\big)\big|}\,
\mathrm{Tr}\big(U_{\rm tgt}^\dagger\, \partial_{\alpha_j} U(T)\big)\right].$$

The gradient is then passed to a standard optimizer such as L-BFGS ([[second-order-methods]]).

## Why it is useful

- **Hardware-native pulses.** The optimizer works directly in the parameter space of the pulses the electronics can
  produce. Transfer functions, filters and frequency limits are included analytically in $c_k(\boldsymbol\alpha, t)$
  instead of being imposed afterwards; see [[pulse-parametrization]].
- **Few, meaningful parameters.** A dozen parameters with a physical meaning (amplitudes, widths, frequencies,
  phases) are easier to calibrate and to transfer to an experiment than hundreds of piecewise-constant values; see
  [[closed-loop]].
- **Accurate.** The ODE solver controls the error of the evolution and of the gradient, with no time-slicing
  approximation.

## How it relates to other methods

GOAT is *forward-mode* differentiation: one extra copy of the evolution is propagated for every parameter. GRAPE's
backward sweep is *reverse-mode* differentiation (the adjoint method), which gets all derivatives for the cost of
about one extra propagation. So GOAT is the natural choice for a few to a few dozen parameters and smooth pulses,
while reverse-mode methods win when there are thousands of parameters. Automatic-differentiation frameworks
implement both modes generically; see [[autodiff-control]].

Related approaches optimize smooth pulses in a fixed analytic basis. GRAFS uses discrete prolate spheroidal
(Slepian) functions, which concentrate energy in a given bandwidth [@lucarelli2018grafs]. CRAB uses randomized
Fourier components [[crab]].

## Strengths and limitations

**Strengths**

- Exact gradients for arbitrary differentiable pulse shapes, including filters and transfer functions.
- Few, interpretable parameters, and pulses that hardware can reproduce.
- Accuracy controlled by the ODE solver.

**Limitations**

- Cost grows linearly with the number of parameters (the coupled system has $1 + n_\alpha$ blocks).
- A local method; the result depends on the chosen pulse family, which may not contain the optimum.
- Evaluating $\partial c_k / \partial \alpha_j$ by hand for complicated parametrizations is tedious; automatic
  differentiation is often used for it.

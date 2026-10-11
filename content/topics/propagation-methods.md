---
updated: 2026-10-11
status: draft
key_papers:
  - key: kosloff1988methods
    note: A classic review of time-dependent propagation methods — Chebyshev, Lanczos, split-operator — and their accuracy and cost.
  - key: moler2003nineteen
    note: The standard survey of ways to compute a matrix exponential, and of how they can fail.
  - key: blanes2009magnus
    note: A comprehensive review of the Magnus expansion and the structure-preserving integrators built on it.
  - key: goodwin2015auxiliary
    note: The auxiliary-matrix approach, giving exact propagator derivatives for optimal control from one larger exponential.
software:
  - name: dynamiqs
    url: https://github.com/dynamiqs/dynamiqs
    note: GPU-accelerated, differentiable solvers for closed and open systems (JAX)
  - name: QuantumControl.jl
    url: https://github.com/JuliaQuantumControl/QuantumControl.jl
    note: Chebyshev, Newton and exponential propagators (via QuantumPropagators.jl), Julia
  - name: Spinach
    url: https://spindynamics.org
    note: large-scale spin-dynamics propagation in Liouville space (MATLAB)
---

Every optimal-control algorithm spends most of its time **propagating**: computing the time evolution of states or
operators under the current controls — and, for gradient methods, its derivatives — over and over again. How
fast and how accurately that is done sets the size of the systems and the number of iterations that are practical.
This page collects the numerical methods behind the optimizers.

## Propagating one time step

Over a short step $\Delta t$ in which the Hamiltonian is (approximately) constant, one needs
$e^{-iH\Delta t}$ or its action on a state.

- **Dense matrix exponentials.** For small systems, $e^{-iH\Delta t}$ is computed directly. Scaling-and-squaring
  with Padé approximants is the standard general-purpose method. Since $H$ is Hermitian, an eigendecomposition is
  also convenient, and it gives exact derivatives (below). Many methods exist and some fail badly in practice
  [@moler2003nineteen].
- **Krylov subspace (Lanczos).** For large sparse $H$, the action $e^{-iH\Delta t}|\psi\rangle$ is approximated
  in the small subspace spanned by $|\psi\rangle, H|\psi\rangle, H^2|\psi\rangle, \dots$, using only matrix–vector
  products [@park1986lanczos].
- **Chebyshev expansion.** The exponential is expanded in Chebyshev polynomials of the spectrally rescaled
  Hamiltonian. The error is distributed uniformly over the spectrum and the method is very efficient for long steps
  [@taleezer1984chebyshev]. Variants with iterative time ordering handle explicitly time-dependent Hamiltonians
  [@ndong2010chebychev].
- **Split-operator.** For particles on spatial grids, kinetic and potential terms are exponentiated separately, in
  momentum and position space, using fast Fourier transforms [@feit1982spectral].

Kosloff's review compares these approaches for molecular dynamics [@kosloff1988methods]. Their trade-offs carry
over to control.

## Time-dependent Hamiltonians

Control Hamiltonians change in time. Options include:

- **piecewise-constant approximation** — natural for [[grape|GRAPE]], with a time step small compared with the
  inverse spectral width of $H(t)$;
- **Magnus integrators**, which exponentiate a truncated Magnus series and stay exactly unitary, with higher-order
  accuracy for smooth controls [@blanes2009magnus];
- **general ODE solvers** (e.g. adaptive Runge–Kutta), which are flexible and error-controlled but not exactly
  unitary — used, for example, by [[goat|GOAT]].

## Derivatives of propagators

Gradient methods need $\partial e^{-iH\Delta t}/\partial u$ where $H = H_0 + u H_k$. Three exact approaches are common:

**Eigenbasis formula.** With $H|a\rangle = \lambda_a|a\rangle$, the matrix elements of the derivative are

$$\Big\langle a\Big|\frac{\partial e^{-iH\Delta t}}{\partial u}\Big|b\Big\rangle
= \langle a|H_k|b\rangle\,
\frac{e^{-i\lambda_a \Delta t} - e^{-i\lambda_b \Delta t}}{\lambda_a - \lambda_b},$$

with the limit $-i\Delta t\, e^{-i\lambda_a\Delta t}$ when $\lambda_a = \lambda_b$.

**Augmented (auxiliary) matrix.** The exponential of a block-triangular matrix contains the derivative in its
off-diagonal block [@vanloan1978integrals]:

$$\exp\!\left[\Delta t\begin{pmatrix} A & B \\ 0 & A\end{pmatrix}\right]
= \begin{pmatrix} e^{A\Delta t} & \displaystyle\int_0^{\Delta t} e^{A(\Delta t-s)}\,B\,e^{As}\,ds \\ 0 & e^{A\Delta t}\end{pmatrix},$$

and with $A = -iH$, $B = -iH_k$ the upper-right block is exactly $\partial e^{-iH\Delta t}/\partial u$. This has
been developed into a general tool for optimal control and spin dynamics [@goodwin2015auxiliary].

**Fréchet-derivative algorithms** compute the derivative of the matrix exponential along a direction with the same
scaling-and-squaring machinery as the exponential itself [@almohy2009frechet].

[[autodiff-control|Automatic differentiation]] obtains the same derivatives automatically, provided the framework
differentiates matrix functions correctly.

## Scaling up

- **Open systems.** Density matrices live in a space of dimension $d^2$, so Liouville-space propagators are
  expensive. Stochastic quantum trajectories trade this for averaging over many state vectors
  [@abdelhafez2019trajectories]; see [[open-system-control]].
- **Many-body systems.** Tensor-network methods (TEBD, tDMRG, TDVP) propagate states with limited entanglement in
  very large Hilbert spaces, and have been coupled to optimal control from the start [@doria2011crab]; see
  [[many-body-control]].
- **Hardware.** GPUs accelerate both the dense linear algebra and automatic differentiation [@leung2017gpu].
- **Approximations as a feature.** Truncated Magnus and Chebyshev expansions also turn the control problem into a
  polynomial one that can be solved globally ([[polynomial-optimization|QCPOP]]).

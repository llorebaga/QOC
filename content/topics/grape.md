---
updated: 2026-10-11
status: draft
key_papers:
  - key: khaneja2005grape
    note: The original paper. Introduces piecewise-constant controls with an efficient gradient computed from one forward and one backward propagation, for NMR pulse design.
  - key: defouquieres2011second
    note: Exact gradients combined with quasi-Newton (BFGS) updates — the form of GRAPE most implementations use today.
  - key: machnes2011dynamo
    note: Compares GRAPE, Krotov and hybrid schemes in a single framework (DYNAMO); a practical guide to which update strategy to use when.
  - key: motzoi2011rapid
    note: GRAPE for rapidly varying Hamiltonians and filtered, bandwidth-limited controls, as needed for superconducting qubits.
software:
  - name: qutip-qoc / qutip-qtrl
    url: https://github.com/qutip/qutip-qoc
    note: GRAPE (and CRAB, GOAT, JOPT) in Python, built on QuTiP
  - name: GRAPE.jl
    url: https://github.com/JuliaQuantumControl/GRAPE.jl
    note: part of the QuantumControl.jl framework in Julia
  - name: Spinach
    url: https://spindynamics.org
    note: spin-dynamics library (MATLAB) with GRAPE for magnetic resonance
---

**GRAPE** — *Gradient Ascent Pulse Engineering* — is the most widely used numerical method in quantum optimal
control. It was introduced by Khaneja, Reiss, Kehlet, Schulte-Herbrüggen and Glaser to design pulse sequences for
nuclear magnetic resonance [@khaneja2005grape] and was soon applied to quantum gates
[@schulteherbruggen2005synthesis]. The method chops the control fields into piecewise-constant segments and
updates all of them at once using the gradient of the fidelity. That gradient costs about as much as two
simulations of the dynamics, however many segments there are.

## The idea

Write the Hamiltonian as a fixed drift plus controllable terms (we set $\hbar = 1$):

$$H(t) = H_0 + \sum_{k=1}^{K} u_k(t)\, H_k .$$

We want control functions $u_k(t)$ on $[0, T]$ that make the evolution do something specific — for example
implement a target gate $U_{\rm tgt}$. GRAPE divides $[0,T]$ into $N$ slices of length $\Delta t = T/N$ and
takes every control to be constant on each slice, $u_k(t) = u_{k,j}$ for $t$ in slice $j$. The evolution then becomes a
product of $N$ fixed propagators,

$$U(T) = U_N U_{N-1} \cdots U_1, \qquad
U_j = \exp\!\Big[-i\,\Delta t\,\Big(H_0 + \sum_k u_{k,j} H_k\Big)\Big],$$

and the fidelity becomes an ordinary function of the $N \times K$ numbers $u_{k,j}$. Maximizing it is a standard
finite-dimensional optimization problem — the infinite-dimensional control problem has been
[[pulse-parametrization|parametrized]].

## The gradient

The crucial observation of GRAPE is that the gradient with respect to *every* $u_{k,j}$ can be obtained from two
sweeps through time. Take the gate fidelity

$$\Phi = \frac{1}{d^2}\,\Big|\mathrm{Tr}\big(U_{\rm tgt}^\dagger U(T)\big)\Big|^2 ,$$

where $d$ is the Hilbert-space dimension. Define the forward-propagated operators $X_j = U_j \cdots U_1$ and the
backward-propagated target $P_j = U_{j+1}^\dagger \cdots U_N^\dagger\, U_{\rm tgt}$. With the Hilbert–Schmidt
product $\langle A | B \rangle = \mathrm{Tr}(A^\dagger B)$, the overlap can be "cut" at any slice:
$\mathrm{Tr}(U_{\rm tgt}^\dagger U(T)) = \langle P_j | X_j \rangle$ for every $j$. A change of $u_{k,j}$ only
affects $U_j$, and to first order in $\Delta t$

$$\frac{\partial U_j}{\partial u_{k,j}} \approx -i\,\Delta t\, H_k\, U_j ,$$

so that

$$\frac{\partial \Phi}{\partial u_{k,j}} \approx -\frac{2}{d^2}\,
\mathrm{Re}\Big[\big\langle P_j \big|\, i\,\Delta t\, H_k X_j \big\rangle\,\big\langle X_j \big| P_j\big\rangle\Big].$$

One forward sweep stores the $X_j$, one backward sweep generates the $P_j$, and the gradient for all slices and
all controls follows from inexpensive matrix products. The same structure holds for state-to-state transfer
(states instead of unitaries), for open systems (density matrices and superoperators), and for other figures of merit
— see [[problem-formulation]]. In the language of optimal-control theory, $P_j$ is the co-state of
[[pmp|Pontryagin's maximum principle]], and the backward sweep is what machine learning calls back-propagation
(see [[autodiff-control]]).

!!! note "Exact gradients"
    The first-order expression is only accurate when $\Delta t\,\lVert H \rVert \ll 1$. The exact derivative of the
    matrix exponential can be computed from the eigendecomposition of each slice Hamiltonian, or from the
    exponential of an augmented block matrix [@goodwin2015auxiliary]. Modern implementations use the exact
    gradient; see [[propagation-methods]].

The original paper updated the controls by plain gradient ascent, $u_{k,j} \leftarrow u_{k,j} + \epsilon\,
\partial\Phi/\partial u_{k,j}$. In practice, GRAPE is almost always combined with a quasi-Newton method such as
L-BFGS, which uses the history of gradients to approximate curvature and converges much faster near the optimum
[@defouquieres2011second] — see [[second-order-methods]].

## In practice

- **Time grid.** $N$ must be large enough to resolve the dynamics, but very fine, independent slices produce
  jagged pulses that hardware cannot reproduce. Smoothness and bandwidth limits are imposed with penalties, filters
  or a coarser control grid than simulation grid [@motzoi2011rapid]; see [[pulse-parametrization]].
- **Constraints.** Amplitude limits are handled with bound-constrained optimizers (e.g. L-BFGS-B) or by
  clipping; power penalties are added to the cost.
- **Robustness.** To make a pulse work across a range of parameters, optimize the *average* fidelity over an
  ensemble of Hamiltonians — the gradient is simply the average of the individual gradients. This is how broadband
  NMR pulses are designed; see [[robust-optimal-control]].
- **Control time.** Below a minimal duration, no control reaches unit fidelity; scanning $T$ with GRAPE is a
  standard way to locate this [[quantum-speed-limits|quantum speed limit]] numerically [@caneva2009qsl].
- **Initial guesses and local optima.** GRAPE is a local method. For many unconstrained problems the
  [[control-landscapes|control landscape]] has no traps [@rabitz2004landscape], but with constraints (short times,
  few parameters, bounded amplitudes) local optima appear and multiple random restarts are common.
- **Cost.** Each iteration needs about $2N$ propagator evaluations. For gates, each involves matrix exponentials of
  dimension $d$ ($\mathcal{O}(d^3)$); for state transfer, only matrix–vector products are needed, which scales to much
  larger systems.

## Variants and relatives

- **Quasi-Newton and Newton GRAPE** — L-BFGS updates with exact gradients [@defouquieres2011second], and
  regularized Newton–Raphson using the full Hessian [@goodwin2016newton]. See [[second-order-methods]].
- **Krotov's method** updates the controls sequentially in time instead of concurrently, and guarantees monotonic
  convergence; GRAPE and Krotov have been compared systematically within one framework [@machnes2011dynamo].
  See [[krotov]].
- **Smooth, analytic controls** — GOAT computes exact gradients for arbitrary parametrized pulse shapes
  [@machnes2018goat]; GRAFS uses a basis of Slepian functions [@lucarelli2018grafs]. See [[goat]].
- **Automatic differentiation** — GRAPE-like gradients computed by machine-learning frameworks on GPUs
  [@leung2017gpu]. See [[autodiff-control]].

Optimal-control design of magnetic-resonance pulses, and gradient-based quantum optimal control in general, predate
GRAPE [@conolly1986mri; @peirce1988optimal]. GRAPE's lasting contribution was a simple, general and efficient
recipe for the gradient of piecewise-constant controls.

## Strengths and limitations

**Strengths**

- Gradients for all parameters at the cost of roughly two simulations.
- Simple and general: works for gates, states, ensembles, open systems and many figures of merit.
- Fast convergence when combined with L-BFGS.

**Limitations**

- A local method: it converges to the nearest optimum, so hard problems need restarts — or a global method such
  as [[polynomial-optimization|QCPOP]].
- Piecewise-constant pulses with many independent segments can be unphysical; hardware constraints must be added
  explicitly.
- Memory grows with the number of slices, because forward-propagated operators are stored.

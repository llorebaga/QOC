---
updated: 2026-10-11
status: draft
key_papers:
  - key: bondar2025qcpop
    note: Introduces QCPOP. Quantum control problems are approximated by polynomial optimization problems and solved globally with moment–SOS and homotopy-continuation methods.
  - key: baladagaggioli2025gates
    note: Gate synthesis by polynomial optimization over the Hermitian generators of the evolution, with certificates of global optimality, benchmarked against GRAPE and CRAB.
  - key: lasserre2001global
    note: The moment hierarchy — the mathematical engine behind global polynomial optimization.
  - key: bondar2020uncomputability
    note: Shows that deciding whether a quantum control task is possible is uncomputable on a Turing machine — the open question QCPOP revisits in the real-number model of computation.
software:
  - name: QControlPolyOpt
    url: https://github.com/dibondar/QControlPolyOpt
    note: code and notebooks accompanying the QCPOP paper (Julia)
  - name: TSSOS
    url: https://github.com/wangjie212/TSSOS
    note: sparse moment–SOS hierarchy solver (Julia)
  - name: HomotopyContinuation.jl
    url: https://github.com/JuliaHomotopyContinuation/HomotopyContinuation.jl
    note: finds all solutions of polynomial systems (Julia)
---

**QCPOP** — *Quantum Control via POlynomial oPtimization* — looks for the **global** optimum of a quantum control
problem instead of a local one. It approximates the control problem by a *polynomial* optimization problem, then uses
methods developed in the last two decades that find, and can certify, the global optimum of polynomials. The method
was introduced by Bondar, Balada Gaggioli, Korpas, Mareček, Vala and Jacobs [@bondar2025qcpop], and extended to gate
synthesis by Balada Gaggioli *et al.* [@baladagaggioli2025gates].

## Why global optimization

Gradient methods such as [[grape|GRAPE]], [[krotov|Krotov]] or [[goat|GOAT]] converge to the *nearest* optimum.
For unconstrained problems the [[control-landscapes|control landscape]] is often free of traps, but realistic
constraints — short durations, few control parameters, bounded amplitudes — can create many local optima. Simple
examples have traps by construction [@pechen2011traps]. Local methods must then be restarted from many initial
guesses, and if the traps are dense enough they may never find a good solution. A global method removes this
problem: one run returns the best solution of the (approximated) problem.

## From quantum control to polynomials

Take a Hamiltonian $H = H_0 + E(t)\,V$ and a figure of merit such as the Hilbert–Schmidt distance
$F = \lVert U(T) - U^\star \rVert^2$ or the infidelity $1 - \big|\mathrm{Tr}\big(U(T)^\dagger U^\star\big)\big|/N$. QCPOP
turns $F$ into a polynomial in finitely many real variables with three approximations [@bondar2025qcpop]:

1. **Magnus expansion.** The propagator is written as $U(T) = \exp(\Lambda_n)$ with
   $\Lambda_n = \Omega_1 + \dots + \Omega_n$, where $\Omega_1 = \int_0^T A(t)\,dt$,
   $\Omega_2 = \tfrac12 \int_0^T\!\!\int_0^t [A(t), A(s)]\,ds\,dt$, … and $A = -iH$ [@blanes2009magnus]. Every
   truncation is exactly unitary, and the series converges when $\int_0^T \lVert A(t) \rVert\, dt < \pi$.
2. **Chebyshev expansion of the exponential.** The matrix exponential is replaced by a truncated Chebyshev
   series with Bessel-function coefficients, a polynomial in the generator $\Lambda_n$.
3. **A finite control basis.** The control is expanded as $E(t) = \sum_{k=0}^{m-1} x_k f_k(t)$, for example a power
   series $f_k(t) = t^k$.

Substituting (3) into (1), each Magnus term becomes a polynomial in the coefficients $x_k$; with (2), so does
$U(T)$, and therefore so does $F$. A QCPOP model is labelled by the truncation orders $(n, p, m)$ — Magnus terms,
Chebyshev terms and control parameters. In the examples studied, $n = 3$ and $p = 5$ were found to be sufficient.

For **piecewise-constant controls** the formulation is even simpler. With $m$ segments of constant amplitude $E_j$,
$U(T) = \prod_j \exp[-i(H_0 + E_j V)\,t_j]$, and only the Chebyshev expansion of each factor is needed — no Magnus
expansion.

## Solving the polynomial problem globally

A polynomial optimization problem asks for the global minimum of a polynomial $f(\mathbf x)$, possibly subject to
polynomial constraints $g_i(\mathbf x) \ge 0$. Two families of methods are used:

- **The moment–sum-of-squares (SOS) hierarchy.** Lasserre's moment relaxations, and their dual SOS formulation,
  form a sequence of semidefinite programs whose optimal values are increasing lower bounds that converge to
  the global minimum under mild conditions [@lasserre2001global; @parrilo2003semidefinite]. When a relaxation is
  tight, this is certified and the minimizer can be extracted. Exploiting sparsity (as in TSSOS) is essential to
  make the relaxations tractable [@wang2021tssos].
- **Homotopy continuation.** This method numerically tracks *all* solutions of the polynomial system of critical-point
  equations, so every extremum is found and the best one chosen [@breiding2018homotopy].

In the original study, homotopy continuation worked better for the infidelity, and the moment–SOS hierarchy for
the Hilbert–Schmidt distance [@bondar2025qcpop].

## What it has shown

- **Traps are no obstacle.** On the three-level problem of Pechen and Tannor, whose objective has a trap at zero
  control [@pechen2011traps], homotopy continuation applied to the QCPOP polynomial returns all extrema. A gradient
  method started near zero finds only the local one.
- **Gate synthesis.** For 1000 random target unitaries of a three-level system, QCPOP reached better fidelities than
  GRAPE and CRAB, at a comparable time per run [@bondar2025qcpop].
- **Dense traps.** In a state-transfer problem between two coupled oscillators at very short times, gradient
  searches fail and need thousands of restarts. QCPOP found the best solution with three control segments in a single
  run, and showed that no two-segment solution exists [@bondar2025qcpop].
- **Certified gates.** Optimizing over the Hermitian generators of the unitaries instead of the unitaries
  themselves keeps the polynomials small. This gives single-shot gate synthesis with certificates of global optimality
  [@baladagaggioli2025gates].

The same idea applies beyond control. Hamiltonian identification can be written as a polynomial optimization
[@bondar2025qcpop], and so can learning the most accurate Markovian (Lindblad) model of an open system from
time-series data [@popovych2022identification] — see [[model-learning]].

## Computability

Deciding whether a given quantum control task is possible is **uncomputable** on a Turing machine: digitized quantum
control can encode Diophantine equations, which no algorithm can solve in general [@bondar2020uncomputability].
Casting control as polynomial optimization gives a different picture in the Blum–Shub–Smale model of computation,
which works with real numbers. There, quantum optimal control problems become computable, with a run time governed
by the convergence of the Magnus expansion and of the moment–SOS hierarchy [@bondar2025qcpop].

## Strengths and limitations

**Strengths**

- Finds the global optimum of the approximated problem in a single run, with certificates in the moment–SOS case.
- Unaffected by traps, however dense — and can prove that *no* better solution exists, which reveals the true limits
  of a given control setup ([[quantum-speed-limits]]).
- The same machinery serves control, Hamiltonian identification and system identification.

**Limitations**

- The size of the semidefinite programs grows quickly with the number of variables and the polynomial degree, so the
  number of control parameters is currently small; sparsity is crucial.
- The optimum is that of the *truncated* problem, so the solution should be checked against the exact dynamics. The
  Magnus variant also requires $\int \lVert A \rVert\, dt < \pi$.
- A young method: tools and practical guidelines are still being developed.

---
updated: 2026-10-11
status: draft
key_papers:
  - key: defouquieres2011second
    note: Shows that exact gradients combined with BFGS-type updates make GRAPE converge dramatically faster — now the standard way to run GRAPE.
  - key: goodwin2016newton
    note: Shows that the GRAPE Hessian costs no more, asymptotically, than the fidelity itself, and that regularized Newton–Raphson needs fewer trajectory evaluations than other GRAPE variants.
  - key: dalgaard2020hessian
    note: Exact second derivatives of the dynamics, which improve on BFGS for constrained gate synthesis in circuit QED.
  - key: nocedal2006numerical
    note: The standard reference on quasi-Newton methods, line searches, trust regions and constrained optimization.
software:
  - name: SciPy optimize
    url: https://docs.scipy.org/doc/scipy/reference/optimize.html
    note: L-BFGS-B, trust-region and SLSQP methods used by many Python control packages
  - name: Piccolo.jl
    url: https://github.com/harmoniqs/Piccolo.jl
    note: direct-collocation quantum optimal control with an interior-point solver (Julia)
---

Most numerical quantum-control methods produce a **gradient**. What they do with it matters as much as how they
compute it. Plain gradient ascent takes small steps in the direction of steepest increase and slows down in long,
curved valleys of the landscape. **Second-order methods** also use the *curvature* of the figure of merit. Newton
methods use the exact Hessian, quasi-Newton methods an approximation built up from successive gradients. They
converge much faster, especially near the optimum. Today they are the default engine behind [[grape|GRAPE]],
[[goat|GOAT]] and most gradient-based control codes.

## Newton and quasi-Newton steps

Near an optimum the figure of merit $J(\mathbf u)$ is well approximated by a quadratic, and Newton's method jumps to
its stationary point:

$$\Delta\mathbf u = -\big[\nabla^2 J(\mathbf u)\big]^{-1}\, \nabla J(\mathbf u).$$

Close to a non-degenerate optimum this converges quadratically. But the Hessian $\nabla^2 J$ of a problem with
$n$ control parameters is an $n \times n$ matrix that can be expensive to compute and is not positive-definite away
from the optimum.

**Quasi-Newton** methods avoid computing it. BFGS updates an approximation $B_k$ of the Hessian from the change in
the gradient along each step, so that it satisfies the *secant condition*

$$B_{k+1}\, \mathbf s_k = \mathbf y_k, \qquad \mathbf s_k = \mathbf u_{k+1} - \mathbf u_k,\quad
\mathbf y_k = \nabla J(\mathbf u_{k+1}) - \nabla J(\mathbf u_k).$$

**L-BFGS** keeps only the last few pairs $(\mathbf s_k, \mathbf y_k)$, so memory grows linearly with $n$; its
bound-constrained variant **L-BFGS-B** handles amplitude limits directly. Combined with a line search or a trust
region that guarantees sufficient progress, these are robust, general-purpose methods [@nocedal2006numerical].

## In quantum control

- **GRAPE with exact gradients and BFGS** converges much faster than the original gradient ascent. Its accuracy
  depends on using the exact rather than the first-order gradient, because quasi-Newton methods are sensitive to
  gradient errors [@defouquieres2011second]. Frameworks that compare update strategies systematically include such
  hybrids [@machnes2011dynamo].
- **Newton GRAPE.** The Hessian of the GRAPE fidelity turns out to be unusually cheap, with the same asymptotic
  cost as the fidelity itself. Regularized so that it is positive-definite far from the optimum (rational function
  optimization), Newton–Raphson GRAPE needs fewer trajectory evaluations than other GRAPE variants
  [@goodwin2016newton]. Newton methods for spin systems have also been analysed from the
  numerical-analysis side [@ciaramella2015newton].
- **Krotov with quasi-Newton updates** combines Krotov's sequential update with BFGS-style acceleration
  [@eitan2011krotovbfgs]; see [[krotov]].
- **Constraints.** Hard limits on amplitudes, slopes, energy or populations of unwanted levels are handled by
  constrained solvers such as sequential quadratic programming and interior-point methods. For constrained gate
  synthesis, exact second derivatives have been shown to outperform the BFGS approximation [@dalgaard2020hessian].

## Direct collocation

A different way to use second-order solvers treats not only the controls but also the **states at every time step**
as optimization variables. The Schrödinger equation is imposed as a set of equality constraints, one per time step,
and the resulting large but very sparse problem is solved with an interior-point method. This *direct collocation*
makes it easy to constrain the state trajectory, the control and its derivatives, and it gives the optimizer more
freedom to move through infeasible intermediate points [@trowbridge2023collocation].

## Practical notes

- A good default is **L-BFGS(-B) with exact gradients**. It needs nothing beyond the gradient, and little tuning.
- Full Newton methods pay off when very high fidelities are needed and the number of parameters is moderate.
- Quasi-Newton methods assume a smooth, deterministic objective. With noisy objectives (experimental
  fidelities, stochastic simulations) they can fail, and [[gradient-free]] methods or stochastic optimizers
  (Adam-type, as in [[autodiff-control]]) are more appropriate.
- Second-order information speeds up convergence to *a* local optimum. It does not help find a better one — that
  needs restarts, continuation in the control time, or a global method such as [[polynomial-optimization|QCPOP]].

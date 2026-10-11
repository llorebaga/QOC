---
updated: 2026-10-11
status: draft
key_papers:
  - key: somloi1993controlled
    note: One of the first applications of Krotov's method to quantum dynamics (laser control of molecular dissociation), by the group that brought the method into quantum control.
  - key: palao2003unitary
    note: Extends the method from state-to-state transfer to the optimization of unitary transformations — the route to quantum gates.
  - key: reich2012krotov
    note: The modern, general formulation, including the second-order term needed for non-convex functionals and non-linear dependence on the control.
  - key: goerz2019krotov
    note: A reference implementation in Python, with a clear pedagogical account of the method and its relation to GRAPE.
software:
  - name: krotov (Python)
    url: https://github.com/qucontrol/krotov
    note: reference implementation, built on QuTiP
  - name: Krotov.jl
    url: https://github.com/JuliaQuantumControl/Krotov.jl
    note: part of the QuantumControl.jl framework in Julia
---

**Krotov's method** is a gradient-type optimization scheme with two distinguishing features. Its update is
*sequential*: the correction to the control at time $t$ uses the state already propagated under the *updated*
control at earlier times. And it is *monotonically convergent*: every iteration is guaranteed not to make the
figure of merit worse. It comes from V. F. Krotov's global improvement methods in control theory. Tannor, Kazakov
and coworkers adapted it to quantum dynamics in the early 1990s for laser control of molecules
[@somloi1993controlled]. Together with [[grape|GRAPE]], it is one of the two classic workhorses of quantum
optimal control.

## The idea

As in all gradient methods, a figure of merit $J_T$ evaluated at the final time is minimized with respect to
control fields $\epsilon_l(t)$ that enter the Hamiltonian. Krotov's method minimizes the augmented functional

$$J = J_T\big[\{|\psi_k(T)\rangle\}\big] + \sum_l \int_0^T \frac{\lambda_{a,l}}{S_l(t)}
\big[\epsilon_l^{(i)}(t) - \epsilon_l^{(i-1)}(t)\big]^2 dt ,$$

where $i$ labels the iteration and $\{|\psi_k\rangle\}$ are the states being steered: one state for state-to-state
transfer, or a basis of states for a gate [@palao2003unitary]. The running cost penalizes the *change* of the
control from one iteration to the next, not the control itself. It therefore vanishes at convergence and does not
bias the final solution. $\lambda_{a,l}$ plays the role of an inverse step size, and the shape function
$S_l(t) \in [0,1]$ switches the update smoothly on and off — a simple way to keep the pulse's beginning and end
fixed.

## The update

For a Hamiltonian linear in the controls and a functional that depends only on the final states, the first-order
update reads (with $\hbar = 1$)

$$\Delta\epsilon_l^{(i)}(t) = \frac{S_l(t)}{\lambda_{a,l}}\;
\mathrm{Im} \sum_k \Big\langle \chi_k^{(i-1)}(t) \Big|\, \frac{\partial H}{\partial \epsilon_l}\, \Big| \psi_k^{(i)}(t) \Big\rangle .$$

Two sets of states appear:

- the **co-states** $|\chi_k^{(i-1)}(t)\rangle$, obtained by propagating the boundary condition
  $|\chi_k(T)\rangle = -\partial J_T / \partial \langle \psi_k(T)|$ *backward* in time with the *old* controls;
- the **forward states** $|\psi_k^{(i)}(t)\rangle$, propagated *forward* with the *new* controls, as they are being
  constructed.

So each iteration is one backward propagation followed by one forward propagation, during which the new control is
computed time step by time step. This sequential structure is what guarantees monotonic convergence. When the
functional is not convex in the states, or the Hamiltonian depends non-linearly on the control, monotonicity
requires an additional second-order term in the update [@reich2012krotov].

## Krotov and GRAPE

Both methods use the same two ingredients — forward-propagated states and backward-propagated co-states, as in
[[pmp|Pontryagin's maximum principle]] — but they combine them differently:

| | Krotov | GRAPE |
|---|---|---|
| Update | sequential in time, uses the updated forward state | concurrent: all time slices updated at once |
| Convergence | monotonic by construction | depends on step size / line search |
| Step size | set by $\lambda_a$ (fixed or adapted) | line search, or a quasi-Newton method |
| Time grid | controls on the propagation grid (continuous-time derivation) | piecewise-constant slices, can be coarse |

A commonly reported pattern is that sequential, Krotov-type updates make rapid progress in early iterations, while
concurrent updates with a quasi-Newton method converge faster close to the optimum. The trade-offs, which depend on
the problem, have been analysed within one common framework [@machnes2011dynamo]. The two ideas can also be combined — for example by adding quasi-Newton updates to Krotov's
method [@eitan2011krotovbfgs].

## Variants and extensions

- **Other monotonic schemes.** Zhu and Rabitz derived a closely related rapidly converging, monotonic iteration
  [@zhu1998rapid]; Maday and Turinici unified several such schemes in one family [@maday2003monotonic].
- **Gates.** Optimizing a unitary amounts to steering a set of basis states simultaneously
  [@palao2003unitary]; see [[gate-synthesis]].
- **Non-linear dynamics.** The method extends to the Gross–Pitaevskii (non-linear Schrödinger) equation, for example to
  load a Bose–Einstein condensate into an optical lattice [@sklarz2002loading]; see [[cold-atoms]].
- **Open systems.** Applied to density matrices with a Liouvillian instead of a Hamiltonian, the same update optimizes
  dissipative dynamics [@reich2012krotov; @goerz2019krotov]; see [[open-system-control]].

## Strengths and limitations

**Strengths**

- Monotonic convergence without line searches.
- Naturally produces time-continuous controls on the simulation grid; the shape function $S(t)$ gives simple
  control over switch-on and switch-off.
- Very general: states, gates, ensembles, open and non-linear dynamics.

**Limitations**

- A local method, like all gradient approaches.
- The step-size parameter $\lambda_a$ needs tuning: too small gives erratic updates, too large slow progress.
- Sequential updates require fine time steps, and constraints such as strict amplitude bounds or bandwidth limits are
  less natural to impose than in parametrized methods.

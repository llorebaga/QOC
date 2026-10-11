---
updated: 2026-10-11
status: draft
key_papers:
  - key: doria2011crab
    note: Introduces CRAB, together with time-dependent DMRG, to optimize the dynamics of a many-body system.
  - key: caneva2011crab
    note: The detailed account of the method — basis choice, randomization, boundary conditions — with benchmark problems.
  - key: rach2015dcrab
    note: dCRAB. Changing the random basis in successive "super-iterations" removes the false traps introduced by a truncated basis.
  - key: muller2022decade
    note: Review of ten years of CRAB and dCRAB, across platforms from cold atoms to NV centres and superconducting qubits.
software:
  - name: QuOCS
    url: https://github.com/Quantum-OCS/QuOCS
    note: the Quantum Optimal Control Suite (dCRAB, GRAPE, AD-based methods) in Python
  - name: qutip-qoc / qutip-qtrl
    url: https://github.com/qutip/qutip-qoc
    note: includes a CRAB implementation
---

**CRAB** — the *Chopped RAndom Basis* method — finds good controls with very few parameters. Instead of
optimizing the value of the field at every time step, it expands the correction to a pulse in a small basis of
smooth functions with *randomized* frequencies, and optimizes the handful of expansion coefficients, typically with
a [[gradient-free|gradient-free]] optimizer. CRAB was introduced by Doria, Calarco and Montangero to control
many-body dynamics simulated with tensor networks [@doria2011crab]. Its refinement **dCRAB** ("dressed" CRAB)
is now one of the standard methods of the field [@muller2022decade].

## The idea

Many control problems do not need a fully flexible pulse: the set of physically relevant controls is often
well described by a few smooth components. CRAB writes the pulse as a guess $u_0(t)$ times a correction expanded in
a truncated basis,

$$u(t) = u_0(t)\left[1 + \frac{1}{\lambda(t)}\sum_{n=1}^{N_c}
\Big(A_n \sin(\omega_n t) + B_n \cos(\omega_n t)\Big)\right],$$

where $\lambda(t)$ enforces boundary conditions — for example that the correction vanishes at $t=0$ and $t=T$
[@caneva2011crab]. The frequencies are the Fourier harmonics with a random detuning,

$$\omega_n = \frac{2\pi n\,(1 + r_n)}{T}, \qquad r_n \in [-\tfrac12, \tfrac12] \text{ random},$$

and the $2N_c$ coefficients $\{A_n, B_n\}$ (sometimes also the $\omega_n$) are optimized. With $N_c$ of order ten,
the search space is small enough for direct-search methods such as Nelder–Mead [@nelder1965simplex]. Those methods
only need the value of the figure of merit, not its gradient.

Why so few parameters can suffice has an information-theoretic answer. The number of independent control
parameters needed is set by the dimension of the manifold of states the dynamics can actually reach in the
available time, and for physical many-body dynamics this can be far smaller than the dimension of the Hilbert space
[@lloyd2014information]. See [[control-complexity]].

## dCRAB: escaping the traps of a truncated basis

Truncating the basis has a price: the restricted optimization can get stuck in "false traps" that are not local
optima of the full problem. **dCRAB** removes them by working in *super-iterations*. After optimizing the
coefficients in one random basis, it keeps the resulting pulse and adds a correction in a *new* random basis,

$$u^{(j)}(t) = u^{(j-1)}(t) + \sum_{n=1}^{N_c} c_n^{(j)} f_n^{(j)}(t),$$

so that, over many super-iterations, the pulse explores an unbounded function space while each individual
optimization stays low-dimensional. Rach *et al.* showed that this gives access to the trap-free landscape of the
full problem while the bandwidth stays limited [@rach2015dcrab]; see [[control-landscapes]].

## Why it is useful

- **Few parameters, smooth pulses.** A small Fourier-like basis builds in a bandwidth limit, so pulses are
  naturally smooth and experimentally friendly; see [[pulse-parametrization]].
- **No gradients needed.** The figure of merit can come from any simulation — tensor networks, mean-field or
  stochastic methods — or from the experiment itself. This makes CRAB a natural choice for
  [[closed-loop|closed-loop optimization]].
- **Many-body problems.** Combined with tensor-network simulations, it was designed for interacting systems from
  the start; see [[many-body-control]].
- **Remote and citizen-science optimization.** In its remote form (RedCRAB), dCRAB has been used to optimize
  an ultracold-atom experiment over the internet, alongside citizen scientists [@heck2018remote].

## Strengths and limitations

**Strengths**

- Small, smooth, bandwidth-limited search space with interpretable pulses.
- Works with any figure of merit, including noisy experimental ones.
- dCRAB avoids the false traps of a fixed truncated basis.

**Limitations**

- Gradient-free optimizers scale poorly with the number of parameters, so each super-iteration must stay small.
- When gradients *are* cheap, gradient-based methods ([[grape|GRAPE]], [[goat|GOAT]]) usually converge in fewer
  evaluations. CRAB's basis can also be used with gradients, and modern suites support both [@rossignolo2023quocs].
- Performance depends on choosing the guess pulse, basis type and number of components sensibly.

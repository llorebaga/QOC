---
updated: 2026-10-12
status: draft
key_papers:
  - key: peirce1988optimal
    note: An early rigorous formulation of quantum optimal control as a variational problem — existence of solutions, numerical approximation and applications.
  - key: nielsen2002fidelity
    note: The simple formula relating the average gate fidelity to the overlap of a quantum operation with the target unitary.
  - key: pedersen2007fidelity
    note: The average fidelity of an operation restricted to a subspace — the standard figure of merit when leakage out of the qubit subspace matters.
  - key: goerz2014dissipative
    note: For a gate on an open system, three well-chosen states are enough to optimize — whatever the dimension of the Hilbert space.
  - key: watts2015perfect
    note: A figure of merit that targets a whole class of gates (all perfect entanglers) instead of a single one, giving the optimizer more freedom.
---

Every optimal-control calculation starts by turning a physical wish — "flip this qubit", "prepare this entangled
state", "make the reaction go this way" — into a **mathematical optimization problem**. That means choosing the
model of the dynamics, the controls, the target, a **figure of merit** that measures success, and the constraints and
penalties that encode what the hardware can do. These choices often matter more than the choice of algorithm: an
optimizer can only find what the functional asks for.

## The ingredients

**Dynamics.** For closed systems, the Schrödinger equation for a state or a propagator,
$\dot U = -i\big(H_0 + \sum_k u_k(t) H_k\big)U$. For open systems, a master equation for the density matrix, most
often of Lindblad form; see [[open-system-control]]. For robustness, an *ensemble* of such equations with
different parameters; see [[robust-optimal-control]].

**Controls.** Functions $u_k(t)$ on $[0, T]$, in practice parametrized by finitely many numbers; see
[[pulse-parametrization]].

**Functional.** The quantity to minimize, usually written as

$$J[u] = J_T\big(\text{state at } T\big) \;+\; \int_0^T g_a\big(u(t)\big)\,dt \;+\; \int_0^T g_b\big(\text{state at } t\big)\,dt .$$

The final-time term $J_T$ measures how close the system ends up to the goal. The running cost $g_a$ penalizes the
control, for example its energy $\lambda \sum_k u_k^2$. The running cost $g_b$ penalizes undesired dynamics, such as
population in a leaky level during the pulse. In the language of control theory these are the Mayer, Lagrange and
Bolza forms of the problem.

**Constraints.** Fixed or free final time $T$, bounds on amplitudes, limited bandwidth, fixed values at the start
and end of the pulse.

The idea of choosing a field to steer molecular dynamics, and of formulating it as a variational problem, took
shape in chemistry in the 1980s [@tannor1985control; @tannor1986coherent; @kosloff1989wavepacket]. In the same
period, optimal control theory was applied to selective molecular excitation [@shi1988optimal], and the quantum
optimal-control problem was given a rigorous formulation, including the existence of optimal solutions
[@peirce1988optimal].

## Common figures of merit

**State-to-state transfer.** The probability of reaching the target,

$$F = \big|\langle \psi_{\rm tgt} | \psi(T) \rangle\big|^2 ,$$

or, for mixed states and general targets, the expectation value of an observable,
$\langle O \rangle_T = \mathrm{Tr}\big(O\,\rho(T)\big)$.

**Gates.** For a unitary $U(T)$ on a $d$-dimensional space and a target $U_{\rm tgt}$, two standard choices are

$$F_{\rm sm} = \frac{1}{d^2}\Big|\mathrm{Tr}\big(U_{\rm tgt}^\dagger U(T)\big)\Big|^2 , \qquad
F_{\rm re} = \frac{1}{d}\,\mathrm{Re}\,\mathrm{Tr}\big(U_{\rm tgt}^\dagger U(T)\big).$$

$F_{\rm sm}$ ignores the physically irrelevant global phase; $F_{\rm re}$ fixes it, which makes the landscape
simpler but also stricter. Experiments usually report the **average gate fidelity** — the fidelity averaged over
all input states — which for a unitary error is a simple function of $F_{\rm sm}$ [@nielsen2002fidelity]:

$$F_{\rm avg} = \frac{d\,F_{\rm sm} + 1}{d + 1}.$$

**Gates with leakage.** When the qubits live in a larger space (transmons, atoms, molecules), let $P$ project onto
the $n$-dimensional computational subspace and $M = P\,U_{\rm tgt}^\dagger U(T)\,P$. The average fidelity over the
subspace is [@pedersen2007fidelity]

$$F = \frac{1}{n(n+1)}\Big[\mathrm{Tr}\big(M M^\dagger\big) + \big|\mathrm{Tr}\,M\big|^2\Big],$$

which automatically penalizes population lost from the subspace. See [[drag]] and [[gate-synthesis]].

**Gates in open systems.** Propagating a full basis of Liouville space (all $d^2$ density matrices) is expensive. But
when the target is a unitary, the dynamics of only **three** suitably chosen states suffices to judge it, whatever the
dimension [@goerz2014dissipative].

**Classes of targets.** Often any gate of a class will do — for instance any *perfect entangler*, from which every
two-qubit gate can be built with local operations. Functionals built from the local invariants of a gate target
the whole class at once, which leaves the optimizer more freedom than fixing one specific gate
[@watts2015perfect].

**Other tasks.** Sensing problems optimize the quantum Fisher information ([[quantum-sensing]]), thermodynamic
problems optimize work or power ([[quantum-thermodynamics]]), and robust problems optimize averages or worst cases
over parameter ensembles ([[robust-optimal-control]]).

## Choosing well

- **Match the functional to the experiment.** A gate that maps one basis state correctly but scrambles phases scores
  well on state transfer and badly on gate fidelity. Optimize what will actually be measured.
- **Phase conventions.** Decide whether global, or even local single-qubit, phases matter. Removing unnecessary
  requirements makes the problem easier.
- **Penalties shape the solution.** Energy penalties produce smooth, low-amplitude pulses but bias the optimum. In
  Krotov's method the penalty is placed on the *change* of the pulse between iterations, so it vanishes at
  convergence; see [[krotov]].
- **Final time.** With $T$ fixed, the optimizer maximizes fidelity. With $T$ free, minimizing time at fixed fidelity is
  a different problem with its own structure; see [[geometric-control]] and [[quantum-speed-limits]].
- **The landscape depends on the functional.** Constraints and the form of $J$ change whether local optima appear;
  see [[control-landscapes]].

The necessary conditions that an optimal solution of any such problem must satisfy are given by
[[pmp|Pontryagin's maximum principle]]. Numerical methods such as [[grape|GRAPE]] and [[krotov|Krotov]] are
efficient ways of solving them.

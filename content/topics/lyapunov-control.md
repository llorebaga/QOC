---
updated: 2026-10-11
status: draft
key_papers:
  - key: mirrahimi2005lyapunov
    note: Lyapunov-based trajectory tracking for the Schrödinger equation, with a precise convergence analysis and its connection to controllability.
  - key: wang2010lyapunov
    note: A careful analysis of when Lyapunov control of quantum states converges to the target, and when it stalls.
  - key: magann2022falqon
    note: FALQON. Lyapunov control turned into a quantum algorithm whose circuit parameters are set by measurements, with no classical optimization loop.
  - key: mccaul2020imposters
    note: Tracking control of a correlated many-body system. Laser fields make the current of one Fermi–Hubbard system follow any chosen path, even mimicking another system.
  - key: goldschmidt2022mpc
    note: Model predictive control for quantum state preparation — repeatedly re-optimizing over a short horizon for robustness to model errors.
---

Not every control law has to come from an optimization. **Lyapunov control**, **tracking control** and
**model-predictive control** borrow constructive ideas from classical control engineering. Lyapunov control drives the
system downhill on an "energy-like" function. Tracking control forces an observable to follow a prescribed path by
inverting the equations of motion. Model-predictive control repeatedly re-plans over a short time window. These
methods give interpretable, often iteration-free designs. They have also inspired recent quantum algorithms.

## Lyapunov control

Choose a function $V(\psi) \ge 0$ that is minimal at the target — for example $V = \langle\psi|O|\psi\rangle$ for an
observable $O$ whose lowest eigenstate is the target — and choose the controls so that $V$ can only decrease. For
$H = H_0 + \sum_k u_k(t) H_k$ and $[O, H_0] = 0$,

$$\frac{dV}{dt} = \sum_k u_k(t)\, f_k(t), \qquad f_k(t) = -i\,\langle\psi(t)|[O, H_k]|\psi(t)\rangle ,$$

so the feedback law $u_k(t) = -K_k\, f_k(t)$ with gains $K_k > 0$ gives $\dot V = -\sum_k K_k f_k^2 \le 0$
[@grivopoulos2003lyapunov]. Because measuring the state would disturb it, the "feedback" is computed on a *simulation*.
Lyapunov control is therefore usually a recipe for designing open-loop pulses, with no iterations.

Whether $V$ decreases all the way to the target, or stalls at another invariant set, is the central question. It
depends on spectral and coupling conditions and on the choice of $V$, and it has been analysed in detail
[@mirrahimi2005lyapunov; @kuang2008lyapunov; @wang2010lyapunov]. The same ideas apply to tracking a moving reference
trajectory. When the linearized system is not controllable, adiabatic modifications can restore convergence
[@mirrahimi2005lyapunov]. With real measurements and quantum filtering, Lyapunov methods also stabilize states by
genuine feedback [@mirrahimi2007stabilizing]; see [[feedback-control]].

## Lyapunov control as a quantum algorithm

On a quantum computer, the quantities $f_k(t)$ can be *measured* and used to set the next parameters of a circuit.
**FALQON** (feedback-based quantum algorithm) does exactly this for combinatorial optimization. The circuit is a
discretized Lyapunov-controlled evolution, its layer parameters come from measurements of the previous layers, and the
solution estimate improves monotonically with depth, with no classical optimization loop. It has been demonstrated
on a superconducting processor for MaxCut [@magann2022falqon], and extended in several Lyapunov-inspired variants
[@magann2022lyapunovqaoa]. See [[variational-algorithms]].

## Tracking control

Tracking control prescribes the *trajectory* $y(t)$ of an observable's expectation value and solves for the field that
produces it. From $\frac{d}{dt}\langle O\rangle = -i\langle[O,H_0]\rangle - i\,u(t)\,\langle[O,H_1]\rangle$, setting
$\langle O\rangle(t) = y(t)$ gives

$$u(t) = \frac{\dot y(t) + i\,\langle[O,H_0]\rangle}{-\,i\,\langle[O,H_1]\rangle},$$

computed along the evolution without iterations [@zhu2003tracking]. The catch is the denominator: where it vanishes,
the field becomes singular. Choosing tracks and formulations that avoid singularities is the main design problem, for
example for orienting molecular rotors [@magann2018tracking] and symmetric-top molecules
[@magann2023symmetrictop]; see [[molecules]]. Tracking also works for correlated many-body systems. Laser fields can
make the current of a Fermi–Hubbard system follow an arbitrary predetermined evolution, even making a metal and a Mott
insulator mimic each other's optical response ("driven imposters") [@mccaul2020imposters]. See [[many-body-control]].

## Model-predictive control

**Model-predictive control** (MPC), a standard of industrial process control, solves a short-horizon optimal-control
problem, applies the first part of the solution, updates the model or state estimate with new information, and
repeats. This closed loop is naturally robust to model discrepancies, coherent disturbances and noise. MPC has been
introduced for quantum state preparation, notably for superconducting qubits, whose Hamiltonians are harder to
characterize than those of cold atoms [@goldschmidt2022mpc]. See [[closed-loop]] and [[model-learning]].

## Strengths and limitations

**Strengths**

- Constructive and often iteration-free: one forward simulation gives the control.
- Interpretable, with guarantees (monotonic decrease of $V$, exact tracking where non-singular).
- Natural bridges to quantum algorithms (FALQON) and to feedback with real measurements.

**Limitations**

- Convergence is not guaranteed: Lyapunov control can stall, and tracking fields can become singular or very large.
- Not optimal in time or energy. Results are often refined with [[grape|GRAPE]] or [[krotov|Krotov]].

---
updated: 2026-10-11
status: draft
key_papers:
  - key: khaneja2001timeoptimal
    note: Time-optimal control of coupled spins as a geometric problem on Lie groups — when local controls are fast, the minimal time is set by the coupling alone.
  - key: khaneja2002subriemannian
    note: Time-optimal pulse sequences for three coupled spins from sub-Riemannian geodesics, showing that avoiding decoupling saves time.
  - key: carlini2006brachistochrone
    note: The quantum brachistochrone — a variational principle for the time-optimal Hamiltonian under constraints.
  - key: boscain2005so3
    note: The complete time-optimal synthesis for a spin with bounded control, on the rotation group.
  - key: nielsen2006geometry
    note: Quantum circuit complexity reformulated as geodesic length in a Riemannian geometry on the unitary group.
---

For small systems, optimal controls can often be found **exactly**. Their dynamics lives on a Lie group (unitaries)
or a sphere (states), the optimal-control conditions of [[pmp|Pontryagin's maximum principle]] become geometric
statements, and optimal trajectories turn out to be geodesics of an appropriate metric. **Geometric control**
provides these exact solutions, the minimal times they imply, and the qualitative structures — bang-bang, singular
and geodesic arcs — that numerical methods then rediscover in larger systems.

## Time-optimal control

The most common geometric problem asks for the **shortest time** in which a target can be reached under constraints
on the controls. Two regimes are particularly clean.

**Bounded controls on a single spin or qubit.** With a drift and control amplitudes limited by $u_{\max}$, the
maximum principle shows that optimal controls are concatenations of **bang** arcs ($u = \pm u_{\max}$), possibly
**singular** arcs, and **off** periods. The complete "optimal synthesis" — the optimal control from every initial
point — is known for spins on the rotation group [@boscain2005so3]. Time-optimal single-qubit operations
[@garon2013su2], population transfer in two- and three-level systems [@boscain2002laser] and the minimal time for a
driven two-level system have all been characterized. In the last case, for some initial states the optimal protocol
switches abruptly from bang–off–bang to bang–bang as the bound on the coupling decreases [@hegerfeldt2013qsl].

**Fast local controls, slow couplings.** In many platforms — coupled nuclear spins, superconducting qubits — local
operations on each qubit are fast, while entangling interactions come from a fixed, slower coupling in the drift.
If local operations are effectively instantaneous, the minimal time to build a unitary is set by the coupling alone.
The problem then reduces to a geometric one on a quotient of the unitary group, solved with a Cartan decomposition
(the familiar $U = k_1\,a\,k_2$, local–entangling–local, decomposition of two-qubit gates) [@khaneja2001timeoptimal].
For three coupled spins, time-optimal sequences are geodesics of a **sub-Riemannian** metric, i.e. the shortest
paths when only some directions can be moved in freely. These sequences can be substantially faster than the usual
decoupling-based constructions [@khaneja2002subriemannian].

## The quantum brachistochrone

A complementary viewpoint fixes the *Hamiltonian* rather than the controls: which Hamiltonian, within a set of
allowed ones (for example with bounded energy spread), takes a given initial state to a given final state fastest?
A variational principle analogous to the classical brachistochrone gives an equation for the optimal Hamiltonian
[@carlini2006brachistochrone]. For the simplest constraint, a fixed energy spread, the optimal evolution follows a
geodesic in the space of states. This connects the brachistochrone to the quantum speed limits of free evolution;
see [[quantum-speed-limits]].

## Geometry of quantum computation

The same ideas apply to circuit complexity. Define a Riemannian metric on the unitary group that makes
many-body directions "expensive" and local directions "cheap". The minimal number of gates needed to build a unitary
is then essentially the length of the shortest geodesic to it, which opens Riemannian-geometry tools to the analysis
of quantum algorithms [@nielsen2006geometry]. See [[control-complexity]].

## With dissipation

Relaxation makes time-optimality even more important, since every microsecond costs coherence. It also changes the
structure of solutions. For a dissipative spin-1/2, the time-optimal control contains singular arcs, and the
predicted protocol has been implemented in NMR [@lapert2010singular]; see [[open-system-control]].

## Why it matters

- **Benchmarks for numerics.** Exact minimal times and protocols are reference solutions for numerical methods such
  as [[grape|GRAPE]], and for scanning control times numerically to locate the speed limit [@caneva2009qsl].
- **Structure.** Bang-bang, singular and geodesic segments explain features of numerically optimized pulses, and
  suggest compact [[pulse-parametrization|parametrizations]].
- **Design principles.** Results such as "the minimal gate time is set by the coupling" guide hardware and gate design
  directly; see [[gate-synthesis]] and [[spins]].

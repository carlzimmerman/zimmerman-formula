# All open doors — constructive calculation checkpoint CD26-1

2026-09-26. This campaign follows the user's instruction to swing on all open
doors, building on the preceding [source review](../closure_resume_2026_09_26/README.md).
The [contract](CONTRACT.md) fixes the thirteen requirements and the no-new-dark-
matter-particle direction. The constructions are judged against those equations
and observations; ΛCDM is not assumed as a theoretical premise.

**There is substantive construction progress, but no complete common action yet.**
The strongest surviving pieces are an integrated exact general-source AQUAL
primitive, a uniformly convex lapse-weighted auxiliary problem, a globally
smooth vacuum-regulated gate, a local same-canonical-pair wave transformation,
and a positive-energy causal completion of the gate's dispersive sector.
Their interfaces still matter: they cannot be combined by importing each
piece's passing result into an action that has never been varied.

## What was actually calculated

| Door | Construction or discriminating calculation | Result and precise remaining boundary |
|---|---|---|
| D1 — exact static law, lensing, G | Vary auxiliary weights and both metric potentials; integrate the exponential primitive | General-source exact AQUAL and leading static no slip obtained in the displayed weak-field construction. Two-scalar principal block is healthy for 0<x≤1/2. Global dynamics and full PPN remain open. |
| D2 — constraints and conservation | Generic ADM Legendre transform, nonlinear trace-kinetic factorization, explicit Ward/gate exchange | Identifies genuine degeneracy and terms that cannot be omitted. A full Dirac constraint classification of one completed action is still required. |
| D3 — health, causal response, zero field | Positive kinetic matrix, general rank-one constraint, conserved-source tidal response; weighted heat repair; causal two-field continuation | Regular rank-one family cannot combine exact high-x tangent, healthy scalar and cancellation of its instantaneous tidal term. Auxiliary convexity is repaired at fixed geometry. Causal dispersive continuation has two canonical pairs. |
| D4 — global environmental gate | Smooth exact plateaus with positive vacuum regulator; tensor/trace/lapse/shift variations | Global domain defect repaired. Shear completion gives tensor speed one on isotropic principal backgrounds. Concave correction fixes the scalar k⁴ sign, then needs causal completion and a common-action embedding. |
| D5 — nonlinear particle-free transport | Conservative DBI mass-coordinate evolution, exact Chaplygin benchmark and Fisher wave bridge | Gentle inflow survives the tested period; fast inflow reaches a converged zero Jacobian. Same-pair wave variables work locally, but nodes and large phase gradients obstruct a global clock. |
| D6 — dark-energy origin and normalization | Four-form energy, acceleration coupling and allowed vacuum counterterm | A vacuum scale enters the gate without a new dimensional constant. Neither gate shape nor κ=1/2 is thereby derived. Requirement 13 allows the relation as a declared input. |
| D7 — empirical intersection | Independent replay of both KiDS footings at interior and failed edge cells | Interior p=1,x0=2.5 witness survives; stored edge failure reproduced. This tests the old phenomenological gate, not the newly varied action. |
| D8 — formal evidence | Lean declarations, exact symbolic checks, controls, convergent numerics and source hashes | Components are certified at stated scope. Action variation, full PDE evolution and the complete theory are not replaced by algebra certificates. |

## The reusable constructive results

**Exact exponential static action.** The directly integrated correction

    F(a)=4a0²[1−(1+x)e^(−x)],  x=|a|/a0,
    Lcorr=F(∇Φ)−ζ|∇(U+Φ)|²

gives U=−Φ with declared boundary conditions. After independent metric variation,
the nonrelativistic density is −a0²G(x)/(8πG)−ρbΦ, with
G(x)=x²+2(1+x)e^(−x)−2. Its variation yields the required AQUAL PDE for
nonspherical sources. The radial derivative is retained:
ET=2e^(−x), EL=2(1−x)e^(−x). A two-scalar realization has a bounded healthy
causal principal sector, but its first longitudinal unit-speed boundary is
x≈0.576316 and its lapse Schur pole is x≈0.738421.

Making the kinetic matrix rank one can preserve a healthy scalar at all these
tangents. However, the independently calculated physical tidal response has a
contact coefficient r²(E−ζ)/(2Dr). At EL<0, both ways to cancel it make the
regular scalar gradient energy negative in the tested family. This is an
architectural obstruction, not failure of AQUAL's own static ellipticity.
See [full equations and exact source transfer](response_inertia/REPORT.md).

**Auxiliary existence and uniqueness.** The geometric heat filter does not
contract the action's lapse-weighted gradient norm in general. An exact Fourier
example has initial norm-squared derivative 154π/25>0. A calculation using the
actual exponential kernel also produces a converged negative Hessian example.
The unchanged filter has a sufficient bound Nmax/Nmin<e²+1. Replacing it with
exp(bΔN), ΔN=N⁻¹Di(NDi), b≥0, gives uniform strong convexity at fixed smooth
positive N and fixed metric, including the C¹ zero-gradient join. Coercivity
plus convexity proves a unique weighted-mean-fixed weak minimizer.
This changes the action and requires new lapse vertices; it is not a coupled
physical-time stability proof. See [proof and controls](auxiliary/RESULT.md).
The [actual lapse variation](auxiliary/LAPSE_VARIATION.md) is also derived:
the measure, acceleration and full operator-exponential dependence are retained.
A finite weighted-graph check agrees with independent central differences to
1.85e−10; freezing the heat operator instead misses a nonzero 0.17816 term in
that test. This closes one variational interface, not the full metric/clock
constraint problem.

**Global gate and an explicit causal continuation.** Using positive vacuum
curvature Λ, the C∞ step in 27ΛR/[8xc(K⁴+εΛ²)] is globally defined with exact
off/on plateaus. ε>0 is a declared dimensionless choice; it shifts the threshold.
The varied shear-completed curvature argument preserves the isotropic tensor
cone. Its scalar sector exposes a wrong-sign k⁴ term. A bounded-slope concave
curvature correction supplies a rigorously nonempty sign window, but a bare
positive k⁴ dispersion is not a fundamental causal theory.

The next construction was therefore actually carried out:

    L=½[ż²−|∇z|²+χ̇²−|∇χ|²−m²χ²]+gχż.

It has positive Hamiltonian and a local energy-flux proof of unit-speed finite
propagation. Its light mode has the desired positive k⁴ expansion, with any
0<cs²<1 matchable by positive parameters. It has two independent scalar pairs.
Deleting χ̇² restores an immediate Yukawa acceleration tail.
See the [gate derivation](environment_gate/REPORT.md) and
[causal completion](causal_completion/RESULT.md). Neither calculation silently
adds a dark-matter particle species or certifies a single-clock embedding.

**Nonlinear transport and the wave door.** The bounded-DBI Hamiltonian is
convex. Its conservative finite-amplitude equations still reach zero Jacobian
for tested fast inflow; spatial refinement is approximately second order and
the crossing changes by only 3.67e−7 under time refinement. This is not inferred
from a linear dispersion relation. The exact cold-limit solution also proves
gentle-flow rebound and supercritical crossing.

Adding Fisher gradient energy admits an exact local canonical transformation
Ψ=√ρ exp(iφ/D), without adding a second pair on ρ>0. Regular complex waves
can have nodes where the clock phase is undefined, and node-free nearly
balanced streams have unbounded phase gradients. The free-wave equation also
has unbounded high-frequency group speed. Thus neither a particle ontology
nor a globally healthy clock follows from wave notation. See
[transport](transport/REPORT.md) and the [Fisher bridge](transport/FISHER_BRIDGE.md).

**Dark energy.** A positive vacuum energy is an available physical scale and
can set an activation threshold. In the explicit four-form class, adding an
allowed constant Cv changes gravitational vacuum energy while leaving its
charge equation unchanged. Even with Cv=0, κ²=2β²/(Zq+2bpβ²) remains a free
coupling ratio. This separates vacuum existence, its magnitude, MOND
normalization and the gate mechanism. It does not derive the origin of dark
energy. Requirement 13 permits retaining a0–Λ as a stated phenomenological
relation while the harder dynamical requirements are solved.

## A common-action path rather than pooled passes

There are two explicit branches worth preserving, with different costs:

1. **Strict clock construction:** retain the direct general-source exponential
   primitive, but change the dynamical constraint/source structure beyond the
   regular rank-one trace-mixing family just resolved. The first deciding test
   is its sourced tidal Green function and full constraint class, including
   k=0 and x=0. A healthy unsourced wave alone is not sufficient.
2. **Explicit matter/amplitude completion:** the causal two-field sector gives
   a concrete replacement for a positive k⁴ truncation. Both scalar pairs must
   be classified and counted; introducing them does not prove that the spec's
   permitted clock/matter exception has been met. Its nonlinear covariant
   embedding must reproduce the same exponential static law and one physical
   metric. This is a separate candidate, not a passed relaxation.

The weighted auxiliary repair belongs to the filtered branch; it does not turn
its spherical QUMOND-like relation into the exact AQUAL PDE. The global gate's
weak-coupling sign witness is not the MOND-normalized empirical cell. The
DBI/Fisher clock is not the two-second-order-scalar causal completion. Adding
the positive pieces changes their equations, kinetic matrices, initial data
and parameter windows. No common candidate has passed that assembly step.

After the common constraint/source block passes, derive the same gate's lapse,
clock and metric variations; solve its homogeneous background and perturbations;
then run the retained [empirical interior cell](empirical/RESULT.md) on that
action. The original model replay has Δχ²=−6.078914952 and −0.955628542 on
the two footings, while the boundary counterexample has one Δχ²=4.591406821.
Fresh cosmological growth, lensing and PPN calculations depend on choosing and
varying the common candidate. No observationally fitted action is claimed here.

## Evidence and handoff

- Bounded computation runs and current input/output hashes are enumerated in
  computation_validation.json. Their contracts and commands live beside the
  results. Successful verification means the displayed calculation was
  reproduced, not that every physical hypothesis passed.
- **44 new theorems in four Lean files passed**, with no admitted proofs and
  only the standard axioms propext, Classical.choice and Quot.sound. Logs,
  theorem-level axiom reports and source hashes are collected
  in lean_manifest.json; verify_evidence.py rechecks recorded evidence without
  pretending to rerun Lean or the simulations.
- **Twelve accepted run manifests validated**, covering eleven bounded
  mathematical computation runs and the response certificate's compiler run.
  The other three compiler runs have separate hash-bound evidence records.
- [Independent review](REVIEW.md) records checks and corrections. Failed
  syntax/preflight attempts, timeouts and the corrected determinant prefactor
  remain distinguishable from accepted results.
- Initial repository commit: 03524d209b7ca0c3900f47ccf5dfe42f9187d7c3. Another
  task advanced it through f3b848273 to 763086b23 during this campaign. Inputs
  are pinned individually. No concurrent XC3 result is silently imported as
  a pass; unrelated edits are preserved.
- The canonical specification hash is unchanged. The recipe receives a new
  dated ingredient amendment; no success criterion is weakened.

**Status: constructive checkpoint complete; gravity-theory closure remains open.**
The remaining implications above are stated for continuation. A finite number
of tested families does not exhaust all possible theories.

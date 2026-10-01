# Checkpoint: identify the pressure information that is missing

2026-09-30, 06:24 UTC pass. Parent: [stage eleven](../stage_11/README.md).
The physical objective remains open. This pass concerns a finite pressure
projection model using inherited stored response coefficients; it makes no
new calibrated pressure, force, mass, lensing or gravity-closure measurement.

## Target, rather than full-profile, identifiability

After the additive map offset is fixed, the twelve measured annuli leave
three free pressure coefficients, at the inherited nodes x=2.5,3,4. Write
H=(A,B,h_b), with twelve inner columns in invertible A. With outer vector z,

    p_inner = A^-1(d - h_b b0 - B z)
    gradient = L_inner A^-1(d-h_b b0) + L_b b0 + ell z
    ell = L_outer - L_inner A^-1 B.

The independent calculation uses full exact RREF of [H;offset selector],
not the worker's block inverse. On the stored binary64 matrix treated as
exact rationals, ell is approximately

    (-0.055054273696391466, -0.09447904974858899, -0.11532043480967945).

Exact fractions are retained in the run outputs. These coefficients relate
dimensionless pressure nodes to dp/dx, with p=C Rt Pe and x=r/Rt.
They are conditional on the inherited finite basis, support and response.

For proposed added observation rows W, only their response on the old null
space matters: D=W_outer-W_inner A^-1 B. The target is identified exactly
when ell belongs to the row space of D. A single added row aligned with ell
suffices despite two remaining pressure directions; a different independent
scalar row can fail. Full pressure reconstruction is not necessary.

The criterion is global on the unconstrained affine family. At the inherited
strictly positive, decreasing baseline it is also necessary locally under
those pressure inequalities: sufficiently small perturbations in either null
direction remain admissible. Necessity is not asserted for every feasible
family lying only on an inequality boundary.

## Controls and physical gap

Root's bounded exact computation checks three canonical null columns,
positive and negative added rows, an orthogonal row and a damaged aligned
row. The successful row raises rank from 13 to 14 without further rank increase
when the target is added. A failing row has rank 14 but becomes rank 15 with
the target; two strict monotone witnesses retain its observation and fixed
offset while changing the gradient. The manifest validates execution and
hashes; interpretation also requires the independent audit and coordinator review.

Synthetic rows are design controls, not observations available from a detector.
Actual outer annuli must use the same center, distance convention, pressure
support, beam, mask, pixel weights and background response. Covariance and
calibration remain missing for precision claims. Exact rank alone does not
bound amplification of measurement or response errors.

- [Independent derivation](pressure_audit/DERIVATION.md)
- [Root finite checks](pressure_audit/run_001/results.json)
- [Root computation manifest](pressure_audit/run_001/manifest.json)
- [Independent audit](pressure_audit/INDEPENDENT_AUDIT.md)
- [FGF024 review](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-024_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

No force/source discrepancy calculation is needed for this projection result.
A later bridge must use both a0 normalizations, distinct constant-vacuum and
H(z) branches, and separate Q/RAR/registered M laws, plus total-pressure and
density conversion. The metric/photon coupling and physical scale sector
remain unresolved.

Reconciliation: FGF024 accepted only in the stated finite scope; four bounded manifests validated, corrected preflight failure retained. Queue: 28 tasks, 15 reviewed and 13 ready, none running. FGF028 actual cached outer-annulus response is next; FGF027 quantitative slab gap remains ready. Neither child is launched.

# FGF049 bounded report

The unconditional O(N^-4) upper lifespan of the actual coupled family is NOT
proved. The author proves an exact conditional upper-time theorem with a
weaker, integrated one-sided force requirement and isolates the missing
actual-source estimate. Outcome: supports_scoped_claim (conditional only).
Independent review and orchestrator acceptance are pending.

For the unchanged data and fixed coefficients, put omega=v0 N^4/L. Constants
B_*,eta>0 in DERIVATION.md depend only on the fixed hydrostatic background.
For every fixed Gamma>0 and sufficiently large N, any positive classical
solution through T_N=B_*/omega on the stated physical cone must violate
at least one of

    integral_0^T_N sup|g| dt <= Gamma v0 N,
    integral_0^T_N sup(-g_x)_+ dt <= eta omega.

The first budget proves cone/characteristic containment. The second controls
inverse density and the adverse force contribution to the weighted-gradient
Riccati equation. A future-tail correction is the decisive step: it uses the
actual integral budget without assuming a pointwise bound. Both sound speeds
and pressure are retained; no frozen potential enters the derivation.

The actual derivative source is -Cn_x/tau in BOTH Q modes transported in
opposite directions. It cannot be dropped or canceled at unequal characteristic
positions. Equations (5.2)-(5.7) record the density amplification, the scale
term, and the exact unclosed estimate. FGF048 proves the needed field control
only on its shorter small-kappa interval. Its early small feedback does not
establish either budget over the remaining interval.

The derived continuation proposition is also conditional: bounded state in a
compact positive chart, bounded first derivatives and a buffered contained
domain imply propagation of the C1,1 seminorm and compatible restart for fixed
N. No actual endpoint is classified as a first-gradient singularity, margin
loss, regularity loss or domain exit without those gates. The energy/flux
includes both fields, pressure, the full scale sector and moving endpoints;
zero velocity gives the exact hydrostatic control.

## Author proof audit (not independent)

Primary verdict for the actual-family upper-time claim: **conditional on a
named input**, specifically the two full-interval feedback budgets above.

Dependency graph: exact fluid equations -> weighted identities -> force-budget
cone -> positive-gradient envelope and inverse-density bound -> future-tail
correction -> impossible reciprocal. The actual field equations supply an
exact formula for the missing input, but do not yet supply its bound.
Continuation is a separate implication from explicitly stated state, gradient
and buffer gates, using the pinned local construction.

| Obligation | Status | Evidence |
|---|---|---|
| Exact task and nine ancestry pins | passed | input_sha256.json and metadata verifier |
| Unchanged C1,1 joins, fixed physical coefficients | passed | Sections 1,3,5 |
| Full dynamic source and scale terms | passed | (1.1),(5.1)-(5.7) |
| Weighted identities at C1 regularity | passed | flow-Jacobian derivation, Section 3 |
| Domain containment on comparison horizon | conditional | proved from (F), (2.2) |
| Integrated Riccati obstruction | passed under hypotheses | (4.1)-(4.6) |
| Actual-family full-interval feedback budgets | not established | Section 5; precise gap |
| C1,1 propagation and restart | conditional | Section 6; compact-state/gradient/buffer gates |
| Actual maximal endpoint classification | not addressed as theorem | gates not established |
| Full energy, moving boundaries, hydrostatic control | passed | Section 7 |
| Physical vacuum/metric/DOF completion | out of scope | Section 8 |

Self-audit recomputed the signs of D_+q=-beta, D_-q=-alpha, the source
-g_x h, and u'=w_c'+H_*K_N. It checked units of both feedback integrals,
strict M bootstrap, positivity of u, the finite negative reciprocal at T_N,
the two differing Q transport paths, and the scale contribution in g_x.
No gap was found in the conditional implication; the actual feedback remains
explicitly unproved. No external theorem or numerical evidence is used.

Proofread: DERIVATION.md, FAILED_ESTIMATES.md and this report, in self-review.
Routine edits: notation/sign/units and scope consistency checked.
Mathematical-token changes during proofreading: none.
Unresolved mathematical issue: full-interval coupled feedback, as stated.
Validation: exact input/output hashes and required JSON fields, administrative
only. Zero mathematical computations; no numerical tolerance or seed applies.

Both a_ref normalizations remain separate, as do constant vacuum, frozen H(z),
and evolving-reference protocols. Q, RAR, registered M and filtered MONO remain
distinct. The added diagnostic scale degree of freedom supplies no physical
vacuum, metric/photon/two-DOF, criterion B, calibrated cluster, cosmological,
historical-novelty or theory-closure conclusion.

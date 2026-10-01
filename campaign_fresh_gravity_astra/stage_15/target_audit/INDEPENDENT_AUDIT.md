# Independent audit of the released-support target algebra

2026-09-30. Auditor /root/coupled_dynamics.
Primary verdict: **proved as written**, within the declared saved finite
operator and exact rational interpretation, with the response construction
remaining a separate inherited premise.

This auditor read only the root algebra/checker, its completed bounded result
and manifest, and inherited FGF-028 NPZ target metadata. No FGF-029 worker
derivation/code was read. No nullspace, dual, rank, response, witness or
numerical experiment was independently recomputed. All current root-manifest
input/output hashes were checked, including the candidate NPZ bytes.

## Claim and reconstruction

Let U be invertible 15-by-15, c a released support column, H=[U,c],
theta=(x,s) and target ell=(L,0). The checker establishes invertibility by
exact pivots 0,...,14 in the first fifteen columns. RREF then gives
[Identity,U^(-1)c], so its returned v=(-U^(-1)c,1) spans ker(H).
This is a one-dimensional ambiguity in the saved operator.

Solve U^T r^T=L^T. Then rU=L and every exact observation fiber satisfies
Lx=r d-(r c)s. Thus ell v=-r c. A nonzero result both proves target
nonidentification and makes rank([H;ell])=16. Counting columns alone would
not prove the target is ambiguous; the code correctly checks the nonzero
target response and augmented rank separately.

The target is the old radius-one slope, with coefficients -5,+5 at indices
5,6 and zero at the new node5 coefficient. Inspection of the inherited NPZ
L metadata confirmed that these entries are exactly the stored target
values. The new scalar s is pressure at radius5, not a released map offset.
Reported derivative dt/ds is positive 0.16303084957824435, so r c has the
opposite sign. The plus-minus witness difference is correctly
2 epsilon ell v=-2 epsilon r c.

## Monotone witnesses and endpoints

The rational baseline 10^-5/(1+x_i)^2 is strictly positive and decreasing
over the sixteen free nodes through radius5. The fixed pressure at radius6
is zero. The code forms ALL sixteen successive gaps, including the final
free p5-to-fixedzero6 gap, and likewise sets the null-vector difference
against zero at that fixed endpoint.

For each nonzero gap perturbation delta_i, epsilon is one half the minimum
m_i/|delta_i|. Each signed witness gap is therefore at least m_i/2>0;
zero delta_i leaves its gap unchanged. This proves positive decreasing
profiles all the way to the fixed endpoint. The pointwise nodal inequalities
also enforce monotonicity of the declared continuous piecewise-linear model.
They do not enforce an unknown smooth physical profile outside that model.

Each witness preserves H theta because Hv=0. The code verifies this directly
using exact rationals and checks the signed target difference. The returned
width is a feasible synthetic separation, not a sharp attainable range,
confidence interval or fitted uncertainty.

## Extra-row and control audit

A scalar row (a,b) has null response k=b-a U^(-1)c. On a compatible
observation fiber, k!=0 determines s and thus the target; k=0 leaves this
ambiguity untouched. A measured value inconsistent with the original fiber
would instead make the system infeasible; the stated recovery argument
presumes consistent exact observations.

The direct s coordinate row has k=1 and restores rank16. An existing-row
duplicate has k=0 and leaves rank15. Fixing s=0 restores invertible U and
the old target identification. An external allowed s interval of width
Delta s maps to target width |r c| Delta s before other constraints, as
stated; it is not an inferred statistical error bar.

The wrong-target mutant adds the old sensitivity to the new target
coordinate. Since v_last=1, its null response is twice the nonzero old
response. This differs from the original certificate and is correctly
detected; it is not mistakenly treated as another target-identifying row.
Old columns and new column identity are checked bitwise before rational
conversion. Full transpose solution validates the dual signs.

## Observed bounded evidence and checks

Root run_001 completed with exit0 in 0.146194 seconds. Its manifest records
120-second wall, 110-second CPU, 1 MiB log and cooperative one-library-thread
limits; no memory/affinity cap is claimed. The script contains exact rational
assertions for the stated ranks, null relation, dual relation, monotone
witnesses, target difference and controls; the successful recorded run
supports those finite assertions. This audit inspected implementation and
recorded output, not an independently rerun certificate.

Observed root output: rank H=15, rank with target=16, sensitivity
0.16303084957824435, synthetic witness target difference
1.7565438812803752e-9, relative separation 0.0006991088561092925.
The exact rational values are preserved in the output; these decimals are
display values only.

Root result SHA256:
3e523eb12c247529a59305338c9e167d8e0578caa163e0861d4ae34545ce1fef.
Root checker SHA256:
ae3e8861b8cc5e5302bae5c0d82c2fdfcdf8920ad7f5963415f1bde27f4b92d5.
Root derivation SHA256:
e42c4d0f5ffcd17664758cda71f2975c3ed919e410ba848feb5e4a4e4acecd27.

## Limits and next implication

The mathematical conclusion is exact for the saved finite matrix treated
as rational. This review does not independently establish that c is the
correct sky/instrument response of the radius5 hat; response construction
and calibration require their separate audit. It does not infer continuum
deprojection uniqueness, robustness to response error, full-map equality,
a measured pressure fit or a sharp constrained target interval.

No mass, force or acceleration is calculated. Density, composition,
calibrated response, both a0 normalizations, distinct vacuum/H histories and
the appropriate Q/RAR/registered M law are still required for a physical
source inference. No dynamical, metric, vacuum or full-theory conclusion is
drawn. A useful next question is whether an available independently calibrated
measurement has nonzero k with uncertainty small enough to constrain s;
the direct-coordinate mathematical example does not supply that observation.

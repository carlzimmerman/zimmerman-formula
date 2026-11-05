# Results and next steps — research checkpoint

κ = ½ FITTED; not theory closed

The requested derivation of physical b=1 and κ=1/2 has **not** been obtained. No full nonlinear stable galaxy theory has been established. This checkpoint closes the current reporting work, not the scientific goal. The owner requested a compact handoff and repository push on 2026-11-04; that explicitly authorizes this push despite the original no-push rule. No further research run is required for this handoff.

## Results worth retaining

| Lane | Result on both footings | Checks |
|---|---|---:|
| AZ23 | Exact conditional causal linear kernel PASS; normalization selection FAIL | 20/20 |
| AZ24 | Nonlinear constraint derivation PASS; an AZ23 source solution can leave the one-sided cusp domain | 17/17 |
| AZ25 | Homogeneous attraction PASS for every width; normalization selection FAIL | 20/20 |
| AZ26 | Constraint crossing PASS; signed cosmic completion's gradient stability FAIL for every width | 25/25 |
| AZ27 | Alternative cosmic gradient repair PASS; unrestricted momentum invertibility FAIL at a nonlinear fold | 24/24 |
| AZ28 | Specific fold removed; frozen local all-direction principal stability PASS; global nonlinear stability NO VERDICT | 23/23 |

These are scoped mathematical checks, not observational passes. Each lane has committed pre-run criteria, result, script, machine-readable output, known-answer/MUTATE controls and limited Lean witnesses. Lean does not certify physical κ or global nonlinear stability. AZ24 preserves its failed initial implementation and explains the repair. Later scope restrictions are recorded; historical hashes describe their original runs.

The latest constructive candidate, AZ28, separates expansion and acceleration:

    S = B/2 integral N sqrt(gamma)
        [KijKij−lambda K²+R3−2Lambda+f(g²)−ell² R3²] + S_baryon,
    f(g²)=4A g−4A² ln(1+g/A).

Its momentum map has constant nonzero trace/traceless eigenvalues for lambda>1, eliminating the AZ27 mixed-invariant fold. Its directional lapse Hessian is positive at every finite acceleration; the inherited curvature-squared term supplies a positive k^4 scalar term at zero acceleration. This does not establish global stability. The sourced calculation explicitly shows a changed force response near the stabilizer scale. The older constant-lambda/k^4 construction is credited rather than claimed as new.

The width A remains independent of the vacuum parameter Lambda. Stability admits a continuous set of positive A, lambda>1 and ell²>0. No calculation selects the ratio A/H0 or a physical b=1. A,lambda,ell,Lambda,B and initial/boundary data remain unselected/FITTED if assigned. For all these lanes, physical κ is NOT EVALUABLE. Ranking by completed acceptance rows remains **0/12 requirements and 0 complete RQ3 rows on both footings**; no new observational survivor.

## Next work, in priority order

1. **Curved-background constrained stability of AZ28.** Retain the R3² operator and matter. Derive lapse/shift constraints and physical scalar/tensor symbols on actual sourced backgrounds. Determine the allowed curvature domain; do not infer it from the flat frozen-coefficient calculation. A necessary instability ends this candidate before a costly galaxy run.
2. **Operational source matching.** If the first gate survives, solve one controlled spherical baryonic initial/boundary-value problem with the stabilizer retained. Establish a resolution-independent solution, force/lensing response and the regime in which Newton's coefficient and the deep-force scale can actually be identified. Freeze criteria and controls before outputs; no width scan to obtain a pass.
3. **Normalization only with a new physical principle.** Even success on the first two items does not fix A/H0. Require an independently motivated equation linking the vacuum and source response, plus a second prediction, before reopening an exact κ claim. A target-centered potential, chosen coupling or assumed Lean premise is insufficient.

For a credit-limited continuation, item 1 is the highest-value calculation. Do not repeat the closed signed-cusp stability test, the old k^4 construction, or additional finite Lean witnesses as if they selected κ. No new simulation, observation download or publication is pending from this checkpoint.

## Navigation

- `P3/AZ28_separable_fold_repair/RESULT.md`: latest candidate and force-response limitation.
- `P3/AZ27_stable_cosmic_completion/RESULT.md`: explicit fold and its scope.
- `P3/AZ26_branch_crossing_stability/RESULT.md`: all-width cosmic gradient failure.
- `P3/STATUS.md`: chronological research status and remaining dependencies.
- `SUMMARY.md`: acceptance-row ranking and earlier P1–P6 work.

All evidence was committed locally as the lanes progressed. Unrelated working-tree edits belong to other work and are excluded from this handoff commit. No claim of scientific completion or data preference is made.

## Subsequent cheap test: AZ29

The curved-background priority has now received a necessary tensor test: unrestricted AZ28 stability FAILS, since c_T²=1−2ell²R3 becomes negative on an allowed positive-dust expanding closed-FRW solution. All 19 exact checks pass. See `P3/AZ29_curved_tensor_gate/RESULT.md`. No galaxy simulation was run. The next inexpensive decision is whether a physically justified weak-curvature effective-theory domain can be supplied; only then does a curved scalar test within that domain merit continuation. This high-curvature failure does not itself exclude weak-curvature galaxies, and it does not select κ. This update is a new local checkpoint, not a claim of a second push.

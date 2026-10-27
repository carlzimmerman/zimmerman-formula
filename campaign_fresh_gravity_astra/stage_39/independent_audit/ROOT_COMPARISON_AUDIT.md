# Comparison audit of coordinator momentum reconstruction

Normalized claim: under exact hydrostatic endpoint traces and a positive classical whole solution on a fixed interval, total momentum gives an exact signed transfer relation and a sufficient conditional first-moment obstruction at B_dagger ell/V. Primary verdict for the entire original note: **correct only after a stated restriction**: its sentence “Equality is not sufficient” must be restricted to equality in the asymptotic coefficient condition, not equality at the exact finite-N transfer threshold. The strict sufficient conditional theorem itself is proved as written. This does not prove the actual transfer estimate or, within this short coordinator note, the trace premise.

Target: `campaign_fresh_gravity_astra/stage_39/coordinator/ROOT_MOMENT_CHECK.md`, SHA256 `1e71ee09cf90fd45159ed5f8fc1eaf7803f12b19fbfd4e5af8fe7d19d82e1a52`, checked before read. Exposure occurred after independent derivation SHA256 `377262c0995702b52c0ad38b41552c0dd614061637a96fcd78a544ea991e3a97` and freeze SHA256 `b0f4c2b00d40965437ff3c1c14cf1908a104fda1abffea13f3eb346a4e49836e` were sent to root. The root note itself discloses author-progress exposure; this review makes no third-blind-derivation claim.

Sign dictionary: root K=tau p g+sigma w k, root F=int K/C, root D=-F. Reviewer F=int(-K/C) equals root D. Reviewer D=int(ng-rho g0) equals the time derivative of root D, not root D itself. With that translation all signs agree.

Dependencies: actual field equations -> K_t=S_x-Cng; matter momentum -> conservation of nv-K/C; stationary hydrostatic stress + assumed traces -> P-F=P0 and M fixed; continuity + positivity -> upper first-moment bound; exact polynomial integral -> threshold. No circular edge/core estimate is used.

| Obligation | Status | Evidence |
|---|---|---|
| K_t sign and scale exchange cancellation | passed | W_x=B g_x-T k; scale equation retains +T k |
| Total stress and field momentum sign | passed | subtracting K_t/C cancels -ng |
| Hydrostatic pressure/stress cancellation | passed | S0_x=C rho g0 and c^2 rho_x=-rho g0 |
| Fixed-interval mass and first moment | passed | exact no-flux traces as named premise |
| Signed necessary transfer inequality | passed | J1=J1(0)+P0 t-int D and J1<=bM |
| 16/15 integral and 8/15 normalized momentum | passed | direct integration; smooth varying rho |
| Fixed strict-margin B_dagger threshold | passed | ratio convergence and fixed theta<1 |
| int p=0 and fixed int g | passed | integrate actual Q equation and potential compatibility |
| Actual protected trace proof in this note | conditional | explicit premise, supplied in reviewer/FGF052 derivation |
| Actual transfer budget | conditional | explicitly unproved |
| Zero-velocity control and scope | passed | substitution gives P=F=D=0 |

The int p=0 identity is valid, including its tau factor: tau d_t int p=[B]-CM=0, because mass is conserved and endpoint B equals B0. The fixed int g identity similarly uses actual fixed phi endpoints. Neither turns int p g into the product of means.

One ancillary sentence needs a scope correction, while the stated strict sufficient theorem requires no change: strict positivity actually gives J1<bM, so every surviving branch has int D>P0 t-R0. Therefore equality at the *exact finite-N transfer threshold* also contradicts survival. The note uses the weaker valid non-strict necessary inequality and a strict sufficient inequality. Its unqualified phrase “Equality is not sufficient” is too broad. It is correct only if referring to equality in the *asymptotic coefficient condition* B_dagger>15/[8(1-theta)], since lower-order corrections have not been bounded with the needed sign. It should not be read as denying the strict positivity improvement at the exact finite-N threshold.

Root independently acknowledged the ambiguity after comparing the frozen reviewer proof and undertook a separate preserved correction; this audit does not alter the target. The strongest safe scope is the stated conditional obstruction. Smallest missing implication for an actual-family upper bound is the full-interval signed transfer estimate, with hydrostatic trace proof additionally required if using this coordinator note alone. Read-only review, no literature, no mathematical executable computations, and no modification of the frozen target.

## Preserved correction check

Read and hash-verified `campaign_fresh_gravity_astra/stage_39/coordinator/ROOT_SCOPE_CORRECTION.md`, SHA256 `5c7ddebe287f9986c0fc99bc14ac2f6564bfad1d2f826f9e59159d6520308360`. Its replacement necessary inequality int D>P0 t-R0 follows from int(b-x)n>0. The corrected sufficient inequality int D<=P0 t-R0 therefore includes equality. The separate strict asymptotic coefficient margin remains correctly distinguished. The correction is accepted; the original's substantive strict sufficient theorem and the corrected exact equality scope are proved. This is an after-exposure correction, not a change to an independent freeze.

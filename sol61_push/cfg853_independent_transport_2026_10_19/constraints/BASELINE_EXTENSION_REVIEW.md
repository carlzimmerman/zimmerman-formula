# Independent review of the fixed-baseline virial extension

**Normalized claim.** For the consistently weighted spherical Plummer tracers of the reviewed theorem, let their common radial acceleration be exactly `g=g0+GM_extra(<r)/r^2`, with `g0` fixed independently of a finite nonnegative extra mass measure. If the same global virial and boundary assumptions hold and the weighted baseline integrals exist, subtracting the baseline virial functional leaves the identical positive-mass Plummer kernel. The sharp mass inequality consequently applies to the residual moments.

**Primary verdict: proved as written** for this algebraic extension in the corrected revision below. Its finite-stock interpretation is valid for the declared fixed additive baseline. The astrophysical identification of that baseline, population mass weights and whole-tracer moments remains conditional. No formation, capture, DF-existence or full-action exclusion follows.

## Reviewed revisions

Date: 2026-10-19. Observed review Git HEAD: `e3fc772b519512de59c4b68260df00bc086d590d`. HEAD advanced externally from the original checkpoint base `42b43a572c921d2894ad475a0969a0078c89b286`; the exact artifact hashes identify this review.

| Artifact | SHA256 |
|---|---|
| [BASELINE_EXTENSION.md](/Users/carlzimmerman/new_physics/zimmerman-formula/sol61_push/cfg853_independent_transport_2026_10_19/BASELINE_EXTENSION.md) | `8f4644b2b6d0cc5fad4db7de22b2a9f4820fc7f1948a9cea86b042de220e6514` |
| [VIRIAL_DERIVATION.md](/Users/carlzimmerman/new_physics/zimmerman-formula/sol61_push/cfg853_independent_transport_2026_10_19/VIRIAL_DERIVATION.md) | `d21e561cbf81a94a5334fb465d4bc05a1e43192565deb3a008788d96894031dd` |
| [source_extraction.json](/Users/carlzimmerman/new_physics/zimmerman-formula/sol61_push/cfg853_independent_transport_2026_10_19/source_extraction.json) | `9a6114429005c7436d2e2cd1cf766bdeb7e11f8c2c4f6692d8f4a9d7e1115839` |
| [baseline_run_002/results.json](/Users/carlzimmerman/new_physics/zimmerman-formula/sol61_push/cfg853_independent_transport_2026_10_19/baseline_run_002/results.json) | `aa590131dde42d35a9a15e330d1acb42278bfe633a2d4adaeaca5e08124a81ab` |
| [baseline_run_002/manifest.json](/Users/carlzimmerman/new_physics/zimmerman-formula/sol61_push/cfg853_independent_transport_2026_10_19/baseline_run_002/manifest.json) | `1aa72aa311a9258b053aeb870849945aabd641205e9b1889915265be0f95c76c` |

An initially inspected extension, hash `0727645df3563f32cd310156ef0e6a4f0f156466c4f28abf24d529eec4c04bcc`, described the selected number fraction as a stellar-mass fraction under equal M/L alone. I flagged that missing conversion, the zero-residual cases and the non-monotonicity of the joint bound under baseline changes. The author corrected these issues and added the separate pointwise one-tracer bound. This reviewer changed only this review file.

## Independent reconstruction and dependency graph

The earlier independent review reconstructs the global identity directly from Jeans. For an arbitrary common radial acceleration it is

`S_i = (4 pi/(3L_i)) integral nu_i(r) g(r) r^3 dr`.

Insert the exact additive force decomposition and separate its two integrable terms:

`Delta S_i = S_i-S0_i = (4 pi G/(3L_i)) integral nu_i(r) M_extra(<r) r dr`.

The same Plummer integration and nonnegative interchange therefore give

`3 a_i Delta S_i/G = integral [1+(s/a_i)^2]^(-3/2) dM_extra(s)`.

This directly reduces the extension to the previously audited measure theorem: positive residuals with ratio `R` require `1<=R<h^3` and the stated sharp mass floor; shell equality and its DF caveat carry over. Subtraction does **not** require an equilibrium tracer distribution in the baseline alone. `S0_i` is a linear virial functional, not a separately proved physical equilibrium or formation history.

For the normalized Plummer density, substituting `r=a_i x` gives exactly

`S0_i=a_i integral x^3(1+x^2)^(-5/2)g0(a_i x)dx`.

The factor of `a_i`, angular normalization and powers are correct. For the declared finite-central-density stellar mixture, `gstar` is proportional to `r` near zero, so either deep-regime baseline behaves as `sqrt(r)`; at large radius it behaves as `1/r`. The integral therefore converges at both ends. The baseline's infinite asymptotic effective mass does not invalidate this weighted integral, although it prevents interpreting the gratis baseline as a finite-stock realization.

## Obligations and limiting cases

| Obligation | Result |
|---|---|
| Common, additive, extra-mass-independent baseline | passed as an explicit hypothesis; not derived for the original action |
| Matching density and moment weights | passed as an inherited hypothesis; observed-sample conversion remains conditional |
| Baseline subtraction and dimensionless integral | passed by direct calculation above |
| Negative residual | impossible for nonnegative extra mass |
| One zero residual | positive kernel forces zero extra mass, so the other residual must also vanish |
| Both zero residuals | exactly zero extra mass; no ratio division is allowed or needed |
| Positive residuals | inherited ratio domain, sharp bound and shell equality apply |
| Baseline feedback or nonlinear response to extra mass | out of scope; fixed subtraction would generally be invalid |
| Tracer-dependent extra forces | out of scope; they do not reduce to one common mass measure |
| Collision/capture rate, E/J transport, survival or stationary DF existence | not addressed and not implied |

## Stock accounting and scope of conservative bounds

At one **fixed** baseline, allowing all `5.364 Mstar/f_ret` as extra mass while charging no baseline cost enlarges the inventory allowance. A failure against that allowance cannot be repaired merely by charging the same fixed baseline to the same stock. This is a conservative bookkeeping relaxation, not a construction that realizes the baseline and extra mass from disjoint finite reservoirs. The observed stellar profile, total stellar M/L, assumed mass-mixture weights and retention convention still enter the result.

The joint residual floor is not monotone under arbitrary baseline changes. For example, with `h=2` and observed moment vector `(y1,y2)=(1,4)`, subtracting a growing central-point baseline `(t,t)` increases the residual ratio `(4-t)/(1-t)` toward `8` at `t=4/7`; the joint floor diverges although both residual components decrease. Thus an uncapped baseline is not automatically the most permissive baseline for the joint test. The corrected text states this restriction correctly.

The separate one-tracer ordering is valid: if `g_actual_baseline<=g0` pointwise and all other conditions are held fixed, positivity of the tracer weight implies `S0_actual<=S0`, hence

`M_extra >= 3 a_MP (S_MP-S0_actual_MP)/G >= 3 a_MP (S_MP-S0_MP)/G`.

This is a genuine lower bound across that ordered baseline class. It needs the actual pointwise ordering; it is not a conclusion about arbitrary backreaction.

## Numerical and source dependencies

I inspected the authoritative saved `baseline_run_002` output and its manifest status `completed`; I did not execute or independently validate its quadrature/checker. Its four cases report outer-only floors `5.57–5.70e7 Msun` against the generous cold allowance `2.82175e7 Msun` (ratios `1.974–2.021`). The exact-baseline joint floors are `7.64–9.21e8 Msun`. These are saved conditional numerical inputs to this review, not independent numerical reproductions. The proof above does not rely on their particular values.

The source measurements were independently authenticated in [VIRIAL_REVIEW.md](/Users/carlzimmerman/new_physics/zimmerman-formula/sol61_push/cfg853_independent_transport_2026_10_19/constraints/VIRIAL_REVIEW.md). The corrected `.63/.37` stellar-mass weights are assumptions. Equal M/L alone cannot turn a selected tracer number fraction into a mass fraction: differing mean tracer luminosities or population selection can change that conversion. Geometry, number/light weighting, membership, binary contamination and full-population moment estimation remain unresolved application bridges.

The strongest safe conclusion is the exact fixed-baseline residual theorem and its separate pointwise one-tracer corollary. Applying their numerical violations to Sextans requires the stated observational and force contracts. The cheapest next check is a forward fit of the selected populations using a derived force decomposition and justified stellar-mass weights, not an interpretation of the algebra as a formation mechanism.

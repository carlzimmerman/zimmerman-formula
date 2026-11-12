# Phase 2 inverse route: which independent information actually identifies the acceleration scale?

2026-11-12. Computation-audit workflow; old development templates only. Work stayed in `/private/tmp/euclid_phase2_20261112/inverse/`. No repository files or Git state were changed, no external data were downloaded, and no Euclid or observed gravity-law residual was fitted.

## Outcome

There is a useful exact observable, **S = T/A_gas = a0/gamma_gas**, that cancels distance and the pure velocity-amplitude inclination degeneracy for each galaxy. It avoids the absolute angular-gas prior that helped T in the earlier experiment. However, **none of the three development templates identifies S precisely**: their transition-regime force is stellar dominated, or their gas-dominated regime is deep MOND. More of the same radial coverage cannot supply the missing within-galaxy shape lever.

Independent population information must constrain the relevant **radial modes**, not only a few accurate anchors. Even perfect relative stellar-population constraints do not remove the common amplitude/inclination mode of T. A conditional 0.05-dex T test was possible here only after adding explicit angular-gas and unbiased inclination information; that is not ruler-free precision. The more invariant S remains broad even with dense hypothetical stellar-population constraints.

No new healthy gravity action or observational validation follows. The progress is an exact nuisance decomposition, adversarial inverse tests, and a target-information requirement that is sharper than “obtain better imaging.”

## 1. Scope, geometry and provenance

Requested repository checkpoint: `8db464d4bc256b981d5812c199d6bdff8705b765`. The root reported that the shared checkout had advanced to `cace4617bb6a518bf910b56a4c0ee8bddce7fa07`. This route uses immutable **hashed phase-1 copies** of SPARC Table 1 and the NGC2403, NGC3198 and DDO154 rotation/mass-model tables. It does not assume the moving checkout equals either checkpoint. Source/copy paths and hashes are recorded in `selection.json`; no repository execution code is imported.

The inputs supply the actual radial sampling, tabulated disk/gas force templates, surface brightness, inclinations and velocity errors. The experiment generates new **noiseless synthetic mean velocities** from these templates; measured velocities are used only for availability and quoted fractional-error information. This is a development-design calculation, not a fit of the actual rotation curves.

The selected law is the pointwise simple-mu prescription

\[
g_b=g^2/(g+a_0).
\]

The disk source is propagated through the same softened Newtonian ring geometry as phase 1, calibrated to the published disk force. Its scale height is h = 0.1 R_d. Gas and stellar templates are separate, and the signed gas-force convention is retained. This is **not** an AQUAL disk solution, a full three-dimensional reconstruction or a model of inclination-dependent light/gas deprojection. Those omissions constrain every interpretation below.

## 2. The exact mode structure

Write w = v_c squared / theta, T = D_A a0, A_star = D_A U and A_gas = D_A gamma_gas, where U and gamma_gas multiply known reference stellar and gas force templates. A_gas is an **angular** coefficient. Knowing gas conversion alone does not fix it if D_A is unknown.

For a fixed source geometry the algebraic model is homogeneous:

\[
(A_\star,A_g,T)\mapsto\lambda(A_\star,A_g,T)
\quad\Longrightarrow\quad w\mapsto\lambda w.
\]

Changing sin i to sin i divided by sqrt(lambda) then leaves the line-of-sight velocity curve unchanged. Relative stellar-population information, baryon positivity and relative radial M/L gradients are invariant under this transformation. They cannot remove this mode, even at infinite signal-to-noise.

An independently measured inclination can anchor it, but an accurate-looking biased inclination prior can instead produce a biased T. A measured absolute angular baryon coefficient can also constrain it; that requires an actual distance-times-conversion constraint and is not the same as a measured conversion factor. In a gas-dominated deep regime an additional product degeneracy survives, so fixing one component is not a universal remedy.

### The gas quotient avoids that mode

The root agent identified the particularly useful invariant:

\[
\boxed{S\equiv T/A_g=a_0/\gamma_g}.
\]

It is unchanged under **each galaxy’s** amplitude/inclination mode. In the restricted velocity-only projection model, one may fix i as a **gauge**, while leaving all global source amplitudes free, and profile S without an inclination prior. This does not establish that the real deprojected gas and light geometry is inclination independent.

If the gas reference shape is correct and gamma_g has a common calibration across redshift, then

\[
\frac{S(z)}{S(z_r)}=\frac{a_0(z)}{a_0(z_r)}
\]

without an absolute distance, sound horizon or global M/L calibration. For unequal conversion factors the right-hand side is multiplied by gamma_g(z_r)/gamma_g(z); their **relative** calibration remains necessary. The density, pressure and potential portal shape tests from phase 1 could use these ratios if S were actually measurable. No rho_DE history was imposed in these inverse fits.

This is not a new unique MOND prediction. It is a way to use transition shape. The gas-calibration convention also differs from a deep BTFR amplitude inference: fixed-distance/inclination gas-dominated BTFR measures a0 times gamma_g and gives inferred a0 proportional to 1/gamma_g. The shape quotient measures a0/gamma_g, so a0 = gamma_g S. There is no contradiction: **deep BTFR does not identify S**.

Tying multiple A_g values through BAO distance ratios and one free common ruler would collapse separate scale modes to one common mode; relative T values can then be invariant. That derivation is correct, but the per-galaxy S quotient is simpler and was prioritized. No shared-ruler mock was needed. Neither construction automatically measures absolute kappa.

## 3. Adversarial truth profiles and independent-information brackets

The first block used three non-power-law positive M/L profiles: a smooth bend, a localized bump near 2 R_d and a smooth broken-gradient profile. They were not members of the single-power inverse family. The flexible inverse used three relative M/L knots. Every profile was normalized at R_d; a global stellar normalization remained free.

Hypothetical independent population observations constrained relative M/L at 0.3, 3 and 10 R_d, with explicitly declared precision brackets of 0.10, 0.05 and 0.02 dex or no constraint. They are assumptions about **total stellar M/L including any IMF variation**, not a claim that Euclid colours supply them. Inclination truth was either at the catalogue value or 3 degrees above it, while the prior remained centred on the catalogue value.

Results from the sparse three-knot inverse illustrate the failure of accurate point anchors:

| Galaxy | Worst absolute log10 T bias across three truth profiles, population contrast sigma = 0.02 dex | Bump-profile nominal Delta-objective <= 1 interval |
|---|---:|---|
| NGC2403 | 0.0419 dex | approximately [-0.125, +0.025] dex |
| NGC3198 | 0.1564 dex | extends below the -0.30-dex grid edge |
| DDO154 | 0.0171 dex | spans essentially the full [-0.30, +0.30] grid |

A small best-fit bias, particularly for DDO154, is not identification. Intervals touching a grid edge are truncated, not reported as complete intervals. These are penalized-profile sensitivity statistics on synthetic means; Delta objective = 1 is a nominal diagnostic, not calibrated coverage.

## 4. Dense radial coverage and the price of precise T

A separately frozen continuation changed **both** inverse flexibility and population-mode coverage: ten population nodes spanning 0.1–40 R_d and nine free relative M/L coefficients. Smooth truth curves still differ from the piecewise-linear inverse. Raw node errors were declared independent; after subtracting the R_d anchor their covariance is sigma squared times (I + ones). This explicitly accounts for the shared reference error.

Population-node errors were bracketed at 0.05 and 0.02 dex; inclination-prior widths at 3 and 0.5 degrees. An optional independent prior constrained log10 A_g to 0 +/- 0.03 dex. That last constraint requires an angular mass scale, combining geometric distance and gas conversion or equivalent independent information. It **reintroduces absolute scale information** and must not be sold as a ruler-free result.

With no A_g prior, dense population information reduced the finite-family MAP bias but left T broad. Tightening only inclination did little. With unbiased 0.5-degree inclination information **and** 0.03-dex A_g information, all three templates and all three injected profiles placed both T_true +/- 0.05 dex beyond the nominal Delta-objective = 1 line:

| Galaxy | Population-node error 0.05 dex: maximum absolute T bias | Minimum Delta objective at T_true +/- 0.05 dex |
|---|---:|---:|
| NGC2403 | 0.00183 dex | 2.105 |
| NGC3198 | 0.00108 dex | 2.302 |
| DDO154 | 0.00017 dex | 1.796 |

This is **conditional finite-family feasibility**, not a general precision guarantee. Sparse versus dense blocks changed flexibility and calibration coverage together; their difference does not isolate one causal factor. No actual stellar-population or angular-gas measurement with these precisions was supplied.

Precision does not protect against bias. If the inclination prior is 3 degrees below the truth, the dense, tightly constrained model can retain tiny velocity residuals while T is biased by approximately **0.024–0.045 dex**. The quoted half-degree prior has become confidently wrong. All these models still hold the source geometry fixed rather than recomputing its inclination dependence.

## 5. Direct S profiles: invariant does not mean well measured

A third frozen block removed all absolute A_g and inclination priors. It fixed inclination only as a gauge of the exact velocity-amplitude symmetry, and directly profiled

\[
\log S=\log T-\log A_g.
\]

The analytic Jacobian includes the required chain: varying log A_g at fixed S changes both the gas coefficient and T. An explicit nonzero scale/inclination transformation leaves the predicted velocities and S invariant to numerical tolerance. Population calibration remains hypothetical and uses the dense correlated-node model above.

With population-node error 0.02 dex, the bump-profile nominal Delta-objective <= 1 intervals are:

| Galaxy | log10 S interval on the declared grid | Status |
|---|---|---|
| NGC2403 | [-0.175, +0.125] dex | completed profile; much wider than 0.05 dex |
| NGC3198 | [-0.300, +0.300] dex | completed profile; much wider than 0.05 dex |
| DDO154 | entire [-0.500, +0.500] dex grid | calibrated-node cases converged; interval truncated |

Across the three alternative truth profiles the smallest Delta objective at S_true +/- 0.05 dex is only 0.0225, 0.0154 and 0.00352 respectively. There is no demonstrated 0.05-dex S measurement in this data design. This remains true even though MAP biases with dense calibration are small.

**DDO154 numerical limit:** its unregularized flexible quotient fits and some profile points reached the 500-evaluation cap. That bounded run is retained as **failed**, not silently promoted to success. Its 0.05- and 0.02-dex population-constrained cases converged and remain broad; the unregularized result is numerically inconclusive. Some completely uncalibrated flexible fits also reach parameter bounds, which restricts their interpretation. No further optimizer expansion is needed to conclude that these data do not establish precise S.

## 6. The missing target information is identifiable before looking at a law residual

For the simple-mu law let

\[
t_i=\frac{\partial\log w_i}{\partial\log T}
=\frac{a_0}{g_i+2a_0},\quad
f_{g,i}=g_{g,i}/g_{b,i}.
\]

In quotient coordinates the velocity-amplitude and stellar/gas-contrast nuisance span is

\[
N_i=\{1,\ (1-t_i)(1-f_{g,i})\}.
\]

The local information in log S, before adding radial M/L uncertainties, is the weighted norm of t after projection out of that span:

\[
\boxed{I_{\log S}=\|W^{1/2}(t-P_Nt)\|^2}.
\]

The calculation uses the quoted catalogue fractional velocity-error model. It is a transparent design diagnostic, not a nonlinear observational forecast.

Before counting, the final small contract specified illustrative thresholds f_g > 0.5 and 0.3 < g_b/a0 < 3. The actual existing templates give:

| Galaxy | Valid radii | Gas-force-dominated radii | Transition radii | Both at once | Ideal exact-shape sigma(log10 S) |
|---|---:|---:|---:|---:|---:|
| NGC2403 | 73 | 20 | 42 | **0** | 0.0768 dex |
| NGC3198 | 43 | 3 | 25 | **0** | 0.2533 dex |
| DDO154 | 12 | 10 | 0 | **0** | 0.7221 dex |

At transition radii, maximum gas-force fractions are only 0.163 and 0.064 in the two spirals. Their gas-dominated radii lie below g_b/a0 = 0.126 and 0.038. DDO154 is gas dominated but entirely deep. Its t varies only about 0.438–0.469, close to the constant deep-limit value 1/2, which is absorbed by amplitude.

Thus **the useful next target class is a resolved gas-force-dominated transition over a radial range**, with independently constrained gas conversion and three-dimensional geometry. The numerical thresholds are illustrative, not a theorem that all other systems fail. The invariant local criterion is nonzero target response after nuisance projection; adequate curvature must survive radial-population, pressure and external-field profiling. More observations that remain only stellar dominated at transition or only gas dominated deep do not create that within-galaxy lever.

For orientation, the adopted ideal linear error model would require I_logS greater than approximately 75.4 for a 0.05-dex one-standard-error target. Existing ideal values are 31.95, 2.94 and 0.362 **before** additional profile uncertainty. This is a requirement calculation, not a promise that these errors scale simply with more galaxies or observing time.

## 7. Mathematical limits and what to measure next

Arbitrary radial M/L and gas profiles remain a structural obstruction. Finite population anchors alone do not bound the function between anchors unless regularity or a physically justified profile class is supplied. The experiments establish finite-family adversarial sensitivity, not minimax control over all positive source functions. Baryon positivity alone cannot remove the exact common-amplitude mode: multiplying all positive source coefficients by a positive lambda preserves positivity.

The next external evidence must supply the missing mode rather than a generic “more data” increment:

1. Independent **relative gas-conversion and gas-shape** information over a gas-dominated transition; global calibration cancels in a redshift ratio only if it is genuinely common.
2. A constrained gas/light deprojection, radial pressure correction and inclination/warp model from actual two-dimensional data. The velocity-only gauge argument does not remove those physical geometry errors.
3. Radial stellar-population/IMF information that constrains the source modes where stars still matter; colours alone are not declared an IMF-gradient measurement.
4. A declared nonspherical gravity equation and forward solver before turning the surrogate-disk result into a gravity test.

The positive result is an invariant quotient and a measurable target-information condition. The negative result is that the present three templates lack sufficient quotient information. This is the substantive checkpoint; another round of fits in the same surrogate geometry would not establish the required observations or a healthy completion.

## 8. Reproduction and audit status

- `selection.json`, `contract.json`, `experiment.py`: sparse-anchor adversarial block, 144 full cases across three separate bounded runs.
- `selection_dense.json`, `contract_dense.json`, `experiment_dense.py`: dense-mode/independent-scale continuation, 144 full cases.
- `selection_quotient.json`, `contract_quotient.json`, `experiment_quotient.py`: direct invariant quotient, 54 full cases. Before launch, an input-preparation syntax error was corrected; no fit or science outcome was produced by that failed preparation command.
- `contract_target_design.json`, `target_design.py`: illustrative target counts and nuisance-projected local response.
- Every run directory contains its input/output hashes, manifest, stdout/stderr and structured results. `manifest_validation.json` records successful manifest validation for all ten evidence records: **nine completed, one failed** (unregularized DDO154 quotient cap as described above). A valid manifest is provenance, not mathematical or astronomical validation.
- Profiles use original velocity space with analytic derivatives. First-block Jacobians and the quotient chain were checked against finite differences; full-fit multi-start spreads and boundary status are recorded. The fixed-source, one-kernel, softened geometry and incomplete covariance remain physical limitations.
- All source/result manifests are preserved. No failed case was removed, and no observed law residual, kappa value or rho_DE linkage was used to tune a truth profile.

## Provenance erratum from independent review

The quotient contract retained `max_nfev = 400` from the earlier block, while `experiment_quotient.py` actually uses **500**. The quotient results, including DDO154’s nonconvergence, therefore describe the actual 500-evaluation limit. This is a disclosed contract/implementation deviation; it does not establish a result for the originally written 400-evaluation bound. The historical script, contract, selection and manifests are preserved rather than rewritten. Completed process status does not certify compliance with every field of the original contract.

Some inherited input prose says `selection.json`; the dense and quotient programs actually read the separately hashed `selection_dense.json` and `selection_quotient.json`. Likewise, inherited `external_constraints` prose mentions the earlier sparse three-anchor locations. For the dense and quotient blocks the actual structured node list and code use **[0.1, 0.3, 0.6, 1, 1.5, 2, 3, 6, 15, 40] R_d**, with R_d as the reference: nine relative contrasts. Dense raw-node sigma values are **0.05 and 0.02 dex**; the quotient additionally includes the no-population-information case. Their contrast covariance is **(sigma ln 10)^2 (I_9 + 1 1^T)** in natural-log units. These are the executed assumptions reported above; the sparse block separately used independent contrast-error brackets. The report does not treat the stale inherited prose as an additional measurement or as the executed calibration model.

No pinned dense/quotient input bytes were edited to correct this metadata. `live_hash_audit.json` explicitly compares all 58 manifest input references against their recorded before/after SHA-256 values: **every live input matches both hashes**. The corrections are confined to this report, the finite summary and new audit files.

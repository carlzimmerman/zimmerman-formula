# CCT020 results

The tested pre-stellar history has not produced the required settled Draco core and Sextans envelope. No dynamics-selected stellar cohort was born in the completed coarse histories. The later coarse phase limits are numerical obstructions, not evidence that the actual field can never settle. Finer runs are assessed only over their measured overlap.

## Later original collapse

| Galaxy | Last evaluated settling window ends at T | CDF range / total mass (limit .01) | Reference-sphere mass relative range (limit .05) | Cold r50 relative range (limit .05) | Terminal reason |
|---|---:|---:|---:|---:|---|
| Draco | 2.80 | .365797 | .179524 | .927788 | Phase occupancy .050245 > .05 at T2.808244 |
| Sextans | 3.00 | .304338 | .192710 | .714571 | Phase occupancy .051135 > .05 at T3.043654 |

Mass and energy conservation remained within their registered limits; that alone did not establish spatial accuracy or settling. The exact failed terminal states are saved and ineligible for restart. The earlier valid Draco T2.5 transfer to twice the mesh failed its unrenormalized mass/energy-transfer screen: relative mass defect .00106139 versus1e-8 and energy defect .000320848 versus1e-4. The transfer was rejected. This is a discrete representation failure, not measured physical mass loss or a proof that every refinement strategy fails.

At the latest valid saved coarse snapshots, Draco T2.5 has 1.4100e8 Msun inside the observed193.22pc reference sphere and projected canonical beta0 LOS support32.06km/s, compared with selected-data constant dispersion9.70km/s. Sextans T3.0 has1.2672e8 Msun inside485.89pc and component support18.67–19.41km/s, compared with8.80km/s. Neither is settled. These are full-profile instantaneous equilibrium-moment diagnostics, not evolved stellar velocities or a formal likelihood. Draco's corresponding held-out PM diagonal squared residual is5349–6577 across the stated beta/radius conventions, also not a covariance-aware likelihood or significance.

## A shared higher-infall-energy trial does not solve the controls

The separate posthoc trial vin/V=.8 is applied to all four dwarfs, with unchanged eta, supply fraction and initial density. At the fixed common T=.5, canonical beta0 projection gives:

| Galaxy | Full-profile projected LOS sigma (km/s) | Selected-data constant sigma (km/s) |
|---|---:|---:|
| Draco |15.69|9.70|
| Sextans components |14.63–16.62|8.80|
| Fornax |36.17|12.14|
| Leo I |22.66|9.03|

Sextans' range is not an invented chemical-population mixture or a joint data fit. The full JSON includes both beta choices and both acceleration footings. This common energy choice has no successful four-dwarf outcome: its evaluated profiles are too concentrated, and none establishes a settled, star-safe configuration. All four energy-trial producers stop for their explicit wall budget before an eligible T>=2 settling evaluation; this is missing later coverage, not a completed late-time exclusion.

## Energy and wave support

For the stationary complete smooth Plummer candidates, canonical beta0 dimensionless E_target−E_initial is −.067574 (Draco), +.116102 (Sextans), +.228260 (Fornax), +.072090 (Leo I). Positive gaps obstruct pure nonnegative-energy export to those exact stationary candidates under the stated isolated fixed-source assumptions. The hypothetical full reservoir mass and unseen outskirts are conditional inputs.

The frozen energy contract's phrase 'time-averaged' was too broad. ENERGY_SCOPE_CORRECTION.md preserves and corrects it: negative density-fluctuation binding must be included. In the original valid base segments, the saved-snapshot covariance term is −.692842 (Draco) and −.458398 (Sextans). These are significant finite sampled terms, but the corresponding averaged virial residuals are +1.247940 and +1.024693; the sampled mean profiles are not the fitted stationary targets. The identity residuals are below2.1e-15 for the currently analyzed records. Sparse snapshot quadrature is not a converged continuous-time average, and records containing invalid terminal states are explicitly flagged.

A regular single smooth positive zero-flux stationary wave also supplies too little amplitude-gradient support for these profiles. Nodal excited modes, multiple frequencies or nonspherical support are distinct hypotheses, not automatically excluded. They need actual formation and quiet stellar-force evidence.

## What is not tested successfully

No qualifying birth means no stellar-survival pass. The fixed pre-stellar baryon source is an externally supported gas proxy, not gas dynamics or a star-formation model. No cosmological collapse-start epoch is specified, so simulated Myr elapsed cannot establish that the real systems settled before their oldest stars. Spin is zero by symmetry. Finite-box energy inventories are not escaping-wave flux at infinity. No parent-action bridge is derived and no result transfers to Claude's other models.

Requested T8 is never substituted for attained coverage.


## Final fine coverage and reproducible outputs

| Run | Attained T | Elapsed Myr | Stop | Stellar birth |
|---|---:|---:|---|---|
| Draco_base | 2.184354 | 209.82 | wall stop | none |
| Draco_base_P9 | 1.294852 | 124.38 | wall stop | none |
| Draco_base_continued | 2.808244 | 269.75 | spatial/invariant/boundary stop | none |
| Draco_energetic_base | 1.692495 | 162.57 | wall stop | none |
| Draco_fine | 1.732327 | 166.40 | wall stop | none |
| Fornax_energetic_base | 0.813804 | 188.07 | wall stop | none |
| LeoI_energetic_base | 1.060308 | 160.58 | wall stop | none |
| Sextans_base | 2.075109 | 192.57 | wall stop | none |
| Sextans_base_continued | 3.043654 | 282.46 | spatial/invariant/boundary stop | none |
| Sextans_energetic_base | 1.848360 | 171.53 | wall stop | none |
| Sextans_fine | 0.771612 | 71.61 | wall stop | none |
| Sextans_fine_continued | 1.722400 | 159.84 | wall stop | none |

The finer original Draco run reaches T1.732327; the resumed finer Sextans run reaches T1.722400. Both preserve their gates and stop for the explicit wall budget. Neither reaches the T>=2 settling eligibility. They therefore do **not** resolve the later coarse collapse. At the last common saved T1.5, coarse/fine CDF sup differences are .00107932 (Draco) and .000576906 (Sextans); unrotated physical-wave L2 differences .0136313 and .00728128, and separately phase-aligned differences .0115955 and .00692053. These are finite paired mesh/tolerance comparisons, not a convergence-order certificate.

`analysis_002/result.json` analyzes all12 field producers:208 profile rows,92 held-out PM rows and33 explicitly labeled matching-time comparisons. Its measured peak RSS is 93110272 bytes. Maximum field-producer RSS is 116015104 bytes; one numerical thread per producer. `analysis_001` is the earlier ten-producer snapshot and remains sealed, rather than overwritten.

Eligible prepared next segments (manual, not launched):

```bash
/opt/homebrew/bin/python3 sol61_push/cold_pre_stellar_settling_2026_10_25/run_continue.py Draco_fine_next
/opt/homebrew/bin/python3 sol61_push/cold_pre_stellar_settling_2026_10_25/run_continue.py Sextans_fine_next
```

These continue accepted fine wall checkpoints from the exact fields and original invariants. They do not bypass the failed coarse or transfer endpoints.

Final `audit_001/result.json`: **806 integrity/operator/control checks, zero failures**, including12 passing unit controls across four modules. Known physical gate failures remain failures. The separate degree8 control failure and `prolong_001` execution failure are retained explicitly. All19 computation manifests validate, including the honestly labeled failed execution record; see `VALIDATION.json`. The audit measured71,254,016bytes peak RSS (largest child49,905,664bytes).

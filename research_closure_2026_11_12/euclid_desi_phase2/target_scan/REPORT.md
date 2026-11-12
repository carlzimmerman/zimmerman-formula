# Full SPARC baseline target-information scan

2026-11-12. This is a bounded design scan of familiar local development data, not a held-out prediction, an observed fit or a survey forecast. The contract and selection were saved before computing the full-sample outcomes. No gravity-law residual was evaluated, no quality flag was used to select agreement, and no repository file or Git state was changed.

## Result

**None of the 175 local SPARC templates has even one valid radius simultaneously satisfying the frozen illustrative conditions gas-force fraction > 0.5 and 0.3 < g_b/a0 < 3.** Consequently none meets the additional radial-variation criterion. No template reaches the declared ideal single-galaxy 0.05-dex quotient-information threshold under the adopted fractional-error model.

NGC2403, used in the earlier inverse experiments, is actually the highest-information template in this full scan. Its failure to give precise gas quotient information was therefore not cured by simply choosing another template under this fixed baseline.

These statements depend on the chosen source normalization and law. They are **not** a theorem that gas domination is necessary for identification, that no galaxy can supply the measurement, or that an ensemble has no information. The cuts are an illustrative diagnostic; the nuisance-projected response is the local information quantity.

## Frozen footing and calculation

The scan used canonical a0 = 9.3603e-11 m/s squared, disk M/L = 0.5, bulge M/L = 0.7, and sign(V_gas) times V_gas squared for the gas force. Disk and bulge amplitudes are treated as separate nuisance directions whenever a nonzero bulge is present. Gas/helium/molecular conventions are inherited from the tabulated SPARC gas template; no new molecular component, correction or external gas-conversion calibration was supplied. The fixed stellar normalizations define a design footing, not measured M/L values for all galaxies.

All 175 `*_rotmod.dat` files were copied and hashed, together with SPARC Table 1. Each row required finite first six columns, R > 0, V_obs > 0, error(V) > 0 and positive summed baryonic source. Catalogue inclination and quality Q are reported **descriptively only**. No cuts based on Q, inclination or fit agreement were introduced afterward.

For the pointwise simple-mu law, write

\[
t_i=\frac{a_0}{g_i+2a_0},\quad
f_{d,i}=g_{d,i}/g_{b,i},\quad f_{b,i}=g_{\rm bulge,i}/g_{b,i}.
\]

The target response for log S, S = T/A_gas = a0/gamma_gas, is t. Project it against the nuisance columns

\[
N=\{1,(1-t)f_d,(1-t)f_b\},
\]

omitting the last column only if the bulge is identically zero. Adopt catalogue fractional log-w errors 2 error(V)/V_obs and compute

\[
I_{\log S}=\|W^{1/2}(t-P_Nt)\|^2,
\qquad \sigma_{\log_{10}S}^{\rm ideal}
=\frac{1}{\ln10\sqrt{I_{\log S}}}.
\]

This is a known-template, local linear information diagnostic with a prescribed fractional-error model. It does not include radial M/L uncertainty, template covariance, pressure corrections, warps, external fields or PSF correlations. It is not a measured error on S.

The illustrative coverage criterion required at least three overlapping radii, a log10 radial span >= 0.3 and target-response span >= 0.05 within the gas-dominated transition set. The ideal 0.05-dex one-standard-error information marker is I >= 1/(ln10 times 0.05) squared, approximately 75.4. Neither marker is a calibrated detection or rejection rule.

The quotient homogeneity argument can apply to other homogeneous gravity prescriptions, but **t and the numerical information are law specific**. A healthy candidate with a different interpolation function must be rescored; these numbers are not transferred to it as a pass.

## Complete denominator and exclusions

| Item | Count |
|---|---:|
| Input rotation/mass-model files | 175 |
| Galaxies scored | 175 |
| Galaxy parse/eligibility exclusions | 0 |
| Matching catalogue metadata records | 175 |
| Raw radial rows | 3,391 |
| Rows used | 3,389 |
| Galaxies with any illustrative overlap | 0 |
| Galaxies meeting radial-variation criterion | 0 |
| Galaxies above ideal 0.05-dex information marker | 0 |

The only two row exclusions are in **UGC01281**: 2 of its 25 tabulated radii have nonpositive total baryonic source under the declared signed-gas footing. The remaining 23 radii are scored. No galaxy was removed. Per-galaxy raw/used/excluded counts remain in the JSON.

## Information ranking, without residual fitting

The highest ten ideal-information values are shown below. Q and inclination are included to expose source quality; they did not alter the ranking or denominator.

| Galaxy | Ideal I | Ideal sigma(log10 S), dex | Catalogue i +/- error | Q | Separate bulge nuisance |
|---|---:|---:|---:|---:|---|
| NGC2403 | 31.95 | 0.0768 | 63 +/- 3 deg | 1 | no |
| UGC09133 | 14.35 | 0.1147 | 53 +/- 6 deg | 1 | yes |
| UGC06787 | 6.87 | 0.1657 | 66 +/- 3 deg | 2 | yes |
| NGC5055 | 6.24 | 0.1739 | 55 +/- 6 deg | 1 | no |
| NGC6503 | 5.58 | 0.1838 | 74 +/- 2 deg | 1 | no |
| UGC02953 | 3.96 | 0.2183 | 50 +/- 4 deg | 2 | yes |
| NGC2903 | 3.22 | 0.2420 | 66 +/- 3 deg | 1 | no |
| UGC02916 | 3.22 | 0.2422 | 50 +/- 5 deg | 2 | yes |
| NGC5033 | 3.16 | 0.2443 | 66 +/- 1 deg | 1 | yes |
| NGC2841 | 2.98 | 0.2517 | 76 +/- 10 deg | 1 | yes |

All 175 rankings, including low-quality systems and very weak or zero projected information, are preserved in `run01/results.json` and `run01/ranked.csv`. The table is not a follow-up recommendation by itself: gas morphology, conversion, pressure and two-dimensional geometry still have to be established independently.

## What this adds

The earlier three-template inverse result points to a broader **baseline sample-coverage gap**: local gas-dominated radii and transition radii do not overlap under the frozen source model. A more useful development target should show resolved gas-force-dominated transition curvature, or otherwise supply large quotient response after all nuisance directions are projected out. Imaging that only improves an already stellar-dominated transition does not by itself supply the gas calibration lever.

This is a target-design requirement for the density/pressure/potential redshift tests, not a new unique MOND prediction or a claim that those tests have passed. Common gas calibration can cancel in a ratio only if it is actually common; unknown redshift-dependent conversion or deprojection can still imitate scale evolution. Ensemble inference could accumulate statistical information under independently justified common calibration and population assumptions; this scan does not evaluate or exclude it.

## Artifacts and reproducibility

- `selection.json` and `contract.json`: thresholds, row rules, nuisance projection, ranking, fixed source footing and non-claims.
- `scan.py`: deterministic scan, with no residual/agreement calculation.
- `inputs/`: 175 copied rotation templates plus the catalogue; original paths and SHA-256 values in `input_hashes.json`.
- `run01/results.json`, `run01/ranked.csv`: complete outputs and exclusions.
- `run01/manifest.json`: **completed** bounded run, with installed manifest validator passing.
- `live_hash_audit.json`: all **178** manifest input references match their recorded before/after hashes and current file bytes. No pinned input was edited after the run.

The absolute source paths were the existing repository data files. This report does not claim a fresh literature or gas-calibration audit. The substantive next step needs a candidate with different physical coverage and independent gas/geometry information, rather than additional nested fits to the same inadequate radial modes.

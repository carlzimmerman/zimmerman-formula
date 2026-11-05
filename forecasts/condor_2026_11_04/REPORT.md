# CONDOR pre-release discrimination screen

Calculated 2026-11-04, before the listed high-resolution CO releases. **No upcoming target is established here as a decisive discriminator between PAPER66's fixed F-DESI model, constant-scale MOND, and dark matter.** This is conditional evidence of degeneracy, not proof that discrimination is impossible. ID2993 and the missing tenth programme target remain incompletely characterized.

## Upcoming releases and ranking

Dates are America/New_York (EST), from the saved live ALMA ObsCore metadata. These are release dates of specific observing units, not first-ever observations of these galaxies. Existing lower-resolution public observations were not analyzed as image cubes.

| Target | High-resolution CO release | Redshift | Absolute ceiling on F-DESI vs matched MOND speed difference | Assessment |
|---|---|---:|---:|---|
| UDS28473 / U4_28473, reference | Nov 5, 2026, 9:42 pm | 2.52455 | 4.86% | Compact CO, small inner differences; original target remains degenerate |
| UDS16442 / U4_16442 | Nov 24, 2026, 7:26 pm | 2.21777 | 3.97% | Largest ceiling among the other identified upcoming targets, but compact CO makes the outer regime difficult |
| ID2993 | Dec 4, 2026, 11:13 am | approximately 1.19 | 0.85% | Very weak MOND separation; insufficient authenticated mass/size/gas inputs for a halo ranking |
| GMASS1084 | Dec 22, 2026, 2:50 pm | 1.55204 | 1.93% | Most interesting conditional outer-curve opportunity among the modeled alternatives; still degenerate with MOND and fitted halos |

Ceilings assume identical baryonic distributions and PAPER66's n=1 interpolation and local acceleration normalization. They are reached only at arbitrarily low acceleration; they are **not expected observed separations**. The model's acceleration ratio is r(z)=sqrt[a^(-3(1+w0+wa)) exp(-3 wa(1-a))], with w0=-0.838, wa=-0.62. Because 0 <= d ln V / d ln a0 <= 1/4, the maximum difference relative to MOND is 1-r(z)^(1/4). The F-flat version is identical to this MOND comparator, so no rotation-curve precision distinguishes those two implementations. Other MOND interpolations or local normalizations are outside this screen.

## Actual modeled differences

Thin exponential stellar and gas discs were evaluated for 36 profiles and 288 radius/branch combinations. These span published size alternatives and gas conversion assumptions, not a probability-weighted posterior. Representative branches:

| Target and radius | Newtonian baryons only | F-DESI | Matched constant-scale MOND | MOND minus F-DESI |
|---|---:|---:|---:|---:|
| UDS16442, 3 kpc | 381.6 km/s | 390.7 km/s | 392.2 km/s | 1.5 km/s |
| GMASS1084, 8 kpc | 266.6 km/s | 297.2 km/s | 299.1 km/s | 1.9 km/s |

UDS16442 uses logMstar=11.22, optical stellar Re=4.291 kpc, gas Re=1.33 kpc, alphaCO=1. GMASS uses logMstar=11.31, stellar and gas Re=8.3 kpc, alphaCO=1. Its gas size is an assumed sensitivity branch, **not a measured exponential CO(3–2) radius**. Neither row asserts that ALMA can measure the stated radius at sufficient precision. UDS28473's historical 431/441/439 km/s row was independently recovered as a numerical cross-check; that row uses a different stellar-mass branch than the new grid.

At these example radii, a single-point three-standard-deviation separation would require total effective velocity uncertainty below about 0.50 and 0.65 km/s respectively, before allowing models to readjust their masses. Channel width alone does not determine velocity precision. Uncertainty in inclination, stellar mass, gas conversion, pressure support and beam smearing must be propagated. A difference from baryons-only Newtonian gravity is not by itself a difference from Newtonian gravity plus dark matter.

## Can competing models imitate the curves?

For each synthetic F-DESI curve, alternatives were fitted coherently across eight radii, from max(1 kpc, one beam) to the assumed gas R90. Stellar normalization could move +/-0.2 dex and gas normalization +/-0.3 dex. No independent adjustment at each radius was allowed.

The entries below are the **largest pointwise residual across all tested branches**, after fitting. They are not forecast measurement errors or confidence levels.

| Target | MOND with adjusted baryonic masses | Newtonian baryons + flexible NFW | NFW with fixed published concentration relation |
|---|---:|---:|---:|
| UDS28473 | 0.054% | 0.013% | 0.185% |
| UDS16442 | 0.050% | 0.018% | 0.134% |
| GMASS1084 | 0.356% | 0.348% | 1.790% |

The main NFW fit allowed concentration 1–10 and halo mass up to 10^14 solar masses, subject to a cosmic baryon inventory bound. As a robustness test, concentration was fixed to the Dutton & Maccio (2014) redshift-dependent relation. This second test uses total-equivalent halo mass, dark amplitude (1-0.157), and an explicit baryon budget. All 36 fixed-relation fits converged and passed that budget. GMASS's worst fixed-relation fits reach the allowed baryonic-mass boundaries, making its outcome especially dependent on improved mass information. No abundance-matching likelihood or halo response was included; this is not an exhaustive test of Lambda-CDM.

Interpretation: even imposing a conventional concentration relation does not give a large, unavoidable discrepancy in these tested profiles. A statistically meaningful preference remains possible with strong independent constraints and sufficiently precise resolved measurements; it has not been demonstrated by this pre-release screen.

## What would make an observation discriminating?

1. Independently constrain stellar/gas masses, inclination, spatial distributions and pressure support, then propagate their shared uncertainties through all models.
2. Measure resolved outer velocities where acceleration is low enough to separate the laws. Compact UDS CO profiles are a major limitation. An ideal annular-flux calculation is included in grid.csv, but is not a validated detection or kinematic-reach forecast.
3. Compare the complete predicted data cubes or a covariance-aware velocity likelihood with nuisance parameters fitted consistently. A curve matching F-DESI only favors it if the competing fitted curves are appreciably worse after accounting for model flexibility.
4. Freeze the mass/concentration constraints and comparison protocol before examining the newly released high-resolution cubes. Do not treat selected post-release baryonic branches as independent predictions.

The practical priority is GMASS1084 for testing an outer mass discrepancy, with UDS16442 as the earlier compact-disc consistency test. Neither currently offers a demonstrated clean F-DESI-versus-MOND test. ID2993 cannot be ranked against dark matter without better authenticated inputs.

## Rest of the programme

The project 2024.1.00100.L query returned nine non-calibrator science names although CONDOR advertises ten targets. The unidentified tenth target is a coverage gap, not evidence that it lacks discriminating power.

| Other archive name | Relevant status in saved snapshot |
|---|---|
| ASPECS1mm.03 | High-resolution band-4 CO already public July 7, 2026; upcoming Dec 22, 2:49 pm EST unit is band-7 dust continuum |
| ID48136 | High-resolution CO already public July 7, 2026 |
| ID51670 | High-resolution CO already public June 26, 2026 |
| UDS17159 | CO unit already public July 24, 2026 |
| zC-400569 | Only a public band-7 unit in the returned rows; no forthcoming CO release identified |

Public targets could be analyzed now, but would not constitute blind forecasts before their CO releases. New dust continuum can help constrain baryonic structure; it is not itself a rotation curve. No claims about an unlisted future observing unit are made.

## Reproducibility and limitations

- Inputs and assumptions: inputs.json, CONTRACT.md, SOURCES.md.
- Main calculation: forecast.py; run01/results.json, grid.csv, profile_fits.json and inventory.json. All nine internal checks passed; manifest validated against current inputs. Includes independent PAPER66 numerical reproduction and analytic/limiting-case checks.
- Halo robustness: halo_robustness.py and halo_contract.json; run02/halo_fits.json. **The overall run02 status is failed** because six of 72 fits (all in the additional +/-0.22 dex concentration variant) did not converge within the iteration cap. Those variant results are excluded from the table and conclusions. The separate 36-fit fixed-relation subset was checked for convergence, coverage and baryon-budget compliance. The failed record is retained intact; no overall success is claimed for run02.
- Only fixed PAPER66 CPL/n=1 parameters were screened. Changing its cosmological parameters, interpolation or calibration requires a new forecast.
- GMASS has published mass/inclination discrepancies and an assumed gas-size branch. ID2993 lacks authenticated gas/size inputs; a tenth survey target is unresolved. These prevent a complete target-by-target claim for all CONDOR galaxies.
- No proprietary cubes downloaded, existing PAPER66 forecasts/seals edited, or results published. This report is a self-reviewed finite computational screen, not a preregistered likelihood analysis.

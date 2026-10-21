# W4-16/17: the population-decline correction is material, but shape-only

Read-only audit completed: 46/46 checks in `raw_cached_audit.json`. This includes exact revision-byte comparisons, cached zero-crossing interpolation, frozen-control/verdict arithmetic, and independent raw eligibility/class counts. No original model, regression, bootstrap, permutation, or synthetic-world script was imported or rerun. The completed preceding W4-14/15 review and its 54-check audit are retained under `/private/tmp/cold-energy-heartbeat-20261021T000805Z/observational/`.

## Exact evidence and frozen outcomes

W4-16 source/results/output bytes match `f2342c5361319995cc0d1baa1017341f4ca19138`; criteria are unchanged from `e8e80f10f098cca23805d30762b31c6f9d64dc0e`. The actual frozen outcome is **UNRESOLVED**, with no declared mechanism signature met. Its full-point WLS median slope is +0.12125 +/- 0.08884, only 1.36 sigma from zero. The gas-class slope is -0.38344 +/- 0.21218 on 17 galaxies, not the same full cohort of 129. Thus the earlier description of a robust outward population decline was already stronger than this evidence.

W4-16's frozen M1 fails: its pressure plant gives positive rho=+0.10189, p=0.28247, rather than the declared significant negative sign. Its M2 passes the limited pattern check (full median changes; gas-class median remains within one saved sigma) but changes the eligible population from 129 to 111 and triggers the wrong mechanism label, ATTRIBUTED to D4. It validates sensitivity to that intervention, not causal identification of a stellar gradient. Code D3 tests any significant sign although the verdict asks for the declared beam-smearing direction; D2 uses a 2-sigma threshold rather than the stated p<0.01 mechanism threshold. Neither discrepancy changes the present UNRESOLVED result. Gas-class points are >=70% gas, not purely gas, so calling their inferred acceleration exactly immune to stellar M/L is also too strong.

W4-17 source/results/output bytes match the correction commit `876f0864202717b8e55251de6a5dbb6da78000c9`; criteria and pre-freeze synthetic files match `b0e8bee92ed41ce643d0292b378d864a3ca63246`. No later criteria amendment is needed to obtain its saved result. All cached zero crossings reproduce by direct interpolation of the saved curves.

For the real mixed-dominance cohort, S11 is exactly p64's original 11 galaxies (raw names are saved). Delta_g and Delta_r stay negative over the declared M/L grid 0.3..1.4; the full-point **unweighted** slope crosses at 0.51394. Therefore **NOT A SINGLE NORMALISATION (gradient-like)** is the correct frozen operational verdict. It does not identify a physical M/L gradient. Other position-dependent masses/kinematics, selection, or model inadequacy can generate the same outcome.

The broad population's unweighted median slope and radial-split curves cross at 0.48362 +/- 0.08035 and 0.58871 +/- 0.07869. These shape statistics are compatible with a common ordinary stellar normalization; they remove the premise that SPARC as a whole has an established outward decline at the fiducial mass model. This is a material correction to the W4-14..16 narrative. It does not prove that all galaxies have no anomaly or that residual structure is confined exclusively to the selected 11; a population median can cancel heterogeneous individual residuals.

## Cohort, truncation and uncertainty limitations

The phrase "130 galaxies" is a union across the M/L grid, not a fixed 130-galaxy sample contributing at every grid point. The code defines S_all from galaxies valid at **any** grid value, then uses nanmedians. Raw eligibility counts are:

| M/L | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 | 1.1 | 1.2 | 1.3 | 1.4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| participating population | 130 | 130 | 129 | 125 | 122 | 115 | 110 | 108 | 104 | 101 | 97 | 92 |
| S11 with Delta_g | 11 | 11 | 11 | 11 | 11 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |

All 11 S11 galaxies still supply full slopes/radial splits across the grid, but the gas/star statistic loses one contributor above 0.7. Valid points also change because g_obs>g_bar>0 is reapplied at every M/L. The population count declines from 2,986 eligible points at 0.3 to 1,475 at 1.4. This truncation is part of the declared pipeline; it means the curves mix normalization response with point/cohort selection. No fixed-cohort sensitivity or missingness correction was done in this audit.

The reported sigma(U*) is the standard deviation **conditional on bootstrap resamples that cross**, not an unconditional confidence interval. Only 150/500 real S11 resamples cross for Delta_g, and 177/500 for Delta_r; their point curves have no crossing. The quoted finite sigmas must not be read as symmetric errors on a measured finite U*. Population crossings are more stable (499/500 and 500/500), but they remain first crossings on a finite grid, with changing eligible data. Pairwise comparison using marginal errors does not recover the unsaved joint covariance.

## Controls and calibration scope

W4-17's saved controls behave under the frozen rules: exact-world A returns SINGLE at 0.5, and the planted-gradient B returns NOT SINGLE. This improves on W4-14..16's failed discriminator/power controls. Both are noiseless forward worlds using the same adopted simple-mu law and SPARC templates. They show these two declared worlds can be separated by this pipeline, not that all alternatives are separable or that the data are generated by the planted gradient.

There is a calibration-cohort disclosure worth retaining. The pre-freeze world-B numbers 1.063/1.293/1.214 combine Delta_g from mixed-class galaxies with s/Delta_r from the broader sample. They are not three S11 values. The final identical-pipeline S11 control gives 1.063/1.194/0.967; the final README distinguishes these, while the frozen calibration summary does not. The final world-B control still meets the frozen NOT SINGLE rule, so this does not reverse its actual control verdict. The calibration script's docstring says WLS but its implementation uses unweighted `polyfit`, consistent with the final W4-17 statistic.

## Cold-source implication

Withdraw the broad claim that a universal outward decline, established by W4-14..16, requires new cold physics. Preserve the narrower conditional residual: the selected mixed gas/star systems do not have both median class/radial residuals removed by one constant M/L over the tested grid. W4-14's pooled non-detection does not establish causal type erasure, and W4-15's opposite-sign INTERMEDIATE environmental correlation does not select an EFE explanation. W4-17 changes the observational priority toward cohort-aware, position-dependent baryon/kinematic checks.

The real-data W4-17 calculation tests **within-galaxy shape**, not the magnitude or universality of the inferred a0 level. Its fixed a0=half c sqrt(G rho_Lambda) is used to generate synthetic worlds, not to fit the real-data zero-crossing statistic. Consequently the new crossings do not determine kappa or independently establish kappa=1/2; that parameter remains FITTED.

None of these labels measures a hot versus condensed cold-medium phase, a cold source amplitude, early dense assembly, merger capture, radiative/charge loss, or a four-dwarf allocation. They supply no kernel that raises Draco/Sextans while protecting Fornax/Leo I. The physical transport and conservation gates remain open; no source action, frozen rule, repository file, or publication was modified here.

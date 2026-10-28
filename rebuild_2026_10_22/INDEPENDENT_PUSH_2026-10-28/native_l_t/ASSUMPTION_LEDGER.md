# Input and assumption ledger

This post-audit ledger sharpens the abbreviated pre-run classification in FROZEN_CRITERIA; it changes no numerical
input or criterion. "Native" labels describe where a formula came from, not a guarantee that it is derived or raw.

| Input / assumption | Classification | Source and practical limit |
|---|---|---|
| canonical / alt a0, kappa=1/2 | FRAMEWORK-NATIVE footing with FITTED coefficient | Theory equation page; never pooled. |
| A2 c_f medians, seed records, first-slope-crossing estimator | FRAMEWORK-NATIVE numerical output | X48 ng48 A2 JSON and x48_analyze.py; finite resolution and estimator dependence. |
| c_f(M)=L*S9(M)/S9(1e14), clamped outside 1e12-1e14 | FRAMEWORK-NATIVE numerical shape plus external level | CL2/CL3/LEE1; below-range values are extrapolation by clamping. |
| L=7.31*c64(1e12)/11.63 | POSITED cross-mass transport of a FRAMEWORK-NATIVE statistic | NL1 criteria §1.3; a 1e12 ratio is assumed at 1e14. Not measured cluster convergence. |
| ng48/64 seed identity | RAW code convention / numerical limitation | X48 common-mode correction says same labels change the physical field with ng. Bootstrap is not paired convergence. |
| ng64-only 68% bootstrap | Statistical convention | NL1 code50-51; excludes ng48-reference and mass-transfer uncertainty. |
| CLASS background A parameters and primordial P(k) | CMB PARAMETER CALIBRATION under the record's dust-limit model | F3 K2 and README §4: record's plik-lite refit, h=0.675780309, fitted A_s,n_s etc. Not raw measurements or a CMB-free prediction. No imported concentration relation. |
| GS1 fair-share/background parameters | FRAMEWORK-NATIVE BAO+BBN parameter inference and measured-budget calibration | CL2/CL3 use h=0.6856427, Omega_m=0.2976016, omega_b=0.0223081; distinct from formation background A. Not recomputed here. |
| delta_c=1.686, Delta=18*pi^2, EPS median coefficient0.974 | ANALYTIC MODEL ASSUMPTIONS | X41 criteria; spherical collapse and half-mass EPS. Scalar reproduction verifies implementation, not their physical validity. |
| Newtonian collisionless dust + Lambda zoom dynamics | POSITED ROUTE-E DYNAMICS | X48 frozen criteria; explicitly omits the a0 floor and is not v3s dynamics. |
| eta(c)=4*c^(5/4)/(3B(1)) and max surface-density floor | FRAMEWORK-NATIVE phenomenological core prescription | X43/X48; no field equation for condensation supplied by this audit. |
| constant-L crossover switch and separate S9-core amplitude | POSITED two-prescription structure | CL3 T_of vs ETAF code; one shared external level does not make the functions identical. |
| Existing empirical grade records | MIXED RAW measurements + SURVEY-CALIBRATION + framework model | CL2/CL3; this audit reads scores only and makes no new raw-data verdict. SPS, distances, gas models and survey nuisances are not re-audited. |
| Run logs, checkpoints, process table, snapshot/done existence | RAW OPERATIONAL observation | LIVE_STATUS timestamp; no partial halo/profile estimate, no ETA. |

No STANDARD-MOND-MACHINERY or LambdaCDM c-M relation is introduced by this new scalar audit. That limited statement
does not certify the entire inherited empirical harness as uncontaminated. Full background/IC and data calibration
audit remains separate from counting the halo-rule coefficients.

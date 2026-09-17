# KS00_INDEX — the eps_tot = 1/(32 pi) slot, swung (2026-09-16)

Format: `KSnn | verdict word | the one number | the file`. Every lane is a committed, runnable script
with its own `.out` (baseline) and `.json`; KS01 and KS06 carry a `MUTATE=1` control that flips a
load-bearing check to FAIL (rc=1). Run any lane from the repository root.

| lane | verdict | the one number | file |
|---|---|---|---|
| KS01 | **SLOT-NOT-LIVE** | the horizon entropy DIVIDES: physical `<h_uu^2>` is O(hbar) (~ G hbar H^2); the 08-09 pure number needs an extra factor S_dS ≈ 3.3e122 = 1/hbar (double count) | `KS01_sds_adjudication.py` |
| KS02 | **CONVENTION** | standard TT-graviton set gives eps_tot = 1/12 (kappa = 1.447); 1/(32 pi) is reached only by dropping the Friedmann factor 8 pi/3 = 8.378 (the loose choice); energy-density route gives a third value 1/90 (kappa 0.53) | `KS02_normalisation_table.py` |
| KS03 | **CANDIDATE-NOT-SELECTED** | 5 candidates inside 2 sigma; 1/2 separated from its nearest distinct rival (0.482) at 0.4 sigma today; needs ±1.2% on kappa for 3 sigma; degenerate with the H0 tension to 0.2% | `KS03_rival_coefficients.py` |
| KS04 | **CONTROL** | at k=3 a fraction 0.108 of O(1) natural numbers land in the 2 sigma kappa band; 0.016 at ±5%; 1/2 is op-count 1 (0 simpler in-band rivals), 1/(32 pi) op-count 3 (13 simpler) | `KS04_look_elsewhere.py` |
| KS05 | **OPEN-UNDER-POSTULATE** | 2/4 enhancement structures (Verlinde, CKN) reach within a factor 2 without a new parameter, but NONE derives the S_dS coherence; dS IR growth needs ~1e122 e-folds, primordial tensors are ~8 decades low | `KS05_category3_enhancement.py` |
| KS06 | **RATIONAL-AVAILABLE-NOT-SELECTED** | kappa^2 = 8 pi eps_tot (sympy exact); 1/(32 pi) = pi(S_dS)·(1/8)(coupling)·1/(4 pi^2)(T_GH); drift is m-independent; the graviton route is a DENSITY mechanism so kappa = 1/2 is rational and available — but its value rides on the normalisation convention (KS02) | `KS06_number_field.py` |

## The one-paragraph result

The gate (KS01) returns **SLOT-NOT-LIVE**. Computing the worldline's `<h_uu^2>` two independent ways —
the thermal coincidence limit and an explicit mode sum — gives the SAME variance, O(hbar) and ~ G hbar H^2,
with no free factor of N: the coincidence limit already IS the incoherent sum over modes. The graviton
field-mode count between horizon and Planck length scales as S_dS^{3/2} (a volume), while S_dS is the
horizon area-cell count; the 08-09 lane's eps_tot = S_dS · eps_1 re-multiplies the already-summed thermal
variance by that area-cell count, an extra factor 1/hbar with no dynamical origin — a double count. So the
horizon entropy **divides** (the 09-01 CTP lane was right), the drift is r-proportional (a Lambda
renormalisation) and shapeless (f = T^2, no interpolation function). The slot is live only under a NAMED
postulate — holographic coherence, an enhancement of exactly S_dS (category III). Conditional on granting
it, KS02 shows the standard normalisation gives kappa = 1.447, not 1/2 (the 1/2 needs the loose choice that
drops the Friedmann 8 pi/3); KS03 shows five coefficient candidates inside 2 sigma with 1/2 unseparated
from its nearest rival and degenerate with the H0 tension; KS04 prices a chance landing at ~11% (2 sigma)
or ~1.6% (±5%); KS05 finds no structure that derives the S_dS factor without substituting another postulate;
KS06 confirms kappa = 1/2 is the right KIND of number (rational, density mechanism) but its specific value
rides on the normalisation convention.

**Bottom line for rung 1 of the CLOSURE_MAP.** By the work order's own success criterion (KS01 must find the
multiplicative structure legitimate under an independently motivated postulate — it does not), kappa = 1/2 is
**a measured constant of the framework, not a derived one; the graviton-bath slot is closed with its
mechanism.** The remaining lanes are context, not rescue.

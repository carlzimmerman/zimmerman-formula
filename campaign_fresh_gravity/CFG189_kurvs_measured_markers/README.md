# CFG189 — the KURVS a₀(z) test re-run with the MEASURED outer rotation markers, for three laws

- **Criteria:** frozen in `FROZEN_CRITERIA.md` (39846c92e), before any marker value was read.
- **Script:** `cfg189_measured_markers.py`, about 1 s.
  - It runs CFG141's pipeline read-only and unmutated.
  - It uses CFG175's three laws, and CFG184's forward model for variant BS.
  - The markers come from the data chat's digitisation (5e8617c81).
- **Runs:**
  - The main run and MUTATE=1 exit 1, because of one kept control failure (C2, disclosed below).
  - MUTATE=1 (measured V × 10^0.3) moves the decision-cell class from lean rival to neither, as required.

## Bottom line

**The measured outer markers leave the lean class at the decision cell unchanged (lean rival). They move all three laws toward the data by 0.3–1.5σ, and T's shift of 1.46σ is past the declared line, so by the frozen form the headline reads CHANGED. One of five variants (both sides, at the shorter radius) flips the class to lean flat.**

| input | flat | a₀ ∝ H(z) | a₀ ∝ t(z)/t₀ | class at μ = 0.67, s = 1 |
|---|---|---|---|---|
| model V, Table B1 col 3 (CFG160, CFG175) | +0.144 ± 0.044 (+3.3σ) | −0.006 (−0.1σ) | +0.323 (+6.9σ) | lean rival |
| **measured, primary** (the farther side's outermost unclipped marker) | **+0.125 ± 0.051 (+2.4σ)** | **−0.021 (−0.4σ)** | **+0.295 (+5.5σ)** | **lean rival** |
| V-a, outer three (weighted) | +2.4σ | −1.0σ | +5.9σ | lean rival |
| V-b, both sides at the shorter side's radius | +0.1σ | −3.2σ | +3.4σ | **lean flat** |
| V-c, clipped included | +2.8σ | +0.1σ | +5.7σ | lean rival |
| V-d, i* deprojection | +2.2σ | −0.7σ | +5.3σ | lean rival |
| BS, σ_int from CFG184 | +2.2σ | −0.6σ | +5.2σ | lean rival |

- **Per disc, measured V_out against the model V.**

  | disc | measured vs model | radius note |
  |---|---|---|
  | KURVS-3 | +10.5% | at 10.06 kpc, not 11.70 |
  | KURVS-7 | −15.2% | |
  | KURVS-8 | −6.6% | |
  | KURVS-9 | +0.4% | |
  | KURVS-11 | −3.3% | |
  | KURVS-13 | +9.7% | |
  | KURVS-15 | −6.5% | |
  | KURVS-16 | −5.8% | at 10.05 kpc, not 10.90 |
  | KURVS-17 | −22.3% | at 7.34 kpc, not 9.90; its two outer markers are clipped |
  | KURVS-21 | −6.0% | |

  - The marker errors are larger than the table's model errors (e.g. ±32.9 against ±14.1 km/s for KURVS-3). That is part of why the z-scores shrink.
- **The shifts at the decision cell, measured minus model:** flat −0.019 dex (−0.84 in z), rival −0.015 dex (−0.29), T −0.027 dex (−1.46).
- **T under Kretschmer:** its KURVS break-even falls from 4.34 to 3.80, and the lower 1σ edge dips below the declared 3.47 ceiling. So T is now gas-allowed at s = 1 by CFG175's rule, but it still under-predicts the decision cell by 5.5σ.
  - At s = 1.42–3.00 T stays gas-excluded (4.97–9.11).
  - At P0 it fits (+0.9σ), as before.
- **Break-evens at s = 1 (flat / rival / T):**
  - model V: 2.11 / 0.62 / 4.34;
  - measured: 1.86 / 0.50 / 3.80.
- **Fit points at μ = 0.67:** flat 0.42, rival 1.12, T < 0. The model V gave 0.39 / 1.03 / < 0.

## Reading

- **Replacing the model velocity by the measured one does not change which way the decision cell leans.** It weakens the lean: flat goes from +3.3σ to +2.4σ, because the markers carry larger errors and scatter about the model by −22% to +11%.
- **The one variant that flips, V-b, is not a free choice.** It measures at the shorter side's outermost radius, typically about 7 kpc instead of 10–12. That trades radius for cancelling any centring offset.
  - At those radii flat fits (+0.1σ) and the rival is −3.2σ.
  - Where the verdict sits depends on which radius is called "the outer point". That is a new form of the dependence CFG160–168 already found.
- **Unchanged by this lane:** the pressure, gas, calibration and rotation-curve-shape dependences (CFG160–168, 170, 175, 184). It replaces a model value by a measured one; it does not remove them.
- **Standing:** the KURVS lean rests on a calibration, gas and radius choice the data cannot fix. Not a detection either way.

## Disclosed departures

1. **C2 fails as frozen** ("the marker radii used match the σ-profile radii within 0.02 kpc"): 22 of 231 markers exceed 0.02 kpc. It is kept, and it makes every run exit 1.
   - Two of those markers are KURVS-3's extra velocity markers at −9.41 and −8.57 kpc, which have no σ counterpart (the data chat's note).
   - The other twenty are KURVS-17's whole panel, offset by a constant 0.065 kpc between the velocity and σ calibrations. That is 8% of a pixel, and the data chat's one flagged galaxy.
   - The side signs agree everywhere, so σ(R_out) is taken from the correct side. The 0.065-kpc offset changes it negligibly.
2. **The frozen headline form fires CHANGED on T's z shift alone** (1.46). The flat/rival class is unchanged. Both are stated.
3. **Spurious floating-point warnings** ("divide by zero / overflow encountered in matmul") come from numpy's Accelerate BLAS on this platform, inside CFG184's exec'd functions. Every result is finite and CFG184's f_bs values are reproduced (for example KURVS-11: 0.242 at R_out, 0.232 at CFG141's radii).

## Controls

- **C1:** with the table's model V and CFG141's σ_out, the pipeline reproduces CFG160's cell (+0.1441 / −0.0060) and CFG175's T cell (+0.3227).
- **C2:** as above.
- **MUTATE=1:** the class changes (lean rival → neither).

## Untested (declared)

- the beam-smearing bias of V;
- correlated neighbouring points;
- the centring of the one-sided variants;
- non-circular motions;
- the COSMOS half of KURVS.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour any model, or that the theory is closed.

## After CFG183 (the referee of CFG175; appended 2026-09-29; the text above is unchanged)

- **T's rows here carry CFG183's caveat on CFG175:**
  - T's s = 1 status is fragile (it turns on a 2% margin to the declared gas ceiling in CFG175, and is already gas-allowed by the lower edge here);
  - P0 is the uncorrected table, not a neutral null;
  - the s = 1 exclusion label is not informative in mocks.
- **Wording for T in this lane:** under Kretschmer at the decision cell, T under-predicts by 5.5σ with the measured markers; its gas status there is not robust to the gas ceiling, the sample or the calibration.


## Corrections after the independent referee CFG194 (255cf12d6; appended 2026-09-29; the text above is left as first written)
The referee re-derived this lane with independent code and REPRODUCES every pass line P1–P8: per-disc inputs identical, 0 of 75 status labels differ. The orchestrating session re-ran the referee's `run_all.sh` in a scratch copy, and every output is identical apart from timing lines. Five sentences above are not supported, or only partly:
1. **"The lean weakens because the markers carry larger errors and scatter about the model."** About half of the drop in z comes from the larger errors, which carry no information: χ² = 2.3 for 10 dof. About 29% comes from the marker-minus-model value, which is noise (p = 0.26). The largest single piece, about 55%, is the change of radius and σ at R_out, mostly KURVS-17.
2. **"Trades radius for cancelling any centring offset."** Centring is not what changes the class. The farther side alone at the same radius gives the same class, so the radius is the whole effect.
3. **"Rests on a calibration, gas and radius choice the data cannot fix."** This is supported, and it is stronger than stated:
   - 12 of 19 pre-declared marker choices leave the class;
   - the lean disappears for a coherent 4.5% lower V;
   - the frozen mock informativeness rule fails once gas and α are uncertain: P(lean rival | flat truth) = 0.26.
4. **"1 of 5 variants flips"** understates the fragility. The lean rival sits 0.45σ above its class edge, and which radius counts as "outer" decides the class.
5. **Omitted above:**
   - Under the measured markers the P0 class changes from non-diagnostic to lean flat (flat −1.94σ).
   - T's s = 1 gas-status change (excluded → allowed) is robust in leave-one-out and bootstrap.
   - The KURVS-17 wording should be "19 markers at 0.065 kpc plus one unpaired clipped marker".

**Standing wording after the referee:** "at z ≈ 1.5 the KURVS measured markers give a fragile lean toward a₀ ∝ H(z) that turns on which radius counts as outer and on the gas and α calibration; not informative once those are uncertain; not a detection; flat a₀ not refuted."

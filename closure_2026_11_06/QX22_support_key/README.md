# QX22: is the law's hot/cold step keyed on kinematic support? NO VERDICT as frozen; the support key fails at about 3 sigma

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: iter_1/FROZEN_CRITERIA.md (f2ac9999a5), committed and
pushed before any script. Script: iter_1/qx22.py (one thread, seconds). Outputs: iter_1/qx22.out / qx22.json, and
qx22_MUTATE.* for M1 and M2. A rerun gives a byte-identical qx22.json.

## What was tested
H': the boost multiplies the law's phantom by 1 + (F0 - 1) s, where s is the dispersion-support fraction from lambda_Re.
- Rotation-supported systems get no boost; dispersion-supported systems get the full one.
- F0 is calibrated on the bright M31 dSphs: 1.58 canonical, 1.54 alt. The X-ray ellipticals give 1.52 / 1.55, a
  systematic that is reported.
- Three mappings s(lambda) were frozen in advance.

## Label: NO VERDICT (narrow)
T1 graded MaNGA DynPop red galaxies (u - r >= 2.5, gas-poor) at r_half. The statistic is low-lambda (< 0.2) minus
high-lambda (> 0.5), on KU2's matched M* x sigma cells.

| | canonical | alt |
|---|---|---|
| D measured (ln) | +0.002 +- 0.045 | +0.002 +- 0.046 |
| M-step: D_pred, z | +0.141, -3.11, KILLED | +0.144, -3.08, KILLED |
| M-lin: D_pred, z | +0.143, -3.16, KILLED | +0.144, -3.09, KILLED |
| M-sq: D_pred, z | +0.140, -3.08, KILLED | +0.139, **-2.99, neither** |

- **The frozen label is missed by 0.01 sigma.** KILLED needs every mapping on both footings, and alt M-sq sits at -2.99
  sigma. The label is NO VERDICT, not KILLED.
- **The numbers are not ambiguous about the support key.** At equal M* and sigma, dispersion-supported red galaxies sit on
  the law exactly as rotation-supported ones do (+0.002 +- 0.045 ln). A support key predicts +0.14 ln (about +0.06 dex).
  It is out at about 3 sigma, but not by the frozen rule. This extends KU2's binary slow/fast result to a prediction.
- **Power:** C-inj recovers 0.137 / 0.135 of the injected 0.143 / 0.144, PASS.

## T2 (graded compatibility): KiDS early/late
MaNGA's mean s for red against blue galaxies at log M* 10-11 predicts a lensing split of only +0.02 to +0.04 dex.
- The measured split is 0.158 +- 0.064.
- M-lin and M-sq are COMPATIBLE only because the 2 sigma window is wide. M-step is not.
- Even where compatible, the support key would carry about a quarter of the KiDS step.

## Reported, not graded
- **T3 type at fixed support** (lambda > 0.5): red minus blue is +0.017 / +0.018 dex (+- 0.009), before blue's missing gas,
  which biases it negative. That is small.
- **T4 Local Group field dwarfs**, types provisional, from memory of McConnachie 2012:
  - gas-poor dSph / transition dwarfs (N 8): +0.134 / +0.123 dex above the SPARC anchor;
  - gas-rich dIrrs (N 5): -0.027 / -0.035.
  - Most dIrrs are dispersion-supported in their stars too (literature, e.g. Kirby+2014 and Wheeler+2017; not on disk). So this split follows gas content or type, not stellar support.
- **T5, what a support key cannot carry:** the fully dispersion-supported classes (bright M31 dSphs, ellipticals) average
  +0.19 dex. X-COP sits another +0.25 dex above that; groups sit +0.04 / +0.05 above.

## Reading (post-data, not the label)
The step does not follow how a system is supported. Dispersion and rotation look the same to the law in gas-poor galaxies at
r_half. The pattern across classes looks more like cold-gas-poor against cold-gas-rich:
- the step is present in dSphs, ellipticals, early-type lenses and hot systems;
- it is absent in SPARC discs, dIrrs and late-type lenses.

QX20's f_gas counted total gas, hot gas included. A **cold-gas (HI) fraction key** is not yet tested. On top of whatever
carries the galaxy-scale +0.19, clusters need another +0.25 dex.

**NEXT candidate (sketch, not graded).** Any covariant version would have to couple the khronon response to a matter
property that tells cold, rotating, gas-rich discs from gas-poor systems at equal mass, field and support. Support itself is
now disfavoured as that property. A coupling to the matter momentum-density coherence (net rotation against isotropic
stress) is therefore NOT the next candidate. A cold-gas key is an empirical target with no covariant form identified.

## Controls
- KA1: KU2's D is reproduced exactly (+0.023332 / +0.025383).
- C-inj: PASS (above).
- M1 (lambda shuffled within cells): |D| <= 2 sigma, PASS.
- **M2 (Newton in place of the law): FAIL as frozen.** D_newton is +0.075 against D_law +0.002, which is 1.6 sigma, not the
  3 sigma frozen. The low/high-lambda difference is only weakly sensitive to swapping gravity, because both groups share
  cells in M* and sigma. The C-inj check, which is what matters for this test's power, passes.

## Not covered
- r_half only (median y 0.8-1.0); MaNGA red galaxies only (492 in the graded groups).
- NSA masses with no gas.
- Dwarf types from memory; no stellar v/sigma table on disk.
- No environment control.

Kappa = 1/2 FITTED; not theory closed.

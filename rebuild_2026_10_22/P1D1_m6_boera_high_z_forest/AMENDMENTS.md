# P1D1_m6_boera_high_z_forest: AMENDMENTS

## A1 (committed alone, before any P1D value is read): how S0e reproduces X63

`x63_m6_forest.py` is a top-level script. Importing it runs it and overwrites X63's committed outputs, so its formulas
cannot be imported without side effects. S0e is therefore met by an **independent re-implementation** of X57's / X63's
M6 formulas in this lane's script. The formulas re-implemented are:

- X57 L399–428: f_max → δ_c,in, δ_b,in; σ²_ad(R_L, 0) from the BBKS shape; F_b,max.
- X63 L147–206: P_ad0, `p1d` on KG (logspace −4 to log 200, 60001 points), iso amplitude, ratio grid.
- X63 L203–206: s/km → h/Mpc.

On the inherited background, the re-implementation must reproduce X63's **committed** `x63_m6_forest_results.json` to
3 decimals, as S0e already requires: max S at R_J 0.1, z 4.2 / 4.6 / 5.0, both footings, and F_b,max(z = 3). This
is stricter than importing, because it is a second implementation checked against the first. Two things are unchanged:

- X22's f_max and R_L are read from X22's committed JSON, as X63 does.
- Gates, thresholds, model, variants and checks are unchanged.

## A2 (committed alone, after a Step-0 STOP, before any grading): inherited-background shape parameters

The first run stopped at S0e: 4/8 items. F_b,max(z = 3) came out 0.06018 against 0.06038, and max S 0.2617 against 0.2614.
The run output is kept as `p1d1_m6_boera_STOP_preA2.out` / `.json`.

- **Cause.** A re-implementation error. X57 (L410–417) and X63 (L83–84) build the BBKS shape and σ₈ normalisation with
  Ω_m 0.315, Ω_b 0.0493 and h 0.674. Their D(z) and E(z) use Ω_m = 0.0493 × 6.364 = 0.31375. The first script used one
  Ω_m for both.
- **Fix.** The background class takes separate shape parameters. INHERITED uses X57's two values. NATIVE uses the same
  L1 values in both places, as frozen.
- **Unchanged.** Gates, thresholds, model, variants and checks. The table values had been parsed at Step 0, but no fit or
  grade was run.

## A3 (fix-forward, 2026-10-27; after the completed NOT DIAGNOSTIC result)

The independent closure review found two interpretation/check defects. This
amendment supersedes the identified claims; the frozen criteria, original fit
script and all historical fit outputs remain unchanged. It does not alter a
data gate or revive the inadequate forward model.

1. **Interpretation correction.** Frozen criteria lines 100–101 reverse the
   upper-envelope implication. Excluding a larger proxy signal does not exclude
   a weaker physical response at the same patch baryon fraction. A template
   limit becomes a physical F_b limit only through an independently validated
   response mapping. X57's F_b,max is a ceiling, not a required population.
   Closing M6 through this forest comparison additionally needs
   F_b,required > F_b,allowed on common conventions.
2. **Check correction.** The original K3 plants through `Sp.predict`, which
   shares SIGN with the fitted model. Its observed mutation failure does not
   independently validate the sign. The original primary K3/K4 are vacuous
   because G1 fails. They remain historical outcomes, not new evidence.
3. **Fix-forward implementation.** `p1d1_independent_sign_check.py` constructs a
   positive injection without accepting SIGN or calling the candidate model.
   It exercises the original script's actual shape and GLS methods, extracted
   without its top-level side effects, on controlled synthetic spectra. The
   positive-sign candidate must recover mu=1; the negative-sign candidate must
   fail against the same injection. The formerly correlated negative injection
   is also demonstrated to falsely recover. This check is unconditional and
   uses neither G0 nor G1. Its fixed-nuisance covariance is synthetic; it is
   only an implementation regression, not observational sensitivity or flux
   calibration. Use `--output NEW_PATH` (exclusive creation) for named results.

The interpretation and exact scope are in `CORRECTION_2026_10_27.md`. Bounded
regression/provenance files live in
`../../closure_program_2026_10_27/technical_fixes/`. No original fit is rerun.

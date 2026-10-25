# X29_late_power_shear: raw KiDS shear cuts the late-heating sheet in half

Criteria: `FROZEN_CRITERIA.md` (35b3573518, committed alone). `AMENDMENT_A1.md` (1e06cc9946, written during the main run,
after canonical was seen). κ = ½ FITTED. Footings never pooled. RAW KiDS-1000 / DES Y3 ξ±, scored with the record's native
scorer (CFG654) against the stored S0 control (NCS0, 1024³). No ΛCDM S₈ number or HMcode. Assumption A: the linear T²
multiplies the nonlinear P. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen rule): **SHEET CUT**, both footings

| | canonical | alt |
|---|---|---|
| X26 allowed points | 45 | 37 |
| **survive** (KiDS Δχ² < 9, all finitely graded) | **23** | **15** |
| excluded, finite Δχ² ≥ 9 (min +22.2) | 13 | 14 |
| ungraded: scorer breakdown (Δχ² > 1e6, see A1) | 9 | 8 |
| survivors: KiDS Δχ² | −3.07 … +6.99 | −3.10 … +6.99 |
| survivors: T²(z = 0, k = 1 h/Mpc) | **0.835 – 0.984** | 0.835 – 0.987 |
| survivors: σ₈ ratio | 0.991 – 0.999 | 0.991 – 0.999 |
| survivors: cosmic C₀ (c_s today) | 96 – 329 km/s | 89 – 268 km/s |
| excluded (finite): T²(k = 1) | ≤ 0.766 | ≤ 0.811 |

**The edge.** Among finitely graded points the shear separates cleanly on the suppression at k = 1 h/Mpc. Points with
T² ≥ 0.835 survive; points with T² ≤ 0.81 are excluded at Δχ² ≥ 22. **Raw cosmic shear allows late heating to remove at most
about 15 % of the power at k = 1 h/Mpc today, and σ₈ by at most about 1 %.** The ungraded points have T²(k = 1) = 0.08–0.83,
so all but one lie on the excluded side of the edge. The exception, at 0.831, sits inside the 0.81–0.835 gap. They are
not counted as excluded.

- **DES Y3:** Δχ² −0.2 to +1.6 on survivors. NOT DIAGNOSTIC, as in CFG654/CFG909, because the T-OWN tooth fails.
- **No amplitude caveat applies.** Survivors span Δχ² −3.1 to +7.0, so none is below −4.

## Checks

- Main run 5/6 (its .out predates A1's code edit; the committed script reruns it 6/6 on identical numbers, see A1's provenance note). K0 failed only at its frozen 1e-10 tolerance: the identity gives Δχ² = −4.3e-5 / −2.1e-5, from the S0
  control's own P_grav vs P offset (A1). K1, K2 (NC1x reproduced exactly), K3 (0.27 GB) and K4 (σ₈ ratio ≤ 1 everywhere) pass.
- Floor rerun (A1) 6/6. It gave the same grades at every point (0 class differences). The artefacts did NOT go away, so
  they are not caused by T² reaching zero. Their cause inside the scorer (strongly suppressed spectra) is not diagnosed
  here. They stay UNGRADED.
- `--mutate` (1/T², power raised): K4 FAILS on both footings, as required (4/6). As a bonus control, raising the power by
  the same factor leaves only 2 / 1 points surviving, so the shear bites in both directions.

## Reading

- The cold-sector spec's late heating survives raw shear, but only its gentle half: cosmic c_s today ≲ 270–330 km/s, with
  suppression at k = 1 of ≤ 15 %.
- Together with X26, the allowed late heating is now pinned from three sides:
  - clusters set the hot temperature in deep wells (550–770 km/s);
  - shear caps how much small-scale power it may erase in the field;
  - the forest caps how early it may switch on.
- This is a sign-definite prediction: a low-z power deficit at k ~ 1 h/Mpc of up to about 15 %, and none at k ≲ 0.3
  (T² ≥ 0.98 there).
- Not graded: the nonlinear response of a hot component in halos (assumption A; it would restore some power), and the
  scorer breakdown points.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `x29_late_power_shear.py`, `.out` / `_results.json` (main), `_A1FLOOR`
(floor rerun), `_MUTATE`, `run_*.log`.

    OMP_NUM_THREADS=1 nice -n 15 python3 x29_late_power_shear.py            # main (K0 fails at the frozen 1e-10 line only; A1)
    OMP_NUM_THREADS=1 nice -n 15 python3 x29_late_power_shear.py --floor    # A1 floor rerun
    OMP_NUM_THREADS=1 nice -n 15 python3 x29_late_power_shear.py --mutate   # K4 must fail

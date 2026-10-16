# CFG808 FROZEN CRITERIA: free cold energy from EXPELLED gas (H-EX), with mass-dependent census supply (committed before any script)

**Motivation (post-hoc, disclosed).** CFG727's eRASS1 pass is a cancellation (diag_terciles: middle tercile short, Z +2.9;
heavy tercile overshot, Z −6; ACCEPT ×2 overshoot). The data want more free cold energy at intermediate mass and less in the
heaviest systems. That tracks the census's retained fraction, which rises with mass. This is a FORWARD test of a rule fixed
here. The diagnostic that motivated it has been seen.

## Rule H-EX (no new constant)
- Everything is CFG727's machinery, with ONE change: the catchment.
- **Catchment:** bc = max(M_cond/0.10, M_retained / f_ret(M_ta)), with M_ta = bc/f_b, solved as a fixed point.
  - f_ret is the record's census, CFG416 fret_of, verbatim: 0.10 below log M_ta 12.5; then +0.45/dex to 13.5; then +0.30/dex,
    capped at 0.90.
  - CFG727 used a constant 0.90 (the X-COP value) at all masses.
- **Supply:** 5.364 × bc.
- **Tethered law:** sourced by ALL retained baryons, condensed plus hot (CFG727's 'ALL' source).
- **Free:** the remainder, which is the cold energy of the expelled baryons (S4 untether-on-unbinding). It is placed by CFG637
  Method A in the total potential, exactly as in CFG727.
- Stellar placement: as in CFG727 (BCG Hernquist R_e = 0.015 R_X; members r^−2.5 over 0.1–1 R_X).

**Cases.** H-EX × {ν_s, ν_mono} × {canonical, alt}. Control: CFG727's 'ALL' (ν_s, canonical) with the constant 0.90 must
reproduce CFG727's stored ALL rows (eRASS1 MID 1.40, ACCEPT OUTER 0.92, eFEDS χ² 29.4) within 0.01.

## Tests and pass rules (ν_s primary; both footings, never pooled)
1. **eRASS1 318:** MID and OUTER within 2σ (jackknife 30), AND **every gas-mass tercile** has |Z_MID| < 3 (terciles as in
   diag_terciles).
2. **ACCEPT 8:** OUTER within 2σ (bootstrap).
3. **eFEDS 131:** χ² p ≥ 0.01.

**Verdict:**
- **PASS** if 1, 2 and 3 all pass on ≥ 1 footing.
- **PARTIAL** if two pass.
- **FAIL** otherwise.

KiDS early types are NOT scored here: the rule changes galaxy-scale supply, so it needs a separate T-K rerun. Stated now.

## Controls
- K1: the ALL control reproduces CFG727 as above.
- M0: the plain law reproduces CFG687 PL (≤ 1%).
- C1: supply = settled + free (< 1e-9).
- MUTATE (reported): f_ret := 0.90 everywhere must reproduce the K1 ALL numbers, which shows the census is the only change.

## Machine
- eRASS stage via par727.py (CFG727's verified parallel driver, implementation only).
- ACCEPT and eFEDS stages run concurrently, 1 process each.
- Before the T1x 1024³ reruns; nothing runs beside those.

κ = ½ fitted; cold energy mass required; not theory closed.

# CL3_one_number: the switch threshold as X43's crossover at the same level L (one number)

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (47625a9db2).
- **Harness:** CL2 (b57ed8751f); crossover as in DT1 (d782d8ec78).

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen rule): **ONE NUMBER PASSES (canonical) at L = 3.75 and 3.9**

| L | T_canonical / T_alt (log M☉) | canonical | alt |
|---|---|---|---|
| 3.75 | 12.236 / 12.574 | **every line passes** (groups +1.76, G-OUT-all −1.85, lensing +0.0) | only its known lines fail |
| 3.9 | 12.149 / 12.486 | **every line passes** (groups +1.79, −1.90, lensing +0.5) | only its known lines fail |
| 4.0 | 12.093 / 12.429 | lensing fails (+22.4): the threshold falls below the lens masses | only its known lines fail |

One external number (L ≈ 3.75–3.9) sets both the switch and the cores on the canonical footing, with the native S9 slope
and the measured cluster budget. The calibrated count drops from two (T, L) to one.

## The limit (read with CL2)

This holds only for the S9 and S3 slopes; the NFW-fit slope fails (CL2). Every held-out test of the switch picture fails
(HO1, HO2, HO3; see CL2's README). Above all, **the Milky Way would need T < 10^11.9, against the lensing need of
T > 10^12.15.** CL3 is therefore a compact description of the graded lines, not a validated mechanism.

## Checks: 10/10

- S0a: T_f(4) reproduces DT1.
- S0b: reproduces CL2's S9 L 4 point.
- K1: the switch property.
- K2: T_f decreases in L.
- K3: 0.67 GB.
- **Pending:** the twin and the rerun.

## Files

- `cl3_one_number.py`
- `cl3_one_number.out` and `cl3_one_number_results.json`
- the per-run outputs

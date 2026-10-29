# X48_native_cf_zoom: native formation concentrations. A1 class (ng 48): NATIVE c_f ABOVE WINDOW, at ng 48; convergence beyond ng 48 not tested. Regrade: NATIVE-CC FAILS, inner band only

> **Correction note (10-26, fix-forward; found by the PAPER62 draft-2 audit 85fd7a6912):**
> 1. The ng 48 summary line below says "MGAS T3 OUTER now passes (Z −0.24)". −0.24 is **G-OUT-T3** (the KT T3 OUTER band),
>    not MGAS T3 OUTER. The MGAS T3 OUTER key (**G-OUT-M3**) is **Z +1.80** (canonical h 0.672). It still passes, so the
>    class is unchanged; the label was wrong.
> 2. "Z −2.41 / −2.06" for G-IN-Mall are the **h 0.672 / h 0.686 cells** on each footing, not canonical / alt. The two
>    footings give the same values (−2.41 at h 0.672, −2.06 at h 0.686).
> Numbers in the committed JSON (`x48_regrade_x43copy_ng48_results.json`) are unaffected. Result commit 737193f3fa's message
> carries the same slip; it is corrected here, not rewritten.


Criteria: `FROZEN_CRITERIA.md` (1932858ae8, committed before any production number). Engine and smoke evidence: df13411b6e,
`SMOKE_EVIDENCE.md`. Physics: collisionless dust + Λ on the record's background A (route E's cold dark energy without the a₀
floor), **not v3s**. κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

The six runs at 10¹³ and 10¹⁴ M☉ were started directly (single-thread, nice 15, owner 10-25 "keep it cranking"), in the
same work folders as their queue twins, which are on hold.

## A1 RESULT (ng 48 grid, 2026-10-26; criteria 1932858ae8 + A1 2bfdeb83a9, implementation acb2bf5277)

All nine ng 48 runs (N = 24 405) completed. They ran directly through `run_direct3.sh` (single thread, nice 15; 838 to 1176 steps).
Checks: K0 constraint ≤ 9e-16, K2 drift ≤ 4e-15, K3 synthetic c = 4 → 3.84 PASS. The MUTATE run (synthetic c = 8) fails K3 and
exits with 1, as required.

| M | ng 48 seeds (c_f, −2 crossing) | median | ng 38 median | particles inside r₋₂ |
|---|---|---|---|---|
| 10¹² | 3.10, 12.74, 7.17 | 7.2 | 10.6 | 516–2873 |
| 10¹³ | 2.31, 13.38, 6.97 | 7.0 | 5.9 | 399–4684 |
| 10¹⁴ | 2.59, 5.62, 9.00 | 5.6 | 11.0 | 702–4358 |

**A1 class: NATIVE c_f ABOVE WINDOW** ([3.3, 4.6] at 10¹³ and 10¹⁴), **at ng 48; convergence beyond ng 48 not tested.**

Reading this as a measurement needs care, and the record has to say so plainly:
- The per-run ng 38 → 48 shifts run from −80 % to +48 % (table in `x48_analyze_ng48.out`). The 10¹⁴ median moved −49 % and the
  10¹³ median +18 %.
- Seed scatter at ng 48 is a factor of 4 to 6 at every mass (2.3–13.4).
- The −2 crossing c_f is therefore not converged at these particle counts. "Above window" is the frozen class, not a settled
  native concentration.
- Reported only: the NFW-form fit has medians 7.1 / 5.6 / 5.05 at 10¹² / 10¹³ / 10¹⁴.

**Regrade (frozen §3, X43 rule with η(M) from the ng 48 medians: η 30.7 / 29.7 / 22.7 vs X43's 14.83).** On both footings:
SPARC passes (0.065 at Υ 0.64 / 0.066 at 0.53). Groups are CONSISTENT (Z +1.53), MGAS T3 OUTER now passes (Z −0.24), and every
MID/OUTER cell passes. **The rule FAILS on the INNER band, G-IN-Mall (OVER, Z −2.41)**, the same ~2× inner over-prediction
that IC1 isolated. Outputs: `x48_regrade_ng48.out`, `x48_regrade_x43copy_ng48.out`.

Reading: a higher c_f clears the two keys that X43 at c_f = 4 failed (groups, MGAS T3 OUTER), but it pushes the inner band over.
At c_f = 4 the inner band passes and those two keys fail. No single c_f passes all 15 cells. X43 stands with c_f = 4 external.
The inner band is the binding problem. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

## FINAL (ng 38 batch, all ten runs, 10-25)

| M | ng 38 seeds (c_f from the −2 crossing) | median | particles inside r₋₂ |
|---|---|---|---|
| 10¹² | 10.60, 12.59, 10.19 | 10.6 | 304–468 |
| 10¹³ | 5.86, 9.02, 5.92 | 5.9 | 447–847 |
| 10¹⁴ | 12.68, 8.03, 11.01 | 11.0 | 296–554 |

**Resolution check (frozen §3):** for 10¹⁴ M☉, seed 1, ng 38 → 48 (N 12k → 24k), the −2-crossing c_f goes **12.68 → 2.59**
(−80 %, line ±20 %), with 4 358 particles now inside r₋₂. **Frozen class: UNRESOLVED.** The ng-38 −2-crossing c_f is not
converged at these particle counts, so the provisional regrade below is not evidence either way.

Reported only (no verdict weight): the NFW-form fit of M(<r) gives 5.90 at ng 38 and **4.00 at ng 48**. The standard
formation value, and the data's pinned 4–4.2, sit right there. One run, and the NFW form is a fitting shape, not a measured
crossing.

**What resolves it:** ng ≥ 48 for every mass and seed (about 6–7 h per run at one thread, so ~7 h wall if all nine run in
parallel), or a faster force solver. Until then X43 stands with c_f = 4 external.

## Provisional c_f at the two masses run first (superseded by the resolution failure above; kept as run)

## Native c_f (frozen measurement, x48_analyze.py; checks K3 pass, drift ≤ 4e-15, constraints ≤ 1e-15)

| M | seed 1 | seed 2 | seed 3 | median | particles inside r₋₂ |
|---|---|---|---|---|---|
| 10¹³ | 5.86 | 9.02 | 5.92 | **5.9** | 447–847 |
| 10¹⁴ | 12.68 | 8.03 | 11.01 | **11.0** | 296–554 |

**Frozen class: UNRESOLVED (pending).** The 10¹² mass and the ng = 48 check are not yet run. On the measured masses, c_f lies
**above** the data window [3.3, 4.6].

## Provisional regrade of X43 (x48_regrade.py; η = 24.2 at ≤10¹³, 52.6 at ≥10¹⁴, interpolated in between)

| key (canonical; alt the same in class) | X43 (c_f 4) | native |
|---|---|---|
| SPARC rms / Υ | 0.078 / 0.77 PASS | **0.068 / 0.68 PASS** |
| groups | Z +2.05 FAIL | **Z +1.62 PASS** |
| MGAS T3 OUTER | Z +2.41 FAIL | **Z +0.79 PASS** |
| MID T1 / T2 / T3 | pass | Z −2.60 / −2.14 / −2.87 (OVER) |
| INNER all | pass | Z −3.52 (OVER) |

**Reading (provisional).** The native concentration clears both keys that every earlier rule failed (groups, MGAS T3 OUTER),
but it over-concentrates the cluster cores. The data sit between c_f ≈ 4 and the native ≈ 11 at cluster mass.

Caveats, to be graded when the batch lands:
- These are isolated spheres: no external tides or late mergers, both of which lower concentration.
- Particle counts inside r₋₂ are modest (300–850); the ng = 48 run tests this.
- c_f rises with mass, the opposite of the usual trend. The likely cause is the constrained mean-curvature peak at high ν.

## AMENDMENT A2 result (2026-10-27): ABOVE WINDOW at nine seeds; the X43 regrade now FAILS the SPARC line

All 18 A2 runs finished, so every mass has 9 seeds at ng 48. Files: `x48_analyze_ng48_A2.out`, `x48_grade_A2.*` and
`x48_regrade_A2.*`. The committed 3-seed `*_ng48` files are unchanged, because X53, X56 and X58 read them. The analysis
only gained a `--tag` output option.

| M200 | c_f, nine-seed median (68 % bootstrap) | NFW-fit median (reported) | grade |
|---|---|---|---|
| 10¹² | **11.63** (8.37–12.74) | 7.10 | ABOVE WINDOW |
| 10¹³ | **8.22** (6.97–11.23) | 5.60 | ABOVE WINDOW |
| 10¹⁴ | **7.31** (7.13–9.00) | 5.40 | ABOVE WINDOW |

**Frozen verdict: ABOVE WINDOW** (window [3.3, 4.6]), at ng 48. Convergence beyond ng 48 is not tested.

**Regrade (X43 rule, nine-seed c_f; η = 56 / 37 / 31):**
- **SPARC line FAILS:** rms 0.0774, median Υ 0.31 / 0.30.
- Groups pass: Z +1.33.
- Clusters fail G-IN-all, G-MID-T1 and G-IN-Mall (all OVER), on both footings.
- The 3-seed pass (`x48_regrade_ng48`) does not survive more seeds.

**Caveats (reported, not graded):**
- Per-seed c_f spans 2.3–22.7.
- In 8 of 27 runs r₋₂ sits at the smallest resolved radius, ≈ 0.010 (M/10¹²)^{1/3} Mpc. Those c_f values are
  resolution-limited and probably biased high. The NFW-fit medians (5.4–7.1) are lower but also above the window.
- A higher-resolution grid (ng ≥ 64) is the test of whether native c_f falls into the window. This lane does not run it.

κ = ½ FITTED. Not theory closed.

## AMENDMENT A3 result (2026-10-29): ng 64 at 10¹² — RESOLUTION-DEPENDENT (falls 33 %), still ABOVE WINDOW

The criteria are in `FROZEN_CRITERIA.md` A3 (54c45e963e). All nine ng 64 seeds finished (N = 57 777). Files:
`x48_analyze_ng64_A3.out`, `x48_grade_A3.*`, and `x48_regrade_A3mixed.*` (reported only).

| 10¹² | c_f median (68 % bootstrap) | NFW-fit median |
|---|---|---|
| ng 48 (A2) | 11.63 (8.37–12.74) | 7.10 |
| **ng 64 (A3)** | **7.74** (6.10–9.24) | 7.75 |

**Frozen labels:**
- **Window:** ABOVE WINDOW ([3.3, 4.6]).
- **Resolution:** **RESOLUTION-DEPENDENT (falls)**, a median shift of −33 %. Convergence beyond ng 64 is not tested.

**r₋₂ against r_conv:**
- Five seeds (2, 4, 5, 6, 8) had r₋₂ ≤ 2 r_conv at ng 48. At ng 64, r_conv fell to ≈ 0.004 Mpc (the 3ε floor) and
  **none of those seeds stays pinned** (r₋₂/r_conv 2.2–7.4). Verdict: DOES NOT TRACK r_conv.
- Their median fell from 13.08 to 9.24. The other four seeds fell from 6.25 to 4.62.
- So the pinned ng 48 values were resolution-inflated. At ng 64 the slope crossing is resolved.
- Caveat: the constrained field is redrawn on each grid, so per-seed shifts mix resolution with realisation.

**Reported regrade** (10¹² at ng 64; 10¹³ and 10¹⁴ still at ng 48):
- **SPARC line passes again:** 0.0652 @ Υ 0.59 (canonical), 0.0659 @ 0.51 (alt).
- **Groups pass:** Z +1.41.
- **Clusters fail:** G-IN-all, G-MID-T1 and G-IN-Mall, all OVER.
- The cluster masses are still at ng 48, where c_f is probably inflated too. **The test this points to is ng 64 at 10¹³
  and 10¹⁴.**

κ = ½ FITTED. Not theory closed.

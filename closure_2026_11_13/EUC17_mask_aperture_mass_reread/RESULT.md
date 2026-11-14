# EUC17 (MASK-APERTURE STELLAR MASS, EUCLID LENS ROWS RE-READ): RESULT

2026-11-13. Criteria 8b31c449c9 (alone, before any mask file or number). Amendment A1 e3db93ac26 (alone, before any
number). As-frozen run 0fc36cf7bc. Amendment A2 aaa56c6789 (alone, POST HOC).

## Verdict

**As frozen: NOT EVALUABLE.** Check K0 failed on one number: the upper bootstrap bound of f₂₅ for the EUC10
reading (11 lenses; 0.818 against the committed 0.909, a step of one lens in eleven). That reading carries no
word. Every point value, every other bound and every committed word of every row reproduced. The cause is a design
error in the check (a 0.01 tolerance on the bound of a fraction that moves in steps of 1/11), not a difference in
any statistic.

**Under A2 (POST HOC; the check's tolerance repaired, one script error corrected), law S, canonical / alt:**

| Row | Committed word | Word with the in-mask mass | Label |
|---|---|---|---|
| **R1** EUC1: 3,192 grade-A lenses, source at infinity | NO VERDICT / NO VERDICT | **CEILING HOLDS / CEILING HOLDS** | CHANGED, ROBUST |
| **R2** EUC4: 124 wide grade-B lenses (θ_E ≥ 1.7″), source at infinity | WIDE LENSES BREAK THE CEILING / same | **WIDE LENSES BREAK THE CEILING / same** | UNCHANGED, ROBUST |
| **R3** EUC1-F on EUC16's 11 certified source redshifts | NO VERDICT / NO VERDICT | **NO VERDICT / NO VERDICT** | UNCHANGED, ROBUST |

In plain words. The Euclid catalogue's stellar mass is the mass inside the modelling circle, and EUC1 and the lanes
built on it spread that mass over an infinite Sérsic body, so they counted too few stars inside every Einstein
radius. Putting the catalogued mass where the catalogue says it is lowers the boost the law needs by a median
0.071 dex on the main sample and 0.132 dex on the wide lenses.

- **The wide-lens fail stands.** 44 % / 38 % of the wide grade-B lenses still need more than 1.78 × their Salpeter
  stars with the source at infinity (line 25 %; was 76 % / 70 %). The median need falls from 2.3 × / 2.2 × to
  1.66 × / 1.57 ×. The fail survives every bracket; its closest approach to the line is a lower bound of 0.258
  (alt, bracket F1b).
- **EUC1 moves from NO VERDICT to CEILING HOLDS** on both footings: 6.0 % / 5.0 % of lenses above the margin, below
  the 10 % contamination floor (was 15.6 % / 13.9 %). By EUC1's own criteria this is **not a pass**: it says only
  that the sample does not exclude "law + Salpeter stars" when every source is infinitely far away. With sources at
  z_s ≈ 2 the would-be word is still CEILING BROKEN (27 %, alt). Recorded as a hit awaiting a blind re-grade.
- **The EUC1-F gate stays NO VERDICT.** The median boost on the 11 certified lenses falls from +0.405 / +0.385 to
  **+0.192 [+0.079, +0.338] / +0.174 [+0.061, +0.322]**. The point value was above the FAILS line (0.25); it is now
  between the lines (0.15 and 0.25). Eleven lenses cannot decide it either way.

κ = ½ FITTED. Footings never pooled. Adopts nothing; no ledger or scorecard edited; no outcome here is a pass of the
lensing gate.

## 1. The numbers (A2, primary f)

| Row, footing | Committed | With the in-mask mass |
|---|---|---|
| R1 f₂₅, canonical | 0.156 [0.143, 0.168] | 0.060 [0.052, 0.068] |
| R1 f₂₅, alt | 0.139 [0.127, 0.151] | 0.050 [0.043, 0.058] |
| R1 b_med, canonical / alt | −0.019 / −0.044 | −0.104 / −0.130 |
| R1 f₀ (need more than Salpeter), canonical / alt | 0.472 / 0.436 | 0.313 / 0.273 |
| R2 f₂₅, canonical | 0.758 [0.677, 0.831] | 0.444 [0.355, 0.524] |
| R2 f₂₅, alt | 0.702 [0.621, 0.774] | 0.379 [0.298, 0.460] |
| R2 b_med, canonical / alt | +0.364 / +0.343 | +0.221 / +0.197 |
| R3 b_med, canonical (N = 11) | +0.405 [+0.137, +0.589] | +0.192 [+0.079, +0.338] |
| R3 b_med, alt (N = 11) | +0.385 [+0.121, +0.574] | +0.174 [+0.061, +0.322] |

Every lens of R1, R2 and R3 has a mask record (no lens dropped).

**Reported, no word.**
- Law B: R1 0.092 [0.082, 0.102] canonical (NO VERDICT: the upper bound is 0.102) and 0.079 [0.069, 0.088] alt
  (CEILING HOLDS); R2 0.556 / 0.516, WIDE LENSES BREAK THE CEILING on both.
- EUC1's conditional readings, alt footing: sources at z_s = 3, f₂₅ 0.296 → 0.149 [0.136, 0.161], would-be word
  CEILING BROKEN → NO VERDICT; sources at z_s ≈ 2, 0.435 → 0.272 [0.257, 0.287], would-be word CEILING BROKEN →
  CEILING BROKEN.
- EUC10's reading on its 11 matched lenses with published source redshifts: b_med +0.543 → +0.337 [+0.079, +0.576]
  canonical, +0.526 → +0.320 [+0.062, +0.560] alt; f₂₅ 0.73 → 0.55. Its EUC1-F line has N = 2 and stays NOT
  EVALUABLE.
- EUC4's secondary (1.3–1.7″) and complement (< 1.0″) bins: **not evaluable here.** The frozen download list did not
  include those lenses (4 of 292 and 23 of 2,045 have a mask). Their committed numbers reproduce with f = 1.

## 2. Brackets (law S, canonical / alt)

| Bracket | R1 f₂₅ | R2 f₂₅ (lower bounds) | R3 b_med |
|---|---|---|---|
| primary | 0.060 / 0.050 | 0.444 / 0.379 (0.355 / 0.298) | +0.192 / +0.174 |
| F1a f with R_e × 0.80 | 0.075 / 0.058 | 0.492 / 0.444 (0.403 / 0.355) | +0.224 / +0.206 |
| F1b f with R_e × 1.25 | 0.051 / 0.044 | 0.387 / 0.339 (0.298 / **0.258**) | +0.157 / +0.139 |
| F2 f with n = 4 | 0.069 / 0.055 | 0.460 / 0.403 (0.371 / 0.315) | +0.199 / +0.180 |
| F3a mask radius + offset | 0.062 / 0.052 | 0.452 / 0.403 (0.363 / 0.323) | +0.201 / +0.183 |
| F3b mask radius − offset | 0.058 / 0.048 | 0.419 / 0.363 (0.331 / 0.282) | +0.182 / +0.164 |
| F4 no-mask lenses at f = 1 | 0.060 / 0.050 | 0.444 / 0.379 | +0.192 / +0.174 |
| F5 n > 9.5 dropped | 0.054 / 0.044 (N 2,919) | 0.422 / 0.367 (N 109; 0.330 / 0.275) | +0.182 / +0.165 (N 10) |

No bracket changes a word, so every row is ROBUST. R1's largest upper bound is 0.085 (F1a, canonical) against the
0.10 line. R3's interval always straddles both lines.

## 3. Checks

| Check | As frozen | Under A2 |
|---|---|---|
| K0 f = 1 reproduces every committed statistic and word | **FAIL** (one bound, EUC10 reading, 1/11) | PASS |
| K0b computed boosts against the four-decimal files | PASS (5.0e-5; limit 6e-5) | PASS |
| K1 share function (0.5 at R_e; n = 1 closed form) | PASS (2.9e-7; 5.6e-17) | PASS |
| K2 shift identity b(M★/f) = b + log₁₀ f, 20 lenses, laws S and B | PASS (1.8e-14) | PASS |
| K3 mask radius > 0, f in (0, 1] | PASS (f 0.181 to 1.000; no mask smaller than its Einstein radius) | PASS |
| K4 premise spot-check on FOR J0332 | PASS | PASS |
| Twin nomask (f = 1: every committed word comes back) | exits 1 | not re-run |
| Twin invert (shift reversed: f₂₅ and b_med rise) | exits 1 (R1 canonical turns CEILING BROKEN) | not re-run |

**K4 in full.** On FOR J0332 the released unconvolved lens-light map has no non-zero pixel outside the mask circle.
Its sum equals the catalogue's lens flux to 1.1 % in VIS and to between −1.2 % and +0.01 % in the seven other
bands. The analytic total of the same Sérsic model is 1.266 × the catalogue flux, so the in-mask share is 0.79,
matching the geometric share (0.80 to 0.82). The catalogue flux is the in-mask sum on this lens. (If the released
radius were a major-axis radius the analytic total would be only 1.03 × the catalogue flux; that reading is
inconsistent with the geometric share and with the released library's convention.)

**K5 (reported).** f = 0.822 for FOR J0332 and 0.637 for L015780 here (circular model, catalogue shape), against the
other agent's 0.804 and 0.587 (elliptical model, best-fit shape, model centre). The circular share gives the smaller
correction on both.

**Script error in the as-frozen run.** Bracket F5 was passed through the 5 % "no mask" rule, which is for lenses
without a mask file. Every row therefore printed FRAGILE (F5). The words before that rule are in the as-frozen
results file and equal the primary words. A2 applies the rule as the criteria state it. With the `--A2` flag off the
script reproduces the as-frozen outputs byte for byte.

## 4. How large the correction is, and the frozen guard S1

| Sample | Median −log₁₀ f (dex) | 16–84 % |
|---|---|---|
| P, all 3,192 | 0.071 | 0.010 to 0.174 |
| P, θ_E < 1.0″ (1,948) | 0.050 | 0.005 to 0.149 |
| P, 1.0–1.3″ (691) | 0.084 | 0.025 to 0.186 |
| P, 1.3–1.7″ (361) | 0.121 | 0.045 to 0.218 |
| P, ≥ 1.7″ (192) | 0.147 | 0.074 to 0.266 |
| W_B (124) | 0.132 | 0.063 to 0.257 |

37 % of P is corrected by more than 0.10 dex and 12 % by more than 0.20 dex. The 11 lenses of R3 range from 0.031 to
0.288 dex; two of EUC10's lenses reach 0.56 dex.

**What S1 requires this file to say.** EUC12 found that the uncorrected ECLIPSE scale already agrees with Auger 2009
and DESI CIGALE to about 0.05 dex. The corrected scale therefore sits about 0.07 dex above those scales for a
typical lens and 0.13 to 0.15 dex above them for wide lenses. That is a reason to doubt the extrapolated wings of
the Sérsic model, most of all for wide, high-index lenses. It does not touch the mass inside the mask, which is the
catalogued mass by definition. Why two catalogues built on total magnitudes agree with an in-mask mass is not
explained here; EUC12 is not re-read.

## 5. Post hoc reading T: stars beyond the mask removed (A2 §3; sets no label)

The corrected body with every star beyond the sphere of the mask radius removed. KT1 2.2e-14, KT2 6.0e-5: both pass.

| Row | Primary | T (wings removed) | Median change in b |
|---|---|---|---|
| R1 f₂₅ | 0.060 / 0.050 | 0.063 / 0.053 | +0.003 / +0.004 dex |
| R2 f₂₅ | 0.444 / 0.379 | 0.460 / 0.411 | +0.010 / +0.011 dex |
| R3 b_med | +0.192 / +0.174 | +0.201 / +0.184 | +0.005 / +0.005 dex |

Every word under T equals the primary corrected word. The corrected numbers do not rest on stars beyond the region
where light was measured: what moves the rows is the mass inside the mask.

## 6. Limits

- **The premise was tested on one lens** (K4). The paper's text is explicit, and the released map of that lens is
  zero outside the mask, but no other lens's maps were fetched. If the released masses were infinite-profile totals,
  every corrected number here would be void.
- **One direction only.** f ≤ 1, so the correction can only lower b. The lines, the 0.25 dex margin and the samples
  are as their lanes froze them.
- **R1's new word is the weak one.** It holds only with every source at infinity. No source-redshift reading of this
  lane favours the law: z_s ≈ 2 still reads CEILING BROKEN as a would-be word, and the gate on real source
  redshifts (R3) has 11 lenses and no verdict.
- **A circular model stands in for the elliptical one**, centred on the lens. Brackets F1 and F3 cover the radius
  convention and the mask offset; a per-lens elliptical share needs each lens's model parameters.
- **No blind re-grade exists.** One word changed (R1), so EUC17R is owed. Not launched here.
- **Not re-read:** EUC4R, EUC5 / EUC5R, EUC6, EUC7, EUC8, EUC12, EUC13 / EUC13R, LNJ1, ESZ1, EXR1 / EXR2. All take
  the catalogue mass as a total. The mask table committed here (`euc17_masks.csv`) lets each be re-read. CJ1's row
  39 is not edited by this lane.

## 7. Files and re-run

- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `AMENDMENT_A2.md`.
- `euc17_fetch.py`, `euc17_fetch.out`, `euc17_masks.csv` (3,366 lenses; 3,357 with a mask; the 9 without have no
  tile id in the key catalogue and are in no graded row). 3,352 requests, 434,659 bytes, one paced stream. Raw
  records outside git with a manifest.
- `euc17.py`; as frozen: `euc17.out`, `euc17_results.json`, `euc17_per_lens.csv`; twins `euc17_MUTATE_nomask.*`,
  `euc17_MUTATE_invert.*`; A2: `euc17_A2.out`, `euc17_A2_results.json`.
- `euc17_posthoc_T.py`, `.out`, `.json`.
- K4 reads the released FOR J0332 inputs under `euclid_for_j0332_fit_2026_11_13/inputs/`, which are on branch
  `codex/euclid-desi-handoff-2026-11-13` (commit dc5b24fe6f) and not on main.

```
python3 -I euc17.py --data-dir <dir with the two ECLIPSE csv files>            # as frozen, exits 2
python3 -I euc17.py --data-dir <dir> --A2                                      # A2 reading, exits 0
EUC17_MUTATE=nomask python3 -I euc17.py --data-dir <dir>                       # exits 1
EUC17_MUTATE=invert python3 -I euc17.py --data-dir <dir>                       # exits 1
python3 -I euc17_posthoc_T.py --data-dir <dir>                                 # exits 0
```

Run by the session that wrote the lane; the as-frozen outputs were reproduced byte for byte after the `--A2` flag
was added. A reproduction, not an independent re-grade.

## 8. Commit ids (local / origin)

| Step | Local | Origin |
|---|---|---|
| Frozen criteria | 8b31c449c9 | 9667471bdb |
| Amendment A1 | e3db93ac26 | 85813a7ba2 |
| Script, mask fetch, as-frozen run, twins | 0fc36cf7bc | d06473eb24 |
| Amendment A2 (post hoc) | aaa56c6789 | c55c7dd7de |
| A2 reading and reading T | 5c31c63589 | 248127c815 |
| This result | 26601d1bf6 | e839856ff6 |

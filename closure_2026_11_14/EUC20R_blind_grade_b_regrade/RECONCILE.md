# EUC20R against EUC20: reconciliation

Written after this lane's blind result was committed (c05ae562b1; reading note 025dc97b73). Only then was EUC20's
`RESULT.md` opened. No EUC20 script or output file was opened for this comparison; numbers attributed to EUC20 below
are quoted from its `RESULT.md`. κ = ½ FITTED; not theory closed. Adopts nothing.

## Labels: full agreement

| Row | Footing | EUC20 (lead) | EUC20R (blind) |
|---|---|---|---|
| G1 | canonical | NO VERDICT, CHANGED, ROBUST | NO VERDICT, CHANGED, ROBUST |
| G1 | alt | NO VERDICT, CHANGED, ROBUST | NO VERDICT, CHANGED, ROBUST |
| G2 | canonical | SLOPE NOT CONSTRAINED, UNCHANGED, ROBUST | SLOPE NOT CONSTRAINED, UNCHANGED, ROBUST |
| G2 | alt | SLOPE NOT CONSTRAINED, UNCHANGED, ROBUST | SLOPE NOT CONSTRAINED, UNCHANGED, ROBUST |
| G3 | canonical | NO SWITCH, FRAGILE; CHANGED, ROBUST | NO SWITCH, FRAGILE; CHANGED, ROBUST |
| G3 | alt | NO SWITCH, FRAGILE; CHANGED, FRAGILE | NO SWITCH, FRAGILE; CHANGED, FRAGILE |

Six of six agree, including the fragility tags (alt G3 FRAGILE because F1a leaves 15 lenses above the boundary and
reads NO POWER, in both lanes). Every check passed in both lanes; both ran the invert twin, which fired.

## Numbers: agreement to the printed digit

- **G1** secondary bin: f₂₅ 0.182 [0.140, 0.226] / 0.154 [0.113, 0.199], b_med +0.071 / +0.047, median correction
  0.108 dex; brackets F1a 0.202 / 0.188 and F1b 0.151 / 0.123; law B 0.243 / 0.223. Identical in both.
- **Other bins**: complement 0.055 / 0.051 (would-be NOT CONFIRMED / NOT CONFIRMED), W_B 0.444 / 0.379, corrections
  0.036 and 0.132 dex. Identical.
- **G3 / LNJ1**: 108 / 6,065 and 22 / 6,151 lenses above / below the boundary; band shares 0.058 / 0.046 and 0.052 /
  0.000; the differing bracket words (canonical: measured rule NO POWER, AGEL JOINT UNDER-PREDICTS; alt: those two and
  catalogue scale NO POWER); AGEL 50 of 50 and 47 of 50. Identical.
- **H2 / H3**: EUC8 fails exactly K1, K5 (K1 0.444 / 0.379; K5 +0.200 → +0.005); LNJ1 fails exactly KA-1, KA-2 (P
  0.060 / 0.050; KA-2 +0.152 / +0.134). Identical.
- **H0**: the same files reproduced byte for byte in both lanes (EUC8 three files, EUC5 A1 two, LNJ1 eight), each log
  differing only in its elapsed-time line; the EUC4 bins exact.
- **EUC8 Part A** shares, all classes, both cases and footings (for example W far 0.451 → 0.294 / 0.421 → 0.258;
  1.3–1.7″ central 0.376 / 0.349). Identical.
- **EUC8 Part B**: EUC20 quotes the compact family's widened far upper bound −0.044 / −0.012 (was −0.214 / −0.186)
  and γ̂ (far, canonical) 2.19 [1.73, 2.30] → 0.20 [<0, 2.24]. This lane did not print those in its RESULT but its
  runs give exactly those values at b★ = 0 (`runs/primary/euc8/euc8_results.json`, `runs/f1/euc8/...`). This lane's
  RESULT reports the two trigger families instead (T's far bound +0.021 / +0.009 / −0.001; γ = 0's near bound), which
  EUC20 does not; both lead to the same word.
- **EUC5 A1**: b_dyn by sample and class, and b_dyn − b_∞ unchanged (+0.103 / +0.119). Identical.

## Where the lanes differ, and why

1. **EUC6 pair set (reading only; same conclusion).** EUC20 uses 249 pairs and compares the worth with a paired
   excess of +3.49 on those pairs; this lane uses EUC6's 243 pairs (EUC6's own coverage rule drops six pairs whose
   background count is below 40 % of the median) and compares with EUC6's +3.38. Numbers: median corrected mass
   difference +0.068 [+0.050, +0.097] (EUC20) against +0.070 [+0.050, +0.097] (here); slope +4.6 [−1.6, +9.4]
   against 4.68 [−1.29, +9.44]; worth +0.31 [−0.12, +0.70] against +0.33 [−0.09, +0.74] galaxies. Checked here: the
   249 complete pairs before EUC6's coverage drop have median D +3.49, so EUC20's set is that one. The criteria refer
   to "EUC6's excess (+3.38 galaxies)", which is the 243-pair number, so this lane's set matches the criteria more
   closely; either way the worth is about a tenth of the excess and both lanes conclude that EUC6 does not need a
   re-matched control set on this account. (Neither lane's "small part" line is frozen: EUC20 says "a small part",
   this lane fixed one third in its reading note before computing.)
2. **How G2's word is taken.** EUC20's collector first printed G2 as NOT EVALUABLE by reading EUC8's own gated
   `verdict` field, then corrected itself to EUC8's Part B rule on the family words and disclosed it. This lane fixed
   that reading in `READING.md` before any run (the source's printed line is not the row's word under H2), so it has no
   first-run discrepancy. Same word.
3. **Twin bookkeeping.** EUC20 runs separate invert twins per route (each exits 1); this lane checks all twin items in
   one collector call that exits 1. Same items fire (W far excess, A1 b_dyn, G1 f₂₅); this lane additionally requires
   the A1 rise on both sample P and sample S.
4. **Limits stated.** EUC20 notes that G3's change comes from membership (the model-rule speed rises with the
   stellar mass) and that LNJ1's measured-speed rule still reads NO POWER; this lane notes in addition that LNJ1's
   primary adds EUC12's common-scale constant measured on the uncorrected catalogue, which was not re-derived. These
   are compatible.

## Standing

EUC20's two changed words (G1 toward the law on a secondary bin; G3 a sharper negative for the crossing-speed joint's
switch, NOT ADOPTED) are reproduced by an independent blind implementation, with the same fragility. The blind
re-grade EUC20 owed is this one. No outcome is a pass of the lensing gate; the premise (catalogue mass = in-mask mass)
rests on the paper's text and one lens, as in EUC17.

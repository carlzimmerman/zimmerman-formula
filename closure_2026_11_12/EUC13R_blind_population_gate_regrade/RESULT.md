# EUC13R (BLIND RE-GRADE OF EUC13, POPULATION SOURCE GATE): RESULT

2026-11-12. READING 865ef2116c (alone) -> code and runs f02d4bda1d -> RESULT_BLIND 5ab93fa25d -> this file, written
after opening EUC13's AMENDMENT_A1, RESULT, RERUN_AND_IDS and outputs. TEST lane. kappa = 1/2 FITTED; not theory
closed. Adopts nothing. Footings canonical / alt, never pooled.

## Verdict

- **Blind words: EUC13-P NO VERDICT / NO VERDICT; f25 CEILING BROKEN / CEILING BROKEN.**
- **Comparison: AGREES WITH DIFFERENCES THAT DO NOT MOVE A LABEL** (gate word, f25 word, every member's point and
  interval within 0.004, the same surviving forward-model setting). One reading label differs by an ambiguity in the
  criteria, not by the data (§3). EUC13 is not relabelled.

A population gate grades modelled or borrowed source populations, not measured sources, and is weaker evidence than
EUC1-F, which stays open. No outcome here is a pass of the theory. The blindness was incomplete: EUC13's two words were
visible in a commit subject at session start (READING §0); every number was recomputed by code written here from the
criteria text, with my own lensing machinery, sample selection, table parsing, COSMOS counts and draws.

## 1. Numbers side by side (b_med, 95 % recentred interval; EUC13R | EUC13)

| member | canonical | alt |
|---|---|---|
| M1 AGEL | +0.237 [+0.215, +0.264] \| +0.238 [+0.213, +0.265] | +0.219 [+0.195, +0.246] \| +0.220 [+0.195, +0.247] |
| M2 SLF IV | +0.299 [+0.256, +0.341] \| +0.298 [+0.253, +0.346] | +0.282 [+0.231, +0.332] \| +0.281 [+0.235, +0.330] |
| M3 mu10 full | +0.234 [+0.220, +0.248] \| +0.233 [+0.219, +0.244] | +0.214 [+0.202, +0.227] \| +0.215 [+0.202, +0.227] |
| M3 mu10 sis | +0.222 [+0.210, +0.234] \| +0.222 [+0.208, +0.233] | +0.204 [+0.192, +0.216] \| +0.204 [+0.191, +0.217] |
| M3 envelope | [+0.210, +0.248] \| [+0.208, +0.244] | [+0.192, +0.227] \| [+0.191, +0.227] |

f25 (EUC13R | EUC13): M1 0.477 [0.440, 0.515] | 0.479 [0.443, 0.519] and 0.449 [0.412, 0.492] | 0.451 [0.415,
0.491]; M2 0.577 [0.516, 0.638] | 0.576 [0.512, 0.645] and 0.549 [0.477, 0.619] | 0.549 [0.480, 0.615]; M3 envelope
[0.436, 0.495] | [0.437, 0.489] and [0.407, 0.462] | [0.408, 0.462]. Median z_s on P: M1 2.06 | 2.05, M2 1.60 | 1.60,
M3 full 2.18 | 2.17, sis 2.28 | 2.27.

Gate logic, both lanes: no upper bound <= 0.15; AGEL's and M3's lower bounds < 0.25 (M2 canonical's 0.256 | 0.253
clears it, alone): NO VERDICT. Every f25 lower bound >= 0.40: CEILING BROKEN.

## 2. Member by member

- **M1 AGEL: AGREES.** My parse of the LaTeX (rule A1: main arc, source flag >= 2, any deflector redshift) gives 94
  systems, not EUC10's 90; after RESULT_BLIND I diffed against EUC10's sample file: the extra four (AGEL085331,
  AGEL144133, AGEL211627, AGEL221912) are systems whose deflector redshift has no flag or flag 1, which EUC10 left
  out; no row differs in value. KA3 by the direct path: +0.2371 / +0.2189 against +0.238 / +0.220 (within 0.002).
- **M2 SLF IV: AGREES.** 51 systems, not 49; the extra two are DESI J033.8095-29.1570 (lens z 0.9 at Q_z 3) and DESI
  J345.8606+23.4757. KA3 +0.2986 / +0.2817 against +0.298 / +0.282. Interval widths agree to 0.005.
- **M3: AGREES.** Same survivor (mu 10; mu 3 and mu marginal fail V1 in both lanes: mixture medians 0.972 | 0.962 and
  1.103 | 1.074 against the observed 1.434; mu 10 1.288 | 1.266, KS p 0.106 | 0.104). V1 used 49 | 47 systems (my two
  extra M2 systems both carry magnitudes).
- **Validation V2: DIFFERS in path, not in outcome.** EUC13 evaluated 8 ECLIPSE lenses from EUC10's 17-entry list and
  V2 passed for mu 10 (KS p 0.105, PIT 7 of 8 above 0.5). Blind to that list, I matched AGEL, SLF IV and SLACS myself
  and found 8 lenses, 4 evaluable (all 4 are in EUC13's 8), so V2 was not applied and mu 10 survived on V1 alone.
  EUC13's warning that the known ECLIPSE sources lie lower than M3 predicts (which would push b_med up, towards M2) is
  therefore not tested here.
- **Bounding readings: AGREE in size.** Frozen text asks for B fixed at b = 0 and 0.5 with mu marginal; I ran it as
  frozen: +0.274 / +0.281 against +0.277 self-consistent (canonical). EUC13 ran it post hoc at mu 10 (A1): +0.232 /
  +0.237 against +0.233. Either way the lens-mass dependence of the weight moves b_med by <= 0.004.
- **Self-consistent boost:** my third-iteration change 0.024 (mu 10) | EUC13 0.017; neither converged further.

## 3. theta_E classes: same numbers, one reading rule differs

Class values agree within 0.003 (e.g. canonical M2: +0.232 | +0.231, +0.333 | +0.333, +0.493 | +0.496; M3 full:
+0.157 | +0.157, +0.275 | +0.276, +0.455 | +0.454). The criteria say "inside / above / below" without saying whether
the point or the interval is placed. I placed the point; EUC13's code (`band word`, euc13.py lines 200-202) calls a
class "inside" if its interval overlaps the band. With the same rule the labels match. With mine, M2 reads **above** in
< 1.0 arcsec (+0.232 > 0.22 canonical; +0.215 > 0.21 alt) and in 1.0-1.3 canonical (+0.333 > 0.30); EUC13's own M2
points are on the same side of those edges. So the RERUN note's line "the 2,639 below 1.3 arcsec sit inside their
sealed bands in every member" holds under the overlap rule only. Wide lenses (>= 1.3 arcsec) are above their band in
every member and footing under either rule (+0.43 to +0.50).

## 4. Checks, both lanes

All pass in both. KA1 +0.0826 / +0.0693 | +0.0815 / +0.0696; KA2 -0.0185 / -0.0439 | the same; KA5 8.5e-5 | 1.5e-4;
KA6 1.017 from raw rows | 0.994 from the binned table (the lead's rebuild also gives 1.017 from raw rows). COSMOS grid
713,373 | 713,374 galaxies: one galaxy at exactly i = 28.0, which I excluded (m < 28) and EUC13 kept; it lies beyond the
27.5 clamp and enters no number. Mutation twin: every member rises on both footings in both lanes (M1 +0.237 -> +0.346
| +0.238 -> +0.347; M3 full +0.234 -> +0.349 | +0.233 -> +0.349); exit 1 in both.

## 5. Differences that do not move a label, and their causes

1. Raw replicate percentiles: EUC13's sit 0.01-0.02 above its points; mine sit 0 to 0.006 below. Both recentre, and the
   recentred bounds agree within 0.004. Likely cause: different error models for EUC1's run 6 (I used symmetric
   half-widths, z floored at 0.05); not traced, EUC13's error code not read line by line.
2. Sample parse 94 / 51 vs 90 / 49 (§2); KA3 passes anyway.
3. V2 path (§2). 4. Bounding-reading setting (§2). 5. One lens dropped in my mu 3 settings (empty n(z | arc)).

## 6. Exposure and limits

Seen before RESULT_BLIND: EUC13's two words (commit subject); the memory-index lines on EUC1 and EUC3 quoted in
READING §0; EUC13's fetch MANIFEST. Opened after RESULT_BLIND: EUC13's AMENDMENT_A1, RESULT, RERUN_AND_IDS,
euc13_results.json, the band rule in euc13.py, its counts table header, and EUC10's euc10_partB_samples.csv (to
explain the N difference). Unverified: the cause of difference 1; whether EUC13's V2 list is right (I could not build
it blind). Not done: a member from Euclid's own photometric source redshifts.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.

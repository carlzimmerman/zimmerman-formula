# EUC16 (BETTER ARC FINDER, PREDICTED-SPLIT SOURCE REDSHIFTS): RESULT

2026-11-13. Criteria 33df43d883 (alone, before any arc from the new finder met any spectrum). Second attempt at gate
EUC1-F after EUC15 (N(P) = 5); one finder frozen; no third attempt in this lane.

## Verdict: NO VERDICT / NO VERDICT (canonical / alt). EUC1-F graded for the first time, at tier TB (frozen fallback).

**N(P) = 11** certified source redshifts (EUC1-F needs 10; EUC15 had 5). Median b, law S: **+0.405 [+0.137, +0.589]**
canonical, **+0.385 [+0.121, +0.574]** alt. Neither line is crossed on either footing: the upper bound is far above 0.15
(no HOLDS) and the lower bound is below 0.25 (no FAILS). All four line-identity readings give the same word. All checks
pass, K8 shows the copied code reproduces EUC15 exactly, and both twins exit 1. The point value sits above the FAILS
line, but the interval is too wide to decide. κ = ½ FITTED. No outcome favours the framework.

## 1. Counts at each stage

| | usable spectrum | VIS box | arc found | median arc radius / θ_E | **evaluable** | SECURE TA | **SECURE TB** |
|---|---|---|---|---|---|---|---|
| S | 2,260 | 2,260 | 2,259 | 1.18 (EUC15 0.61) | **1,053** (EUC15 536) | 29 | **19** |
| X | 923 | 923 | 918 | 1.04 (0.62) | **350** (210) | 5 | **0** |
| P | 1,164 | 1,164 | 1,164 | 1.14 (0.71) | **578** (311) | 17 | **11** |

Checks K1 −0.0185 / −0.0439, K2 +0.2314 / +0.2149, K5, K6 19,030 of 19,033, K7 S and X, **K8** (EUC15's finder in this
code: coverage, every gate count, pre-guard count and N(P) = 5 identical), C1: all pass. Injections into 300 evaluable S:
I1 272 (90.7 %), I2 1 (0.3 %), I3 0. **Twins:** newton exits 1 (anchor +0.330 / +0.330 against +0.231 / +0.215; P
rose on both footings); nowindow exits 1 (pre-guard TA pairs 203 → 828).

## 2. Gates (limits scaled to the new evaluable counts by EUC14's formulas)

| Tier | P | S (rate) | X (limit) | rotated 90°, S (limit) | sign-flipped S (limit) | mirrored S | truth | |
|---|---|---|---|---|---|---|---|---|
| TA | 17 | 29 (2.8 %) | **5 (1.9): FAIL** | 4 (5.8) | **8 (5.8): FAIL** | 14 | recovered | fails |
| TB | 11 | 19 (1.8 % [1.1, 2.8]) | 0 (1.3) | 1 (3.8) | 2 (3.8) | 2 | recovered | **all pass** |

As in EUC15, TA's thresholds admit noise (five grade-X single lines, two of them EUC14's L023203 and L026011). At TB
grade X gives 0 of 350 (95 % upper bound 1.05 %) against 1.8 % for lenses. Truth L015763: arc (−1.17, −1.10)″, z_s
1.3649, k 1.05, S/N 51.5; not independent (the finder's 0.03 was chosen partly to keep this arc, criteria §2b).

## 3. Certified lenses of P at TB (`figs/euc16_secure_*.png`)

| Lens | line | z_l | z_s | k | half-split | S/N | b canonical / alt | source-free b alt |
|---|---|---|---|---|---|---|---|---|
| L001890 (EUC15) | Hα, one line | 0.640 | 1.0363 | 1.20 | 1.30″ | 13.5 | +0.851 / +0.838 | +0.315 |
| L004747 | Hα + [S II] 3.4σ | 0.800 | 1.1792 | 0.80 | 0.75″ | 12.2 | +0.054 / +0.042 | −0.582 |
| L001520 (EUC15) | Hα, one line | 0.970 | 1.2292 | 1.00 | 0.69″ | 13.0 | +0.688 / +0.679 | −0.162 |
| L006510 | Hα, one line | 0.630 | 1.5129 | 0.90 | 1.22″ | 8.1 | +0.419 / +0.401 | +0.089 |
| L001449 (EUC15) | Hα, one line | 0.860 | 1.5782 | 1.25 | 0.90″ | 14.9 | +0.589 / +0.574 | +0.117 |
| L017181 | [O III] + 4960 3.6σ | 0.840 | 1.7079 | 0.85 | 0.76″ | 18.2 | +0.137 / +0.121 | −0.271 |
| L001874 | Hα + [O III] 6.7σ, Hβ 3.1σ | 0.340 | 1.7711 | 1.00 | 1.10″ | 13.0 | +0.252 / +0.234 | +0.112 |
| L016344 | Hα, one line | 0.320 | 1.8324 | 1.10 | 1.36″ | 11.7 | +0.135 / +0.117 | +0.007 |
| L004690 | [O III] + 4960 4.1σ | 0.890 | 2.1360 | 1.15 | 0.82″ | 9.5 | +0.480 / +0.462 | +0.135 |
| L012745 (EUC15) | [O III] + 4960 5.5σ | 0.350 | 2.1855 | 1.05 | 2.63″ | 14.2 | +0.405 / +0.385 | +0.282 |
| L001971 (EUC15) | [O III] + 4960 8.3σ | 1.060 | 2.4677 | 0.90 | 0.76″ | 29.3 | +0.151 / +0.134 | −0.210 |

**All five of EUC15's lenses are kept**, as the criteria (§5) expected; six are new. **5 of 11 rest on a single line.**
Also certified in S (grade B): L011473, L011858, L012019, L012253, L013774, L014252, L016686, L023035.

## 4. Readings (law S, P, N = 11; canonical / alt)

| | canonical | alt | word |
|---|---|---|---|
| single lines as Hα (primary) | +0.405 [+0.137, +0.589] | +0.385 [+0.121, +0.574] | NO VERDICT / NO VERDICT |
| as [S III] 9533 | +0.405 [+0.151, +0.589] | +0.385 [+0.134, +0.574] | same |
| as [O III] 5008 | +0.271 [+0.137, +0.416] | +0.255 [+0.121, +0.396] | same |
| as [O II] 3727 | +0.246 [+0.117, +0.405] | +0.223 [+0.097, +0.385] | same |

S (N = 19, never the word): +0.177 [+0.135, +0.419] / +0.165 [+0.117, +0.401]. Robustness (reported): two-line classes
only (N = 6) +0.202 [+0.095, +0.443] / +0.184; with AMBIGUOUS-OWN (N = 35) +0.227 [+0.169, +0.392] / +0.210 [+0.151,
+0.374]; DESI deflector z unchanged. **Leave-one-out** (reported): lower bound +0.137 to +0.151 / +0.121 to +0.134,
upper bound +0.497 to +0.591 / +0.479 to +0.575. No single lens, identity or robustness row moves either bound across
its line; the word NO VERDICT is not fragile. A HOLDS would need the upper bound to fall by about 0.44.

## 5. Selection check (source-free b, law S, z_s at infinity)

Certified 11: median +0.116 / +0.089; all of P (3,192): −0.019 / −0.044. Their percentiles in P: 0.90, 0.72, 0.30,
0.16, 0.57, 0.76, 0.74, 0.88, 0.01, 0.23, 0.69 (mean 0.54). θ_E median 1.02″ against 0.90″; z_l median 0.80 against
0.66. **The certified few are spread across P but lean to larger θ_E and higher z_l, and their source-free median is
higher by about 0.13.** The reading describes lenses whose arc lies along their field's dispersion and shows a line,
not the median of P.

## 6. Disclosures

- **Second attempt** at the same gate after seeing EUC15's five and their b values; one finder frozen; no third attempt.
- The finder was chosen among ten on image-only evidence (criteria §2b). The model-mismatch fraction 0.03 is the largest
  of the tried values that keeps the truth arc, so it is partly fitted to the truth lens. No evaluable count,
  dither direction or spectrum flux was looked at before the freeze.
- `euc16.py` is a copy of EUC15's `main`, not an import; K8 shows the copy reproduces EUC15 to every count.
- No download or network fetch. One thread, `nice -n 10`. Derived image-evidence files outside git (`_external_data/.../euc16/`).

## 7. What this means

EUC1-F is graded for the first time and gives NO VERDICT / NO VERDICT: 11 lenses are too few, and five of them single
lines, to bound the median boost on either side. EUC1 stays NO VERDICT / NO VERDICT. A word needs many more certified
lenses (later releases with more roll angles) or follow-up source redshifts; this lane estimates no number.

## 8. Files

`FROZEN_CRITERIA.md`; `euc16_arc.py` (frozen finder), `euc16_finder_dev.py` + `euc16_finder_dev*.out` (image evidence);
`euc16.py`, `euc16_figs.py`; `euc16.out`, `euc16_results.json`, `euc16_sources.csv`, `euc16_CHECK_v1*`, `euc16_MUTATE_*`,
`figs/euc16_secure_*.png`. Commits: criteria 33df43d883; scripts and run 84c7b33eec.

    EUC16_FINDER=v1 python3 -I -B euc16.py --data-dir <dir>   (K8, then)   python3 -I -B euc16.py --data-dir <dir>
    EUC16_MUTATE=newton|nowindow python3 -I -B euc16.py --data-dir <dir>   (twins exit 1)

## 9. Commit ids and the lead's re-run (2026-11-13)

- Criteria 33df43d883 (origin e0a3eae0a6); scripts and run 84c7b33eec (origin ec4a708755); result 5ffd920204 (origin
  05c4d81dc7).
- The lead re-ran the lane from a copy at the same folder depth in its documented order (K8 check run, main run, both
  twins): the five JSON and CSV outputs equal byte for byte; the four logs differ only in the elapsed-seconds line; the
  twins exit 1. A first re-run that skipped the K8 check run was the lead's error and is discarded.
- A reproduction, not an independent re-grade. No number or label changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

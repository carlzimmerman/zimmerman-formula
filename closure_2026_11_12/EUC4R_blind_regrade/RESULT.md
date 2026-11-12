# EUC4R: blind re-grade; does not relabel EUC4

2026-11-12. Part A only. Protocol 63fcd55a56 (alone, before any code); blind script and outputs dfb9cd3a7e (before
EUC4's RESULT, code or outputs were opened); this file and `euc4r_compare.*` written after unblinding.

kappa = 1/2 FITTED. Footings never pooled. One-sided test: no outcome favours the framework. Not "theory closed".

## Word: WIDE LENSES BREAK THE CEILING / WIDE LENSES BREAK THE CEILING (canonical / alt). Same as EUC4.

On W_B (grade B, theta_E >= 1.7", N = 124), law S, source at infinity: f25 = **0.758 [0.677, 0.831]** canonical and
**0.702 [0.613, 0.782]** alt. EUC4's point values are identical (0.758 / 0.702: the same 94 and 87 lenses of 124).
The canonical interval is identical; the alt interval differs by one lens at each end (EUC4 [0.621, 0.774]). The cause is
the bootstrap generator's order (section 3), not the physics. The lower bounds sit 0.36-0.43 above the 0.25 line.

**Disclosed before the blind run:** EUC4's word (and EUC1's) was visible in commit subjects and in the memory index
before my protocol was written. No EUC4 number was seen. My numbers are blind; my word is not.

## 1. Bin by bin (law S, source at infinity)

| Sample | N (mine / EUC4) | f25 canonical: EUC4R / EUC4 | f25 alt: EUC4R / EUC4 | b_med can / alt (both) | Word (both) |
|---|---|---|---|---|---|
| **W_B, theta_E >= 1.7"** | 124 / 124 | 0.758 [0.677, 0.831] / same | 0.702 [0.613, 0.782] / 0.702 [0.621, 0.774] | +0.364 / +0.343 | BREAK / BREAK |
| Secondary, 1.3-1.7" | 292 / 292 | 0.425 [0.366, 0.479] / 0.425 [0.370, 0.479] | 0.380 [0.325, 0.435] / 0.380 [0.329, 0.435] | +0.207 / +0.182 | BREAK / BREAK (secondary) |
| Complement, < 1.0" | 2,045 / 2,045 | 0.092 [0.080, 0.105] / 0.092 [0.080, 0.105] | 0.082 [0.070, 0.093] / same | -0.101 / -0.127 | reported, no word |

Law B (beside it): W_B 0.831 / 0.798, identical point values; one non-word cell differs by one lens (complement, law B,
alt: 0.1086 mine, 0.1081 EUC4; section 3). b_med agrees to 1.3e-5 dex in every cell. Mutation twin (a0 -> 1e-30):
W_B f25 0.758 -> 0.968 and 0.702 -> 0.968, exit 1, as EUC4. EUC4's descriptive W_B medians (z_l 0.43, theta_E 1.99",
log M* 11.66, theta_E/theta_e 0.98, n 5.8), f0 (0.99), 2.3 x / 2.2 x Salpeter and the counts 192 of 3,192 (grade A) and
124 of 2,981 (grade B) all reproduce.

## 2. Checks

| Check | Result |
|---|---|
| sha256 of both CSVs against EUC1's frozen hashes | match |
| E2: identifiers shared by grade A (6,073) and grade B (8,999) | 0, no duplicates; key grade = object grade on 15,072/15,072 |
| Point mass at a0 -> 0 returns M | 5e-9 |
| g proportional to 1/r returns M_2D proportional to R | 1.9e-5 |
| Node doubling (256 -> 512 nodes) | b moves 4e-15 dex |
| Lenses at a bisection edge | 0 |
| E1' (comparison, not a gate): my f25 on EUC1's P | 0.1560 / 0.1388 against EUC1's 0.156 / 0.139 |
| MUTATE newton | f25 on W_B rises on both footings, exit 1 |

## 3. Every difference, traced (`euc4r_compare.py`, run after unblinding, imports both codes)

1. **Bootstrap intervals.** EUC4 creates one `default_rng(20261112)` and passes it through all twelve Part A statistics
   in order; I re-seed for each statistic (protocol §3.10). Feeding EUC1's `stats()` one shared generator in EUC4's order
   reproduces **all twelve** of EUC4's published intervals exactly; with a fresh generator it reproduces mine. Only
   W_B law S canonical, the first draw, sees the same stream in both, which is why it alone matches. Size: one lens
   (1/124 = 0.008 on W_B, 1/292 = 0.003 on the secondary bin).
2. **Per-lens b.** My b exceeds EUC1's machinery by at most 6.2e-5 dex (median 1.3e-5). Stepping my code toward EUC1's:
   the solar mass (A55's 1.98847e30 against my IAU 1.98841e30) gives exactly 1.31e-5 dex; the series b_n (Ciotti-Bertin)
   against my exact b_n gives the rest (up to 4.9e-5); distances (grid against quadrature) and the projection nodes
   (one 400-node panel against two 128-node panels) differ by < 1e-10. With all four switched the two codes agree to 0.
3. **One indicator flip,** outside the word: lens EUCL-DR1-L012001, complement bin, law B, alt, b = 0.250001 (mine)
   against 0.249988 (EUC1's code). That is the complement law B alt difference in section 1.

Nothing else differs: same samples (same identifiers in every bin), same cuts, same counts removed (n outside
0.6-10: 10 in grade A, 16 in grade B; nothing else removed).

## 4. Criteria ambiguities that could move a label

None found that does. Each one I fixed in the protocol, with its size on W_B:
- bootstrap generator and order: one lens per bound (above); a label is at risk only within ~0.01 of 0.25 or 0.10;
- exact or series b_n, solar-mass constant: <= 6.2e-5 dex per lens; one flip, in a non-word cell;
- bin edges (>= or >): no grade-B lens sits exactly at 1.0, 1.3 or 1.7";
- `large_system_warning` and the boolean flags: plain booleans, every key row matched, none blank;
- z_s = 1100 (written) against a literal infinity: at z_s = 1e6 W_B f25 falls to 0.750 / 0.694 [lower bounds 0.669 /
  0.605]. EUC1 §3's claim that Sigma_cr has converged to < 1 % by z_s = 1100 is not true for z_l >~ 1.4 (1.06 % at
  z_l = 1.5 against z_s = 1e4, with radiation neglected); immaterial here (W_B median z_l = 0.43), and b at z_s = 1100
  still bounds every real source from below;
- R_e circularisation and SIE against effective theta_E: input choices, not re-run here; EUC4's robustness gives
  0.669 / 0.629 and 0.744 / 0.696, both BREAK (EUC4's numbers, not verified by me).

The complement's law S canonical upper bound (0.1046 EUC4, 0.1051 mine) is the one bound near a threshold; the
complement carries no word.

## 5. What this re-grade does and does not establish

It establishes that EUC4's Part A numbers do not depend on an error in the shared `euc1.py`: code written from the
criteria text alone, with its own deprojection, distances, projection and solver, reproduces EUC4's per-lens b to
6e-5 dex, every point value to the last printed digit, and every interval once the generator order is matched.

It does not test what both codes take from the same criteria and catalogue: the spherical Prugniel-Simien stars-only
model, the catalogue's photometric redshifts, Salpeter masses and area-equivalent Einstein radii, or EUC4's robustness
runs, Part B and section 5 readings (not re-run). It does not relabel EUC4.

## 6. Files

`PROTOCOL.md`; `euc4r.py` with `euc4r.out`, `euc4r.json`, `euc4r_lenses.csv` (per-lens b, both laws and footings, for P
and the three grade-B bins) and the `_mutate_newton` twins (exit 1); `euc4r_compare.py` with `euc4r_compare.out` and
`euc4r_compare.json` (post-unblinding). Run: `python3 -I euc4r.py`, then `EUC4R_MUTATE=newton python3 -I euc4r.py`,
then `python3 -I euc4r_compare.py`.

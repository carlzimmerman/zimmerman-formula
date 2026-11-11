# DSB1: the hosted dwarf classes under form B with a full systematics budget frozen blind. Frozen reading STOPPED AT KA-c; amended reading NO POWER (every graded class, both footings)

TEST lane. It relabels nothing, registers nothing, and changes no label of RB2, DG1, SE2, XF1, X1 or S1. Cold dark energy
is a gravitating field component, never a particle. Footings canonical (a0 9.3603e-11) / alt (1.1312e-10), never pooled.

## Labels (unchanged from the blind files)

- **Frozen reading** (criteria 2c7beb7b92): **STOPPED AT KA-c, no label** (RESULT_BLIND.md, 8e189b5326). The planted-offset
  recovery line could not pass because one budget term (T10, binaries in 4-10 km/s systems) is one-sided by its frozen prior.
- **Amended reading** (AMENDMENT_2026-11-10_KA_c.md, 18ac23bd5a, post-freeze, committed alone before any graded number;
  KA-c replaced by a differential recovery check, nothing else changed): **lane NO POWER** (RESULT_BLIND_AMENDED.md,
  edf326295c).

| class | canonical: residual [95 %], MDO | alt: residual [95 %], MDO | label (both footings) |
|---|---|---|---|
| MW ultra-faint (31 + 9 censored) | +0.572 [-0.043, +1.173], 0.88 | +0.542 [-0.087, +1.127], 0.90 | NO POWER |
| MW classical (8) | +0.167 [-0.264, +0.596], 0.62 | +0.134 [-0.305, +0.570], 0.63 | NO POWER |
| bright M31 (25 + 1 censored) | +0.171 [-0.245, +0.609], 0.63 | +0.134 [-0.271, +0.547], 0.59 | NO POWER |
| Coma UDGs (9) | +0.258 [-0.670, +0.726], 1.23 | +0.227 [-0.664, +0.691], 1.20 | NO POWER |

Residual = measured minus form B, dex in g, primary reading. NO POWER: the interval contains 0 but a planted 0.30 dex
offset would not be detected with probability 0.8 (frozen line). No class fails on either footing. Every median stays
above 0. Reported, not graded: MW ultra-faint reads B FAILS HIGH on both footings if its 9 censored rows are fixed at their
limits (+0.666 [+0.052, +1.267] / +0.632 [+0.040, +1.253]) or dropped (+0.646 [+0.026, +1.244] / +0.612 [+0.011, +1.200]),
and at the strong-tide edge on canonical (+0.654 [+0.011, +1.269]).

## COMPARISON (written after RB2's and DG1's results were opened; no label moved)

### Budget off against RB2's class numbers

DSB1's budget-off pass (X1's build copied with seed 20261031, B primary, XF1's boot_median; Coma mean with CFG933's se)
against rb2.json:

| class | DSB1 budget off, can / alt | RB2, can / alt | difference |
|---|---|---|---|
| MW ultra-faint | +0.634 [+0.433, +0.865] / +0.592 [+0.391, +0.822] | +0.6339 [+0.4325, +0.8650] / +0.5924 [+0.3908, +0.8219] | 0 to the printed digit |
| MW classical | +0.281 [-0.015, +0.573] / +0.241 [-0.052, +0.536] | +0.2811 [-0.0153, +0.5728] / +0.2414 [-0.0523, +0.5357] | 0 |
| bright M31 | +0.273 [+0.085, +0.473] / +0.231 [+0.046, +0.429] | +0.2728 [+0.0854, +0.4735] / +0.2313 [+0.0464, +0.4290] | 0 |
| Coma UDGs (statistics only) | +0.325 [+0.102, +0.548] / +0.285 [+0.062, +0.508] | mean +0.3247 / +0.2853; stat-only [+0.105, +0.547] / [+0.062, +0.509] | mean exact; interval within 0.003 (analytic 1.96 se vs SE2's Monte Carlo) |

So DSB1's prediction code is RB2's form B: same rows, same cut, same numbers. RB2's two FAILS HIGH (MW ultra-faint, bright
M31) are what DSB1 sees with measurement scatter only. DSB1's own centres differ from these by -0.06 (UFD), -0.11
(classical), -0.10 (bright M31) and -0.07 (Coma) dex: the censored rows, T10's one-sided binary inflation, the
equilibrium-flagged rows kept with their term, and T8's Jensen shift on the Coma mean.

My a_c (T13, Coma, 0.045 dex) and s_mem (0.008 dex) equal RB2's re-derived s_aniso (0.100 ln = 0.043 dex) and s_mem (0.019 ln
= 0.008 dex) for Coma. RB2's graded Coma interval (SE2's knob posterior, [-0.066, +0.723] / [-0.114, +0.675]) is narrower
than DSB1's [-0.670, +0.726]: DSB1's per-galaxy dispersion draws (T8) on a mean of log sigma^2, the resolution floor T9c and
the coherent aperture term are wider than SE2's linear knobs.

### DSB1's budget against DG1's Part A

| class | DG1 A-full (budget + limits), can / alt | DSB1 primary, can / alt | DSB1 variant closest to DG1 |
|---|---|---|---|
| MW ultra-faint | +0.550 [-0.090, +1.175] / +0.509 [-0.110, +1.141] | +0.572 [-0.043, +1.173] / +0.542 [-0.087, +1.127] | (same) |
| bright M31 | +0.299 [-0.181, +0.774] / +0.258 [-0.237, +0.747] | +0.171 [-0.245, +0.609] / +0.134 [-0.271, +0.547] | flagged rows dropped: +0.207 [-0.208, +0.611] / +0.169 [-0.250, +0.573] |
| DG1 budget, measured only, MW ultra-faint | +0.645 [+0.006, +1.276] / +0.603 [-0.033, +1.230] | censored dropped: +0.646 [+0.026, +1.244] / +0.612 [+0.011, +1.200] | |

- **Agreement.** Built blind and independently, DSB1's budget reaches DG1's Part A reading: neither of RB2's FAILS HIGH
  survives a systematics budget with the censored rows in. The class centres stay high (+0.5 to +0.6 ultra-faints, +0.1 to
  +0.3 bright M31). The widths are carried by the same two coherent knobs: the membership / dataset term (DG1 m_c 0.119,
  DSB1 0.116 dex in sigma for the ultra-faints) and the Upsilon prior (0.30 dex in both).
- **Same hinge, found twice.** Both lanes find that the ultra-faint verdict turns on the 9 upper-limit rows: without them
  DG1's budget misses 0 by 0.006 dex on canonical, and DSB1's misses it by 0.026 / 0.011 dex on both footings. With them
  both contain 0. DG1 uses a Kaplan-Meier median (limits as bounds); DSB1 draws each limited dispersion uniform below its
  limit. Fixed at their limits, DSB1 still reads FAILS HIGH.
- **Differences and their causes.**
  1. Bright M31 centre 0.13 dex lower in DSB1. About 0.04 comes from keeping the four equilibrium-flagged systems (And I,
     XVII, XIX, XXV) with T14 instead of removing them (DG1, by SE2's admissibility). About 0.05 comes from T10, the Minor+2010
     binary inflation that DG1 does not carry for systems above 4 km/s. The remainder comes from DG1's per-system RB2 scatter
     and the two anisotropy widths (next point).
  2. Anisotropy width: DG1 uses SE2's stored a_c (0.089 UFD, 0.116 bright M31, from v3's E-V vs E-W in X1); DSB1 froze
     a_c computed on B's own prediction (0.036-0.038). DG1's is wider, so DG1's intervals are a little wider for bright M31
     (0.96 vs 0.85).
  3. DG1 gives no power statement for Part A. DSB1's frozen power line turns "consistent" into NO POWER: every minimum
     detectable offset is 0.59-1.23 dex. On the budget both lanes use, the dwarf classes cannot see a factor-2 departure
     from B in either direction. Even with the M/L zero point removed (M1), no class reaches the 0.30 line, and MW classical
     lacks it on the bootstrap alone (8 systems with about 0.3 dex scatter).
- **Not a difference:** DG1's history parts (B, C, D) are outside DSB1's scope and were not compared.

### What this does to the record (no relabel)

RB2's labels stand as its own frozen reading. With a budget frozen before the numbers, the hosted dwarf classes do not
decide form B either way: the deciding step the paper lists returns NO POWER, not a pass. The one place the data still
lean against B is the ultra-faint class, whose centre sits about +0.55 dex above B on both footings and whose interval
clears 0 unless the upper-limit rows are drawn below their limits.

## Known answers and mutations

- KA-a PASS (X1's Delta[Newton] and sdMC, 178 rows, exact; central-value function median 0.0035, max 0.053 dex).
- KA-b PASS (Fornax log M_1/2 7.976 vs Campbell+2017 7.88, PROVISIONAL, and LVD 7.98).
- KA-c FAIL (frozen; recovery +0.304 / +0.296 classical, +0.337 / +0.314 Coma against +0.40 +- 0.10); diagnosed on the mock
  only: T10 -0.12 (classical), T8 -0.06 (Coma).
- KA-c' PASS (amended; differential recovery +0.399 to +0.426 on every graded class and footing).
- M1 PASS (T1 removed narrows every width), M2 PASS (a0 doubled lowers every residual by 0.14-0.15 dex), M3 PASS but
  vacuous except alt bright M31 (only cell with MDO <= 0.60; it read FAILS HIGH on +0.60). The three dSph classes read FAILS
  HIGH on the +0.60 mock on both footings, Coma read NO POWER.

## Run

`nice -n 19 python3 dsb1.py` (frozen reading, stops at KA-c, about 1 s), `--amend` (40 s), `--mutate` (5 s). One thread,
fixed seeds, no large arrays on disk. Temporary diagnostic script in the system temp directory, removed.

## Not checked, or PROVISIONAL

- PROVISIONAL widths: T2, T6 (dSph), T7 (Coma), T9, T9c, T10, T12, T14, T15 and KA-b's 7.88 (web summaries or stated rules;
  Campbell+2017 and Minor+2010 papers were not read in full).
- The host distance is not moved with the distance draws. The power rule's shift construction was checked only at +0.40.
- The ultra-faint verdict depends on the censored-row rule. That dependence was not foreseen when the rule was frozen.
- DF2 / DF4 and the four individual MW rows were not regraded. No screening (L* = 0).
- The graded labels exist only under a post-freeze amendment. The frozen reading has no label.

## Files and commits (local main; not pushed)

- FROZEN_CRITERIA.md: 2c7beb7b92 (alone).
- dsb1.py, dsb1.out / .json, RESULT_BLIND.md (frozen reading, stopped): 8e189b5326.
- AMENDMENT_2026-11-10_KA_c.md: 18ac23bd5a (alone).
- dsb1.py (amended mode), dsb1_amended.*, dsb1_MUTATE.*, RESULT_BLIND_AMENDED.md: edf326295c.
- This file: the commit after edf326295c (id in its message).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

# DSB1 blind result, amended reading: NO POWER (every graded class, both footings)

Two readings, reported in this order:
- **Frozen reading (criteria 2c7beb7b92): STOPPED AT KA-c, no label** (RESULT_BLIND.md, commit 8e189b5326).
- **Amended reading (AMENDMENT_2026-11-10_KA_c.md, commit 18ac23bd5a, post-freeze, committed alone before any graded number):
  lane label NO POWER.** The amendment only replaced KA-c's recovery line with a differential one; budget, statistic, power
  line and label rules are the frozen ones.

Blind: RB2's and DG1's results (RESULT.md, .json, .out) were not opened before this file was committed. Run: `nice -n 19
python3 dsb1.py --amend` (40 s) and `--mutate` (5 s), one thread, fixed seeds; outputs dsb1_amended.json / .out,
dsb1_MUTATE.json / .out. The frozen outputs dsb1.json / .out are unchanged.

## Labels

**Lane: NO POWER.** No graded class fails on either footing, and no graded class has the power the frozen line asks for
(a planted 0.30 dex offset detected with probability 0.8): every minimum detectable offset is 0.59-1.23 dex.

| class | canonical | alt | class label |
|---|---|---|---|
| MW ultra-faint | NO POWER | NO POWER | NO POWER |
| MW classical | NO POWER | NO POWER | NO POWER |
| bright M31 | NO POWER | NO POWER | NO POWER |
| Coma UDGs | NO POWER | NO POWER | NO POWER |

## Per class, primary reading (graded): residual = measured minus form B, dex in g; 95 % interval; MDO

| class | N (meas + cens) | canonical | MDO | alt | MDO | budget null shift can / alt |
|---|---|---|---|---|---|---|
| MW ultra-faint | 31 + 9 | +0.572 [-0.043, +1.173] | 0.88 | +0.542 [-0.087, +1.127] | 0.90 | -0.018 / -0.008 |
| MW classical | 8 + 0 | +0.167 [-0.264, +0.596] | 0.62 | +0.134 [-0.305, +0.570] | 0.63 | -0.099 / -0.106 |
| bright M31 | 25 + 1 | +0.171 [-0.245, +0.609] | 0.63 | +0.134 [-0.271, +0.547] | 0.59 | -0.058 / -0.074 |
| Coma UDGs | 9 | +0.258 [-0.670, +0.726] | 1.23 | +0.227 [-0.664, +0.691] | 1.20 | -0.072 / -0.112 |

The null shift is the budget's own centre shift on a mock that sits exactly on B (T10's one-sided binary prior for MW
classical and bright M31; T8's Jensen bias for Coma); it is already inside the residuals above, not added on top.

Reported, not graded:
- **MW ultra-faint, censored-row rule.** The class sits at the edge: the main rule (censored dispersions uniform on
  [0, UL]) gives intervals whose lower ends are -0.043 / -0.087. With the 9 censored rows fixed at their limits:
  +0.666 [+0.052, +1.267] / +0.632 [+0.040, +1.253], B FAILS HIGH on both footings; with them dropped (RB2's convention):
  +0.646 [+0.026, +1.244] / +0.612 [+0.011, +1.200], B FAILS HIGH on both footings. The ultra-faint row's verdict therefore
  rests on the frozen censored-row rule: the 9 upper-limit rows, drawn below their limits, are what pull the interval
  across 0.
- **Strong-tide edge:** MW ultra-faint +0.654 [+0.011, +1.269] B FAILS HIGH canonical, +0.606 [-0.031, +1.247] NO POWER alt
  (SPLIT); every other class and the weak edge read NO POWER on both footings (numbers in dsb1_amended.out).
- Equilibrium-flagged rows dropped (Bootes III, And I, And XVII, And XIX, And XXV; no Coma galaxy is flagged): no label moves.
- Coma with T8 drawn symmetric in log sigma (amendment's variant): +0.314 [-0.434, +0.776] / +0.282 [-0.425, +0.735],
  MDO 1.00 / 0.95, NO POWER.
- M31 others: +0.434 [-0.404, +1.047] / +0.390 [-0.430, +1.024], NO POWER. LG field (control, B = isolated law):
  -0.086 [-0.433, +0.238] / -0.116 [-0.481, +0.212], NO POWER (MDO 0.50 / 0.52).
- **Budget off in RB2's convention** (X1-built per-system medians and sds under B primary, XF1 boot_median; Coma mean
  +- 1.96 se, no knob): MW ultra-faint +0.634 [+0.433, +0.865] / +0.592 [+0.391, +0.822]; MW classical +0.281 [-0.015, +0.573]
  / +0.241 [-0.052, +0.536]; bright M31 +0.273 [+0.085, +0.473] / +0.231 [+0.046, +0.429]; Coma +0.325 [+0.102, +0.548] /
  +0.285 [+0.062, +0.508]. So with measurement scatter only, MW ultra-faint and bright M31 lie above B on both footings
  (and Coma too by the bare se); the budget, not a change of centre, is what turns them into NO POWER (the centres move by
  0.06-0.11 dex; the widths grow 2-5 times).

## Which terms carry the width (95 % width, primary, canonical; alt within 0.06)

| class | all terms | bootstrap only | largest terms alone (incl. bootstrap) | width with that term removed |
|---|---|---|---|---|
| MW ultra-faint | 1.24 | 0.38 | T11 membership / dataset 0.97, T1 M/L zero point 0.72, T10 binaries 0.46, T9 velocity floor 0.45 | T11 0.81, T1 1.09 |
| MW classical | 0.91 | 0.59 | T1 0.83 (all others add nothing visible) | T1 0.59 |
| bright M31 | 0.81 | 0.30 | T1 0.70, T11 0.43, T10 0.40, T8 0.36 | T1 0.60 |
| Coma UDGs | 1.32 | 0.28 | T8 dispersion errors 0.70, T17 aperture / tracer 0.56, T1 0.52, T9c resolution floor 0.48 | T8 0.82, T9c 0.98 |

- All the dominant terms are coherent across the class except T8; that is why the widths do not average down.
- T11 for the ultra-faints is SE2's rule verbatim: LVD against McConnachie 2012 dispersions for 10 matched ultra-faints,
  m_c = 0.116 dex in sigma (0.23 dex in g), mostly a mean offset between the two compilations.
- T1 is the record's own prior (Upsilon_V 2, bracket 1-4 read as +-1 sigma, 0.30 dex). B responds to M* almost linearly
  where the tidal cut is active, so it gives 0.6-0.8 dex of width by itself.
- Even with nothing but the bootstrap over systems, MW classical has no power (width 0.59, MDO about 0.42): 8 systems
  scatter by about 0.3 dex. The other three classes would have power at the 0.30 line on measurement scatter alone.
- With T1 removed (mutation M1), every class still reads NO POWER (narrowest width 0.58, MDO above 0.4).

## Known answers (amended gate: KA-a, KA-b, KA-c')

- KA-a PASS: X1's Delta[Newton] and sdMC, 178 rows, both footings, exact (0.0, line 1e-9); central-value function median
  |d| 0.0035, max 0.053 dex.
- KA-b PASS: Fornax log M_1/2 7.976 against Campbell+2017 7.88 (PROVISIONAL) and LVD 7.98.
- KA-c FAIL (frozen line; this is the frozen reading's stop): full-budget recovery of +0.40 gave +0.304 / +0.296 (classical)
  and +0.337 / +0.314 (Coma).
- KA-c' PASS (amended): rec(+0.40) - rec(0) = +0.421, +0.402, +0.402, +0.410 (canonical: UFD, classical, bright M31, Coma);
  +0.408, +0.402, +0.399, +0.426 (alt); line |d - 0.40| <= 0.10. Form B limits exact; budget-off planted recovery 3e-16.

## Mutations (dsb1_MUTATE.*)

- M1 PASS: T1 removed narrows every graded width on both footings (e.g. classical 0.86 -> 0.60, bright M31 0.86 -> 0.58).
- M2 PASS: a0 doubled lowers every graded residual by 0.14-0.15 dex on both footings (e.g. UFD +0.572 -> +0.422).
- M3 PASS but weak: planted +0.60 reads B FAILS HIGH in MW ultra-faint, MW classical and bright M31 on both footings, NO
  POWER in Coma. The frozen bite condition only binds where MDO <= 0.60, which is alt bright M31 alone (MDO 0.59): it read
  FAILS HIGH. Elsewhere the condition was vacuous; the three dSph classes still detected +0.60 in this one mock.

## Hand estimates against the outcome

Centres were as guessed (UFD +0.57 against +0.3-0.6; classical +0.17 against 0-0.2; bright M31 +0.17 against -0.1-0.2;
Coma +0.26 against +0.2-0.4). The widths were underestimated: I guessed 0.3-0.6 dex half widths; they are 0.40-0.70.
The lane came out NO POWER, the second of the two outcomes I named as likely.

## What was not checked, or is PROVISIONAL

- PROVISIONAL widths (web look-ups or stated rules without a look-up): T2 (0.10 dex), T6 dSph zero point (0.10 mag), T7
  Coma R_e (10 %), T9 DEIMOS floor spread (Simon & Geha 2007 2.2, Kirby+2015 1.49 km/s; web summary), T9c Coma resolution
  floor (no look-up), T10 Minor+2010 30 % (web summary; arXiv text says 20 %), T12 Campbell+2017 23 % (web summary, paper
  not read), T14 0.20 dex (stated rule), T15 host-mass widths (no look-up), KA-b's 7.88 (web summary of Campbell's table).
- The host distance d is not moved with the distance draws (X1's convention); the Jacobi radius sees only V_c and T15.
- The power rule's shift construction assumes the interval shape does not change with the planted offset; KA-c' supports it
  at +0.40 only.
- The class verdict for MW ultra-faint depends on the censored-row rule (above); the rule was frozen, the dependence was not
  foreseen.
- No screening (L* = 0), as RB2's graded primary; DF2 / DF4 and the four individual MW rows are outside the four classes and
  were not regraded.
- The frozen KA-c failure means the graded labels exist only under a post-freeze amendment.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

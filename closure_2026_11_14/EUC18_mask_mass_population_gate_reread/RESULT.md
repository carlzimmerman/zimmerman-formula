# EUC18 (MASK-APERTURE STELLAR MASS, SECOND RE-READ: THE POPULATION GATE): RESULT

2026-11-14. Criteria c8908592a4 (committed alone, before the driver and before any number). No amendment. Every
check passes as frozen; the twin exits 1.

## Verdict (law S, canonical / alt)

| Row | Committed | With the in-mask mass | Label |
|---|---|---|---|
| **Q1** EUC13-P gate (median boost on P, drawn source redshifts) | NO VERDICT / NO VERDICT | **NO VERDICT / NO VERDICT** | UNCHANGED, ROBUST / ROBUST |
| **Q2** f₂₅ statistic (share of P needing more than 1.78 × Salpeter) | CEILING BROKEN / CEILING BROKEN | **CEILING BROKEN / CEILING BROKEN** | UNCHANGED, ROBUST / **FRAGILE** |

In plain words. EUC17 found that EUC1's word moves to CEILING HOLDS once the catalogued mass is put inside the
modelling circle, but only with every source infinitely far away. This lane asks the same of the row that uses
realistic source redshifts, by running EUC13's own code on the corrected masses.

- **With realistic sources the main sample still breaks the ceiling.** Between 28 % and 43 % of the 3,192 lenses
  still need more than 1.78 × their Salpeter stars, against a 25 % line (was 43 % to 58 %). Every member's lower
  bound stays above the line: the lowest is 0.283 (canonical) and 0.256 (alt).
- **On the alt footing that word is fragile.** The bracket that enlarges the correction (R_e × 1.25) drops two
  members below the line (lower bounds 0.228 and 0.236) and reads NO VERDICT. No bracket moves the canonical word.
- **The gate on the median stays NO VERDICT, on the other side.** The members' medians were +0.20 to +0.30 dex,
  around the FAILS line (0.25). They are now **+0.12 to +0.21 dex** (1.3 × to 1.6 × Salpeter), around the HOLDS line
  (0.15). HOLDS needs every member's upper bound at or below 0.15; they are 0.179, 0.261 and 0.156 (canonical) and
  0.162, 0.244 and 0.138 (alt).
- **The wide lenses still lack about a quarter of their mass** (reading, source at infinity): the share of the
  lensing lower bound that law and stars do not supply falls from 45 % / 42 % to 29 % / 26 %, and the missing mass
  from 3.2 / 2.9 to 2.0 / 1.75 × 10¹¹ M☉.

EUC17's hit on EUC1 therefore does not carry over to realistic source redshifts. Nothing here is a pass. A
population gate grades modelled or borrowed source populations, not measured sources.

κ = ½ FITTED. Footings never pooled. Adopts nothing; no ledger or scorecard edited.

## 1. Members on P (EUC13's own code; point and 95 % interval)

| Member, footing | b_med committed | b_med corrected | f₂₅ committed | f₂₅ corrected |
|---|---|---|---|---|
| M1 AGEL DR2, canonical | +0.238 [+0.213, +0.265] | +0.152 [+0.125, +0.179] | 0.479 [0.443, 0.519] | 0.320 [0.283, 0.359] |
| M1, alt | +0.220 [+0.195, +0.247] | +0.134 [+0.107, +0.162] | 0.451 [0.415, 0.491] | 0.293 [0.256, 0.330] |
| M2 DESI SLF IV, canonical | +0.298 [+0.253, +0.346] | +0.210 [+0.162, +0.261] | 0.576 [0.512, 0.645] | 0.432 [0.358, 0.506] |
| M2, alt | +0.281 [+0.235, +0.330] | +0.194 [+0.145, +0.244] | 0.549 [0.480, 0.615] | 0.405 [0.333, 0.482] |
| M3 forward model, full weight, canonical | +0.233 [+0.219, +0.244] | +0.146 [+0.132, +0.156] | 0.474 [0.453, 0.489] | 0.324 [0.309, 0.343] |
| M3 full, alt | +0.215 [+0.202, +0.227] | +0.127 [+0.116, +0.138] | 0.445 [0.427, 0.462] | 0.297 [0.280, 0.315] |
| M3 sis weight, canonical | +0.222 [+0.208, +0.233] | +0.134 [+0.123, +0.146] | 0.456 [0.437, 0.472] | 0.305 [0.287, 0.323] |
| M3 sis, alt | +0.204 [+0.191, +0.217] | +0.116 [+0.106, +0.127] | 0.427 [0.408, 0.443] | 0.280 [0.261, 0.298] |

The surviving members and the surviving forward-model setting (μ = 10) are the committed ones. Median source
redshifts are unchanged (2.05, 1.60, 2.17 / 2.27). The forward model's self-consistent boost falls from +0.205 /
+0.184 to +0.116 / +0.098.

## 2. Gate block and brackets (intervals over surviving members; M3 as an envelope)

| Run | Footing | b_med intervals (M1; M2; M3) | f₂₅ intervals (M1; M2; M3) | Q1 | Q2 |
|---|---|---|---|---|---|
| committed | canonical | [+0.213, +0.265]; [+0.253, +0.346]; [+0.208, +0.244] | [0.443, 0.519]; [0.512, 0.645]; [0.437, 0.489] | NO VERDICT | CEILING BROKEN |
| committed | alt | [+0.195, +0.247]; [+0.235, +0.330]; [+0.191, +0.227] | [0.415, 0.491]; [0.480, 0.615]; [0.408, 0.462] | NO VERDICT | CEILING BROKEN |
| **primary** | canonical | [+0.125, +0.179]; [+0.162, +0.261]; [+0.123, +0.156] | [0.283, 0.359]; [0.358, 0.506]; [0.287, 0.343] | NO VERDICT | CEILING BROKEN |
| **primary** | alt | [+0.107, +0.162]; [+0.145, +0.244]; [+0.106, +0.138] | [0.256, 0.330]; [0.333, 0.482]; [0.261, 0.315] | NO VERDICT | CEILING BROKEN |
| F1a (R_e × 0.80) | canonical | [+0.140, +0.195]; [+0.177, +0.276]; [+0.138, +0.172] | [0.309, 0.385]; [0.384, 0.532]; [0.313, 0.369] | NO VERDICT | CEILING BROKEN |
| F1a | alt | [+0.122, +0.177]; [+0.159, +0.259]; [+0.121, +0.153] | [0.284, 0.359]; [0.358, 0.506]; [0.286, 0.341] | NO VERDICT | CEILING BROKEN |
| F1b (R_e × 1.25) | canonical | [+0.107, +0.159]; [+0.145, +0.242]; [+0.103, +0.138] | [0.251, 0.328]; [0.331, 0.478]; [0.260, 0.315] | NO VERDICT | CEILING BROKEN |
| F1b | alt | [+0.089, +0.142]; [+0.127, +0.225]; [+0.087, +0.118] | **[0.228, 0.301]**; [0.305, 0.454]; **[0.236, 0.288]** | NO VERDICT | **NO VERDICT** |

Q2 canonical under F1b keeps its word by 0.001 (lowest lower bound 0.251). Q1 is NO VERDICT in every run: M2's upper
bound never falls to 0.15.

## 3. Checks (all as frozen)

| Check | Result |
|---|---|
| H0 f = 1 reproduces EUC13's committed outputs | PASS: results file and per-lens file identical byte for byte; the log differs in 2 of 70 lines, both elapsed times |
| H1 source folders of EUC13, EUC1, EUC10 untouched | PASS: no changed path |
| H2 exactly the reference-number checks fail under the correction | PASS in all three corrected runs: KA2, KA3 (M1), KA3 (M2) fail; KA1, KA4, KA5, KA6 pass; M3 survivor μ = 10 |
| H3 the shift arrives | PASS: source-free b_med on P −0.1043 / −0.1298, EUC17's corrected value −0.1043 / −0.1298 |
| Twin invert (masses lowered instead) | exits 1: every member's b_med rises on both footings (M1 +0.316 / +0.298) |

EUC13's own summary line reads NOT EVALUABLE in the corrected runs, as the criteria said it would: KA2 and KA3
assert EUC1's and EUC10's uncorrected numbers. The words above are read from its gate block.

## 4. Readings (no word)

**Wide lenses, share of the lensing mass still missing** (class W: 316 lenses, grades A and B, θ_E ≥ 1.7″; source at
infinity; law S; check KW reproduces EUC8's committed values exactly at f = 1):

| Footing | Share not supplied [16–84 %] | Excess mass (median) | Lenses needing more |
|---|---|---|---|
| canonical | 0.451 [0.279, 0.655] → **0.294 [0.080, 0.498]** | 3.17e11 → 1.98e11 M☉ | 99.7 % → 91.5 % |
| alt | 0.421 [0.245, 0.631] → **0.258 [0.036, 0.466]** | 2.91e11 → 1.75e11 M☉ | 99.1 % → 88.0 % |

Median correction on W: 0.143 dex. The gas lanes (ESZ1, EXR1, EXR2) were built on the uncorrected excess; the body
of gas they need is about 40 % smaller. They are not re-read here.

**Einstein-radius classes, b_med per member** (canonical; alt is about 0.02 lower): below 1.0″ +0.15 to +0.23 →
+0.07 to +0.16; 1.0–1.3″ +0.27 to +0.33 → +0.17 to +0.23; at or above 1.3″ +0.45 to +0.50 → +0.30 to +0.35.
EUC13's code also prints each class against EUC5's sealed dynamical bands, and the widest class now prints
"inside" where it printed "above". **That comparison is not like for like and is not reported as a change:** the
bands were built on the uncorrected mass, and the same correction would lower them.

## 5. Limits

- The premise (catalogue mass = in-mask mass) rests on the paper's text and on one lens, as in EUC17.
- The correction can only lower b. The lines and the sample are EUC13's.
- Only the two bounding brackets were run (EUC17 found they bound the others). Q2's alt word depends on which radius
  convention is right: the catalogue's radius as given keeps it; a radius 25 % larger loses it.
- A circular Sérsic share stands in for the elliptical one.
- EUC13R, the blind twin of EUC13, is not re-read (its own code does not use EUC1's loader). No blind re-grade of
  this lane exists; no word changed, so none is owed by the house rule.
- Not graded (criteria §7): EUC8 Part B, EUC5 / EUC5R, EUC6, LNJ1, EUC4's secondary and complement bins (mask table
  did not cover them when this lane was frozen; the grade-B masks have since been fetched into
  `closure_2026_11_14/EUC19_grade_b_mask_table/`, which this lane does not use), ESZ1, EXR1 / EXR2, EUC7, EUC12.
  CJ1's row 39 is not edited.

## 6. Files and re-run

- `FROZEN_CRITERIA.md`; `euc18_run.py` (driver: EUC1's loader wrapped, EUC13's script run unmodified, its writes
  redirected); `euc18_collect.py`; `euc18.out`, `euc18_results.json`.
- `runs/<mode>/` for f1, primary, F1a, F1b, invert: EUC13's three output files as that run wrote them,
  `driver.json`, `exit_code.txt`.

```
python3 -I euc18_run.py --mode f1      --data-dir <ECLIPSE dir> --lit <EUC10 literature dir>     # harness
python3 -I euc18_run.py --mode primary --data-dir <ECLIPSE dir> --lit <EUC10 literature dir>
python3 -I euc18_run.py --mode F1a | F1b ...
python3 -I euc18_run.py --mode invert ...                                                        # exits 1
python3 -I euc18_collect.py --data-dir <ECLIPSE dir>                                             # exits 0
```

Each EUC13 run takes 8 to 15 minutes on one thread and about 0.5 GB. Run by the session that wrote the lane.

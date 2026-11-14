# EUC20 (MASK-APERTURE STELLAR MASS, THIRD RE-READ: THE GRADE-B LANES): RESULT

2026-11-14. Criteria cbd14e4ca4 (committed alone while the grade-B mask fetch was running, before its table was
opened). No amendment. Every frozen check passes; the three twins exit 1 and bite. One collector error, corrected
and disclosed in §3.

## Verdict (law S, canonical / alt)

| Row | Committed | With the in-mask mass | Label |
|---|---|---|---|
| **G1** EUC4's secondary bin (292 grade-B lenses, 1.3″ ≤ θ_E < 1.7″, source at infinity) | WIDE LENSES BREAK THE CEILING / same | **NO VERDICT / NO VERDICT** | **CHANGED**, ROBUST / ROBUST |
| **G2** EUC8 lane word (how concentrated the missing mass must be) | SLOPE NOT CONSTRAINED / same | **SLOPE NOT CONSTRAINED / same** | UNCHANGED, ROBUST / ROBUST |
| **G3** LNJ1 (is the lens excess the candidate sixth rule's switch?) | NO POWER, FRAGILE / NO POWER | **NO SWITCH, FRAGILE / NO SWITCH, FRAGILE** | **CHANGED**, ROBUST / FRAGILE |

In plain words.

- **The ceiling break at infinite source distance is now confined to the widest lenses.** In the 1.3–1.7″ grade-B
  bin the share needing more than 1.78 × Salpeter falls from 43 % / 38 % to **18 % / 15 %**: no longer above the 25 %
  line, not below the 10 % floor. Below 1.0″ it is 5.5 % / 5.1 % (NOT CONFIRMED on both footings; was NO VERDICT /
  NOT CONFIRMED). At or above 1.7″ it stays broken (44 % / 38 %, EUC17). G1 is a hit awaiting a blind re-grade,
  not a pass: with sources at z ≈ 2 the same class still lacks 38 % / 35 % of its lensing mass (§4).
- **EUC8's word does not move.** A compact central mass is still TOO CONCENTRATED and every extended family is
  still ALLOWED, on both footings and in both brackets. The margin on the compact family shrank: its widened upper
  bound is −0.044 / −0.012 dex where it was −0.214 / −0.186.
- **LNJ1 gains power and reads NO SWITCH.** With the corrected masses 108 lenses sit above the candidate rule's
  boundary speed on the canonical footing (26 before) and 22 on alt (none before). The share of lenses above the
  band is 5.8 % below the boundary and 4.6 % above it (canonical), 5.2 % and 0 % (alt): no step at the boundary.
  This counts against reading the Euclid lens excess as the switch of the candidate sixth rule (crossing-speed
  joint, NOT ADOPTED). It says nothing new about the law. The word is FRAGILE by LNJ1's own brackets: the
  measured-speed rule reads NO POWER, and with AGEL-drawn source redshifts the joint UNDER-PREDICTS above the
  boundary in 50 of 50 draws (canonical; median residual +0.245 dex) and 47 of 50 (alt). On alt, bracket F1a leaves
  15 lenses above the boundary and reads NO POWER.

κ = ½ FITTED. Footings never pooled. Adopts nothing; no ledger or scorecard edited; no outcome here is a pass of the
lensing gate.

## 1. EUC4's grade-B bins (exact shift; every lens has a mask)

| Bin | Median correction | f₂₅ committed | f₂₅ corrected | Word |
|---|---|---|---|---|
| W_B ≥ 1.7″ (124), canonical / alt | 0.132 dex | 0.758 / 0.702 | 0.444 [0.355, 0.524] / 0.379 [0.298, 0.460] | BREAK / BREAK (as EUC17) |
| **secondary 1.3–1.7″ (292)**, canonical | 0.108 dex | 0.425 [0.370, 0.479] | **0.182 [0.140, 0.226]** | BREAK → NO VERDICT |
| secondary, alt | | 0.380 [0.329, 0.435] | **0.154 [0.113, 0.199]** | BREAK → NO VERDICT |
| complement < 1.0″ (2,045), canonical | 0.036 dex | 0.092 [0.080, 0.105] | 0.055 [0.046, 0.065] | NO VERDICT → NOT CONFIRMED (reported) |
| complement, alt | | 0.082 [0.070, 0.093] | 0.051 [0.042, 0.060] | NOT CONFIRMED → NOT CONFIRMED (reported) |

Secondary bin, median boost: canonical +0.071 [+0.046, +0.108] dex, alt +0.047 [+0.020, +0.080]. Brackets on the
secondary bin: F1a 0.202 [0.158, 0.250] / 0.188 [0.144, 0.236]; F1b 0.151 [0.113, 0.192] / 0.123 [0.086, 0.161]:
NO VERDICT in every one. Law B on the secondary bin: 0.243 / 0.223, NO VERDICT (was BREAK on both).

## 2. LNJ1 through its own code (one substitution on the mass column)

| | Committed | Corrected |
|---|---|---|
| Lenses above / below the boundary, model rule, canonical | 26 / 6,147 | 108 / 6,065 |
| alt | 0 / 6,173 | 22 / 6,151 |
| Share above the band, below / above the boundary, canonical | 0.138 / 0.154 | 0.058 / 0.046 |
| alt | 0.121 / none | 0.052 / 0.000 |
| Raw word, canonical / alt | NO POWER / NO POWER | NO SWITCH / NO SWITCH |
| Bracket words that differ | canonical: three; alt: none | canonical: measured rule NO POWER, AGEL draws JOINT UNDER-PREDICTS ABOVE THE BOUNDARY; alt: those two and catalogue scale NO POWER |

LNJ1's own boundary twins (half and double the boundary speed) bite and its shuffle twin destroys, in the corrected
run as in the committed one. LNJ1 is a TEST lane, post hoc twice by its own note; its word inherits that.

## 3. Checks

| Check | euc8 | euc5 (A1) | lnj1 | EUC4 bins |
|---|---|---|---|---|
| H0 f = 1 reproduces the committed outputs | PASS: 3 files identical, log differs in 1 elapsed-time line | PASS: 2 identical, log 1 timing line | PASS: 8 files identical, log 1 timing line | PASS: every statistic and word |
| H1 source folders untouched | PASS | PASS | PASS | PASS |
| H2 exactly the reference-number checks fail | PASS: K1, K5 | PASS: gates and sample sizes unchanged | PASS: KA-1, KA-2 | n/a |
| H3 the shift arrives | PASS: K1 prints 0.444 / 0.379 = EUC17's corrected values | | KA-1 prints the same and EUC1's 0.060 / 0.050; KA-2 prints EUC18's M1 +0.152 / +0.134 | W_B row equals EUC17's |
| H4 lenses of S without a mask | 0 of 6,173 | 0 | 0 | 0 |
| Twin invert | exits 1; W excess rises | exits 1; b_dyn rises | none (as frozen) | exits 1 |

**Collector error, corrected.** The collector's first run printed G2 as NOT EVALUABLE because it read EUC8's own
`verdict` field. That field is gated by EUC8's checks, and K1 and K5 fail under the correction by design (H2). The
row's frozen rule is EUC8's Part B rule on the family words, so the collector now applies that rule to the family
words the corrected run produced (and check H5 shows the rule returns the committed word from the committed
family words). The family words did not change, so the word is SLOPE NOT CONSTRAINED. Every other line of the
collector output is identical between the two runs; the first is kept as `euc20_firstrun.out`.

## 4. Readings (no word)

**EUC8 Part A: share of the lensing mass that law S and the catalogued stars do not supply** (median; all of sample
S, 6,173 lenses):

| Einstein-radius class (N) | Source at infinity, canonical / alt | Source at max(2, z_l + 0.5), canonical / alt |
|---|---|---|
| ≥ 1.7″ (316) | 0.451 → 0.294 / 0.421 → 0.258 | 0.613 → 0.502 / 0.590 → 0.476 |
| 1.3–1.7″ (653) | 0.290 → 0.092 / 0.256 → 0.046 | 0.502 → 0.376 / 0.475 → 0.349 |
| 1.0–1.3″ (1,211) | 0.104 → 0.000 / 0.063 → 0.000 | 0.402 → 0.293 / 0.373 → 0.262 |
| below 1.0″ (3,993) | 0.000 → 0.000 / 0.000 → 0.000 | 0.287 → 0.203 / 0.258 → 0.173 |

With sources near z = 2 the median lens of every class still lacks a fifth to a half of its lensing mass. The share
of lenses needing any extra mass in that case: 99.7 %, 93.9 %, 86.6 %, 74.2 % (canonical).

**EUC8 Part B numbers** (25 dispersion lenses, θ_E ≥ 1.3″): EUC5's class reading that K5 checks goes from b_dyn
+0.200 to +0.005 (canonical): at the corrected mass the stars' fibre dispersions need no boost under the law. The
slope at which the class median crosses zero goes from 2.19 [1.73, 2.30] to 0.20 [below 0, 2.24] (far case): less
constrained than before.

**EUC5 under A1** (55 lenses of S, 32 of P; raw dispersions). Its word is NOT EVALUABLE on its dispersion-recovery
gate, before and after. Median b_dyn: sample S +0.193 → +0.062 (canonical), +0.187 → +0.055 (alt); sample P +0.196
→ +0.054, +0.191 → +0.048. By class (alt): below 1.0″ +0.043 → −0.027; 1.0–1.3″ +0.169 → +0.098; 1.3–1.7″ +0.227 →
+0.027; ≥ 1.7″ +0.252 → +0.084. **Dynamics minus the source-free lensing bound is unchanged to every digit**
(+0.103 [+0.011, +0.136] canonical, +0.119 [+0.029, +0.152] alt), as it must be: both shift by the same amount per
lens. The dispersions still ask for about 0.1 dex more than lensing's lower bound.

**EUC6** (its word cannot move without a new control set). The 249 wide-lens / control pairs, matched at catalogue
mass (median difference +0.018 dex), differ by **+0.068 dex [+0.050, +0.097]** at corrected mass: the wide lenses
are now heavier than their controls. On the controls' own richness–mass slope (+4.6 galaxies per dex, [−1.6, +9.4],
poorly constrained) that is worth **+0.31 galaxies [−0.12, +0.70]** against a paired excess of +3.49 on these pairs
(EUC6 quotes +3.38 on its 243). A small part: on this evidence EUC6 does not need a re-matched control set.

## 5. Limits

- The premise (catalogue mass = in-mask mass) rests on the paper's text and on one lens, as in EUC17.
- The correction can only lower the boost. The lines and samples are the source lanes'.
- G1 is a source-at-infinity statement. No reading with realistic source redshifts favours the law (§4; EUC18).
- G3's change comes from membership: the model-rule speed rises with the stellar mass, so more lenses cross the
  boundary. LNJ1's measured-speed rule, which does not use the stellar mass for membership, still reads NO POWER.
- A circular Sérsic share stands in for the elliptical one; only the two bounding brackets were run.
- No blind re-grade of this lane exists. Two words changed (G1, G3), so one is owed. Not launched here.
- Not graded: EUC5 / EUC5R words (instrument gate), EUC6's word, EUC4R, EUC13R, ESZ1, EXR1 / EXR2, EUC7, EUC12.
  CJ1's row 39 is not edited.

## 5a. Blind re-grade EUC20R (dated addition, 2026-11-14; no number or label of this file changes)

`closure_2026_11_14/EUC20R_blind_grade_b_regrade/` (a separate session that read only the criteria and wrote its own
code). **Its labels, as frozen, are the same in all six row and footing slots**, fragility tags included: G1 NO
VERDICT, CHANGED, ROBUST on both; G2 SLOPE NOT CONSTRAINED, UNCHANGED, ROBUST on both; G3 NO SWITCH, FRAGILE, CHANGED,
ROBUST on canonical and FRAGILE on alt (bracket F1a reads NO POWER there in both builds). Its numbers equal this
file's to the printed digit, and every one of its checks passes with no amendment.

- Blindness: its starting context showed no EUC20 subject among the recent commits and one memory-index line that
  named this lane without a word or number. A first attempt earlier the same day stopped itself as not blind (this
  lane's result subject was still in its recent-commit list) and wrote nothing.
- Lead's re-run of its code (harness, the four other modes, collector, twin collector): exits 0, 0, 0 and 1 as
  documented; the only lines that differ from its committed outputs are elapsed times and its run log.
- Commits (local / origin): reading 025dc97b73 / e1cbb7d045; code, runs and result c05ae562b1 / 851cd135f8;
  comparison 7cc9287d31 / 3e2be69fd4.

The limit in §5 that no blind re-grade exists is superseded by this section. G1 and G3 are now confirmed by an
independent implementation; G1 is still not a pass.

## 6. Files and re-run

- `FROZEN_CRITERIA.md`; `euc20_run.py` (driver), `euc20_bins.py`, `euc20_collect.py`.
- `runs/<lane>/<mode>/` for euc8, euc5a1, lnj1 × f1, primary, F1a, F1b (and invert for euc8, euc5a1): the source
  lane's output files as that run wrote them, `driver.json`, `exit_code.txt`.
- `euc20_bins.out`, `euc20_bins_results.json`, `euc20_bins_MUTATE_invert.*`; `euc20.out`, `euc20_results.json`;
  `euc20_firstrun.out`, `euc20_firstrun_results.json` (the collector's first run).
- Masks: `closure_2026_11_13/EUC17_mask_aperture_mass_reread/euc17_masks.csv` and
  `closure_2026_11_14/EUC19_grade_b_mask_table/euc19_masks.csv`.

```
python3 -I euc20_run.py --lane euc8|euc5a1|lnj1 --mode f1|primary|F1a|F1b|invert --data-dir <ECLIPSE dir>
python3 -I euc20_bins.py --data-dir <ECLIPSE dir>                       # exits 0
EUC20_MUTATE=invert python3 -I euc20_bins.py --data-dir <ECLIPSE dir>   # exits 1
python3 -I euc20_collect.py                                             # exits 0
```

About four minutes in all, one thread. Run by the session that wrote the lane.

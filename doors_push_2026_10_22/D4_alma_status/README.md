# D4_alma_status: the two sealed ALMA tests, readiness and honest power

**Verdict: CRISP FINDING** (on power and on a gap in the plans). The tests themselves stay DATA-GATED (U4_27928 on 2026-11-06,
GS4_24110 on 2026-11-28). Criteria: `FROZEN_CRITERIA.md`, committed alone first (3537e6f81). Script: `d4_alma_status.py`,
6/6 checks PASS. MUTATE (`D4_MUTATE=1`) drops the M★ term of σ_Δv, and K4 fails (5/6, exit 1).

κ = ½ is FITTED. The two footings are never pooled. One disc excludes no model. Not theory closed. Nothing here says the data
favour the framework. No download, no archive query. No campaign file or seal was edited (K6).

## 1. What data are expected, and when
- **U4_27928.** ALMA 2024.1.00100.L (CONDOR, PI Rizzo), CO(2-1), band 3, 0.066″ beam, 6.3 h. Public **2026-11-06**.
- **GS4_24110.** ALMA 2025.1.01377.L (PI Boogaard), [CI](2-1) plus continuum, band 6, 0.089″ beam, 3.9 h. Public **2026-11-28**.
- Both dates come from CFG570's archive metadata. K5 checks that they equal the plans' dates. Nobody has re-checked them on
  the archive (A-X8).
- **Nothing is on disk.** No file in the repo carries either programme ID or target name (P4e). The record also holds no MOUS UID.
- CFG943 is the Gaia DR4 lane, not ALMA. Its "power gap" is about wide binaries.

## 2. Is the harness complete?
**Yes, on MOCK data, for every addendum.** I did not re-run the mock cubes. The CFG942 history already shows each addendum
implemented, with the result committed:
- CFG806 clarification and CFG809 clarification: 826ebb739.
- CFG809 addendum A and CFG806 addendum A: 90bdb0153.
- CFG809 addenda B, C and D: 9dcfc3ce4, 88db01f47 and b6fa9901d.

K1 passes 27/27 in every run. The last commit holds both MUTATE controls on mock data. Both bite:
- U4: G1's selection-aware S/N is −0.30, so G1 fails and the run exits 1.
- GS4: under addendum D, a fresh mask in the shifted window gives S/N +0.29, below 3, and the run exits 1.

Two caveats are already in the record (b6fa9901d), and they still stand:
- Both bites rest on the selection-aware null. In the shifted window the literal S/N passes on pure noise (GS4 11.0, U4 8.6).
- If GS4's 1.875 GHz spw is centred on 270 GHz, the run has no MUTATE control at all.

## 3. Honest power (from the sealed numbers, using each governing plan's own statistic)
**Expected outcome: nothing is scored on either disc.**
- The record's forecast (CFG942 R7) puts G1's S/N at native resolution at 0.18–0.58 for U4 and 0.04–0.15 for GS4. That is for an
  extended disc carrying the framework's required gas. G1 needs 5.
- Neither plan has a taper branch (A-U12, A-G14). So the expected result on both dates is "G1 FAIL, upper limit".
- Under the expected outcome, the separation is zero on both discs.

**Ceilings with perfect data** (zero flux noise, gas exactly at one model's need):

| disc | pair | best z (noise-free) | where | z with a 5 km/s V_c error |
|---|---|---|---|---|
| U4 | framework vs R-H, ν_mono (the governing kernel) | 4.34 | canonical, V_c 250 | 3.25 (Rg = Rd F-DESI) |
| U4 | framework vs R-H, n=1 | 5.22 | canonical, V_c 250 | 3.53 |
| U4 | framework vs R-H, n=2 | 2.46 | alt, V_c 250 | 2.14 |
| U4 | n=1 vs n=2 | 5.09 | alt, V_c 225, F-DESI | 3.08 |
| GS4 | framework vs R-H (σ, non-FLOOR) | none: R-H is FLOOR (ν_mono, n=1) | | |
| GS4 | framework vs R-H, n=2 | 1.45 | | |
| GS4 | n=1 vs n=2 | **0.51** | every branch ≤ 0.51 | |

How to read the table:
- **U4's ≥ 3σ ceiling lives in a narrow V_c window, about 240–260 km/s.** At 275 km/s the ceiling is 1.6 (canonical) and 2.1 (alt).
  At 300 km/s it is about 1.0–1.3. Above the sealed grid, recomputed with CFG571's functions (CFG806 §2's rule), it is 0.78 / 0.61 /
  0.40 at 325 / 350 / 400 km/s on the canonical footing and 0.95 / 0.74 / 0.50 on the alt footing. KMOS3D's integrated Hα σ of
  224.5 km/s hints at V_c > 300 km/s (CFG942 README).
- **U4's 4.3σ also depends on the owner's A-U15 choice.** That choice keeps the 0.2 dex M★ systematic out of the required range.
  At V_c 250 (canonical), R-H's requirement at M★ − 0.2 dex is 10.37. F-DESI's nominal requirement is 10.42. So the plan's own
  stellar systematic moves the rival onto the framework. Propagated, the separation is 0.00 at V_c 250 and 275, and 0.48 at 300.
  CFG942 already said this in words (A-U15). These are the numbers.
- **GS4 cannot tell n=1 from n=2 under CFG809.** The gas needs differ by 0.19–0.68 dex (R_g = R_d). Inside R_e, though, the stars dominate
  V_bar, and σ_Δv carries 0.2 ⊕ 0.2 dex. So every n=1-vs-n=2 pair reads z ≤ 0.51.
- **GS4's framework-vs-rival split is a FLOOR-rule statement, not a σ separation.** Taken alone, R-H's Δ_v is at most 1.80σ. There
  are 14 ν_mono R-H FLOOR rows, and the FLOOR persists at M★ − 0.2 dex in 6 of them (all at M★ 10.89).

**Plain answer to "is any disc ≥ 3σ?"** Under the expected sensitivity, no. With perfect data, only U4, and only if three things
hold: V_c falls in about 240–260 km/s, the M★ systematic stays outside the range (A-U15), and the V_c error is about 5 km/s. GS4 never
reaches 3σ for any pair.

## 4. What is crisp and could be fixed before data arrive
1. **The canonical law's sealed prediction has no governing reading.**
   - THEORY_CANONICAL_2026-10-21_DRAFT.md:35 states the law as g_N = g²/(g + a0). That is n=1, the AG4e kernel.
   - The governing plans score only CFG571's ν_mono seal. No file in either plan directory names AG4e or AG4d (P4a: 0 of 11 files).
   - So the November verdict lines will be about the ν_mono kernel, which the canonical file calls "a declared variant". AG5's law-form
     reading is the only place n=1 and n=2 are read, and AG5 carries no verdict weight.
   - On U4 this matters, because n=1 vs n=2 reaches z 5.09 noise-free at V_c 225 (alt footing).
2. **A record statement is too strong.** argon_push/AG4e_n1_alma_seal/README.md:26 says GS4's gas "is also a law-form test: little
   gas favours n=1 … ≥ 10¹⁰ favours ν_mono or n=2". Under the governing CFG809 statistic, every n=1-vs-n=2 pair is ≤ 0.51σ. The
   ordering n=1 < ν_mono < n=2 is real, but this disc cannot resolve it.
3. **THEORY_CANONICAL_2026-10-21_DRAFT.md:316 gives the ν_mono range.** It says "framework needs log M_gas ~9.1–10.7". That is the
   ν_mono range. Under the canonical n=1 law at M★ 10.89 on the alt footing, both F-DESI and F-flat are FLOOR: any [CI] detection then
   puts the canonical-law framework "in tension (FLOOR)" on that branch. Even under ν_mono, F-flat at M★ 10.89 alt is FLOOR.

**Proposed owner addendum** (wording only; not committed into any campaign directory):

> *CFG806-U4 and CFG809-GS4, addendum E (before any data).* The verdict kernel stays ν_mono, as sealed in CFG571. The canonical
> law's own seal, AG4e (n=1, sha 9802de0d…), and AG4d (n=2, sha d64727b5…) are scored by the same §3–§5 rules, gates and readings
> as a labelled parallel reading per kernel, never pooled with ν_mono or with each other. Their requirement at the measured V_c is
> recomputed with CFG571's head and the kernel swapped, as AG4d/AG4e did. At the sealed grid points it must reproduce the seal
> exactly. Each report states which kernel each line is about. The canonical statement's §6 ALMA rows quote the n=1 requirement
> beside the ν_mono one. No law-form statement is made from GS4 alone (the n=1 vs n=2 ceiling is ≤ 0.51σ under §4).

The alternative is to make n=1 the verdict kernel. That is the owner's choice. Either way, the CFG942 harness would need a kernel
switch, tested on MOCK before 2026-11-06.

## What this lane does not show
- It does not re-verify the archive dates or sensitivities, and it does not check whether the archive products will be tapered.
- The power numbers are ceilings: zero flux noise, a 5 km/s V_c error, and gas set exactly at one model's need. They are not forecasts
  of the measured result.
- It does not re-run the MOCK cubes. Harness completeness is taken from the committed CFG942 outputs and their K1 rows.

## Files
`FROZEN_CRITERIA.md`, `d4_alma_status.py`, `d4_alma_status.out`, `d4_alma_status_results.json`, `d4_alma_status_MUTATE.out`,
`d4_alma_status_results_MUTATE.json`. Run with `OMP_NUM_THREADS=1 nice -n 10 python3 -B d4_alma_status.py`, which takes seconds and
under 0.3 GB.

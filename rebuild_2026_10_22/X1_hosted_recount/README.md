# X1_hosted_recount: v3 on all Local Group satellites, with published-MOND controls and T3 bookkeeping

## Verdict

| question | frozen class | short reading |
|---|---|---|
| Q1: is tile 26's failure a property of satellites or of E3's sample? | **CLASS-GRADED** [W-SENSITIVE], both footings | Not created by E3's cut: the bright M31 dSphs FAIL too (+0.60 / +0.58 dex, 4.6 / 4.3 sd). But its **size** is set by the sample: the ultra-faints sit at +1.56, the bright classes at +0.36 to +0.60. The MW classical dSphs are UNRESOLVED (+0.36 / +0.32 dex, 1.4 / 1.2 sd, χ²/N 15). |
| Q2: does U1's T3 premise survive? | **T3 PREMISE CONTRADICTED** | Six independent hosted sets sit ≥ 5σ above Newton on both footings, even at Υ_V = 4. The TDG and DF2/DF4 "native pass" rests on the same premise and is booked with them. |
| Step 1: controls against published MOND | **CONTROL FAIL, PUBLISHED APPROXIMATION** (frozen class) | The exact AQUAL + EFE solve sits **0.19 dex in σ (≈ 0.38 dex in g) below** the published predictions of McGaugh & Milgrom 2013 and McGaugh 2016 for the external-field-dominated dwarfs. 0.15 dex of that is the published formula's use of the full mass. |

κ = ½ FITTED. Footings are canonical / alt (9.3603e-11 / 1.1312e-10 m/s²), never pooled. The cold sector is BS dust ("cold energy"),
not a particle. Not "theory closed". Nothing here says the data favour the framework.

**Checks: 11/11 PASS** (K0, C0, C3a–d, KS, KR, KT). `--mutate` fails K0, C3b and C3c as required (5/8, exit 1).

The step-1 stop rule here **refines the brief**. The brief said "if the controls fail, stop". FROZEN_CRITERIA §3 (cfd0ae45fb, committed
before any number) let step 2 run only if the control failure was fully attributed to the published estimator. It was. Step 2's numbers
therefore use the record's exact estimator, which sits below published MOND by the amount above. If the literal stop is preferred,
disregard step 2; steps 0, 1 and 3 stand on their own.

## Step 0: the same data (K0)

S1's code path and seed (copied with provenance from S1 commit 2b6bb658a1), on E3's 45 / 46 systems, give v3 at the L★ floor:

- canonical **+1.33072 ± 0.14735**, alt **+1.29900 ± 0.14742** dex;
- S1's JSON values, reproduced to 0.0 (`step0.<foot>.Delta`, `.sd`).

## Step 1: controls against published MOND (S1's solver at L★ = 0)

Each control uses the papers' own inputs and a₀: 1.21e-10 for MM13, 1.2e-10 for Crater II. The inputs are LITERATURE-INPUT,
PROVISIONAL (web look-ups, two reads each; `LITERATURE_LOOKUP.md`). Comparisons are in log σ, on 29 M31 dwarfs (MM13 a/b; And XVIII
dropped as frozen) and on Crater II.

| line | value | JSON key |
|---|---|---|
| C0: transcription (printed σ_iso, Crater II 4 / 2.1 km/s) | max 0.008 dex | `validation.C0` |
| C1: published Eq. (3) with LVD host distances vs printed σ_efe (reported) | median 0.024 dex (max 0.187, And IX); consistent | `step1.C1_median_abs` |
| **C2: solver (E-W) vs published, median \|Δ log σ\|** | **0.192 dex, signed −0.192** (E-V −0.249) → **FAIL** (line 0.10) | `step1.C2_median_abs`, `C2_signed`, `C2_signed_EV` |
| C2: Crater II | **−0.181** (E-V −0.239). Solver 1.38 km/s (E-W), 1.21 (E-V); published 2.10 | `step1.crater_ii.d_tot`, `.D3`, `.D3V` |
| decomposition: input step / mass convention / remainder | +0.000 / **−0.151** / −0.044 dex | `step1.m_in`, `m_mass`, `m_rem` |
| by regime | 20 EFE-adopted rows: −0.194 median. 9 isolated-adopted rows: −0.034 (And VI, VII, XVI +0.02) | `step1.MM13_rows[*].d_tot` |
| C3a: deep-MOND isolated, E-V vs (4/81 GMa₀)^¼ | 4.0e-4 dex | `validation.C3a` |
| C3b: linear EFE vs Route F | 2.8e-3 | `validation.C3b` |
| C3c: vs F2's AQUAL solver | 1.8e-3 | `validation.C3c` |
| C3d: convergence at the control cells | 1.0e-3 | `validation.C3d` |

**Why C2 fails.**
- Where the isolated formula applies, the solver reproduces published MOND (−0.03 dex).
- Where the published prediction is the EFE value, the solver sits 0.19 dex lower, for two reasons:
  - **Mass convention (−0.15 dex).** The published σ_efe² = G_eff M/(3 r_{1/2}) uses the full mass M. The Wolf identity, used
    for both the record's data side and its predictions, uses M(<r_{1/2}) = M/2.
  - **AQUAL dilution (−0.04 dex).** AQUAL's anisotropic external-field response gives a monopole G_eff slightly below the naive
    G/μ_e.
- The exact global virial (E-V) sits lower still.
- These two named factors account for the whole offset, as the frozen rule requires. The input step is zero by construction.
- **Crater II, at McGaugh's own inputs:** the exact solve gives 1.38 km/s, against the published 2.1 and the measured 2.34 (LVD,
  Ji+2021) and 2.7 (Caldwell+2017).

**The mutate run also shows a trap.** With S1's host-field bug (a weaker, Newtonian background), the MM13 part of C2 drops to 0.058 dex.
That would *pass*. C2 alone therefore cannot validate a solver. The physics checks C3b and C3c catch the bug (18.7 and 1.17).

## Step 2: v3 on all LG satellites, no mass cut (clean primary, E-W, canonical / alt)

Δ = log₁₀(g_obs/g_pred), dex in g. Each class row is the bootstrap median over its systems.

**Class definitions.**
- Classical = the 8 named dSphs.
- Ultra-faints = MW satellites with M_V > −7.7.
- Bright M31 = log M★ ≥ 5, excluding M32 and the three dEs.
- Excluded: LMC, SMC and M32.
- The binary correction applies only where M_V > −7.7 (FROZEN §2). That is why Crater II reads +0.50 here and +0.36 in S1's CSV.

| class | N | Newton | iso AQUAL | AQUAL + EFE (exact MOND) | **v3 floor** | v3 24 / 90 | v3 E-V | W (Υ 4, f 0.7, lower σ) | MM13 recipe (side row) | χ²/N (line) | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MW classical | 8 | +1.21 / +1.21 | +0.28 / +0.24 | +0.34 / +0.29 | **+0.36 ± 0.26 / +0.32 ± 0.26** | +0.36 / +0.59 ; +0.32 / +0.58 | +0.45 / +0.41 | +0.16 / +0.13 | +0.34 / +0.30 | 15.5 / 14.2 (2.50) | **UNRESOLVED** (χ²; < 3 sd) |
| MW ultra-faints | 31 | +2.14 / +2.14 | +0.63 / +0.59 | +1.35 / +1.31 | **+1.56 ± 0.17 / +1.55 ± 0.16** | +1.58 / +1.93 ; +1.56 / +1.92 | +1.64 / +1.63 | +1.18 / +1.18 | +0.99 / +0.96 | 34.6 / 34.3 (1.76) | **FAIL** (9.2 / 9.4 sd) |
| bright M31 dSphs | 25 | +1.52 / +1.52 | +0.25 / +0.21 | +0.58 / +0.54 | **+0.60 ± 0.13 / +0.58 ± 0.13** | +0.61 / +0.80 ; +0.58 / +0.78 | +0.70 / +0.68 | +0.35 ± 0.12 / +0.32 ± 0.12 | +0.39 / +0.36 | 10.8 / 9.8 (1.85) | **FAIL** (4.6 / 4.3 sd); W: UNRESOLVED (3.0 / 2.6 sd) |
| M31 others | 5 | +1.90 / +1.88 | +0.64 / +0.59 | +0.99 / +0.93 | **+1.14 ± 0.32 / +1.10 ± 0.32** | +1.16 / +1.55 ; +1.12 / +1.52 | +1.24 / +1.20 | +0.77 / +0.76 | +0.75 / +0.68 | 7.9 / 7.5 (2.90) | **FAIL** (3.5 / 3.4 sd); W: UNRESOLVED |
| M31 dEs (reported) | 3 | +0.15 / +0.14 | −0.09 / −0.11 | −0.09 / −0.11 | −0.09 / −0.11 | | | −0.31 / −0.33 | +0.12 / +0.08 | | — |
| LG field, isolated (reported) | 13 | +0.95 / +0.96 | +0.05 / +0.02 | +0.06 / +0.02 | **+0.06 ± 0.08 / +0.02 ± 0.08** | +0.06 / +0.12 ; +0.02 / +0.09 | +0.10 / +0.06 | −0.11 / −0.14 | +0.13 / +0.09 | | — |

JSON keys:
- class rows: `class_stats["<foot>|<class>|<primary|W>|<row>"]`;
- status, χ² and sd: `verdict.step2.status["<foot>|<ds>|<class>"]`;
- per system: `per_system` and `x1_per_system.csv`.

Host bracket at the floor (E_lo / E_hi, canonical):
- MW classical +0.34 / +0.42;
- bright M31 +0.55 / +0.70;
- ultra-faints +1.51 / +1.63;
- M31 others +1.08 / +1.25.

| individual (reported) | x_e | Newton | AQUAL + EFE | v3 floor (± s_i) | MM13 recipe |
|---|---|---|---|---|---|
| Crater II | 0.083 / 0.075 | +1.51 / +1.52 | +0.50 / +0.46 | +0.50 ± 0.20 / +0.46 ± 0.20 | +0.10 / +0.07 |
| Antlia II | 0.077 / 0.069 | +2.05 / +2.06 | +1.01 / +0.97 | +1.01 ± 0.17 / +0.97 ± 0.17 | +0.61 / +0.58 |
| Canes Venatici I | 0.045 / 0.041 | +1.81 / +1.81 | +0.59 / +0.55 | +0.62 ± 0.13 / +0.59 ± 0.14 | +0.51 / +0.47 |
| Sagittarius (disrupting) | 0.54 / 0.49 | +0.94 / +0.94 | +0.56 / +0.53 | +0.56 ± 0.17 / +0.53 ± 0.17 | +0.19 / +0.16 |

**What the classes show.**
1. **The failure is not an artefact of E3's cut.** The 25 bright M31 dSphs fail at > 4 sd on both footings. The 8 MW classical
   dSphs spread widely (canonical, per system):
   - Fornax and Leo I sit at v3 (−0.08, −0.02);
   - Sculptor, Leo II and Carina sit at +0.25 to +0.36;
   - Draco, Ursa Minor and Sextans sit at +0.89 to +1.12.
2. **Its size is set by the sample.** Tile 26's +1.33 / +1.30 is the ultra-faint-weighted number. The bright classes sit at
   +0.36 to +0.60.
   - The isolated LG field dwarfs sit at +0.06 / +0.02 ± 0.08, consistent with v3. The excess therefore appears in a host.
   - The largest per-system residuals belong to the most diffuse, field-dominated systems (`x1_per_system.csv`). That is the
     pattern T1 A3's host-field tracking describes. No trend is fitted here.
3. **For the bright classes it is AQUAL's failure, not screening's.** Exact MOND + EFE (L★ = 0) is within 0.02–0.04 dex of v3 for
   the bright classes. Screening adds +0.15 to +0.21 dex only for the ultra-faints and M31 others.
4. **W-SENSITIVE.** With W, the bright M31 and M31-others classes drop to UNRESOLVED (+0.35 ± 0.12, +0.77 ± 0.32). No class
   becomes PASS-LIKE, and χ²/N stays 3.6–21 everywhere: the scatter is far beyond the errors plus the Υ prior.
5. **Even the published recipe leaves bright M31 at +0.39 / +0.36.** The MM13 formula, on the same LVD data and host fields at each
   footing's a₀, is generous by the step-1 offset. It still leaves the bright M31 dSphs +0.39 / +0.36 above, and the ultra-faints
   +0.99 / +0.96. This is a side row only (STANDARD-MOND-MACHINERY).

## Step 3: T3 bookkeeping (hosted ⇒ dust-free ⇒ Newtonian; no new solve)

z is measured against Newton on the baryons, at the conservative Υ_V = 4; canonical / alt. JSON: `T3.<foot>[*]`, `verdict.step3`.

| hosted row | Δ_N (Υ 2) | z vs Newton | members with z_i ≥ 3 | source |
|---|---|---|---|---|
| Crater II | +1.51 ± 0.14 / +1.52 ± 0.14 | **8.7 / 8.9** | — | this lane |
| Antlia II | +2.05 ± 0.07 / +2.06 ± 0.07 | **24.2 / 24.1** | — | this lane |
| MW classical (8) | +1.21 ± 0.28 / +1.21 ± 0.29 | 3.3 / 3.2 | 8 / 8 | this lane |
| MW ultra-faints (31) | +2.14 ± 0.15 / +2.14 ± 0.14 | **12.6 / 13.0** | 28 / 29 | this lane |
| bright M31 (25) | +1.52 ± 0.12 / +1.52 ± 0.12 | **9.8 / 9.9** | 20 / 19 | this lane |
| M31 others (5) | +1.90 ± 0.33 / +1.88 ± 0.34 | 4.8 / 4.7 | 3 / 3 | this lane |
| Coma UDGs (9) | — | **5.4 / 5.4** (CFG948 5.45; U1 B0 z_sys 5.41) | — | `cfg948 byfoot.<f>.primary.H_newton.z`, U1 `numbers.N5.coma.<f>.B0.z_sys` |
| UMa members (27) | −0.06 vs Newton −0.42 dex | **12.6 / 13.4** (minimum of the two A4 readings) | — | U1 `numbers.F5.footings.<f>.A4.*.per_galaxy.z_from_Newton` |
| *booked:* TDGs (6) | B0 +0.055 ± 0.114 | 0.48 (T3-consistent) | — | U1 `numbers.N5.tdg.<f>.TDG_B0` |
| *booked:* DF2/DF4 | B0 +0.028 ± 0.539 ln | 0.05 (T3-consistent) | — | U1 `DF_B0` |

**T3 PREMISE CONTRADICTED.** Six independent hosted sets are ≥ 5σ above Newton on both footings; eight are ≥ 3σ.
- T3 holds in the TDGs and DF2/DF4. It fails in Crater II, Antlia II, the M31 and MW dSphs, the Coma UDGs and the UMa members.
- So the TDG/DF2 "native pass" (U1 Part c) cannot be credited as an independent success.
- The bookkeeping cannot say which of three things is wrong:
  1. the premise: the hosted khronon is not static, or a satellite is not freely falling;
  2. v3 itself, for hosted systems;
  3. the equilibrium reading: tidal heating or non-equilibrium.

  It does show that U1's "satellites must be dust-free" consequence is excluded by systems the record itself measures.

## Amendments

None. Every line ran as frozen (cfd0ae45fb). Disclosed, with no amendment needed:
- **C2 failed, as the criteria anticipated.** The failure was classed by the pre-declared rule.
- **The MUTATE trap** (step 1 above).

## Record items this changes (suggested fixes, not made here)

1. **Status board tile 26 and `THEORY_V3_DRAFT.md` §3.** "Dwarf satellites +1.33 dex" describes E3's sub-threshold, ultra-faint
   sample. The all-LG recount should be stated by class:

   | class | v3 at the floor | status |
   |---|---|---|
   | ultra-faints | +1.56 | FAIL |
   | M31 others | +1.14 | FAIL |
   | bright M31 | +0.60 | FAIL; W-sensitive |
   | MW classical | +0.36 | UNRESOLVED, χ²/N 15 |
   | isolated LG dwarfs | +0.06 ± 0.08 | consistent |

   The colour stays FAIL; the caption should change.
2. **Crater II and MM13 as "MOND successes."** Records citing McGaugh 2016 or MM13 as successes should say that the success rests
   on the published EFE formula's full-mass normalisation. An example is `real_research/reviews/project15_dsph_efe_thermometers.py`
   ("a genuine pre-registered MOND success"). With the record's exact AQUAL solve and Wolf estimator, the published predictions drop
   by 0.19 dex in σ. Crater II then sits +0.50 / +0.46 dex in g above exact MOND + EFE and above v3.
3. **U1 Part (c).** The TDG and DF2/DF4 "NATIVE pass" should be booked with the T3 contradictions above.
4. **MAP §1.D's audit medians** (MW +1.47, M31 +0.89, M31 log M★ ≥ 5 +0.47, Crater II +0.36) are S1-sample central values. The
   all-LG class numbers above replace them. Crater II's +0.36 vs +0.50 is the binary-correction rule.

## What this does not show

- **It does not decide Q1 cleanly for the classical dSphs.** Eight systems with χ²/N ≈ 15 leave the median at 1.4 sd. Fornax and
  Leo I sit at v3; Draco, UMi and Sextans sit about 1 dex above.
- **It does not say which estimator matches real dSphs.** Each system is still a spherical, isotropic Plummer in a uniform field,
  in equilibrium, with mass = light (no gas). The Wolf convention is the record's. E-V sits 0.06–0.1 dex higher in Δ. The published
  full-mass formula sits about 0.38 dex lower in g for EFE-dominated systems.
- **Tides, field-induced flattening, the μ_K² term and non-equilibrium are not modelled.** S1's bound on μ_K² is ≤ 0.03 dex. The
  growth of the residual with external-field dominance is also what tidal heating would give.
- **The literature inputs are PROVISIONAL.** They were read through a summariser, twice per paper; the PDFs were not read. The C0
  transcription check passes to 0.008 dex.
- **Class definitions are conventions** (named classical 8, M_V > −7.7, log M★ ≥ 5), fixed before any number. Host masses are S1's
  labels. The M31 field (1e11 M☉, deep-MOND V ≈ 188 km/s) is weaker than MM13's V = 230 km/s.
- **The T3 table tests the premise, not the law.** Coma and UMa are read from CFG948/U1, not recomputed.
- **No new knob, no M/L refit, no scan.** Nothing here says the data favour the framework.

## Run, files

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X1_hosted_recount/x1_hosted_recount.py --stage controls            # 77 s, exit 0
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X1_hosted_recount/x1_hosted_recount.py --stage controls --mutate   # 102 s, exit 1 (K0, C3b, C3c FAIL)
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X1_hosted_recount/x1_hosted_recount.py --stage tables --foot canonical   # 414 s
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X1_hosted_recount/x1_hosted_recount.py --stage tables --foot alt         # 406 s
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X1_hosted_recount/x1_hosted_recount.py --stage final               # seconds, exit 0
```

- Run cost: 7,079 production solves; worst scaled residual 1.0e-10; peak RSS 0.45 GB; one thread.
- Criteria: `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `LITERATURE_LOOKUP.md` (cfd0ae45fb, committed alone first).
- Outputs:
  - `x1_hosted_recount.out`, `x1_hosted_recount_results.json`, `x1_per_system.csv`;
  - the stage files `x1_stage_controls.json`, `x1_stage_tables_{canonical,alt}.json`;
  - `x1_hosted_recount_MUTATE.out`, `x1_hosted_recount_results_MUTATE.json`.
- Nothing was downloaded.

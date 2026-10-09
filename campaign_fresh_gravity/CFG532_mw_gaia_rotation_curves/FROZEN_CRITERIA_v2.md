# CFG532b FROZEN CRITERIA: the review's other Gaia-era curves, plus a combined slope test by tracer class

This file is written and committed alone, before CFG532b's script exists and before any of these tables' values enter a score (2026-10-09). CFG532's own frozen file (FROZEN_CRITERIA.md, 9d73cbc17) and its results (af144e0a8) are unchanged and are not re-opened.

- κ = ½ is FITTED. Both footings are used and never pooled (canonical 9.36e-11, alt 1.13e-10 m/s²). The kernel is ν_mono.
- The cold energy's MASS is still required. Nothing here may be reported as "theory closed" or as the data favouring the framework.
- The DR4 preregistration and the *_HASH files are READ ONLY.

## 0. Sources

The owner approved the downloads in the coordinating session on 2026-10-09, and the coordinator fetched the arXiv sources. Their bytes and SHA-256 are in FETCH_LOG_532b.md, which is copied into this lane. They are stored in ../_external_data/cfg532_work/src/<id>/. This lane fetches nothing.

Planned extraction, read from the .tex only (no digitising). The table locations were found by their captions, before freezing:

| curve | file : table lines | R0 / solar motion (paper's own) | errors in the table | class | role |
|---|---|---|---|---|---|
| Wang+23 (LIM, all Gaia DR3) | 2211.05668/HFW-3DRC-v1.tex : 777–802 (label tabrot) | R0 8.34, (U,V,W)sun = (11.1, 12.24, 7.25) (lines 201–202) | statistical | RGB/LIM, group LIM | scored |
| Jiao+23 (Wang re-binned, with full systematic budget) | 2309.00048/rc_mw_z3.tex : 4–27 | R0 8.34 for this curve (AA tex footnote, line 344) | include systematics (per the paper's caption, line 294) | RGB/LIM, group LIM | scored |
| Zhou+23 (APOGEE + LAMOST LRGB) | 2212.10393/GRC.tex : 447–488 (label tfrc) | read from the text by the script, where stated; otherwise "not located" | statistical (the systematics are in the text) | RGB/LIM, group APOGEE-RGB | scored |
| Sylos Labini+23 "DR3+" | 2302.01379/ms.tex : 284–335 (label tabrot) | R0 8.122 (line 210) | as published | RGB/LIM, group LIM (a combination built on Wang+23) | scored, REPORTED ONLY (never combined) |
| Feng+26 (Gaia DR3 classical Cepheids) | 2512.21780/Main.tex : 233–252 (Table1) | R0 8.275, Z 0.025 (line 170) | bootstrap (statistical) | Cepheid | scored |
| Mróz+19 (Cepheids) | 1810.02131/pap.tex: the only table is model parameters | 8.09 (fig. caption) | — | Cepheid | **NOT SCORED** (no RC table) |
| Ablimit+20 (Cepheids) | 2004.13768/arxiv.tex: no table | — | — | Cepheid | **NOT SCORED** (no table) |
| Sylos Labini 2024 (off-plane generalised RCs) | 2410.14307/manuscript.tex: its only table is σ_vz coefficients | — | — | — | **NOT SCORED** (no in-plane RC table) |

Ou+24 and Eilers+19 come from CFG532, and their numbers are the ones in cfg532_results.json. For the combined test they are re-scored by the same script with the same code path.

The script parses every table from its .tex line range. It checks that the row count matches the table's rows, and it prints the file and line of the first and last row. Any column beyond (R, V, σ), such as Zhou's star count, is ignored.

## 1. Scoring (the CFG532 method, unchanged)

- **Machinery:** cfg532_mw_curves.py's law and scoring functions (`v_model`, `score`, `slope`, `fit_nfw`, `fit_kepler`), executed read-only from the committed CFG532 script.
- **Baryons:** McMillan17 census baryons are HELD fixed. The rules are RM-v and RM-φ (with ALG as a reference), in both footings. M*_need is post hoc, reported only, with z against 5.43 ± 0.57e10. χ², p, NFW and Kepler fits, and the verdict labels are all exactly as in CFG532 §4.
- **Errors (primary):**
  - A curve whose table errors are statistical only (Wang+23, Zhou+23, Feng+26) gets a declared 3% systematic added in quadrature. This is the convention CFG532 used for Eilers and inside 22 kpc for Ou.
  - Jiao+23 and SL23 are used as published.
  - Variants are reported, and a verdict flip is reported as "systematics-dependent":
    - S1: table errors only.
    - S2: 5% added in quadrature (not applied to Jiao or SL23).
    - S3: radii rescaled to R0 = 8.178 by R × 8.178/R0_paper. This is crude, and the velocities are not re-derived.
- **Slope window:**
  - RGB/LIM class: dlnV/dlnR over 15 ≤ R ≤ 27.5 kpc, as in CFG532.
  - Cepheid class: the curves stop near 18–20 kpc, so the primary window is 10 kpc ≤ R ≤ R_max of the curve. The 15 ≤ R ≤ R_max slope is also reported.
  - A curve with fewer than 4 points in its window has a NOT DIAGNOSTIC slope and does not enter the combination.
  - The law's slope is fitted at the same radii with the same weights.

## 2. Combined slope test (declared before scoring)

- **Statistic per curve:** Δ_i = b_data,i − b_law,i, with σ_i = σ_b,i, the LS slope error from the curve's primary errors. This is computed per footing × rule at census baryons.
- **Shared data:**
  - Jiao+23 re-derives Wang+23's data, and SL23 DR3+ is built on Wang+23. These three form ONE group (LIM).
  - Eilers+19, Ou+24 and Zhou+23 all use APOGEE red giants with Gaia astrometry and share stars. They form ONE group (APOGEE-RGB).
  - Exactly one curve per group enters a combination.
- **RGB/LIM primary combination:** Ou+24 (APOGEE-RGB) + Jiao+23 (LIM). Each is the group's member with the widest R range and a full systematic budget.
  - Combined Δ̄ is the inverse-variance mean, and Z = Δ̄/σ̄.
  - It is computed as (i) independent and (ii) with a declared correlation ρ = 0.5 via GLS, because the two still share Gaia DR3 astrometry and the R0/V_sun conventions.
- **Variants (reported):** every other one-per-group pair, i.e. {Eilers, Ou, Zhou} × {Wang, Jiao}, each under the independent and ρ = 0.5 versions. The headline is the primary pair, and the range across all pairs is printed.
- **Cepheid class:** Feng+26 alone, since Mróz+19 and Ablimit+20 have no table. Its tracer is never combined with the RGB/LIM class.
- **Combined verdict per class × footing × rule:**
  - |Z| ≤ 2: SHAPE CONSISTENT.
  - 2 < |Z| ≤ 3: SHAPE TENSION.
  - |Z| > 3: SHAPE EXCLUDED.
  - NOT DIAGNOSTIC if the combined σ̄ exceeds |b_law − (−0.5)|/2 (the class cannot tell the law from Keplerian at 2σ).
- **Reported only (no verdict):** published linear slopes from the text, where a paper gives one (e.g. Mróz+19 dΘ/dR −1.34 ± 0.21 km/s/kpc), compared with the law's dV/dR on an even grid over the paper's stated range. These are a paper's fit parameters, not a table, so they are flagged as such.

## 3. MUTATE (CFG532B_MUTATE=1, separate *_MUTATE outputs; it must fire, exit 1 = DETECTED)

- **M1, law off** (Newtonian census baryons): p_census < 1e-6 on every scored new curve, in both footings.
- **M2, law on with baryons × 0.5:** p_census < 1e-6 and not CONSISTENT on every scored new curve, in both footings and both rules.
- **M3, injected Keplerian tail:**
  - Each RGB/LIM curve's V at R ≥ 15 kpc is replaced by V_model(15)·(R/15)^−0.5, keeping the curve's own errors. V_model(15) is the curve's interpolated V at 15 kpc.
  - The primary combined Z must then exceed 3 in magnitude (SHAPE EXCLUDED) in every footing × rule. This shows the combination can detect a Keplerian decline.

## 4. Gaia DR4 decider (computed and reported)

- The per-class combined σ̄ that DR4 must beat to separate the law's slope from the combined measured slope at 3σ, and from Keplerian at 3σ.
- The law's census V at 15, 20 and 25 kpc for each footing × rule.

## 5. Disclosures before freezing (dated 2026-10-09)

- To find the tables, I opened the table headers. In doing so I saw a few rows: Jiao+23's first five (9.5–13.5 kpc), SL23's first twelve and last four (inner, and 25.75–27.25), Feng's first three (6.6–8.5 kpc) and Zhou's first one. No slope or score was computed from them.
- The review's summary values were already known: the Wang slope −2.3 ± 0.2, the Jiao slope −2.18 ± 0.23 and γ −0.47 ± 0.15, the Mróz slope −1.34 ± 0.21, and Feng's "mild decline".
- So was CFG532's result, including the law's slope of −0.10 to −0.19 and the Ou-driven shape miss.

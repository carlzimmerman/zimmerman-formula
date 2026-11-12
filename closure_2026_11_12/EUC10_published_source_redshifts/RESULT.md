# EUC10 (PUBLISHED SOURCE REDSHIFTS): RESULT

2026-11-12. Criteria 21578af22b (alone, before any script or match). Scripts and outputs fc728754de.

## Verdict: EUC1-F NOT EVALUABLE / NOT EVALUABLE (canonical / alt). EUC5-F NOT GRADED in all three classes.

Every spectroscopic lensed-source redshift that the reachable public record carries for ECLIPSE positions gives
**14 lenses** (any grade). Only **2 are in sample P** and the same 2 in S; the gate needs 10. Of the other 12, eight fail the
catalogue's `lens_model_success` or `final_sample` flag, three have no stellar mass and one is a large-system lens. Even
counting every unverified NED pointer as real, N(P) would be 3 and N(S) 5. The gates stay open.

All checks pass (null 0, mutation exits 1). KA3: the published 1.366 for L015763 was recovered (Bergamini et al.,
Table 1); that lens fails `final_sample`, so it is not in P. κ = ½ FITTED; not theory closed. Footings never pooled.
No outcome here favours the framework.

## 1. What was matched (`euc10_matches.csv`; all machine-readable, none PROVISIONAL)

| Lens | Grade | z_s | Source of the redshift | In P / S | b law S (can / alt) |
|---|---|---|---|---|---|
| L015871 | A | 1.1748 | DESI SLF IV (MUSE), Q_z 1 | P, S | +0.627 / +0.611 |
| L016382 | A | 2.344 | AGEL DR2 flag 2; AGEL env.; SIMBAD (2024ApJ...970...86S) 2.3443 | P, S | +0.482 / +0.461 |
| L000613 | A | 2.478 | AGEL DR2 flag 3; AGEL env. | model fail | +0.529 / +0.509 |
| L004966 | A | 0.920 | AGEL DR2 flag 2; AGEL env. | model fail | +0.543 / +0.526 |
| L008070 | A | 2.035 | AGEL DR2 flag 2 | model fail | +1.232 / +1.212 |
| L014483 | A | 0.620 | Lemon+2022/2023 (Gaia IV) text; NED | not final | +0.615 / +0.603 |
| L015763 | A | 1.366 | Bergamini+ DR1 Table 1; EUC2 DESI 1.3657 | not final | +0.219 / +0.203 (photo-z) |
| L017819 | A | 1.210 | SuGOHI II compilation (VizieR), lensed quasar | model fail | −0.159 / −0.176 |
| L002353 | A | 3.2068 | NED + SIMBAD, Nord+2016 | large system | −0.474 / −0.495 |
| L008608 | B | 0.8461 | DESI SLF IV, Q_z 1 (lens 4.7″ off) | model fail | +0.734 / +0.718 |
| L013325 | B | 1.4488 | DESI SLF IV, Q_z 1 | model fail | +1.243 / +1.225 |
| L002052 | A | 2.823 | NED (KiDS J0233−3447, 2025ApJ...987L..31L) | no mass | — |
| L005653 | A | 1.2978 | SIMBAD (lensed quasar, Schechter+2017) | no mass | — |
| L014237 | A | 2.375 | NED (DES J0408−5354 images) | no mass | — |

Excluded: L001750 (two differing values, frozen conflict rule; outside P and S). 22 NED objects with a spectroscopic
redshift but no lensed-image type are pointers only (`euc10_ned_pointers.csv`; 1 lens in P, 3 in S).

## 2. Gates (law S, z_l = ECLIPSE photo-z, source at its published redshift)

| Gate | N | b_med [95 %], canonical / alt | Word |
|---|---|---|---|
| EUC1-F, sample P | 2 | +0.554 [+0.482, +0.627] / +0.536 [+0.461, +0.611] | NOT EVALUABLE / NOT EVALUABLE |
| EUC5-F, θ_E < 1.0″ | 0 | — | NOT GRADED |
| EUC5-F, 1.0–1.3″ | 0 | — | NOT GRADED |
| EUC5-F, ≥ 1.3″ | 2 | +0.554 / +0.536 (band +0.03 to +0.32 / +0.31) | NOT GRADED |

Two lenses, both wide (θ_E 1.9–2.1″), each needing 3–4 × Salpeter: not a population, not a grade.

## 3. Readings (not gates)

- All 11 matched lenses with valid EUC1 inputs (any flag): b_med +0.543 [+0.219, +0.734] / +0.526 [+0.203, +0.718];
  f₂₅ = 0.73. Law B on S: +0.593 / +0.580. At the DESI deflector redshift: unchanged (neither P lens has one).
- **Selection.** Matched (11) vs P: θ_E 1.55″ vs 0.90″, z_l 0.38 vs 0.66, log M★ 11.71 vs 11.42, n 6.0 vs 5.3,
  θ_E/θ_e 0.36 vs 1.07. Published sources favour bright, wide, low-z, group-hosted lenses, exactly where EUC1's map has
  the highest b: any reading on them overstates the P median.

## 4. Part B: population reading (NOT A GATE; never EUC1-F)

P's 3,192 lenses given source redshifts drawn from published imaging-selected samples (10 nearest in lens redshift;
θ_E is not tabulated, so z_l only; 200 draws):

| Sample | N | median z_l / z_s | b_med canonical | b_med alt |
|---|---|---|---|---|
| AGEL DR2 (DES/DECaLS; flag ≥ 2) | 90 | 0.56 / 1.95 | +0.238 [+0.233, +0.243] | +0.220 [+0.215, +0.225] |
| DESI SLF IV (MUSE; Q_z ≤ 2) | 49 | 0.39 / 1.43 | +0.298 [+0.290, +0.306] | +0.282 [+0.274, +0.289] |

**Bracket: +0.24 to +0.30 (canonical), +0.22 to +0.28 (alt).** Between the 0.15 and 0.25 lines, so a P sample whose
sources look like these would most likely read NO VERDICT, and would read FAILS if its sources are like SLF IV's.
Intervals are draw spread only. Limits: ground-based selection of bright, wide
arcs; optical/NIR spectroscopy under-samples 1.5 ≲ z ≲ 2.5 and faint high-z sources; Euclid finds fainter, smaller
lenses whose sources are likely fainter and higher; matching on z_l alone ignores the θ_E dependence. Fainter,
higher-redshift sources would lower these numbers (EUC1's z_s = 3 reading is +0.146 / +0.125). HSC/DESI (18), SLF II
(18) and SLF III (6) are below the frozen N ≥ 20 and were not used.

## 5. Checks (all pass)

KA1 SLACS at true z_s +0.0815 / +0.0696 (target +0.082 / +0.070). KA2 L015763 (DESI z_l, z_s 1.3657) +0.2314 / +0.2149
(1.70 × / 1.64 × Salpeter). KA3 published 1.366 recovered. KA4 EUC1 reproduced (3,192; −0.0185 / −0.0439). NULL at
positions +0.3° Dec: 0 accepted (limit 2). MUTATE newton: b_med on P matched +0.554 → +0.665, +0.536 → +0.665; exit 1.

## 6. Deviations and interpretations (disclosed)

1. CDS Strasbourg was down; VizieR and SIMBAD were used via the CfA mirrors. SIMBAD's full list of lensed-type objects
   with a redshift (12,682 rows) was downloaded once and matched locally at the same positions and 10″ radius;
   `gLe`/`gLS` were treated as pointers and quality E as not secure. Neither choice changes N(P).
2. Literature hits were read by eye; each entry in `euc10_build_matches.py` cites file and line and the script checks
   the value is there. AGEL's environment table and Bergamini's Table 1 were read from locally extracted PDF text.
3. The conflict rule was applied literally, excluding one multi-source system (outside P and S).
4. Downloads 193.5 MB of the 200 MB cap (arXiv e-prints 190 MB). No IRSA, ESA or SPARCL query.

## 7. What this says

Published follow-up does not reach Euclid's gate sample (2 of 3,192); EUC1-F stays open until spectroscopy of the
ECLIPSE lenses themselves (Storfer et al., 4MOST) or a grism lane (EUC9). The few lenses with published sources are the
wide, group-type systems where EUC1 located the excess; they read b ≈ +0.5, consistent with EUC1's map and EUC5's rise
with θ_E, and not a population result. The lead's hand estimate: 5–30 overlap is right for all grades (14), wrong for
P (2); Part B's bracket (+0.22 to +0.30) sits inside its "+0.2 to +0.3", untested by any gate.

Files: `euc10_fetch_ned.py`, `euc10_fetch_lit.py`, `euc10_scan_lit.py`, `euc10_parse_samples.py`,
`euc10_build_matches.py`, `euc10.py` and their outputs (`euc10_*.csv`, `.json`, `.out`, `euc10_MUTATE_newton.*`).
Fetched data, not in git: `_external_data/euc10_published_source_z/` with `MANIFEST.txt`.

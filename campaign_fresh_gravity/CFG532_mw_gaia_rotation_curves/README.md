# CFG532: the Gaia-era Milky Way rotation curves (the "Keplerian decline" debate) against the law, with census baryons held fixed

- **Trigger:** Melchiorri & Ruchika, arXiv:2608.10189 (revised 2026-09-12). This is a review of the MW rotation curve and the debate over a Keplerian decline. Its LaTeX source was the only download (see `FETCH_LOG.md`).
- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (9d73cbc17).
- **Script:** `cfg532_mw_curves.py`, which runs in a few seconds at nice 10 with 2 threads.
  - Outputs: `cfg532.out` and `cfg532_results.json`.
  - MUTATE: `CFG532_MUTATE=1` writes `cfg532_MUTATE.out` and `cfg532_results_MUTATE.json`. It exits 1, meaning DETECTED.
- **Re-used, not edited:** CFG514's solver and McMillan17 baryons, and CFG516's round-rule machinery (`Base`, `build_PD`, `rho_b2`). Both are executed read-only.
- **Settings:**
  - κ = ½ is FITTED. Both footings are used and never pooled (9.36e-11 / 1.13e-10).
  - The kernel is ν_mono.
  - The cold energy's MASS is still required.
  - This is not "theory closed". Nothing here says the data favour the framework.
  - The DR4 preregistration and the `*_HASH` files were not touched.

## Scope (owner decision via the coordinator, 2026-10-09)

Only curves already on disk are scored:
- **C1:** Ou+24 Table 1 (37 points).
- **C2:** Eilers+19 Table 1 (38 points).
- **C3:** the review's own 35-entry compilation, parsed from the fetched LaTeX. It is a heterogeneous mix of disc and halo tracers, so it is used as a cross-check only and never enters the overall verdict. **C3d** is the same compilation restricted to R ≤ 26.5 kpc.

**Not on disk, so not scored and not fetched (for owner approval).** Sizes are rough estimates and have not been checked. Each table is a few kB. The arXiv source tarballs are usually 1–10 MB.

| curve the review uses | source | what would be needed |
|---|---|---|
| Wang+23 (Gaia DR3 LIM, 9.5–27.5 kpc) | arXiv:2211.05668, ApJ 942, 12, Table 1 | the table from the arXiv source (~1–5 MB tarball) |
| Jiao+23 (the "Keplerian" curve, 9.5–26.5 kpc) | A&A 678, A208, Table 3. The arXiv id is not in the review's bib; 2309.00048 is recalled and unverified | CDS or the arXiv source (~1–5 MB) |
| Zhou+23 (set aside by Jiao on distance scale) | arXiv:2212.10393, ApJ 946, 73 | arXiv source (~1–5 MB) |
| Mróz+19 (Cepheids, 4–20 kpc) | arXiv:1810.02131, ApJL 870, L10 | arXiv source (~1 MB) |
| Ablimit+20 (Cepheids) | arXiv:2004.13768, ApJL 895, L12 | arXiv source |
| Sylos Labini+23 / Sylos Labini 2024 | arXiv:2302.01379 / 2410.14307 | arXiv source |
| Feng+26 (Cepheids, mild decline 6–18 kpc) | arXiv:2512.21780 | arXiv source |
| halo-tracer points (Huang+16, Ablimit & Zhao 17, Kafle+12, Wegg+19) | MNRAS 463, 2623; arXiv:1708.00170; ApJ 761, 98; MNRAS 485, 3296 | already folded into C3 by the review |
| Põder+23 | **not cited in the review**; not checked | — |

## Results (numbers from `cfg532_results.json`; McMillan17 census baryons HELD; M\*_need is post hoc and reported only)

χ² is computed against N points with nothing fitted. The slope is dlnV/dlnR over 15–27.5 kpc. "Δ" is the gap between the data's slope and the law's, in units of the data slope's error.

| curve | foot | rule | χ²/N | p | M\*_need (z vs 5.43±0.57e10) | slope: law vs data (Δ) | verdict |
|---|---|---|---|---|---|---|---|
| Ou+24 | can | RM-v | 55.9/37 | 0.024 | 6.09e10 (+1.2) | −0.160 vs −0.325±0.074 (−2.2σ) | EXCLUDED (shape) |
| | | RM-φ | 257/37 | 1e-34 | 7.16e10 (+3.0) | −0.119 (−2.8σ) | EXCLUDED |
| | alt | RM-v | 12.9/37 | 1.00 | 5.57e10 (+0.2) | −0.148 (−2.4σ) | EXCLUDED (shape) |
| | | RM-φ | 126/37 | 1e-11 | 6.57e10 (+2.0) | −0.107 (−3.0σ) | EXCLUDED |
| Eilers+19 | can | RM-v | 30.7/38 | 0.80 | 5.85e10 (+0.7) | −0.158 vs −0.278±0.071 (−1.7σ) | **CONSISTENT** |
| | | RM-φ | 199/38 | 1e-23 | 6.87e10 (+2.5) | −0.117 (−2.3σ; −2.0σ at M\*_need) | NEEDS-HEAVY-DISC (+2.5σ) |
| | alt | RM-v | 11.5/38 | 1.00 | 5.36e10 (−0.1) | −0.146 (−1.9σ) | **CONSISTENT** |
| | | RM-φ | 87.4/38 | 9e-6 | 6.31e10 (+1.5) | −0.106 (−2.4σ) | EXCLUDED (shape) |
| C3 compilation (cross-check) | can / alt | RM-v | 56.7 / 36.2 (of 35) | 0.012 / 0.41 | 5.82 / 5.27e10 | −0.156 / −0.144 vs −0.298±0.055 (−2.6 / −2.8σ) | EXCLUDED (shape) |
| | can / alt | RM-φ | 250 / 107 | ≪0.01 | 6.85 / 6.22e10 | −3.3 / −3.5σ | EXCLUDED |

- **ALG reference** (CFG513's radial algebraic law): it needs M\* of 6.67–6.95e10 canonical (+2.2 to +2.7σ) and 6.08–6.32e10 alt. Its shape is −2.2 to −2.9σ off.
- **Variants:**
  - At 7.3e10 (L172 shapes), RM-v canonical fits Ou with χ² 12.7/37.
  - At 6.0e10, RM-φ canonical gives χ² 424 on Ou.
  - The variants never move the law's slope beyond the range −0.104 to −0.190.
- **Overall, as frozen** (the worse of C1 and C2): **EXCLUDED in all four footing × definition cells.** Ou+24's 15–27.5 kpc slope drives this in every cell. C3 agrees.
- **Heavy disc:**
  - RM-v needs essentially the census: z between −0.1 and +1.2.
  - RM-φ needs M\* of 6.3–7.2e10, which is +1.5 to +3.0σ above McMillan's 5.43 ± 0.57e10.
  - The record's 7.3–8.2e10 total-baryon requirement (CFG513, h34) is reproduced for RM-φ and ALG. RM-v largely removes it.

## The fail, checked as hard as a win

1. **The fail is a SHAPE fail, and it is marginal.**
   - RM-v passes the amplitude test on every curve (p 0.02–1.0 at census).
   - Its outer slope is shallower than Ou's by 2.2σ (canonical) and 2.4σ (alt). The frozen threshold is 2σ.
   - The law's slope lies between −0.10 and −0.19 in every cell. The data lie between −0.25 and −0.33. Kepler is −0.5.
   - So the measured decline is about twice as steep as the law gives, and about half as steep as Keplerian. The Keplerian slope is itself 2.4σ (Ou) and 3.1σ (Eilers) away from the data.
2. **The same frozen shape rule also rejects the NFW fitted to the same curve** (post-run diagnostic (a), not a verdict input):
   - The fitted NFW's slope is −0.171 on Ou, a −2.1σ offset, so it would FAIL. It is −2.9σ on C3 and −2.6σ on C3d, and it passes on Eilers at −1.6σ.
   - The law's shape on Ou (RM-v, −0.160) is almost the same as the fitted NFW's.
   - This shape miss is therefore shared by the smooth halo models. It is not specific to the law. It is still a miss, and it is reported as one.
3. **The verdict depends on systematics.** Each paper reports its own systematics:
   - **S2** (5% inner systematic, the top of the authors' range) flips Ou RM-v to CONSISTENT in both footings, and Ou/Eilers RM-φ alt to CONSISTENT.
   - **S1** (random errors only) excludes every law cell at 3.5–9.9σ. It also makes the data slope's error 0.017–0.024, which ignores the stated systematics.
   - **S3** (R0 = 8.34, crude) turns Ou RM-v canonical into NEEDS-HEAVY-DISC.
   - Eilers' own gradient systematic (±0.46 km/s/kpc, post-run (b)) puts RM-v at −1.6 / −1.8σ, which passes. RM-φ comes out at −2.4 / −2.6σ.
4. **The R ≥ 19 kpc points alone do not discriminate.** On Ou, RM-v canonical gives χ² 4.2 over 11 points, and the Kepler fit gives 2.1. The 15% outer systematics absorb both. The discriminating lever is 15–22 kpc.
5. **Not modelled:** non-equilibrium effects (Sgr bending waves, the LMC, Wang's north–south asymmetry) and Jeans re-derivations. They enter only through each paper's stated systematic budget.

**Plain reading:**
- No on-disk curve requires a Keplerian decline.
- With census baryons, the law gets the amplitude right under RM-v and needs a +1.5 to +3σ heavy disc under RM-φ.
- The law's outer slope is about 2–3σ too shallow against Ou+24 and the compilation. That is the same size as the fitted NFW's miss, and it depends on the systematics.
- This is a live tension, not a kill. The review's "extreme" reading (M_dyn ≈ 2e11, near-Keplerian) is not what these tables measure: their slope sits between flat and Keplerian.

## What Gaia DR4 (2026-12-02) must show to decide

- **The law's prediction** is dlnV/dlnR(15–27.5 kpc) between −0.10 and −0.19 for every baryon variant and footing. Heavier discs move this slope by only about 0.02–0.04, so it is a mass-independent test.
- **Census V(20 kpc):**
  - RM-v: 199.5 (canonical) and 206.6 (alt) km/s. The data at 20 kpc lie +1.4 to +1.8 km/s above the canonical value and 5.2 to 5.7 km/s below the alt value.
  - RM-φ: 192.4 (canonical) and 199.3 (alt) km/s. The data lie 8.5 to 9.0 km/s above the canonical value.
- **To decide, DR4 needs a slope error of about 0.04–0.07 or better,** systematics included. That is enough to separate the law from today's measured slopes at 3σ. Separating the law from Kepler at 3σ needs only 0.12–0.13.
- **Decision rule:**
  - If DR4 holds the slope at −0.25 or steeper with σ ≤ 0.04, the law is excluded on shape regardless of disc mass.
  - If DR4 finds −0.20 or shallower, the law's shape passes. Then the remaining question is the RM-φ amplitude, which needs +1.5 to +3σ of extra disc.
  - A Keplerian −0.5 would exclude the law and the smooth NFW alike.

## Controls

- **K1:** CFG516's χ²_RC against Eilers is reproduced to 0.001%.
- **K2:** the compilation parse returns 35 rows covering 6.3–49.0 kpc.
- **K3:** the slope estimator returns exactly −0.5 for a Keplerian curve and 0 for a flat one.
- **K4:** NFW beats bare baryons on Ou (9.9 against 3755).
- **MUTATE: 12/12 cells DETECTED.**
  - M1, the law switched off, gives χ² 3755 / 3476. It would need M\* = 1.2e11 and still fails.
  - M2, the law with M_b × 0.5, gives p < 1e-280 in every cell, and no cell is CONSISTENT.

## Disclosures

- The record's numbers seen before freezing (CFG513, h34, CFG516) are listed in the frozen file, §8.
- **Post-run diagnostics (a)–(c)** were added after the first run. They are labelled in the output and do not feed the verdict.
- **The DR4 slope** is computed on an even grid from 15 to 27.5 kpc, so it is up to 0.012 shallower than the data-weighted slope.
- **The C3 errors** are the review's, and they already include systematics.
- **M\*_need** scales the stars only, with gas held fixed. It is computed as s × 5.43e10; the grid's own stellar mass is 5.45e10.

---

# CFG532b: the review's other curves, from owner-approved arXiv sources, and a combined slope test by tracer class

- **Criteria:** `FROZEN_CRITERIA_v2.md`, committed alone first (fe132d6c7).
- **Script:** `cfg532b_more_curves.py`.
  - Outputs: `cfg532b.out` and `cfg532b_results.json`.
  - MUTATE: `CFG532B_MUTATE=1` writes `cfg532b_MUTATE.out` and `_MUTATE.json`. It exits 1, meaning DETECTED.
  - The CFG532 machinery is executed read-only, so the method is unchanged.
- **Sources:** the coordinator fetched them after the owner approved; see `FETCH_LOG_532b.md`. This lane fetched nothing.
  - Every table is parsed from its `.tex` line range, and the row counts are checked.
  - Nothing was digitised.

## Extraction

| curve | file : rows | N, R range | R0 (paper) | errors used |
|---|---|---|---|---|
| Wang+23 (LIM, all Gaia DR3) | 2211.05668/HFW-3DRC-v1.tex:782–800 | 19, 9.5–27.5 | 8.34; (U,V,W)⊙ 11.1, 12.24, 7.25 | stat ⊕ 3% |
| Jiao+23 (Wang re-binned, with systematics) | 2309.00048/rc_mw_z3.tex:8–25 | 18, 9.5–26.5 | 8.34 | as published |
| Zhou+23 (APOGEE + LAMOST LRGB) | 2212.10393/GRC.tex:452–485 | 34, 5.2–24.0 | 8.122; V_R⊙ 11.1, V_φ⊙ 245.6 | stat ⊕ 3% |
| Sylos Labini+23 "DR3+" (built on Wang) | 2302.01379/ms.tex:289–333 | 45, 5.25–27.25 | 8.122 | as published (REPORTED ONLY) |
| Feng+26 (Gaia DR3 Cepheids) | 2512.21780/Main.tex:238–249 | 12, 6.6–17.6 | 8.275 | bootstrap ⊕ 3% |
| Mróz+19 (Cepheids) | NOT SCORED: no RC table. Its text slope is compared, reported only | — | 8.09 | — |
| Ablimit+20, Sylos Labini 2024 | NOT SCORED: no in-plane RC table | — | — | — |

## Per curve (census baryons HELD; M\*_need post hoc; numbers from `cfg532b_results.json`)

Slope windows are 15–27.5 kpc for RGB/LIM and 10–17.6 kpc for Feng.

| curve | foot | RM-v: χ²/N, M\*_need (z), slope Δσ → verdict | RM-φ: χ²/N, M\*_need (z), Δσ → verdict |
|---|---|---|---|
| Wang+23 | can | 23.6/19, 5.68e10 (+0.4), −3.6σ → EXCLUDED (shape) | 75.7/19, 6.60e10 (+2.1), −4.2σ → EXCLUDED |
| | alt | 31.1/19, 5.06e10 (−0.6), −3.8σ → EXCLUDED (shape) | 40.3/19, 5.91e10 (+0.8), −4.4σ → EXCLUDED |
| Jiao+23 | can | 41.9/18, 5.81e10 (+0.7), −2.9σ → EXCLUDED | 230/18, 6.85e10 (+2.5), −3.6σ → EXCLUDED |
| | alt | 25.6/18, 5.26e10 (−0.3), −3.1σ → EXCLUDED (shape) | 95.7/18, 6.23e10 (+1.4), −3.8σ → EXCLUDED |
| Zhou+23 | can | 71.3/34, 6.21e10 (+1.4), −0.5σ → NEEDS-HEAVY-DISC (+1.4σ) | 305/34, 7.28e10 (+3.2), −1.1σ → NEEDS-HEAVY-DISC (+3.2σ) |
| | alt | 10.7/34, 5.70e10 (+0.5), −0.7σ → **CONSISTENT** | 154/34, 6.70e10 (+2.2), −1.3σ → NEEDS-HEAVY-DISC (+2.2σ) |
| Feng+26 (Cepheids) | can | 81.9/12, 6.79e10 (+2.4), +2.1σ → EXCLUDED | 207/12, 8.03e10 (+4.6), +1.5σ → EXCLUDED |
| | alt | 39.9/12, 6.29e10 (+1.5), +1.9σ → EXCLUDED | 134/12, 7.46e10 (+3.6), +1.3σ → NEEDS-HEAVY-DISC (+3.6σ) |
| SL23 DR3+ (reported only) | can / alt | 358 / 143 of 45, −6.0 / −6.6σ → EXCLUDED | −8.0 / −8.6σ → EXCLUDED |

**Slopes.** These are the measured dlnV/dlnR in the class window, against Kepler at −0.5:
- Wang −0.356 ± 0.058
- Jiao −0.319 ± 0.057
- Zhou −0.186 ± 0.061
- SL23 −0.271 ± 0.020
- Feng −0.026 ± 0.067 (10–17.6 kpc; flat)

The law's slope is −0.10 to −0.17. The NFW fitted to each curve has slope −0.227 (Wang), −0.167 (Jiao), −0.153 (Zhou) and −0.064 (Feng). Its shape misses Wang by −2.2σ and Jiao by −2.7σ.

## Combined slope test (declared groups: APOGEE-RGB = {Ou, Eilers, Zhou}, LIM = {Wang, Jiao, SL23}; one curve per group)

| class | foot | rule | primary Ou+Jiao: Δ, Z (indep.) | Z at ρ = 0.5 | all 6 pairs Z | verdict |
|---|---|---|---|---|---|---|
| RGB/LIM | can | RM-v | −0.164 ± 0.045, −3.63 | −3.00 | −4.20 … −2.05 | SHAPE EXCLUDED |
| | can | RM-φ | −0.204 ± 0.045, −4.53 | −3.75 | −5.06 … −2.84 | SHAPE EXCLUDED |
| | alt | RM-v | −0.176 ± 0.045, −3.90 | −3.23 | −4.46 … −2.29 | SHAPE EXCLUDED |
| | alt | RM-φ | −0.216 ± 0.045, −4.79 | −3.96 | −5.31 … −3.07 | SHAPE EXCLUDED |
| Cepheid (Feng alone) | can | RM-v | +0.140 ± 0.067, +2.08 | — | — | SHAPE TENSION |
| | can / alt | RM-φ / RM-v / RM-φ | Z +1.49 / +1.87 / +1.29 | — | — | SHAPE CONSISTENT |

**Mróz+19's published gradient** (−1.34 ± 0.21 km/s/kpc over 4–20 kpc; a text value, reported only) is matched by the law: −1.50 / −1.23 / −1.31 / −1.04 km/s/kpc, which is +0.8, −0.5, −0.2 and −1.4σ.

## Reading, the fail checked as hard as a win

1. **RGB/LIM: the outer shape is now a 3–5σ tension. The amplitude is not the problem.**
   - When the APOGEE-RGB and LIM groups are combined, the measured 15–27.5 kpc slope (about −0.32) is steeper than the law's (−0.11 to −0.16). The miss is 3.6–4.8σ treated as independent, and 3.0–4.0σ at ρ = 0.5.
   - Under RM-v the amplitude needs essentially the census disc: z between −0.6 and +1.4 on every new curve.
2. **The same statistic also rejects a smooth NFW halo fitted to each curve** (post-run diagnostic, not a verdict input).
   - The fitted NFW gives Z −3.39 (independent) and −2.81 (ρ 0.5) for Ou+Jiao, and −1.66 to −3.39 across pairs.
   - So the steep 15–27 kpc decline is a problem for every smooth equilibrium model. It is not specific to the law.
   - The law still does worse than the NFW, by about 0.2–1.4 in Z.
3. **The verdict depends on which curve and which systematics.**
   - Zhou+23, from the same APOGEE family on a longer distance scale, finds a slope of only −0.186. That is consistent with the law (−0.5 to −1.3σ), and RM-v alt is CONSISTENT outright.
   - The pairs that use Zhou or Eilers give Z −2.05 to −3.07. The headline therefore rests on the Ou and Jiao/Wang distance scales, which is the distance-calibration spread the review itself describes.
   - Using 5% systematics flips Zhou to CONSISTENT. Using table errors only excludes every cell.
4. **Cepheids (Feng+26), a different tracer, see a flat curve to 17.6 kpc** (−0.026 ± 0.067).
   - The law's mild decline is +1.3 to +2.1σ too steep there, the opposite sign to the RGB/LIM miss.
   - Feng's amplitude is about 237 km/s, so the law needs a heavier disc there (+1.5 to +4.6σ).
   - With only 3 points beyond 15 kpc, the Cepheids say nothing about the 15–27 kpc decline.
5. **Not modelled:** non-equilibrium effects (Sgr bending waves, Wang's north–south asymmetry, the LMC), and any common Gaia DR3 astrometric or zero-point systematic shared by both RGB groups. The ρ = 0.5 variant is the only allowance made for that shared systematic.

## What Gaia DR4 (2026-12-02) must show to decide

- **RGB/LIM:**
  - The law predicts 15–27.5 kpc slopes of −0.11 to −0.16.
  - The combined error is 0.045 today. Telling the law from the combined measured −0.32 at 3σ needs 0.055–0.072. Telling it from Kepler needs 0.11–0.13. Both are therefore already met formally, before shared systematics.
  - DR4 decides by resolving the **distance-scale spread**: Zhou −0.19 against Ou/Jiao/Wang −0.32 to −0.36. If an independent distance calibration (e.g. DR4 parallaxes at 15–25 kpc) lands on the Ou/Wang scale and the slope stays at −0.3 or steeper with σ ≤ 0.05, the law's shape is excluded. The fitted NFW then fails too.
  - If the distance scale lands on Zhou's, the law's shape passes.
- **Cepheids:**
  - The tracer needs to extend beyond 20 kpc.
  - Separating the law from Feng's flat curve at 3σ needs σ 0.03–0.05 (0.067 today).
  - A flat Cepheid curve to 25 kpc alongside a declining RGB curve would point to tracer or equilibrium systematics, not to gravity.
- **Census V for the law:** at 15/20/25 kpc it is 209/200/194 km/s (RM-v, canonical), 216/207/201 (RM-v, alt), 199/192/188 (RM-φ, canonical) and 206/199/195 (RM-φ, alt).

## Controls

- **X:** the row counts for Wang, Jiao, Zhou and Feng match their tables.
- **Import:** CFG532's own controls K1–K3 pass when its code is imported.
- **MUTATE: DETECTED in 34/34 cells.**
  - M1 (law off) gives χ² 1411–42280.
  - M2 (baryons × 0.5) gives p < 1e-100 and no CONSISTENT cell.
  - M3 injects a Keplerian tail beyond 15 kpc. The combined Z then reaches −6.0 to −8.9, which shows the combination can detect a Keplerian decline.

## Disclosures

- Some table rows were seen while locating the tables, before freezing. They are listed in FROZEN_CRITERIA_v2 §5.
- The fitted-NFW combined test is a post-run diagnostic.
- S3 (R0 rescale) only rescales radii.
- SL23 is built on Wang+23 and is never combined.
- κ is fitted, and the cold energy's mass is still required. This is not "theory closed".

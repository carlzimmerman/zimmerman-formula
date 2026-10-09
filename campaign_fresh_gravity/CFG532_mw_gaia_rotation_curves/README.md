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

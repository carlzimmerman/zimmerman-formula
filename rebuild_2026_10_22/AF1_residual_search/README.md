# AF1_residual_search: no formula transfers. No clean variable carries the a0 law's residual across samples; what ranks high across samples is sample identity

Criteria: `FROZEN_CRITERIA.md` (5827cd5c57), committed alone first; `AMENDMENT_A1.md` before any Stage 2 number. Scripts `af1_stage1.py`, `af1_stage2.py`, `af1_stage3.py`, `af1_grade3.py`; numbers in `af1_stage1.out`, `af1_stage2.out`, `af1_stage3.out`, their JSON, tables `af1_table_*.csv`. **Not blind**: I knew the record's gas lead and the law's misses. No theory claim. kappa = 1/2 FITTED. Footings never pooled. Cold sector stays retired; nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

## Verdict
| Stage | Frozen label | canonical | alt |
|---|---|---|---|
| 2 CARRIES ACROSS | **none** | 0 variables | 0 variables |
| 2 SURVIVES WITHIN | 10 variables, in dwarfs, groups, per-cluster shear only | most y-SHADOW or label-like; table below | same |
| 3 | **NO FORMULA TRANSFERS** | 0 of 18 complexities | 4 of 18 alone (12, 15, 22, 24), so fails "canonical and alt" |
| 4 | not triggered | | |

A failed search, and Stage 2 stands as the main result.

## Stage 1: the table
Rows: SPARC 3166 (153 galaxies, BF1's cuts), LITTLE THINGS 19, groups 63, X-COP 35 (7 clusters), shear 24 (3 gas terciles x 8 radii; KT view 23), dwarfs 81, MW 37. Law's rms, canonical (alt): SPARC 0.177 (0.178), LT 0.327 (0.323), groups 0.326 (0.326), X-COP 0.476 (0.444), shear 0.336 (0.313), dwarfs 0.574 (0.546), MW 0.061 (0.042). All known answers K1-K6 pass; the a0 x 1.5 twin fails K1-K5 and passes K6, which doesn't use a0. Rerun byte-identical.

**They measure different things.** Circular speed; Jeans dispersion on early types; hydrostatic mass; projected lensing excess surface density; half-light dispersion on dwarfs; a curve on a model baryon set. Hydrostatic and lensing masses differ (LF1, GM1) and nothing here corrects that. Coverage per variable and sample is in `af1_stage1.json`.

Systematics by sample: SPARC distance and inclination, fixed Upsilon 0.5, 0.7; LT one outer point, sE 0.075; groups stars only, gas not on disk; X-COP hydrostatic bias, 7 clusters; shear f* 0.034, h 0.672, gas +0, f_gas fixed by construction, y a band average; dwarfs assumed gas-free, tides and binaries as X1 carried them, no external field in the target; MW Upsilon inside McMillan's model, gas share from a published form I recalled, PROVISIONAL, spherical. **Colour isn't on disk for any sample**; SPARC's Hubble type stands in. Environment exists only for SPARC and dwarfs, T only for shear.

## Stage 2: what carries information
Pi: rank 3. Basis y, f, ell = R a0/c^2, G Sigma/a0, v^2/c^2 (LEAKY), kT/mc^2. **Baryonic potential and baryonic dynamical time are y ell and sqrt(ell/y)**, so they carry nothing new; observed potential and time contain the target.

73 clean tests per footing, first Holm line 6.9e-4. 14 are floor-limited (X-COP within, shear terciles): they can't reach the line, so that's a limit, not "no signal". Pure-noise variable: 0 survive.

| Survives, Holm, both footings | Where, canonical rho | Reading |
|---|---|---|
| m_sys, lell | dwarfs -0.62, -0.58, partial on y holds | Fainter or smaller dwarfs miss more. AUC 1.0 cluster vs galaxy: elsewhere these are labels |
| ly, ly_star, lsig_eff | groups +0.45, dwarfs -0.44 | **Opposite signs**, same quantity in gas-free samples. No single y-correction serves both |
| lx_host, ld_host | dwarfs +0.40, -0.43 | Gone once y is partialled (p 0.16, 0.09), y-SHADOW. UX4's "luminosity or acceleration" again |
| ly_band, lM500, lz | shearCL OUTER, about +0.25 | The outer excess rises with mass. **All three collinear**: partial on the other two p 0.42-0.92, unseparated. Selection in a flux-limited catalogue can't be excluded |

- **Gas isn't separated, on this test.** ly_gas survives nowhere. In shearCL ly_band is a gas proxy and doesn't beat M500 or z. kT in shear: MID +0.25 (p 0.04), OUTER +0.20, N about 100, neither passes; it doesn't confirm or settle X21's kT.
- **SPARC has no survivor.** Within-galaxy ly -0.20, lell +0.23, mock 0.17, p about 1e-3 and 3e-3, fail Holm. Between-galaxy Hubble type -0.16, p 0.05. The law's disc residual is close to structureless at this statistic.
- **X-COP inside clusters:** |rho| 0.83-0.91 with y, y_gas, f, ell, x, gas slope, m_sys, all at floor p 0.016, and all the same radial trend. The data can't say which.

**Sample identity.** lx_rad gain 0.35 (p 5e-5) leads honestly, but exists only in SPARC, X-COP, shear: leave-one-out +0.50, +0.61 in the clusters, **-4.7 in SPARC**. It explains clusters' profile and fails discs. ly_gas gain 0.30, stratified p 0.07, LOSO positive 1 of 5. lz gain 0.32, AUC 1.0. No variable reaches LOSO in half of covered samples and the stratified line. Pure noise gets gain 0.05; label control 0.003.

**Separability.** Galaxies: 21 of 21 pairs NOISE-LIMITED, nothing to separate. Clusters, n 35 held out: ADDITIVE 8, both 4, NEITHER 2, NOISE-LIMITED 1, on a thin base where the two forms mostly differ by less than noise; not a form. Pooled: 18 of 21 NOISE-LIMITED, alt has 1 PRODUCT, on no shared basis.

**Power.** The frozen plant **FAILED**: 0.3 log10(1 + y_gas) is invisible, as y_gas is about 0.02 in discs, which I'd not checked. Post-result plant, UX3's own term log10(1 + 13.29 y_gas) on noise 0.1: ly_gas ranks first, gain 0.64, 4 of 5 LOSO, Holm in SPARC. **So Stage 2 would see that term if discs carried it, and they don't**; this repeats UX3's disc break by a method-free route. The frozen failure stands as a failed check.

## Stage 3: PySR
PySR 1.5.9, already installed, no download. Features with full coverage among survivors: ly, ly_star, lell, m_sys. **Gas wasn't offered:** ly_gas didn't survive and lacks dwarfs and groups. Partial-coverage survivors weren't searchable pooled. 400 iterations, about 90 s each, one thread, nice 19. compute_queue couldn't start it (BF1 over 4 GB, disk 23 GB under 30). Depth check 4000 iterations, 16-23 min, same label, `af1_stage3_deep.*`.

Planted: RECOVERED, holdout rms 0.101 against 0.12. Scrambled front matches the real one closely: **mean holdout rms real 0.225-0.25, scrambled 0.24-0.25, label control 0.262.**

Best per footing, holdout rms; law, then label control, then equation. **`af1_stage3.out` has every row, constants and margins.**
| Sample | law | label | canonical c14 (k 4) | alt c22 (k 5) |
|---|---|---|---|---|
| SPARC | 0.165, 0.169 | 0.176 | 0.181 | 0.173 |
| LT | 0.369, 0.368 | 0.369 | 0.379 | 0.400 |
| groups | 0.352, 0.358 | 0.432 | 0.383 | 0.374 |
| X-COP | 0.482, 0.450 | 0.097 | 0.107 | 0.097 |
| shear | 0.331, 0.315 | 0.316 | 0.150 | 0.193 |
| dwarfs | 0.556, 0.527 | 0.418 | 0.330 | 0.310 |
| MW | 0.062, 0.039 | 0.023 | 0.046 | 0.030 |
| Beat label | | | 3 of 7 | 5 of 7 |

Margins at these two, beside frozen lines: X-COP +0.042, 0.107 (canonical misses 0.10), -0.002, 0.097 (alt inside); SPARC median -0.059, -0.015; groups Z -1.4, -1.2; shear chi^2 5, 11 of 10; **IC 1613 Z -8.3, -8.3, against the law's -7.9, worse**. A margin isn't a pass of the keys; the 15-key grader wasn't run. Half the X-COP clusters and shear cells on a radial split are not independent of training.

**What the equations are.** Nearly all are a U in z_m_sys, with high residual at both mass ends, plus ell. Those are AUC 1.0 labels, and the scrambled front, which keeps sample means, finds the same shape. **A label-tuned switch, not a law.** X-COP's holdout barely beats a single constant (0.097).

**Bullet: NOT EVALUABLE for every equation.** All hold z_lell or z_m_sys, which have no local meaning on a map. UX6's path is reproduced for the law (M300 1.11, 0.73; dkappa -0.068, -0.111). UX6's DEAD stands. IC 1613 fails all rows.

## Data, plainly
The residual's largest coherent pattern is: clusters are short by a level that falls outward and rises with mass, unseparated from gas, M500, z; dwarf satellites are short in a way tied to their small mass; discs carry almost nothing. **Nothing in this lane tests a collisionless component**, and this lane doesn't point at one or away from one; the Bullet evidence for offset mass is UX6's and earlier.

## Failed or unfinished
- Frozen Stage 2 plant failed; replaced post-result, disclosed.
- Frozen text left partial vs raw open; closed in A1 before numbers.
- Permutation among rows in the stratified null ignores within-galaxy correlation, so it is generous.
- y-SHADOW is untestable for tests where no partial exists; shear's partial is on the other two variables, post-result.
- Stage 2 not rerun on a0 x 1.5; twin stops at K. Stage 3 not rerun for byte identity (`deterministic=True`). Scrambled is one seed.
- Not done: a gas-including PySR on the 5 samples with y_gas (excluded by the frozen rule); T, environment, colour not searchable across samples, as they aren't on disk across samples.
- Search is limited to these operators and size 25. **Not an impossibility statement.**

kappa = 1/2 FITTED. Not theory closed.

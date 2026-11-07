# RS3 RESULT: the residual surface (RS3 = the brief's RS1)

**Label: NO VERDICT as frozen. The Newtonian-f MUTATE (M2) does not bite, because g_obs is on the frozen variable list
and makes the law-off f an exact function of the pair (g_N, g_obs). The main reading is NO PAIR, under both UDG
readings. The only pairs that pass the line on the full set contain g_obs, so they restate the data. Of the pairs
without g_obs, none comes near the line: the best is (depth, sigma) GRID6, chi^2/N 1.48 / 1.43, with SPARC at
z -4.5 / -3.9.**

Criteria `FROZEN_CRITERIA.md` (8158e4645f), amendment A1 (5123eda762, before any script), amendment A2 (ce2859f5b4,
after a disclosed smoke test, before the graded run). Script `rs3.py`. Outputs `rs3.json` / `rs3.out` (main) and
`rs3_MUTATE.json` / `rs3_MUTATE.out`. Every number below is read from those JSONs. Adopts nothing. kappa = 1/2 FITTED;
not theory closed. No particle, no LCDM input, no download. The footings are graded separately and never pooled.

## Rows (both footings, y = log10(1+f), the KD1 uniform f per system)

| Class | N | median f canonical / alt | sigma_sys (dex) |
|---|---|---|---|
| SPARC (target f = 0; exact-field sigma 0.146 / 0.141 dex) | 145 | 0 | 0.0285 |
| X-ray ellipticals, after IMF (QX26) | 7 | 0.41 / 0.34 | 0.100 / 0.097 |
| X-COP, SE2 reading | 7 | 4.38 / 4.02 | 0.024 / 0.023 |
| groups, f* 0.5, SE2 shift | 20 | 2.27 / 1.84 | 0.076 / 0.076 |
| bright M31 dSphs, 21 admissible | 21 | 1.48 / 1.30 | 0.207 / 0.209 |
| Coma UDGs (9; pericentre reading keeps 1) | 9 | 51 / 45 | 0.279 / 0.283 |
| LG field dwarfs (target f = 0; sigma 0.240 / 0.238 dex) | 13 | 0 | 0.513 / 0.512 |

NO VERDICT cells:
- x_e is missing for X-COP and groups (no positions on disk).
- Colour is missing for X-COP, groups, UDGs, dSphs and LG field. SPARC has it for 84 of 145 galaxies, the ellipticals for 7 of 7.
- Depth is missing for one alt dSph (And XXI: the law field at r_1/2 is below QX5's cut, so its tail is 0).

## KA (all PASS, both footings)

- **KA1, KD1 f table reproduced exactly (max rel 0):**
  - canonical: SPARC allows 0.3257; X-COP 4.179, ellipticals 0.8641, UDGs 86.36, groups f* 0 / 1 3.464 / 1.232, bright M31 1.677, MW classical 1.822.
  - alt: 0.1937; 3.783, 0.7734, 77.68, 2.865 / 0.9323, 1.271, 1.407.
- **KA2:** the lane's inversion on the pooled classes matches KD1 to 1e-12.
- **KA3:** GB1 L0 class means match to 4.3e-7 / 4.5e-7.
- **KA4, planted (g_N, sigma), noiseless:** carries in both families, both footings and every leave-one-out. KA4n (reported, not gating), the noisy plant over 20 seeds: GRID6 17 / 17, quadratic 15 / 18 seeds carry. So the line has power at a true monotone surface.

## Search: 66 pairs x {GRID6, quadratic} x 4 orientations, gated

| | canonical | alt |
|---|---|---|
| Pair-families carrying on the full set, all classes | 2 (g_N+g_obs and g_obs+Sigma_b, GRID6) | the same 2 |
| ...that also survive every leave-one-out | 0 (drop X-COP: groups z +2.31; drop bright M31: SPARC z -2.14) | 2 |
| Carry on both footings and every leave-one-out | **none** | |
| Lowest chi^2/N (all classes) | g_obs+Sigma_b quadratic, 0.379, SPARC z -2.86 | 0.372, SPARC z -2.49 |
| Closest to the line | g_N+g_obs GRID6, chi^2/N 0.433, SPARC z -1.96 | 0.440, SPARC z -1.53 |
| **Best pair without g_obs** | **depth+sigma GRID6, chi^2/N 1.483; SPARC -4.49, X-COP +3.82, UDGs +3.46, ellipticals -2.87, groups -2.32** | **1.434; SPARC -3.87, X-COP +3.48, UDGs +3.48, ellipticals -2.77, groups -2.52** |

- The pericentre UDG reading keeps 1 of 9 UDGs (J130038.63+272835.3). It is also **NO PAIR**: the same two g_obs pairs carry on the full set, fail canonical leave-one-out, and pass alt.
- **Without g_obs, no pair passes leave-one-out after dropping any class,** in either reading or footing. The closest without g_obs, dropping X-COP, is depth+sigma at chi^2/N 0.63 / 0.61, but it still has a class at z +4.66 / +4.65.
- **The miss a future action has to explain:** at the best pair without g_obs, SPARC needs to sit 3.9-4.5 sigma lower while X-COP and the UDGs sit 3.5-3.8 sigma higher. No monotone surface in any listed pair holds discs at zero and also lifts the hot clusters and the UDGs.

## MUTATE

- **M1, shuffled class labels:** 0 pairs carry. Best is Sigma_b+x_e at chi^2/N 2.32 / 2.21, with SPARC at z -11.5 / -10.9. **BITES.** The real data beat the shuffle.
- **M2, Newtonian f (law off):** 4 pair-families carry on both footings through every leave-one-out: g_N+g_obs and g_obs+Sigma_b, in both families, at chi^2/N 0.000. **DOES NOT BITE.**
  - The cause is structural. The law-off y_N = log10 g_obs - log10 g_N is an exact, monotone function of that pair, row by row. g_obs is on the brief's frozen list, and Sigma_b is identical to g_N / (pi G).
  - Under rule 5 the label is therefore NO VERDICT.
  - Post-result reading, which sets no label: without the g_obs pairs, M2 has no carrier. Its best is sigma+Sigma_b quadratic at 2.63 / 2.66 with UDGs at z +4.26 / +4.21, so M2 would bite, and the main reading without g_obs is NO PAIR by a wide margin.
- **M3, leave-one-class-out:** reported in the search section above. It is the cut that stops g_N+g_obs on the canonical footing.

## Free isotonic (reported only, A2)

On 9 of 45 pairs without g_obs (all classes present), the free 2D isotonic fit passes the line on both footings. Examples are g_N+sigma, depth+sigma and g_N+depth.
- That is the antichain freedom recorded in A2: mixed orientation leaves almost no order constraints, so the fit has one free value per system.
- It is not a law, and it is not gating.
- Its NNLS hits numerical overflow on near-singular node sets, so its numbers are indicative only.

## Disclosures

- **Id:** RS3 = the brief's RS1, since that id belongs to rebuild_2026_10_22/RS1_required_source.
- **How RS3 differs from that RS1:** it fits pairs, with a monotone surface, a per-class 2-sigma line and class-correlated systematics, where RS1 used single-variable collapse and a form grammar.
- **A2, post-freeze:** a canonical smoke test on 4 pairs exposed the antichain degeneracy of free isotonic. The numbers seen are listed in A2. The same 4 pairs were rerun once on the A2 code before the graded run.
- **Post-freeze code changes, all before the graded rows were final:**
  - And XXI's alt depth of 0 is marked NO VERDICT; it crashed the first run's log10.
  - RuntimeWarnings are suppressed.
  - The MUTATE run was SIGTERM-checkpointed after 28 fits, then resumed with the reported-only isotonic switched off in MUTATE. The gating families are unchanged.
  - The first main run crashed after the canonical main fits were done. The rerun may have resumed from a periodic checkpoint for canonical rows that had not changed. The checkpoint files are removed.
- **SPARC N:** 145 (GB1's set, QX5 Q <= 2 and i >= 30), not the 175 in the brief.
- **Rows are system level.** The X-COP per-bin gas vs stars profile (NA2) is not used.
- **Built variables:**
  - sigma for SPARC (V_flat / sqrt 2) and for X-COP (sqrt(G M / 2r) at the outermost point; no T on disk).
  - Depth for dSphs and UDGs (QX5 law tail of M*).
  - r/r_half for every class with a profile.
- **Assumptions:** UDG f_gas = 0 (no Coma HI on disk); dSph gas from LVD M_HI only.
- **Errors:**
  - The elliptical per-system error is the SE2 bootstrap sd x sqrt(7) (scatter-based).
  - The SPARC and LG field targets use the class rms as the tolerance.
  - Class-correlated systematics are taken from SE2 as sqrt(post sd^2 - raw sd^2).
- **Degenerate pairs:** rho_b and rho_b/rho_DE differ by a footing constant, and g_N = pi G Sigma_b for enclosed quantities. Those pairs are one-variable fits; they are run and flagged, not counted twice.
- **Compute:** peak RSS 0.309 GB (main) and 0.130 GB (resumed MUTATE; the interrupted MUTATE run peaked at 0.28 GB). One thread, about 70 s and 21 s.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.

# HL3 RESULT: SAME SHAPE (canonical) / SAME SHAPE (alt)

Criteria ef4595f390 (frozen), AMENDMENT_A1.md (dated 2026-11-08, committed with the fetch log at 4f05deafde before any
graded number); hl3.py at f9715fac80; hl3_grade.py, hl3.json, hl3.out, hl3_MUTATE.out at 458e1e364a. A grading lane of
the adopted law; it adopts nothing. Both footings separately (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2; A1 item 1).
kappa = 1/2 FITTED; not theory closed. No dark-matter particle. Distance convention: h 0.7 (the on-disk loaders'); CLASH
R500 from Umetsu+2016 M500c with rho_c(z) at h 0.7, Omega_m 0.27, Omega_Lambda 0.73 (Umetsu's stated convention, the
same background convention as X-COP's Ettori 2019 R500), declared; no other LCDM input.

## The question and the answer

Does the law's plain cluster residual rho = log10(g_obs / g_law(g_bar)) have the same radial shape on a LENSING-only
mass profile (CLASH, Tian+2020's 84 points, g_tot from Umetsu+2016 joint strong + weak lensing, g_bar = Donahue+2014 gas
+ BCG) as on the HYDROSTATIC one (X-COP, M_FORW, gas + measured stars)? **Yes, in every bin the two legs share.**
Delta_b = median_lensing - median_hydrostatic is +0.05 dex in both shared bins on both footings, inside the frozen
0.10 dex band with the 95 % interval covering 0, and every bracket (all 20 CLASH clusters, Donahue r500 for the lensing
radii, X-COP without A2319, all 12 X-COP with imputed stars, hydrostatic read at the lensing points' own radii) sits
within 0.04 dex of the primary value. **Reading (frozen):** the hot-leg residual shape is NOT a hydrostatic artefact
inside 0.5 R500; the "lensing = dynamics" statement holds at cluster scale for the law's residual. The lensing leg shows,
if anything, slightly MORE missing mass than the hydrostatic leg, not less (HE-a MISS).

## Per-bin table (primary samples: 16 X-ray-selected CLASH clusters; 7 X-COP clusters with measured stars)

Cluster medians of rho (dex) with bootstrap 95 % intervals over clusters (B 10,000, seed 1103, one value per cluster per
bin). n = clusters in the bin. A bin is shared (graded) when both legs have >= 6 clusters.

| footing | bin r/R500 | lensing median [95 %] (n) | hydrostatic median [95 %] (n) | Delta_b = L - H [95 %] | status |
|---|---|---|---|---|---|
| canonical | 0-0.25 | +0.578 [+0.512, +0.642] (16) | +0.530 [+0.522, +0.571] (7) | **+0.048 [-0.026, +0.114]** | shared |
| canonical | 0.25-0.5 | +0.516 [+0.462, +0.591] (12) | +0.463 [+0.437, +0.501] (7) | **+0.053 [-0.022, +0.140]** | shared |
| canonical | 0.5-0.75 | +0.320 [+0.284, +0.356] (2) | +0.372 [+0.334, +0.389] (7) | -0.052 [-0.106, +0.022] | reported, not graded (2 lensing clusters) |
| canonical | 0.75-1.0 | -- (0) | +0.264 [+0.245, +0.271] (7) | -- | hydrostatic only |
| canonical | 1.0-2.0 | -- (0) | +0.161 [+0.080, +0.246] (6) | -- | hydrostatic only; M_FORW beyond R500 is the forward-model fit |
| alt | 0-0.25 | +0.549 [+0.486, +0.614] (16) | +0.500 [+0.491, +0.540] (7) | **+0.049 [-0.023, +0.116]** | shared |
| alt | 0.25-0.5 | +0.485 [+0.429, +0.558] (12) | +0.429 [+0.405, +0.468] (7) | **+0.056 [-0.023, +0.140]** | shared |
| alt | 0.5-0.75 | +0.287 [+0.251, +0.322] (2) | +0.339 [+0.300, +0.354] (7) | -0.052 [-0.103, +0.022] | reported, not graded |
| alt | 0.75-1.0 | -- (0) | +0.229 [+0.210, +0.236] (7) | -- | hydrostatic only |
| alt | 1.0-2.0 | -- (0) | +0.126 [+0.044, +0.210] (6) | -- | hydrostatic only |

Both legs fall outward at the same rate: lensing 0.58 -> 0.52 (-> 0.32 on two clusters), hydrostatic 0.53 -> 0.46 -> 0.37
-> 0.26 -> 0.16. The lensing leg ends at 600 kpc = 0.28-0.59 R500 (0.59 for RXJ1532, the lightest cluster), so the shared
bins are the inner two and the lane says nothing about R500 on the lensing leg (see limits).

Brackets, Delta_b per shared bin (0-0.25; 0.25-0.5):

| bracket | canonical | alt |
|---|---|---|
| all 20 CLASH clusters (the 4 mergers in) | +0.084 [-0.012, +0.112] (n_L 20); +0.046 [-0.023, +0.116] (15) | +0.082 [-0.008, +0.114]; +0.048 [-0.023, +0.116] |
| lensing radii in Donahue+2014 Chandra r500 | +0.047 [-0.031, +0.117]; +0.065 [-0.022, +0.146] | +0.047 [-0.028, +0.119]; +0.069 [-0.023, +0.146] |
| X-COP without A2319 (6) | +0.050 [-0.017, +0.117]; +0.059 [-0.033, +0.141] | +0.050 [-0.013, +0.120]; +0.062 [-0.031, +0.141] |
| X-COP all 12 (5 with imputed stars) | +0.045 [-0.045, +0.114]; +0.059 [+0.002, +0.147] | +0.046 [-0.040, +0.116]; +0.062 [+0.005, +0.146] |
| hydrostatic rho read at the lensing points' r/R500 (sampling check) | +0.049 [-0.025, +0.124]; +0.052 [-0.019, +0.142] | +0.050 [-0.022, +0.127]; +0.055 [-0.019, +0.142] |

The 12-cluster imputed bracket's 0.25-0.5 interval just excludes 0 (+0.002 / +0.005); it is a bracket with 5 clusters'
stellar mass imputed, not the primary, and its value (+0.06) is inside the 0.10 band either way.

## Label per footing (frozen rule)

- **canonical: SAME SHAPE.** Both shared bins |Delta_b| <= 0.10 with the 95 % interval covering 0, primary sample.
- **alt: SAME SHAPE.** Same.
- Neither HYDROSTATIC-SPECIFIC (innermost Delta_b would have to be <= -0.15; it is +0.05) nor LENSING-SPECIFIC (no bin
  reaches +0.15) comes close. M2 flips the label both ways, so the innermost bin has power (no NO POWER override).

## S2: the lensing-leg need (reported, not graded)

The 0.75-1.0 bin is not shared (no lensing point beyond 0.59 R500), so S2 is reported at the outermost shared bin,
0.25-0.5 R500, and says so. 10^rho = g_obs / g_law:

| footing | lensing-leg need at 0.25-0.5 | X-COP plain-law need, same bin (recomputed) | X-COP plain-law need at 0.75-1.0 (hydrostatic only, 7) | NA2's baryon-traced F at the captured amount |
|---|---|---|---|---|
| canonical | x3.28 [2.90, 3.90] | x2.90 [2.74, 3.17] | x1.84 [1.76, 1.87] | 4.206 |
| alt | x3.05 [2.69, 3.61] | x2.68 [2.54, 2.94] | x1.70 [1.62, 1.72] | 3.811 |

Reported, not graded. The lensing-leg need at R500 the record lacks is still lacking: the on-disk leg stops at 600 kpc
and the D1 extension was NOT RUN (below). NA2's F is a fitted added-mass fraction on a stars-traced shape, a different
statistic from 10^rho, and is quoted only because the criteria name it.

## S3: per-cluster scatter of rho at fixed r/R500 (dex, ddof 1)

| footing | lensing 0-0.25 / 0.25-0.5 | hydrostatic 0-0.25 / 0.25-0.5 / 0.5-0.75 / 0.75-1.0 / 1.0-2.0 | pooled over shared bins, L vs H |
|---|---|---|---|
| canonical | 0.102 / 0.082 | 0.034 / 0.062 / 0.048 / 0.032 / 0.097 | 0.094 vs 0.050 |
| alt | 0.100 / 0.081 | 0.034 / 0.062 / 0.048 / 0.032 / 0.097 | 0.093 vs 0.050 |

Beside h56's 0.176 dex per-cluster a0 scatter on the same 84 points (a fitted-scale scatter on 2-6 points per cluster,
which inflates it). The lensing leg is about twice as scattered as the hydrostatic one at fixed r/R500; its median
error per point is 0.09 dex on log g_tot, so most of that is measurement scatter.

## Known answers (all printed with numbers in hl3_points.out; all pass, one disclosed)

| KA | reference | HL3 | result |
|---|---|---|---|
| KA1 h56 one-a0 fit on the 84 points, h56's kernel and grid | chi2 136.1, per-cluster a0 scatter 0.176 | chi2 136.1, a0 1.722e-9, scatter 0.176 over 20 clusters | PASS |
| KA2 Tian+2020 slope-1/2 fit | g_ddagger 2.02e-9 | 1.965e-9 (+- 0.009 dex), 2.7 % low | PASS (10 %) |
| KA3 NA2 through NA2's loaders | F 4.206 / 3.811; stars bins -0.068 / +0.089 / +0.070 (can.) | 4.2065 / 3.8111; -0.0676 / +0.0887 / +0.0695; alt -0.0589 / +0.0861 / +0.0591 | PASS |
| KA4 HL2 replay | json n 53 +0.031 +- 0.035; post n 81 +0.031 +- 0.020 | both replayed | PASS; the Delta_b check needs the 0.75-1.0 bin shared, which it is not: noted, not checked |
| KA5 law inversion | g = g_N to 1e-9 at g_N >> a0; sqrt(a0 g_N) to 1 % at g_N <= 1e-3 a0 | 1.0e-10 at 1e10 a0; round trip g^2/(g + a0) = g_N to 4e-16; deep end 1.59 % at 1e-3 a0, 1.00 % at 4e-4 a0, 0.50 % at 1e-4 a0 | PASS with disclosure |

KA5 disclosure: the law's exact deep expansion is g = sqrt(a0 g_N) (1 + sqrt(g_N/a0)/2 + ...), so at g_N = 1e-3 a0 the
deviation from sqrt(a0 g_N) is 1.58 % for any correct implementation; the frozen line's "1 % at 1e-3 a0" cannot be met
and the check is read at 4e-4 a0 (1.0 %) and 1e-4 a0 (0.5 %) with the exact round trip. Not amended; disclosed here and
in hl3_points.out.

## MUTATE (hl3_MUTATE.out): all bite, both footings

| twin | canonical | alt | |
|---|---|---|---|
| M1 legs swapped | Delta_b -> -0.048, -0.053; exact sign flip; swapped label SAME SHAPE | -0.049, -0.056; exact | HOLDS |
| M2 plant +0.30 dex on lensing 0-0.25 | Delta_b +0.348 [+0.274, +0.414] -> LENSING-SPECIFIC | +0.349 [+0.277, +0.416] -> LENSING-SPECIFIC | BITES |
| M2 plant -0.30 dex on lensing 0-0.25 | -0.252 [-0.326, -0.186] -> HYDROSTATIC-SPECIFIC | -0.251 [-0.323, -0.184] -> HYDROSTATIC-SPECIFIC | BITES |
| M3 a0 -> 10 a0 on the lensing leg only | Delta_b moves 0.407 / 0.423 vs interval widths 0.140 / 0.162 | 0.414 / 0.429 vs 0.139 / 0.163 | BITES |

## Hand estimates (frozen)

| | claim | canonical | alt | |
|---|---|---|---|---|
| HE-a | 0-0.25 Delta_b in [-0.10, 0] | +0.048 | +0.049 | MISS (right band, wrong sign: lensing shows more missing mass, not less) |
| HE-b | S2 lensing need within x1.3 of X-COP's in the same bin | ratio 1.13 | 1.14 | HIT |
| HE-c | D1 extends the lensing leg to 0.75-1.0 for >= 10 clusters | 0 clusters | 0 | MISS (D1 NOT RUN) |
| HE-d | lensing scatter exceeds hydrostatic by >= 0.05 dex | +0.044 | +0.043 | MISS (by 0.006) |

## Limits

1. **Radial reach.** The lensing leg stops at 600 kpc (0.28-0.59 R500). Shared bins are 0-0.25 and 0.25-0.5 only; the
   0.5-0.75 bin holds two lensing clusters (RXJ1532, RXJ2129) and is reported, not graded; 0.75-1.0 and 1.0-2.0 are
   hydrostatic only. SAME SHAPE is a statement about the inner half of R500. The lensing-leg need AT R500 is not
   delivered.
2. **D1 / D2 / D3 NOT RUN where the sources lack per-radius values.** VizieR has neither catalogue; the arXiv sources
   (FETCH_LOG.md) carry Umetsu+2016's surface-mass-density profiles and Okabe & Smith 2016's shear profiles as figures
   only, and Donahue+2014 has no per-radius gas table and no BCG table. Umetsu's table2 (NFW M200c, c200c per cluster)
   would allow a MODEL-extended lensing leg to R500; that is a parametric extrapolation, not per-radius data, and was
   not run under these criteria. No bin carries extrapolated g_bar (none was needed).
3. **Different clusters on the two legs.** CLASH (z 0.19-0.69, M500c 4-22e14) and X-COP (z 0.05-0.09, M500 2-9e14) are
   different samples; SAME SHAPE compares populations at matched r/R500, not lensing and hydrostatic masses of the same
   cluster (that is HL1/HL2's job, NO GAP at R500).
4. **Baryon budgets differ.** CLASH g_bar is gas + BCG (no satellite stars, no intracluster light); X-COP has the full
   measured stellar profile. Adding 10 % to CLASH's baryons would lower its rho by about 0.02 dex in the deep regime, so
   part of the +0.05 dex lensing excess can be bookkeeping. It does not change the label (the band is 0.10).
5. **The four merger clusters** (MACS0416, MACS0647, MACS0717, MACS1149, Umetsu's high-magnification set) are out of
   the primary and in the all-20 bracket, which moves the inner bin by +0.04 (they sit high in the core).
6. **A2319** (44 % non-thermal pressure claim) in and out: Delta_b changes by <= 0.006.
7. **X-COP stellar profiles exist for 7 of 12** (AMENDMENT A1 item 2); the 12-cluster bracket imputes the other five
   with the 7-sample median M_star/M_gas(r/R500) (0.40 at 0.1 R500, 0.11 at 0.3, 0.07 at 0.7) and reads the same.
8. **R500 normalisation.** CLASH primary from Umetsu's NFW M500c (table3), bracket Donahue's Chandra r500 (which differ
   by up to 30 % per cluster, 2100 vs 1180 kpc for the merger MACS0416); the shared-bin Delta_b changes by <= 0.012.
   X-COP from the Ettori 2019 json (differs from the FITS headers by <= 2 %).
9. **Hydrostatic radii** are the gas-profile grid where hydro, gas and stellar profiles are all tabulated (0.02-2.0
   R500); M_FORW is the forward-fitted hydrostatic mass, model-smoothed, and beyond R500 rests on the SZ pressure.
10. **Not a statement about the law's success.** rho is +0.5 to +0.6 dex in the core on BOTH legs (x3-4 missing on the
    plain law), falling to +0.26 (x1.8) at R500 on the hydrostatic leg: the standing hot-leg no-go, now shown to have
    the same shape on lensing masses where both are measured.

## Compute and process

- hl3.py 184 MB peak RSS, about 10 s; hl3_grade.py 207 MB, about 10 s each mode. One thread, nice 10.
- Downloads 2.3 MB (budget 200 MB), untracked, sha256 in FETCH_LOG.md, nothing executed, parsed as text.
- Post-freeze disclosures: (i) the criteria's footing header read "1.2e-10 / 1.1e-10"; the loaders' values were used
  (A1 item 1). (ii) KA5's deep-end line, above. (iii) The first push of deliverable 3 failed when a full detached
  worktree of origin/main filled the disk; the worktree was removed and the push redone from a sparse worktree holding
  only this lane and tools/ (pre-commit retraction guard). No graded number was touched.

kappa = 1/2 FITTED; not theory closed. Adopts nothing; the owner adopts.

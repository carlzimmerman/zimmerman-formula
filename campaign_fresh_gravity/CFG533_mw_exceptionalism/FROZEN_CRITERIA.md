# CFG533 FROZEN CRITERIA: "MW exceptionalism" — does the law get EXTERNAL outer slopes right, and is the MW decline direction-dependent?

Frozen 2026-10-09, before any CFG533 script was written or any SPARC slope was computed. Committed alone.

**Trigger.** CFG532b found that the Milky Way's 15–27.5 kpc slope dlnV/dlnR (RGB/LIM curves; Ou+24/Jiao+23 primary, combined ≈ −0.32) is steeper than the law's −0.11 to −0.16 at census baryons. Combined Z is −3.0 to −4.8 (SHAPE EXCLUDED as frozen there). A fitted NFW also fails (Z −3.4). The review arXiv:2608.10189 (§ "The puzzle of MW exceptionalism", on disk) reports Bariego-Quintana & Llanes-Estrada (2026): SPARC terminal slopes are consistent with flat, while the MW is not.

**Framework, as always.** a0 = κ c √(G ρ_DE), with κ = ½ FITTED. Footings are canonical 9.36e-11 and alt 1.13e-10 m/s². They are run separately and NEVER pooled. Kernel ν(y) = 1/(1 − exp(−√y)); no EFE. The round cold-energy rule applies, and the cold energy's MASS is still required. Never "theory closed". Only data on disk are used; nothing is downloaded. No knobs: every choice is fixed below.

## Part A — external control on SPARC

**Data.** `real_research/data/SPARC_Lelli2016c.mrt` (19-token rows; NEVER SPARC_table.txt) and the 175 `real_research/data/sparc_data/*_rotmod.dat` files.

**Selection.** Q ≤ 2 and Inc ≥ 30°.

**Law (external).** ALG, the record's algebraic RAR on rotmod baryons:
- V_bar² = V_gas|V_gas| + 0.5 V_disk² + 0.7 V_bul².
- g_bar = V_bar²/R, and g_law = ν(g_bar/a0) g_bar.
- V_law = √(R g_law).

This is the law in the plane. RM-v differs from ALG only through the sphere-vs-disc enclosed baryon mass, which is small at the large radii used here (CFG516). On the MW, CFG532 found ALG's shape miss (−2.2 to −2.9σ) to be the same size as RM-v's. Points with g_bar ≤ 0 are dropped.

**MW windows, mapped to scaled radius (both declared; both run).**
- **S-Rd (primary):** R/R_d ∈ [6.0, 11.0]. This is 15/2.5 to 27.5/2.5, with R_d = 2.50 kpc, the McMillan17 thin disc used in CFG514/532. SPARC R_d is the mrt `Rdisk`.
- **S-rM:** R/r_M ∈ [15/r_M,MW, 27.5/r_M,MW], with r_M = √(G M_b/a0) per footing.
  - MW: M_b = 6.642e10 (CFG532 B1 grid, stars + gas), giving r_M = 9.95 kpc (canonical) and 9.05 kpc (alt). The windows are therefore [1.508, 2.765] (canonical) and [1.657, 3.038] (alt).
  - SPARC: M_b = 0.5 L[3.6] + 1.33 M_HI (mrt). The bulge is taken at Υ 0.5 here, a declared simplification for the scaling only.

**Coverage rule (per galaxy, per window).** At least 4 rotmod points inside the window, AND R_max,in / R_min,in ≥ 1.35 (half the MW window's log span). Galaxies failing this are counted as "not reaching", never scored.

**Slope estimator.** Identical to CFG532's `slope()`: a weighted LS of ln V on ln R inside the window, with weights (V/eV)².
- b_data comes from V_obs with eV.
- b_law comes from V_law at the same radii, with the same weights.
- Δ = b_data − b_law. σ_i is the data slope's LS error.

**Ensemble statistic (per window × footing cell).** The ensemble error comes from the galaxy-to-galaxy scatter, so per-galaxy error underestimates cannot inflate Z. For N scored galaxies:
- mean Δ;
- SE = std(Δ, ddof 1)/√N;
- Z = mean/SE;
- median Δ, with a bootstrap 68% interval (2000 resamples, seed 533).

Reported and not used in the verdict: the inverse-variance mean with σ_i ⊕ 0.03.

**MW analogues (two declared definitions, reported separately).**
- **AN-V:** mrt Vflat ∈ [180, 260] km/s.
- **AN-M:** SPARC M_b ∈ [3.32, 13.3]e10 M☉ (MW M_b within a factor of 2).

For each, report: how many there are; how many reach each window; their mean/median Δ; and their measured slopes.

**Exceptionalism metrics (reported).**
- The fraction of scored galaxies (and analogues) with measured b_data ≤ −0.28. This is the MW RGB/LIM regime: Eilers −0.278, Ou −0.325, Jiao −0.319, Wang −0.356.
- The percentile of the MW's combined Δ (CFG532b primary Ou+Jiao, read from `cfg532b_results.json`) within the external Δ distribution.

**Per-cell verdict.**
- **NOT DIAGNOSTIC** if N < 10 or SE > 0.05.
- Otherwise **LAW MATCHES EXTERNAL SLOPES** if |mean Δ| ≤ 0.05 AND |median Δ| ≤ 0.05.
- Otherwise **LAW MISSES EXTERNAL SLOPES** if |mean Δ| > 0.05 AND |Z| ≥ 3.
- Otherwise NOT DIAGNOSTIC.

0.05 is one third of the MW's miss (~0.16–0.22). The analogue subsets use the same rule with N ≥ 5. They are reported and do not set verdict A.

**Verdict A** (over the 4 full-sample cells: 2 windows × 2 footings):
- MISSES if any diagnostic cell MISSES.
- MATCHES if every diagnostic cell MATCHES and at least one is diagnostic.
- Otherwise NOT DIAGNOSTIC.

The sign of any miss is reported. A negative sign means the law is too shallow, the same direction as the MW.

## Part B — inside view: direction dependence of the MW decline

**Sources.** The on-disk `.tex` sources in `../_external_data/cfg532_work/src/` (Wang+23, Jiao+23, Zhou+23, Sylos Labini+23/24, Feng+26, Mróz+19, Ablimit+20) and the review.

Every `table`/`deluxetable` environment is searched for a rotation curve tabulated separately by azimuth, hemisphere (z > 0 vs z < 0, north/south) or height. Figures are NOT digitised.

**Verdict B.**
- **DIRECTION-DEPENDENT** if on-disk split tables give 15–27.5 kpc slopes differing by > 2σ.
- **NOT** if split tables exist and agree within 2σ.
- **NO DATA** if no split table is on disk.

Authors' text-level statements about splits (e.g. "< 2% within 22 kpc") are quoted and turned into the largest Δslope they allow (δV/V at the window's outer end over ln(R_out/15)). They do not set the verdict. If NO DATA, list what would be needed (not fetched).

## Part C — disequilibrium bracket (ORDER OF MAGNITUDE, PROVISIONAL)

Using the review's on-disk numbers (non-circular motions 10–20 km/s at R ~ 20 kpc from Sgr bending waves; LMC reflex "tens of km/s"), compute the slope bias in a Jeans pipeline in two cases:
- (i) the bias ramps from 0 at 15 kpc to δv at 27.5 kpc: Δb ≈ (δv/V)/ln(27.5/15);
- (ii) a constant offset (which leaves the slope unchanged to first order).

Use V ≈ 200 km/s, with δv = 10 and 20 km/s. A recalled asymmetric-drift term σ_R ≈ 28–35 km/s (Zhou's 28.4 km/s beyond 13 kpc is on disk) gives the pressure-term scale σ_R²/V per unit log-derivative error. This is labelled an order-of-magnitude bracket, not a test. Recalled values are flagged.

## Overall verdict

- **MW TENSION LOCALISED TO MW** iff A = LAW MATCHES EXTERNAL SLOPES. The tension is then in the MW's measurement or dynamical state, not in the law's outer shape in general. This does NOT show which, and it does not remove the MW miss.
- **GRAVITY-LEVEL TENSION** iff A = LAW MISSES with mean Δ < −0.05 in the missing cell(s), i.e. external declines are also steeper than the law.
- **OPEN** otherwise. This includes a miss of the opposite sign, or NOT DIAGNOSTIC.

B = DIRECTION-DEPENDENT is reported as supporting evidence and cannot by itself produce LOCALISED.

## Controls and MUTATE

- **K1:** the slope estimator returns −0.5 for Kepler and 0 for flat.
- **K2:** the ALG implementation reproduces CFG516's `ALG_rotmod` weighted rms (0.1117 canonical / 0.1005 alt) within 0.005 dex on Q ≤ 2 points with g_obs, g_bar > 0. The selection differs slightly from CFG516's mask, hence the tolerance.
- **K3:** the MW combined Δ values are read from `cfg532b_results.json`, not retyped.
- **MUTATE (`CFG533_MUTATE=1`; outputs `_MUTATE`):** the law prediction is replaced beyond each window's inner edge R_lo by a Keplerian tail V_law(R_lo)(R/R_lo)^−½. The statistic MUST return LAW MISSES EXTERNAL SLOPES in all 4 cells, with positive sign. Exit 1 = DETECTED.

## Disclosures (pre-freeze)

- Seen before freezing: CFG532/532b README and results JSON (MW slopes and Z quoted above); CFG516 README (ALG rms values); the review's exceptionalism section, including Bariego+26's SPARC result as described there.
- Seen in the `.tex` sources: Wang+23 text (no significant V_φ dependence on |Z| for R > 15 kpc; V_R vs azimuth only in figures); Jiao+23 text (l-split < 2% within 22 kpc, comparable to the cross-term, ≤ ~8%, beyond); Zhou+23 text (±30° azimuth split ≲ 1%); Feng+26 text (azimuthal wedges ≤ 3%); SL24 (|z| slices, χ² table only). The table-environment captions were listed.
- No SPARC slope, coverage count or analogue count was computed or looked at before freezing.

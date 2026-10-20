# CFG931 FROZEN CRITERIA: do faint rotators carry the dwarf excess? (energy picture E vs kinematic picture K at matched g_bar)

Block 930–939 (LEDGER row CFG930–939, orchestrator reservation 2026-10-20). Frozen 2026-10-20, committed ALONE before any
script of this lane exists and before any residual (E) of this lane has been computed. Kind: DATA DISCRIMINATOR
(pre-registered). κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data and framework-native
quantities only (no HMcode, BAHAMAS or ΛCDM mass function). Extra mass is cold energy, not a particle. Not "theory closed".

## 1. Question

The law g_N = g²/(g + a0), a0 = ½c√(Gρ_DE), leaves an excess in faint pressure-supported dwarfs (about +0.37 dex at
g_bar < 1e-12; CFG827/828, CFG919 class mean +0.372 dex). Two pictures of that excess disagree about FAINT ROTATORS:

- **K (kinematic; CFG919 ordering):** the excess goes with pressure support. Faint rotators sit ON the law at any M*.
- **E (energy; lane CFG930, run in parallel, its directory not touched):** the excess is primordial cold matter left where
  baryonic feedback energy (∝ stars formed) was too small to settle it. Rotators of low M* (≲ 1e6–1e7 M☉) should carry an
  excess like dSphs at the same g_bar; bright rotators should not.

At matched g_bar, with E_X the mean excess of group X:
- (i) low-M* rotators, (ii) high-M* rotators, (iii) dSphs of matched M*;
- **E predicts E(i) ≈ E(iii) > E(ii) ≈ 0. K predicts E(i) ≈ E(ii) ≈ 0 < E(iii).**

## 2. Record check (done before freezing; targeted reads only)

- **CFG828** (criteria, README, .out, script): where dSphs overlap SPARC (g_bar ≥ ~1e-12, N = 8), dwarfs sit with the discs,
  D = +0.051 ± 0.073 dex; 21 dwarfs below SPARC's floor average +0.44 dex; SPARC is flat at +0.02–0.07 dex to its floor
  (8.3e-13; lowest 0.25-dex bin −12.00 holds 36 points).
- **CFG919** (criteria, A1, README; code lines 1–360, 377–400, 436–460): SELECTOR CONTRADICTED (FRAGILE under V6). Class
  means (ln): DW +0.856 ± 0.102, SPARC small (Mb ≤ 3e9) +0.137 ± 0.084, SPARC large +0.002 ± 0.050; W2 Spearman(f_P, ε_g)
  ρ −0.17, p 0.04 (weak anti-ordering, below the violation bar, confounded with mass).
- **CFG921** (README): no one-constant posit selects the excess; dwarf vs red-lens amplitude ratio 3–5.
- **CFG873 / CFG874** (READMEs): isolated dwarfs, gas counted. CFG873 HI-bearing trio +0.46 dex (stars only) → +0.23
  (primary gas) → +0.12 (all gas inside r½); CFG874 (11 isolated) c −0.100 ± 0.091, E +0.194 ± 0.077, UNDECIDED.
- **CFG860** (README head): NOT GAS; isolated gas-free and gas-bearing dwarfs both above the law.
- **LEDGER row CFG930–939**; no CFG930 directory or commit exists at freeze time, so CFG930's declared selector form is not
  available (section 4).

**This lane is NOT blind.** Disclosed in section 9: before freezing I saw CFG919's V0 cells for DW/SS/SL, CFG828's per-dwarf
Δ table, and an outcome-blind inventory count (M*, g_bar and quality cuts only).

## 3. Data inventory (on disk only; nothing downloaded)

**Rotators with RESOLVED rotation, baryonic mass and M\*:**
- **SPARC** (Lelli+16): `real_research/data/sparc_data/*_rotmod.dat` + `SPARC_Lelli2016c.mrt`. Cuts as CFG828/914/919:
  Q ≤ 2, Inc ≥ 30°, point cut errV/V_obs < 0.10. g_bar = (V_gas|V_gas| + 0.5 V_disk|V_disk| + 0.7 V_bul|V_bul|)/R (V_gas
  includes helium); g_obs = V_obs²/R. **M\* = 0.5 × L[3.6]** (Table 1, the Υ_disk convention). 147 galaxies, 2696 points.

**Rotators on disk that are NOT usable as graded rotators (inventory only):**
- **Lelli+15 tidal dwarfs** (`real_research/data/tdg/`, 6 objects): one asymmetric-drift-corrected V_circ at R_out, M_bar,
  M* = 3e7–1.1e8. Tidal origin (a confounder for a primordial-cold-matter picture), inclination-limited, single point.
  Reported as an INFO line (section 7), no class weight.
- **UNGC** (Karachentsev+13; `ungc_karachentsev2013.tsv`): W50, i, vAmp, log L_K, log M_HI, but no radius column in the
  on-disk extraction, so no g_bar. Not usable.
- **ALFALFA** (a100, Durbala+20, Leisman+17 HUDs), **FASHI DR2**, **MIGHTEE-HI** (CFG301): unresolved line widths without a
  resolved rotation radius. Not usable as resolved rotators.
- **LVD local-field dIrrs:** LVD has no rotation column (only stellar vlos_sigma). The gas-rich rotating dIrrs WLM,
  NGC 6822, IC 1613, Leo A, Sagittarius dIrr and Pegasus dIrr are in LVD but carry no rotation data on disk (excluded from
  CFG828/880 for that reason). No LITTLE THINGS, SHIELD, FIGGS or Leo P kinematics are on disk.

**Pressure-supported comparison sample (iii):** the 83 LVD dwarfs of CFG880 (Υ_V = 2, Wolf at r½ = (4/3) r_h, HI gas inside
r½ counted by CFG874's extended-root disc), via the CFG880 input slice exec'd read-only (writes refused). M\*_dw = 2 L_V.
Δ_dw = 2 log10(σ/σ_law), the same quantity as CFG919's DW E/ln 10.

**Outcome-blind inventory count (pre-freeze, scratch; no g_obs, σ or residual touched):**
- SPARC rotators with M* < 1e7 that pass the cuts: **1** (UGC 4483, 6.5e6; lowest point g_bar 10^−11.32).
  **Rotators with M\* < 1e7 and g_bar < 10^−11.5: 0.** UGCA 444 (M* 6.0e6) reaches 10^−12.33 but none of its points pass
  errV/V < 0.10.
- M* < 3e7 with g_bar < 10^−11.5: 3 (D564-8, DDO 154, NGC 3741). M* < 1e8: 8 (CamB, D564-8, D631-7, DDO 154, NGC 3109,
  NGC 3741, UGC 5764, UGCA 442).
- Per 0.5-dex cell, galaxies (low / high M*): split 1e7: [−12.5, −12.0) 0 / 3; [−12.0, −11.5) 0 / 31; [−11.5, −11.0) 1 / 103.
  Split 1e8: 3 / 0; 8 / 23; 12 / 92.
- CFG880 dwarfs per cell, M* < 1e7: 15 / 8 / 1; M* < 1e8: 17 / 10 / 2.

## 4. Groups and the M* split

- **Primary split (the E picture's declared range): M\* = 1e7 M☉.** (i) SPARC rotators with M* < 1e7; (ii) SPARC rotators
  with M* ≥ 1e7; (iii) CFG880 dwarfs with M*_dw < 1e7.
- **Extended splits (secondary, labelled E′): 3e7 and 1e8.** Same definitions. They test an energy picture whose threshold
  lies above the declared ≲ 1e6–1e7. Under E with a 1e7 threshold, rotators of 1e7–1e8 are "bright" and E predicts no
  excess for them, the same as K. So a K-FAVOURED class at an extended split does **not** exclude E at its declared
  threshold. An E-FAVOURED class there would still be reported as E′-FAVOURED.
- **E_SN/E_bind: NOT COMPUTED.** CFG930's declared form is not on disk at freeze time. At a fixed IMF, E_SN ∝ M*, so the M*
  split stands in. No energy ratio of this lane's own invention is used.
- M* conventions differ (3.6 μm Υ 0.5 vs V-band Υ 2); disclosed, not corrected.

## 5. Statistic (per footing, per split)

- **Residual:** Δ = log10(g_obs/g_law), g_law = g_bar ν_e(g_bar/a0), ν_e(y) = 1/(1 − e^{−√y}) (floor y ≥ 1e-15). Gas is
  counted in g_bar for every group.
- **Window W = [10^−12.5, 10^−11.5)**, the two CFG914/919 GRID cells (0.5-dex edges) at the dwarf onset. Cell index
  w = digitize(log g_bar, GRID) − 1, GRID = arange(−20, 10, 0.5) (w 15 = [−12.5, −12), w 16 = [−12, −11.5)).
- **Per system and cell:** rotator galaxy g: δ_{g,c} = mean Δ over its points in c. Dwarf d: δ_{d,c} = Δ_d if its g_bar is
  in c.
- **Group cell mean:** m_{X,c} = mean over the systems of X present in c.
- **Eligible cells:** c ∈ W with n_i,c ≥ 1, n_ii,c ≥ 3 and n_iii,c ≥ 3. **Weights** w_c ∝ n_i,c (the faint-rotator g_bar
  distribution) over eligible cells.
- **E_X = Σ_c w_c m_{X,c}.** Differences: **d_K = E(i) − E(ii)** (K predicts 0, E predicts Δ_ref); **d_E = E(iii) − E(i)**
  (E predicts 0, K predicts Δ_ref); **Δ_ref = E(iii) − E(ii)** (the lever).
- **Errors:** independent bootstrap over systems within each group (4000 draws, rng 931; a galaxy's cells move together;
  weights renormalised over the cells a draw populates). For dwarfs σ_iii = max(bootstrap sd, √(Σ_c w_c² Σ_d σ_Δ,d²)/n_c),
  with σ_Δ,d = 2 e_d/(σ_d ln 10), e_d the σ error on the side of σ_law (CFG914). **Systematic floor F = 0.05 dex per group
  mean** (CFG919's per-cell floor) in quadrature: σ(A − B)² = σ_A² + σ_B² + 2F².

## 6. Classes (per footing, per split)

1. **NOT DIAGNOSTIC (DATA)** if no eligible cell, or N_i < 5 galaxies, N_ii < 5 galaxies or N_iii < 3 dwarfs over the
   eligible cells.
2. **NOT DIAGNOSTIC (NO LEVER)** if z(Δ_ref) < 2: the dSphs of matched M* do not stand above the bright rotators in the
   window, so neither picture's distinguishing prediction is testable there.
3. **E-FAVOURED** (E′-FAVOURED at an extended split): z(d_K) ≥ 2 and z(d_E) < 2.
4. **K-FAVOURED:** z(d_E) ≥ 2 and z(d_K) < 2.
5. Otherwise **NOT DIAGNOSTIC**, sub-labelled INTERMEDIATE (both ≥ 2) or UNRESOLVED (neither).

**Per split:** a class holds only if both footings give it; otherwise NOT DIAGNOSTIC (SPLIT BY FOOTING), both reported.
**Lane class = the primary split's class.** The extended splits give a separate, labelled secondary class.

**Variants** (reported per footing and split; if any changes a class, the class is labelled FRAGILE, not changed):
- V1 floor 0 (statistical errors only); V2 floor 0.10 dex;
- V3 pressure-support bracket for rotators: g_obs = (V_obs² + 2σ_g²)/R with σ_g = 8 km/s, all SPARC points (it raises
  faint rotators most, i.e. toward E);
- V4 dwarf sample of CFG828 (29 dwarfs, Υ_SFH, no gas, gas-rich dIrrs excluded) in place of CFG880's 83;
- V5 window [10^−12.5, 10^−11.0);
- V6 pairwise cells: d_K over cells with (i) and (ii), d_E over cells with (i) and (iii), each weighted ∝ n_i,c; Δ_ref =
  d_K + d_E;
- V7 group (iii) restricted to M*_dw within [min M*_i, split).

## 7. Power, stated in advance

Minimum detectable difference (one-sided z = 2 at 80 % power): MDD = 2.84 σ. Assumed scatters: rotator galaxy-mean
residual 0.12 dex (the published RAR scatter, about 0.11–0.13 dex); dwarf scatter 0.35 dex (CFG828). Floor F = 0.05 dex.

| split | N_i / N_ii / N_iii (eligible cells) | σ(d_K) | MDD_K | σ(d_E) | MDD_E | expected lever Δ_ref |
|---|---|---|---|---|---|---|
| 1e7 | 0 / 31 / 8 | — | — | — | — | — (no group i) |
| 3e7 | 3 / 28 / 9 (cell w 16) | 0.102 | 0.29 | 0.153 | 0.43 | ≈ 0.15–0.20 |
| 1e8 | 8 / 23 / 10 (cell w 16) | 0.086 | 0.25 | 0.138 | 0.39 | ≈ 0.15–0.20 |

Without the floor: MDD_K 0.14, MDD_E 0.34 dex at 1e8. The expected lever comes from the record: CFG919's DW cell at
[−12, −11.5) is +0.40 ln (+0.175 dex), and CFG828's dwarfs in that range sit about +0.15–0.2 dex above SPARC.
**Advance statement:** the primary split cannot run (N_i = 0). At the extended splits the lever (≈ 0.17 dex) is below
both MDDs, so the on-disk data are expected to be NOT DIAGNOSTIC (most likely NO LEVER or UNRESOLVED). The script prints the
realised MDDs (no class weight). A decisive test needs faint rotators at g_bar < 1e-12, where the dSph lever is ≈ 0.3–0.7
dex (CFG828/919).

## 8. Controls (any K failure stops the lane: no class is reported)

**K-tests (own code):**
- **K1:** CFG828 reproduced: N_in, mean_D, se_D, sparc_median_all, out_of_range_mean_delta for canonical|nu_e and alt|nu_e
  match `cfg828_results.json` to ≤ 1e-9 (bootstrap default_rng(828) in CFG828's loop order).
- **K2:** CFG919 SPARC class means SS and SL (E and se, V0, both footings) and W2 (ρ, p, both footings) match
  `cfg919_results.json` to ≤ 1e-9 (cells_sparc recipe, rng 919 per class, floor 0.05 dex, GLS class mean).
- **K3:** CFG919 DW class mean (E, se, both footings) matches to ≤ 1e-9, through the CFG880 input slice exec'd read-only.
- **K4:** SPARC loader gives 2696 points / 147 galaxies; the lowest-M* galaxy in Table 1 is UGCA 444 at 6.0e6.

**MUTATE inject (`CFG931_MUTATE=inject` → `cfg931_MUTATE_inject.out` / `cfg931_results_MUTATE_inject.json`):**
- **I-30:** +0.30 dex added to log g_obs of every group-(i) point (the record's dSph-level excess), every split, both
  footings. Required: d_K moves by exactly +0.30 (≤ 1e-9) wherever N_i > 0. **Recovery required "when N allows"**, defined
  as: the data gate passes and 2.84 σ(d_K) ≤ 0.30. There the class must be E-FAVOURED (E′ at an extended split), or the
  control FAILS and no class is reported. Where N does not allow, the outcome is reported as "not recoverable at this N".
- **I-E (E world):** group (i) shifted so that E(i) = E(iii) at the point estimate (shift = d_E). Reported as a realistic
  power diagnostic: the class it gives shows whether the E picture's own prediction is detectable here. No pass/fail.

**MUTATE shuffle (`CFG931_MUTATE=shuffle` → `cfg931_MUTATE_shuffle.out` / `cfg931_results_MUTATE_shuffle.json`):**
- **S1:** on the I-30 data, shuffle the low/high-M* labels among the rotators present in the eligible cells (group sizes
  kept), 1000 draws (rng 9311). Required where N allows: median d_K over shuffles ≤ ½ d_K(I-30), and E-FAVOURED in ≤ 10 %.
- **S2:** on the real data, the permutation p of d_K (no class weight).

## 9. Disclosure (what I saw before freezing)

- **CFG919 V0 cells** (from `cfg919_results.json`), canonical, ln units: DW w 15 +0.603 (17 dwarfs), w 16 +0.403 (10);
  SS (Mb ≤ 3e9) w 16 +0.079 (19 galaxies), no SS cell at w 15; SL w 16 −0.081 (12). Alt: DW w 16 +0.314; SS w 16 −0.009;
  SL w 16 −0.169. Class means and W2 as in section 2.
- **CFG828's per-dwarf Δ table** and SPARC bin medians (in its .out).
- The outcome-blind counts of section 3 (two scratch scripts; they read M*, g_bar, quality cuts and the CFG880 sample's
  M_V, r_h and HI only).
- Data headers: SPARC MRT, LVD column list and PROVENANCE, TDG files (all rows), UNGC header and first row, FASHI README;
  directory listings of `real_research/data`, `real_research/data/dsph`, `_external_data`; heads of the CFG92 and CFG301
  READMEs (no low-M* resolved rotators there).
- **Expectation formed from this:** at [−12, −11.5) low-mass rotators (Mb ≤ 3e9) sit near the law while the dwarfs sit about
  +0.17 dex above it. This leans K, but the mass split (Mb ≤ 3e9) is not this lane's M* split, and the lever is small.
  Expected outcome: primary NOT DIAGNOSTIC (DATA); extended splits NOT DIAGNOSTIC (lever below MDD).

I have not computed any residual of this lane's groups, any d_K / d_E / Δ_ref, or any class.

## 10. If NOT DIAGNOSTIC for lack of data

The README names the public data sets that would decide it (resolved HI kinematics of rotators with M* < 1e7 reaching
g_bar < 1e-12: LITTLE THINGS, SHIELD, FIGGS, VLA-ANGST, Leo P and similar), with sizes only where on-disk notes give them,
for the owner's download decision. Nothing is downloaded by this lane.

## 11. Compute and hygiene

- Compute: one core (OMP_NUM_THREADS=1, nice -n 10), < 1 GB, one process at a time; numpy/scipy; seconds.
- No other lane's files edited (CFG828/880/919 read or exec'd read-only with writes refused). CFG930's directory not touched.
- Commits with explicit paths only. Any post-hoc change is a dated, labelled amendment (AMENDMENT_A*.md), committed before
  the numbers it affects are reported.

# CFG940 FROZEN CRITERIA: are faint gas-rich rotators ABOVE, ON or BELOW the law at low g_bar? (McQuinn+2022, 25 dwarfs)

Block 940–949 (LEDGER row CFG940–949, orchestrator reservation 2026-10-20 ~21:30, owner-approved download). Frozen
2026-10-20, committed ALONE before any script of this lane exists and before any number of this lane has been computed by
code. Kind: DATA TEST (pre-registered). κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data
and framework-native quantities only (no HMcode, BAHAMAS or ΛCDM mass function). Extra mass is cold energy, not a particle.
Not "theory closed". **This lane is NOT blind** (section 10).

## 1. Question

The law g_N = g²/(g + a0), a0 = ½c√(Gρ_DE), scored with the kernel ν_e(y) = 1/(1 − e^{−√y}) (CFG827/828/931), leaves an
excess of about +0.37 to +0.44 dex in faint PRESSURE-SUPPORTED dwarfs at g_bar < 1e-12 (CFG828: +0.44 below SPARC's floor;
CFG919 DW class mean +0.372). SPARC has no faint rotator (M* < 1e7) below g_bar ~ 10^−11.5, so CFG931 was NOT DIAGNOSTIC
(DATA). McQuinn+2022 (ApJ 940, 8; on disk, committed 64cee36d7) give 25 faint gas-rich rotators (7 SHIELD, 12 VLA-ANGST,
6 LITTLE THINGS) with one asymmetric-drift-corrected rotation speed V_cor at the HI extent R_max, M*, M_HI and M_bary.

Three outcomes and what they mean:
- **ABOVE** (like the dSphs at matched g_bar): the excess is a small-system property, independent of kinematics.
- **ON**: the kinematic picture (excess goes with pressure support; CFG919/931 point estimates), and CFG934's cooling-floor
  prediction (its floor stops acting above M_b ~ 1e5 M☉, so rotators with M_b ~ 1e7–1e9 sit on the bare law).
- **BELOW**: a deficit. That would be a new problem for the law itself unless a declared systematic explains it. (CFG936:
  systems without a primordial halo sit at Newton; an INFO line reports the Newtonian reading, no class weight.)

## 2. Data (on disk only; nothing downloaded)

- `real_research/data/faint_rotators_mcquinn2022/apjac9285t1_mrt.txt` (Table 1) and `apjac9285t2_mrt.txt` (Table 2), passed
  to the script as arguments, parsed by the MRT byte positions with this lane's own code, run with `python3 -I`. Untrusted
  data: no value is executed; sha256 checked against PROVENANCE.md (K0).
- Record inputs read only: SPARC rotmod files and Table 1 (`real_research/data/sparc_data/`, `SPARC_Lelli2016c.mrt`);
  `cfg827_results.json`, `cfg824_results.json`, LVD csvs (CFG828's 29 dwarfs); `cfg828_results.json`, `cfg919_results.json`
  (K targets); CFG880's input slice exec'd read-only with writes refused, exactly as CFG931 did (variant V10 only).

## 3. Per-galaxy quantities (the 25 McQuinn+22 galaxies = the faint-rotator sample)

- **R_max (primary):** R = (D_PV/2) × Dist, arcsec → rad (unrounded). K3 requires it to reproduce the tabulated R_max to
  ≤ 0.051 kpc. Error e_R = tabulated e_Rmax. Variant V16 uses the tabulated (rounded) R_max.
- **V (primary):** V_cor (asymmetric-drift corrected). e_V = e_Vcor. If K4 finds that e_Vrot does NOT already contain the
  inclination error, the term V_rot·cot i·e_i (e_i in rad, converted to V_cor by V_rot/V_cor) is added in quadrature;
  otherwise it is not added again (no double counting).
- **g_obs = V²/R** (primary). V_rot in place of V_cor is variant V1.
- **Helium:** the MRT header does not define M_bary. K2 finds which f_He ∈ {1.00, 1.33, 1.36, 1.40} reproduces
  logMbary = log10(10^logM* + f_He·10^logMHI) for all 25 to ≤ 0.015 dex. If f_He ≥ 1.33, M_bary is used as tabulated
  (helium included). If only 1.00 works, M_bary is recomputed as M* + 1.33 M_HI. Gas in estimator B is always 1.33 M_HI.
- **g_bar, estimator A (primary):** g_bar^A = G·M_bary/R². R_max is the HI extent, so this is an upper bound on the
  spherical enclosed-mass g_bar. Because g_law rises with g_bar, **E under A is a lower bound on E** (spherical reading). A
  thin disc can pull up to ~20 % harder than G·M_tot/R² at 3–6 scale lengths; variant B5 measures that.
- **g_bar, estimator B (bracket):** g_bar^B = G·[f(R/R_d*)·M* + f(R/R_s)·1.33·M_HI]/R², f(x) = 1 − (1 + x)e^{−x} (exponential
  disc, enclosed fraction).
  - Gas scale R_s: CFG873/874's recipe copied unchanged: Wang+16 R_HI = ½·10^(0.506 log M_HI − 3.293) kpc, solve
    Σ(R_HI) = 1 M☉/pc² for an exponential disc, extended (larger) root; fallback R_HI/2 (fallbacks counted and printed).
  - Stellar scale R_d*: a declared size relation fitted by this lane to raw on-disk data: OLS of log10 Rdisk on log10 M*
    over SPARC Table 1 galaxies with 0 < M* < 1e9 and Rdisk > 0 (M* = 0.5 L[3.6], SPARC's convention). The fit (a, b, rms)
    is printed.
  - Bracket variants (reported with B): B2 compact (smaller) root; B3 R_HI := R_max (the measured extent); B4 R_d* × 2;
    B5 Freeman thin disc for both components with B's scale lengths (V² = 2GM/R_d·y²[I0K0 − I1K1], y = R/2R_d);
    B6 R_d* ÷ 2.
- **Residual:** E = log10(g_obs/g_law(g_bar)), g_law = g_bar·ν_e(g_bar/a0), y floor 1e-15, per footing.
- **Per-galaxy error σ_E:** finite differences over V (±e_V), R (±e_R, entering g_obs and g_bar together) and the masses
  (A: ±e_logMbary; B: ±e_logMstar and ±e_logMHI separately), in quadrature: σ_E² = Σ_k [(E(x_k⁺) − E(x_k⁻))/2]².

## 4. Comparison groups

- **(a) dSphs (primary): CFG828's 29 dwarfs** (CFG827 Υ_SFH M*, CFG824 σ, Wolf r½ = (4/3) r_h, g_bar = G(M*/2)/r½²,
  g_obs = 3σ²/r½, gas-rich dIrrs excluded), built by CFG931's K1 code path (copied), E_d = log10(g_obs/g_law), σ_E,d =
  2·eso/(so·ln 10). K5 reproduces CFG828. **Variant V10:** CFG880's 83 LVD dwarfs (Υ_V = 2, gas inside r½), K6 reproduces
  CFG919's DW class mean.
- **(b) SPARC rotators:** CFG931's loader (Q ≤ 2, Inc ≥ 30°, errV/V < 0.10), per-galaxy mean E in each cell, ν_e. The
  McQuinn+22 galaxies also in SPARC (DDO154, NGC3109, NGC3741, UGC04305 = Ho II, UGC04483, UGC07559 = DDO 126,
  UGC07577 = DDO 125, UGCA444 = WLM) are removed from the SPARC group and reported as overlap rows (INFO I4).

## 5. Windows, matching, statistics (per footing, per estimator)

- **Cells:** GRID = arange(−20, 10, 0.5) (CFG914/919/931), c = digitize(log10 g_bar, GRID) − 1.
- **W1 (primary window): g_bar < 1e-12**, each estimator's own g_bar. **WS (secondary): all g_bar.**
- **Mean E** = unweighted mean over the window's rotators (N galaxies, one point each).
  se_E = √(max(sd/√N, √Σσ_E²/N)² + F²), **F = 0.05 dex** systematic floor (CFG919/931's per-group floor).
- **Matched dSph level:** eligible cells hold ≥ 1 window rotator and ≥ 3 dSphs. w_c = n_rot,c/Σ n_rot (eligible cells).
  E_dSph,m = Σ w_c m_dSph,c; dSph cell se_c = max(sd_c/√n_c, √Σσ_E,d²/n_c); se_dSph,m = √(Σ w_c² se_c²). E_rot,m = mean over
  the N_m rotators in eligible cells, se_rot,m = max(sd/√N_m, √Σσ_E²/N_m) (measurement term alone if N_m = 1).
  **D = E_dSph,m − E_rot,m, σ_D = √(se_rot,m² + se_dSph,m² + 2F²).**
- **SPARC matched level** (same recipe, cells with ≥ 3 SPARC galaxies, galaxy-mean E per cell, se_c = sd_c/√n_c):
  D_SP = E_rot,m′ − E_SP,m with σ = √(se² + se² + 2F²). Reported; no class weight.

## 6. Classes

**Primary window W1, per footing and estimator, in this order:**
1. **NOT DIAGNOSTIC (DATA)** if N < 5 rotators in W1.
2. **BELOW** if mean E ≤ −2 se_E.
3. **ABOVE** if mean E ≥ +0.20 dex and D exists and |D| < 2 σ_D (consistent with the matched dSph excess). Sub-label
   "(z < 2)" if mean E < 2 se_E.
4. **ON** if |mean E| < 2 se_E and D exists and D ≥ 3 σ_D (the matched dSph excess excluded at ≥ 3σ).
5. Otherwise **NOT DIAGNOSTIC**, sub-labelled NO dSph MATCH (no eligible cell), ELEVATED BELOW dSph LEVEL (mean E ≥ 2 se_E,
   not ABOVE), UNRESOLVED (|mean E| < 2 se_E, D < 3 σ_D) or OTHER.

- **Footings:** a class holds only if both footings give it (main token); otherwise NOT DIAGNOSTIC (SPLIT BY FOOTING).
- **Lane class = estimator A's W1 class.** Estimator B's W1 class (and B2–B6) are computed. If any of them differs from A,
  the lane class carries **BRACKET-DEPENDENT** with the differing classes listed.
- **FRAGILE:** if any non-subset systematic variant (V1–V4, V6, V7, V9–V12, V16), applied to A, changes A's class. Subset
  variants (V5, V13, V14, V15) are reported with no FRAGILE weight (they lose N).

**Secondary (WS, all 25, labelled secondary, no lane-class weight), per footing and estimator:** S-BELOW if mean E ≤ −2 se_E;
S-ABOVE if mean E ≥ +2 se_E; S-ON otherwise. D (matched dSphs) and D_SP (matched SPARC) are reported beside it. Same footing,
bracket and FRAGILE labels.

## 7. Systematics, declared (each alone, on A and B)

| id | systematic | change | direction on E |
|---|---|---|---|
| V1 | asymmetric drift removed | V = V_rot | down |
| V2 | asymmetric drift doubled | V² = V_rot² + 2(V_cor² − V_rot²) | up |
| V3 | inclination low by 1σ (low i inflates V) | i′ = max(i − e_i, 10°), V_rot′ = V_rot sin i/sin i′, V² = V_rot′² + (V_cor² − V_rot²) | up |
| V4 | inclination high by 1σ | i′ = min(i + e_i, 90°), same recipe | down |
| V5 | low-inclination galaxies dropped (subset) | keep i ≥ 40° | — |
| V6 | distance −10 % (all) | g_obs × 1/0.9; R × 0.9; masses × 0.81 | up |
| V7 | distance +10 % (all) | the inverse | down |
| V9 | kernel | ν_simple, the law's algebraic form g_N = g²/(g + a0); dSphs re-scored with it | — |
| V10 | dSph sample | CFG880's 83 LVD dwarfs, gas counted | — |
| V11 / V12 | floor | F = 0 / F = 0.10 dex | — |
| V13 / V14 | rising-curve lower bound (subsets) | plateau (P) only / rising (R) only | — |
| V15 | beam smearing proxy (subset) | D_PV ≥ 100 arcsec only | — |
| V16 | R_max rounding | tabulated R_max | — |

- **Enclosed-mass bracket:** A vs B (and B2–B6), section 6.
- **Combined corner C-UP (INFO, no class weight):** B + V2 + V3 + V6 together, the largest upward push the declared
  systematics allow. If C-UP stays at mean E ≤ −2 se_E, the deficit is not explained by the declared systematics at their
  declared sizes; if it reaches the law, a combination of them can.
- **The "still rising" issue.** A rising curve's V(R_max) is a valid point measurement at R_max: under B (enclosed mass at
  R_max) it is a fair test of the law there. Under A (total mass) it is not: the mass beyond R_max is counted, so rising
  curves are pushed down most. For the BTFR (V_flat vs M_bary) a rising V(R_max) is only a lower bound on V_flat, which is
  part of what a published "turndown" can be made of. The R/P split is printed for A and B.
- **Distance:** in the deep regime E is nearly independent of R (R cancels for total mass), so a distance error acts
  through g_obs ∝ 1/D: −10 % in D gives about +0.046 dex. Per-galaxy distance errors (2–5 %) are inside e_Rmax/e_V.

## 8. Power, stated in advance (assumed, not measured)

Per-galaxy σ_E from e_V/V ≈ 0.05–0.25: about 0.05–0.2 dex; with intrinsic scatter about 0.1 dex, sd ≈ 0.2 dex. dSph side:
about 15 dwarfs per matched set, scatter 0.35 dex (CFG828), se_dSph ≈ 0.09.
- N = 5 in W1: se_E ≈ 0.10 (floor included); BELOW needs mean E ≤ −0.20; σ_D ≈ 0.14, so ON needs D ≥ 0.43: with the dSphs
  at +0.37 to +0.44, ON is reachable only if the rotators sit at or a little below the law.
- N = 10: se_E ≈ 0.08, σ_D ≈ 0.125, ON needs D ≥ 0.375.
- **Advance statement:** ON is power-limited by the dSph side; BELOW and ABOVE are reachable at N ≥ 5.

## 9. Controls (any K failure stops the lane: no class is reported)

**K-tests (own code):**
- **K0:** both files' sha256 equal the PROVENANCE.md values; 25 rows each, same names in the same order; 7 AGC (SHIELD) rows.
- **K1:** log M_dyn = log10(V_cor²·R_max/G) from the tabulated V_cor and R_max reproduces the table's logMdyn for all 25
  to ≤ 0.05 + δ_round, δ_round = 2·0.5/(V ln 10) + 0.05/(R ln 10) (G = 4.30091e-6 kpc (km/s)² M☉⁻¹). The same check with
  V_rot is printed (it tells which speed the paper used).
- **K2:** the helium factor (section 3); passes if some f_He in the list reproduces all 25 to ≤ 0.015 dex.
- **K3:** V_rot = V_PV/(2 sin i) to ≤ 1.0 km/s for all 25 (V_PV is the full PV width); recomputed R_max to ≤ 0.051 kpc.
- **K4 (decision, not pass/fail):** e_Vrot vs √((e_VPV/(2 sin i))² + (V_rot cot i e_i)²) and vs the same without the
  inclination term; the inclination error counts as included in e_Vcor if the rms residual is smaller with it.
- **K5:** CFG828 reproduced through this lane's code path (CFG931's K1 recipe): N_in, mean_D, se_D, SPARC median, out-of-
  range mean, canonical and alt ν_e, ≤ 1e-9 against `cfg828_results.json`.
- **K6:** CFG919 DW class mean (E, se, both footings) ≤ 1e-9 via the CFG880 slice (variant V10's input).
- **K7:** SPARC loader 2696 points / 147 galaxies.

**MUTATE plant (`--mode plant` → `cfg940_MUTATE_plant.out` / `cfg940_results_MUTATE_plant.json`).** A plant at level T
replaces each window rotator's log g_obs by log g_law(g_bar) + T + (E_i − Ē), keeping the observed scatter and σ_E; the
planted mean must equal T to ≤ 1e-9 (pipeline check). Per footing, estimator A and B, window W1 and WS:
- **P37 (T = +0.37):** must classify ABOVE wherever the data gate passes, D exists and |E_dSph,m − 0.37| < 2σ_D (the planted
  value is itself consistent with the matched dSph level). Elsewhere reported as "not required (reason)". In WS: S-ABOVE
  required where 0.37 ≥ 2 se_E.
- **PdSph (T = E_dSph,m):** must classify ABOVE where the data gate passes, D exists and E_dSph,m ≥ 0.20.
- **P0 (T = 0):** must classify ON where the data gate passes, D exists and E_dSph,m ≥ 3σ_D ("power allows"); elsewhere
  reported as "ON not reachable at this N". In WS: S-ON required.
- **P−37 (T = −0.37):** must classify BELOW where the data gate passes and 0.37 > 2 se_E. In WS: S-BELOW required.

**MUTATE shuffle (`--mode shuffle` → `cfg940_MUTATE_shuffle.out` / `cfg940_results_MUTATE_shuffle.json`).** Rotator/dSph
labels permuted within each eligible cell (per-cell counts kept), 1000 draws (rng 9401), estimator A and B, both footings,
W1 and WS:
- **S1 (real data):** required |median D_shuf| ≤ 0.25 σ_D(real) and the fraction with |D_shuf/σ_D,shuf| ≥ 3 ≤ 0.05.
  The fraction with |z| ≥ 2 is printed.
- **S2 (on the P0 data):** required median D_shuf ≤ ½ D(P0) where D(P0) ≥ 2σ_D.
- Required only where the data gate passes and D exists; elsewhere "not run (reason)".

Exit codes: 0 = K passed and every required control in the mode met; 1 = a required MUTATE control failed; 2 = a K-test
failed (no class). Run order: K, MUTATE plant, MUTATE shuffle, then main.

## 10. Disclosure (what I knew or saw before freezing)

- **McQuinn+22's own reading was known:** the paper (its title says so) reports a turn-down of the baryonic Tully–Fisher
  relation at low masses (faint dwarfs rotating slower than the extrapolated relation) and a changing baryon fraction.
  That is a published BTFR reading, not a framework verdict, and not this lane's statistic (a point test at R_max).
- **Seen:** both MRT tables in full (all 25 rows of each) while reading the byte formats; PROVENANCE.md; the SPARC MRT
  header; the names of the SPARC rotmod files matching the overlap aliases (directory listing only).
- **Mental arithmetic while reading the format, disclosed:** helium 1.33 checked by hand on AGC110482, NGC3109 and
  Sextans A (it fits); log M_dyn checked on AGC110482 (7.37 vs 7.4); e_Vrot of Sextans A is consistent with containing the
  8° inclination error. **For AGC110482 I estimated g_bar^A ≈ 2e-11 and g_obs ≈ 9e-12, i.e. below even Newton with the
  total baryons**, and that its Wang+16 R_HI (≈ 1.2 kpc) is about twice its R_max. I also estimated g_bar^A of order
  2–8e-12 for NGC3109, DDO154 and Ho II. No other galaxy was estimated.
- **Record read:** CFG931 (criteria, README, A1, A2, code), CFG828 and CFG827 READMEs, CFG873/CFG880 gas functions, the
  CFG934 README head, LEDGER rows CFG910–CFG936.
- **Expectation formed from this:** under A most of the 25 have g_bar above 1e-12 (small R_max), so W1 under A may fail the
  data gate (NOT DIAGNOSTIC (DATA)); B lowers g_bar and may populate W1. In WS a deficit under A is expected at least for the
  smallest-R_max galaxies. Whether it survives B, the overlap calibration and the declared systematics I do not know.

## 11. INFO lines (no class weight)

- **I1** rising vs plateau split (V13/V14) with the BTFR note of section 7.
- **I2** M* < 1e7 subset (CFG931's primary split): N and mean E, W1 and WS.
- **I3** Newtonian reading (CFG936): mean log10(g_obs/g_bar) with se; "AT NEWTON" if |mean| < 2 se.
- **I4** overlap calibration: for the 8 SPARC overlaps, SPARC's own g_bar and V at the same angular radius
  (R_SP = R_max·D_SPARC/D_McQ; rotmod without the point cut; Υ 0.5/0.7; out of range by > 10 % → no value): E_McQ vs
  E_SPARC, and log(g_bar^SPARC/g_bar^A), log(g_bar^SPARC/g_bar^B). Reading rule: the estimator whose median log ratio is
  closer to 0 is the better calibrated end of the bracket.
- **I5** survey split (SHIELD / VLA-ANGST / LITTLE THINGS) mean E.
- **I6** C-UP corner (section 7).

## 12. Compute and hygiene

- One core (OMP_NUM_THREADS=1, nice -n 10), < 1 GB, one process at a time; numpy/scipy; seconds. Nothing downloaded.
- No other lane's files edited (CFG828/880/919/931 read or exec'd read-only with writes refused). Data files untouched.
- Commits with explicit paths only; no push. Any post-hoc change is a dated, labelled amendment (AMENDMENT_A*.md),
  committed before the numbers it affects are reported.

κ = ½ FITTED; footings never pooled; not theory closed.

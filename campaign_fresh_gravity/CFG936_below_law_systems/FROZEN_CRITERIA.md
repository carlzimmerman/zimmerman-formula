# CFG936 FROZEN CRITERIA: systems below the law (Lelli+15 tidal dwarfs, NGC 1052-DF2/DF4). Score CFG930's sealed S1; can the framework put a system below its own law without an external-field effect?

- **Block:** CFG930–939. The LEDGER reservation (commit 4e4f0f5e4) names CFG936 for this lane. This lane uses CFG936 only.
- **Kind:**
  - Part A: score of a SEALED statement (CFG930 S1; seal commit cbb3b9888, sha256 57b1141e…).
  - Part B: a route test. Three routes are tested: two framework-native, and one declared contrast that is not a framework
    route. The lane adds no new constant and fits none.
- **Status of this file:** committed ALONE, before any script exists and before any number of this lane is computed.
- **Standing rules:**
  - κ = ½ is FITTED.
  - The footings 9.3603e-11 and 1.1312e-10 m/s² are scored separately and never pooled.
  - The extra mass is cold energy, not a dark-matter particle.
  - Verdicts are framework-native and use raw data only. No ΛCDM machinery enters.
  - The framework's own numbers are EFE-free: the acceleration-response theorem CL-AR (PAPER55), and CFG925 R3 (satellites
    show no EFE). The EFE route (iii) is therefore a declared contrast only.
  - No result here means "theory closed", and nothing here says the data favour the framework.

## 1. What was seen before freezing (disclosure; this lane is NOT blind)

**Read in this session, before this file:**

| source | what was seen |
|---|---|
| CFG930 | SEALED_PREDICTIONS.md (hash verified: 57b1141e…); criteria §9. S1 says "predicted excess = 0 at every eps (same as the bare law). A TDG sample (gas counted, the same estimator) with mean excess > 2 se above the law contradicts H-ELS". Criteria §9 adds "must sit on the law". |
| CFG931 | README, AMENDMENT A2 and the INFO code block. **The TDG INFO number:** mean Δ = −0.690 (canonical) / −0.728 (alt) dex, per object −0.40 to −0.89 (canonical), velocity-only σ 0.15–0.38, log g_bar −11.71 to −11.03 |
| CFG933 | README and the per-galaxy JSON. DF2: E_obs −1.709 ± 0.541. DF4: −2.170 ± 0.794 (canonical). The z values (−3.22 / −2.79 canonical, −3.37 / −2.88 alt) are taken against P2's E_pred (+0.034 / +0.041), not against the bare law. R4 secondary σ: DF2 10.8, DF4 8.0 km/s |
| CFG763 | README, criteria, code and output. τ_min,95 is 0.724 / 0.832 Gyr at −1σ ages and 1.202 / 1.380 Gyr at nominal ages; the upper bound 3.47 Gyr comes from SPARC. **CFG763 used the 1-D EFE at nominal host mass** for the six Lelli TDGs, and was calibrated on those same TDGs plus Arp 72c |
| CFG768 | README and JSON. Part A (α_P = 0): f_cap primary 5.9e-4 (DF2) / 1.6e-3 (DF4), bracket maximum 1.0 at fallback ends; label OTHER. Part B: universal clock at the lenient 6 Gyr gives f 0.82, Z −3.97 / −4.27 (DF2) and −3.93 / −4.18 (DF4): EXCLUDED |
| CFG769 | README. C-A6 ("own supply"), sealed predictions for six other trail galaxies |
| CFG657 | README and code (capture channels S, F, D; GAL dict with vD+22 ages; HOSTS; PRIMARY and BRACKET) |
| CFG7 | FG041/FG001 README and C2 code. The six TDGs are Newtonian (χ² 1.09); the law+EFE is worse by Δχ² +5.2 to +12. FG001 says "formed embedded … tidal dwarfs, … collision debris such as DF2/DF4: Newtonian". C2: Lelli's Table 9 is reproduced at a0 1.25e-10 (max \|dV\| 1.03 / 1.42 km/s) |
| CFG441 | README. Tier B Newton χ² 1.10 for 7; the law+EFE is worse by +33 / +39 |
| THEORY_CANONICAL | 10-14 S3/S4: S4 says "Debris born moving through resting cold energy captures none (tidal dwarfs)". v2 (10-16) S3 replaced "each halo settles only its own supply" with the catchment rule (supply 5.364 N M_b, N = 1/f_ret), and S4 kept the debris line. The 10-18 addendum says TDGs and the trail are not diagnostic for clumps |
| CFG804 | fret_of / N_of code |

**Back-of-envelope expectations (mental arithmetic while reading; no script).** They are written here so that none can be
claimed later as a discovery:
- **X1.** S1 is expected to read NOT DIAGNOSTIC (BELOW THE LAW), because of CFG931's −0.69 dex.
- **X2.** The zero-supply (Newtonian) prediction for the TDGs is Δ ≈ −log10 ν ≈ −0.73 dex mean, against −0.69 observed
  (CFG7 already shows χ²_N ≈ 1.1). Expected: route (i) EXPLAINS T.
- **X3.** The clock at τ = 3.47 Gyr with TDG ages 0.35–0.75 Gyr gives f ≈ 0.10–0.19 and Δ_pred ≈ −0.47 to −0.57, mean about
  −0.5 against −0.69, with se ≈ 0.1. That is borderline. This lane computes it EFE-free.
- **X4.** For DF2/DF4, Newtonian gives E_N ≈ −2.0 / −1.9 against −1.71 / −2.17, which is consistent. The clock at ages
  ≥ 6 Gyr gives f ≥ 0.82 and E ≈ −0.17, which fails (as CFG768 B).
- **X5.** The EFE for DF2, from NGC 1052 (1e11 M☉ at about 79 kpc projected), gives E_EFE ≈ −0.8 against −1.71
  (z ≈ −1.6). DF4 sits about 21 kpc in projection from NGC 1035.

## 2. Data (on disk only; nothing downloaded)

- **TDGs (class T):** the six Lelli+15 TDGs, from `real_research/data/tidal_dwarfs/lelli2015_tdg.csv`:
  - V_circ ± e (asymmetric-drift corrected);
  - M_bar ± e, where M_bar = 1.37 M_HI + M_mol + M_*;
  - M_star, M_atom, M_mol;
  - R_out ± e;
  - t_orb ± e, t_merg/t_orb;
  - host L_K and D_p.

  Their shared columns (V, eV, M_bar, eM_bar, R_out, eR_out, D_p) must equal those of `real_research/data/tdg/lelli2015_tdgs.csv`,
  the file CFG931 read (identity check, K1).
- **Arp 72c:** `CFG441_old_tdgs_tidal_origin/data/tierB_arp72c.csv`. It is used ONLY in the CFG763 K reproduction (K3) and
  in the EFE-free re-run of CFG763's lower bound (D-ii), as CFG763 used it. It is never in a class-T statistic.
- **DF2/DF4 (class U):** CFG657's GAL dict, read from the text of cfg657_capture.py. It holds CFG655's frozen table (M*,
  R_e, D = 20 Mpc, σ_obs +up/−lo) plus the vD+22 positions and stellar ages (8.28 +2.07/−1.41 and 10.68 +1.38/−1.51 Gyr).
  The R4 secondary dispersions come from cfg933.py's SEC dict (text).
- **Hosts:**
  - TDG hosts: M_host = 0.6 L_K (Lelli's convention, as in CFG7/CFG441/CFG763), at D_p.
  - NGC 1052 and NGC 1035: CFG657's HOSTS positions and its PRIMARY / BRACKET masses (Mg 1e11 [5e10, 3e11]; M35 5e9
    [3e9, 1e10]).

## 3. Estimators (both footings, exact values; kernel ν_e(y) = 1/(1 − e^{−√y}))

### 3.1 Class T (CFG931's INFO path; this is the "same estimator" S1 names)

- **Quantities at R_out:** g_obs = V_circ²/R_out; g_bar = G M_bar/R_out² (spherical, all tabulated baryons, gas counted).
- **Residual:** Δ = log10(g_obs/g_law), with g_law = g_bar ν_e(g_bar/a0).
- **Constants:** G 6.674e-11, M☉ 1.989e30, kpc 3.0857e19 (CFG931's).
- **Route prediction:**
  - ν_eff = 1 + f (ν − 1), where f is the route's filled fraction of the law's cold mass inside R_out;
  - Δ_pred = log10(ν_eff/ν);
  - residual r_i = Δ_obs,i − Δ_pred,i, which equals log10(g_obs/g_route).
- **Per-object error σ_i:** the quadrature sum of the V_circ, M_bar and R_out contributions to r_i.
  - Each contribution is a one-sided numerical derivative with a 1% step (CFG441/CFG763's pred_err form), taken in log space.
  - It is propagated through both g_obs and the route's g_pred.
  - The velocity-only σ = 2 eV/(V ln 10) (CFG931's sDelta) is a variant.

### 3.2 Class U (CFG933's sealed estimator)

- **Quantities:** r12 = (4/3) R_e; M_b = M*/2 (gas-free); g_bar = G M_b/r12²; ν = ν_e; σ_law = sqrt(r12 g_bar ν/3).
- **Observed:** E_obs = 2 ln(σ_obs/σ_law).
- **Route prediction:** E_pred = ln(ν_eff/ν), so σ_pred = σ_law e^{E_pred/2}.
- **Error and z:**
  - sE = 2e/σ_obs, where e is the lower error if σ_obs > σ_pred and the upper error otherwise (CFG933's side rule);
  - z_i = (E_obs − E_pred)/sE.
- **Constants:** G 6.674e-11, M☉ 1.989e30, pc 3.0857e16.
- **Variant:** CFG657's zf (ν_mono, with the M* error on σ_pred; CFG655's form).

## 4. Part A: scoring S1

- **Statistic:** the mean Δ over the six TDGs.
- **se:** sd(Δ, ddof 1)/√6, combined in quadrature with a Υ floor. The floor is half the shift of the mean Δ between
  M_star × 2 and M_star × ½ (CFG930 §4 uniform recipe: Υ propagates into M_bar).
- **Also reported:**
  - the measurement-term se, sqrt(Σσ_i²)/6;
  - the median, with 1.2533 rms/√6 (CFG930's class-S form).

  If the class changes under either alternative, it is labelled FRAGILE.
- **Class, per footing:**
  - **S1 FAILS:** mean Δ > +2 se. This is the seal's kill clause, verbatim.
  - **S1 HOLDS:** −2 se ≤ mean Δ ≤ +2 se. The sample sits on the law, as the seal says it must.
  - **NOT DIAGNOSTIC (BELOW THE LAW):** mean Δ < −2 se.
    - The kill clause cannot fire, but the seal's premise (a TDG sample on the law) is not met.
    - H-ELS and the bare law both predict 0, so they share the deficit, and S1 was not written to score it.
    - The README must state plainly that no excess is seen.
- **Variants (reported):** velocity-only σ; the ν_simple kernel (ν = ½[1 + sqrt(1 + 4/y)], the law as written,
  g_N = g²/(g + a0)); M_mol × 0 and × 2. A variant that changes the class marks it FRAGILE.
- **Power line (no class weight):** the uniform-dwarf-excess alternative is CFG919's DW class mean, as reproduced in CFG931's
  K3: +0.856 / +0.765 ln, which is +0.372 / +0.332 dex. The line reports whether 2 se lies below it.

## 5. Part B: the deficit question

- **Class T:** the six TDGs; residuals in dex of g.
- **Class U:** DF2 and DF4; residuals in ln σ².

### 5.1 Class rule (per route, class and footing)

- **Statistics:**
  - r̄ is the mean residual;
  - se = max(sd(r, ddof 1)/√n, sqrt(Σσ_i²)/n) (CFG933's convention);
  - χ² = Σ(r_i/σ_i)², with p from χ²(n). No parameter is fitted in this lane.
  - Per-object z_i = r_i/σ_i.
- **Reference:** the law's own deficit is r̄_law, the mean residual against the bare law (f = 1).
- **EXPLAINS:** at the route's primary reading, |r̄| < 2 se AND p ≥ 0.05.
- **PARTIAL:** not EXPLAINS at primary, but either |r̄| ≤ 0.5 |r̄_law| at primary (the route removes at least half of the
  discrepancy), or EXPLAINS at ≥ 1 declared bracket corner.
- **FAILS:** otherwise.
- **NOT TESTABLE:** the route makes no prediction for the class from on-disk inputs.
- **Robustness qualifier:** FRAGILE if any declared bracket corner or variant gives a different class; ROBUST otherwise. The
  count is reported, and the primary label stands.
- **Route overall (per footing):**
  - EXPLAINS if T and U both EXPLAIN;
  - FAILS if both FAIL;
  - NOT TESTABLE if both are NOT TESTABLE;
  - otherwise PARTIAL, with the per-class labels shown.

### 5.2 Route (i): supply (framework-native)

**Rule.** The cold mass inside the aperture is the smaller of the law's target and the captured free supply:
- f = min(1, M_sup/M_tgt), with M_tgt = (ν − 1) M_b,ap;
- for T, M_b,ap is M_bar inside R_out; for U, it is M*/2 inside r12.

**(i-P) PRIMARY:**
- **T:** S4 of THEORY_CANONICAL 10-14 ("debris born moving through resting cold energy captures none"), which v2 did not
  remove, together with v2's S3 catchment.
  - A TDG's catchment lies inside its host's settled region. That cold energy is tethered to the host's baryons, and only
    expelled shares are free (H-EX).
  - So M_sup = 0 and f = 0: Newtonian.
- **U:** the record's derived capture rule, CFG657 (channels S + F + D), with α_P = 0 (CFG768 Part A, one c_P), at CFG657's
  PRIMARY inputs.
  - f = f_cap from CFG657's capture(), exec'd read-only from its text.
  - S4's f = 0 is the strict limit.

**(i-B) BRACKET corners:**
- **T** (a recent-catchment upper bound: channel F of CFG657 applied to TDG inputs, with everything ambient captured):
  - M_F = ρ_amb (4π/3) R_c³ with P_F = 1;
  - ρ_amb = k V_f²/(4πG R²), V_f = (G M_host a0)^{1/4}, R = R_fac D_p;
  - R_J = R (ν M_bar/(2 M_g,in))^{1/3}, with M_g,in = V_f² R/G;
  - r* = sqrt(G M_bar/a0)/ln(1 + 1/5.364);
  - R_c = min(R_J, r*);
  - S = 0 (S4: tidal material leaves at the parent's rotation speed); D = 0 (α_P = 0).
  - Corners: R_fac {1, 0.5} × M_host factor {½, 1, 2} × k {1, 3}, 12 in all.
- **U:**
  - S4 strict, f = 0;
  - CFG657's capture at α = 0, at each one-at-a-time end of CFG657's BRACKET except α. This is CFG768 Part A's set:
    16 corners.

**(i-C) CONTRASTS (reported, no class weight):**
- (a) own cosmic share kept: M_sup = 5.364 M_b,ap. This is the 10-14 S3 rule that v2 removed.
- (b) the v2 catchment as if the system were an isolated, cosmically assembled galaxy: M_sup = 5.364 N M_b,ap, with
  N = 1/f_ret(M_ta) from CFG804's census. This is the same computation as MUTATE M3.

### 5.3 Route (ii): settling clock (framework-native; CFG763)

**Model.** f(t) = 1 − exp(−t/τ), with τ in CFG763's committed bracket [τ_min,95, 3.47 Gyr]:
- τ_min,95 = 0.72 canonical / 0.83 alt;
- 3.47 is set by SPARC's old discs, f(8 Gyr) ≥ 0.9.

The route is EFE-free.

**PRIMARY:**
- τ = 3.47 Gyr: the slowest clock old discs allow. The lower end was fitted to these same TDGs with the 1-D EFE, so it is
  not an independent prediction for them.
- Nominal ages:
  - T: t = (t_merg/t_orb) × t_orb, as in CFG763;
  - U: the vD+22 stellar ages, 8.28 / 10.68 Gyr, read as the time since the debris formed.

**Bracket corners:**
- **T:**
  - ages −1σ (floored at 0.05 Gyr) and +1σ, at τ = 3.47;
  - nominal ages at τ = τ_min,95 (reported; this end is TDG-calibrated).
- **U:**
  - ages −1σ;
  - CFG768's lenient cap t = min(t − σ_lo, 6 Gyr);
  - τ = τ_min,95 at nominal ages.

**D-ii (diagnostic, reported prominently, no class weight).** CFG763's own F1/F2 re-run EFE-free.
- Same seven objects, same V-space error recipe, same τ grid.
- Ages at −1σ (and nominal).
- Kernel: ν_e at the exact footings; ν_mono is a variant.
- Output: τ_min,95(EFE-free), with the window OPEN iff it is ≤ 3.47 Gyr on both footings.

### 5.4 Route (iii): EFE, a declared contrast and NOT a framework route

**Formula.** FM12 eq. 60 = Lelli+15 eq. 4, with ν_e (= Lelli's ν_1):
- a_i = g_Ni ν((g_Ni + g_Ne)/a0) + g_Ne [ν((g_Ni + g_Ne)/a0) − ν(g_Ne/a0)];
- the route's f-equivalent is ν_eff = a_i/g_Ni.

**Class T:**
- g_Ne = G M_host/D_p², with M_host = 0.6 L_K;
- corners: M_host × ½ and × 2.

**Class U:**
- g_Ne = the scalar sum of the Newtonian fields of NGC 1052 (1e11) and NGC 1035 (5e9), at their projected separations at
  D = 20 Mpc (CFG657 positions). This is the most generous field: projected distance ≤ 3D distance, and the scalar sum ≥ the
  vector sum.
- Corners:
  - CFG657's host-mass ends (5e10 / 3e11; 3e9 / 1e10);
  - NGC 1052 alone at 2 R_proj.

**Also reported:**
- for T, the common host-mass multiplier that sets r̄ = 0;
- for each DF galaxy, the g_Ne/a0 that gives E_EFE = E_obs, set beside the estimate.

Labelled "contrast: what an EFE-based explanation would need". It never enters the framework verdict.

## 6. Controls

**K tests** (`CFG936_MODE=K` → cfg936_K.out, cfg936_results_K.json). Any K failure stops the lane (exit 2).
- **K1. CFG931's TDG INFO.** Per object, lgbar, Δ and sDelta, and the means −0.690 / −0.728, are reproduced through this
  lane's class-T path, reading the tdg/ CSV, to 1e-12 against cfg931_results.json. The two CSVs agree on the shared columns.
- **K2. CFG933's DF2/DF4.**
  - σ_law, E_obs, sE and z (against P2's E_pred, read from cfg933_results.json), per galaxy and footing, to 1e-9.
  - The GAL entries equal CFG933's membership entries (M*, R_e, σ and its errors).
  - z against the bare law is reported.
- **K3. CFG763's clock bracket.** This lane's re-implementation (CFG4_common.nu_mono and CFG4_common.A0, the 1-D EFE at
  nominal host, CFG763's error recipe and grid) reproduces cfg763_results.json, both footings:
  - τ_min,95 at −1σ and nominal ages, to 1e-9, so the grid values are identical;
  - χ²_min, to 1e-9;
  - CFG763's K1 χ² (τ → 0: 34.018 / 40.290; τ → ∞: 1.105), to 1e-3;
  - the upper bound −8/ln 0.1 rounds to 3.47.
- **K4. CFG768.** For DF2/DF4, through CFG657's capture() and zf exec'd read-only, to 1e-9 against cfg768_results.json:
  - f_cap(α = 0) primary, min and max;
  - Part B universal f and Z_at_f.
- **K5. CFG7 C2.** This lane's EFE code reproduces max |dV_ISO| and max |dV_EFE| at a0 = 1.25e-10 over n = 1, 2
  (1.0292483628918347 / 1.416069913474189) to 1e-9.
- **K6. CFG804 census.** N_of(10.5) = 10, from the verbatim slice.
- **K7. Limits** (1e-12):
  - f = 1 gives Δ_pred = 0;
  - f = 0 gives Δ_pred = −log10 ν;
  - the EFE with M_host = 0 gives the bare law.

**MUTATE** (separate outputs, cfg936_MUTATE_<tag>.out / cfg936_results_MUTATE_<tag>.json):
- **M1 `onlaw` (required):** the TDG V_circ is replaced so that g_obs = g_law exactly. S1 must read HOLDS on both footings.
- **M2 `plus04` (tooth):** g_obs = g_law × 10^0.4. S1 must read FAILS on both footings.
- **M3 `fullsupply` (required):** route (i) with M_sup = 5.364 N M_b,ap (N = 1/f_ret, census), for T and U. It must give
  f = 1 and |Δ_pred| < 1e-12 (|E_pred| < 1e-12) for every object, i.e. no deficit.
- **M4 `oldclock` (tooth):** route (ii) with every age set to 13.0 Gyr, at τ = 3.47. It must give |Δ_pred| < 0.02 dex for T
  and |E_pred| < 0.05 for U: an old system cannot sit below the law on the clock.

**Exit codes:** 0 = OK; 1 = a required or tooth MUTATE control failed; 2 = a K failure.

## 7. Plain-statement rule (README)

- **No framework-native route EXPLAINS a class:** the README says plainly that the framework cannot put that class below its
  law without an EFE. It says the data then contradict the "real assembled mass, no EFE" picture for that class, unless a
  label or input is wrong.
- **Route (i) EXPLAINS only through a zero-supply rule (S4 / FG001):** the README says so. The framework's only way below
  the law is then to deny a system its cold energy. That makes the prediction binary (the law, or Newton), set by a
  formation label and not derived from the system's observables.
- **On calibration:** the README states which of these objects were already in the calibration or motivation set of each
  rule (CFG7/FG001, CFG441, CFG655/657, CFG763), so that none of it is read as an out-of-sample confirmation.

## 8. Compute, outputs, amendments

- **Script:** a single cfg936.py, with CFG936_MODE = K | MUTATE_onlaw | MUTATE_plus04 | MUTATE_fullsupply | MUTATE_oldclock |
  MAIN (the default). Main outputs are cfg936.out and cfg936_results.json.
- **Compute:**
  - one core (OMP_NUM_THREADS=1, nice -n 10), each process < 1 GB, one process at a time, seconds each;
  - nothing downloaded;
  - committed code is exec'd read-only, with writes refused;
  - no other lane's file is edited.
- **Amendments:** any change after this commit is a dated, labelled AMENDMENT_A<n>.md. It states whether it was made before
  or after the K, MUTATE or main run. No class rule changes after a main-run number is seen.

κ = ½ is FITTED. The footings are never pooled. The extra mass is cold energy; no dark-matter species. Not "theory closed".

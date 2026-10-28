# HO2_sluggs_milkyway_heldout — FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-27. One held-out test of the frozen combined picture ("CL2 picture") on two data sets the calibrating
lanes (X43, X48, X62, CF1/CF2, CL1, CL2) never graded: the four SLUGGS centrals of GR1 and the Milky Way lines of GD1 /
GD2. Standing rules: κ = ½ FITTED. Footings never pooled; canonical (a₀ = 9.3603e-11 m/s²) is primary, alt
(1.1312e-10 m/s²) gets its own verdict. Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a
particle; ΛCDM appears only as the rival. Not "theory closed". Nothing here may say the data favour the framework.
No downloads. Passing is evidence; failing is information.

## 0. Held out, and what is not blind

- **Held out:** neither the SLUGGS centrals nor any Milky Way line entered X43 / X48 / X62 / CL1 / CL2. GR1 and GD1/GD2
  graded the OS1 core law (Σ ∝ σ^q), not the CL2 picture.
- **Not blind (disclosed):** the record already prints, for the same data,
  - SLUGGS: route-E X38 halos (q = 0) at mean +0.197 / +0.182 dex; OS1 at +0.127; the law (CFG528b row M K0, ν_mono)
    at +0.181 / +0.171.
  - MW: the v3 (AQUAL) sealed V_c(R₀) 215.5 / 220.6 km/s and K_z(R₀) 92.3 / 96.8 M☉ pc⁻² on McMillan 2017; X5's law
    cells need a short disc and miss Bovy & Rix's summary K_z by +4.7σ to +6.6σ.
  The rules below are GR1's and GD2's own, not tuned; but the writer knew these numbers. A reader should weight the
  verdict accordingly. **Expected (written now):** the MW sits below the switch (GD1: lgM200 11.93), so it takes the
  law branch; the algebraic law on McMillan baryons is expected near v3's V_c and with K_z well above 66.4, i.e. a
  likely MW fail on L2b. The SLUGGS outcome is not predictable from the record: the η-floor raises Σ above Σ_a₀ for
  M200 ≳ 10^12.1 (canonical), which acts in the direction GR1 found helpful.

## 1. The frozen CL2 picture (implemented exactly)

- **Switch.** A system carries a route-E cold dark energy halo iff it is a satellite OR its M200 > 10^12.3 M☉, where
  M200 = 10^(a + b(log M_b − 10)) from EM1's R1 relation (A_c2b_refit: a 11.18, b 0.9; graded) on the system's own
  baryon mass (as X62's X43 copy: `M > 10**12.3`). Strict `>`.
  - **Below:** the galaxy law on baryons only, g = g_N ν(|g_N|/a₀), ν(y) = ½ + √(¼ + 1/y), no halo.
  - **Above:** route E = Newtonian baryons + halo, no law boost (X62's LF_G / LF_M).
- **Halo.** Burkert, ρ₀ r₀ = Σ, normalised as X38 / X43 / GR1: total mass M200 inside R200 (200 ρ_c at background A's
  h), r₀ from X38's A1 compact root; a saturated halo (M200 above the Burkert maximum) sits at the peak r₀ and is
  counted. Σ = max(a₀/(2πG), η(M200) Σ_coll(M200)), η(M) = (4/(3 B(1))) c_f(M)^{5/4}, B(1) = 3 ln 2 − π/2,
  Σ_coll = X43's Lacey–Cole half-mass collapse surface density on the record's CLASS background (X43's `sigma_coll`,
  same tag as the M200 relation). c_f(M) = 4 · c_nat(M)/c_nat(10^14), c_nat = 11.63 / 8.22 / 7.31 at log M 12 / 13 / 14
  (X48 `x48_analyze_results_ng48_A2.json` `cf_by_mass`, read at run time), linear in log M, clamped outside 12–14 (CL2's
  `cf_table("S9", 4.0)` with `np.interp`). This is CL2's S9, L = 4, T = 12.3 point.
- **Footings:** canonical 9.3603e-11, alt 1.1312e-10 m/s², each with its own Σ_a₀ and its own law; never pooled.

## 2. Branch of each system (rule fixed now; the numbers are printed by the script)

- **SLUGGS (GR1's four).** The record's own classification (CFG331 / CFG528 / GR1):
  - M87 (NGC 4486) and NGC 5846 are **host centres** (Virgo; the NGC 5846 group). Their branch is decided by the group
    mass. The record carries the hosts only as R500 = 700 / 380 kpc (CFG528's template, PROVISIONAL). The script prints
    M500 = 500 ρ_c (4π/3) R500³ at background A; the branch is "above" if that exceeds 10^12.3 OR the galaxy's own
    M200(M★) does.
  - NGC 4365 and NGC 4374 are **accreted systems** (CFG331: "accreted systems, so they get their own baryons only"),
    i.e. satellites under the switch → route E.
  - Each galaxy's own M200(M★) is printed beside its branch. The halo, as in GR1's isolated reading, is the galaxy's own
    M200(M★) Burkert with the CL2 Σ; host halos stay omitted (disclosed, as GR1).
- **Milky Way:** not a satellite. Its branch is set per baryon model by its own M200 (EM1 R1, bg A, on the model's total
  baryon mass on the solver grid, as GD2). Every model below 10^12.3 takes the law branch; any above takes route E with
  the CL2 halo. The count per branch is printed.

## 3. Graded sub-tests and pass rules (per footing; canonical primary)

### 3a. SLUGGS centrals (GR1 §1b, executed read-only)

- Machinery: GR1's script head (SC1/X38/EM1/X30 namespaces, CFG528b's Jeans solver `sig_multi`, measured GC density
  profiles and anisotropy, row M) executed read-only as a text copy; CFG466 errors; CFG528's `score`.
- Route-E field: g(r) = G [M★ r²/(r + a_h)² + M_h(r)]/r², M_h(r) = π Σ r₀² B(min(r, R200)/r₀) with Σ the CL2 Σ of the
  galaxy's own M200(M★). **M★ = GR1's route-E JAM analogue**: 0.5 M★ + M_h(< r₁₂; M★) = 0.5 M_JAM, Brent in log M★ on
  [M_JAM·10⁻³, M_JAM]; no root → not computable (counted).
- If a galaxy were on the law branch (none is expected under §2), its field would be the law on the JAM-analogue stars
  (0.5 M★ ν(G 0.5 M★/r₁₂²/a₀) = 0.5 M_JAM), with this lane's ν.
- **Class (GR1's rules):** PASS = CFG528's `closes` (≥ 3 of 4 with Z < 2, none Z < −2, all computable). IMPROVES ON
  X38 = not PASS, |mean| ≤ 0.5 × |mean of X38 q = 0 on the same machinery| (GR1's −50 % bar), none reversed.
  FAILS = otherwise.

### 3b. Milky Way (GD2's four lines on X5's 175-cell box, plus GD1's McMillan 2017 point)

- Baryons: GD2's Newtonian path (P4 `mw_grid`, `rho_axisym` nq 4, `Problem.solve_newton`), X5's frozen family / grid /
  tags, unchanged. GD1's baryon model (McMillan 2017) is graded on the same path (`rho_mcm`; GD2's K0 shows it equals
  GD1/S3's field to 0.1 %).
- **Law branch on this path:** at each cell centre the Newtonian field (g_R, g_z) is multiplied by ν(|g_N|/a₀); V_c and
  K_z are then read exactly as P4's `mw_obs` / X5's `vc_plane` read them (same interpolation, same unit conversion).
  This is the algebraic (pointwise) law, as the CL2 harness applies it; it is not an AQUAL/QUMOND field solution
  (disclosed; no curl-field correction).
- **Route-E branch:** GD2's `grade` with Σ replaced by the CL2 Σ.
- **Lines (GD2's, frozen 78f30f7368):** L1 |v_c − 229.1| ≤ 9.2 AND |v_c − v_E| ≤ 2e_E (X5 `eilers_target`); L2a χ²_Kz ≤
  67.459 (43 MAPs, BR_E5); L2b |K_z(R₀, 1.1) − 66.4| ≤ 4.4; L3 χ²_Ou ≤ 59.893 (37 points, S3 error model). Distance D as
  GD2.
- **Class per footing (GD2's, bg A graded; bg B reported):** FEASIBLE IN PRIORS / FEASIBLE (WIDE PRIORS ONLY) / V+K ONLY
  / INFEASIBLE, first match wins. GD2's PRIMARY/VARIANT V_last split does not exist here (Σ has no σ); one row per
  footing.
- **GD1 point (McMillan 2017):** each of L1, L2a, L2b, L3 reported PASS/FAIL, with z vs Eilers 229.05 ± 4.65 and vs
  Bovy & Rix 66.4 ± 2.2 (GD1's reported z's). Graded as "McMillan passes all four" yes/no; it does not change the class.

### 3c. Lane verdict (per footing)

| verdict | rule |
|---|---|
| HO2 PASSES BOTH | SLUGGS PASS and MW FEASIBLE IN PRIORS |
| HO2 PASSES BOTH (MW WIDE PRIORS ONLY) | SLUGGS PASS and MW FEASIBLE (WIDE PRIORS ONLY) |
| HO2 SLUGGS ONLY | SLUGGS PASS, MW V+K ONLY or INFEASIBLE |
| HO2 MW ONLY | SLUGGS not PASS, MW FEASIBLE (either) |
| HO2 FAILS BOTH | SLUGGS not PASS (IMPROVES counted as not PASS, named) and MW V+K ONLY or INFEASIBLE |

Canonical is the headline; alt printed beside it; if they disagree the lane says SPLIT with both.

## 4. Step 0 (stop rule): the harness must reproduce the source lanes under their original settings

If any S0 check fails in the normal run, the script prints STOPPED AT STEP 0, writes no verdict and exits 1.
- **S0-GR1:** GR1's head executed read-only; K0c (CFG528b row M K0 to 1e-6 dex); SLUGGS at q = 0 and at q_f
  (OS1 halos, GR1's own halo function) equal GR1's committed per-galaxy offsets and class means to 1e-6 dex on both
  footings; groups at q = 0 equal GR1's committed mean (1e-6) and Z (1e-4).
- **S0-GD2:** GD2's script executed read-only as a text copy (outputs suppressed); every class and every line count in
  `classes` equals the committed `gd2_x5_box_results.json`; the best-cell v_c equals it to 1e-6.
- **S0-GD1:** GD1's script executed read-only (outputs suppressed) in its plain, `--os1 172.98` and `--os1 229.05`
  modes; headline V8 and K_z (s = 1, bg A, both footings) equal the committed JSONs to 1e-6.
- **S0-CL2 (the picture is implemented right):** with this lane's Σ_CL2 and switch, P4 T3's group estimator (GR1's copy)
  on the 63 Tian+2026 groups reproduces CL2's committed S9 / L 4 / T 12.3 groups mean (1e-4), Z (1e-3) and the
  above-switch count n_active on both footings (`CL2_native_cf_slope/x62_x43copy_on_shpS9_L4_T12.3_B_results.json`).

## 5. Checks

- **K1 Σ table:** Σ_coll(10^12, bg A) = 6.8 ± 0.06 M☉ pc⁻² (X41/X43); c_f table at L 4 = 6.37 / 4.50 / 4.00 (±0.01);
  the log-M interpolation table for Σ_coll agrees with direct `sigma_coll` at five test masses to 1e-4 relative.
- **K2 switch property:** every graded system takes exactly the branch its flag selects (counted, 0 violations).
- **K3 law-path identity:** with ν ≡ 1 the MW law path reproduces GD2's Newtonian `newton()` observables (V_c(R₀), K
  at the 43 MAPs, K_z(R₀), Ou curve) for McMillan to 1e-9 relative.
- **K4 SLUGGS root:** JAM-analogue residual < 1e-8.
- **K5 resources:** peak RSS < 1 GB per process, one thread.
- **Rerun-identical:** a second normal run produces a byte-identical results JSON (checked after the run, reported in
  README).
- **MUTATE twin (`HO2_MUTATE=1`, outputs `*_MUTATE`):** the switch flag is inverted (every system takes the other
  branch) and the S0-CL2 targets are multiplied by 1.01. The twin must FAIL **S0-CL2** and **K2**; it runs past Step 0
  (stop rule disabled in the twin) and exits 1 when these fail, as designed.

## 6. Reported only (no class weight)

- SLUGGS: the 'bar' reading (CFG528's extrapolated hot gas added to the field and to M_b, as GR1); the law branch for
  all four (what an isolated-central-below-switch reading would give); each galaxy's M★/M_JAM, lgM200, Σ/Σ_a₀,
  saturation.
- MW: bg B class; best cell, max-v_c cell, short-disc best v_c (GD2's `classify` fields); the McMillan point's V_c(20 kpc)
  and dlnV/dlnR 15–27.5 on the law branch.

Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ho2_heldout.py` (twin: `HO2_MUTATE=1`). Amendments only
in `AMENDMENTS.md`, each committed before the run it affects.

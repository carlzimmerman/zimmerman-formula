# CFG324: candidate B's large-scale growth, derived from B's declared rule and scored on raw data. FROZEN CRITERIA

Lane CFG324. Written and committed before any lane script exists. Verdict words per reading: PASS, FAIL, NOT DETERMINED.
Standing rules: κ = ½ is FITTED and fixed; both footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt); the kernel
is ν_mono (user decision 09-26); no knob scans and no fits of theory constants; no downloads. Candidate B keeps its cold
component (Ω_c h² = 0.1200, FITTED like ΛCDM's): the mass is still required and it is not a particle species. Nothing here
says the theory is closed or that the data favour the framework.

## 0. Why, and the not-blind statement

AUDIT_SIGMA8 (`campaign_fresh_gravity/AUDIT_SIGMA8_2026-10-03/README.md`, dd14eb3d3) found the bare chassis fails structure
growth (all matter feels ν_mono: about ×7 in amplitude by z ≈ 6, excluded by CMB lensing) and that candidate B's growth
was never computed: gate 3.03 is "met by allowance" (`closure_map/GATES.md` row 3.03; `CFG4_cosmology.py` takes the ΛCDM
P(k) as given). CFG4_switch H4 set B(k, z) = 1 on every linear mode by assertion.

Read before freezing (so these numbers are known, not blind): CFG4_README parts 1–5 (T1–T6; the separability table H3;
H4's 1.000 / −0.39σ with the bound-only switch; H6's leak 1.060 linear / 1.528 halofit; part 5's H2 additive reading failing
X-COP by +20–45% and H3's phantom budget Ω_ph(x) table); `closure_map/GATES.md` rows 3.01–3.09; STANDING_2026-09-29;
CFG7_README (FG001); CFG251_FROZEN_CRITERIA T5(c); the audit's README and diagnostics output (σ₈ 23.32 / 27.48, the
growth-ratio history, D6's Local Group field 0.010–0.013 a₀); FP22's ledger lines L22b, L22g, L22j, L22k (reading (b)
1.45–2.2× σ₈ with no separator); hunt h85 (the Local Group β from the same 2M++ cube, 0.33–0.45; it quotes a published
β* = 0.431). No 6dFGS fundamental-plane velocity fit against the 2M++ field exists in the record, and no number from one was
seen. No growth ODE for readings R2 or R3 below has been run.

## 1. Candidate B and the readings the record allows (scored separately, never pooled)

B = CFG4's target T1–T6 + FG001 hierarchical ownership (`closure_map/GATES.md` line 14). The rules that bear on growth:
- **T2** (CFG4_README "The target equations"): inside ON regions g = ν(|g_N,b|/a₀) g_N,b; the law's dark density is
  ρ_eff = ∇·[(ν − 1) g_N,b]/(4πG). The kernel's argument is the BARYONIC Newtonian field.
- **T3 the switch**: ON iff the region lies inside a top-level bound system that has turned around, Δ(<r) ≥ Δ_ta(z),
  with the density edge r_e = x_e r_ta (B declares x_e = 0.4, GATES line 14) and M_b ≥ M_*.
- **T4**: the cold fluid behaves as CDM wherever the law is off.
- **T5**: identity bookkeeping, dark mass = max(M_ph, (Ω_c/Ω_b) M_b), DECLARED (CFG4_target ledger T5).
- **FG001** (CFG7_README): the law acts on a system's own baryons only if the system is top-level.

The record leaves two points open that change growth: the bookkeeping of the bound regions' phantom (CFG4_switch ledger
S5 "OPEN: added → leak; replaced → ΛCDM's lensing"; GATES row 3.02 lists both), and the switch variable (the 09-26 user
decision "switch variable = all doors: each gate variable is its own labelled cell"; MS1: the switch reads baryons, never
the carrier or curvature; CFG4 H3 lists field strength y as a candidate variable and records that it does not separate the
web). So three readings:

| | reading | record citations | what it does to the linear web |
|---|---|---|---|
| **R1** | bound-only switch (T3 on the total enclosed contrast) + identity bookkeeping (T5) + FG001 | CFG4_README T3, T5; GATES 3.02 (primary line), line 14; CFG4_target ledger T5 | unbound linear web OFF; inside bound regions the phantom IS the cold component (mass conserved) |
| **R2** | bound-only switch (T3) + ADDITIVE bookkeeping: the bound regions' phantom adds to the cold component | CFG4_switch H6 and ledger S5; GATES 3.02 ("if the phantom is ADDED in bound regions"); CFG4_target H2 (recorded as failing X-COP; scored here anyway for growth) | unbound web OFF, but a net positive phantom density sits in every turned-around system and sources the web's potential |
| **R3** | field-strength (acceleration) door: ON where the baryonic field y_b = \|g_N,b\|/a₀ exceeds a threshold y_th ≤ 2.1e-5 (the KiDS requirement in CFG4 H3); law T2, phantom sourced by baryons, felt by all matter; no bound system, so no identity | CFG4_README part 2 H3 row "field strength y"; 09-26 "all doors" decision; MS1 (switch reads baryons) | the whole linear web ON (y_b ~ 1e-3 ≫ y_th at all z), boosted by the baryons' share |

R1 is B as declared. R2 and R3 are the cells the record itself names as open or as candidate switch variables. No fourth
reading is added, and no reading is chosen as "the" B by its score.

## 2. Equations per reading (N = ln a; Ω_m(a) = Ω_m a⁻³/E²; GR Friedmann background, unchanged in every reading: GATES 3.04)

- **R1:** D'' + (2 + dlnH/dN) D' = (3/2) Ω_m(a) D. Exactly ΛCDM linear growth on every linear mode (the switch is off where
  Δ(<r) < Δ_ta, and identity conserves the mass inside bound regions). Lensing on the linear base = CLASS ΛCDM. On the
  halofit base = CLASS halofit; the in-halo redistribution of the cold component into the phantom profile at fixed mass is
  not modelled, and its effect is bounded (reported, not load-bearing) by |ΔA| ≤ A_halofit − A_linear.
- **Boundness of the web (all readings, reported):** the Press–Schechter turned-around mass fraction
  f_ta(R, z) = erfc(δ_lin,ta(z)/(√2 σ(R, z))) with the record's δ_lin,ta(z) (CFG4_switch D1) and CLASS σ(R, z), at
  R = 8, 20, 50 h⁻¹Mpc and z = 0, 1, 2. "The large-scale web is unbound" means f_ta(R ≥ 20 h⁻¹ Mpc, z = 0) < 0.05.
- **R2:** δ_ph = b_ph δ_m on linear scales, with the phantom's mean comoving density Ω_ph(z) and b_ph = 1 (a lower bound:
  turned-around mass is biased high).
  D'' + (2 + dlnH/dN) D' = (3/2) Ω_m(a) [1 + Ω_ph(z)/Ω_m] D, and the lensing source is Ω_m δ_m [1 + Ω_ph(z)/Ω_m].
  Ω_ph at z = 0 and z = 0.25 is read from `CFG4_target_results.json` (key `{footing}|nu_mono|z{z}|m7.0`, x = 0.4: B's x_e).
  Linear in z between them. Above z = 0.25 two declared variants, both scored:
  - **R2-est:** Ω_ph(z) = Ω_ph(0.25) · [S(z)/S(0.25)] · [f_ta(1 h⁻¹Mpc, z)/f_ta(1 h⁻¹Mpc, 0.25)], with
    S(z) = [(1 + z)³ (1 + δ_ta(z))/(1 + δ_ta(0))]^(−1/3) (each phantom's mass ∝ its edge radius in deep MOND; the edge
    ∝ r_ta) and the record's k = 1 h/Mpc turned-around share (CFG4_target H3);
  - **R2-min:** Ω_ph(z) = 0 above z = 0.25 (a hard lower bound on the reading).
- **R3:** D'' + (2 + dlnH/dN) D' = (3/2) Ω_m(a) [1 − f_b + f_b ν_mono(y_b)] D, y_b = f_b g_rms(a, D)/a₀, with g_rms the
  audit harness's own field statistic (exec'd from the L341 copy, as in `audit_sigma8_diagnostics.py`), f_b = ω_b/ω_m of
  that harness. The boost is on for z ≤ 100 only (baryons have caught up with the cold component; MOND before z = 100 is
  ignored, which can only make R3 look better). Initial amplitude as the audit (σ₈ = 0.811 ΛCDM anchor scaled back).
- **Scale-independent readings (R2, R3, chassis, MUTATE):** P_X(k, z) = [D_X(z)/D_ΛCDM(z)]² × P(k, z) on both bases
  (on the halofit base this under-counts the nonlinear excess for a boost > 1, so it errs toward passing), and for R2 also
  × [1 + Ω_ph(z)/Ω_m]². C_L^φφ = CLASS C_L^φφ × Limber[P_X]/Limber[P]. Limber: C_L^φφ = 4/(L + ½)⁴ ∫dχ ((χ* − χ)/χ*)²
  [1.5 Ω_m H₀² (1 + z)]² P((L + ½)/χ, z), CLASS spectra at XR26's Planck 2018 parameters.

## 3. Observables and data

1. **CMB lensing:** Planck 2018 MV band powers 8–400 (9 bins) and the amplitude 1.011 ± 0.028, as typed in XR26
   (`real_research/cross_thread_review_2026_09_26/XR26_cmb.py`, PL18_MV / LENS_AMP; exec'd read-only as CFG4_cosmology
   does). Amplitude A = inverse-variance-weighted mean of the band ratios to the CLASS ΛCDM band powers; χ² over 9 bins.
2. **Peculiar velocities:** 6dFGSv fundamental-plane data (`real_research/data/fp_6dfgs_campbell2014.tsv`, J band, the
   8,896 galaxies flagged Js = 1) against the 2M++ density cube (`real_research/data/twompp_density.npy`, 257³, Galactic
   Cartesian, spacing 400/256 h⁻¹Mpc, Local Group at cell 128).
   - Predicted velocity for β = 1: v(k) = i 100 δ(k) k⃗/k² km/s (h⁻¹Mpc units), FFT on the cube zero-padded to 384³;
     radial component u_i at each galaxy's redshift-space position (r = cz/100, CMB frame; group cz where given).
   - Model: log R_e,i (kpc/h, from the catalogue) = a log σ₀ + b log I_e + c + η_i, η_i = −log10(1 − v_i/cz_i),
     v_i = β u_i + V⃗_ext·r̂_i. Ordinary least squares in log R_e (a, b, c, β, V⃗_ext: 7 linear parameters after
     η ≈ v/(cz ln 10)); the exact η is used in a final Gauss–Newton step. Errors: 500-galaxy-resample bootstrap.
   - Estimator bias: 50 mocks that keep every galaxy's (σ₀, I_e, position), draw log R_e from the fitted FP with its
     measured scatter plus η from β_true = the data fit, and re-apply the catalogue's apparent-magnitude limit
     (m_mock = m_obs − 5 Δlog R_e at fixed I_e; limit = the sample's own maximum J_tot) and its σ₀ floor. The mean bias
     is subtracted from β and its spread added in quadrature.
   - σ₈,g of the cube: top-hat 8 h⁻¹Mpc variance of the cube inside r < 100 h⁻¹Mpc (full sky coverage), octant jackknife
     error. Two declared corrections from CLASS ΛCDM spectral shape at z = 0: (i) the cube's 4 h⁻¹Mpc Gaussian
     presmoothing, factor σ(TH8)/σ(TH8 × G4) on halofit P; (ii) nonlinear → linear, factor σ₈,lin/σ₈,halofit. The
     systematic error on σ₈,g is the full size of the two corrections combined.
   - fσ₈,obs = β_corrected × σ₈,g,lin. The prediction per reading is f σ₈(z_eff) of the matter, z_eff = the sample's median
     redshift, from the reading's D(z) (continuity holds in every reading, so v = aHf δ_m/k).
3. **Reported, not load-bearing:** the 8 published RSD fσ₈ points typed in CFG4_cosmology (gate 3.03: Δχ² vs ΛCDM ≤ 4);
   the y_b rms of the web along the history (R3's switch argument).

## 4. Decision thresholds (per reading and per footing; the weaker footing decides)

- **Lensing:** PASS if |A − 1.011| ≤ 2 × 0.028 on BOTH the linear and halofit bases; FAIL if |A − 1.011| > 2 × 0.028 on the
  linear base; NOT DETERMINED if linear passes and halofit fails (FP22 L22k's convention).
- **Velocities:** z_v = (fσ₈,pred − fσ₈,obs)/σ_obs (stat ⊕ bias spread ⊕ σ₈,g systematic). PASS |z_v| ≤ 2; FAIL |z_v| > 3;
  NOT DETERMINED in between.
- **R2:** scored on both variants; if R2-min and R2-est disagree, R2 is NOT DETERMINED on that observable.
- **Reading verdict:** FAIL if either observable FAILs; PASS if both PASS; otherwise NOT DETERMINED.
- **Overall:** "B's growth is TESTED" iff R1 (B as declared) gets PASS or FAIL. The outcome is stated per reading.

Pre-declared expectations (estimates, not targets): R1 lensing PASS (P 0.9), R1 velocities PASS or ND (P 0.7); R2 FAIL on
lensing in R2-est (P 0.7), R2-min UNCERTAIN; R3 FAIL on both (P 0.9).

## 5. Controls

- **C1 ΛCDM:** CLASS at XR26's parameters reproduces XR26's committed ΛCDM lensing χ² = 10.1456 to 1e-3 and lies within 2σ
  of 1.011 ± 0.028. The Limber ratio pipeline agrees with CLASS's C_L^φφ to ≤ 1% averaged over 8–400. The R1 ODE matches
  CLASS's D(z)/D(0) to ≤ 0.5% for z ≤ 5.
- **C2 chassis ("all matter feels ν_mono"):** the audit harness reproduces σ₈ = 23.32 / 27.48 to 1%, and its lensing
  amplitude is > 2σ above Planck on the linear base on both footings (reproduces the audit / FP22 L22j exclusion).
- **C3 velocity pipeline:** the catalogue's log R_e is reproduced from its angular radius and cz (group cz where given) to
  rms ≤ 0.005 dex; the FFT velocity at the origin points within 15° of h85's direct-sum apex; a shuffled-u null gives β
  consistent with 0 within 3σ; the FP scatter lies in 0.07–0.15 dex.
- **C4 R3 premise:** CLASS δ_b/δ_cdm ≥ 0.9 at z = 100 for k = 0.1 h/Mpc.
- **MUTATE (env CFG324_MUTATE=1, outputs suffixed _MUTATE):** R1's growth boosted ×2 in amplitude for z ≤ 10 (P × 4,
  fσ₈ × 2). Its lensing and velocity rows must FAIL (rc = 1).

## 6. Deliverables

`cfg324_growth_lensing.py` (growth per reading, lensing, boundness, RSD; writes `cfg324_growth_lensing.out` and
`_results.json`), `cfg324_velocities.py` (6dFGS × 2M++; reads the first script's fσ₈ predictions), each with check() rows
and an "N/M checks pass" line, MUTATE versions, and a README. Run from the repository root; κ = ½ fixed.

# CFG514 FROZEN CRITERIA: looking out through the Milky Way's cold energy, direction by direction

Written and committed alone, before any script for this lane exists and before any model is compared with any data.
Offline only: data already on disk. Nothing is downloaded; data that would be needed is listed as "needs owner go".
κ = ½ is FITTED. Both footings, a0 = 9.36e-11 (canonical) and 1.13e-10 (alt) m/s². The cold energy's mass is still
required (no particle species is added). Not theory closed.

## 0. The idea and what the record already holds

Idea (owner, 10-08): from Earth we look out through the Milky Way's own cold energy. Directions that pass through more
of the framework's predicted cold energy should be compared with directions that pass through less. Cold energy is
transparent and gravitates only, so every directional signal is gravitational.

In the settled-phantom working model (WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md) the settled cold energy has the law's
phantom profile, ρ_ph = ∇·[(ν_mono(|g_b|/a0) − 1) g_b] / 4πG, derived from the baryons with no free constant. That is
QUMOND's phantom. Near the disc it is flattened (a "phantom disc"); a ΛCDM NFW halo is near-spherical. That shape
difference is the directional prediction tested here.

Prior record, read first and not redone:
- Vertical-force front (real_research/reviews/mi_vertical_*, mi_aqual_mcmillan2017_2026.py, mi_aqual_mond_refit_2026.py):
  AQUAL with the α=2 kernel on McMillan 2017 baryons fits Σ_dyn(1.1 kpc) but fails v_c(R0) by ~35 km/s; ν_vert/ν_rad = 1.024.
- Hunt item 34 (hunt_2026/h34_h35_h38_milky_way.py): K_z,1.1(R) vs the 43 Bovy & Rix 2013 MAPs with ν_mono, using the
  ALGEBRAIC estimate K_z = ν(|g_N|) K_z^N (curl term dropped): normalisation 88.0 / 92.7 vs 67.5 measured (+30%),
  scale length 3.98 vs 2.69 ± 0.11 kpc. FAIL. Item 38: Bird+2022 M(<52, 73 kpc) reproduced with nothing fitted. PASS.
- CFG433: Fritz+18 satellites, V_c 231.9 ± 21.4 km/s at 78 kpc vs 170 / 178 predicted, NON-DIAGNOSTIC (power).
- CFG447: an EFE-blind force is excluded by DR3 wide binaries; the material (settled) phantom is the consistent reading.

What is new here: (i) the full QUMOND field in (R, z), so the phantom disc is computed rather than approximated (item 34's
algebraic K_z is replaced by the true field of the computed phantom); (ii) the zero-knob edge; (iii) a side-by-side NFW
fitted to the same rotation curve; (iv) every observable ordered by direction, with a spherical-phantom MUTATE.

CFG513 (Milky Way cold-energy profile vs NFW) runs in parallel and owns the bias catalogue. This lane does not build one;
it reads CFG513's files if present when the README is written and cites them.

## 1. Models (all declared now)

Baryons: McMillan 2017 (MNRAS 465, 76) Table 3 best fit, exactly as implemented in mi_aqual_mcmillan2017_2026.py
(thin + thick exponential discs, flattened bulge, HI and H2 sech² discs). M_b = the grid-integrated total of that model.
R0 = 8.122 kpc (Eilers+19's adopted value); the Sun at z = 0. Solar motion (11.1, 245.6, 7.3) km/s in (U, V, W)
with V including rotation (declared; only O4 uses it).

- **F0 (zero-knob framework):** QUMOND with ν_mono(y) = 1/(1 − exp(−√y)), baryon amplitude A = 1. Two linear solves on an
  axisymmetric finite-volume (R, z) grid: ∇²Φ_N = 4πGρ_b, then ρ_ph = ∇·[(ν−1) g_N]/4πG, then ∇²Φ = 4πG(ρ_b + ρ_ph).
- **F0e (zero-knob edge):** F0 with ρ_ph set to 0 at spherical radius r > r_edge = r_M / ln(1/(1 − f_b)),
  r_M = √(G M_b/a0), f_b = 0.157134 (the record's value, CFG462/CFG423).
- **FA / FAe:** as F0 / F0e with one baryon amplitude A (all components scaled) fitted to the rotation curve. This gives
  the framework one fitted constant; the NFW gets two. FA is the robustness check, F0 the prediction.
- **N (ΛCDM rival):** the same baryons (A = 1) plus a spherical NFW halo, (M200, c) fitted to the same rotation curve.
- **MUTATE (spherical phantom):** ρ_ph replaced by its angle average ⟨ρ_ph⟩(r) on spherical shells (the enclosed phantom
  mass profile kept), every observable recomputed, outputs written separately (_MUTATE). Applied to F0, F0e, FA, FAe.

Rotation curve for every fit: Eilers+2019 Table 1 (real_research/data/mw_rc_eilers2019_table1.tsv), 38 points,
σ_i = ½(σ− + σ+) ⊕ 0.02 v_c (a declared 2% systematic). χ² and best-fit values are reported for every model.

Numerical controls (all must pass; a failure is reported and the lane stops at that point):
- **K1** Newtonian Plummer sphere (M = 1e11 Msun, b = 3 kpc) on the grid: |g| within 1% of analytic for r = 1–100 kpc.
- **K2** QUMOND Plummer: |g| within 2% of the exact spherical ν(g_N) g_N for r = 1–100 kpc.
- **K3** McMillan baryons: grid mass within 2% of the analytic total; Newtonian Σ(|z| < 1.1 kpc, R0) from the solver
  within 3% of the direct column integral.
- **K4** F0 midplane v_c at 40–60 kpc within 3% of the spherical estimate ν(GM_b/r²/a0) GM_b/r².
- **K5** MUTATE: enclosed phantom mass M_ph(<r) of the sphericalised density equals F0's within 0.5% at 5–100 kpc.
- **K6** NFW fit converges (finite Hessian), parameters reported.

## 2. Observables, data, statistics and verdict rules (declared before any comparison)

Verdict words per observable: **FAVOURS FRAMEWORK / FAVOURS NFW / NOT DIAGNOSTIC.** A FAVOURS verdict needs the same
sign on BOTH footings AND in BOTH F0 and FA; otherwise NOT DIAGNOSTIC. Observables with no on-disk data are
PREDICTION ONLY and get NOT DIAGNOSTIC (data needed is listed).

**O1. K_z,1.1(R) — the radial run of the vertical force at |z| = 1.1 kpc (ON DISK).** Data: Bovy & Rix 2013 Table 3,
43 MAPs (real_research/data/mw_kz11_bovyrix2013_table3.tsv, the arXiv ancillary file). They assume R0 = 8 kpc; the model is
evaluated at R = R_tab + (8.122 − 8.0) (fixed R0 − R). Model: K_z(R, 1.1 kpc)/(2πG) from the solved field.
- Statistic 1 (primary): χ² over the 43 MAPs with σ_i ⊕ 5% of the measured value (declared systematic; McMillan's
  independent 73.9 vs the 67.5 refit is a 10% spread). Stat-only χ² reported too.
  Δχ² = χ²_F − χ²_N. FAVOURS FRAMEWORK if Δχ² ≤ −4; FAVOURS NFW if Δχ² ≥ +4; else NOT DIAGNOSTIC.
- Statistic 2 (shape, informational): the exponential K0 exp(−(R − R0)/h) refit to model and data with the same weights;
  h and K0 reported with their distance from the data's values in units of the data fit's errors.

**O2. K_z(z) at R0 for z = 0.25–4 kpc (PREDICTION ONLY).** Reported: K_z^F/K_z^N per z, and the phantom-disc
signature S = K_z(1.1)/K_z(4.0). No tabulated K_z(z) on disk → NOT DIAGNOSTIC. DR4 forecast with an ASSUMED 3% error per
z-bin (declared, not sourced).

**O3. Halo potential flattening q_Φ(r) (PREDICTION ONLY).** q_Φ(r) = z-intercept / R-intercept of the equipotential through
(R = r, z = 0), at r = 10, 20, 30, 50, 100 kpc, for the total potential and for the dark-component potential alone; the
dark-density axis ratio q_ρ at the same radii (second-moment of ρ_dark on the shell). Stream constraints are not on disk
→ NOT DIAGNOSTIC. Forecast with an ASSUMED σ(q_Φ) = 0.05 (declared, not sourced).

**O4. Latitude dependence of halo-star velocity dispersion (ON DISK: DESI DR1 MWS rvtab files under
_external_data/desi_mws/rvtab, downloaded for CFG225 with the owner's go).**
- Sample cuts: RVTAB SUCCESS = 1, RVS_WARN = 0, RR_SPECTYPE = STAR, VRAD_ERR < 10 km/s, 7000 ≤ TEFF ≤ 9500 K,
  2.5 ≤ LOGG ≤ 3.75, FEH < −1.2; dereddened Legacy (g − r)_0 in [−0.25, 0.00] with EBV from the fibermap and coefficients
  3.214 / 2.165 (recalled); M_g from the Deason+2011 BHB polynomial in (g − r)_0 (RECALLED, UNVERIFIED);
  one entry per TARGETID (lowest VRAD_ERR). Galactocentric r in 15–40 kpc (primary), 10–60 kpc (variant).
- Velocities: v_gsr = VRAD projected solar motion removed. Angle: Galactocentric latitude θ = arcsin(|z|/r).
  "plane" = |θ| < 30°, "pole" = |θ| > 50°.
- Statistic: ratio ρ_σ = σ_pole / σ_plane, each σ by maximum likelihood with individual errors, error by 1000 bootstrap.
- Prediction per model: isotropic axisymmetric Jeans σ²(R,z) = (1/n_t) ∫_z^∞ n_t ∂Φ/∂z' dz' with the Bird+22 BHB tracer
  (spherical broken power law, slope −3.5 inside 22 kpc, −4.7 outside); variant: tracer flattened q_t = 0.7 (recalled
  halo-star flattening). Predicted ρ_σ = rms model σ over the actual pole stars / over the actual plane stars.
- **Power gate (applied first):** if |ρ_σ^F − ρ_σ^N| < σ(ρ_σ measured) on both footings → NOT DIAGNOSTIC; the measured
  ratio is still printed as information. If the gate passes: FAVOURS X if |z_Y| − |z_X| ≥ 2 on both footings and both
  F0/FA, where z = (measured − predicted)/σ; else NOT DIAGNOSTIC.

**O5. Satellites by direction (Fritz+18 via CFG433).** No satellite positions are on disk (Table 2 has none) → the split
cannot be run (positions need owner go). Power argument only: predicted V_c(pole)/V_c(plane) at 30–100 kpc, F vs N,
against the half-sample error ≈ √2 × 21.4/231.9. NOT DIAGNOSTIC if the predicted difference is below it.

**O6. Shapiro delay and gravitational redshift by direction (PREDICTION ONLY).** Directions: GC (0°, 0°), anticentre
(180°, 0°), NGP (b = 90°), Baade's window (1.0°, −3.9°), LMC (280.5°, −32.9°, 50 kpc), SMC (302.8°, −44.3°, 62 kpc),
M31 (121.2°, −21.6°). Differential Shapiro delay Δt(n̂, D) − Δt(NGP, D) = −(2/c³) ∫_0^D [Φ(n̂, l) − Φ(NGP, l)] dl for
D = 1, 8, 50 kpc; gravitational redshift (Φ(source) − Φ(Sun))/c in km/s for sources at the LMC, at 20 kpc toward the NGP and
the GC, at 100 kpc toward M31. F − N differences reported. NOT DIAGNOSTIC (no measurement; static delays have no
reference and redshifts are degenerate with unknown systemic velocities; magnitudes quantified).

**O7. Microlensing optical depth (PREDICTION ONLY).** Smooth cold energy (a field) and CDM particles both give
τ_dark = 0, so the dark-component prediction is identical by construction → NOT DIAGNOSTIC. Reported for reference: τ from
the baryons (same in all models) toward Baade's window (source 8.5 kpc), LMC, SMC, M31 (MW part to 300 kpc), and the
hypothetical τ if the dark component were compact, F vs N.

**O8. Lensing of extragalactic sources by the MW's dark component (PREDICTION ONLY).** Effective convergence
κ(n̂) = (4πG/c²) ∫_0^{300 kpc} ρ_dark l dl (source at infinity); all-sky mean, dipole and quadrupole contrast, F vs N.
NOT DIAGNOSTIC (amplitude and unobservable uniform part quantified).

**O9. The dark-column sky map (descriptive; the owner's "more vs less" map).** Σ_dark(l, b) = ∫_0^{100 kpc} ρ_dark dl,
F0 vs N, plotted; plane/pole and GC/anticentre contrasts reported. No verdict.

**O10. Radial (not directional): enclosed mass and the edge (ON DISK).** Bird+2022 Jeans M(<73 kpc) KG = 4.30 ± (0.95 ⊕ 0.60)
and M(<52 kpc) BHB = 4.10 ± (1.20 ⊕ 0.60) e11 Msun (real_research/data/mw_halo_bird2022_jeans.txt). Model M(<r) from the
spherical-average of the field, z per point. FAVOURS X if Σz²_Y − Σz²_X ≥ 4 on both footings; else NOT DIAGNOSTIC. Reported
for F0, F0e, FA, FAe, N. The edge's effect on CFG433's V_c at 78 kpc is reported (CFG433 owns that test).

## 3. Ranking and the DR4 question

For each observable: D_now = |X_F − X_N| / σ_now (on-disk error; "—" if none) and D_DR4 = |X_F − X_N| / σ_DR4 with the
DECLARED, UNSOURCED σ_DR4 assumptions above (O2 3% per bin; O3 0.05; O1 2% per R-bin over 6–12 kpc; O4 from the DR4 RVS
halo-star count scaled as 1/√N with an ASSUMED ×10 sample). The best discriminator is the highest D_DR4 among observables whose
F − N gap the MUTATE shows to be shape-driven.

## 4. MUTATE rule

The spherical-phantom MUTATE must remove any shape-based preference: for every observable with a FAVOURS verdict or with
D_DR4 ≥ 2, the MUTATE's F − N gap must shrink by ≥ 50% or the FAVOURS verdict must disappear. Where it does not, that
preference is labelled "not shape-based" (normalisation-driven) and the directional verdict for it becomes NOT DIAGNOSTIC.
The MUTATE run exits 1 when it detects the shape signal removed (pass) and 0 otherwise, following the record's convention.

## 5. Outputs

cfg514_directional.py (CFG514_MUTATE=1 for the MUTATE), cfg514_directional.out, cfg514_directional_MUTATE.out,
cfg514_results.json, cfg514_results_MUTATE.json, a figure (dark-column sky map F vs N, K_z(z), K_z,1.1(R), q_Φ(r)),
README.md with the direction-test table. Committed locally only, this folder only; nothing pushed.

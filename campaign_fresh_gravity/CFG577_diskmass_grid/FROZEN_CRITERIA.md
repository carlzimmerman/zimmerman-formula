# CFG577 FROZEN CRITERIA — DiskMass σ_z with the grid solver (repeat of CFG576 with its two failures fixed)

(owner chat 10-09, "yes set it up"). Committed alone before any script.

Data: identical to CFG576 (DMS VI/VII TeX tables, copied in CFG576_diskmass_sigz/data/, read from there).
Models: CFG516's definitions by execution, unedited (CFG514 axisymmetric grid, ν_mono, PD = full QUMOND,
RM-φ = round cold mass equal to PD's enclosed phantom). Both footings, never pooled; κ = ½ fitted.
Per galaxy baryons on the grid: stellar disc Υ_K·I_K(R) with an exponential vertical profile of scale h_z (DMS VII);
bulge Hernquist, a = 0.2 kpc, mass B/D × disc light × Υ_K; atomic gas exponential (scale 2 h_R, sech² 0.10 kpc);
molecular gas exponential (scale h_R, sech² 0.05 kpc); I_K from μ0,K with M_sun,K = 3.28 (PROVISIONAL).
Υ_K fitted per galaxy and per model so the model's own in-plane circular speed equals the tanh rotation curve
(DMS VI Table 5, deprojected with i_TF) at the scoring radius; Υ_K ∈ [0.02, 5].
Prediction (replaces CFG576's one-zone factor): line-of-sight-weighted vertical Jeans,
 σ_pred² = 2 ∫_0^∞ z ρ_*(z) K_z(R, z) dz / Σ_*, with each model's full K_z from the grid.
 (For a pure self-gravitating exponential disc this equals 1.5 π G Σ h_z, DMS's k = 1.5; checked as control C3.)
Statistic: r = σ_pred / σ_meas at R = 1.5 h_R (PRIMARY) and 2.2 h_R; median over galaxies, bootstrap 68% (seed 577).
Gates (all frozen):
 G-cal: PD on the alt footing must give median r in [1.15, 1.45] (Angus et al. 2015 ≈ 1.3) — unchanged from CFG576.
 G-Υ (new): for a model to count as CONSISTENT, ≥ 25 of 30 galaxies must be fittable AND its median Υ_K must lie in
  [0.3, 1.0] (K-band stellar-population range, PROVISIONAL band, declared now).
 CONSISTENT iff median r ∈ [0.85, 1.15] AND G-Υ passes.
Verdict per footing: INCONCLUSIVE if G-cal fails; ROUND FAVOURED if RM consistent and PD not; PD FAVOURED if PD
 consistent and RM not; NOT DIAGNOSTIC otherwise. Overall = same call on both footings, else SPLIT.
Controls: C1 grid stellar mass vs analytic disc mass to 2%; C2 Newtonian reference (B = 1 analogue: baryons only)
 reported; C3 the Jeans integral on a pure Newtonian exponential disc reproduces 1.5 π G Σ h_z to 5%.
MUTATE (CFG577_MUTATE=1): a0 × 10 in RM. RM must NOT be consistent (G-Υ included).
Variants (reported): h_z × 0.75; no gas; 2.2 h_R.
Disclosed limits: TF inclinations; DMS σ_z exponential fits (young-tracer bias debated); h_z inferred from h_R;
 isothermal-in-z Jeans closure; assumed gas and bulge shapes; cold energy's mass required; not theory closed.

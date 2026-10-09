# CFG576 FROZEN CRITERIA — DiskMass σ_z: round rule (RM) vs phantom disc (PD)

(owner chat 10-09, "do the DiskMass test"). Committed alone before any scoring script.

Data (from the arXiv TeX sources, never recalled): DMS VI (arXiv:1307.8130) Table 1 (distance, μ0,K, h_R, B/D),
Table 5 (arctan rotation-curve fit), Table 6 (σ_z,0 and dispersion scale length h_σz); DMS VII (arXiv:1308.0336)
Table hR/hz (h_R, h_z in kpc) and the baryonic-mass table (log M_atom, log M_mol). σ_z,meas(R) = σ_z,0 exp(−R/h_σz).
DMS convention kept: exponential vertical profile, k = 1.5, Σ_dyn = σ_z² / (π G k h_z).

Per galaxy, both footings (9.36e-11 / 1.13e-10, never pooled), kernel ν_mono, κ = ½ fitted:
 Baryons: stellar thin exponential disc Υ_K·I_K(R) (I_K from μ0,K, M_sun,K = 3.28, PROVISIONAL), bulge = point mass
 (B/D × disc light × Υ_K), atomic gas exponential with scale 2 h_R, molecular gas exponential with scale h_R
 (shapes ASSUMED, disclosed), masses from DMS VII.
 Υ_K fitted per galaxy so that V_rc(R)² = R ν(g_bar/a0) g_bar at the scoring radius (in-plane law; CFG516: RM and
 PD in-plane fields agree to ≲0.5%). Υ_K ∈ [0.02, 5]; no solution → galaxy dropped and counted.
 Vertical prediction at z = h_z: σ_pred² = π G k h_z Σ_bar · B, with Σ_bar = stars + gas and
  B_PD = ν(|g_N|/a0), |g_N| = sqrt(g_bar² + K_N²), K_N = 2πGΣ_bar(1 − e^{−1});
  B_RM = 1 + K_cold / K_N, K_cold = (g_obs − g_bar)·h_z / R (round cold mass carrying the law's mass).
Statistic: r_M = σ_pred,M / σ_meas at R = 1.5 h_R (PRIMARY) and 2.2 h_R (secondary). Median over galaxies with a
 bootstrap 68% interval (2000 resamples, seed 576).
Calibration gate G-cal: on the alt footing (closest to Angus et al. 2015's a0), PD's primary median r must lie in
 [1.15, 1.45] (Angus+15 report MOND/measured ≈ 1.3). If G-cal fails the approximation is not trusted: INCONCLUSIVE.
A model is CONSISTENT iff its median r ∈ [0.85, 1.15]. Per footing: ROUND FAVOURED if RM consistent and PD not;
 PD FAVOURED if PD consistent and RM not; NOT DIAGNOSTIC otherwise. Overall = same call on both footings, else SPLIT.
Variants (reported, not gates): k = 2 (sech²); h_z × 0.75; no gas; the 2.2 h_R radius.
Controls: C1 ≥ 20 of 30 galaxies give a valid Υ_K on both footings; C2 Newtonian (B = 1, Υ_K from the Newtonian RC)
 reported as the DMS-style reference.
MUTATE (CFG576_MUTATE=1): a0 × 10 in RM; RM must then NOT be consistent.
Disclosed limits: σ_z from the DMS exponential fits (young-tracer bias debated, Aniyan et al.); h_z from the
 h_R–h_z relation, not measured; one-zone vertical approximation (B at z = h_z); assumed gas shapes; κ fitted;
 cold energy's mass required; not theory closed.

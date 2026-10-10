# CFG583 FROZEN CRITERIA — does the law's residual track the baryon MIX (gas, bulge) at fixed baryonic mass?

(owner chat 10-09, "yes run the baryon mix test"). Committed alone before any script.
Motivation: CFG531's KiDS shortfall is in early types (+0.83) not late (−0.31) and grows with M*; CFG580–582 closed
the missing-baryon escapes. Question: does the law's error follow the baryon composition, not just total mass?

Data on disk: SPARC (real_research/data/SPARC_Lelli2016c.mrt + sparc_data/*_rotmod.dat). Cuts: Q ≤ 2, Inc ≥ 30°.
Law: algebraic, ν_mono, both footings (9.36e-11 / 1.13e-10 m/s², never pooled); Υ_disk 0.5, Υ_bul 0.7 (SPARC standard).
 g_bar = (V_gas|V_gas| + Υ_d V_disk² + Υ_b V_bul²)/R; residual per point Δ = log g_obs − log(ν(g_bar/a0) g_bar).
Per galaxy: Δ_out = mean Δ over points with g_bar < a0/3 (the low-acceleration regime nearest KiDS's 50–100 kpc),
 ≥ 3 points required (PRIMARY); Δ_all over all points (variant).
Predictors: log M_b (M_b = 1.33 M_HI + Υ_d L_disk + Υ_b L_bul); f_gas = 1.33 M_HI / M_b; f_bul = Υ_b L_bul /
 (Υ_d L_disk + Υ_b L_bul), with L_bul = 2π∫SB_bul R dR from the rotmod profile and L_disk = L[3.6] − L_bul.
Model: OLS Δ_out = a + b(log M_b − 10) + c f_gas + d f_bul.
Significance: permutation of f_gas (resp. f_bul) among galaxies within log M_b quintiles, 2000 permutations,
 seed 583, two-sided p for c (resp. d).
Expected sign if the KiDS pattern holds in SPARC: c < 0 (gas-poor under-predicted), d > 0 (bulge-rich under-predicted).
Verdict per predictor: RELATION FOUND iff p < 0.005 (0.01 Bonferroni over 2 predictors) on BOTH footings with the
 same sign, AND the sign survives Υ_d = 0.4 and 0.6. Labelled KIDS-CONSISTENT if the sign is the expected one,
 OPPOSITE otherwise. Else NO RELATION. Overall reported per predictor.
Reported: Δ_all variant; Hubble-type T in place of f_bul; KiDS CFG531 class numbers (early/late, M* tertiles) as
 context (no new KiDS statistic); the time question is out of scope (SPARC is z ≈ 0).
Controls: C1 ≥ 100 galaxies pass the cuts with ≥ 3 outer points; C2 |median Δ_out| < 0.1 dex on both footings;
 C3 null calibration: across 200 datasets with Δ_out shuffled within mass quintiles the fraction of p < 0.05 for c is
 0.05 ± 0.035.
MUTATE (CFG583_MUTATE=1): inject Δ_out += −0.20 f_gas; c must be recovered negative with p < 0.005 on both footings.
Disclosed: Υ is fixed (residuals partly absorb Υ errors, which scale with stellar fraction); SPARC is gas-rich discs,
 few bulge-dominated systems; κ fitted; cold energy's mass required; not theory closed.

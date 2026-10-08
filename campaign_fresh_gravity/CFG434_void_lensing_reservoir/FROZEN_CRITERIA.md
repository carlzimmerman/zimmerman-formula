# CFG434 FROZEN CRITERIA: does void lensing allow a smooth unsettled reservoir?

Frozen before any CFG434 script exists. kappa = 1/2 is FITTED. No dark-matter particle; the cold fluid's MASS is still required. This lane uses no a0 value (it tests the reservoir's large-scale contrast only), so the two footings do not enter; nothing is pooled.

## Door (door 8)
WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md, open piece 5: "Unsettled cold fluid must be smooth on scales of 30 Mpc or more, or it adds lensing (CFG363 additive reading)." CFG365: the law uses ~10-35% of each system's cold supply; 65-90% is unsettled. CFG363 (anchored row): even with halo lensing equal to observation, the moved cold mass over-lenses unless it is smooth on >~30-100 Mpc.

Cosmic voids found in BOSS galaxies have radii 34-58 Mpc/h (50-85 Mpc), and their lensing profiles reach 3 R_V. They sit exactly on the scale where piece 5 needs the reservoir smooth. A void's lensing measures the contrast of ALL real mass. A reservoir that is smooth at that scale contributes no contrast.

## Data (fetched, see ../../../_external_data/cfg434_work/FETCH_LOG.md)
UNIONS x BOSS void lensing (arXiv 2507.13450v2, Table "tab:fit_stats"). The authors fit their measured Delta Sigma(R) with the measured BOSS void-galaxy cross-correlation divided by one free bias b_Vg (Delta Sigma_model is linear in 1/b_Vg):
- Full 2.47 +- 0.36 (2975 voids, mean R_V 40.3 Mpc/h, z 0.467): PRIMARY
- LOWZ 2.49 +- 0.49 (z 0.331); CMASS 2.48 +- 0.55 (z 0.530); Small 2.82 +- 0.60 (R_V 33.7, z 0.466); Large 2.77 +- 0.57 (R_V 57.9, z 0.469): robustness rows
- Paper's fiducial cosmology: Omega_m 0.307, h 0.6777, sigma8 0.8225. The void catalogue's reconstruction used beta = f/b = 0.37, "chosen to be the closest match to the fiducial cosmology".
- The paper's own comparison: b_Vg / b_g(Sugiyama+22) = 1.36 +- 0.27.
Disclosed: these numbers were read before this freeze (they were needed to choose the observable). The rule below is fixed before any prediction was computed.

## Observable
A = b_ref / b_Vg = (lensing contrast seen) / (LCDM matter contrast implied by the galaxies). A = 1 means the voids lens exactly as LCDM matter would.
- Likelihood Gaussian in u = 1/b_Vg, sigma_u = sigma_b / b_Vg^2 (the fit is linear in 1/b_Vg). Reported alternative (not decisive): Gaussian in b_Vg.
- PRIMARY reference REF-C: b_ref = f(z)/0.37 with f = Omega_m(z)^0.55, Omega_m = 0.307, at each catalogue's mean z. A 5% uncertainty on b_ref is added in quadrature.
- SECONDARY reference REF-L: b_ref = b_Vg(Full)/1.36 (the paper's Sugiyama ratio), Full only. Sugiyama's bias comes from lensing at R > 12 Mpc/h with sigma8 free. A reservoir smooth at those scales would bias it the same way as the voids, so REF-L tests only scale DEPENDENCE. It is reported and never decisive.

## Predictions (the reservoir's void-scale contrast b_u is a NEW free parameter: 0 = smooth, 1 = traces matter)
Reservoir share of the matter contrast: eps = f_u x (5.364/6.364), with f_u in [0.65, 0.90] (CFG365; cm10's 0.75-0.81 lies inside). So eps is in [0.548, 0.759].
LCDM void-selection systematic (tracer bias inflated in voids: Pollina+17 ~17%, Nadathur+19b up to 25%, as cited by the data paper): R_sel in [1.00, 1.25]. It applies to every model.
- LCDM: A = 1/R_sel.
- Reading I (the record's piece-5 wording; CFG363 anchored row): the clumped matter already carries LCDM contrast, and the reservoir is EXTRA mass on top. A_I = (1 + eps b_u)/R_sel.
- Reading II (conserved cosmic share; the reservoir is PART of Omega_m): A_II = (1 - eps (1 - b_u))/R_sel.
The two readings are never pooled.

## Decision rule (Full, REF-C)
For each reading and for b_u = 0 (SMOOTH) and b_u = 1 (CLUMPY): z = (A_obs - A_pred)/sigma_A, evaluated at all four corners of (eps, R_sel) and over a 21 x 21 grid inside them. The hypothesis is scored at the corner MOST favourable to it (smallest |z|), so a fail is verified as hard as a pass.
- CONSISTENT if min|z| <= 2; DISFAVOURED if 2 < min|z| <= 3; EXCLUDED if min|z| > 3.
- Bound on b_u: the set of b_u in [0, 1] with |z| <= 1.96, at the most lenient and the most stringent corner, per reading.
- Power check (C-POW, required): |A(b_u=1) - A(b_u=0)| = eps/R_sel must be >= 2 sigma_A at the least favourable corner (eps 0.548, R_sel 1.25). If it fails, every verdict is NON-DIAGNOSTIC.
Headline per reading: "SMOOTH RESERVOIR <verdict> under reading I / II". If reading I gives CONSISTENT and reading II gives EXCLUDED (or the reverse), the headline is "BOOKKEEPING FORK" with both rows.

## Robustness (reported, never decisive)
LOWZ, CMASS, Small, Large separately (REF-C); REF-L; Gaussian in b_Vg; R_sel fixed to 1 (no selection systematic). DES Y1 (Fang+2019, arXiv 1909.01386): b_slope around voids is "slightly higher" than the large-scale bias, "consistent at the 2 sigma level". Figure only, so it is used as a direction check, not a number.

## Controls (main run exits 1 if C1-C3 or C-POW fail; failures are kept and reported)
- C1: b_ref(Full) = f(0.467)/0.37 lies in [1.9, 2.1] (an LCDM LRG bias).
- C2: REF-C and REF-L references agree within 15% (both are LCDM-normalised LRG biases).
- C3 limits: eps -> 0 gives A_I = A_II = 1/R_sel; reading II at b_u = 1 equals LCDM exactly (to 1e-12).
- C4 (reported): LCDM itself scored by the same rule (CONSISTENT expected; if not, flagged).

## MUTATE (`--mutate`, writes cfg434_void_MUTATE.out and cfg434_results_MUTATE.json)
A deliberately planted fake measurement: A_obs is replaced by reading II's SMOOTH prediction at the mid corner, A = (1 - 0.654)/1.125, with the real sigma_A. The run MUST then return reading-II SMOOTH = CONSISTENT and reading-I SMOOTH = DISFAVOURED or EXCLUDED. The MUTATE run exits 1 (= detected) only if both flips happen; otherwise it exits 0 and the main verdict is flagged as resting on an unvalidated rule.

## Scope
A one-amplitude test on a published stack. Not a profile-shape test, no covariance re-analysis, no new catalogue cross-correlation. b_ref uses LCDM growth f(z) to turn beta into a bias. A model in which the clumped component grows differently changes b_ref, and that caveat is reported.

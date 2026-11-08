# CMB1 frozen criteria: anatomy of the primary-CMB requirement for a cold component

Frozen and committed alone, before any CMB1 script or graded number. Kappa = 1/2 FITTED; not theory closed. Adopts
nothing. Anatomy lane (cold dark energy; no particle). Footings graded separately, never pooled: canonical a0 9.3603e-11,
alt 1.1312e-10. One thread, < 1 GB, no download. No LCDM prior: flat brackets only, no external prior.

**Lane id.** CMB1 is opened in CLOSURE_REGISTER (e21513a8b2, by Theory completion). There is no CMB1 directory, and no
other CMB1 commit.

**Question.** Which measured feature of the primary CMB says "a component that does not feel photon pressure, about
5.4 x baryons, at z 1100"? Could anything other than such a component produce it?

## Known before this freeze (not blind)

- **F1A numbers (7026dcb48e):**
  - B2 cold PA chi2 3740.16 / 3740.30; baryons-only (MB) 176,655.7 / 170,414.7.
  - DeltaMB +172,915.6 / +166,674.4.
  - R 5.41.
  - MB fits pinned at bracket edges: n_s 1.3, foreground amplitudes 50, calibrations 1.1.
- **Feasibility check of the smooth-matter fluid, at a non-fit cosmology** (h 0.674, omega_b 0.02236, omega_c 0.1209,
  A_s 2.1e-9, n_s 0.965; no likelihood evaluated):
  - CAMB 1.6.6 DarkEnergyFluid with the tabulated w(a) = -rho_L / (rho_L + rho_X a^-3) carries Lambda plus a smooth
    dust X in one fluid.
  - It matches the cold model's H(z) to <= 3e-7 at z 0-1e6, and theta* to 2e-6.
  - With c_s^2 = 1e-6, the fluid reproduces the cold TT to 0.13-1.8 % (largest at L > 2000). With c_s^2 = 1e-4 the
    mismatch is up to 6 %.
  - With c_s^2 = 1, the TT first peak sat at L 165 instead of 221.
- **The PA likelihood has no L < 30 data.** There is no low-L TT or EE; tau is free with a flat bracket.

## Code

- cmb1.py imports f1a.py's own likelihood classes (CamSpec P-ACT cut, ACT DR6 SACC reader), its footing rule and its CAMB
  theory call. It imports nothing from QX3, QX10 or QX15.
- Theory: CAMB 1.6.6, lmax 7000, lpa 1, linear lensing, as in F1A A1.
- Blocks run one after another, not as parallel subagents. Each block loads the likelihood (0.6-0.9 GB), so parallel
  runs would break the < 1 GB rule. This is disclosed.

## Block A: Delta chi2 by multipole range and spectrum (additive)

- **Evaluation point.** Each F1A B2 best fit (cold and MB, per footing), with its stored profiled nuisances. Total Delta
  must reproduce F1A's DeltaMB to 0.1 (KA-1).
- **Additive contribution.** For each likelihood, c_i = r_i (C^-1 r)_i. Sum c_i over the data points of each piece.
  The pieces plus the prior terms sum exactly to the total. Piece Delta = c(MB) - c(cold).
- **Pieces:**
  - Planck: TT (143x143, 217x217, 143x217 together; per cross-spectrum reported) in L 30-500 and 500-1000; TE and EE in
    L 30-500 and 500-600.
  - ACT (by bin L_eff): TT, TE and EE in 600-1000, 1000-2000 and > 2000.
  - Calibration priors, as their own row.
  - L < 30: not in the likelihood; reported as "no data".
- **Reported, not additive:** each piece's own block chi2 r_B^T (C_BB)^-1 r_B.

## Block B: physical features (data vs model, in data sigma)

The same estimator is applied to the data and to each model's predicted data vector, (theory + foreground) / calibration
at that model's nuisances.

**Peak estimator (TT).**
- Planck 143x143. A generalized-least-squares quadratic fit with the 143x143 sub-covariance in each window:
  - P1: L 170-280
  - P2: L 480-600
  - P3: L 760-880
- Height = the vertex value; position = the vertex L.

**Damping estimator.** ACT TT CMB-only bandpowers. R_damp = the mean of the bins with L_eff 2000-3000, divided by the
mean of the bins with L_eff 600-1000 (calibration cancels).

**Features:**
- F_oe = H1 / H2 (odd/even, baryon loading)
- F_32 = H3 / H2 (the third peak, potential driving by a component that does not oscillate)
- F_damp = R_damp (damping tail)
- F_pos1 = L1, and F_sp = (L3 - L1) / 2 (sound-horizon angle, peak spacing)

**Sigma.** 1000 Monte Carlo draws from the data covariance (the 143x143 block, and the ACT TT block), with the
estimator applied to data + draw. Feature distance is z = (F_model - F_data) / sigma_F, reported for cold, MB and the
block C fits. Feature chi2 values are not additive with block A; the RESULT says so.

**Adequacy (reported).** For the cold fit, every |z| <= 3 is expected. A larger |z| is disclosed and does not stop
the lane.

## Block C: equality-only vs baryon-density-only fits (per footing, B2 footing rule)

- **E (equality only):**
  - Baryons plus a smooth matter-like component X: the CAMB fluid above with c_s^2 = 1 and omega_cdm 1e-7. X sets
    z_eq and the expansion like the cold component, but it does not cluster.
  - Free: omega_X in [0, 0.40], omega_b in [0.0215, 0.0230], ln(1e10 A_s), n_s in [0.80, 1.30], tau in [0.01, 0.15].
  - Footing h as in F1A, with omega_X in place of omega_d.
- **B (baryon density only):**
  - Baryons only (omega_cdm 1e-7), with omega_b free in [0.0215, 0.20] and footing h from omega_b.
  - Free: ln(1e10 A_s), n_s, tau, same brackets.
- **Fits:** Nelder-Mead, two starts of 300 evaluations, as in F1A.
- **Statistics:**
  - Delta_E = chi2_E - chi2_cold, and Delta_B = chi2_B - chi2_cold, where chi2_cold is F1A's B2 cold fit for that footing.
  - Recovered fraction f_E = (DeltaMB - Delta_E) / DeltaMB, and f_B likewise.
  - Block A and block B are also reported at the E and B best fits.
- **KA-E (the fluid apparatus):**
  - (i) The background check above, repeated at the cold best fit: H(z) within 1e-5 and theta* within 1e-5.
  - (ii) The apparatus offset O = |chi2_PA(fluid with c_s^2 = 1e-6, omega_X = omega_d) - chi2_cold| at the cold best fit.
  - Delta_E is graded only if Delta_E > 10 O. Otherwise block C reads NO VERDICT for E.

## Labels (per footing; the lane label needs both footings to agree)

**Block C label:**
- **CLUSTERING PINNED:** Delta_E > 25 and Delta_B > 25. Neither the equality epoch alone nor the baryon density alone
  stands in for a component that clusters.
- **EQUALITY SUFFICES:** Delta_E <= 9.
- **BARYONS SUFFICE:** Delta_B <= 9.
- **PARTIAL:** otherwise. f_E and f_B are reported.

**Carrier statement.**
- The block A piece with the largest share of DeltaMB is named.
- The feature with the largest |z| at the MB fit and at the E fit is named.
- If the E fit misses F_32 by |z| > 5 while F_pos1 and F_sp are within 3, the third-peak / potential-driving feature
  is named as the one that requires clustering.

## MUTATE (separate outputs)

- **M1 (swap omega_b and omega_d):**
  - At each cold best fit, swap omega_b and omega_d. Canonical h is unchanged by the swap; alt h is fixed.
  - PASS if |Delta F_oe| > 5 sigma_oe, and the F_32 shift in sigma units differs from the F_oe shift by sign or by a
    factor outside [0.5, 2].
- **M2 (accounting):** the block A pieces plus the prior rows sum to the total Delta within 1e-6 relative.
- **KA-1:** the total Delta reproduces F1A's DeltaMB within 0.1.

If M1, M2 or KA-1 fails, the lane label is NO VERDICT.

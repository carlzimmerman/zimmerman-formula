# CFG502: FROZEN CRITERIA -- the two-halo / environment term for the KiDS isolated-lens stack, from first principles, then an equal-terms re-score

Written 2026-10-08, before any script of this lane exists and before any number of this lane has been computed. Nothing below changes after a result is seen. Any departure goes in the README as a dated, disclosed departure; this file is not edited.

## 0. Why

Every KiDS isolated-lens verdict on the record (CFG352, CFG377, CFG413, CFG486, CFG487, CFG495, CFG498, CFG501) depends on the term that carries the signal beyond each lens's own turnaround radius. With CFG377's free R^-0.8 amplitude, the law to r_ta, the V1 clock taper and CFG413's best pass and the 5.85 r_M edge fails (+60.5 / +70.6). With CFG495's PM two-halo frozen (A_equiv 0.07, corrected -0.02), every model fails (chi2 ~ 158-401 / 15), LCDM included. CFG486 judged the free template's amplitude implausible as a two-halo term. This lane builds that term from first principles for THIS selection, freezes it, validates it on LCDM, then re-scores every model with the same term.

## 1. The selection, as the record documents it (CFG96_stage_stack.py, reproduced exactly, check C5)

- Pool: KiDS-DR4 bright sample, r < 20, 0.1 < z_ANNz2 < 0.5, unmasked, finite LePhare MASS_MED > 7; log M* = MASS_MED + 0.15.
- Lens candidates ("ALL"): pool with log M* < 11 and finite u - r (605k).
- Isolated ("ISO", W = 10): no pool galaxy with log M* > log M*_lens - 1 within 3 Mpc comoving transverse and |chi_phot,lens - chi_phot,neighbour| < W = 10 Mpc (comoving distances from photo-z, H0 = 70, Om = 0.3). This is the 181,477-lens stack P. f30 = the W = 30 subset (57,265).
- Key point to be quantified, not assumed: the window W (10 Mpc) is much narrower than the photo-z scatter of a pair at the same true redshift, so true neighbours (a satellite's own central, a central's own satellites) are vetoed only with probability p_W, and satellites leak into the "isolated" sample.

## 2. The environment model E (frozen; LCDM-equivalent universe; no parameter is fitted to any lensing data)

Total predicted stack for model X: m_X + E, where m_X is the model's own lens profile (everything inside the lens's own r_ta, as the record defines each model) and E is identical for every model.

Per lens of stellar mass M* (log M* of the lens catalogue) at redshift z, at physical projected radius R:

E(R) = H(R) + (1 - f_W) T2h(R; b_c) + f_W [ T_host(R) + T2h(R; b_h) ]

**Cosmology.** Flat, Om = 0.3153, h = 0.6736, Omega_b h^2 = 0.02237, n_s = 0.9649, sigma_8 = 0.8111 (Planck 2018, the record's values plus Planck's n_s, sigma_8). Linear P(k, z): colossus Eisenstein-Hu 1998 (with BAO); xi_lin(r, z) from it.

**Halos.** M200c. Halo mass function Tinker+08 (colossus, 200c); linear bias Tinker+10 (colossus). Concentration Duffy+08 (the record's c(M200c, z)). NFW truncated at r200c for the host term; the record's NFW-to-r_ta for the LCDM own profile (CFG495 lens_model). (U): these are literature relations, recalled / taken from colossus, not fitted here.

**Galaxy-halo connection (HOD).**
- Centrals: Moster+13 mean relation (cfg495_lenslib.moster_ms; masses in the record's units, converted to Msun/h for colossus) with a log-normal scatter of 0.15 dex in log M* at fixed halo mass. P(M | cen, M*) proportional to dn/dlnM x Gauss(log M*; f(M), 0.15).
- Satellites: N_sat(> M*_t | M) = max(M - M_min(M*_t), 0) / (17 M_min(M*_t)), M_min(M*_t) = the record's inverse Moster (cfg495_lenslib.inv_moster), i.e. alpha = 1 and M_1 = 17 M_min (Zehavi-type HOD, (U) recalled). The satellite stellar-mass function in a host is -dN_sat(>M*|M)/dlog M*. P(M | sat, M*) proportional to dn/dlnM x (-dN_sat/dlog M*).
- Parent satellite fraction f_par(M*, z) = n_sat / (n_sat + n_cen), both per dex in M* from the integrals above.

**Photo-z leakage, measured from the data (photometry only; the shear catalogue is not read for this).**
- Close pairs: for every lens candidate (ALL), pool companions with log M*_j > log M*_lens - 1 within R_p < 0.3 Mpc comoving; background from the annulus 4-6 Mpc comoving scaled by area. Histogram of Delta chi_phot (5 Mpc bins, |Delta chi| < 600 Mpc), in lens-z bins 0.10-0.15, ..., 0.45-0.50.
- p_W(z) = (excess pairs with |Delta chi| < W) / (excess pairs with |Delta chi| < 600 Mpc), for W = 10 and 30, interpolated linearly in z. No Gaussian assumption. Reported: the Gaussian-equivalent pair sigma.
- Pool completeness for qualifying neighbours: log M*_lim(z) = the 5th percentile of pool log M* in the slice |z_phot - z| < 0.01.

**Isolation passage (Poisson, true neighbours only; chance projections are common to centrals and satellites at fixed M*, z and cancel in f_W).**
- Threshold M*_t = max(M*_lens / 10, M*_lim(z)).
- Central in halo M: P_c(M) = exp(-p_W N_sat(> M*_t | M)).
- Satellite in host M: P_s(M) = (1 - p_W) exp(-p_W N_sat(> M*_t | M)) (the host's central always qualifies and is always in the pool).
- f_W = f_par <P_s> / (f_par <P_s> + (1 - f_par) <P_c>), with <P_s> averaged over P(M | sat, M*) and <P_c> over P(M | cen, M*). The host distribution used in T_host and b_h is P(M | sat, M*) x P_s(M), renormalised; b_c uses P(M | cen, M*) x P_c(M).
- The veto of correlated neighbours in OTHER halos (two-halo neighbours) is not modelled; its size is quantified in the PM emulation (section 4).

**Terms.**
- T2h(R; b) = b x DeltaSigma[ rho_bar_m(z) xi_lin(r, z) on r > r_ta ], computed with the record's shell projector (cfg100 dsigma) on a physical radial grid r_ta..200 Mpc. r_ta = the LCDM-equivalent turnaround radius of the lens (cfg495_lenslib.lens_model, inverse Moster + Duffy NFW), the same r_ta for every model.
- H(R) = -DeltaSigma[ rho_bar_m(z) on r < r_ta ] (the mean-density hole: every model puts the TOTAL mass inside r_ta, and a uniform background lenses nothing).
- b_c = <b_T10(M)> over the passed-central distribution; b_h = <b_T10(M)> over the passed-satellite host distribution.
- T_host(R) = <DeltaSigma_off(R; M)> over the passed-satellite host distribution: the host's truncated NFW, seen from a satellite whose offset follows the host's projected (truncated) NFW, computed in Fourier space: DeltaSigma_off(R) = M Int k dk / (2 pi) u_h(k) u_s(k) J2(k R) with u the normalised truncated-NFW transform (u_s = u_h).
- Not modelled (stated, the same for every model): tidal stripping of a satellite's own halo (each model's own profile is used for satellites as for centrals); lens photo-z errors in R and Sigma_crit; boost / source-lens association; m-bias (the data have none, as CFG377).

**Stacking.** CFG377's lens groups (0.01 dex in log M_gal x 0.03 in z), group log M* = mean of the members' log M*; E tabulated on a (log M*, z) grid (log M* 8.5-11.0 step 0.05, z 0.10-0.50 step 0.05) at physical R (log grid 0.005-20 Mpc), bilinear in (log M*, z) and log-log in R; evaluated at the group's 6-point node radii R = sqrt(G M_gal / g); pair-weighted with the data's WW (CFG377's pstack). E is computed per W: W = 10 (stack P), W = 30 (f30), W = infinity (p_W = 1 makes no sense; ALL uses f_par and P_c = P_s = 1).

## 3. Data and statistics

- PRIMARY: CFG377's stack P (181,477 lenses, 15 g_bar bins 1e-15..5e-12 m/s^2, 50-patch jackknife, Hartlap (50 - 15 - 2)/49 = 0.6735). chi2 = h r^T C^-1 r. No free parameter in any scored row. p from chi2 with 15 dof.
- NULL N1 (reported, frozen): the f30 stack (CFG96 sums), its own jackknife, E at W = 30, LCDM.
- NULL N2 (reported, frozen): the ALL stack (every lens candidate, no isolation), re-measured with the CFG96 / agentK estimator verbatim (sources z_B > z_l + 0.2, same g_bar bins), 50 patches by the agentK assign_patches on the ALL positions, Hartlap; E with f_par and no isolation; LCDM. The staging pass must reproduce cfg110_perlens.npz WG / WW for the ISO lenses to relative 1e-9 (check C6).
- Reported diagnostics: inner 9 bins (R <= 0.445 Mpc) and outer 6 bins chi2 separately; the residual amplitude of CFG377's R^-0.8 template fitted ON TOP of E (what is still missing, if anything).

## 4. PM cross-check (reported; frozen tolerance)

- S0 (LCDM-equivalent) z = 0 snapshots at 256^3 in 200 Mpc/h: cfg359 S0_FLAT seed 359, cfg411 S0 seeds 360 and 361. The 512^3 S0 (cfg411 N512) is run once only if memory and time allow (reported either way).
- Peaks: local maxima of the CIC density (256 mesh, 3x3x3), M_ta = mass inside the radius where the mean enclosed density reaches Delta_ta rho_bar (the run's JSON Delta_ta), from the particles; keep log M_ta >= 13.3 [Msun/h]. Mass bins 13.3-13.7 and 13.7-14.3.
- DeltaSigma around each peak from all particles projected along z through the full periodic box, comoving annuli 0.5-10 Mpc/h.
- Halo-model prediction for the same peaks at z = 0: Duffy NFW whose mass inside r_ta equals M_ta (as cfg495_lenslib.group_q), plus T2h(b_T10(M200c)) outside r_ta, plus H.
- Tolerance: median PM / model over comoving R in [1.5 r_ta, 8 Mpc/h] within [0.7, 1.3] in each mass bin (all peaks). If it fails, the verdict carries the label "2h NOT CROSS-CHECKED".
- Isolation emulation (reported): each peak's line-of-sight coordinate is displaced by N(0, sigma_chi) (sigma_chi = the measured Gaussian-equivalent single-galaxy sigma at z = 0.25 in Mpc/h, periodic); a peak is PHOTO-ISO if no other peak with M_ta > 0.3 M_ta,lens lies within 2.02 Mpc/h (3 Mpc) projected with |Delta chi_phot| < 6.74 Mpc/h (10 Mpc); TRUE-ISO uses sigma_chi = 0. Reported: DeltaSigma beyond r_ta for PHOTO-ISO / ALL and TRUE-ISO / ALL. (Peaks resolve only group-mass hosts; the 0.3 mass ratio stands in for KiDS's 0.1 in stellar mass. It is an emulation of the mechanism, not of the KiDS sample.)

## 5. Contamination check from photometry (reported; frozen tolerance)

Around ISO lenses: excess pool galaxies MORE massive than the lens within R_p < 0.5 Mpc comoving with 10 < |Delta chi| < 600 Mpc, background from the 4-6 Mpc annulus (same cuts) scaled by area, per lens z bin. Prediction: f_W [ P_proj(<0.5 | M) (1 + N_sat(> M*_lens | M)) ] averaged over the passed-satellite host distribution + (1 - f_W) x (two-halo count n_3D pi R1^2 b_c^2 w_p,lin(R1)), with n_3D of more-massive pool galaxies at the lens z measured from the annulus counts with |Delta chi| < 50 Mpc. Tolerance: measured / predicted within [0.67, 1.5] in the stack-weighted mean; outside it the verdict carries the label "CONTAMINATION NOT CONFIRMED BY COUNTS".

## 6. Validation rule (frozen gate) and verdicts

1. **Gate.** LCDM (CFG495's LCDM own profile: point M_gal + (1 - f_b f_ret) NFW to r_ta, inverse Moster + Duffy) + E must reach **p > 0.01 on the 15 bins of stack P** (chi2 < 30.58). If not: **MODEL STILL INADEQUATE**. The per-model table is then computed and reported for information only, no model verdict and no clash verdict is drawn, and the README says what is missing.
2. If the gate passes, per model and footing (canonical 9.3603e-11, alt 1.1312e-10; never pooled): PASS if p > 0.01, else FAIL.
   - (i) LCDM NFW (footing-free); (ii) the law to r_ta (CFG413 x = 1; cfg100 r_ta_law); (iii) the 5.85 r_M edge (CFG487 edge_only_E1, the growth rule's edge with present baryons); (iv) the CFG487 V1 clock taper to r_ta (= CFG498 V1_cap; cap inert on KiDS); (v) the CFG495 drawdown F_dd (= F_nodd + PROP). Reported, not in the verdict: F_nodd, the law to 0.5 r_ta (CFG413's best).
3. **The edge-vs-lensing clash.** best = the lowest chi2 among (i)-(v) on that footing. **RESOLVED** if chi2(iii) - best <= 4 on both footings; **CONFIRMED** if chi2(iii) - best >= 9 on both footings; otherwise **OPEN**. Labels from sections 4-5 attach to the verdict.

## 7. Controls and MUTATE

- C1: the stack P data vector equals CFG377's committed primary ESD (1e-10 relative).
- C2: the LCDM own vector equals CFG495's committed LCDM vector (1e-6 relative); (ii)-(v) reproduce the record's free-A chi2 (CFG413 x = 1, CFG487 edge_only_E1, CFG498 V1_cap, CFG495 F_dd with the free template) within 0.01.
- C3: T2h without the r_ta exclusion, via the shell projector, equals the Hankel form b rho_bar Int k dk/(2 pi) P_lin(k) J2(k R) within 2% at R = 0.5-5 Mpc.
- C4: DeltaSigma_off at zero offset (u_s = 1) equals the centred truncated-NFW DeltaSigma within 1% at R = 0.05-2 Mpc.
- C5: the isolation rebuild reproduces lr_lenses.npz exactly.
- C6: the ALL staging pass reproduces cfg110_perlens WG / WW for the ISO lenses (1e-9 relative).
- **MUTATE (CFG502_MUTATE=1, outputs *_MUTATE.*):** (M1) E = 0: the law-to-r_ta chi2 must equal CFG413's A = 0 value (241.29 / 180.51) within 0.01 and the edge row must equal CFG487's edge_only_E1 no-2h chi2 within 0.01. (M2) f_W = 0 (no contamination, two-halo kept): the LCDM chi2 on the 6 outer bins must change by more than 4 from the main run. A failed MUTATE is reported as a failed control.

## 8. Wording and limits

kappa = 1/2 is FITTED; a0 flat; footings never pooled. "Cold energy" = the cold clumping component; its mass is still required and no particle species is added. Nothing here says the data favour the framework; never "theory closed". On-disk data only; no download (anything needed beyond disk is listed as "needs owner go"). nice -n 15, <= 4 threads. Large arrays live in ../_external_data/cfg502_work and are not committed.

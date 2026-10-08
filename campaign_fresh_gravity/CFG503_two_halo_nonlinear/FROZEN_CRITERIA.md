# CFG503: FROZEN CRITERIA -- a nonlinear two-halo term, tidal stripping of leaked satellites, and the central SHMR uncertainty, for the KiDS isolated-lens stack; then an equal-terms re-score

Written 2026-10-08, before any script of this lane exists and before any number of this lane has been computed. Nothing below changes after a result is seen. Any departure goes in the README as a dated, disclosed departure; this file is not edited.

## 0. Why

CFG502 (criteria cacadd50d, results 4dac09899) built the environment term E for the KiDS isolated-lens stack from a standard halo model and found that ~17% (stack-weighted) of the "isolated" lenses are leaked satellites (photo-z isolation window 10 Mpc vs ~115 Mpc pair photo-z scatter; confirmed by companion counts, 0.85 of prediction). LCDM + E reached chi2 45.92 / 15 (p 5.5e-5) and failed the p > 0.01 gate. The remaining misfit had two named causes: (a) the 1.0-1.4 Mpc data sit +2.3 / +4.0 sigma above LCDM + E (linear-bias b xi_lin outside r_ta under-predicts the one-halo / two-halo transition); (b) the inner bins sit 1-2.6 sigma below LCDM (satellites' own halos not stripped; one SHMR only). The nulls show the same: f30 chi2 34.1, ALL chi2 172.2 (inner 119.1).

This lane adds three pieces of standard halo-model physics, each a declared literature prescription, fixed here before any re-score, and nothing else. No parameter is fitted to any lensing data.

## 1. What is kept from CFG502 unchanged (copied code, not edited)

Selection, stacks, data vectors, jackknife covariances (50 patches, Hartlap), lens grouping (CFG377), the p_W(z) photo-z leakage measured from close pairs, the isolation passage model, the HOD form (log-normal 0.15 dex central scatter; alpha = 1, M_1 = 17 M_min satellites), Tinker+08 HMF, Tinker+10 bias, Duffy+08 c(M200c), the mean-density hole H inside r_ta, the offset host term T_host, the sharp exclusion at the lens's LCDM-equivalent r_ta, the E-table grids and interpolation, and every model's own profile for CENTRALS. CFG502's staged arrays (`_external_data/cfg502_work/cfg502_stage.npz`) are read, not rebuilt.

E(R) = H(R) + (1 - f) b_c T2h(R) + f [ T_host(R) + b_h T2h(R) ]  (f = f_W for W = 10 / 30; f = f_par for ALL), as CFG502.

## 2. Upgrade 1: nonlinear halo-matter two-halo term (primary)

- T2h(R) = DeltaSigma[ rho_bar_m(z) zeta(r) xi_NL(r, z) on r > r_ta ] per unit bias, with the CFG502 shell projector and grid (r_ta..200 Mpc physical).
- xi_NL from CAMB 1.6.6 nonlinear matter power with halofit_version = "takahashi" (Takahashi+12), Planck 2018: H0 67.36, ombh2 0.02237, omch2 0.1200, mnu 0.06 eV, ns 0.9649, As rescaled so that sigma_8(z = 0) = 0.8111; P(k) to k = 200 h/Mpc, extended beyond by the local log-slope; xi(r) = (1 / 2 pi^2) Int k^2 P(k) j0(k r) dk with a taper exp(-(k / 300 h/Mpc)^2), tabulated at each E-table z.
- zeta(r) = (1 + 1.17 xi_NL)^1.49 / (1 + 0.69 xi_NL)^2.09: the scale-dependent (radial) halo bias of Tinker+05 (eq. B7), as used in the Cacciato / van Uitert / Dvornik galaxy-galaxy-lensing halo models. (U): recalled from the literature, not read from disk.
- The same T2h shape multiplies b_c (centrals) and b_h (leaked satellites' hosts). b_c, b_h are the Tinker+10 linear biases averaged as in CFG502.
- Reported only (not in any verdict): b xi_NL without zeta; b xi_lin from CAMB linear.

## 3. Upgrade 2: tidal stripping of leaked satellites' own halos (primary)

- A leaked satellite sits at 3D distance D from its host's centre, distributed like the host's truncated NFW (the same u_s = u_h assumption as CFG502's T_host), D <= r200c of the host; host masses from CFG502's passed-satellite host distribution for that sample (W = 10, W = 30, ALL).
- The satellite's LCDM-equivalent halo: Duffy NFW with M200c = SHMR^-1(log M*_lens, z) (the same as the central's), extended to its r_ta as in the record.
- Tidal radius: the Jacobi radius for a circular orbit, r_t^3 = m(< r_t) D^3 / [ M_h(< D) (3 - dlnM_h/dlnr |_D) ] (King 1962; Binney & Tremaine section 8.3), m = the satellite's LCDM-equivalent NFW, M_h = the host's NFW. r_t is capped at the satellite's r_ta. (U): recalled.
- The rule applied to EVERY model's own profile, with the same r_t (LCDM-equivalent, footing-free, like r_ta in E): for a leaked satellite, the distributed own mass (everything except the point M_gal) is truncated sharply, M_d(r) -> M_d(min(r, r_t)) (the Mandelbaum+05 / Gillis+13 / Sifon+15 truncated-subhalo form). The stripped mass is not re-added anywhere (the host NFW already holds its full M200c).
- Stacked own vector = (1 - f) own_full + f <own_truncated>, the average over hosts and D (computed exactly as the ESD of the averaged truncated enclosed mass, since DeltaSigma is linear in M(r)). Centrals are not stripped.
- E is not changed by stripping (the hole H and the satellites' T2h keep the CFG502 form; disclosed simplification).

## 4. Upgrade 3: the central SHMR, propagated

- PRIMARY: Moster+13 (the record's; cfg495_lenslib.moster_ms / inv_moster).
- ALTERNATIVE: Behroozi+13 (eqs. 3-4 and their best-fit z-dependent parameters: epsilon0 -1.777, epsilon_a -0.006, epsilon_z 0, epsilon_a2 -0.119; log M10 11.514, M1a -1.793, M1z -0.251; alpha0 -1.412, alpha_a 0.731; delta0 3.508, delta_a 2.608, delta_z -0.043; gamma0 0.316, gamma_a 1.319, gamma_z 0.279; nu = exp(-4 a^2)), (U) recalled. Behroozi's halo mass is Mvir (Bryan-Norman Delta_vir); converted from M200c through the record's Duffy NFW. Masses used as published (no h rescaling), as the record does for Moster+13.
- Everything that depends on the SHMR is recomputed under the alternative: the central HOD weights, M_min of the satellite HOD, f_W / f_par, b_c, b_h, host distribution, r_ta and T2h exclusion, the LCDM own profile (and F_nodd / F_dd, which use the LCDM-equivalent halo), and the stripping r_t. The law-type own profiles do not depend on it except through r_t.
- Propagation: for each sample and each model X, delta_X = stack_X(Behroozi) - stack_X(Moster) (the full model vector, E included). chi2_X = r^T (C_data / h + delta_X delta_X^T)^-1 r, r = data - stack_X(Moster), h = Hartlap. That is one nuisance direction with a unit Gaussian prior along the SHMR difference, declared here, not fitted. Data-only chi2 under each SHMR is reported alongside.

## 5. Validation gates (frozen) and verdicts

All gates use the PRIMARY environment (halofit + zeta, stripping, Moster) and the SHMR-propagated chi2 of section 4.
- **G1 (primary):** LCDM on stack P (181,477 lenses, 15 bins), p > 0.01 (chi2 < 30.58).
- **G2 (null N1, f30, 57,265 lenses, E at W = 30):** LCDM p > 0.01.
- **G3 (null N2, ALL, 605,531 lenses, no isolation, f = f_par):** LCDM p > 0.001 (chi2 < 37.70). Looser than G1 because ALL has 3.3x the lenses, so systematics the halo model leaves out (miscentring, lens photo-z in R and Sigma_crit, source-lens association) weigh more; declared before any number.
- If G1, G2 and G3 all pass: VALID. Per model and footing (canonical 9.3603e-11, alt 1.1312e-10; never pooled): PASS if p > 0.01 on stack P, else FAIL. Models (CFG502's): (i) LCDM NFW; (ii) the law to r_ta; (iii) the 5.85 r_M growth edge (CFG487 edge_only_E1); (iv) the CFG487 V1 clock taper (= CFG498 V1_cap); (v) the CFG495 drawdown F_dd. Reported only: F_nodd, the law to 0.5 r_ta.
- If any gate fails: **MODEL STILL INADEQUATE**. The per-model table is reported for information only; no model verdict and no clash verdict. The README says what physics is still missing. No re-tuning.
- **Clash (edge vs lensing), only if VALID:** best = the lowest chi2 among (i)-(v) on that footing. RESOLVED if chi2(iii) - best <= 4 on both footings; CONFIRMED if chi2(iii) - best >= 9 on both; otherwise OPEN.
- Labels carried: CFG502's companion-count check (0.85, inside tolerance) stands for the Moster HOD; the PM check of CFG502 tested the linear term only, so the verdict carries "nonlinear 2h NOT CROSS-CHECKED BY PM" (256^3 cannot resolve the transition; not re-run).

## 6. Controls

- C1: stack P data = CFG377 primary ESD (1e-10 relative).
- C3n: T2h with xi_NL (zeta = 1), no exclusion, via the shell projector equals rho_bar Int k dk / 2 pi P_NL J2(k R) within 2% at R = 0.5-5 Mpc, z = 0.15 / 0.25 / 0.40.
- C3l (reported, not load-bearing): CAMB linear xi vs colossus EH98 xi at r = 1-20 Mpc.
- C7: the stripping code with r_t beyond r_ta for every satellite returns the unstripped own vectors (1e-9 relative).
- C8 (reported): median r_t / r200c(satellite) and the stack-weighted stripped fraction of the satellites' NFW mass inside 0.5 Mpc.

## 7. MUTATE (CFG503_MUTATE=1; outputs *_MUTATE.*)

- **M0 halofit off (linear, CFG502's colossus EH xi_lin, zeta = 1), stripping off, Moster only, data-only covariance:** must reproduce CFG502's committed stack P chi2 for all seven rows on both footings, and the N1 / N2 LCDM chi2, within 0.01 (load-bearing).
- **MH halofit off only** (CAMB linear xi, zeta = 1; stripping and SHMR propagation on): reported, with its gate numbers.
- **MS stripping off only** (halofit + zeta and SHMR propagation on): the LCDM inner-9 chi2 on stack P must differ from the main run by more than 2, or some inner bin's LCDM model value must move by more than 0.5 sigma (load-bearing "stripping visible").
- A failed MUTATE is reported as a failed control.

## 8. Wording and limits

kappa = 1/2 is FITTED; a0 flat; footings never pooled. "Cold energy" = the cold clumping component; its mass is still required and no particle species is added. Nothing here says the data favour the framework; never "theory closed". On-disk data only; no download. nice -n 15, <= 4 threads. Large arrays in ../_external_data/cfg503_work, not committed.

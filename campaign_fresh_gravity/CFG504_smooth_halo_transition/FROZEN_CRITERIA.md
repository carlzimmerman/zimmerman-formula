# CFG504: FROZEN CRITERIA -- a continuous one-halo / infall / two-halo transition, calibrated on our own LCDM-equivalent PM boxes, in place of the sharp r_ta truncation + sharp exclusion; then the CFG503 gates and the equal-terms re-score

Written 2026-10-08, before any script of this lane exists, before any halo catalogue is built or any profile is fitted, and before any KiDS re-score. Nothing below changes after a result is seen. Any departure goes in the README as a dated, disclosed departure; this file is not edited.

## 0. Why

CFG503 (criteria f56e146a1, results b78648975): with a halofit two-halo term, satellite stripping and the SHMR propagated, LCDM still fails G1 (stack P chi2 34.34 / 15, p 0.003) and G3 (ALL 73.99 / 15); G2 (f30) passes. The misfit sits at 1.04 and 1.38 Mpc (R / r_ta ~ 0.9-1.2, pulls +3.5 / +4.9 sigma). The named cause is the record's convention that every model's own profile stops sharply at r_ta while the mean-density hole stops and the two-halo term starts sharply there. The missing physics is a continuous one-halo-to-two-halo (splashback / infall) transition. This lane calibrates one on our own LCDM-equivalent PM snapshots (local compute, no download), freezes it, and repeats CFG503's validation and re-score with it. Nothing is fitted to lensing data.

## 1. Kept from CFG503 unchanged (code copied into this folder, not edited in place)

Selection, stacks P / f30 / ALL, data vectors, 50-patch jackknife covariances with Hartlap, CFG377 lens grouping, p_W(z), the isolation passage, the HOD, Tinker+08 HMF, Tinker+10 bias, Duffy+08 c(M200c), the offset host term T_host, the leaked-satellite fraction f, the Tinker+05 zeta x CAMB halofit (Takahashi) xi_NL two-halo shape (mode "nlz"), the Jacobi-radius stripping weights of leaked satellites (CFG503's tidal-radius tables, same r_t for every model), the SHMR propagation (Moster+13 primary; Behroozi+13 difference as a rank-one covariance term), the five scored models and two reported ones, both footings (canonical 9.3603e-11, alt 1.1312e-10; never pooled), the gates G1-G3 and the clash rule. CFG503's committed env / own tables in `_external_data/cfg503_work/` are read for the M0 reproduction and the r_t weights.

## 2. The halo catalogue (PM, z = 0)

- Snapshots (LCDM-equivalent S0 controls, z = 0, L = 200 Mpc/h, PM mesh = particle grid):
  - PRIMARY calibration, 512^3 (mesh cell 0.391 Mpc/h, m_p 5.19e9 Msun/h): `cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512` and `cfg424_work/cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360`.
  - Resolution check only, 256^3 (cell 0.781 Mpc/h): `cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360`, `..._seed361`, `cfg359_work/cfg359_S0_FLAT_canonical_N256`.
  - One 512^3 particle load at a time; the script checks that no other 512^3 job is running before each 512^3 load.
- **Finder: spherical overdensity at the turnaround contrast, on particles, seeded by density peaks.**
  - Seeds: local maxima (3x3x3, periodic) of the CIC density of all particles on the run's mesh with rho / rho_bar > 20 (CFG502's seed rule).
  - Centre: the centre of mass of the particles within one mesh cell of the seed, iterated twice (re-centred on the previous CoM).
  - Mass: M_ta = the particle mass inside r_ta, the radius at which the mean enclosed density falls to Delta_ta rho_bar (Delta_ta = the run JSON's z0 value), log-interpolated on 50 radii from 0.5 cell to 12 Mpc/h. M_200m (Delta = 200 rho_bar) is recorded where defined (reported).
  - De-duplication: by descending M_ta, a candidate whose centre lies inside the r_ta of a kept heavier halo is dropped (the catalogue is distinct turnaround-scale halos, i.e. centrals).
  - Kept: log M_ta >= 12.3 [Msun/h].
- **Mass bins** (log M_ta, Msun/h): U1 12.3-12.6, U2 12.6-12.9, U3 12.9-13.2, U4 13.2-13.5, R1 13.5-13.8, R2 13.8-14.1, R3 14.1-14.4, R4 14.4-15.2. At most 1000 halos per bin per run (random subsample, seed 504).
- **Resolution limit (stated, frozen):** a bin is RESOLVED in a run only if its median r_ta >= 5 mesh cells (so 0.5 r_ta >= 2.5 cells). At 512^3 that is r_ta >= 1.95 Mpc/h, i.e. log M_ta >~ 13.5: R1-R4. At 256^3 only the top bin can qualify. Below 2.5 mesh cells the PM force is softened and no profile point is used. The KiDS stack's lenses have LCDM-equivalent log M_ta (Msun/h) median 12.48, 16-84% 12.05-12.94 (from CFG503's r_ta tables; no lensing data used), so the KiDS transition is an EXTRAPOLATION of about 1 dex below the calibrated range.

## 3. The measured profile

- Per halo: particle pair counts in 48 log-spaced spherical shells from 0.15 to 20 Mpc/h (periodic); xi_hm = counts / (n_bar V_shell) - 1. Stack = equal-weight mean over the bin's halos, in comoving r (bins are narrow; the model is averaged over the same halos, below).
- Errors: jackknife over 27 sub-volumes (3x3x3 by halo centre), diagonal only for the fit.
- The stacked xi_hm(r) for every bin and run (U1-R4) is tabulated in the results JSON from 0.15 to 20 Mpc/h: one-halo, infall and two-halo regions together.

## 4. The transition form (declared before fitting) and the calibration

**Form.** Around a halo of turnaround radius r_ta, with x = r / r_ta:

    Delta rho(r) = [ rho_own(r) - rho_bar ] f_t(x) + rho_bar b zeta(r) xi_NL(r) [ 1 - f_t(x) ],
    f_t(x) = [ 1 + (x / x_t)^beta ]^(-gamma / beta),   beta = 4, gamma = 8 (Diemer & Kravtsov 2014 transition term with their recommended beta, gamma for mass-selected stacks; (U) recalled).

rho_own is the halo's own (one-halo) profile CONTINUED beyond r_ta by its own formula; rho_bar b zeta xi_NL is CFG503's two-halo term. With f_t = Theta(1 - x) this is exactly the record's sharp model (own truncated at r_ta, the mean-density hole inside r_ta, the two-halo term outside). x_t is the one calibrated number.

**Model on the PM halos (z = 0).** rho_own = the Duffy NFW (record's LL.nfw, z = 0) whose mass inside r_ta equals the halo's M_ta (as cfg495 group_q), continued beyond r_ta; b = Tinker+10 b(M200c, z = 0) (colossus, PM cosmology: Om 0.3138, h 0.6736, sigma_8 0.811); zeta xi_NL = CFG503's CAMB halofit (Takahashi) xi_NL at z = 0 times Tinker+05 zeta. Shell averages by numerical integration inside each shell. The bin model = mean over 25 M_ta quantiles (2-98%) of the bin's halos.

**Calibration (per resolved bin and run):**
1. A (a nuisance for the box's missing large-scale power, sigma_8 realisation and bias-model error) = weighted least squares of xi_meas = A b zeta xi_NL on shells with 2.5 r_ta,med <= r <= 20 Mpc/h (where f_t ~ 0).
2. With A fixed, x_t = argmin chi2 (diagonal jackknife errors) on shells with max(2.5 cells, 0.25 r_ta,med) <= r <= 2.5 r_ta,med, over a log grid x_t in [0.1, 3] (400 points).
3. sigma(x_t): refit steps 1-2 on each of the 27 leave-one-out stacks (jackknife).
- Reported: step-2 chi2 / dof; a fit with beta, gamma free (grid); the 256^3 fits; the unresolved bins U1-U4 (fit with the 2.5-cell floor; extrapolation check below).
- **PRIMARY x_t for KiDS** = inverse-variance mean of x_t over the resolved (512^3 run, bin) fits. sigma_tot = max(formal error of the mean, standard deviation of the individual fits).
- **Assumption (stated):** the transition is self-similar in x = r / r_ta, independent of mass below the calibrated range and of redshift (z = 0 calibration applied at lens z 0.1-0.5 in units of each lens's r_ta(z)).
- A is NOT carried to KiDS: the KiDS two-halo amplitude stays CFG503's (A = 1).
- Label "TRANSITION FORM POOR FIT ON PM" if the median step-2 chi2 / dof over resolved bins exceeds 3 (does not change the gates).
- Extrapolation check (reported): on U1-U4 at 512^3, chi2 of the primary-x_t model (A from step 1) on the shells allowed by the 2.5-cell floor up to 2.5 r_ta,med; and the free x_t there.

## 5. Mapping onto the KiDS models (fixed here)

All models use the SAME window f_t(r / r_ta), with r_ta = the lens's LCDM-equivalent turnaround radius (CFG503's r_ta_lcdm for the SHMR in use; footing-free), exactly as E already used one LCDM-equivalent r_ta for every model.

- **E (identical for every model):** E(R) = H_s(R) + (1 - f) b_c T_s(R) + f [ T_host(R) + b_h T_s(R) ], with H_s = -DeltaSigma[ rho_bar(z) f_t ] and T_s = DeltaSigma[ rho_bar(z) zeta xi_NL (1 - f_t) ] on r in [5e-3, 200] Mpc (shell projector). T_host, f, b_c, b_h as CFG503.
- **Own profiles:** each model's distributed (non-point) enclosed-mass profile, the record's formula continued beyond the record's r_ta truncation to r_ext = max(8 x_t, 6) r_ta, then windowed: M_w(r) = Int f_t dM. The point mass M_gal is not windowed.
  - LCDM: (1 - f_b f_ret) NFW continued. F_nodd: f_b (1 - f_ret) NFW + cold + M_exc (frozen beyond r_edge, as the record) continued. PROP (drawdown): -q rho_c continued with the record's q. F_dd = F_nodd + PROP.
  - Law to r_ta and the V1 clock taper: the law (and V1's taper) continued beyond the record's r_ta,law.
  - Model-intrinsic boundaries inside are kept: the 5.85 r_M growth edge (law to its r_edge, nothing beyond) and the reported law to 0.5 r_ta,law (nothing beyond). They are then windowed like every other model.
- **Leaked satellites:** CFG503's stripping, M_d(min(r, r_t)), applied to the continued profile, then the same window. Unstripped slot = the continued profile.
- **Reported variants (none changes a verdict):** (a) x_t +- sigma_tot; (b) x_t linearly extrapolated in log M_ta from the resolved 512^3 fits to each lens's LCDM-equivalent M_ta (clipped to [0.1, 3]); (c) A carried (two-halo times the mean resolved A); (d) E-only smoothing (own profiles kept sharp as CFG503, E smooth); (e) framework own profiles windowed in units of their own r_ta,law (LCDM and E unchanged).

## 6. Gates, verdicts, clash (CFG503's, unchanged)

With the PRIMARY transition and SHMR-propagated chi2:
- G1 LCDM stack P p > 0.01 (chi2 < 30.58); G2 LCDM f30 p > 0.01; G3 LCDM ALL p > 0.001 (chi2 < 37.70).
- All pass: VALID; per model and footing PASS if p > 0.01 on stack P. Models (i) LCDM, (ii) law to r_ta, (iii) 5.85 r_M growth edge, (iv) CFG487 V1 clock taper, (v) CFG495 F_dd; reported F_nodd, law to 0.5 r_ta.
- Any gate fails: MODEL STILL INADEQUATE; the table is information only; no model or clash verdict; the README states what is still missing. No re-tuning.
- Clash (only if VALID): best = lowest chi2 of (i)-(v) per footing; RESOLVED if chi2(iii) - best <= 4 on both footings; CONFIRMED if >= 9 on both; else OPEN.
- Labels carried: "transition PM-calibrated at log M_ta >= 13.5 (z = 0, 512^3, mesh 0.39 Mpc/h) and extrapolated ~1 dex to KiDS masses assuming self-similarity in r / r_ta"; CFG503's companion-count label.

## 7. Controls and MUTATE

- C1: stack P data = CFG377 primary (1e-10).
- C10 (load-bearing): the finder's M_ta on the 256^3 cfg411 seed360 run, for halos with log M_ta >= 13.3, agrees with CFG502's peak masses on the same run (CFG502's peak code, copied and re-run here, since CFG502 saved no per-peak catalogue) (median |d log M_ta| < 0.05 dex for matched centres within 1 cell).
- C11 (reported): the stacked xi_hm of a bin from per-halo counts equals a direct dual-tree count for the same halos (1e-9).
- C9 (reported): a steep window (beta = 64, gamma = 128, x_t = 1) gives the stack-P E vector within 0.05 sigma of the sharp one per bin.
- **MUTATE M0 (load-bearing, CFG504_MUTATE=1, outputs *_MUTATE.*):** f_t = Theta(1 - x) through this lane's code (each model's record boundary): must reproduce CFG503's committed main stack-P chi2 for all 7 rows on both footings, and G2 / G3 LCDM, within 0.01.
- **MUTATE SHUF (load-bearing):** on the cfg411 512^3 run, the particle positions are replaced by uniform random positions (same N, seed 504) and the real halo catalogue is kept. For every resolved bin the measured mean xi_hm over shells in [0.5, 3] r_ta,med must satisfy |mean| < 3 sigma_jk and |mean| < 0.05 |real mean|; the step-1 A is reported (expected ~0). A failed MUTATE is reported as a failed control.

## 8. Wording, limits, compute

kappa = 1/2 is FITTED; a0 flat; footings never pooled. "Cold energy" = the cold clumping component; its mass is still required and no particle species is added. Nothing here says the data favour the framework; never "theory closed". On-disk data only; no download. nice -n 15, <= 4 threads / processes. Large arrays in ../_external_data/cfg504_work, not committed.

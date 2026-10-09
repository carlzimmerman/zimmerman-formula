# CFG506: FROZEN CRITERIA -- a framework-native lensing "ruler" (environment term) built from the zero-knob simulations, then a KiDS re-score with it; plus a zero-knob diagnostics pack

Written 2026-10-08, before any script of this lane exists, before any halo catalogue, source field, ruler or KiDS number of this lane has been computed. Nothing below changes after a result is seen. Any departure goes in the README as a dated, disclosed departure; this file is not edited.

## 0. Why (owner's point, 2026-10-08)

The environment / two-halo term E used to score every model against the KiDS isolated-lens stack (CFG502 / 503 / 504) is built from LCDM ingredients (Tinker HMF and bias, NFW, Moster / Behroozi SHMR, CAMB halofit, LCDM-equivalent S0 PM boxes) and it is validated by requiring LCDM to fit. That can tilt the test against the framework. This lane builds the same term from the zero-knob rule's own simulations (CFG424 engine, RC = 0, "TA"), validates it with a model-independent photometric check that assumes no gravity model, and does NOT require LCDM to fit. Local compute on our own snapshots only; no downloads.

## 1. Boxes (z = 0 snapshots in `_external_data/cfg424_work`, `cfg411_work`, `cfg359_work`; read-only)

L = 200 Mpc/h, PM mesh = particle grid. 512^3: cell 0.391 Mpc/h, m_p 5.19e9 Msun/h. 256^3: cell 0.781, m_p 4.15e10.
- TA (zero-knob rule) 512^3: FLAT canonical seed 359; FLAT canonical seed 360; FLAT alt seed 359; DE canonical seed 359.
- S0 (LCDM-equivalent control) 512^3: cfg411 S0 N512 (seed 359), cfg424 S0 N512 seed 360.
- 256^3 (resolution check and diagnostics): TA FLAT canonical / alt seeds 359, 360, 361; TA DE canonical / alt seed 359; S0: cfg359 S0 N256 (seed 359), cfg411 S0 N256 seeds 360, 361.
- Rulers (never pooled across footings or branches): **canonical** = mean of TA FLAT canonical s359 and s360; **alt** = TA FLAT alt s359; **DE branch** (reported, own verdict rows) = TA DE canonical s359; **S0 ruler** = mean of the two S0 512^3 boxes. 256^3 rulers are reported only.
- Memory rule: one 512^3 particle load at a time; before each 512^3 load the script checks `pgrep -f "N512|512 0 MIXA|cfg4[0-9][0-9]_pm.py .* 512"` (and cfg50x 512 jobs) and waits; nice -n 15; <= 4 threads.

## 2. What "lensing mass" means in the zero-knob model (frozen)

The engine (cfg424_pm.py, RES, RC = 0) moves particles with the Newtonian force of ONE Poisson source: lap(a phi) = 1.5 Om (delta + S / (1.5 Om / a)), where delta is the CIC particle contrast (baryons + cold energy together; the particles carry both) and S = e - comp is the added source:
- e = f_sw x max(s_ph - s_c, 0) x catch: the phantom excess (T1 switch f_sw confined to the edge balls x_supply r_ON around resolved peaks, r_ON >= 1.56 Mpc/h), inside the catchments (balls of r_ON);
- comp = s_c q_C: the cold energy drawn from the same catchment C in proportion to the cold density, q_C = sum_C e / sum_C s_c (the per-catchment compensation, i.e. the drawdown), so S sums to zero on every catchment.
The lensing mass of the zero-knob model is this same source: rho_lens / rho_bar = 1 + delta + S / (1.5 Om) at a = 1 (no gravitational slip is assumed; the engine has none). S is recomputed at z = 0 from the saved particle positions with the engine's own functions (imported read-only; the RES / RC = 0 branch copied from CFG495's `sources()`, which copies the engine). Check K1: the recomputed q_max equals the run JSON's z0 q_max within 1e-4 relative; K2: |sum S| / sum e < 1e-3 per box. For S0 boxes S = 0. A particles-only ruler (S omitted) is reported to show S's share.

## 3. Halo finder (CFG504's, copied from cfg504_pm.py, not edited)

Spherical overdensity at Delta_ta (run JSON z0 value) on particles, seeded by local maxima (3x3x3, periodic) of the CIC density with rho / rho_bar > 20; centre = CoM of particles within one cell of the seed, iterated twice; M_ta from counts on 50 log radii 0.5 cell .. 12 Mpc/h; de-duplicated heavier-first within the heavier halo's r_ta; M_200m recorded. **Departure from CFG504's thresholds (declared now):** pre-screen log M_ta >= 11.5 at the seed cell centre (CFG504: 12.0) and keep log M_ta >= 11.8 (CFG504: 12.3), because the KiDS lenses sit at LCDM-equivalent log M_ta ~ 12.0-12.9. Completeness limit: log M_ta >= log10(150 m_p) (11.89 at 512^3, 12.79 at 256^3); halos below it are kept as neighbours but no lens bin is built on them. Control C10 (reported): on S0 512^3 seed 360 the catalogue above log M_ta 12.3 matches CFG504's on-disk catalogue (`cfg504_work/cfg504_pm_S0_512_b.npz`) with median |d log M_ta| < 0.01 dex for centres matched within one cell.

## 4. Galaxies in the boxes (the one non-box input is the OBSERVED stellar mass function)

- SMF: Baldry et al. 2012 (GAMA) double Schechter, (U) recalled: log M_* = 10.66, phi1 = 3.96e-3, alpha1 = -0.35, phi2 = 0.79e-3, alpha2 = -1.47 (Mpc^-3, h = 0.7; densities converted to (Mpc/h)^-3 with the box h 0.6736; stellar masses used in the record's H0 = 70 units, i.e. as the KiDS catalogue's log M*).
- Centrals: every distinct halo. Satellites: occupation N_sat(> m | M) = max(M - M_min(m), 0) / (17 M_min(m)) (CFG502's form, alpha = 1, M_1 = 17 M_min; empirical regularity (U), the only galaxy-halo number not measured in the boxes), M = the host's box M_ta.
- M_min(m) is solved jointly by abundance matching on each box: n_box,cen(> M_min(m)) + n_sat(> m) = n_SMF(> m), bisection on a grid of m (0.02 dex); central log M* = the matched value at its M_ta plus a log-normal 0.15 dex scatter (seed 506). This uses the box's own halo mass function: no LCDM HMF, bias, profile or SHMR enters.
- Satellite numbers per host: Poisson draw (seed 506) of N_sat(> m_floor | M), m_floor = 8.6; each satellite's log M* by inverse-CDF of N_sat(> m | M); position = a randomly chosen particle of that host within r_200m (0.3 r_ta if r_200m is undefined), so satellites trace the host's own simulated matter.
- m_lim,box = the central log M* at the completeness mass; lens bins below it are not built.

## 5. Selection emulation (KiDS isolated lenses, stack P), per projection axis (x, y, z) and per redshift node z_n = 0.15, 0.25, 0.35, 0.45

- Pair kernel K_n(dchi): the measured excess close-pair histogram (`cfg502_stage.npz` H_in - H_an x 0.09 / 20, 5 Mpc bins, |dchi| < 600 Mpc), summing the two z bins of each node (0.10-0.20, 0.20-0.30, 0.30-0.40, 0.40-0.50), normalised. Veto probability for a pair at true line-of-sight separation D (box, periodic, |D| <= 100 Mpc/h = 148.5 Mpc): p_n(D) = Int_{-10}^{10} K_n(u - D) du (Mpc). No Gaussian assumption.
- Lens = any box galaxy (central or satellite) with log M* in a lens bin. Neighbour = any box galaxy with log M*_j > max(log M*_lens - 1, mlim(z_n)) (mlim from `cfg502_stage.npz` Z0 / mlim, the pool's 5th percentile) within 2.02 Mpc/h (3 Mpc) transverse.
- Isolation weight (expected survival, no random draw): w = prod_j [1 - p_n(D_j)] x exp(-lambda_far - lambda_miss), with lambda_far = n_thr pi (2.02)^2 Int_{|D| > 100 Mpc/h} p_n dD (uncorrelated chance projections beyond the box) and lambda_miss = n_miss pi (2.02)^2 x 13.48 Mpc/h, n_miss = max(n_SMF(> thr) - n_box(> thr), 0) (galaxies above threshold that the box lacks, treated as uncorrelated).
- Leaked satellites therefore enter exactly as photo-z leakage allows; f_native(M*, z_n) = the w-weighted satellite fraction of the isolated lenses (reported, and used as the leaked-satellite fraction that mixes each model's stripped / full own profile).
- Lens sampling: at most 6000 centrals and 6000 satellites per lens bin per box (seed 506), weights kept; lens bins 0.1 dex from 8.5 to 11.1 in log M*.

## 6. The native environment term E_native

- Field: rho_lens of section 2. Projected along each axis onto a fine 2D grid (8 N_mesh per side; particles by CIC; S per coarse column spread uniformly over its fine cells). Disc means Sigma_bar(< R) by the exact Fourier disc filter 2 J1(kR)/(kR) at 41 radii geomspace(0.02, 15) comoving Mpc/h, sampled at the lens (bilinear); DeltaSigma(R) = Sigma_bar(< R) - Sigma(R) at the 40 geometric mid-radii.
- **Centrals: own region removed with the record's convention.** Everything inside the lens's own turnaround radius belongs to each model's own profile, so the content of the 3D sphere r < r_rem around the halo centre (particles, and S cells by cell centre) is removed; r_rem = the record's LCDM-equivalent r_ta for that log M* and z_n (CFG503 `moster_RTA`, the same r_ta every model's E already used), converted to comoving h units. Removing the sphere's content makes the mean-density hole H automatic.
- **Satellites: nothing removed** (their own subhalo is not in the field: they sit on host particles); E_sat = DeltaSigma of the field around them (host seen off-centre + everything else). Their own stripped profile comes from each model, as in CFG503.
- E_native(R; bin, z_n) = w-weighted mean over lenses and the three axes. Errors: 27 sub-volume jackknife (3x3x3 by lens 3D position).
- Physical units at lens redshift: comoving mapping of the z = 0 box (stated assumption: no growth correction): R_phys = R_com / (h (1 + z_n)), DeltaSigma_phys = DeltaSigma_com x h (1 + z_n)^2. Tabulated onto CFG503's (LMS, ZG, RG) grid: linear in log M* between bin centres (clamped at the lowest complete bin below m_lim,box; the stack weight affected is reported), linear in z between nodes (clamped), log-linear in R (zero beyond 15 Mpc/h comoving).
- Shuffled-centre twin (MUTATE SHUF, same lenses, same weights and r_rem, uniform random 3D positions, seed 507) computed in the same pass.
- Reported alongside: the box's TOTAL stacked DeltaSigma (own + environment, nothing removed) around central lenses, trusted only at R_com >= 2.5 cells.

## 7. Validation of the native ruler (model-independent; LCDM is NOT required to fit)

Photometric companion count (CFG502 section 5): excess galaxies MORE massive than the lens within R_p < 0.5 Mpc comoving (0.337 Mpc/h) with 10 < |dchi_phot| < 600 Mpc, minus the 4-6 Mpc annulus (2.69-4.04 Mpc/h) scaled by area, per isolated lens. Box emulation: per lens, pairs weighted by [1 - p_n(D)] (beyond the window; |D| <= 100 Mpc/h), companions with log M*_j > max(log M*_lens, mlim(z_n)), lenses weighted by w; tabulated vs (log M*, z_n), evaluated at every KiDS isolated lens (log M*, z) and weighted by the lens's lensing weight (sum of WW), exactly as CFG502's "stack-weighted" mean. Measured = CFG502's per-lens excess from `cfg502_stage.npz` (stack-weighted 0.25 per lens; check C4 reproduces it). **The comparison uses KiDS lenses with log M* >= m_lim,box** (measured recomputed on that subset); the all-lens ratio is reported.
- **Native ruler VALID** for a footing iff measured / predicted is within CFG502's tolerance [0.67, 1.5] for that footing's ruler. Otherwise INVALID: the re-score is computed and reported for information only, with no model verdict.

## 8. KiDS re-score (CFG503's data, grouping, own-profile tables and Hartlap; nothing else changed)

- Data: CFG377 stack P (181,477 lenses, 15 bins, 50-patch jackknife). Own profiles: CFG503's committed tables (`cfg503_own_tables.npz`), Moster primary with the Behroozi - Moster difference of the OWN vector as a rank-one covariance term (the ruler is SHMR-free); leaked-satellite mixing (1 - f) full + f stripped with f = f_native. Prediction for model X = own_X + E_native, evaluated through cfg495_lenslib.finish at each group's node radii and pair-weighted (pstack).
- chi2 = r^T (C_data / h + C_ruler + d d^T)^-1 r, C_ruler = the jackknife covariance of the ruler's 15-bin stack vector (mean of two boxes: (C1 + C2) / 4). Data-only chi2 reported.
- **Verdict bins: the inner trusted bins R <= 0.445 Mpc (0.3 / h Mpc; 9 bins; Hartlap (50 - 9 - 2) / 49).** The full 15 bins are reported (Hartlap 0.6735).
- Models: (i) LCDM; (ii) law to r_ta; (iii) 5.85 r_M growth edge; (iv) CFG487 V1 clock taper; (v) CFG495 F_dd (the zero-knob rule's engine-rule lens: edge + drawdown); reported F_nodd, law to 0.5 r_ta. Both footings (canonical 9.3603e-11, alt 1.1312e-10; never pooled), each with its own footing's ruler; the DE-branch ruler gives a separate canonical row set. LCDM is scored with the SAME native ruler (equal terms) and, for comparison only, with the S0 ruler.
- Per model and footing (only if that footing's ruler is VALID): PASS if p > 0.01 on the 9 trusted bins, else FAIL. **"The framework fits with its own ruler"** on a footing iff at least one of (ii)-(v) passes there; the answer is reported per model (F_dd first).
- Also reported: the old LCDM-native terms (CFG503 E_nlz; CFG504's committed E if committed by the time of scoring) through the same code for the same rows, and per-bin native / LCDM-native ratios.

## 9. Ruler comparison (reported)

Per stack-P bin: E_native (canonical, alt, DE, S0) vs CFG503's E_nlz (and CFG504's if available); the ratio, the difference in data sigma, and the split into centrals / leaked satellites / S share. 3D stacked profiles TA / S0 around matched-mass distinct halos reported.

## 10. Controls and MUTATE

- C1: stack P data = CFG377 primary (1e-10). C2: this lane's scoring code with E = CFG503's E_nlz and f = CFG503's f reproduces CFG503's main stack-P chi2 (15 bins) for all 7 rows on both footings within 0.01 (load-bearing). C3: the Fourier-disc DeltaSigma of a single point mass on the fine grid equals M / (pi R^2) within 2% at R >= 3 fine cells (load-bearing). C4: measured companion excess = CFG502's (1e-9). K1, K2 (section 2; load-bearing for TA boxes). C10 (section 3; reported).
- **MUTATE SHUF (load-bearing):** the ruler built around shuffled (uniform random) centres must carry no environment signal: with H = -DeltaSigma of a uniform rho_bar sphere of radius r_rem (the hole alone), the shuffled stack-P vector minus H must satisfy, in every bin, |E_shuf - H| < 3 sigma_jk(E_shuf) or < 0.1 sigma_data, and the bin-mean |E_shuf - H| < 0.1 x the bin-mean |E_native - H|.
- **MUTATE S0 (load-bearing):** the ruler built from the S0 boxes by the same code must reproduce the LCDM-native term: CFG504's committed stack-P E vector if committed when scoring runs, otherwise CFG503's E_nlz (disclosed): |E_S0 - E_ref| <= max(0.3 |E_ref|, 1 sigma_data) in at least 12 of the 15 bins. A failure is reported as a failed control and stated next to every verdict (it means the native and LCDM-native constructions differ beyond the gravity model, e.g. through the galaxy-halo connection).
- Outputs of MUTATE runs are written as *_MUTATE.*.

## 11. Zero-knob diagnostics pack (reported; committed tables and small PNGs)

- D1 settled vs unsettled cold energy: projected 20 Mpc/h slabs of (1 - f_b)(1 + delta) f_sw (settled: switch ON) and (1 - f_b)(1 + delta)(1 - f_sw) (unsettled), plus e and comp, for TA FLAT canonical s359 at 512^3 and 256^3; mass fractions settled / unsettled and the share inside distinct halos.
- D2 catchment draw: q_C per catchment vs the catchment's mass and vs its host's M_ta, quantiles per mass bin, at 256^3 and 512^3 (all TA boxes); q_max per box vs the run JSONs (the 0.30 -> 0.49-0.57 rise).
- D3 concentrations vs S0: per distinct halo with r_ta >= 5 cells, M(< r_200m / 2) / M_200m converted to an NFW c (mesh-limited, labelled), median per mass bin, TA / S0 at matched seeds (359: TA FLAT can vs cfg411 S0; 360: TA FLAT can s360 vs cfg424 S0 s360).
- D4 matter power ratio P_TA / P_S0 vs k at z = 0 from the run JSONs, matched seeds, both resolutions, mean and seed scatter.
- D5 halo mass function ratio TA / S0 (distinct halos, M_ta, 0.2 dex bins) at matched seeds, both resolutions, Poisson errors.

## 12. Wording and limits

kappa = 1/2 is FITTED; footings never pooled. "Cold energy" = the cold clumping component; its mass is still required and no particle species is added. Nothing here says the data favour the framework; never "theory closed". The z = 0 box is mapped to lens redshifts without growth correction; the PM force is softened below ~1 cell (0.39 Mpc/h at 512^3), so the environment inside ~0.3 Mpc of satellites is mesh-limited; the satellite occupation ratio 17 and the SMF are external (U) inputs; the engine's phantom excess exists only around resolved peaks (r_ON >= 1.56 Mpc/h), so galaxy-scale lenses' own profiles come from the analytic models. Large arrays live in ../_external_data/cfg506_work and are not committed.

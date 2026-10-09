# CFG520: FROZEN CRITERIA -- CFG506's native lensing ruler with its galaxy-halo rule recalibrated to the MEASURED parent satellite fraction (CFG519), then CFG506's validation and re-score unchanged; plus CFG502 / CFG503 re-scored with the measured leaked-satellite fraction

Written 2026-10-08, before any script of this lane exists and before any number of this lane (calibrated rule, box table, ratio, chi2) has been computed. Nothing below changes after a result is seen. Any departure goes in the README as a dated, disclosed departure; this file is not edited.

Inputs already on record (committed): CFG506 (criteria 27a6c64ee; native ruler INVALID: companion ratio 0.653, leaked fraction 0.343 F / 0.432 P); CFG519 (criteria ff98baf04; leaked-satellite fraction of the isolated lenses f_obs = 0.2234 +- 0.0044 tot; parent 0.313; spec companions 0.125; CFG506's photometric ratio stays the like-for-like validation).

## 0. What is and is not changed

- **Changed (part A):** only the satellite occupation of CFG506's section 4. CFG506: N_sat(> m | M) = max(M - M_min(m), 0) / (17 M_min(m)), M = host box M_ta, M_min(m) solved jointly by abundance matching to the GAMA SMF on each box.
- **Unchanged:** boxes, lensing source (engine's own Poisson source, S = e - comp), halo finder and catalogue, SMF, central scatter 0.15 dex, seeds (506 / 507), satellite placement on host particles, selection emulation (pair kernel, isolation weights, variants F and P), DeltaSigma construction, own-sphere removal, jackknife, tabulation, scoring code, data, own-profile tables, Hartlap factors, trusted bins, footings.
- The halo catalogue is read from CFG506's per-box files (`_external_data/cfg506_work/cfg506_box_<KEY>.npz`: cen, Mta, rta, M200m, r200m), i.e. the same finder output, not re-found (no new PM simulation, no new halo finding). Check: halo count = CFG506's `n_halos` for each box.
- Boxes: the six 512^3 boxes of CFG506 (TA FLAT canonical s359, s360; TA FLAT alt s359; TA DE canonical s359; S0 s359, s360). Rulers exactly as CFG506: canonical = mean(TA can s359, s360), alt = TA alt s359, DE = TA DE can s359 (own rows), S0 = mean(S0 s359, s360). 256^3 boxes give no lens bin (m_lim,box 11.02) and are not re-run.

## 1. Calibration target (CFG519 data; computed by this lane from CFG519's own state with CFG519's own cell code)

- Satellite label S_IC (G3C member, not the iterative centre), lens candidates ALL (no isolation cut) inside the G09/G12/G15 overlap with a G3C match (CFG519 `srcA = inside & L_m`), lens weight wl = sum of WW (CFG519's weight; no shear enters).
- Per (log M*, z_phot, colour) cell: CFG519's `cell_frac` (>= 20 matched lenses, frozen fallback pooling over z, then over colour). The parent fraction of a (log M*, z) cell = the colour sub-cells weighted by the ALL-candidate weight W (sum of wl over all 605,531 candidates) of each sub-cell.
- **Calibration targets T_a**: the two mass bins entirely above the box completeness (m_lim,box = 10.42-10.44): a = [10.50, 10.75) and [10.75, 11.00); T_a = the W-weighted mean over the z_phot cells 0.1-0.2, 0.2-0.3, 0.3-0.4. z 0.4-0.5 is excluded (G3C least complete there; CFG519). Errors: CFG519's 12-region jackknife. The (log M*, z) cell table including 8.5-10.5 and z 0.4-0.5 is reported.
- C_T (load-bearing): the same code reproduces CFG519's f_ALL_parent 0.3133864615 and ISO f_IC 0.2234274645 within 1e-9.

## 2. The recalibrated galaxy-halo rule (calibrated on the S0 boxes ONLY)

- **Primary form (one constant):** N_sat(> m | M) = max(M - M_min(m), 0) / (B M_min(m)); B replaces 17. M_min(m) is re-solved on each box by CFG506's joint abundance match with B in place of 17 (box HMF + power-law extension, unchanged).
- **Box parent fraction f_box,a(B)**: all box galaxies with log M* in bin a (centrals with the 0.15 dex scatter, satellites), as the expectation over the catalogue halos (Gaussian scatter for centrals; N_sat(> lo | M) - N_sat(> hi | M) for satellites), mean of the two S0 512^3 boxes. C_A (load-bearing): the drawn catalogue (seed 506, CFG506's draw code) agrees with the expectation within 0.01 in each bin, on both S0 boxes, at the calibrated rule.
- **Fit:** B* minimises sum_a w_a (f_box,a - T_a)^2, w_a = the stack-P ISO lensing weight (sum of WW over the 181,477 isolated lenses) in bin a. Grid log10 B in [0.5, 3.5] step 0.005, then bounded refinement (xatol 1e-4 dex).
- **Acceptance (CAL-OK):** |f_box,a - T_a| <= 0.05 in both bins AND |weighted mean f_box - weighted mean T| <= 0.02.
- **Declared fallback (only if the primary fails CAL-OK):** N_sat(> m | M) = [max(M - M_min(m), 0) / (B M_min(m))]^alpha, (B, alpha) on a grid alpha in [0.30, 1.50] step 0.01 with B refined per alpha as above; same acceptance. The abundance match and the satellite mass draw use the same N_sat(> m | M). If the fallback also fails CAL-OK: **CALIBRATION FAILED**, the lane stops there (no validation, no re-score) and reports why.
- **Blindness:** the calibration script reads only the two S0 box catalogues, CFG519's state, CFG502's staging (cells, WW) and the SMF; no TA box and no shear / ESD file. It records the files it opened; a TA or ESD path in that list voids the calibration.
- The calibrated rule (form and constants) is then applied IDENTICALLY to every box (TA and S0), each re-solving its own M_min(m) by its own abundance match, exactly as CFG506.

## 3. Validation (CFG506 section 7, unchanged, plus the leaked-fraction check)

Per ruler, frozen variant F (CFG506's neighbour threshold); variant P (CFG506 departure D1) computed and reported the same way, no verdict of its own.
- **V-A (CFG506's rule, copied):** photometric companion count, measured / predicted, lenses with log M* >= m_lim,box (CFG506's lens weight convention, measured = CFG502's per-lens excess), within [0.67, 1.5].
- **V-B (new, from CFG519):** the ruler's stack-weighted leaked-satellite fraction (CFG506's convention: the w-weighted satellite fraction of the isolated box lenses on CFG503's grid, pair-weighted over stack P) within 2 sigma_tot of f_obs: |f_native - 0.2234| <= 0.0089. (CFG519's looser 0.22 +- 0.03 is reported alongside.)
- **Ruler VALID iff V-A and V-B both hold.** Otherwise INVALID: no re-score verdict for it (re-score numbers, if computed, are information only).
- Reported: all-lens companion ratio; parent fraction per box bin vs the CFG519 cell table; ISO / ALL of the box vs CFG519's 0.757; isolation pass fraction box / KiDS.

## 4. KiDS re-score (only if a ruler is VALID; CFG506 section 8, unchanged)

- DeltaSigma stage of CFG506 (maps, own-sphere removal, shuffled twin, jackknife) run on the recalibrated galaxies; scoring through CFG506's code: stack P (CFG377, 15 bins), own profiles from CFG503's tables, leaked-satellite mixing with f = f_native, Moster primary with the Behroozi - Moster own difference as a rank-one term, ruler jackknife covariance added.
- Models: LCDM, law to r_ta, 5.85 r_M edge, V1, F_dd; reported F_nodd and law to 0.5 r_ta. Both footings (canonical 9.3603e-11 with the canonical ruler; alt 1.1312e-10 with the alt ruler; never pooled); the DE ruler gives its own canonical rows; LCDM is also scored with the S0 ruler.
- **Verdict bins: the 9 trusted bins R <= 0.445 Mpc** (Hartlap (50 - 9 - 2) / 49). PASS if p > 0.01. "The framework fits with its own ruler" on a footing iff at least one of law to r_ta, edge, V1, F_dd passes there (F_dd reported first). The full 15 bins are reported (Hartlap 0.6735).
- If the canonical ruler is VALID and the alt ruler is not (or vice versa), each footing gets the verdict of its own ruler only.

## 5. Part B: CFG502 / CFG503 with the measured leaked fraction

- **Rule:** each lane's leaked-satellite fraction grid f(log M*, z) (CFG502 `W10_f`; CFG503 `moster_W10_f` and `behroozi_W10_f`) is scaled by one factor so that its stack-weighted value equals f_obs = 0.2234: s = 0.2234 / X, X = the value CFG519 compared against (CFG502 0.17122385594807057; CFG503 Moster 0.1805564701196465; CFG503 Behroozi: its own stack-weighted value by CFG506's convention). f' = clip(s f, 0, 1). The shape in (log M*, z) is kept; everything else is unchanged.
- E is rebuilt from each lane's own pieces: E(f') = HOLE + (1 - f') b_c T2h + f' (T_host + b_h T2h). CFG502 from its table (HOLE, S2H, bc, bh, Thost); CFG503 (Thost not stored) by E(f') = HOLE + b_c S2H_nlz + f' X_f with X_f = (E_nlz - HOLE - b_c S2H_nlz) / f, per grid point. Check B0 (load-bearing): f' = f rebuilds each lane's committed E table within 1e-9 relative (+ 1e3 Msun/Mpc^2 floor).
- **CFG502:** own vectors = its committed per-model stack vectors minus its committed E vector (both in `cfg502_score_results.json`); model' = own + E(f'). Data-only chi2 with CFG502's Hartlap. Check B1 (load-bearing): with f' = f the code reproduces CFG502's 14 stack-P chi2 within 0.01.
- **CFG503:** f' enters both places CFG503 uses f: E and the own-profile mixing (1 - f') full + f' stripped (primary). Reported: E-only (own mixing at the original f). Scored with CFG506's scoring function (the one that reproduced CFG503's chi2 in CFG506's C2). Check B2 (load-bearing): with f' = f, CFG503's 14 stack-P chi2 reproduced within 0.01.
- Reported per model, both footings: chi2 (15 bins), inner 9 and outer 6 (CFG502), chi2_15 and inner 9 (CFG503), and the shift Delta chi2 = new - old. Also reported: a constant f' = 0.2234 grid, and each lane's gate statement with f' (CFG502: LCDM p > 0.01 on 15 bins; CFG503 G1 the same). This is a re-score with a measured input, not a new verdict on the frameworks: CFG502 / 503's own "MODEL STILL INADEQUATE" labels remain unless the gate passes, and then only the gate statement is reported.

## 6. Controls and MUTATE

- C1 stack P data = CFG377 primary (1e-10). C2 CFG506's C2 (CFG503 reproduction by the scoring code) passes again. C4 measured companion excess = CFG502's 0.2537226181 (1e-9). C_T, C_A, B0, B1, B2 above. In the DeltaSigma stage (if run): K1, K2 (TA), C3 as in CFG506.
- **R0a (load-bearing): CFG506 reproduction at the old occupation.** In the same particle load, the box path at B = 17, alpha = 1 reproduces CFG506's stored selection tables (F_ and P_ CT, W_all, FS, LMW, LMWW) for every 512^3 box within 1e-9 relative.
- **R0b (load-bearing):** the validation code applied to CFG506's own box files reproduces CFG506's committed companion ratios and f_native (variants F and P, every ruler) within 1e-9.
- **R0c (load-bearing, only if a re-score runs):** the re-score code applied to CFG506's own box files reproduces CFG506's committed canonical variant-F chi2 (all 7 rows, both footings, inner 9 and 15 bins) within 0.01.
- G0 (load-bearing, if the DeltaSigma stage runs): the galaxies regenerated in the DeltaSigma stage are identical to the validation stage's.
- **MUTATE M2X (load-bearing; must FAIL validation):** the same calibration procedure and the same rule form as the main run, with every target doubled (2 T_a), applied to every box; the canonical ruler must come out INVALID. If it comes out VALID, every verdict of this lane carries "VALIDATION WITHOUT POWER".
- MUTATE SHUF (CFG506's, load-bearing for the canonical ruler) on the recalibrated rulers if the DeltaSigma stage runs; MUTATE S0 (CFG506's) reported only.
- MUTATE outputs are written as *_MUTATE.*.

## 7. Compute and wording

nice -n 10; OMP / MKL / OpenBLAS / vecLib threads 2; box particle arrays read from disk (no new PM simulation). Each particle-load step records its peak RSS; if a step needs more than ~12 GB it is stopped and reported, not forced. Large arrays in `../_external_data/cfg520_work` (not committed).
kappa = 1/2 is FITTED; footings never pooled. "Cold energy" = the cold clumping component; its mass is still required and no particle species is added. Nothing here says the data favour the framework; never "theory closed". Limits carried from CFG506: z = 0 box mapped to lens redshifts without growth correction; PM softening below ~0.4 Mpc/h (inner bins mesh-limited); SMF external (U); box stellar masses carry no photometric-mass noise, the KiDS masses do.

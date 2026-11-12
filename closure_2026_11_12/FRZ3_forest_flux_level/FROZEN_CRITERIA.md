# FRZ3 FROZEN CRITERIA: the forest row at FLUX level (rule 5's redistribution through the transmitted flux)

Committed alone, before any graded FRZ3 number exists. TEST lane, quarantined. Relabels nothing, registers nothing.
Footings canonical (a0 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), graded separately, never pooled. Cold dark energy is a
gravitating field component; no particle is added. A HOLDS outcome is not a pass for the theory and needs an independent
re-grade; nothing here says the data favour the framework.

## 0. The question, and what was seen before this freeze

FRZ1 (criteria 1835d8fb7d) and its blind re-grade FRZ1R found the forest row FAILS at z 2.2 to 4.4: Delta chi^2
9916 / 9009 (FRZ1) and 8142 / 7686 (FRZ1R), canonical / alt, gate 4. Both fed the matter-power ratio R_cold(k, z) of rule 5
through the record's LINEAR 1D projection (`ss1_cosmo.forest_eval`). That is the weakest link: absorption comes mostly from
gas at overdensity 0 to 10 outside halos and saturates inside them. This lane paints rule 5's layout onto a density field,
computes the transmitted flux with saturation, and measures the flux-power ratio directly.

Seen before this freeze: FRZ1's criteria and RESULT (its table, brackets, known answers, mutations; R_cold at z 3, k 1 / 3 / 5
= 0.992 / 0.845 / 0.665 canonical, 0.992 / 0.831 / 0.669 alt); FRZ1R's RESULT (8142 / 7686; the remainder convention
difference); FRZ2's RESULT (no a0(z) power law passes; P0.5 252 / 167). Pre-freeze checks run while building the code, none
of them a graded number: (i) my copy of the layout (`frz3_layout.py`, below) with FRZ1's remainder convention reproduces
FRZ1's stored R_cold at z 2.2 / 3.0 / 4.4, k 1 / 3 / 5, on both footings to the 4th decimal (check b0); (ii) catalogue sizes
in the 20 Mpc/h box: about 1.46e5 / 1.37e5 / 1.10e5 haloes above 1e8 Msun/h at z 2.2 / 3.0 / 4.4, mass fraction inside
turnaround spheres 0.56 / 0.44 / 0.27, every layout conserves M_ta to 4e-16; (iii) timing smoke runs of the field code at
grid 192, 448 (stopped: resident memory 9.4 GB, over the 8 GB limit, so the grid went to 384) and 384 in a scratch
directory; their ratio outputs were not opened.

## 1. Layout (inherited; copied, not rebuilt)

`frz3_layout.py` copies FRZ1R's `frz1r_hm.py` (self-contained CFG556 numerics: EH no-wiggle at sigma8 0.811 times D(z)^2,
Tinker 2008 with its z-scaling, Tinker 2010 bias, Duffy c(M, z), Moster stars, beta gas, Delta_ta(z) interpolation, PD1 share
at z 1, a0 constant in physical units), with FRZ1's conventions restored: primary = FRZ1 reading L with the unplaced
remainder laid out isothermally (rem r / r_ta); reference = FRZ1's comparison layout Rb (condensed baryons, the rest in the
NFW shape out to r_ta). Both have M_ta inside r_ta, so each halo's difference has zero net mass. Brackets use FRZ1R's
remainder (NFW shape) and FRZ1's reading V (virial scope, with its own Rb).

## 2. Fields, flux, statistic (fixed)

- **Box and grid:** periodic cube L = 20 Mpc/h comoving, 384^3 cells (cell 0.0521 Mpc/h; 3D Nyquist 58 h/Mpc). A 1e11
  Msun/h halo's turnaround radius is 0.48 / 0.50 / 0.53 Mpc/h at z 2.2 / 3.0 / 4.4: 9 to 10 cells. Velocity cell 5.4 to
  6.8 km/s; the line-of-sight Nyquist wavenumber is 0.58 s/km at z 2.2 and 0.46 at z 4.4, 23 and 10.7 times the largest DESI
  k used in that bin (0.0255 / 0.0430 s/km); stated factor >= 10. The box fundamental is 0.0030 to 0.0024 s/km; DESI points below it take
  R_F at the first mode (flat). Velocity conversion with the halo model's flat cosmology (h 0.6736, Om 0.3138).
- **Base field (one per seed, shared by both footings and every variant):** a Gaussian field with the linear spectrum at z
  (the layout's EH x D^2), filtered by exp(-k^2 lambda_P^2 / 2), made lognormal and normalised to mean 1; this carries the
  mass outside haloes, weight f_s = 1 - (painted halo mass) / (box mass). Halo catalogue: Poisson counts per mass point of the
  layout's Tinker 2008 mass function (1e8 to 1e16 Msun/h), grouped in painting bins of 0.05 dex (count-weighted mean
  profile); positions drawn with probability proportional to (1 + delta_s)^b(M) (Tinker 2010 bias), uniform within the
  cell, CIC deposit with the CIC window divided out. The reference field paints every halo with the reference profile
  U_R(k); the form B field paints the SAME haloes with rule 5's U_L(k), i.e. it is the reference field plus the zero-mass
  difference. Same white noise for every z (seed only); four seeds 0 to 3.
- **Gas:** 1 + delta_gas = f_s (1 + delta_s) + (haloes) x exp(-k^2 lambda_P^2 / 2); lambda_P = 80 proper kpc at every z
  (Kulkarni et al. 2015 at z 3, from memory, PROVISIONAL), i.e. 0.172 / 0.216 / 0.291 Mpc/h comoving at z 2.2 / 3.0 / 4.4.
  Gas traces total matter above lambda_P (the record pipeline's own assumption).
- **Flux (FGPA):** tau_real = A (1 + delta_gas)^beta with beta = 2 - 0.7 (gamma - 1); T = T0 (1 + delta_gas)^(gamma - 1),
  T0 = 1.2e4 K, gamma = 1.4 (beta 1.72) at every z (PROVISIONAL, typical of published z 2 to 4 measurements); thermal
  broadening per cell, Gaussian with b = 12.85 sqrt(T / 1e4 K) km/s, periodic, kernel to 5 b_max. No peculiar velocities
  (real space), no hydrodynamics, no shock heating or self-shielding in haloes, no temperature cap, no UV fluctuations,
  no metals or DLA masking. A is tuned separately in each field so the mean flux over all skewers equals
  F_bar(z) = exp(-tau_eff), tau_eff = 0.751 ((1 + z) / 4.5)^2.90 - 0.132 (Becker et al. 2013, from memory, PROVISIONAL):
  0.863 / 0.669 / 0.319 at z 2.2 / 3.0 / 4.4.
- **Skewers:** every 8th line along each of the three axes (6912 per field, 384 pixels each).
- **Statistic:** P1D_F per mode (delta_F = F / <F> - 1); R_F(k_par, z) = P1D_F(form B) / P1D_F(reference) per seed; the graded
  R_F is the mean over seeds of the per-seed ratios. Fed to the record's gate in place of the projected matter ratio: at each
  DESI DR1 P1D point (the 755 points of `forest_setup`, md5 33d7fc21bfd3d745ed71a0bbe80ca433) r = R_F(k, z_bin) (linear in k
  between modes), d = (r - 1) P_data, Delta chi^2 = d C^-1 d with the full covariance. Gate **Delta chi^2 <= 4**, per footing.
- **Matter level on the same fields (for the softening factor):** R_paint(k) = P_m(form B) / P_m(reference), 3D matter power
  of the painted fields (smooth part plus unsmoothed haloes) in 50 log bins 0.3 to 35 h/Mpc, seed mean; fed to the record's
  gate exactly as FRZ1 did (`forest_eval`, form B's CLASS reference, amplitude sqrt(R) on its (KG, ZG) grid, nearest bin),
  using R_paint for k <= 10 h/Mpc and flat at the end values outside (FRZ1's convention). **Softening factor** =
  Delta chi^2(flux) / Delta chi^2(matter, painted). Reported beside it, not graded: Delta chi^2 from the direct 1D power ratio
  of the gas skewers (gas level).
- **Redshifts and staging:** stage 1 (anchors) z 2.2, 3.0, 4.4 with every variant, four seeds; stage 2 the other nine DESI
  bins, primary fields only (reference and rule 5, both footings), four seeds (seeds 0 and 1 first; 2 and 3 if machine time
  allows, total budget about 4 h). The graded Delta chi^2 uses all twelve bins; a bin not computed takes R_F linearly
  interpolated in z between its computed neighbours (stated in RESULT if used).

## 3. Labels (per footing, fixed)

- **FOREST ROW FAILS AT FLUX LEVEL:** Delta chi^2(flux) > 4. **FOREST ROW HOLDS AT FLUX LEVEL:** <= 4 (not a pass for the
  theory; needs an independent re-grade). **NO VERDICT:** a known answer fails, or, at any anchor z, the seed-to-seed scatter
  S of R_F exceeds the effect E (E = rms over the DESI-range modes of (mean R_F - 1); S = rms over the same modes of the
  standard deviation of the per-seed R_F), or a mutation does not bite.
- **Brackets (anchors only, reported beside the label):** gamma 1.2 (beta 1.86) and 1.6 (beta 1.58); lambda_P x 0.5 and x 2
  (smooth field regenerated with the same white noise; halo positions kept); minimum halo mass 1e10 Msun/h (haloes below keep
  the reference profile); FRZ1's reading V (B field = reference + (V - RV)); FRZ1R's remainder convention. A bracket's
  12-bin Delta chi^2 is estimated as Delta chi^2(primary, 12 bins) x [Delta chi^2(bracket) / Delta chi^2(primary)] on the
  three anchor bins (joint covariance block). **Rule:** if any bracket lands on the other side of the gate, the label carries
  FRAGILE with the brackets named; the label itself does not change.

## 4. Known answers (any failure: NO VERDICT)

- **(a)** halo difference switched off (B = R + 0 x difference, through the same code path): R_F = 1 exactly, Delta chi^2 = 0.
- **(b)** the painted R_paint reproduces FRZ1's R_cold at k 1, 3, 5 h/Mpc at each anchor z, both footings, within
  |R_paint - R_FRZ1| <= 0.01 + 0.25 |R_FRZ1 - 1|. (b0, already passed: the copied layout's halo-model R_cold equals FRZ1's.)
- **(c)** optically thin limit (beta 1, no broadening, 1 - <F> = 1e-7): R_F equals the direct 1D gas-skewer power ratio at
  every DESI-range mode of each anchor, within 1e-3 + 0.01 |R_gas - 1|.
- **(d)** mean flux matched: |<F> - F_bar(z)| <= 1e-4 in every field.
- The DESI md5 matches, and the gate gives 0 at R = 1.

## 5. Mutations (anchors; `_MUTATE` outputs; each must bite)

- **M1 saturation removed** (delta_F replaced by -delta_tau, tau as primary, broadening and beta kept): bites if
  |ln(Delta chi^2_M1 / Delta chi^2_matter)| < |ln(Delta chi^2_flux / Delta chi^2_matter)| on the three anchor bins, both footings.
- **M2 halo difference doubled** (B = R + 2 (L - R)): bites if Delta chi^2(flux) on the anchor bins increases, both footings.

## 6. Hand estimate (before any number)

Halo centres are saturated in both fields, so rule 5's main matter-level change (mass taken out of NFW centres) is mostly
invisible in the flux; the mass it moves out toward r_ta raises the overdensity there from about 2 to 3 toward 3 to 6,
which is forest-sensitive, so the flux sees broader, shallower absorbers around haloes. Pressure smoothing (0.2 Mpc/h)
washes out much of the k 3 to 5 h/Mpc structure. I expect R_F - 1 at z 3 of -1 % to -5 % at k_par 0.01 to 0.03 s/km
(sign uncertain, maybe positive at low k after mean-flux retuning), a softening factor 0.02 to 0.3, and Delta chi^2(flux)
of order 100 to 2000: expected label FAILS AT FLUX LEVEL on both footings, about 15 % chance of HOLDS on either.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

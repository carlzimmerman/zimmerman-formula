# SRF1R READING: blind flux-level build of SRH1's forest gate for the settled-radius family

Committed alone, before any SRF1R script is in this folder and before any flux-level number of this lane exists. TEST lane:
adopts nothing, relabels nothing (SRH1, FZS1 and SRH1R keep their labels), registers nothing. Footings canonical (a0
9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), graded separately, never pooled. Cold dark energy is a gravitating field
component; no particle is added. kappa = 1/2 is FITTED. **The settled-radius family is post hoc**: it was chosen after the
forest failed at matter level (FRZ1, then FZS1). **A window is not a pass**: it is a hit on a post hoc family that would
need a further independent check. Nothing here says the data favour the framework.

## 0. Question, what I have read, blindness

Question. SRH1 graded its forest gate G1 at matter level (the record's linear projection of R_cold(k, z) onto the DESI DR1
P1D, Delta chi^2 <= 4) and found f <= 0.722 / 0.725, against galaxy lensing G4's f >= 1.004 / 1.050: WINDOW EMPTY. Graded
at FLUX level instead, what is the largest f the forest allows (f_max), does one f pass G1 to G4 together, and is f = 1
inside?

Read before this freeze: SRH1's RESULT, FROZEN_CRITERIA, `srh1_hm.py`, `srh1_forest.py`, `srh1_hm.out`, `srh1_grade.out`
(first 30 lines); FZS1's FROZEN_CRITERIA, RESULT (to its known-answer table), `fzs1_diag.py` / `.out`; FRZ1's `frz1_hm.py`
and `frz1_forest.py`; `ss1_cosmo.py` lines 212 to 238 (`forest_setup`, `p1d_at`, `forest_eval`); CFG556's library lines 40
to 76, 105 to 112, 180 to 216 (mass function, `rgrid`, `U_of`, `U_set`, `spectra_std`, `spectra_ta`); FRZ3R's `READING.md`
and `RESULT.md` (only those two files of FRZ3R; I listed FRZ3R's folder to find them and so saw its file names, nothing
else). Not opened: anything of SRF1, any FRZ3 or FRZ3R script, part or output, PAPER72, `reviews/`. No `git log` /
`show` / `diff` on SRF1's folder. Nothing of SRF1 has been seen, by accident or otherwise.

Known from FRZ3R's RESULT (used as known answers, section 5): full layout, reading T (positive turnaround-scope painted
field, about half FRZ1's matter change): flux Delta chi^2 363 / 425, matter level of the same fields 5035 / 4377, ratio
0.072 / 0.097; frozen field M: flux 790 / 904, matter 10816 / 9672. FRZ3 (another build) found flux 4.71 / 2.58 against
matter 4720 / 4120. The two builds differ mainly by the pressure-smoothing scale and halo clustering on the IGM.

## 1. Pre-freeze design checks (disclosed; matter level only, no flux number, no Delta chi^2 of this lane)

From SRH1's halo model (its `srh1_hm.py` prefix executed in a scratch directory, read-only), canonical:

- **Which haloes carry the change.** SRH1's one-halo difference P_S - P_Rb at f = 1, z 2.2: 90 % is carried by haloes
  above 2.7e12 (k 3) / 2.0e12 Msun/h (k 10), half by haloes above 1.1e13 / 5.6e12. At z 3.0: 90 % above 1.6e12 / 1.5e12.
  The two-halo part is 3 % (k 3) and 0.4 % (k 10) of the one-halo part. At f = inf (FRZ1's full layout) 90 % lies above
  5e11 / 3e11 (z 2.2) and 2e11 / 1.3e11 (z 3.0, k 3 / 10).
- **These haloes are rare.** Expected counts in a 20 Mpc/h box at z 2.2: 9 above 1e12, 1.5 above 3.2e12, 0.2 above 1e13
  Msun/h (z 3.0: 3.4, 0.4, 0.02). A Poisson box of the size FRZ3R used would hold almost none of the haloes that carry the
  change. **This is why the construction below inserts the heavy haloes one at a time with importance weights** instead of
  drawing them at their true abundance.
- **Radii (f = 1, z 2.2, comoving Mpc/h):** M 1e11: R_set 0.054, r200m 0.111, r_ta 0.477 (galaxy regime). M 1e12: 0.121,
  0.239, 1.054 (galaxy). M 1e13: 0.411, 0.516, 2.336 (cluster regime). At z 3.0 the 1e12 halo is already cluster regime
  (R_set 0.170).
- **Mass fractions in turnaround-scope haloes** (sum n M_ta / rho_m, M >= 1e8): 0.56 / 0.44 / 0.27 at z 2.2 / 3.0 / 4.4;
  below 10^10.8 Msun/h: 0.32 / 0.30 / 0.23. Halo numbers at and above 10^10.8 in a 20 Mpc/h box: 265 / 171 / 58.
- **Timing only:** a 384^3 real FFT takes about 0.05 s with 4 workers on this machine (random numbers; no field built).

## 2. Fields (fixed)

**Halo model and layouts: SRH1's, unchanged.** `srh1_hm.py` executed up to its "checkpointed run" marker from its own path
(read-only; it executes FRZ1's and CFG556's code). At each DESI bin z: `set_z(z)`; the reference halo is FRZ1's "Rb"
layout (`layout(hb, foot, mode="Rb")`), the settled halo is SRH1's `lay_S(foot, z, fac=f)` (law layout inside
R_set = f R_fold, cold reference outside, enclosed mass matched at R_set). Both end at r_ta with mass M_ta. Halo grid,
mass function (Tinker 2008 with z-scaling) and concentrations are FRZ1's (PROVISIONAL, inherited).

**Box.** Periodic, L = 20 Mpc/h comoving, N = 384 (cell 0.0521 Mpc/h), real space (no peculiar velocities), skewers = every
grid line along axis 2 (147,456 per field). Velocity per comoving Mpc/h: 100 E(z) / (1 + z) km/s, E from CFG556's flat
cosmology (its h and Om).

**Background field B (one per z, seed, footing).** Density in units of the mean:
- smooth part f_s (1 + delta_LN), f_s = 1 - sum over all grid masses >= 1e8 of n M_ta / rho_m (section 1: 0.44 to 0.73);
  delta_LN lognormal with target power P_2h(k) / f_s^2, P_2h = P_lin(z) I_Rb(k)^2 the two-halo term of the Rb
  turnaround-scope halo model (CFG556 `spectra_ta`), made on the grid by xi_G = ln(1 + xi_T), negative Gaussian modes
  clipped;
- plus haloes with 1e8 <= M < 10^10.8 Msun/h ("light"): Poisson counts per 0.1 dex bin from W_M V, uniform positions,
  each bin's count-weighted mean Rb profile U(k) (CFG556 `U_of`), CIC deposit divided by the CIC window (floor 0.1),
  applied in k-space.
- White noise and positions seeded by the seed only, shared by both footings and by every bracket except B8 and B9.

**Heavy haloes (M >= 10^10.8 Msun/h), inserted one at a time.** For each 0.1 dex bin from 10.8 to 14.6, K_b positions are
drawn uniformly in the box (K_b = 24 for bins whose expected count N_b = W_M V < 24; otherwise K_b = 48), each with a
grid mass drawn inside the bin with probability proportional to W_M; importance weight w = N_b / K_b. Each inserted halo
h is placed ALONE on top of B:
- reference skewers: B_gas + g_R,h(r); settled skewers: B_gas + g_S,h(r); r = distance from the halo centre (periodic).
- g(r) is the halo's density profile (from its M(<r), central point mass included) smoothed by the 3D Gaussian of the gas
  smoothing scale lambda_P, computed in real space shell by shell (each shell of mass dM at r_j spread by the exact 3D
  Gaussian kernel), in units of the mean density, sampled at cell centres.
- the settled-minus-reference difference g_S - g_R vanishes outside R_set + (smoothing), because M_S = M_R at and outside
  R_set. Only skewers within R_att = R_set + 4 lambda_P + 1 cell of the halo axis are computed for the difference.
- The halo's own reference profile is present on those skewers in both versions (out to r_ta), so the change is seen
  against the halo's own outskirts and the IGM around it.
This is a dilute (isolated-halo) insertion: heavy haloes never overlap each other. At the true abundance at f <= 3 the
changed regions of heavy haloes fill under 1 % of skewers, so the dilute limit is the true one there; at f = inf (known
answer b) it is an approximation for haloes near 10^11.

**What f changes.** Only the heavy haloes' profiles. Light haloes (M < 10^10.8) keep their reference layout in both
versions: at f = 1 their R_set is below 0.035 Mpc/h (under one cell). The halo-model share of the f = 1 matter change they
carry is computed and reported (check c0).

## 3. Gas, flux, statistic (fixed; FRZ3R's adopted gas physics)

- **Gas:** 1 + delta_gas = matter density smoothed by exp(-k^2 lambda_P^2 / 2) (B in k-space; inserted haloes in real
  space as above); lambda_P = 79 comoving kpc = 0.0532 Mpc/h at every z (Kulkarni et al. 2015 as read by FRZ3R; PROVISIONAL).
  Values below 1e-6 floored at 1e-6 (fraction recorded).
- **FGPA:** tau = A (1 + delta_gas)^beta, beta = 2 - 0.7 (gamma - 1); T = T0 (1 + delta_gas)^(gamma - 1), T0 = 1e4 K,
  gamma = 1.5 (beta 1.65) (FRZ3R's values, the record's stage16 defaults; PROVISIONAL). No temperature cap in the primary.
- **Thermal broadening:** Gaussian exp(-v^2 / b^2), b = 12.85 sqrt(T / 1e4 K) km/s, in 16 classes of log b from 2 to
  800 km/s (class centre b; b outside clipped into the end classes), each class convolved along the line of sight by FFT
  (periodic); negative tau from ringing clipped at 0.
- **Mean flux:** F_bar(z) = exp(-tau_eff), tau_eff = 0.751 ((1 + z) / 4.5)^2.90 - 0.132 (Becker et al. 2013 as written in
  the record; PROVISIONAL). A is tuned on B alone so that <exp(-A tau_1)> over B = F_bar to 1e-5 relative; the same A is
  used for every inserted-halo skewer of that field.
- **P1D estimator:** delta_F = F / F_bar - 1 on each skewer; P1D(k_v) = (L_v / N^2) |FFT(delta_F)|^2, averaged.
- **Flux change from the heavy haloes:**
  - Delta P(k) = (1 / N_sk) sum_h w_h sum over h's skewers [ |FFT delta_F,S|^2 - |FFT delta_F,R|^2 ] (L_v / N^2);
  - Delta F_bar = (1 / N_sk N) sum_h w_h sum over h's cells (F_S - F_R);
  - mean-flux matching by linear response: the settled field's A is A (1 + eps), eps = Delta F_bar / <A tau F>_B, which
    adds eps dP/deps, with dP/deps measured on B by a finite difference eps0 = 1e-3 at fixed normalisation F_bar;
  - R_F(k_v) = 1 + [Delta P(k_v) + eps dP/deps(k_v)] / P1D_ref(k_v), with P1D_ref = P1D(B) plus the heavy haloes' own
    reference contribution at true abundance: (1 / N_sk) sum_h w_h sum over skewers within r_ta + 4 lambda_P of h
    [ |FFT delta_F,R|^2 - |FFT delta_F,B|^2 ] (L_v / N^2).
- **Seeds:** anchors z 2.2, 3.0, 4.4: seeds 0, 1, 2; the other nine DESI bins: seed 0. R_F at an anchor is the mean over
  seeds of the per-seed R_F.
- **Flux gate:** at every DESI DR1 P1D point (`forest_setup`, 755 points, md5 33d7fc21bfd3d745ed71a0bbe80ca433) r =
  R_F(k_data) of its own bin's field, linear in k between box modes, flat at the first mode below the box fundamental;
  d = (r - 1) P_data; Delta chi^2_flux,real = d C^-1 d with the full covariance.
- **Matter level of the same construction:** R_paint(k) = 1 + Delta P_3D(k) / P_3D,ref(k), Delta P_3D = sum over heavy
  grid masses of n M-weighted (U_S^2 - U_R^2) / rho_m^2 (the one-halo expectation of exactly the inserted profiles; for
  uniform placement the cross terms vanish in expectation), P_3D,ref = measured 3D power of B (seed mean) + the heavy
  haloes' one-halo term sum n U_R^2 / rho_m^2. Fed to the record's projection as FRZ1 / FRZ3R did: `forest_eval` with form
  B's CLASS reference, amplitude sqrt(R) on the (KG, ZG) grid by nearest DESI bin, R_paint used for 0.3 <= k <= 10 h/Mpc,
  flat at its end values outside. Result: Delta chi^2_matter,real(f).
- **Record's matter level at every grid f:** Delta chi^2_SRH1(f) from SRH1's own path (`ratios_S`, then the FRZ1 forest
  pipeline as `srh1_forest.py` runs it). For f on SRH1's grid it must equal SRH1's stored values (check c0).

**Graded statistic.** The carry factor K(f) = Delta chi^2_SRH1(f) / Delta chi^2_matter,real(f) converts my construction's
matter level to the record's. **Delta chi^2_G(f) = Delta chi^2_flux,real(f) x K(f)**: the flux-to-matter softening of my
fields applied to SRH1's own matter-level number. Where Delta chi^2_matter,real(f) < 0.01, K is taken as its value at
f = 0.7. The unscaled Delta chi^2_flux,real(f) is a bracket (B0, "carry convention") inside the FRAGILE rule.

**G1 at flux level passes at f iff Delta chi^2_G(f) <= 4.** f_max = the largest grid f such that every grid f up to it
passes; the edge is interpolated linearly in log Delta chi^2_G between the last passing and the first failing grid point.

## 4. f grid (fixed)

Flux computed at f = 0, 0.30, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.10, 1.25, 1.40, 1.60, 1.80, 2.00, 2.50, 3.00, 4.00,
6.00 and inf (R_set = r_ta, FRZ1's full layout). SRH1's other grid values (0.35, 0.40, 0.45, 0.55, 0.65, 0.75) are not
computed at flux level (SRH1's matter Delta chi^2 there is <= 5.35); they are reported as "flux not computed" and enter
the edge only through interpolation between computed neighbours. The spacing above 0.7
(about 10 to 15 %) locates the edge to a few per cent by interpolation. Brackets use f = 0.70, 1.00, 1.25, 1.60, 2.00, 3.00,
inf.

## 5. Known answers (any failure: NO VERDICT, numbers reported ungraded)

- **(a) f = 0:** the inserted settled profile equals the reference: Delta P = 0, eps = 0, R_F = 1 at every mode and every
  bin, Delta chi^2 = 0 (|value| <= 1e-12), both footings; DESI md5 matches; the gate returns 0 at R = 1.
- **(b) f = inf (R_set = r_ta, beyond the layout's reach):** the full-layout numbers of this construction, unscaled, against
  FRZ3R's reading T (the positive turnaround-scope build): Delta chi^2_matter,real within a factor 2 of 5035 / 4377, and
  Delta chi^2_flux,real within a factor 3 of 363 / 425. Reported beside: field M's 790 / 904 and 10816 / 9672, and FRZ1's
  9916 / 9009 (the graded Delta chi^2_G at f = inf against FRZ1 x FRZ3R's ratio, 715 / 874, reported only).
- **(c) matter level:**
  - c0: my recomputation of SRH1's path reproduces SRH1's stored G1 Delta chi^2 at every f of its grid I recompute (f = 0.3,
    0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.25, 1.5, 2.0) to 0.01, in particular 38.741 / 36.658 at f = 1. Reported: the same
    with only haloes >= 10^10.8 changed (the light-halo share).
  - c1: at f = 1, Delta chi^2_matter,real / 38.74 (canonical) and / 36.66 (alt) lies in [0.25, 1.5] (my fields carry at
    least half and at most 1.22 times SRH1's amplitude change).
  - c2: along the grid, K(f) / K(1) lies in [0.5, 2] at every grid f from 0.7 to 6 where Delta chi^2_SRH1(f) >= 1.
  - How much of SRH1's change my fields carry is reported per anchor and k (R_paint - 1 over R_cold - 1 at k 3, 5, 10).
- **(d) mean flux:** |<F> - F_bar| / F_bar <= 1e-4 over B in every field and variant (and in mutation M1's linear flux);
  |eps| <= 0.01 at every f <= 6 (linear response valid).
- **(e) seed scatter:** at z 2.2 and 3.0, both footings, at f = 1 and at the two grid points bracketing f_max: E = rms over
  the DESI-range modes (box fundamental to the bin's DESI maximum) of (R_F - 1), S = rms of the standard error of the
  three-seed mean. NO VERDICT if S > E / 3. z 4.4 is exempt where E < 1e-4. Per-seed Delta chi^2 of the anchor block
  reported.
- **(f) confinement:** for every heavy grid mass at z 3, f = 1: |g_S - g_R| outside R_set + 5 lambda_P is below 1e-6 of
  the peak |g_S - g_R|; M_S(r_ta) = M_R(r_ta) = M_ta to 1e-9 (SRH1's KA-M).

## 6. Mutations (separate `*_MUTATE*` outputs; each must bite on both footings, or NO VERDICT)

- **M1 saturation removed:** F = 1 - A tau (tau, broadening and beta kept; A tuned on B so that <F> = F_bar), anchors
  seed 0, f = 1 and f = 2. Bites if the anchor-block flux Delta chi^2 (joint covariance of the three anchor bins) changes by
  a factor >= 1.25 either way at f = 1 or at f = 2. Its direction (toward the matter level or away) is reported.
- **M2 R_set doubled:** at f = 1 with R_set = 2 f R_fold (run as its own case, not read off the grid), anchors seed 0.
  Bites if the anchor-block flux Delta chi^2 is >= 2 x that at f = 1.

## 7. Brackets (frozen; anchors, seed 0, the bracket f list of section 4)

A bracket's 12-bin value = Delta chi^2_G(primary) x [anchor-block flux Delta chi^2 (bracket) / anchor-block flux Delta
chi^2 (primary, seed 0)], each at that f.
- B0 carry convention: the unscaled Delta chi^2_flux,real (12 bins, all seeds), no bracket run needed.
- B1 lambda_P x 0.5; B2 lambda_P x 2; B3 lambda_P = 100 proper kpc (= 0.1 (1 + z) h Mpc/h comoving; 0.269 at z 3).
- B4 gamma 1.2; B5 gamma 1.6 (temperature-density slope; beta moves with it).
- B6 tau_eff x 0.9; B7 tau_eff x 1.1 (mean flux).
- B8 clustered placement: heavy-halo positions drawn with probability proportional to exp(b_M delta_L(x)), delta_L the
  smooth field's Gaussian smoothed at 0.5 Mpc/h and scaled to the linear sigma at that smoothing, b_M the Tinker 2010 bias
  of the halo's grid mass (light haloes stay uniform); weights unchanged.
- B9 resolution: N = 256 (cell 0.078 Mpc/h), same box, seed 0, every ingredient rebuilt.
- Reported only, outside the FRAGILE rule (not on the brief's list; a physics choice FRZ3R did not make): B10 temperature
  capped at 1e5 K (b <= 41 km/s) to mimic hot, collisionally ionised halo gas that the FGPA does not describe.

**FRAGILE** if any of B0 to B9 (a) puts f = 1 on the other side of the flux gate from the primary, or (b) opens a window the
primary does not have, or closes the primary's window (bracket f_max, interpolated on the bracket f list, on the other side
of f_lo).

## 8. Labels (per footing, never pooled)

Other gates are taken from SRH1's committed outputs, not re-graded: G2 lower edge 0.391 / 0.391; G3 holds at every f; G4
lower edge 1.004 / 1.050 (SRH1's interpolated edge; G4 FAILS at f = 1.00 on both footings, +2.003 / +2.04 sigma early
type, and passes from 1.25 on its grid). f_lo = max(G2 edge, G4 edge) = 1.004 / 1.050.

- **WINDOW OPENS AT FLUX LEVEL [f_lo, f_max]** if f_max >= f_lo, with "f = 1 INSIDE" if f = 1 passes all four gates, else
  "f = 1 OUTSIDE" (as frozen this needs G4 at f = 1, which SRH1 graded FAIL on both footings, so f = 1 is OUTSIDE unless
  that changes; whether f = 1 passes the forest at flux level is stated beside the label), with or without FRAGILE. **A hit
  on a post hoc family, not a pass of form B.**
- **WINDOW EMPTY AT FLUX LEVEL** if f_max < f_lo; the gap f_lo / f_max is given.
- **NO VERDICT** if a known answer (a) to (f) fails or a mutation does not bite.

Reported beside the label, ungraded: f_max on its own; the window read with SRH1R's blind finding that lensing as graded
cannot see f (lower edge then G2's 0.391); Delta chi^2_flux,real, Delta chi^2_matter,real, Delta chi^2_SRH1, K and the
softening ratio at every grid f; per-bin values (own covariance blocks); the gas-level 1D ratio at the anchors.

## 9. Physics left out (stated in the result)

Hydrodynamics (gas follows matter above lambda_P), shock heating and hot halo gas (bracket B10 only), collisional
ionisation, self-shielding and damped systems in haloes, UV-background and temperature fluctuations, metals, continuum
errors; peculiar velocities and infall; heavy haloes isolated from each other (dilute insertion); halo positions
uncorrelated with the IGM in the primary (B8); the changed profiles of light haloes (< 10^10.8); the two-halo part of the
change (3 % of the one-halo part at f = 1, z 2.2, k 3); the 20 Mpc/h box's missing large-scale power (DESI points below
the box fundamental take the first mode's ratio); FRZ1's halo model and SRH1's layout as inherited (PROVISIONAL).

## 10. Compute plan (frozen)

Stage 0 (light, one process per footing at most 4 in all): halo-model tables per (z, footing): heavy-mass profiles
M_R(r), M_S(r; f) and their smoothed g(r) for each lambda_P variant; light-bin U_R(k); Delta P_3D, the heavy one-halo
term; SRH1's path Delta chi^2 at every grid f. Stage 1 (heavy, one job, `nice -n 19`, 4 worker processes, restartable part
file per (stage, z, seed, footing), SIGTERM stops between parts with exit 75, done-file at the end): anchors (3 seeds),
the nine other bins (seed 0), mutations, then brackets B1 to B10 in that order. If time runs short, brackets are dropped
from the end and reported as not computed. Peak memory target under 12 GB; large temporary tables deleted at the end.

## 11. Hand estimate and expectation (before any flux number)

- At f = 1 the change sits in haloes above about 2e12 Msun/h, inside R_set = 0.4 to 0.8 r200m. There the gas overdensity
  is above about 50 (NFW at 0.8 r200m), so tau = A Delta^1.65 with A about 0.2 to 0.4 is above 100: deep saturation. The
  absorption trough's edge (tau about 1) lies where Delta is about 2 to 3, at 2 to 3 r200m, far outside R_set.
- So the flux sees the settled change only through the broadened wings of the hot, dense core gas (T = 1e4 Delta^0.5 gives
  b of 100 km/s and more in the cores in this FGPA) and the mean-flux matching. A flatter interior at fixed enclosed mass
  lowers the central density a little: the trough narrows by a logarithmic amount.
- My expectation: softening (flux / matter on the same fields) of 0.002 to 0.03 at f <= 2, well below FRZ3R's 0.07 to 0.1
  for the full layout (whose change reaches r_ta, into Delta of 1 to 10 gas). Then Delta chi^2_G at f = 1 of about 0.1 to 1
  (the forest passes at f = 1), and f_max between 1.4 and 3 (SRH1's matter level is 134 at 1.25, 280 at 1.5, 452 at 2).
- Expected label: WINDOW OPENS AT FLUX LEVEL [1.004, about 2] / [1.050, about 2], f = 1 OUTSIDE (by G4, not by the forest),
  probably FRAGILE (the carry convention B0 or lambda_P x 2 or B3 likely move the edge across f_lo). Odds: window opens 55 %,
  empty 20 %, NO VERDICT 25 % (known answer b, the factor-3 match to a build that itself disagrees with FRZ3 by a factor
  100, or the seed scatter e).
- B10 (temperature cap) should cut the flux response at small f strongly, because it removes the broad wings of hot cores
  that carry it in the FGPA.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

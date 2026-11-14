# WLG1R FROZEN CRITERIA: blind builder's reading of WLG1's frozen question (BLIND_BRIEF.md, ec7fed6252)

2026-11-14. Written by the blind builder and committed alone, before any script of this lane exists, before any query of
this lane is sent and before any number of this lane is computed. TEST lane, blind re-grade. Adopts nothing, relabels
nothing, registers nothing, edits no scorecard. Footings side by side, never pooled: canonical a0 = 9.3603e-11, alt
a0 = 1.1312e-10 m/s^2 (EUC1's alt 1.132e-10 only inside KA-5). Cold dark energy is a gravitating field component of the
record, not a particle and not matter. kappa = 1/2 and X = 5.41 are FITTED; nothing here can show the theory closed or the
data favouring the framework over LCDM. POST HOC (as the brief states): a favourable word is a HIT awaiting review, never a
pass of the theory.

The builder has not opened WLG1's folder, the scorecard, the paper drafts, XJ1R, EUC18 or the memory folder, and will not.
Sections 0 to 7 and 9 of the brief are adopted as written. This file fixes the builder's reading where the brief leaves a
choice. Every reading below is fixed now; none will be changed after a number is seen.

## A. Question and words (unchanged from the brief)

(S) speed s = v_L(M_b, z_l) / v*(z_l), v_L = (10 G (1 + X) M_b H(z))^(1/3), v*(z) = a0 / (10 (1 + X) H0) / E(z),
H0 = 67.4 km/s/Mpc, Omega_L = 0.6847 (JNT2's `jnt2_common.py`, imported read-only). (A) amount r = log10(M_obs / M_ref).
Median with 2,000-resample bootstrap of lenses, numpy default_rng(20261114) (a fresh generator with that seed for every
interval), 2.5 / 97.5 percentiles.

- (S): FAST if lower bound >= 1; SLOW if upper bound < 1; MIXED otherwise.
- (A): FITS if the interval overlaps [-0.10, +0.10]; UNDER if lower bound > +0.10; OVER if upper bound < -0.10.
- Control condition: graded C lenses with s >= 1 under the same configuration; if >= 20, their median r interval must
  overlap [-0.10, +0.10]; fewer than 20: met trivially (stated).
- Word, first that applies: 1. SLOW -> **GROUPS TOO SLOW: ROW 40 FAILS, BLIND**; 2. UNDER -> **HALO SHORT: ROW 40 FAILS,
  BLIND**; 3. FAST + FITS + control met -> **WIDE LENSES ARE FAST GROUPS: ROW 40 PASSES, BLIND** (a HIT, post hoc);
  4. otherwise **NO VERDICT, BLIND**.
- **FRAGILE** if any of the 13 brackets (G-0, G-HI, B-UNC, B-RAW, B-W05, B-W12, R300, R600, N-B, B-C07, B-C14, B-ZS2,
  B-STAR+) gives a different word; each changes one thing against the primary.
- **NOT EVALUABLE** if any known answer (KA-1 to KA-7) or instrument check (N1, N2) fails, any must-bite twin (TW-ZS,
  TW-INJ, TW-X0) does not bite, or fewer than 150 W lenses are graded. Applied per footing.

## B. Readings fixed by the builder

1. **Cosmologies.** Distances (D_A, D_L, Sigma_cr, projected radii) in EUC1's catalogue cosmology (flat, H0 67.74,
   Om 0.3089; `euc1.py` imported read-only). H(z) for R_sys, v_L and v* from JNT2's (67.4, 0.6847), so that KA-7 holds in
   one convention. FRZ1's halo (h 0.6736, Planck baryon and cold densities) copied from LNJ1 for the halo shape only.
2. **R_sys iteration.** M_b(<R) = M*_lens + M*_mem(<R) + M_gas, with the class gas counted whole at every R (ESZ1's
   aperture is about 700 kpc; it is not apportioned in radius). R <- (G (1 + X) M_b(<R) / (100 H(z_l)^2))^(1/3), start
   300 kpc, stop at |dR| < 0.1 kpc or 30 iterations (the last R is used; non-converged lenses counted and reported), then
   clipped to [100, 600] kpc (a non-positive M_b gives 100 kpc). Members are counted in 30 <= R < R_sys after clipping.
   Clip counts reported.
3. **Negative sums.** Net member mass may be negative and is kept everywhere. If M_b <= 0, v_L is taken as
   -(10 G (1 + X) |M_b| H)^(1/3) (so s < 0, ordering kept). A halo with non-positive mass (X M_b, X (M_b - M*_lens) or
   M_gas) contributes 0 to the cylinder (shape undefined); such lenses are counted and reported.
4. **Photo-z rows.** Fetched fresh by this lane's own code (all ids, not only a spot check), from
   `dr1.phz_photo_z_wide` LEFT JOIN `dr1.phz_physical_parameters_wide` on object_id, the columns of the brief; ids are the
   distinct object_ids passing the neighbour cut in the 665 EUC6R cones (hashes against EUC6R's manifest checked first),
   at most 1,000 per request, one stream, >= 1.5 s between requests, retries 10, 30, 90, 270 s, generic client name.
   Raw gz under a new folder `_external_data/wlg1r_phz_by_id/` (untracked); manifest `wlg1r_fetch_manifest.csv`
   committed. If a column named in the brief lives in the other table or is absent, the builder takes it from where it
   exists and says so. As an extra check (no gate), the builder compares its rows with the untracked
   `_external_data/wlg1_phz_by_id/` files for at least 10 cones and reports agreement.
5. **Member selection.** Cut (EUC6R's, local, NaN fails): flux_h_templfit > 5.75, spurious_flag = 0,
   det_quality_flag < 4, point_like_prob < 0.7; then a photo-z row with phz_classification = 2 and finite phz_median
   inside |phz_median - z_l| <= w (1 + z_l); the lens's own MER object (ECLIPSE `MER_object_id`) excluded by id.
   Projected R = haversine separation x D_A(z_l) (EUC6R's), at the target's z (for R fields the paired W lens's z).
6. **Member mass.** log M = phz_pp_median_stellarmass + 2 log10(D_L(z_l) / D_L(z_pp)) + Delta, z_pp =
   phz_pp_median_redshift. "No finite positive mass" means the PP mass or z_pp is missing, non-finite, or <= 0 (also -99):
   such objects get log M = log10(4 pi D_L(z_l)^2 F_H) + <log(M/L_H)> + Delta, with F_H = flux_h_templfit and <log(M/L_H)>
   the median, over every window object with a PP mass in every target of the configuration at 30 <= R < 1000 kpc, of
   [moved log M_PP - log10(4 pi D_L(z_l)^2 F_H)] (same units; no k-correction). Counted and reported.
7. **Delta.** Median over W and C lenses (the full 316 + 249 targets, before edge or coverage rules) whose ECLIPSE
   MER_object_id has a photo-z row with a finite positive PP mass and z_pp > 0, of [log M*_lens (configuration's lens scale)
   - moved log M_PP,lens]. Delta is added to every census object (members and background alike), so the background is on
   the members' scale. B-UNC recomputes Delta with uncorrected lens masses; B-RAW sets Delta = 0.
8. **Lens stars.** Primary log M*_lens = eclipse_log_survived_mass_med - log10 f_in_mask + 0.036, f from EUC17's
   `euc17_per_lens.csv` (rows P and W_B); controls: P row if present, else uncorrected (counted); L lenses (not in S):
   catalogue + 0.036, uncorrected. B-UNC: catalogue + 0.036 for all.
9. **Background.** Sigma_bg = sum of member-window masses at 600 <= R < 1000 kpc / (pi (1000^2 - 600^2)) kpc^2;
   M*_mem = sum(30 <= R < R_sys) - Sigma_bg pi (R_sys^2 - 30^2).
10. **B-STAR+.** Read as: the stellar part of M_b is M*_lens + 1.4 M*_mem (lens x 1.0, plus 0.4 x M*_mem as an
    unmeasured allowance on top of the members). The lens stars in the cylinder are unchanged.
11. **Gas.** Per lens, class level (brief section 3): G-MID W 5.2e12, C 0, L and R 0; G-0 none; G-HI W 8.3e12, C 3.0e12.
    Gas enters M_b (speed) and the cylinder only with the halo's shape normalised to M_gas inside turnaround (never a cusp).
12. **Cylinder.** LNJ1's code copied (Abel projection on LNJ1's Gauss-Legendre grid in u, r = R_E cosh u, out to
    1e6 kpc; FRZ1 halo M_ta = X M_b h / (1 - f_b), NFW at 200 x mean density with c(M) = cfac 10.14 (M / 2e12)^-0.081
    (1 + z)^-1.01, truncated at turnaround; the (z, log M_200m) table with bilinear interpolation). The gas term uses the
    r_s and r_ta of the configuration's cold halo. N-A: M_ref = M*_lens F_2D(R_E) + C_cyl(X M_b) + C_cyl(M_gas). N-B:
    M_ref = M_law,S(M*_lens) + C_cyl(X (M_b - M*_lens)) + C_cyl(M_gas), law S as EUC1's g_law with the configuration's a0.
    (A) is graded on every graded W lens as if fast. EUC8's missing mass in the fast layout, M_obs - M*_lens F_2D(R_E), is
    reported with the median ratio of the halo terms to it, beside EUC8's law excess (KA-5's quantity).
13. **Graded lenses.** Targets whose cone passes EUC6R's edge rule (N_bg >= 0.4 x median N_bg over the W, C and L
    targets, counted by this lane's code) and whose cut objects at R < 1000 kpc have photo-z rows for >= 80 % (counted).
    The same rules apply to C, L and R targets. Graded W vs C pairing: by EUC6R's pair index where both are graded.

## C. Known answers (all must pass; as the brief)

KA-1 LNJ1 stars-only speeds (catalogue + 0.036) equal `lnj1_per_lens.csv` s_model_can / s_model_alt to 1e-4 for the 316
W lenses; count s >= 1 is 1 / 0. KA-2 logM_obs_inf, logM_law_can, logM_law_alt, logM_joint_X5.41_can reproduced to
1e-3 dex. KA-3 every target's n_in, n_bg equal `euc6r_counts.csv`; paired median W - C richness +3.59 on 242 pairs
(to 0.01). KA-4 v*(0) = 668.53 / 807.93 km/s (to 0.01). KA-5 EUC8's excess_far per W lens (EUC1 footings, catalogue
mass, law S, z_s = 1100, floored at 0 as EUC8) to 1e-3 relative in the median of |relative difference|. KA-6 >= 90 % of
W and of C lenses have their own MER object in their cone with a photo-z row (each sample separately). KA-7
sqrt(G M / R_200c(M)) = (10 G M H(z))^(1/3) to 1e-9 relative on three masses (1e11, 1e13, 1e15 Msun at z 0.5).

## D. Instrument checks and twins

- **N1** blank fields R (edge and coverage rules applied), net member mass inside fixed 300 kpc at the paired W lens's z,
  primary window and scale: |median| <= 1.0e11 Msun.
- **N2** median net member mass inside 300 kpc of graded L minus that of graded C: bootstrap (L and C resampled
  independently) lower bound > 0.
- **TW-ZS (must bite).** Each graded W lens's window centred on the z of another graded W lens (permutation from
  default_rng(20261114); any fixed point swapped with its neighbour), all else (radii, mass moving, Delta) unchanged; the
  median net member mass of W inside 300 kpc must be at most half the main value (and the main value must be > 0).
  Outputs `wlg1r_MUTATE_ZS.*`; the run exits 1.
- **TW-INJ (must bite).** M_obs replaced by M_ref per lens: (A) must read FITS on both footings. `wlg1r_MUTATE_INJ.*`,
  exit 1.
- **TW-X0 (builder's own, must bite).** The cold share set to X = 0 in the amount only (M_ref = lens stars + gas halo
  term): (A) must read UNDER on both footings (the statistic must see a missing halo when one is removed); otherwise
  NOT EVALUABLE. `wlg1r_MUTATE_X0.*`, exit 1.
- Reported (no gate): TW-H (v*/2), TW-D (2 v*) speed readings; controls C through the whole pipeline with W - C pairs.

## E. Outputs

`wlg1r_fetch.py`, `wlg1r.py`, `wlg1r.out`, `wlg1r.json`, `wlg1r_per_lens.csv`, `wlg1r_fetch_manifest.csv`, twins
`wlg1r_MUTATE_{ZS,INJ,X0}.*`, `RESULT_BLIND.md`. Shared code imported read-only: EUC1's `euc1.py` (cosmology, Sersic
fractions, g_law, quadrature nodes), JNT2's `jnt2_common.py` (H, v*, v_L); LNJ1's halo and projection functions copied.
`nice -n 19`, one thread. Not pushed. No home paths, no personal names.

kappa = 1/2 FITTED; X = 5.41 FITTED; not theory closed. Adopts nothing.

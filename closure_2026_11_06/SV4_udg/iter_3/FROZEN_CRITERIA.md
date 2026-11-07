# SV4 iter_3: the large-scale external field from the whole local matter distribution (FROZEN)

Shared rules: ../FROZEN_CRITERIA.md. Committed before any script or number. AGC 114905 only: QX4 iter2 found that
no g_e in [0, 3 a0] rescues Malin 1, so Malin 1 needs no catalogue (label carried: NOT RESCUED, QX4).

## Catalogue (on disk, committed)

data_assembly/alfalfa_sdss_local_control/alfalfa_sdss.csv (ALFALFA alpha.100 x Durbala+2020, 31,503 rows). Its
fall-sky footprint contains AGC 114905. Distances are the catalogue's own (dist_mpc, e_dist_mpc; cz/70 above
6000 km/s, flow model below; a convention of the catalogue, disclosed). AGC 114905 is placed at its catalogue row
(RA 21.32708, Dec 7.36028, D 75.7 +- 2.3 Mpc), so all separations are in one distance system; the 78.7 Mpc
placement is reported beside. The galaxy's own row is excluded.

Baryonic mass per galaxy: M_i = M_* + 1.33 M_HI, M_* = the LARGEST of logms_taylor, logms_mcgaugh, logms_gswlc
that is present (0 if none), M_HI from logmhi.

## Field

- Vector estimate (reported): g_vec = | sum_i G M_i (r_i - r_0)/|r_i - r_0|^3 |, catalogue positions, d < R_max.
- Graded upper bound: g_bound = (F_c / f_sky) sum_i G M_i / d_eff,i^2 over d < R_max, with
  d_eff,i = sqrt(R_p,i^2 + max(0, |D_i - D_0| - 2 sqrt(e_i^2 + e_0^2))^2) (no cancellation, every galaxy moved as
  close as its 2 sigma distance allows, all missing sky filled at the footprint's own column).
  - f_sky: fraction of equal-area cells (RA step 2 deg x sin Dec step 2/57.3) holding >= 1 catalogue galaxy.
  - F_c = 10: baryons not in an HI-selected catalogue (gas-poor early types, hot gas, galaxies below the flux limit).
    Declared generous, not tuned: stated before computing; the F_c that would reach the window is reported.
  - R_max = 200 Mpc graded (inside the catalogue's 18,000 km/s limit); 50 and 100 Mpc reported.
  - The field from beyond R_max is taken as zero (homogeneous exterior), disclosed; the bound's growth with R_max is
    reported so the reader sees the trend.
- Readings, both graded: (N) g_bound is the Newtonian g_e that enters inside nu (QX14's reading); (M) QX4's reading,
  g_e = nu(g_bound/a0) g_bound.

## Window (what the rescue needs)

QX4 iter2's 1D estimator, g = nu(|g_N + g_e|/a0)(g_N + g_e) - nu(g_e/a0) g_e, with the exact-field factor applied:
V_model(g_e) = V_alg(g_e) x T_k, T_k = exact/algebraic at g_e = 0 from this lane's KA0 solve. The window is the set of
g_e (grid 1e-4 to 3 a0, 2000 log steps) with p >= 0.05. QX4's algebraic window (0.0756-0.2909 / 0.0768-0.2925 a0)
is reproduced beside (KA3, 2 % on the edges).

## Labels (per footing, per reading)

- NOT RESCUED (field excluded): g_bound < the window's lower edge.
- RESCUED is not available from a bound: if g_bound >= the lower edge, the label is NOT EVALUABLE (bound too loose)
  unless g_vec itself lies in the window, which would be RESCUED (field supplied).

MUTATE: a planted point mass of 2 x M_req (QX14: 1.0e12 Msun canonical, 1.8e12 alt) at QX14's d_min (141 / 172 kpc)
added to the catalogue must lift g_vec into or above the window (label flips away from NOT RESCUED). Outputs to
iter3_MUTATE.*.

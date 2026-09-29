# N4 -- the holographic count coefficient c' (pre-registration)

Written 2026-09-28 BEFORE `n4_holographic_count.py` was run (nothing in this lane has been computed when this is written).
Target: 1/alpha = 137.035999177 (Thomson limit). Relation tested: N^2 = c' S_dS gives 1/alpha = 12 pi c' (lane C: N_max^2 = 1/(4 alpha x), S_dS = 3 pi/x,
x = Lambda l_P^2). Needed (inverse map, not a hit): c' = 1/(12 pi alpha) = 3.635. Planck-scale alternative target: 1/alpha_em(m_P) = 104.94 (one loop, read from
ALPHA_CHAIN_STATUS.md; the script recomputes it as a cross-check with the corrected b_Y = (5/3) b_1 = 41/6).

## What I read (declared)
Read IN FULL: ALPHA_CHAIN_STATUS.md; C_holographic_species/c3_holographic_charge_equalities.py; A_wgc_extremal/a1_rn_ds_special_points.py; D_calibration_bar/alpha_bar_checker.py
(assess/selftest logic) and D_PREREGISTRATION.md (first 70 lines); first 60 lines of a2_dirac_extremal_and_handles.py; C0_PREREGISTRATION.md (truncated in the middle: the
P4 section was read). NOT read: lanes B, E-K scripts, lane M. No external literature is read or cited in this lane; the RN-dS geometry is derived from the metric function in c3.

## Hypotheses
H1 (structural theorem). The classical Einstein-Maxwell-Lambda solution, and every thermodynamic or holographic quantity built from it (M, S, T, Phi*Q, Bekenstein
   E*R, horizon radii, dS_2 curvature), depends on (alpha, N) only through Q_geo^2 = alpha N^2 l_P^2. Therefore NO purely geometric or thermodynamic relation can separate alpha
   from the integer N; any relation that fixes alpha needs an extra COUNT coefficient k (N^2 = k S) that geometry does not supply. Consequence: alpha = (pure geometric number)/(k),
   so 'c' forced by geometry' is not available; c' is exactly the object that has to come from non-geometric counting physics.
H2 (range). A relation N^p = k S^q gives alpha proportional to x^(2q/p - 1); only p = 2q gives O(1/100). The magnetic dual (n_max^2 = alpha/x) gives alpha = 3 pi c'_m, out of range
   for every c'_m >= 1/(4 pi); flat extremal N^2 = k S_ext gives 1/alpha = pi k, out of range unless k = 43.6.
H3 (enumeration). No enumerated c' clears lane D's bar. Expected: all misses > 1e-2 (relative, in 1/alpha). Some values may fall within a factor 2 of 3.635; if so that is a
   statement about the density of 'natural' numbers near 3.6, not evidence.
H4 (choice count). No c' in the list is forced without at least three declared choices (entropy reference Y, counting unit u, coefficient k); the least-choice candidate
   (nats, S_dS, k = 1, c' = 1, 1/alpha = 12 pi = 37.7) misses by a factor 3.6.
H5 (inequality reading). N_max^2 <= S_dS (c' <= 1) is VIOLATED by the measured alpha (real c' = 3.635); N_max^2 <= A_dS/l_P^2 = 4 S_dS is satisfied with 10% margin (a bound, not a value).

## Exact derivations (sympy) that must reproduce
G1 ultracold (triple root) point: Q_geo^2 Lambda = 1/4, r0^2 Lambda = 1/2, M_g^2 Lambda = 2/9, Phi_H = Q_geo/r0 = 1/sqrt 2, z^2 = Q^2/M^2 = 9/8, f''(r0) = 0 (dS_2 radius infinite:
   the near-horizon geometry is R^{1,1} x S^2).
G2 entropies: S_uc = pi r0^2/l_P^2 = pi/(2x) = S_dS/6; S_Bek = 2 pi M_g r0 / l_P^2 = 2 pi/(3x) = (2/9) S_dS; Coulomb identity S_uc = 2 pi (Phi Q) r0/l_P^2 (an alpha-free identity, because
   both sides are proportional to alpha N^2).
G3 magnetic dual: n_max^2 = alpha/x; N_max n_max = 1/(2x) (alpha-free); flat extremal S_ext = pi alpha N^2.
G4 scaling invariance (H1): rescaling N -> lam N, alpha -> alpha/lam^2 leaves the metric function and every quantity above unchanged.

## Enumerated candidates (fixed now; nothing is added after the run)
F1 electric dS count, scored family, 45 trials: N_max^2 = k * u * S_Y, i.e. c' = k u (S_Y/S_dS), with
   Y in {S_dS, S_uc, 2 S_uc (BH + cosmological horizon, Gibbons-Hawking sum), 3 S_uc (three coincident roots), S_Bek (E = M_uc, R = r0)}  (5)
   u in {1 (nats), 1/ln 2 (bits), 4 (Planck cells A/l_P^2)}  (3)
   k in {1/2, 1, 2}  (equipartition, saturation, doubling e.g. two photon polarisations)  (3)
   => 45 trials (fewer distinct c'). Each is reported with c', 1/alpha_pred = 12 pi c', miss vs 137.036 and vs 104.94, in range or not.
F2 magnetic dual (45, same grid): alpha_pred = 3 pi c'; range test only (not scored: all out of range).
F3 flat extremal (9): 1/alpha = pi k u; range test only.
F4 alpha-free identities (N_max n_max = 1/(2x); Coulomb-Bekenstein): reported as null, not scored.
F5 power-law exponents (p, q) in {1,2,3,4}^2: alpha exponent table, range test.
Total enumerated: 45 + 45 + 9 + 16 exponent pairs; the scored trial count for the bar is 45 (family size), with n_targets = 2 (Thomson and Planck-scale alpha), 0 fitted reals.
The horizon scale (Hubble radius) makes the IR coupling the natural target: the Coulomb field at r0 ~ 1e26 m is at momentum far below m_e, so the relevant alpha is the Thomson one;
the Planck-scale value is scored only as the second target.

## Diagnostic (declared): density of natural c' near 3.635
D1 the number of distinct rationals p/q with 1 <= p, q <= 12 within a factor 2, within 10%, and within 1% of c'_needed; and of c' values in F1 within a factor 2 and 10%.

## Pass / fail criteria
* Question 'is a c' forced?': PASS-forced only if some c' is reached with NO declared choice AND clears the bar. Expected: FAIL.
* Bar (lane D): P < 1e-3 after look-elsewhere (assess with size = 45, n_targets = 2), miss <= 5e-10, zero fitted reals, scale stated. Reported per candidate; any single clear would be
  reported as a numerical match only, still needing a forced derivation of k, u, Y.
* Controls (in the script): positive control: a hypothetical exact c' (miss 1e-11, size 45) clears the bar (shows the bar can be passed); the inverse-map c' = 3.6349 is flagged
  inverse-map and is not scored as a hit. MUTATE control: invoke `python3 n4_holographic_count.py --mutate` (the ONLY trigger; argv `--mutate`): it replaces the triple-root charge
  Q^2 = 1/(4 Lambda) by 1/(2 Lambda) and the S_uc = S_dS/6 ratio by 1/3; the symbolic checks G1/G2 must FAIL and the script exit 1.
* Real run must exit 0 and write n4_holographic_count.out; the mutated run writes n4_holographic_count_MUTATE.out.

## Amendment 1 (2026-09-28, after the first run; visible, nothing loosened on the physics)
The first run exited 1 because three of my own check statements were wrong as written (not because a physics result changed):
1. G1h: `solve(dM^2Lambda/dy = 0)` also returns y = 3/2 (outside the physical range 0 < y <= 1); the check is restricted to 0 < y <= 1.
2. F2: I pre-registered 'out of range for every c'_m >= 1/(4 pi)', but the grid contains c'_m down to 1/12, giving alpha_pred = 3 pi c'_m as low as 0.785. The threshold is restated
   as 'alpha_pred >= 0.1' (at least 13x the measured 7.3e-3); the H2 conclusion (the magnetic dual is out of range) is unchanged.
3. D1: my check demanded '> 5 rationals within 10%'; that count was a guess. The actual numbers (19 of 91 within a factor 2, 3 within 10%, 1 within 1%) are reported without a pass/fail
   expectation. D1 is a report-only diagnostic.
Also replaced the vacuous G3d (quoted) by a computed check (flat extremal r_+ = Q_geo). The F1 grid, the bar settings, the targets and the MUTATE trigger are unchanged.

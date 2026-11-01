# BOLTZ1_covariant_closure: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Source: queue item 11, an outside AI's scrambled text. A claim to test, not a method. kappa = 1/2 FITTED, unused. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework. v3s is not reopened: its khronon, J sector and K bound on mu_K are not used as this lane's theory; Q6's arithmetic for a stiff term is used only as a check.

**Record check already done (read, not rerun):** RF5 (patched CLASS: rho_c = rho_c0 a^-3 S(a), tanh in ln a, width 0.05, fed by a w = -1 reservoir, delta Q = 0; window z_on 3e4 to 1e6, grid top); X34; X22; Q6, Q7; DR2 (P(X) dust limit, caustics, c_s^2 = (Q-1)/Q); ER2; X14; O1. No lane states whether RF5's turn-on family is inside P(X), and no lane ran RF5's harness with the turn-on removed. RF5 names the gap: "the frozen grid stops at the edge, and its best cell is the one that failed G0".

**Not blind.** Known beforehand: RF5's whole table, forest 420/327 at z_on 1e6, G0 failing narrowly, P1D4's V-hiz 433/327, Q6's mu_K,BBN 1.84e8 h/Mpc.
**Expectation on record:** Part A: no turn-on in P(X). Part B: ceilings only. Part C: plik, BAO, SN, shear as the 1e6 cell, forest near 400-420, G0 still fails.

## Part A. Is RF5's turn-on inside shift-symmetric P(X)?
Rule: single field, P(X), healthy branch rho + P >= 0, P_X > 0, c_s^2 = dP/drho >= 0. Exact: d(rho a^3)/dln a = -3 P a^3. Treat RF5's cold + reservoir as the one fluid P(X) would have to be: rho_u = rho_c + rho_res, P_u = -rho_res.
- S1 sympy: c_s^2 = P_X/(P_X + 2X P_XX) equals dP/drho on the branch; continuity identity above.
- S2 sympy: for any S(ln a) with S' > 0, the unified c_s^2 = -(dlnS/dln a)/3.
- N1 numeric: X34's S at all 14 RF5 grid z_on; the max of c_s^2 across the step, and Delta P / Delta rho across it.
Label **NO TURN-ON IN P(X)** if S1, S2 residuals are 0 and c_s^2 < 0 at every point of the step on every grid z_on. Otherwise **TURN-ON ALLOWED**.

## Part B. Stream crossing against growth: c_s^2 ceilings in the one-number family
Family: K = mu^2 (Q-1)^2 (DR2 S3b), normalised as S = (c^3/16 pi G) Int sqrt(-g) 2K. No a0. mu is not fitted; only bounds are read.
- S3 sympy: for Q - 1 << 1, c_s = sqrt(4 pi G rho)/mu (c = 1 inside mu), so proper Jeans wavenumber = mu, and the n = 1 polytrope radius is R = pi/mu.
- Ceilings on c_s (floors on mu), each from the record: BBN (Q6's arithmetic, Delta N_eff,equiv(1 MeV) <= 0.5); forest c_s <= 6 km/s at z = 3 (X22's lower number); crossing: R = pi/mu <= epsilon of the lowest zoom, 154 pc at 1e8 (OP1's epsilon(M) = 714 pc (M/1e10)^(1/3)).
- Reported only, no line: c_s at zoom densities and RF5's window translated through the density map.
Label **CEILINGS ONLY, NO PINCER** if mu = 100 mu_BBN meets every line above and none of them is a floor on c_s. **PINCER** if a floor on c_s from the record crosses a ceiling.
Label **PRESSURE CORE EXCLUDED IN THIS FAMILY** if R(mu_BBN) < 154 pc. This family only. DBI (Q7) removes the BBN line, so that form is a different selected Lagrangian; not graded.
No CLASS run is needed for Part B. A strict statement of crossing by a single-valued phi is DR2/X14's, cited, not redone.

## Part C. The dust limit through RF5's own harness: the z_on = infinity cell
The mu -> infinity P(X) has no z_on and no new number. Its linear equations in synchronous comoving gauge are CLASS's w = 0, c_s = 0 cold equations. Run: RF5's binary with the turn-on off. Driver imports rf5.py read-only; own cells dir in this lane, own work dir outside the repo. rf5.py's frozen settings unchanged: free omega_b, omega_c, 100theta_s, lnA, n_s, tau, w0, wa, A_planck; start at the 1e6 best fit; same steering; same shear scale cut (RF5's committed file, not recomputed); same forest recipe, 5 z, stride 4, seed 0, 2 % floor.
Lines (RF5's, unchanged): G-CMB p >= 1e-3 on 605 dof; G-BAO p >= 1e-3 on 13; G-SN p >= 1e-3 on n-1; G-SHEAR p >= 1e-3 on n_keep - 1; G-A0 CFG689's band at z 1, 1.5, 2.33. G-S: S - S_min <= 25, S_min = min(2324.0347, this cell's S).
G0: joint p >= 0.01 on 327 dof and each z p >= 1e-3.
Labels:
- **DUST LIMIT PASSES GATES, FOREST NOT DIAGNOSTIC** if the gates pass, G0 fails.
- **DUST LIMIT PASSES GATES, FOREST G0 NOW PASSES** if G0 passes. This is only a pointer: RF5's frozen verdict is not edited, and the consequence for lower z_on cells goes to the owner.
- **DUST LIMIT FAILS <gate>** if any gate fails.
- A pass here is "early dust", X34's reading. It says nothing about galaxies. No Delta chi2 to any LCDM reference.

## Overall answer label
**NEEDS A SELECTED LAGRANGIAN** unless Part A is TURN-ON ALLOWED, Part B is PINCER, or Part C changes a gate. The report then names the decision.

## Checks (all required, else no verdict)
- K1 harness: Lik at RF5's committed 1e6 best fit, turn-on at 1e6, reproduces its plik, BAO, SN within |d| <= 1e-6, or, if CLASS's run-to-run noise is larger, stated and held to |d| <= 1e-3 (tool check).
- K2 forest: forest_profile on RF5's table R1_1000000 z 3.6 reproduces 87.35939598984058 within 1e-6.
- K3 binary: patched binary off against vanilla at the same parameters, max |dC/C| <= 1e-4, TT, EE, phiphi (RF5's K1 line).
- K4 BBN: this lane's arithmetic reproduces Q6's mu_K,BBN from its JSON, relative |d| <= 1e-6, with Q6's parameters.
- K5 sympy residuals 0 (S1-S3).
- K6 energy identity of the unified fluid on X34's S: numeric d rho_u/dln a + 3(rho_u + P_u) relative <= 1e-6.
MUTATE (separate outputs, BOLTZ1_MUTATE=1, must fail): m1 reservoir pressure sign flipped, S2 or N1 must fail; m2 stiff term a^-3 not a^-6, K4 must fail; m3 turn-on left on at 1e4 in K3's run, K3 must fail.

Compute: one driver, at most 3 CLASS children (RF5's NCLASS), nice 15, one thread each; SIGTERM checkpoint via RF5's own Preempted path; rerun resumes. Local commit only.

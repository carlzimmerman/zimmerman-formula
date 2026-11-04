# A19: SIDM beyond one cross-section, and warm dark matter (frozen before any number)

Rival language, adopts nothing, never feeds anything outside this folder. kappa = 1/2 FITTED; not theory closed. Script `scripts/recipe21.py`, output `scripts/recipe21.out`. Written before the script was run.

## Common machinery

- Baryons, sample, law and grade from `scripts/lib.py` (171 SPARC galaxies, Y_disk 0.5, Y_bul 0.7).
- Halo: M200 = m200_of(M_*, dn) (Moster SHMR in lib), c = cflat(M200, dc, 0) x (Sigma_b/100 Msun pc^-2)^s_c with Sigma_b = M_b/R_d^2 (as A16 N2), times the WDM factor in (d). Dark mass (1 - f_b) NFW, f_b = min(M_b/M200, 0.5), as A15 U3.
- SIDM core, as A15 U3 (Kaplinghat et al. 2014 style): isothermal Jeans inside r1 in the baryon (spherical, from v_bar) plus dark potential, rho and M matched to the NFW at r1; r1 from rho_NFW(r1) <sigma v>/m t = 1, t = 10 Gyr. <sigma v> over the relative-velocity Maxwellian of two particles of 1D dispersion sigma0 (mean relative speed 4 sigma0/sqrt(pi), the A15 form).
- Fast solver (A15's per-galaxy least-squares is too slow for fits): per galaxy a vectorised grid of sigma0 (28 values, 0.25 to 1.5 V_max) by rho0 (40 values, 0 to 5 dex above rho_NFW(r1)), 100 log radii from 1e-3 r1 to r1, the same Euler step as A15. For each sigma0 the first rho0 with rho(r1) = rho_NFW(r1) is taken (interpolated), then sigma0 where M(r1) = M_NFW(r1); if several, the root with the lowest rho0 (low-density branch); if none, the sigma0 of smallest mass mismatch, counted as unmatched (|log mismatch| > 0.03) and printed.
- **Control C0, frozen gate on the code:** fast solver, base halo, sigma/m = 1 cm^2/g constant, must reproduce A15 U3 (rms to law 0.1212) within 0.01 dex. If it fails, the solver is fixed before any model row is read, and disclosed here.

## Models, knobs, bounds

- (a) velocity-dependent SIDM, sigma/m = s0/(1 + (v/w)^4) on the relative speed v. Knobs log10 s0 [cm^2/g] in [-1, 2], log10 w [km/s] in [1, 3]. 2 knobs.
- (b) (a) plus SHMR normalisation dn in [-0.3, 0.3], c normalisation dc in [-0.3, 0.3] dex, compactness exponent s_c in [-0.5, 0.5]. 5 knobs.
- (c) Ren et al. 2019 style: per-galaxy dlog M200 in [-0.6, 0.6] (2 sigma of 0.3 dex) and dlog c in [-0.22, 0.22] (2 sigma of 0.11 dex) about the SHMR and Diemer19; one global constant sigma/m chosen from {0.5, 1, 3, 10} cm^2/g by all-galaxy rms to law. Count 2 x 171 + 1 = 343 parameters (Ren et al. also free Y per galaxy; not done here, so this is less freedom than theirs).
- (d) warm dark matter: c_WDM/c_CDM = (1 + gamma1 M_hm/M200)^(-gamma2). d1: Schneider et al. 2012 coefficients gamma1 = 15, gamma2 = 0.3; d1b: Bose et al. 2016 (COCO) gamma1 = 60, gamma2 = 0.17. Both coefficient pairs FROM MEMORY; a web search found the papers (arXiv 1112.0330, 1507.01998) but not the numbers, so they are unverified. Knob log10 M_hm [Msun] in [6, 12], NFW, no core: 1 knob. d2: d1 plus a constant sigma/m core, log10 sigma/m in [-1, 2]: 2 knobs. The WDM drop in halo abundance (which would move the SHMR) is not modelled, stated.

Fits: scipy least_squares on log g against the law over all points, bounded, diff_step 0.05, at most 25 evaluations for (a), 30 for (b), 2 starts for (a) and (b); bounded scalar search for d1. Per-galaxy (c): least_squares, at most 20 evaluations per galaxy.

## Gates (every model)

- G-E: lib.grade E1 <= 0.02, E2 <= 0.04, E3 <= 0.02 on all-data tuning.
- G-H: holdout, tune on GS[::2], unseen rms to law on GS[1::2] <= 0.025 dex. For (c) the per-galaxy parameters cannot move to unseen galaxies: gated reading = sigma/m chosen on GS[::2], GS[1::2] graded at the prior centre (dlogM = dlogc = 0); reported but not gated: GS[1::2] refitted per galaxy (not unseen), and a radius holdout (per-galaxy fit on odd radii, graded on even radii).
- Reported: rms to observed, knob count, knobs at bound (within 1e-3 of the range), unmatched-core count.
- EXACT only if G-E and G-H all pass.

## Acceleration scales (reported for each model where it exists)

- K1 core acceleration per galaxy g_c = sigma0^2/r1: median, rms dex over galaxies, kappa_eff = median/(c sqrt(G rho_DE)), rho_DE = Ode0 RHOC.
- K2 cross-section scale a_x = G/(sigma/m) (the core condition rho(r1) <sigma v> t / m = 1 is G rho1 v t = a_x): at the fitted constant sigma/m, and at s0 and at sigma/m(v = w) for (a), (b). Prefactor freedom (2 pi etc.) stated, not used.
- K3 a_w = w/t for velocity-dependent fits, t = 10 Gyr.
- K4 WDM: g200 = G M_hm/R200(M_hm)^2 at the fitted half-mode mass.
- Gate for each: kappa_eff within 0.05 dex of 0.5; z evolution a(z)/a(0) at z = 1, 1.5, 2.33 in [0.76,1.03], [0.71,1.12], [0.33,1.21]. K2 is a constant of the particle (ratio 1); K3 taken at t = age(z) capped at 10 Gyr; K1 for a dark-only halo at the median SPARC M200 with Diemer19 c(z), rho_c(z), t = min(10 Gyr, age(z)); K4 at fixed M_hm with rho_c(z).
- A scale that passes kappa_eff only by a cross-section chosen near G/(0.5 c sqrt(G rho_DE)) (about 7 cm^2/g) is a hand coincidence: no SIDM process links sigma/m to rho_DE.

## Pre-run change, before any graded number (compute budget)

A timing test on 20 galaxies (no grade, no model number read) gave 5.7 s per full-sample evaluation at the 28 x 40 grid, which with the evaluation counts above would exceed the 25-minute limit. Changed before the first run: grid 20 sigma0 x 28 rho0 (same ranges); one start for (a) (log s0 0, log w 2) and one for (b) (from (a)'s fit, halo knobs 0); max_nfev 12 for (a), (b), d2, 15 for d1, 8 for holdout re-tunes and 8 per galaxy in (c) (scipy counts these without the Jacobian evaluations). Control C0 still gates the coarser grid against A15.

## Expected in advance

(a) E1 about 0.10 to 0.12, FAIL. (b) about 0.07 to 0.09, FAIL. (c) improves a lot, about 0.03 to 0.05, still fails E1 or E2, and the gated holdout fails at about the (a) level. (d) about 0.12 to 0.15, FAIL; WDM lowers c and so the inner pull, which the law does not want at low mass. K1 spreads over galaxies (> 0.1 dex) and rises with z; K2 is constant, so it passes the z band by construction, and its kappa_eff lands at 0.5 only if the fitted sigma/m happens to be near 7 cm^2/g; K3 and K4 far below a0. No model EXACT.

## A19 BUG, after the first run's C0 line (no model number was printed)

The first run is kept as `scripts/recipe21_before_fix.out`. C0 passed its frozen rms gate (0.1218 against 0.1212) by coincidence: its bins had the opposite sign to A15 U3 (mean residual -0.05 against A15's +0.04), and 160 of 171 cores were unmatched. Cause: the grid-interpolated root of the two matching conditions is inaccurate where rho(r1) is not monotonic in rho0 (mismatch 0.2 to 0.35 in ln on the galaxies checked). The run was stopped before any model row. Fix: the grid point with the smallest squared mismatch (lowest rho0 among those under 0.05, the low-density branch) starts a damped Newton solve of both conditions on (ln rho0, ln sigma0), at most 12 steps, stop at 1e-3. On five galaxies checked against A15's `sidm()` the fixed solver gives the same r1 to 0.02 % and the same accelerations to 0.000 dex. Added after seeing the bug, reported but not a frozen gate: the C0 mean residual and the worst bin difference to A15 U3's printed bins. Budgets and grid stay as the pre-run change.

## A19 VERDICT on the fixed run (`scripts/recipe21.out`, 552 s): NOT EXACT, no model

| model | knobs | E1 rms to law | E2 p95 | E3 worst bin | holdout unseen | rms to observed | at bound |
|---|---|---|---|---|---|---|---|
| C0 control, sigma/m 1 constant | 0 | 0.1200 (A15 0.1212) | 0.2102 | 0.0687 | - | 0.2124 | - |
| (a) v-dep SIDM, s0 1.17 cm^2/g, w 279 km/s | 2 | 0.1224 | 0.2307 | 0.0632 | 0.1124 | 0.2096 | none |
| (b) (a) + dn, dc, s_c | 5 | 0.0797 | 0.1621 | 0.0220 | 0.0794 | 0.2018 | dn at +0.3 |
| (c) per-galaxy M200, c; sigma/m 0.5 | 343 | 0.0487 | 0.0988 | 0.0247 | 0.1096 at prior centre (gated); 0.0460 refitted, 0.0566 radius holdout (not gated) | 0.1958 | 77 of 342 per-galaxy |
| (d1) WDM S12, log M_hm 9.91 | 1 | 0.1195 | 0.2355 | 0.0551 | 0.1067 | 0.2191 | none |
| (d1) WDM B16, log M_hm 9.83 | 1 | 0.1183 | 0.2286 | 0.0477 | 0.1067 | 0.2192 | none |
| (d2) WDM S12 + SIDM 0.548 | 2 | 0.1162 | 0.2161 | 0.0476 | 0.1021 | 0.2097 | none |

Disclosures: (a) lands above the constant-cross-section control it nests (0.1224 against 0.1200), so its 12-evaluation, one-start fit stopped short; the true (a) optimum is at most about 0.120, which changes no gate. (c)'s chosen sigma/m is the lowest of the four allowed values, so the optimum may sit below 0.5; 0.5 to 1 differ by 0.003 dex. (c) has fewer per-galaxy knobs than Ren et al. (no per-galaxy Y). WDM coefficients from memory, unverified; the two sets give the same grade to 0.001 to 0.007 dex.

Acceleration scales: none ties to rho_DE. K1 core sigma0^2/r1: kappa_eff 0.095 to 0.191, spread 0.18 to 0.67 dex over galaxies, rising 1.25 to 1.33x by z 1 and 1.9 to 2.1x by z 2.33 (fails the band). K2 G/(sigma/m): constant, so the z band passes by construction, but kappa_eff 3.0 to 7.1 at the fitted cross-sections (0.5 to 1.2 cm^2/g); it would need about 7 cm^2/g, a hand choice no SIDM process ties to rho_DE. K3 w/t: kappa_eff 0.002 to 0.005, and grows 1.7 to 3.6x by z. K4 g200(M_hm): kappa_eff about 0.003, grows 2.2 to 5.3x. Expected in advance mostly held; (c) landed at 0.049, at the edge of the expected 0.03 to 0.05. Rival language; passing would show freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

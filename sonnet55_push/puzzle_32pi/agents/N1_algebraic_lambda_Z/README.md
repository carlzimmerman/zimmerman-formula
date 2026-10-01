# N1: the algebraic-in-Lambda branch (Nariai-type vacuum accelerations) -- a fair, principle-first test

## Bottom line (verdict: NOTHING NEW as a derivation; one DISCRIMINATING-STYLE structural result; kappa = 1/2 stays FITTED)
1. The only menu member that matches the data, a0 = G M_N/L^2 = c H_Lambda/(3 sqrt3) (Z = 5.196, a0^2 = c^4 Lambda/81), evaluates the Nariai mass's field at the radius L, which is NOT in the static patch of that mass's own geometry (f(L) < 0; at M_N the static patch is empty). Every radius that belongs to the M_N geometry (horizon, cosmological horizon, photon sphere, zero-force radius: all coincide at L/sqrt3, proved) gives Z = sqrt3 = 1.73, excluded at > 7 sigma. So the match uses a chosen radius and is NOT promotable.
2. Data: on the rho_Lambda footing N is +0.4 sigma (ensemble E) against +1.3 sigma for the framework's 5.789 (likelihood ratio 2.1, i.e. nothing); but the sign flips with the interpolating function: under Upsilon-free RAR/simple (which the data prefer) N is -2.1 sigma and Z = 5.789 / 2 pi fit (-0.85 / +0.15 sigma), LR N:F = 0.14. No candidate is within 1 sigma under all four kernels, on either footing.
3. Look-elsewhere: with a menu of 8 distinct Z values the chance that one lies as close to the data as N does is 28% (Monte Carlo = analytic); the integers n = 8 and 9 in a0 = c^2 sqrt(Lambda)/n both fit at 1 sigma, and 6 of 138 simple radical decoys do.
4. Differing consequences are small: Omega_Lambda from a0 = 0.73 +- 0.08 (record a0) versus 0.906 +- 0.10 for the framework (observed 0.685 +- 0.007; 0.56 vs 2.2 sigma with the record's quoted 5.4% error, 0.44 vs 1.5 with 8.2%); predicted a0 at the Planck footing 1.043e-10 versus 0.936e-10 (11.4% apart, about 4% in the wide-binary boost). a0(z) is flat in both. No cutoff for clusters (M_N = 2.2e22 solar masses).

## What I did
`PREDECLARED.md` (sha256 7e0a8008...5227, file `PREDECLARED.sha256`) fixes the menu A1-A12, a stated principle and self-consistency test for each, decoys D1-D3 and the promotion rule, before any script ran. Disclosure: I knew lane V's N offsets (+0.4 sigma Lambda footing) and expected the Nariai coincidences; the A8 (exact stable-orbit threshold) number was not known to me. `run_all.sh` reruns everything (exit 0). n01: 26/26 checks, n02: 13/13; controls and mutations (M_N/2 breaks the coincidences and moves A1's Z to 6 sqrt3; planted-truth and far-menu controls for the decoy machinery; Lambda->0 limit ISCO = 6M; analytic = MC). The script order: `n01_menu.py` (sympy exact Z, geometry), `n02_confront.py` (data, LRs, kernels, Omega_Lambda, decoys). Data numbers are lane V's (read, not refit); I fixed one thing in n01 during the run (a bad mass grid for the orbit scan, then replaced by the exact double root).

## (1) The menu and its principles (Z = c H_Lambda / a0; all exact)
| id | acceleration | Z | principle (declared) and its problem |
|---|---|---|---|
| A1 | G M_N/L^2 (r = L) | 3 sqrt3 = 5.196 | field of the largest static mass at the dS-horizon distance. Geometry inconsistent: r = L lies beyond the M_N geometry's own horizons; chosen radius. |
| A2-A5 | G M_N/r^2 at r_b = r_c = r_ph = r_0 = L/sqrt3 (also = Lambda repulsion there) | sqrt3 = 1.732 | same principle with a radius of the same solution. All four radii coincide exactly (proved); the cost is Z = A1/3. |
| A6 | c^4/(4 G M_N) (Schwarzschild kappa of M_N) | 4/(3 sqrt3) = 0.770 | flat-space horizon of a Lambda-bound mass. |
| A7 | G M_N/(6 G M_N)^2 (Schwarzschild ISCO) | 4 sqrt3 = 6.928 | Lambda ignored; M_N has no orbits at all. On the Lambda footing +2.8 sigma (E). |
| A8 | exact SdS: largest mass with a stable circular orbit, field there | sqrt3/2 = 0.866 | M_crit = (2 sqrt3/225) L = 0.08 M_N at r = L/(5 sqrt3) (double root of the stability polynomial, verified by bisection); a genuine existence threshold but a different scale. |
| A9/A10 | kappa at Nariai: f-normalised 0; Bousso-Hawking sqrt3 H (= 1/dS2 radius) | infinite / 1/sqrt3 | degenerate horizon. |
| A11 | vacuum mass (4 pi/3) rho_Lambda L^3 = L/2 field at L; Lambda repulsion r/L^2 at L | 2; 1 | the kappa = 1 and Hubble-ball values. |
| A12 | extremum of static-observer proper acceleration | none | strictly monotone between horizons (M = 0.02..0.19): no maximal-force point exists in SdS; removed. |
Structural result (proved, n01): A1 = A2/3 exactly because (r_N/L)^2 = 1/3. The number 3 sqrt3 survives only by pairing the Nariai mass (a property of the hole) with the pure-dS radius (a property of the empty universe), two objects that cannot coexist. I cannot find a principle that makes ordinary-galaxy accelerations equal to that mixed quantity; "largest static mass at the Hubble distance" gives a field, not a reason the MOND transition of a 1e11 solar-mass disc sits there. So A1 has data compatibility but no consistent principle; A2-A8 have consistent principles and fail the data.

## (2) Data (lane V's a0, both footings; + = candidate above the data)
| scenario (a0 in 1e-10, error) | Z_data Lam / tot | F 5.789 | 6 | 2 pi | N 5.196 | LR N:F (Lam) |
|---|---|---|---|---|---|---|
| E ensemble (1.097, 12.2%) | 4.94 / 5.97 | +1.30 / -0.25 | +1.59 / +0.04 | +1.97 / +0.42 | +0.41 / -1.13 | 2.1 |
| record quoted (1.0766, 5.44%) | 5.03 / 6.08 | +2.53 / -0.90 | +3.18 / -0.25 | +4.02 / +0.59 | +0.57 / -2.87 | 21 |
| record + systematics (1.081, 16.1%) | 5.01 / 6.06 | +0.89 / -0.28 | +1.11 | +1.40 | +0.22 / -0.95 | 1.5 |
| Upsilon-free alpha1 (1.083, 8.2%) | 5.00 / 6.05 | +1.77 / -0.53 | +2.20 / -0.09 | +2.76 / +0.47 | +0.46 / -1.84 | 4.3 |
| Upsilon-free RAR (0.873, 8.2%) | 6.21 / 7.50 | -0.85 / -3.15 | -0.41 / -2.71 | +0.15 / -2.15 | -2.16 / -4.46 | 0.14 |
| Upsilon-free simple (0.881) | 6.15 / 7.43 | -0.74 / -3.04 | -0.30 | +0.26 | -2.05 / -4.35 | 0.16 |
| Upsilon-free standard (1.117) | 4.85 / 5.86 | +2.14 / -0.15 | +2.57 / +0.28 | +3.13 / +0.84 | +0.83 / -1.47 | 7.0 |
| MLS16 RAR fixed Upsilon (1.20, 20.1%) | 4.52 / 5.46 | +1.23 | +1.41 | +1.64 | +0.70 / -0.24 | 1.7 |
(Lam/tot entries where given; s_tot includes H0 0.74% and, on Lam, Omega_Lambda 0.5%; H0 = 73 moves E/Lam to N -0.24, F +0.64.) LRs are point-hypothesis ratios with no free parameter; the record-quoted 5.44% row uses the crude clustered error that lane V showed underestimates (8.2% galaxy bootstrap, 16% with measured systematics), so its LR = 21 is not to be quoted. N is natural only on the Lambda footing (it depends on Lambda alone); on the total footing it is -1.1 to -4.5 sigma. Stable across all four kernels: nothing (no candidate has |z| < 1, and none |z| < 2, for all four kernels on either footing). The Z-ordering is decided by the kernel, which is itself decided by the data at about 3 sigma in favour of RAR (lane V), under which N loses and 2 pi, 6, 5.789 win.
False-match control: the 8 distinct menu values are log-spread from 0.58 to 6.9; P(some value within |z| <= 0.41 of the data) = 0.283 (MC 200k menus = analytic 0.282); the principle-free integer family a0 = c^2 sqrt(Lambda)/n fits at n = 8 (-0.55) and n = 9 (+0.41) (and 10 at +1.3, the framework's n = 10.03); 6 of 138 sqrt-grammar decoys lie within 1 sigma. An 0.4 sigma agreement among ~10 candidates is therefore ordinary.

## (3) Consequences that differ from 32 pi
- Lambda form: N is a0^2 = c^4 Lambda/81 (pi-free); in rho form a0^2/(G rho_Lambda) = 8 pi/81 (pi appears). The framework is the reverse: a0^2 = c^4 Lambda/(32 pi) carries pi in the Lambda form and is pi-free (4) in the rho form. Both are the same kind of coefficient claim; which variable is 'natural' is not settled by any computation here. (Lindemann, lanes L and X3: an algebraic-in-Lambda principle can only give an algebraic Z, so sqrt(32 pi/3) is unreachable on this branch, and 3 sqrt3 unreachable from the framework's.)
- Omega_Lambda = Z^2 (a0/cH0)^2: N 0.758 +- 0.185 (E), 0.730 +- 0.080 (record a0), 0.739 +- 0.122 (alpha1 8.2%), 0.48 (RAR); framework 0.940 / 0.906 / 0.917 / 0.596. Observed 0.685 +- 0.007. Errors are a0's (twice the relative error) plus H0. Not discriminating at the present a0 precision; sign flips with the kernel as lane V found.
- a0 at the observed Omega_Lambda, Planck H0: N 1.043e-10, F 0.936e-10, 6: 0.903, 2 pi: 0.863 (H0 = 73: 1.130 / 1.014 / 0.978 / 0.934).
- a0(z): N depends on Lambda only, hence FLAT, the same as the framework (no discrimination).
- Wide binaries: a0 differs by 11.4%, the boost by about 4% at y ~ 0.3 (lane V sensitivity 0.4); below present and likely DR4 control of the interpolating function and external field.
- Solar system / EFE: no change in structure; the acceleration scale differs by 11%.
- Mass cutoff: M_N = c^2 L/(3 sqrt3 G) = 2.2e22 solar masses (Planck, Omega_L = 0.685), 7 orders above clusters; a Nariai-type bound does NOT cut off MOND halos or explain the cluster scale (lane V: cluster g ~ 17x a0).

## (4) Honest caveats
- Z depends on footing (a factor sqrt(Omega_Lambda) = 0.83) and on kernel (alpha1 1.083 vs RAR 0.873 e-10, 20%). The N agreement is a low-a0-is-high property: it needs the alpha1/standard kernels or ensemble E on the Lambda footing. The data prefer RAR-like shapes, where the ordering reverses.
- A1 was found after the data table existed; my menu was declared after seeing that N fits, so it is not an independent prediction; the decoy control is my attempt to price that.
- Nothing is promoted. The principle (maximal static mass as the origin of the galaxy MOND scale) was never shown to be about galaxies.

## NOT established
Any reason that ordinary-galaxy accelerations know the Nariai mass; which footing or kernel is correct; any distinction between N, 5.789, 6, 2 pi on present data.

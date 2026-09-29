# N2 -- emergence with a forced tower spectrum (pre-registration)

Written 2026-09-28 BEFORE any script in this directory was run. Nothing has been computed in this lane yet; the only numbers below are
hand estimates written down so that they can be falsified, and each is labelled as such.
Target: 1/alpha = 137.035999177 (Thomson limit). Everything at another scale is stated with its scale. alpha runs.

## Question (red-team branch 2)
Emergence says 1/e_i^2 = 0 at the species cutoff Lambda_sp = M_red / sqrt(N), so the low-energy couplings are one-loop threshold sums over the charged
states below the cutoff. The SM alone leaves 1/alpha_em ~ 107 at the cutoff (lane M, m4). What if the charged content is a TOWER whose charges and multiplicities are
fixed by field content and geometry, and whose spacing fixes N? Is there then a forced principle that fixes a gauge coupling?

## Conventions (fixed now)
* Running: d(1/alpha_i)/d ln mu = -b_i/(2 pi), i in {Y, 2, 3}, alpha_Y UN-normalised (Q = T3 + Y), so b_Y = 41/6, b_2 = -19/6, b_3 = -7 for the SM
  (GUT-normalised b_1 = (3/5) b_Y = 41/10; the lane-A slip was b_Y = (3/5) b_1; forbidden here and checked). 1/alpha_em = 1/alpha_Y + 1/alpha_2 above the EW scale.
* One-loop coefficient of a state: b = -(11/3) C_A [vector] + (2/3) T [Weyl] + (1/3) T [complex scalar] + (1/6) T [real scalar]; a MASSIVE vector counts as vector + real adjoint scalar
  (the eaten A_5 / Goldstone), i.e. -(7/2) T(adj); Dirac = 2 Weyl. T(U(1)_Y) = sum Y^2 x (dimension of the other factors). A Dirac fermion of unit charge: b = 4/3, i.e. 2/(3 pi) per ln.
* Inputs (lane B, `rg_common.py`, read only): 1/alpha_em(M_Z) = 127.930, sin^2 = 0.23122, alpha_s(M_Z) = 0.1180, M_Z = 91.1876 GeV, M_red = 2.435e18 GeV, and the
  measured offset 1/alpha(0) - 1/alpha(M_Z) = 9.106 (hadronic-inclusive; a measured-mass input, walled). The SM zero modes run with the SM one-loop coefficients from M_Z up.
* Species cutoff, declared (Dvali form; O(1) coefficient NOT derived, lane C measured its spread): Lambda_sp^2 N(Lambda_sp) = M_red^2, N(Lambda) = N_0 + (dof of all tower states with mass <= Lambda),
  N_0 = 118 (lane C/M count). Real solution may not exist (N is a step function); then Lambda_sp is pinned at the threshold where the bound is first violated (declared).
* Emergence boundary: 1/alpha_i(Lambda_sp) = 0.

## The towers (declared now; the list is complete)
Tower geometry: S^1/Z2 (a circle orbifold), compactification scale M_c = 1/R, KK levels at m_j = j M_c (j = 1, 2, ...).  R (equivalently x = Lambda/M_c) is the free modulus.
* TA "matter tower": SM fermions (45 Weyl -> one 4D Dirac per level, 180 dof) and the Higgs doublet (4 dof) in the bulk, gauge fields on the brane; plus a massive KK graviton (5 dof) per level.
  Hand expectation of the per-level coefficient (Y,2,3): (27/2, 49/6, 8); 189 dof per level.
* TB "universal tower" (UED-type): all SM fields in the bulk: adds a massive KK vector in each adjoint (36 dof, coefficient -(7/2) C_A). Hand expectation (27/2, 7/6, -5/2); 225 dof per level.
  (The published UED coefficients (81/10, 7/6, -5/2) in GUT normalisation are RECALLED, not read; not used as inputs.)
* TC "orbifold-GUT gauge/Higgs tower" (structural sign test only, no scored trial): SU(5) gauge + 5_H in the bulk of S^1/(Z2 x Z2'), matter on the branes. Levels: even j: SM massive
  adjoint vectors + Higgs doublet, coefficient (1/6, -41/6, -21/2), 45 dof (with graviton); odd j: X,Y massive vectors + colour-triplet Higgs, hand expectation (-521/18?, -21/2, -41/6)
  (Y entry to be checked by script; the SU(5) universal-shift check is the gate). This is the "anomaly-fixed by group theory" case: the parity assignment is a declared discrete choice.
* Anomaly consistency (declared scope): SM Weyl content per generation checked exactly (sum Y^3, sum Y, SU(2)^2Y, SU(3)^2Y, SU(3)^3-type not needed); KK levels are Dirac (vector-like) so cancel per level;
  fixed-point (boundary) anomaly cancellation for chiral zero modes on an orbifold needs brane Chern-Simons terms: NOT derived here, stated as recalled. Not tested: S^2 towers, Regge/winding
  towers with exponential degeneracy (the sum diverges as the degeneracy grows; heterotic couplings are lane H), and towers with a forced R.

## What is forced and what is declared (to be reported unchanged)
Forced by field content/geometry: per-level charges, multiplicities, coefficients b_{i,j}; the spacing pattern m_j = j M_c; the one-loop log coefficient 2/(3 pi) per unit Dirac.
Declared: which towers; which fields are in the bulk; N_0; the O(1) coefficient of the species cutoff; sharp thresholds; the boundary condition 1/alpha = 0 at Lambda_sp; the number of gravitons per level.
Free: M_c (R). The requirement 1/alpha_i(Lambda_sp) = 0 is one equation per coupling in ONE unknown.

## Scripts (count = 4 plus one shared library; each has a MUTATE control, invocation: positional `MUTATE`, exit code 1)
1. `n1_tower_content.py` -- exact Fractions: per-level coefficient tables (checks H1), SM zero-mode check, SU(5) universal-shift check for TC, anomaly sums, sympy closed form of the one-loop sum
   S(x) = sum_{n<=floor x} ln(x/n) = floor(x) ln x - ln floor(x)!, its asymptotics x - (1/2) ln(2 pi x) + O(1/x) (sympy series + numeric). MUTATE: hypercharge normalisation 3/5 instead of 5/3.
2. `n2_emergence_solve.py` -- self-consistent Lambda_sp(M_c); for each tower and each of three closures (fit M_c to 1/alpha_Y, 1/alpha_2, or 1/alpha_3 at M_Z) the roots, the residuals
   1/alpha_i(Lambda_sp), predictions of the other two couplings, sin^2, 1/alpha_em(M_Z), 1/alpha_em(0) = +9.106; two N conventions (with / without KK gravitons). MUTATE: drop the
   self-consistency (fixed N_0) -> the identity check must fail.
3. `n3_scale_scheme.py` -- systematic bands: (a) Lambda_sp -> c Lambda_sp, c in {1/2, 2}; (b) hard-cutoff scheme constant (lane J: -0.2804 per ln(Lambda^2/m^2) for a Dirac fermion, i.e. 0.02231 per unit b),
   applied to every state as an order-of-magnitude estimate; (c) share of the tower sum carried by the linear (5D-divergence) term; (d) required modulus shift. MUTATE: ceil instead of floor in the sharp sum.
4. `n4_score_bar.py` -- scores every closure with lane D's checker (imported read only); verdict per criterion. MUTATE: run the checker's own selftest in mutate mode.

## Everything that will be tried (declared count)
3 towers x 3 closures x 2 N-conventions = 18 solves; scored trials = 2 towers (TA, TB) x 3 closures = 6 (main N convention); TC is structural (no scored trial); the other N convention is reported.
Look-elsewhere family size passed to the checker: 18 (log2 = 4.17), one fitted real (M_c), one stated scale (Thomson).

## Criteria (declared now)
* N1 (content): every per-level table equals its hand expectation (TC odd Y entry excepted, gated by SU(5) universality), SM zero modes reproduce (41/6, -19/6, -7), anomaly sums vanish, closed-form sum = brute-force sum to 1e-12. Exit 0 iff all pass.
* N2 (self-consistency): at every solution Lambda^2 N(Lambda) = M_red^2 to 1e-9 relative (or the solution is flagged pinned).
* N3 (sign feasibility, expectation): TA has a root for all three closures; TB has none for closure 3 (b~_3 < 0) and none for closure 2; TC none (all coefficients negative). Reported as found; a wrong expectation is reported as wrong.
* N4 (emergence vs requirement 0, at the Y-closure root): report 1/alpha_Y, 1/alpha_2, 1/alpha_3, 1/alpha_em at Lambda_sp. Pass "consistent with 0" iff each is within its own systematic band (n3). This is a NECESSARY test only; the band is expected to be so wide (tens of units) that passing is non-discriminating, and that is to be stated.
* N5 (forcedness of x = Lambda/M_c): does anything in the tower fix x? Test: the geometric relation M_red^2 = (pi or 2 pi) R M_5^3 with M_5 = Lambda_sp and N = N_0 + n_lvl x (no root expected since n_lvl >> 2 pi). Also the closure spread: x_Y, x_2, x_3 agree within 10% (necessary for a joint fixing). Hand estimate (unverified): TA x_Y ~ 32, x_2 ~ x_3 ~ 38, spread ~ 20%, so N5 joint expected to FAIL at 10% and to pass only within the band.
* N6 (the bar, lane D): a closure is evidence only if P < 1e-3 after look-elsewhere, |miss| <= 5e-10 or the stated predicted precision (the systematic band of n3 divided by 137.036), zero fitted reals, scale stated. A prediction whose band exceeds the miss tolerance cannot be scored; that is a finding, not a pass. Expectation: every closure fails (one fitted real, band >= 10%).
* Post-hoc rule: any relation noticed after seeing numbers is labelled post-hoc and not scored. No parameter is scanned to make a criterion pass; M_c is solved, not tuned, and each closure states which measured coupling it spends it on.

## Declared expected outcome
No forced principle. Emergence with a declared tower turns the requirement 1/alpha_Y(Lambda) = 0 into a determination of the modulus x = Lambda R (about 30 levels); alpha is traded for R, the same object lane F found, and
the power-law (5D linear) term makes the O(1) ambiguity of Lambda_sp worse, not better, than in the log case (band ~ b~ x ln(c)/2 pi, tens of units of 1/alpha).

## Literature status
No paper was read for this lane. The Dvali species bound, the emergence proposal (Heidenreich-Reece-Rudelius), UED coefficients (Dienes-Dudas-Gherghetta / Appelquist-Cheng-Dobrescu), orbifold-GUT parities (Kawamura, Hall-Nomura), boundary anomalies on orbifolds (Arkani-Hamed-Cohen-Georgi) are RECALLED from memory and from what other lanes wrote; none is used as an input value.
Lanes read: ALPHA_CHAIN_STATUS.md (in full), rg_common.py (in full), m4_lane_c_content_and_cutoff.py and .out (in full), alpha_bar_checker.py (in full), D and C pre-registrations (read, D partly, C in full), lane J pre-registration lines on the scheme constant (grep).

## Amendments (appended after the runs; no criterion above was edited)
* A1 (hand-arithmetic slip in this file): the TC odd-level hypercharge entry was written -521/18 with a question mark; the script gives -523/18 (= -175/6 + 1/9). The SU(5) universal-shift gate passes with -523/18. No result depends on it (TC has no root for any closure).
* A2 (wrong expectation, N3): TB closure 2 DOES have a root (x = 250.8). It is absurd on its face: it needs 1/alpha_Y(Lambda_sp) = -468 and 1/alpha_3(Lambda_sp) = +143. Reported as an expectation not met.
* A3 (wrong expectation, band size): the pre-registration expected the scale band to be tens of units. When M_c is refitted to the same coupling for each c in {1/2, 2}, the predicted 1/alpha_em(0) moves by only 0.4-2.5 units (0.3-1.9 %), because the refit absorbs the shift; so the band is NOT so wide that N4 is non-discriminating. The absolute size of the lane-J scheme constant kappa*sum(b) (5-12 units in 1/alpha_i for TA) is the relevant scale for testing a residual against 0, and that comparison was chosen after seeing the residuals (declared post-hoc, reported, not scored). Both are printed in n3 and n4.
* A4 (post-hoc, not scored): the near-agreement of the TA closures 2 and 3 (x = 38.44 vs 38.60) is a consequence of b~_2 - b~_3 = 1/6 per level and of Lambda_sp landing where the SM 1/alpha_2 - 1/alpha_3 (plus the small tower differential) is about the measured 21.1. A crude estimate (also post-hoc) puts the chance of that landing within 1 % at roughly 30 % over plausible x; no evidence.

## Results (appended after the runs)
Scripts: n1_tower_content.py, n2_emergence_solve.py, n3_scale_scheme.py, n4_score_bar.py (+ tower_lib.py); outputs n?_*.out and n?_*_MUTATE.out, n2_results.json, n3_results.json. Every real run exits 0; every MUTATE run (positional argument) exits 1.
* N1 PASS. Per-level (Y,2,3): TA (27/2, 49/6, 8), 189 dof; TB (27/2, 7/6, -5/2), 225 dof; TC even (1/6, -41/6, -21/2), odd (-523/18, -21/2, -41/6). SU(5) gate passes; SM anomalies vanish; sum closed form = brute force to 1e-15; the sharp-threshold sum is smooth, x - (1/2) ln(2 pi x) - 1/(12 x).
* N2 PASS. Lambda^2 N = M_red^2 holds to 2e-16 at every solution (no pinned solutions occurred).
* N3: TA roots for all three closures; TB none for closure 3, a root for closure 2 (expectation wrong, A2); TC none (every SU(2)/SU(3) coefficient negative).
* Closures (main convention, gravitons included), TA: Y-closure x = 31.47, M_c = 1.00e15 GeV, Lambda_sp = 3.15e16 GeV, N = 5977, predicts 1/alpha_2(M_Z) = 20.6 (meas 29.58), 1/alpha_3 = -0.59 (meas 8.47), sin^2 = 0.173, 1/alpha_em(0) = 128.06 (-6.6 %); 2-closure x = 38.44, 1/alpha_em(0) = 151.69 (+10.7 %); 3-closure x = 38.60, 152.24 (+11.1 %). At the Y-closure root the implied 1/alpha_2, 1/alpha_3 at the cutoff are 8.98 and 9.06, not 0.
  TB (universal tower): Y-closure implied 1/alpha_2, 1/alpha_3 at the cutoff = 41.0, 57.2: decisive failure of joint emergence.
* N5 FAIL: the geometric relation M_red^2 ~ (pi or 2 pi) R M_5^3 with M_5 = Lambda_sp has no positive root (n_lvl = 189 or 225 >> 2 pi); the three TA closure moduli differ by 22.7 %; x is not fixed by anything in the tower.
* N6: no closure clears the bar (one fitted real, misses 6.6-11 % = 1e8 x the tolerance, and 6-11 x outside each closure's own systematic band; the three TA predictions of 1/alpha_em(0) disagree by 19 %).
* Forced vs declared, as reported: forced = charges, multiplicities, per-level coefficients, spacing pattern, log coefficient. Declared = which fields are in the bulk, N_0, the species-cutoff coefficient, sharp thresholds, boundary condition 0 at Lambda_sp. Free = R.
* The power-law regime: 69-73 % of F_Y and > 100 % of F_2, F_3 come from the linear (5D-divergence) term x b~/(2 pi); the -(1/2) ln(2 pi x) boundary term is -5.7 units in 1/alpha_Y (lane J's hard-cutoff constant is 0.03 for one Dirac fermion; a tower multiplies it by the number of states), and the total lane-J-scale constant kappa*sum(b) is 9.5 (Y), 5.6 (2), 5.4 (3) in 1/alpha for TA.

# CFG896: alpha door D02, a Higgs-sector boundary condition solved for the hypercharge (FROZEN pre-registration)

Written 2026-10-20, before any script of this lane was written or run. No number of this lane has been computed by a script when this file is committed. The hand estimates I made while designing it are disclosed in section 10.

This is **attempt #1 of the post-ledger alpha campaign** (rules: `campaign_fresh_gravity/CFG895_alpha_campaign_ledger/ALPHA_CAMPAIGN_RULES.md`; door: `ALPHA_DOORS.md`, section D02). Nothing here is expected to derive alpha. NOT DIAGNOSTIC or KILLED are normal outcomes and will be reported as such.

**Wall note.** The Standard-Model mass sector is WALLED in the record. This lane reads measured masses (m_t, m_H, M_W) and alpha_s as labelled inputs and derives none of them. It tests a boundary principle for the Higgs quartic, not the mass sector. kappa and the record's Z play no part. Alpha stays an INPUT of the record unless a DERIVATION grade is reached, and the rules say none can be reached in one lane.

## 1. Mechanism

Several proposed principles fix the Higgs quartic coupling lambda near the Planck scale: asymptotic safety with a positive gravitational anomalous dimension for lambda (lambda irrelevant, so lambda(M_P) is driven to approximately zero; the Shaposhnikov–Wetterich mechanism, arXiv:0912.0208, RECALLED, not read in this lane), the multiple point principle (lambda = 0 and beta_lambda = 0 at a common scale; Froggatt–Nielsen, RECALLED, not read), and the Veltman condition (the one-loop quadratic divergence of the Higgs mass vanishes). Each condition is an equation in the running couplings at a high scale. The hypercharge coupling g_Y enters lambda's running through the gauge terms of beta_lambda and through the running of y_t, and it enters the Veltman combination directly. So, with measured m_H, m_t and alpha_s held fixed, each condition is an equation for g_Y. Two conditions at one scale are two equations for (g_Y, g_2), which predict alpha(0) and M_W together.

## 2. Forced-kernel candidates and their classes (rules §2)

* C_b(M_s) = lambda(M_s) = 0. **K1-conditional**: forced only if the asymptotic-safety scenario with A_lambda > 0 is accepted (my reading of the mechanism is RECALLED, not checked against the source, because downloads are not authorised for this lane). Otherwise it is a postulated principle (K2).
* C_c(M_s) = 16 pi^2 beta_lambda(M_s) = 0, with beta_lambda = d lambda / d ln mu from the same three-loop function that runs lambda (Y1's `yuk_lam_B`, times 2 for d/d ln mu). **K2** (flatness of the potential at M_s; not forced by AS as I read it: AS forces lambda ~ lambda*, not the vanishing of the SM part of beta_lambda).
* C_d(M_s) = 6 lambda + (9/4) g_2^2 + (3/4) g_Y^2 − 6 y_t^2 = 0 (one-loop Veltman condition, MS-bar couplings at M_s, V = lambda |H|^4 as in Y1). **K2** (naturalness). The coefficients are re-derived in the script from the field-dependent supertrace STr M^2 (check K3); they are not taken from memory.
* C_a: lambda = 0 and beta_lambda = 0 at a common free scale mu*, equivalently lambda_min = min over mu of lambda(mu) = 0 with mu* the position of the minimum. **K2** (multiple point principle).
* Joint pairs (C_i, C_j) at one scale: the class is the weaker of the two legs: (b,c) K2, (b,d) K2, (c,d) K2.

Why the solution set is discrete: each single condition is one smooth equation in one unknown (ln g_Y) with nonzero derivative at a regular point; each pair is two equations in two unknowns (ln g_Y, ln g_2) with a Jacobian that the pre-flight computes. Several roots in the perturbative range would make the variant NOT DIAGNOSTIC (section 8).

## 3. Which alpha, which scale, which scheme

* The prediction is alpha(0), the Thomson limit (target 1/alpha(0) = 137.035999177, CODATA 2022, used only as the target).
* The unknowns are the MS-bar couplings g_Y(mu) and (joint variants) g_2(mu) at mu = M_t = 172.57 GeV (pole mass), in Y1's conventions: g_1^2 = (5/3) g_Y^2, a_Y = 4 pi / g_Y^2, a_2 = 4 pi / g_2^2, unbroken-phase a_em = a_Y + a_2.
* The map to alpha(0) is the record's: **1/alpha(0) = a_Y(M_t) + a_2(M_t) + Delta_t**, with Delta_t = 137.035999177 − [a_Y + a_2](M_t) evaluated on Y1-central. This is the same construction as CFG895's "+32.6" offset from M_P and lane B's measured 0 -> M_Z offset (9.106), transported to mu = M_t. In inverse-coupling units the one-loop running is additive and independent of the coupling, so Delta_t is alpha-independent at leading order; alpha enters it at two loops, and the script bounds that (section 6). **Consequence, stated so it cannot be hidden:** the graded comparison is in substance a comparison at mu = M_t between the a_em that the principle produces and Y1-central's a_em(M_t), which was built from the measured (G_F, M_W, M_Z). That on-shell combination is a forbidden alpha proxy as an INPUT (rules §1.4); here it is used only as the comparison target, never as an input to the prediction.
* Running: Y1's validated machinery, unchanged and imported read-only (`real_research/alpha_principle_2026/Y1_running_precision/y1_lib.py`): gauge betas at four loops, y_t and lambda at three loops, DOP853 (Y1 `Traj` defaults), from mu = M_t up to 3e21 GeV.
* High scales: M_P = 1.220890e19 GeV and M_red = 2.435e18 GeV (Y1's X_P and X_R).
* Error carried for the running and the map (rules §1.3): Y1's sigma(1/alpha_em)/137.036 = 8.8e-4, i.e. sigma_map = 0.1206, plus Y1's Thomson link 0.008, in quadrature.

## 4. Inputs (all already cited in the repository, in `y1_lib.PDG`, PDG 2024; no downloads)

| Input | Value | Label | Used in |
|---|---|---|---|
| M_t | 172.57 ± 0.29 (exp) ± 0.30 (non-perturbative, Y1 E3); 0.42 in quadrature | measured | all variants |
| alpha_s(M_Z) | 0.1180 ± 0.0009 | measured | all |
| M_H | 125.10 ± 0.09 | measured | all |
| M_W | 80.3692 ± 0.0133 | measured | singles only (fixes g_2 through Buttazzo's matching); joint variants PREDICT it |
| v = (sqrt 2 G_F)^(-1/2) | 246.21971 GeV | measured (exact for this purpose) | implicit in Buttazzo's matching formulas |
| y_b, y_tau at M_t | SMDR reference values | measured/derived | all (enter at 1e-5) |
| Matching items | y_t ± 0.0005, lambda ± 0.0003, g_3 4.26e-5 relative, g_2 1.16e-5 (Y1 E5) | declared theory errors | full budget |
| RGE order | y_t and lambda betas at 2 instead of 3 loops (Y1 E7, full difference as 1 sigma); gauge five-loop estimate (Y1 E6) | declared theory errors | full budget |

* g_3(M_t) from alpha_s by Y1's QCD-only route with its SMDR calibration (Y1 amendment A6). y_t(M_t) and lambda(M_t) from Buttazzo's interpolation formulas (as in Y1-central). g_2(M_t) from Buttazzo's formula at the measured M_W (singles).
* **Not an input anywhere on the prediction side:** M_Z, alpha at any scale, sin^2 theta_W, Delta alpha_had, or Y1-central's g_Y. Y1-central's g_Y(M_t) = Buttazzo's value at the PDG inputs (built from M_W, M_Z, G_F) is used only (i) as the expansion point of the pre-flight ("if the principle is right, the root lies here") and (ii) through the target, as stated in section 3.
* **Forbidden proxies** (rules §1.4): alpha at any scale, R_K, Z_0, mu_0, R_inf with m_e, the Bohr radius, the Thomson cross-section, the classical electron radius, g−2, an on-shell sin^2 theta_W built with G_F and M_W, real numbers fitted to alpha, kappa, Z. None is used as an input.
* **Where a measured alpha could hide (contamination list, quantified in the script):**
  1. Buttazzo's matching formulas for lambda(M_t), y_t(M_t) and g_2(M_t) were fitted at fixed M_Z and G_F, i.e. at the measured alpha; electroweak corrections are O(alpha). Bound: I take the entire printed NNLO-minus-tree correction of lambda (lambda_tree = M_H^2/(2 v^2)) and of g_2 (LO 0.65294 to NNLO 0.64779) as alpha-proportional, and 2% of y_t as the electroweak share of its matching (the remainder is QCD); a 1% change of alpha moves each by 1% of that share.
  2. G_F from the muon lifetime carries an O(alpha/pi) QED correction (about 4e-3 in the rate); v moves by about 1e-5 per 1% of alpha. Stated, not propagated (v is not a free argument of Buttazzo's formulas).
  3. alpha_s world average (lattice entries with QED effects): about 1e-5 per 1% of alpha. Stated.
  4. Electromagnetic final-state corrections in the M_t, M_H, M_W analyses: inside the quoted errors. Stated.
  5. Delta_t (the target transport): two-loop QED running, computed in the script for the leptons and bounded for the hadrons by 3 times the leptonic value.
  6. The target itself (Y1-central's a_em(M_t), from G_F, M_W, M_Z): used as the comparison target only.

## 5. Option space: K = 13, every member pre-declared, all graded

| ID | Variant | Unknowns | Scale | Predicts |
|---|---|---|---|---|
| S1 | (a) lambda = beta_lambda = 0 at free mu* (lambda_min = 0) | ln g_Y (mu* follows) | free | alpha(0) |
| S2 | (b) lambda = 0 | ln g_Y | M_P | alpha(0) |
| S3 | (c) beta_lambda = 0 | ln g_Y | M_P | alpha(0) |
| S4 | (d) Veltman | ln g_Y | M_P | alpha(0) |
| S5 | (b) | ln g_Y | M_red | alpha(0) |
| S6 | (c) | ln g_Y | M_red | alpha(0) |
| S7 | (d) | ln g_Y | M_red | alpha(0) |
| J1 | (b)+(c) (the "AS-forced" pair of the door) | ln g_Y, ln g_2 | M_P | alpha(0), M_W |
| J2 | (b)+(d) | ln g_Y, ln g_2 | M_P | alpha(0), M_W |
| J3 | (c)+(d) | ln g_Y, ln g_2 | M_P | alpha(0), M_W |
| J4 | (b)+(c) | ln g_Y, ln g_2 | M_red | alpha(0), M_W |
| J5 | (b)+(d) | ln g_Y, ln g_2 | M_red | alpha(0), M_W |
| J6 | (c)+(d) | ln g_Y, ln g_2 | M_red | alpha(0), M_W |

* The door wrote "K ≤ 8". That undercounts: the scale choice {M_P, M_red} applies to the single conditions as much as to the pairs. The honest count is 13, and 13 is used.
* M_W in the joint variants: from g_2(M_t) by inverting Buttazzo's g_2 formula, M_W = 80.384 + 0.014 [g_2 − 0.64779 − 0.00004 (M_t − 173.34)] / 0.00011. The formula holds M_Z fixed; the M_Z dependence of the g_2 matching at one loop is bounded in the script with Y1's analytic one-loop threshold `threshold1_g2` (reported, not graded). M_Z is a derived output of the joint variants (not graded: it is fixed by alpha and M_W given G_F).
* Declared conventions that are NOT counted as options (fixed now): MS-bar couplings (not the effective-potential lambda_eff); the one-loop form of the Veltman condition (the door's); beta_lambda at the three-loop order that runs lambda; matching at mu = M_t; the two high scales above. Choosing any other would be a new lane.

## 6. Leverage and precision pre-flight (rules §1.6), computed before any solving

At the measured point (all inputs central; g_Y and g_2 at Y1-central values), by central finite differences on full Y1 trajectories:

1. The leverages dC/d ln g_Y(M_t) for every condition at both scales (and dC/d ln g_2(M_t) for the joint variants), including C_a (lambda_min, re-minimised for each perturbation). In particular the door's quantities: d lambda(M_P)/d ln g_Y and d beta_lambda(M_P)/d ln g_Y.
2. The input derivatives dC/dx and the derivatives of the map, d(1/alpha(0))/dx at fixed unknowns, for x in {M_t, alpha_s, M_H} (door set) and additionally {M_W (singles), y_t matching, lambda matching, g_3 matching, g_2 matching (singles), RGE order (E7), gauge five-loop (E6)}.
3. Linear propagation through the implicit function theorem. Singles: d ln g_Y/dx = −(dC/dx)/(dC/d ln g_Y); joints: d(ln g_Y, ln g_2)/dx = −J^(-1) dC/dx. Total d(1/alpha(0))/dx = partial derivative at fixed unknowns + d(1/alpha(0))/d(unknowns) times d(unknowns)/dx. Same for M_W (joints).
4. Two numbers per variant:
   * sigma_PF(1/alpha(0)): from M_t (0.29 GeV, the PDG experimental error, as the door specifies), alpha_s and M_H only, in quadrature. A strict lower bound on the route's error.
   * sigma_full(1/alpha(0)): every item of step 2, with M_t at 0.42, plus sigma_map (0.1206) and the Thomson link (0.008), in quadrature.
   Joints also give sigma_full(M_W) and the alpha–M_W correlation, and the condition number of J.
5. **Pre-flight decision (frozen):** a variant is **NOT DIAGNOSTIC and stops** if sigma_PF(1/alpha(0)) > 1.37 (the door's rule: 1% of 137.036) **or** sigma_full(1/alpha(0)) > 1.37 (stricter, same threshold). A joint variant whose alpha leg passes but with sigma_full(M_W) > 0.80 GeV (1%) proceeds but is graded as a single-coupling route (ceiling CONSISTENT, rules §4.3 corollary). Only variants that pass proceed to solving.
6. Reported by-product, **not an alpha result**: the consistency of each principle with the measured world at the measured point, z = C(measured) / sigma_full(C) (singles), chi^2 with 2 dof (joints, full input covariance of the two conditions). This says whether the measured inputs satisfy the principle; it predicts nothing about alpha.
7. Substitution numbers (rules §4.2), computed at the measured point for every variant from the same Jacobian: the shift of the would-be prediction of 1/alpha(0) when every place of section 4's contamination list is scaled as if alpha were 1% larger. A variant that reaches a value fails the identity test if that shift exceeds 0.137 (10% of the 1% shift that an identity would show).

## 7. Gates and controls (before the graded output; any gate failure makes the script exit non-zero and every variant NOT COMPLETED)

* **K1 (reproduce Y1's validated numbers exactly):** (i) Y1-central at X_P gives a_Y 55.2342, a_2 49.2026, a_3 52.9713, a_em 104.4368 (printed in `y1_4_budget.out`), |difference| ≤ 1e-4 each; (ii) Buttazzo's inputs with Y1's like-for-like run (three-loop gauge + pure-QCD four-loop, Buttazzo's g_3) give g_1 0.61537, g_2 0.50546, g_3 0.48731, y_t 0.38248, lambda −0.01437 at 1.22089e19 (printed in `y1_2_validate_published.out`), |difference| ≤ 1e-5 each (the printed digits).
* **K2 (lambda(M_P) sensitivities):** at Buttazzo's point with Y1's steps (M_t ± 1 GeV, alpha_3 0.1191/0.1177, M_H ± 1 GeV) the lambda(M_P) sensitivities equal Y1's printed −0.00649, +0.00186, +0.00281 within 2e-5.
* **K3 (Veltman coefficients):** the phi^2 coefficient of STr M^2(phi) built in sympy from the field-dependent masses (W: 6 dof, g^2 phi^2/4; Z: 3 dof, (g^2 + g'^2) phi^2/4; top: −12 dof, y_t^2 phi^2/2; h: 1 dof, 3 lambda phi^2; Goldstones: 3 dof, lambda phi^2; with V = lambda (H^dagger H)^2 = lambda phi^4/4) equals the coefficients (6, 9/4, 3/4, −6) typed in C_d, exactly.
* **K4 (beta_lambda in C_c):** the beta_lambda used in C_c equals 2 × Y1's `yuk_lam_B` lambda component on the trajectory (relative 1e-12), and its one-loop part equals the textbook 16 pi^2 beta_lambda = 24 lambda^2 − 6 y_t^4 + (3/8)(2 g^4 + (g^2 + g'^2)^2) + lambda (12 y_t^2 − 9 g^2 − 3 g'^2) at 20 random coupling points with y_b = y_tau = 0 (relative 1e-12).
* **K5 (finite differences):** every derivative whose effect on any reported sigma exceeds 1% of that sigma has forward and backward differences agreeing within 5%, and the derivative at step epsilon and at epsilon/2 agreeing within 2%.
* **K6 (an input moved by 5 sigma moves the result as expected):** with M_t + 5 x 0.42 GeV, every condition value moves by 5 x its linear derivative within 15% (the nonlinearity allowance).
* **K7 (positive controls, planted known answers):** (i) single planted condition C_plant = a_Y(M_P) − a_Y^Y1(M_P) (the central value computed in-script): the pre-flight must PASS it (sigma_full ≤ 1.37), and the solver must return 1/alpha(0) = 137.035999177 within 1e-6 relative; (ii) joint planted pair (a_Y(M_P), a_2(M_P)) = Y1-central values: the pre-flight must pass and the joint solver must return 1/alpha(0) within 1e-6 relative and M_W = 80.3692 within 1e-4 GeV.
* **MUTATE control** (`python3 cfg896_preflight.py MUTATE`): the load-bearing hypercharge terms of the two boundary conditions are sign-flipped: +(3/4) g_Y^2 -> −(3/4) g_Y^2 in C_d, and in C_c the hypercharge-containing one-loop gauge terms ((27/400) g_1^4 + (9/40) g_1^2 g_2^2 in Y1's normalisation) flip sign. K3 and K4 must then FAIL and the script must exit 1; exit 3 if the control does not bite. The run reports how each variant's leverage and sigma move under the flip. The real run must exit 0.
* An independent blind re-derivation (rules §4.6) is NOT part of this lane. If any variant ever reaches a value inside its error, that re-derivation is required before any grade above CONSISTENT is discussed.

## 8. Solving (only variants that pass section 6) and grading

* Singles: scan g_Y(M_t) in [0.5, 2.0] x the expansion point on 41 log-spaced points, refine every sign change with brentq; trajectories that hit a Landau pole or fail below 3e21 GeV are excluded points. Joints: scipy fsolve from a 5 x 5 grid of starts in [0.6, 1.6]^2 times the expansion point; distinct roots are those differing by more than 1e-6 in ln g.
* At each root: 1/alpha(0), M_W (joints), and the route's own errors by re-linearising at the root (same items as sigma_full).
* **Grades (rules §5, exactly these words):**
  * NOT COMPLETED: a gate of section 7 fails, or the variant cannot be evaluated (for S1: lambda has no interior minimum between 1e10 and 3e21 GeV at the measured point).
  * NOT DIAGNOSTIC: fails the pre-flight; or more than one admissible root whose predictions differ by more than the route's 1 sigma.
  * KILLED: no root in the scanned perturbative range (the principle cannot be met with the measured inputs); or the prediction misses 137.036 by more than 2 sigma_route (singles); or, for joints, chi^2 (2 dof, full covariance of 1/alpha(0) and M_W against 137.036 and 80.3692 ± 0.0133) > 6.18. I read the door's "misses by more than its propagated error" as the 2-sigma band: a 1-sigma kill would kill a true principle about a third of the time. Disclosed.
  * CONSISTENT: inside, but P_family ≥ 1e-3 ("allowed, not predicted"; never a derivation).
  * EVIDENCE / DERIVATION: cannot be awarded in this lane (needs the blind re-derivation, the V1 harness against all five measurements, a second prediction that checks out, and the look-elsewhere test). A variant that passes every lane-internal criterion is graded CONSISTENT (pending) and flagged.
* Substitution test (section 6.7) and the residual and shape tests (rules §4.2) apply to any value: there is no closed form and no series here, so the residual and shape tests are not applicable and are stated as such.

## 9. Trials factor, attempt count and the precision demanded

* All 13 variants are pre-declared graded variants, so **N_mech goes from 359 to 372** whatever their grades (rules §3, the conservative reading: a NOT DIAGNOSTIC variant is still counted). Post-ledger attempt counter: this lane is attempt #1.
* Prior (rules §4.3): log-uniform 1/alpha in [10, 1000], density rho_alpha = 1/ln 100 = 0.217 per unit relative deviation. For M_W: the default log-uniform [10, 1000] GeV (0.217) and a stricter physical prior M_W = g v/2 with g in [0.1, 3] (density 1/ln 30 = 0.294); the stricter (0.294) applies.
* P_single = K_v x prod_i (2 rho_i max(|miss_i|, sigma_i)/value_i), and P_family ≈ N x P_single. Two readings, the stricter applies:
  * (A) 13 separate trials, each with K_v = 1, N = 372: single coupling needs delta ≤ 1e-3/(372 x 0.434) = **6.2e-6**;
  * (B) one lane trial with K = 13 and N = 360: delta ≤ 1e-3/(13 x 360 x 0.434) = **4.9e-7** (stricter; applies).
  * Joint (alpha, M_W) under (B): 13 x 360 x (2 x 0.217 x delta_alpha)(2 x 0.294 x delta_MW) < 1e-3.
* Single-trial mechanism bar (one trial, K_v = 1): delta ≤ 2.3e-3. With Y1's running error alone (8.8e-4) a single-coupling variant has P_single ≥ 3.8e-4, so the singles can reach CONSISTENT at most (rules §4.3 corollary). Only a joint variant can, in principle, clear the campaign-wide bar.

## 10. Expected outcome (written so it can be wrong) and the hand estimates behind it

Hand estimates made while designing this file, from Y1's printed Buttazzo sensitivities (lambda(M_P) −0.0066 per GeV of M_t, +0.0018 per 0.0007 of alpha_3, +0.0029 per GeV of M_H; y_t(M_P) +0.0051 per GeV) and the one-loop formulas; none comes from a script of this lane:
* At the PDG inputs lambda(M_P) ≈ −0.010 with sigma ≈ 0.0036, so the measured world misses lambda(M_P) = 0 by about 3 sigma (z ≈ −3).
* 16 pi^2 beta_lambda(M_P) ≈ +0.03 (positive: lambda's minimum lies below M_P); the Veltman combination at M_P ≈ −0.22.
* Leverages per unit ln g_Y(M_t), including the one-loop transport factor (g_Y(M_P)/g_Y(M_t))^2 ≈ 1.8: lambda(M_P) of order 0.02–0.1; 16 pi^2 beta_lambda(M_P) about 0.3; Veltman about 0.6. With d(1/alpha(0))/d ln g_Y ≈ −2 a_Y(M_t) ≈ −196, the expected sigma(1/alpha(0)) is roughly 10–30 for (b), 2–6 for (c), 5–15 for (d), and similar to (b) for (a).
* **Expected:** every single variant NOT DIAGNOSTIC (as the door itself predicted). The joint pairs are expected to be worse, not better: g_Y and g_2 enter lambda and beta_lambda mainly through g^2 + g'^2 at high scale, so J should be close to singular. If any variant passes, I expect it to be KILLED, because the measured world sits about 3 sigma from lambda(M_P) = 0 and beta_lambda(M_P) and the Veltman combination are far from zero.
* If every variant is NOT DIAGNOSTIC, this is the first NOT DIAGNOSTIC result on door D02; under rules §6 a second consecutive one on D02 (without a new forced element) would close the door.

## 11. Files and hygiene

* `cfg896_preflight.py` (pre-flight, gates, controls, and the solving stage for variants that pass; writes `cfg896_preflight.json`), outputs `cfg896_preflight.out` (real) and `cfg896_preflight_MUTATE.out` (control). FIRSTRUN outputs are kept if a later amendment changes anything. `README.md` with the grades.
* Single core (`OMP_NUM_THREADS=1 nice -n 10`), < 1 GB, < 10 min per run. Y1 is imported read-only; no file of any other lane is edited. Amendments to this file are appended below this line with date and reason; nothing above it changes.

## Amendments

All three amendments below were written AFTER the first run (`cfg896_preflight_FIRSTRUN.out`, `cfg896_preflight_FIRSTRUN.json`, kept unchanged) and are therefore POST HOC. I had seen every number of that run when writing them. **As frozen, the FIRSTRUN verdict is NOT COMPLETED for all 13 variants**, because three gates failed (K5, K6, K7(ii)); the FIRSTRUN script printed the would-be grades next to "gates: FAILED" instead of overriding them, which is also corrected below. None of the amendments changes a condition, an input, an error item, the map, the pre-flight threshold, the decision rule or a kill criterion. The pre-flight numbers and the roots of the FIRSTRUN do not depend on them.

* **A1 (K5, item linearity).** FIRSTRUN failed K5 on the item derivatives of C_c (beta_lambda at M_P and M_red) with respect to M_t (asymmetry 0.077–0.14) and alpha_s (0.28–0.42); the printed list was truncated to six entries, so the amended script prints the full list under the frozen criterion. Diagnosis (to be shown by the amended script, not assumed): the asymmetry is genuine curvature of beta_lambda near the Planck scale, from its 24 lambda^2 term (lambda(M_P) ≈ −0.011 moves by about 0.0027 per sigma of M_t, so delta lambda / lambda ≈ 0.24), not numerical noise. The evidence the script must print: (i) the asymmetry is unchanged when the ODE tolerance is tightened from rtol 1e-11 to 1e-13; (ii) the 24 lambda^2 term carries most of the second difference of C_c; (iii) K6's 5-sigma shifts follow the quadratic model built from the ±1 sigma points (A2). The frozen 5% asymmetry rule was a poor proxy for what it protects, which is the accuracy of the linear (central-difference) propagation: for a quadratic dependence the central difference is the exact slope at the centre and the missing variance is a fraction asym^2/2 of that item's variance. **Replacement:** K5 keeps its frozen part (a) unchanged for the derivatives with respect to the unknowns (step stability within 2%, asymmetry < 5%). Its item part is replaced by **K5(b), a nonlinear Monte Carlo of the pre-flight itself**: N = 200 Gaussian draws (seed 896) of the two-sided items (M_t 0.417, alpha_s, M_H, M_W, y_t, lambda, g_3 and g_2 matching); for each draw and each variant the shifted condition C_v(unknowns; x_j) = C_v(measured point; central inputs) is solved by chord-Newton with the measured-point Jacobian (tolerance 1e-10 in ln g, at most 40 iterations); sigma_MC of 1/alpha(0) must agree with the linear quadrature of the same items within 20% (Y1's criterion) for every variant and both planted controls, with at most 2% of draws unconverged. The one-sided items (E6, E7) and the map error are not drawn, as in Y1. The frozen item-asymmetry list is still printed and reported as "frozen K5 item criterion: FAIL, superseded by A1". **Use of the MC for the decision:** the frozen linear rule still decides the pre-flight. If the MC version of sigma_full (sigma_MC combined in quadrature with E6, E7, the map error and the Thomson link) falls on the other side of 1.37, the variant is reported as FRAGILE and graded NOT DIAGNOSTIC, with the stage-2 result (if any) stated beside it.
* **A2 (K6).** FIRSTRUN failed K6 only for C_c (ratios 1.275 at M_P and 1.344 at M_red; all other conditions 1.009–1.020). The frozen check compared the 5-sigma shift with the linear term alone, ignoring the curvature that K5 measures; the quadratic model predicts 1 + 5 asym / 2 = 1.278 and 1.346 from the FIRSTRUN asymmetries. **Replacement:** the expected 5-sigma shift is 5a + 25b with a = (v+ − v−)/2 and b = (v+ + v− − 2 v0)/2 from the ±1 sigma points; tolerance 15% unchanged. The linear ratios are still printed.
* **A3 (K7(ii), joint solver acceptance).** FIRSTRUN's joint solver rejected all 25 starts of the planted pair. Diagnosis (scratch check, to be reproduced by the amended script, which prints fsolve's flag and the residual per start): fsolve reaches the planted root to |ln g| ~ 1e-16 with residual ~1e-14, but returns ier = 5 ("not making good progress") because xtol = 1e-12 lies at the noise floor of the ODE-based function; my acceptance rule demanded ier = 1. **Replacement:** a start is accepted when max |F| ≤ 1e-9 at the returned point, whatever the flag. The same rule applies to the stage-2 joint solves.
* **A4 (grading when a gate fails).** The amended script prints "NOT COMPLETED (gate)" for every variant if any gate fails, with the would-be grade in brackets, as section 7 already required.

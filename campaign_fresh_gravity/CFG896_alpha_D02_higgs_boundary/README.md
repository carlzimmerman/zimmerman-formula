# CFG896: alpha door D02, a Higgs-sector boundary condition solved for the hypercharge

**Result: no variant fixes alpha.** Of the 13 pre-declared variants, 11 are NOT DIAGNOSTIC: even if the principle were true, the measured-input errors would leave 1/alpha(0) uncertain by 2.4 to 14 units, against the 1.37 (1%) bar. The other 2 variants, beta_lambda = 0 at M_P and at M_red, are KILLED: they give 1/alpha(0) = 162.1 ± 2.4 and 149.3 ± 1.5. Nothing here derives alpha, and alpha stays an INPUT. This is attempt #1 of the post-ledger alpha campaign (rules and door: `../CFG895_alpha_campaign_ledger/`).

**Wall note.** The Standard-Model mass sector is WALLED in the record. This lane takes the measured masses (m_t, m_H, M_W) and alpha_s as labelled inputs and derives none of them. It tests a boundary principle for the Higgs quartic coupling, nothing more. kappa and the record's Z play no part.

## What was tested

Door D02 (`ALPHA_DOORS.md`) treats a Higgs-sector boundary condition as an equation for the hypercharge coupling g_Y(M_t), with measured m_H, m_t and alpha_s held fixed. Imposing two conditions at one scale lets (g_Y, g_2) be solved jointly, which predicts alpha(0) and M_W together.

Four conditions were used:

* lambda(M_s) = 0, the asymptotic-safety reading (kernel class K1-conditional);
* beta_lambda(M_s) = 0 (K2);
* the one-loop Veltman condition 6 lambda + (9/4) g² + (3/4) g'² − 6 y_t² = 0 (K2). Check K3 re-derives these coefficients from STr M²;
* lambda = beta_lambda = 0 at a free scale mu*, the multiple point principle (K2).

The two scales are M_P = 1.22089e19 GeV and M_red = 2.435e18 GeV. That gives 13 variants: 7 singles, in which M_W fixes g_2, and 6 joint pairs. The door said "K ≤ 8". That undercounts, because the scale choice applies to the singles as well, so the honest K is 13.

The running is Y1's validated machinery, imported read-only: four-loop gauge betas, three-loop y_t and lambda, and Buttazzo matching at M_t. The map to alpha(0) is 1/alpha(0) = a_Y(M_t) + a_2(M_t) + Delta_t, where Delta_t = 9.2604 is the Y1-central offset.

The rules require a leverage pre-flight before any solving. Assume the principle holds exactly at the measured point. If the input errors still leave sigma(1/alpha(0)) > 1.37, the variant is NOT DIAGNOSTIC and stops. The test is applied twice: once with the door's inputs only (m_t at 0.29, alpha_s, m_H), giving sigma_PF, and once with the full budget, giving sigma_full. Only variants that pass both are solved.

## Grades (after amendments A1–A4; as frozen, the first run is NOT COMPLETED, see below)

| ID | Variant | Kernel | sigma_PF | sigma_full | full, MC | sigma(M_W) GeV | z / chi² of the principle at the measured point (not an alpha result) | Grade |
|---|---|---|---|---|---|---|---|---|
| S1 | lambda = beta_lambda = 0 at free mu* | K2 (MPP) | 11.49 | 14.19 | 13.74 | – | z −3.09 | NOT DIAGNOSTIC |
| S2 | lambda(M_P) = 0 | K1-cond. (AS) / K2 | 10.15 | 12.50 | 12.27 | – | z −3.03 | NOT DIAGNOSTIC |
| S3 | beta_lambda(M_P) = 0 | K2 | 0.83 | 1.28 | 1.25 | – | z +13.0 | **KILLED**: 1/alpha(0) = 162.06 ± 2.45 (+10.2 sigma) |
| S4 | Veltman at M_P | K2 | 4.87 | 5.80 | 5.42 | – | z −5.0 | NOT DIAGNOSTIC |
| S5 | lambda(M_red) = 0 | K1-cond. (AS) / K2 | 10.74 | 13.25 | 13.09 | – | z −3.08 | NOT DIAGNOSTIC |
| S6 | beta_lambda(M_red) = 0 | K2 | 0.70 | 1.10 | 1.09 | – | z +9.0 | **KILLED**: 1/alpha(0) = 149.32 ± 1.55 (+7.9 sigma) |
| S7 | Veltman at M_red | K2 | 5.20 | 6.19 | 5.79 | – | z −5.9 | NOT DIAGNOSTIC |
| J1 | lambda = beta_lambda = 0 at M_P (the door's "AS-forced" pair) | K2 (weaker leg) | 2.59 | 3.51 | 3.42 | 2.77 | chi² 340 | NOT DIAGNOSTIC |
| J2 | lambda = 0 + Veltman at M_P | K2 | 4.03 | 5.51 | 5.35 | 3.11 | chi² 434 | NOT DIAGNOSTIC |
| J3 | beta_lambda = 0 + Veltman at M_P | K2 | 2.42 | 3.27 | 3.19 | 2.50 | chi² 223 | NOT DIAGNOSTIC |
| J4 | lambda = beta_lambda = 0 at M_red | K2 | 3.16 | 4.28 | 4.20 | 2.90 | chi² 95 | NOT DIAGNOSTIC |
| J5 | lambda = 0 + Veltman at M_red | K2 | 4.82 | 6.57 | 6.44 | 3.28 | chi² 822 | NOT DIAGNOSTIC |
| J6 | beta_lambda = 0 + Veltman at M_red | K2 | 2.89 | 3.91 | 3.84 | 2.60 | chi² 81 | NOT DIAGNOSTIC |

All sigmas are in units of 1/alpha(0). The pre-flight threshold is 1.37. "full, MC" is the nonlinear Monte Carlo version of sigma_full (amendment A1). For every variant the ratio MC/linear is 0.93–0.99, and no pre-flight decision changes (no variant is FRAGILE).

## Key numbers (from `cfg896_preflight.json`)

**The measured point.** These are Y1-central couplings at mu = M_t = 172.57: g_Y 0.358427, g_2 0.647643, y_t 0.932859, lambda 0.125968. At M_P:

* lambda = −0.01133;
* 16 pi² beta_lambda = +0.02660 (beta_lambda = +1.69e-4 per unit ln mu);
* Veltman combination = −0.1924.

At M_red, the same three are −0.01154, +0.01527 and −0.2291. lambda reaches its minimum, −0.01164, at mu* = 3.57e17 GeV.

**The door's leverages,** taken at fixed measured m_H, m_t, alpha_s and M_W:

| Quantity | Derivative with respect to ln g_Y(M_t) |
|---|---|
| lambda(M_P) | +0.0586 |
| beta_lambda(M_P) | +1.94e-3 (16 pi² × beta_lambda: +0.307) |
| Veltman(M_P) | +1.295 |
| lambda_min | +0.0519 |

Per unit ln g_2(M_t), the corresponding derivatives are +0.160 for lambda(M_P), +0.204 for 16 pi² beta_lambda(M_P) and +2.346 for Veltman(M_P). The map from the couplings to the observables has these slopes:

* d(1/alpha(0))/d ln g_Y = −195.6;
* d(1/alpha(0))/d ln g_2 = −59.9;
* d M_W/d ln g_2 = 82.4 GeV.

**Why the lambda routes are NOT DIAGNOSTIC.** The error on lambda(M_P), sigma ≈ 0.0037, is dominated by m_t and alpha_s. Dividing it by a leverage of 0.059 per unit ln g_Y gives sigma(ln g_Y) ≈ 0.064, which is about 12.5 in 1/alpha(0). The Veltman condition has more leverage, but its error, sigma ≈ 0.038, comes from y_t and lambda at M_P, which leaves about 6. Only beta_lambda has enough leverage relative to its error to pass the bar. The largest items are M_t (1.10 for S3), the lambda matching (0.47), M_H (0.29) and the y_t matching (0.23).

**The two beta_lambda variants are killed.** The measured world has beta_lambda(M_P) > 0 at 13 sigma (and at M_red at 9 sigma). Making it vanish needs a g_Y(M_t) that is 11% smaller (at M_P) or 6% smaller (at M_red), and so 1/alpha(0) = 162.06 ± 2.45 or 149.32 ± 1.55. Each has one root in the scanned range, and the errors were re-linearised at the root.

**The joint pairs are not a two-leg test.** The alpha(0) and M_W predictions are correlated at +0.976 to +0.985. Two Higgs-sector conditions constrain essentially one combination of (g_Y, g_2), so the rules' K9 assumption that joint P values multiply does not hold for this door. The joint Jacobian is not near-singular: cond(J) in sigma units is 6.3–15.5. My expectation that it would be was wrong, and the variance sits in the shared m_t / alpha_s direction instead.

**By-products (consistency of each principle with the measured world; these are not alpha results):**

* lambda(M_P) = 0 is missed by 3.0 sigma, and lambda_min = 0 by 3.1 sigma. This is the known near-criticality tension, here with Y1's inputs including the 0.30 GeV non-perturbative m_t error.
* beta_lambda = 0 is missed by 13.0 sigma (M_P) and 9.0 sigma (M_red).
* The Veltman condition is missed by 5.0 and 5.9 sigma.
* The joint pairs have chi² (2 dof) of 81–822.

## Controls

* **K1 (reproduces Y1 exactly).** Y1-central at X_P gives a_Y 55.23423, a_2 49.20258, a_3 52.97131 and a_em 104.43681, against Y1's printed 55.2342, 49.2026, 52.9713 and 104.4368. Buttazzo's inputs give g_1 0.615371, g_2 0.505457, g_3 0.487311, y_t 0.382475 and lambda −0.014367 at M_P, against Y1's printed 0.61537, 0.50546, 0.48731, 0.38248 and −0.01437. PASS.
* **K2.** The lambda(M_P) sensitivities are −0.00649 per GeV of M_t, +0.00186 per 0.0007 of alpha_3 and +0.00281 per GeV of M_H, equal to Y1's printed values. PASS.
* **K3.** sympy builds STr M²(phi) from the field-dependent masses; its phi² coefficient is 9g²/4 + 3g'²/4 + 6 lambda − 6 y_t², identical to the coefficients typed in C_d. PASS.
* **K4.** The beta_lambda in C_c equals the beta_lambda that runs lambda (difference 0). Its one-loop part equals the textbook form to 2e-16 at 20 random points. PASS.
* **K5(a), derivatives with respect to the unknowns.** They are linear and step-stable. PASS.
* **K5(b), Monte Carlo** (200 draws, chord-Newton re-solves). The ratio MC/linear is 0.920–0.994 for all 13 variants and both planted controls, with at most 1 of 200 draws unconverged. PASS.
* **K6.** With M_t moved by 5 sigma, every condition moves as the quadratic model built from the ±1 sigma points predicts, with ratios 0.998–1.001. PASS. The frozen linear version (ratios 1.009–1.344) fails, as explained below.
* **K7, positive controls with planted answers.**
  * The planted single condition a_Y(M_P) = Y1 value passes the pre-flight with sigma_full 0.121. The single solver returns 1/alpha(0) = 137.035999177.
  * The planted joint pair passes with sigma_full 0.121 and sigma(M_W) 0.004 GeV. The joint solver returns (137.035999177, 80.36920).
  * Both PASS.
* **MUTATE** (`cfg896_preflight_MUTATE.out`). The hypercharge terms of the two conditions are sign-flipped. K3 and K4 then fail, and the run exits 1 as required. The leverages move as expected:
  * 16 pi² d beta_lambda(M_P)/d ln g_Y goes from +0.307 to −0.277;
  * d Veltman(M_P)/d ln g_Y goes from +1.295 to +0.085, so the Veltman variants' sigma_full rises from 5.8 to 88;
  * the lambda variants, which use no flipped term, are unchanged.

  The MUTATE run skips the Monte Carlo to save CPU while the 1024³ run is live.
* **Substitution numbers** (rules §4.2). Every slot where a measured alpha could hide is scaled as if alpha were 1% larger. The slots are the electroweak shares of the lambda, y_t and g_2 matching, and the two-loop QED part of Delta_t (0.0091 in 1/alpha from leptons, bounded at 4× for hadrons). The would-be prediction shifts by:
  * 0.88–1.01 for S1, S2 and S5 (65–74% of the 1.37 an identity would show, because their leverage is weak);
  * 0.36–0.39 for the Veltman variants;
  * 0.13–0.14 for S3 and S6 at the measured point, and 0.29 and 0.19 at their roots;
  * 0.29–0.58 for the joint pairs.

  These are conservative bounds: the whole NNLO-minus-tree matching correction of lambda and g_2 is treated as proportional to alpha. Even so, the two variants that reached values would also have failed the identity test, whose threshold is 0.137. No closed form or series is involved, so the residual and shape tests do not apply.

## The first run, the amendments, and what "as frozen" means

The first run (`cfg896_preflight_FIRSTRUN.out` and `.json`, kept unchanged and committed with amendments A1–A4 in b2fa5ad0d before the amended run) failed three gates. **As frozen, its verdict is NOT COMPLETED for all 13 variants.** The amendments are post hoc: I had seen every number when I wrote them. None of them changes a condition, an input, an error item, the map, the threshold or a kill criterion, and the pre-flight numbers and roots are identical in both runs.

* **K5 (5% item-asymmetry rule).** It failed on the derivatives of beta_lambda with respect to M_t (asymmetry 0.08–0.14) and alpha_s (0.28–0.42), 16 entries in total. The amended run shows the cause is genuine curvature and not numerical noise:
  * the asymmetry is identical at ODE rtol 1e-11 and 1e-13 (0.11122 and 0.13831 both times);
  * the 24 lambda² term alone gives about 1.9× the observed M_t curvature of 16 pi² beta_lambda (other terms cancel about half of it), because lambda(M_P) ≈ −0.011 moves by about 0.0027 per sigma.

  The rule was a poor proxy for what it protects, which is the accuracy of linear propagation. It was replaced by a nonlinear Monte Carlo of the pre-flight, which agrees with the linear numbers to within 8%.
* **K6 (linear 5-sigma expectation).** It failed for beta_lambda (ratios 1.275 and 1.344). The quadratic model from the ±1 sigma points predicts these to within 0.2%. The amended check uses that model.
* **K7(ii) (joint solver).** The solver rejected every start. In 20 of the 25 starts, fsolve had reached the planted root (residual ≤ 2e-14) but returned flag 5, because xtol sat at the noise floor of the ODE. The acceptance rule had demanded flag 1, so it now accepts by residual. The 5 starts with flag 1 lay in the hypercharge Landau region and are correctly rejected.
* **A4.** If any gate fails, the script now prints NOT COMPLETED. The first-run script had printed the would-be grades next to "gates: FAILED".

## Disclosures

* **The sources were not read.** The Shaposhnikov–Wetterich mechanism (arXiv:0912.0208) and the Froggatt–Nielsen multiple point principle are RECALLED, not read, because downloads were not authorised for this lane. The kernel-class assignments rest on my reading of them: AS forces lambda ≈ lambda*, not beta_lambda = 0. The conditions themselves are well-defined equations. The Veltman coefficients were re-derived (K3).
* **The comparison target is built from an alpha proxy.** In substance, the graded comparison is made at mu = M_t, against Y1-central's a_em(M_t). That a_em was built from the measured (G_F, M_W, M_Z), the on-shell combination the rules forbid as an input. Here it is used only as the target, never as an input. Delta_t depends on alpha only at two loops (bounded above).
* **Hand estimates against results.** Before writing the pre-registration I estimated the measured-point values and the leverages for lambda and beta_lambda correctly. I underestimated the Veltman leverage by about 2×. I expected every single variant to be NOT DIAGNOSTIC, and that was wrong for beta_lambda: it passed the pre-flight and was then KILLED. I expected near-singular joint Jacobians, and that was wrong too: the joint failure is the shared m_t / alpha_s error, with 98% correlation between the two predictions.
* **Declared conventions, not counted as options:** MS-bar lambda (not lambda_eff); the one-loop Veltman form; beta_lambda at three loops; matching at M_t. A different choice would be a new lane. The g_2 matching formula is M_Z-blind; the bias this causes is 0.0019 GeV of M_W per 1% change in g_Y, which is negligible.
* **Rules §6 stop rule.** This is the first NOT DIAGNOSTIC / KILLED result on D02. Every member of its pre-declared option space is now graded. A second lane would need a new forced element (for example lambda_eff or a forced scale), and two consecutive such results close the door.
* **Compute.** One core at nice 10, 121 MB. The real run took 556 s (dominated by the Monte Carlo); MUTATE took 16 s. Never say "theory closed".

## Attempt count and ledger row

* This is post-ledger alpha attempt **#1**. All 13 variants were pre-declared and graded, so **N_mech goes from 359 to 372**, the conservative reading of rules §3. The campaign now has 102 ledger attempt rows (101 + 1) and 0 derivations.
* Campaign-wide precision demanded for a single coupling: 4.9e-7 under the stricter reading (K = 13, N = 360), or 6.2e-6 under the other reading (N = 372). No variant came within orders of magnitude of either.
* Row for `ALPHA_ATTEMPTS_LEDGER.md`, reported to that ledger's owner (this lane edits no other lane's files):

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| CFG896 | SEL | campaign_fresh_gravity/CFG896_alpha_D02_higgs_boundary | Door D02: Higgs boundary condition (lambda = 0, beta_lambda = 0, one-loop Veltman, MPP at free mu*; M_P / M_red) solved for g_Y(M_t), and pairs for (g_Y, g_2) jointly with M_W; Y1 running | S3 162.06 ± 2.45, S6 149.32 ± 1.55 (beta_lambda = 0 at M_P / M_red); no value from the other 11 | 11 NOT DIAGNOSTIC (pre-flight sigma(1/alpha(0)) 2.4–14 > 1.37: weak g_Y leverage against the m_t and alpha_s errors; joint alpha–M_W predictions 98% correlated, so they are not two tests); 2 KILLED (+10.2, +7.9 sigma). As frozen, the first run was NOT COMPLETED (3 gates; amendments A1–A4 post hoc) | 13 | cfc23448b / b2fa5ad0d / the run commit of this lane |

## Files

| File | Contents |
|---|---|
| `CFG896_PREREGISTRATION.md` | Frozen criteria (commit cfc23448b, committed alone before any script), plus post-hoc amendments A1–A4 (commit b2fa5ad0d, written after the first run and before the amended run). |
| `cfg896_preflight.py` | Gates K1–K7, the pre-flight for all 13 variants, the Monte Carlo cross-check, and the solving stage for variants that pass. |
| `cfg896_preflight.out`, `cfg896_preflight.json` | The amended real run (exit 0). |
| `cfg896_preflight_MUTATE.out`, `cfg896_preflight_MUTATE.json` | The MUTATE control (exit 1). |
| `cfg896_preflight_FIRSTRUN.out`, `cfg896_preflight_FIRSTRUN.json` | The first run under the frozen gates (exit 1: K5, K6 and K7(ii) failed), kept unchanged. |

Run: `OMP_NUM_THREADS=1 nice -n 10 python3 cfg896_preflight.py` for the real run (about 9 minutes, mostly the Monte Carlo), and `... cfg896_preflight.py MUTATE` for the control (about 16 s). Both use one core and about 120 MB.

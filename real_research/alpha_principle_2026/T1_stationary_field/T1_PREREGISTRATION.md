# T1 -- an INVENTED principle: a self-sustained electric field in de Sitter space (pre-registration)

Written 2026-09-29 BEFORE `t1_stationary_field.py` was run. This lane exists because the user asked for an invented principle. The distinction
that governs it: inventing a HYPOTHESIS and testing it is legitimate; a principle conceived after seeing alpha = 1/137 cannot gain credibility
by fitting 137, only by predicting something it was not built to fit.

## The invented principle (P1)

In dS_4 a constant physical electric field E dilutes as a^-2 unless the vacuum supplies a current. From the divergence of the field tensor
(nabla_nu F^(nu z) = -2 E H / a, verified symbolically in AH4 check V3) the current needed to sustain constant E is |J| = 2 E H, directed so as to
ANTI-screen the field. In the on-shell renormalization (alpha = the measured Thomson value; the scheme of AH4/Q1) the renormalized linear
conductivity is sigma/H = alpha * G(M) with M = m/H. P1 states: **the stationary (self-sustained) field exists exactly when sigma = -2H, i.e.
alpha * G(M) = -2**, which for a charged species is one equation in (alpha, M). If P1 were a principle of nature, alpha would be fixed by the
lightest charged species' mass in horizon units.

## Declared criteria (before running)

* P1 has power only if it can be satisfied by a KNOWN charged fermion (electron, muon, tau, quarks) at its measured M = m/H_0 within a factor 2.
* The scalar has G_s > 0 (screening) in the AH4 convention; the Dirac fermion has G_f < 0 at every M (Q1). So only a fermion can sustain the field.
* Required outputs: (i) the M* that solves alpha G_f(M*) = -2 at alpha = 1/137.036, and the corresponding mass in eV for H = H_0;
  (ii) |alpha G_f| for the actual electron, muon, tau, top; (iii) the factor by which the known species fall short;
  (iv) the small-M identity: alpha G_f = -2  <=>  ln(1/M) = 3 pi/(2 alpha) + gamma_E - 1/6, i.e. H is the QED Landau-pole scale of that fermion to a scheme constant.
* Expected outcome (stated in advance): P1 FAILS for every known charged fermion by a huge factor; the required M* is ~1e-281 (a fermion 300 orders lighter than H),
  so P1 is a dead invention. It is reported as such; it is not rescued by any choice.

## Reading rules
alpha stays an INPUT; kappa = 1/2 FITTED; scope is the dS_4 single Dirac fermion, minimal coupling, planar patch, in-vacuum, first order in E, no backreaction on H.
The on-shell scheme is what makes sigma's sign meaningful (a finite counterterm shifts sigma by a constant times H).

## Amendment 1 (2026-09-29, after the first run, disclosed)

First run (kept as `t1_stationary_field_FIRSTRUN.out`): checks C1 and C2 FAILED and the table showed a suspiciously flat |alpha G_f| ~ 1e-42 for all four species. Diagnosis, run before any
change: at M ~ 1e38-1e44 the quantity ln M - Re psi(iM) must cancel to ~ -1/(12 M^2) ~ 1e-79; at 40 digits of precision it returned 5.7e-40 (garbage) while at >= 90 digits it returns -6.5975685e-79
(the expected value). The failure was in MY script's precision, not in the physics and not in a threshold. Change made: mp.dps 40 -> 250. No criterion or threshold was changed
(C1, C2 keep the declared '1e70'). My in-head estimate of the shortfall (~80 orders) was in the right range; the pre-registration did not state a number.

## Amendment 2 (2026-09-29, after an independent re-run; disclosed, no result changed)

(a) The control was tightened: `--mutate` now exits 1 only if EXACTLY check B1 fails, and exits 3 if the control is broken (it previously counted ANY failed check as 'control works'). A first attempt compared full check labels
instead of check IDs and wrongly reported 'broken'; fixed to compare IDs. (b) The status wording 'falls short by 1e81 or more' is corrected to: the electron falls short by a factor of 9.8e80 (about 1e81); the muon, tau and top by more.

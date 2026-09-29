# Lane A -- gravity-charge relations (WGC, Dirac + extremality, RN-dS special points): pre-registration

Written 2026-09-28 BEFORE any script in this directory was run. Only literature abstracts were fetched beforehand (see "Sources actually read").
Amendments, if any, are appended below the last section, never edited in place.

## Question

Is there a FORCED EQUALITY (not an inequality) between the minimal charge e and Planck/cosmological units, without introducing a particle mass,
that could fix alpha? Target: alpha = 1/137.035999177 (Thomson limit). Scale statement is part of every claim (see S7).

## Setup (declared)

Units hbar = c = 1, l_P^2 = G. Geometric charge Q^2 = G q^2 (Heaviside-Lorentz q, alpha = e^2/4pi), so the elementary electric charge has Q_e^2 = alpha l_P^2.
Dirac (HL): e g = 2 pi n, so the magnetic geometric charge is Q_m^2 = G g^2/(4 pi) = n^2 l_P^2/(4 alpha).
Reissner-Nordstrom-de Sitter: f(r) = 1 - 2M/r + Q^2/r^2 - Lambda r^2/3 (G=1 geometric mass M). x = Lambda l_P^2 = 2.85e-122 (AH5).

## Hypotheses and declared checks (script -> criterion)

### a1_rn_ds_special_points.py  (symbolic RN-dS structure)
* S1: the degenerate-root system f = f' = 0 is solved exactly by the one-parameter curve y = Lambda r0^2:  Q^2 = r0^2 (1-y),  M = r0 (1 - 2y/3).
  The branch is cold/extremal for y < 1/2, ultracold (triple root, f=f'=f''=0) at y = 1/2, charged Nariai (r_+ = r_c) for 1/2 < y < 1; y = 1 is Schwarzschild-dS Nariai (Q = 0).
  PASS if the sympy identities reduce to 0 and a numerical root-multiplicity count on 9 sample y-values matches the labels.
* S2: Q^2 Lambda = y (1-y) <= 1/4 with equality only at the ultracold point (Q^2 = 1/(4 Lambda)), and the extremal charge-to-mass ratio z_ext = Q/M = sqrt(1-y)/(1-2y/3) lies in [1, 3/(2 sqrt 2)].
  PASS if exact. STATED CONSEQUENCE TO CHECK: every special charge value of RN-dS is a pure number times Lambda^(-1/2) (or the M-linked Lambda^0 ratio z in [1, 1.0607]); no special charge value contains a number ~ alpha.
* S3: T = 0 on the cold branch, T_+ = T_c on the Nariai branch (symbolic).
* MUTATE: Q^2 = r0^2 (1-2y). Must FAIL S1.

### a2_dirac_extremal_and_handles.py  (Dirac + extremality, equalities only)
* D1: Q_e Q_m = n l_P^2 / 2 exactly and independent of alpha, in BOTH Gaussian and HL unit bookkeeping (symbolic). PASS if both give the same alpha-free product.
* D2: extremal (Lambda = 0) magnetic BH of n Dirac quanta: r_+ = Q_m = n l_P/(2 sqrt alpha), M = n m_P/(2 sqrt alpha), A = pi n^2 l_P^2/alpha, S = A/(4 l_P^2) = pi n^2/(4 alpha).
  Also the electric n=1 extremal object: r_+ = sqrt(alpha) l_P (sub-Planckian). Report numbers at alpha = 1/137.036. These are RE-EXPRESSIONS of alpha, valid only if a value of M, r_+, A or S is independently forced.
* D3: self-dual point Q_e = Q_m gives alpha = n/2 (n = 1: alpha = 1/2). PASS = computed; a hit requires within 1e-3 of the target (declared expectation: NO).
* D4 (dS capacity): a RN-dS object carries at most N_max = 1/(2 sqrt(alpha x)) electric quanta (ultracold), and equating n quanta to any special charge gives alpha = c^2/(n^2 x) with c a pure number from S2.
  Report N required at the target. Verdict rule: alpha is fixed by this only if the integer n is forced; a 1e-3 window in alpha contains ~ 1e58 integers, so a fit to alpha is automatic and carries zero evidence. FAIL as a route unless n is forced by something else.
* D5 (handles on k = r_+/l_P of the minimal magnetic extremal BH, alpha = 1/(4 k^2); fixed list, declared now): k in {1, 2, sqrt(8 pi/3), Z = 2 sqrt(8 pi/3), 2 pi, 4 pi, Z^2 = 32 pi/3} (7 handles, the AH6 list re-used) plus the integer route k = N/2 for the two nearest integers N = 11, 12 (2 handles) plus the self-dual alpha = 1/2 (1 handle). TRIAL COUNT = 10.
  A handle HITS if |alpha_handle/alpha - 1| < 1e-3. Required k = 1/(2 sqrt(alpha)) = 5.853 is REPORTED, not fitted. Expected chance hits: each handle has probability 2 * 5e-4 / ln(100) = 2.2e-4 of landing in the window if k is log-uniform over [1,100] (declared prior), so E[chance hits] = 10 * 2.2e-4 = 2.2e-3.
  Declared expectation: no hit. Post-hoc remark allowed but NOT scored: Z = 5.7888 is within 1.1% of the required k (not a hit at 1e-3); the numerology 1/alpha = 4Z^2+3 (FDR-dead) is 1/(4 alpha) = Z^2 + 3/4 here, i.e. it needs an unexplained additive offset.
* MUTATE: Dirac condition with 4 pi instead of 2 pi (wrong quantum). Must FAIL D1.

### a3_inequalities_and_scale.py  (honest inequality table + scale)
* I1: WGC (hep-th/0601001, as read: an inequality, a charged particle with mass/charge below the extremal ratio). In HL geometric form z = e q M_Pl,red sqrt2 / m >= 1 (O(1) convention flagged). Compute the electron's margin. Inequality only -> cannot fix alpha.
* I2: Lambda-corrected extremality is still bounded by z_ext <= 1.0607 (S2), so the WGC threshold cannot move by more than 6% and never depends on x at any visible order. Report the Lambda-induced shift for a Planck-size and a Hubble-size object.
* I3: Festina Lente (2106.07650 abstract read: a LOWER BOUND on charged-particle mass from charged Nariai BHs, O(1) constant not fixed in what was read). Margin computed with the constant set to 1 and to 10 (flagged as convention; not scored).
* I4: BPS/supersymmetric saturation is an equality but is NOT tested here (needs SUSY and leaves the gauge coupling a modulus); stated as scope.
* I5 (scale): the BH-scale relations of D2 hold for the coupling at mu ~ 1/r_+ ~ Planck scale, not the Thomson value. Report a fermion-only one-loop QED running of alpha from the electron mass to m_P using standard fermion masses as INPUTS (no mass is derived; SM mass sector stays walled), only to show the size of the scale mismatch. Reported, not scored, and not a claim about the true SM alpha(m_P).
* MUTATE: swap the inequality direction of WGC (z <= 1). Must FAIL I1 for the electron.

## Overall pass/fail (declared)

* The route yields a FORCED PRINCIPLE for alpha only if: (i) an equality among {extremality, Dirac, RN-dS special points, WGC saturation} gives alpha with no free integer, no mass and no choice made after seeing the target; (ii) its scale is stated; (iii) the trial count and chance-hit expectation are as declared here.
* DECLARED EXPECTED OUTCOME: NO. Reason (to be checked, not assumed): the only equalities are extremality (needs a mass or a size) and Dirac (alpha-free product); together they only trade alpha for r_+, M, A or S of the minimal extremal object. The RN-dS special points add charges of size Lambda^(-1/2), 122 orders from Planck, and pure-number ratios z <= 9/8 from which no alpha follows. Everything else (WGC, FL) is an inequality.

## Scope / not tested

Higher-derivative corrections to extremality (free coefficients), SUSY BPS towers, dilatonic and non-abelian charges, string-theory towers (sublattice WGC), radion or moduli dependence, running of alpha with a real spectrum, quantum corrections to the semiclassical BH at r ~ few l_P. kappa = 1/2 stays FITTED; the SM mass sector stays walled; no dark-matter particle.

## Sources actually read (abstract pages only, via WebFetch)

hep-th/0601001 (Arkani-Hamed, Motl, Nicolis, Vafa): WGC is an inequality (light charged states with mass/charge below extremal BH ratio).
2106.07650 (Montero, Vafa, Van Riet, Venken): FL bound, a lower bound on charged-particle masses from charged Nariai BHs; O(1) constant not visible in the abstract page.
hep-th/0304042 (Polchinski): completeness principles; Dirac's monopole implies charge quantization, the converse discussed. It concerns which charges exist, not the value of e.
Full texts were NOT read; formulas in a1-a3 are derived symbolically, not quoted.

## Amendment 1 (2026-09-28, appended after the first run of a3; a1 and a2 unchanged except one check noted here)

Bugs and a misleading illustration found on first run, all in my own scripts; no physics conclusion of a1/a2 changes.
* a1: the final "consequence" check was vacuous (`True`). Replaced by a real check that Q^2 Lambda on the special curve has only the free symbol y. Rerun: 14/14 pass, MUTATE exits 1.
* a3 I2b: the first run FAILED because 30-digit arithmetic cannot resolve z_ext - 1 ~ 1e-122 (a precision bug, not physics). Fixed with 500-digit arithmetic for that quantity.
* a3 I1c: was vacuous (`True`); turned into a printed statement.
* a3 I5: the fermion-only one-loop QED running I first declared was MISLEADING (it gave 1/alpha(m_P) = 59.8 because it omits the W and Higgs sectors, which cancel most of the running above m_Z).
  Replaced by the one-loop SM running of alpha_Y^-1 + alpha_2^-1 from measured m_Z inputs (b_Y = 3/5 * 41/10, b_2 = -19/6). Reported, not scored except as a scale-size statement (I5a, I5b).
  Post-hoc note (NOT scored): with alpha(m_P) ~ 1/132, the required k is ~ 5.75, about 0.6% from Z = 5.7888. This rests on an approximate one-loop spectrum-dependent input and was noticed after seeing the numbers; it is not a hit at the pre-registered 1e-3 and not a derivation.

## Amendment 2 (2026-09-28, correction of a bug found by the red-team lane M; disclosed)

`a3_inequalities_and_scale.py` line 77 used b_Y = (3/5)(41/10) = 2.46. Since alpha_1 = (5/3) alpha_Y, the hypercharge coefficient is b_Y = (5/3)(41/10) = 41/6 = 6.83, which lane M derived independently from field content (m1_lane_a_running_check.py) and which lanes B and F already had. Effect: 1/alpha_em(m_P) is 104.94, not 132.39; the required minimal-object size at m_P is k = 5.12, so Z = 5.7888 is 13% away, NOT 0.6%. The lane's post-hoc remark ('within 0.6% of Z') was produced by the bug and is VOID. It was repeated in lane D's commit message (1d23899e6) and in ALPHA_CHAIN_STATUS.md (corrected there). Changes made now: the b_Y line, and the I5a range check widened from 1%-10% to 1%-30% because the correct shift from m_Z is -18% (that widening is a consequence of the corrected number, disclosed here, not a tuned outcome). The a3 outputs were regenerated (.out and _MUTATE.out); the real run exits 0 and the MUTATE control exits 1. No verdict of the lane changes: the bug created a spurious hint, it never closed a branch.

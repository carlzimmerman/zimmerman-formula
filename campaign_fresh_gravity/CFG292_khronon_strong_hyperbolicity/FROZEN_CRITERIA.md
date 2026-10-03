# CFG292 — FROZEN CRITERIA: strong hyperbolicity of GR + the BPS khronon (C-H/K principal symbol) and criterion-B cone compatibility

Frozen 2026-10-02, before any CFG292 script was written or run. Nothing below may be edited after the
commit that adds this file; corrections go in a dated section appended at the end.

Item addressed: XC2's OPEN item ("strong hyperbolicity of GR + the BPS khronon on arbitrary nonlinear
backgrounds", `real_research/extra_crispy_2026/XC2_wellposedness_scoping.py`, SCOPE paragraph), i.e. the
Cauchy-problem obligation of recipe G4/G5 and the 2026-09-26 user decision "causality = criterion B"
(`qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md`, user-decision block; §§5, 6, 8, 11).

## 1. The system (taken from committed files, not chosen here)

- **Action.** L340 (`real_research/g03_audit_2026/L340_filtered_khronon_completion.py`, docstring):
  I_CHK = I_CH + c^3/(16 pi G) Int sqrt(-g) [ alpha_c a_mu a^mu - c_2 K^2 ], beta = 0 (c_T = 1), the
  Horava parameter lambda_K = 1 + c_2. a_mu = h_mu^nu d_nu ln N, K = nabla_mu n^mu, n_mu = -N d_mu tau,
  N = X^(-1/2), X = -g^{mu nu} d_mu tau d_nu tau (C-H's own clock, `qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md`).
  L350 G5's leaf-average form -c_2 (K - <K>)^2 differs only in the k = 0 projection (finite rank), so it has
  the same principal symbol; this is stated, not re-derived.
- **Principal part.** The claim to be used: the principal symbol of C-H/K is that of
  sqrt(-g) [ R - beta K_mu nu K^mu nu - c_2 K^2 + alpha a_mu a^mu ] (BPS khronometric form, alpha = alpha_c,
  beta = 0 for the chassis; beta is kept symbolic only to state conditions). It rests on three committed results,
  which are re-verified in-lane (check R0) before use:
  - XC2 B5: the linearised MOND operator S^T D^T C D S is order -infinity (smoothing);
  - XC1 A3: eliminating U gives the clock inertia 2C/(1+C), and U = ln N makes the C-H term vanish identically;
  - XC6 D3/D4: the filter's own metric variation delta S puts no derivative on a hard leg; principal symbol with
    delta S retained = GR + BPS.
- **R0, the in-lane re-verification (load-bearing).**
  (a) read XC2's committed results JSON and confirm B5 passed with its own rule (monotone fall, < 1e-4 at K = 4/xi,
  bounded prefactor); read XC6's committed JSON and confirm D3, D4 passed;
  (b) sympy: the frozen-coefficient symbol of S^T D^T C D S is e^{-xi^2 |k|^2} k^T C k with
  C = C_T (1 - e e^T) + C_L e e^T; its ratio to the Einstein-Hilbert principal part |k|^2, times |k|^n, tends to 0
  for every n (order -infinity), for bounded C;
  (c) sympy: the U-elimination Schur complement is 2 C E/(1 + C E) |k|^2 |delta ln N|^2 with E = e^{-xi^2 |k|^2}
  (order -infinity as an inertia correction, positive for C > 0);
  (d) nu_mono's C_T, C_L rebuilt as in L340 A1; C_T = nu - 1 is bounded on y >= y_min > 0 and unbounded as y -> 0.
  **Disclosed limitation, frozen now:** where the filtered field vanishes C_T ~ y^(-1/2) diverges, so the
  frozen-coefficient smoothing statement fails pointwise there (XC2 B7: Lipschitz at isolated zeros,
  log-Lipschitz at planar ones; XC5: open zero-field regions are Hoelder-1/2, no linear theory). The scope of
  every result below excludes open zero-field regions.
- **Parameter values (committed, not scanned).**
  alpha_c window (9.624e-14, 3.2e-9) and c_2 window (7.289e-3, 0.0667) from
  `real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json` (numbers.P1);
  the six Planck-era c_2 ceilings from `real_research/g03_audit_2026/L350_chk_cosmological_G_gate_results.json`
  (numbers.G2.rows[].c2_ceiling), as XC1 A4 used them; the recipe §9 edge lambda_K <= 1.10 (c_2 = 0.10).
  Evaluation points = {alpha_min, alpha_max} x {the six L350 ceilings, c2_min, c2_max, 0.10}: 18 record points.
  Values enter exact arithmetic as rationals rounded to 6 significant digits (disclosed; conditions are sign /
  non-degeneracy conditions, so the rounding cannot move a verdict unless a point sits on a degeneracy locus,
  which is checked).
  XC1 A9's UV khronon speed range 4.4e2 - 7.9e5 c is the comparison number for the scalar speed.

## 2. Formulations

Common machinery. g = gbar + h, tau = taubar + pi, frozen (constant) background (gbar, d taubar). The khronometric
Lagrangian is exactly a quadratic form in the jets J = (d g, d d tau) with coefficients depending on (g, d tau)
only; the EH term in Gamma-Gamma form is quadratic in d g with g-dependent coefficients. Therefore the principal
symbol at any point of any background is the Hessian of this quadratic form at (g, d tau) of that point: the
constant-background computation IS the general frozen-coefficient symbol. Symbol: substitute d_l h_mn -> xi_l H_mn,
d_l d_s pi -> xi_l xi_s Pi (and d_l du^m -> xi_l U^m for the aether control) and take the Hessian P(xi).
Gauge-fixing term -c_gf sqrt(-gbar) gbar^{mu nu} C_mu C_nu with the de Donder vector
C_nu = gbar^{ab}(d_a h_{b nu} - 1/2 d_nu h_{ab}); c_gf is FIXED by the GR control (the value that makes the GR
symbol proportional to gbar^{mu nu} xi_mu xi_nu) and never tuned afterwards.

- **F1 (covariant, harmonic gauge, khronon retained).** Full de Donder gauge fixing on h; pi dynamical. The
  khronon row/column carries a leaf-elliptic factor (h^{mu nu} xi_mu xi_nu); it is removed by the order reduction
  pi~ = |nabla| pi (Douglis-Nirenberg / Leray-Volevich weights t_h = 2, t_pi = 3; the k = 0 mode of pi is the
  tau -> f(tau) relabelling, a gauge). Hyperbolicity is tested with respect to the leaf conormal d tau. F1 is a
  linear check about tau-aligned backgrounds; it is not a nonlinear scheme (its harmonic time is not tau).
- **F2 (leaf-sliced; the formulation that carries the verdict).** Unitary time gauge t = tau (pi = 0); the spatial
  diffeomorphisms are fixed by the spatial components of a de Donder vector, gauge term
  -c_gf N sqrt(gamma) gamma^{ij} C_i C_j:
  - F2a: C_i = d^mu h_{mu i} - 1/2 d_i (gbar^{ab} h_ab) (4-D trace; = the spatial harmonic coordinate condition);
  - F2b: C_i = d^mu h_{mu i} - 1/2 d_i (gamma^{jk} h_jk) (spatial trace).
  The lapse h_00 is eliminated through its leaf-elliptic equation (Schur complement); this requires
  P_{00,00}(k) != 0 for k != 0 and P_{00,00} independent of xi_0 (checked).
- **Einstein-aether control system.** sqrt(-g)[R - c1 nabla_a u_m nabla^a u^m - c2 (nabla.u)^2
  - c3 nabla_a u^m nabla_m u^a + c4 a^2] (signature -+++ form of Jacobson & Mattingly 2004), unit constraint solved
  (delta u^0 = h_00/2 on the aligned background), full de Donder gauge.

## 3. Tests (per formulation, at every evaluation point)

The second-order (after the elliptic reductions) symbol is written P(xi_0, k) = A xi_0^2 + B xi_0 |k| + C |k|^2,
first-order reduction M(khat) = [[0, I], [-A^-1 C, -A^-1 B]] (variables |k| u, d_t u).

- T1 characteristic determinant: det P factored block by block (helicity decomposition about khat = z with u
  aligned; block-diagonality verified, not assumed); every factor identified (tensor, scalar, gauge/constraint,
  leaf-elliptic).
- T2 A invertible.
- T3 every eigenvalue of M real.
- T4 complete eigenvectors: for every distinct eigenvalue, geometric multiplicity = algebraic multiplicity (exact
  rational/algebraic arithmetic).
- T5 uniformity in khat: on the full (unsplit) matrices, at >= 5 random unit khat (mpmath, 60 digits), the
  eigenvalues and the condition number of the eigenvector matrix equal those at khat = z to relative 1e-20.
- **Strongly hyperbolic <=> T2 and T3 and T4 and T5.**
- T6 general frozen background: constant gbar with lapse != 1, non-zero shift, non-diagonal gamma_ij, tau = t:
  every characteristic root obeys (xi_0 - N^i k_i)^2 = N^2 s^2 gamma^{ij} k_i k_j with s in the aligned speed set,
  the leaf-elliptic factor is proportional to gamma^{ij} k_i k_j, and T3/T4 repeat numerically (F1 and F2a).
- T7 non-leaf slicing: constant aether boosted (v = 3/5) relative to the coordinate time: for k perpendicular to v,
  det P(xi_0, k) has non-real roots xi_0 (expected from the leaf-elliptic factor), i.e. the Cauchy problem must be
  posed on tau-leaves. If instead all roots are real, that is reported as found.
- CB criterion B: for every mode the cone is Q_A(xi) = (u.xi)^2 - s_A^2 h(xi, xi) with 0 < s_A^2 < infinity, all
  sharing the axis u; Q_A(d tau) > 0 (every leaf spacelike for every finite cone, however large s_A); the
  leaf-elliptic factor h(xi, xi) >= 0 with kernel span(d tau) only (degenerate cone lying in the leaf, explicitly
  allowed by the user decision); future-directed rays have d tau > 0. The scalar speed range over the 18 points is
  compared with XC1 A9.

## 4. Controls (each can fail; a control that does not behave as stated fails the run)

- C1 GR alone (no khronon, alpha = beta = c_2 = 0, metric only), full de Donder: strongly hyperbolic (T2-T5),
  all speeds 1.
- C2 minimal Horava (alpha = 0, beta = 0, c_2 = c2_max): NOT strongly hyperbolic in F1 and in F2a (expected: A
  singular after the elliptic reduction, the scalar's xi_0^2 coefficient vanishes; Jacobson & Pulakkat 2025,
  J. Phys. A 58 315404: a mode obeying an equation first order in time, and a failed Cauchy problem after shell
  collapse). The control fails if it comes out strongly hyperbolic.
- C3 Einstein-aether test point (c1, c2, c3, c4) = (1/10, 1/5, 1/20, 1/30) (arbitrary, non-special): the
  characteristic factors reproduce, exactly, s_2^2 = 1/(1 - c13), s_1^2 = (2 c1 - c1^2 + c3^2)/(2 c14 (1 - c13)),
  s_0^2 = c123 (2 - c14)/(c14 (1 - c13)(2 + c13 + 3 c2)) (Jacobson & Mattingly 2004 PRD 70 024003 Table 1;
  Jacobson 2008 arXiv:0801.1547 eqs 11-13); and the khronometric scalar factor found in T1 equals s_0^2 under
  (c14, c13, c2) -> (alpha, beta, c_2) (Guemruekcueoglu, Saravani & Sotiriou 2018 eq. 4, used by XC1).
- C4 MUTATE (environment MUTATE=1): alpha_c -> -alpha_c at every point. Expected: non-real characteristic speeds
  (c_S^2 < 0), strong hyperbolicity fails, exit code 1. Outputs go to *_MUTATE files.
- C5 degeneracy probe (disclosure only, not load-bearing): one point with c_S^2 = 1 (the gauge speed); report
  whether a Jordan block appears (Sarbach, Barausse & Preciado-Lopez 2019 CQG 36 165007 need lambda_S^2 != 1).

## 5. Conditions

The conditions on (alpha_c, beta, lambda_K) and on the speeds are DERIVED, not assumed: symbolic factorisation of
the block determinants, symbolic generic nullity at each eigenvalue, and the parameter loci where generic pivots
vanish (checked at C5). They are reported as found.

## 6. Decision rule (recipe §6 vocabulary, exactly one)

- **CONDITIONAL** if: F2a or F2b is strongly hyperbolic at all 18 points, F1 is strongly hyperbolic at all 18
  points with the same physical speeds, T6 and CB hold, R0 re-verifies, and C1-C4 behave. Scope label, mandatory:
  linearised, frozen-coefficient, high-frequency principal symbol; the stated gauge; filtered field non-vanishing.
  Not PASS, because nonlinear local well-posedness (smooth symmetriser for the quasilinear system, constraint
  propagation, the elliptic-hyperbolic coupling theorem) is not proved here and open zero-field regions are
  excluded.
- **KILL** if a gauge-invariant failure occurs at a record point with the controls behaving: a non-real physical
  speed, or a singular physical-sector leading coefficient.
- **OPEN** if the physical speeds are real and non-degenerate but no pre-registered formulation is strongly
  hyperbolic (Jordan blocks in the gauge sector only), or if a control misbehaves, or if R0 fails.
- Both F2 variants are reported whatever happens; neither is dropped after the fact.

## 7. Wording rules

Never "theory closed", "well-posed theory", "data favour the framework" or "kappa derived"; kappa = 1/2 is FITTED
and is not used here. Per recipe §11: "no ill-posedness in the tested sector and scope", never "well-posed".
Literature look-ups were made through a summarising web fetch of arXiv abstract / HTML pages and are PROVISIONAL
as quotations (the speed formulas are additionally checked by C3's exact algebra).

---

## Appended 2026-10-02, after the run (the frozen text above is unchanged)

Five disclosures. None of them changes a test or the decision rule.

1. **T5 implementation.** The frozen T5 named mpmath eigenvalues at random khat. In the first run `mpmath.eig` failed to
   converge (QR iteration) on the defective F1 companion matrices. T5 was therefore run with exact arithmetic instead:
   the unsplit pencils at z and at 5 random rational unit vectors (rational parametrisation of the sphere, exactly unit),
   with exact roots, multiplicities and nullities. The condition number of the eigenvector matrix is still computed in
   mpmath at 60 digits, from eigenspace-orthonormal bases built at the exact roots. The comparison is now exact, which is
   stronger than the frozen 1e-20 tolerance; the condition-number tolerance is unchanged.
2. **T6 implementation.** The bivariate determinant in (xi_0, s) was too slow. It is replaced by univariate determinants
   at s = 1 and s = 2: the cone division is exact at both, and the left-over factor is xi_0-free with q(2)/q(1) = 4,
   i.e. proportional to s^2 gamma^{ij} k_i k_j. The overall factor sqrt(-gbar) is divided out first.
3. **C5 outcome.** At c_S^2 = 1 the merged eigenvalue of F2a stays semisimple (multiplicity 3, nullity 3). So, unlike
   the Einstein-aether tetrad formulation of Sarbach, Barausse & Preciado-Lopez, c_S != 1 is NOT a condition in F2a.
4. **Speed range.** Over the 18 points the scalar speed is 443.8 .. 9.505e5 c. The top value comes from the recipe edge
   c_2 = 0.10 at alpha_min, a point XC1 A9 did not include (XC1's range is 443.8 .. 7.936e5 c).
5. **A gap in the sec. 6 decision rule.** Sec. 2 designates F2 as the formulation that carries the verdict, but the
   sec. 6 CONDITIONAL clause also requires F1 to be strongly hyperbolic.
   - The run found F2a strongly hyperbolic at all 18 points. F1 and F2b are only weakly hyperbolic: there is a Jordan
     block at the gauge speed 1, in the gauge/constraint sector only, and the physical speeds are simple and identical.
   - So the CONDITIONAL clause is not met, as written. Nor is the KILL clause (no gauge-invariant failure). Nor is the
     OPEN clause's first branch, because a pre-registered formulation IS strongly hyperbolic.
   - The script therefore reports the frozen-rule result as an OPEN fall-through and states that a post-hoc reading
     would be CONDITIONAL. Which reading stands is for the owner to decide. The rule is not re-written here.

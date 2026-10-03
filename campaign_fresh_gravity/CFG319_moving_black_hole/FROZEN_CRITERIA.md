# CFG319: the slowly moving black hole (gate G11's named condition) for the filtered C-H/K chassis. FROZEN CRITERIA

Lane CFG319. Written and committed before the lane script exists. Verdict words: PASS, CONDITIONAL, KILL, OPEN.
Standing rules: kappa = 1/2 is FITTED; no knob scans and no fitting (alpha_c and c_2 are read from committed files);
nothing here says the theory is closed or that the data favour the framework; the cold mass the CMB needs is
untouched and still required.

## 0. What was read before freezing, and the not-blind statement

Read: CFG318's FROZEN_CRITERIA, README and script (chassis map, static O(alpha) solution, dipole logic); CFG311's
README and script (khronon sensitivity normalisation, s = alpha sigma1).

Literature, through a summarising fetch tool (arXiv abstract pages, ar5iv HTML, the arXiv export API); values and
wording are PROVISIONAL, the summariser is not the paper. No PDF was fetched.
- **Ramos & Barausse 2019** (PRD 99 024034, arXiv:1811.07786). Khronometric action
  S = -(1/16 pi G) Int sqrt(-g) [R + lambda (div u)^2 + beta grad_mu u^nu grad_nu u^mu + alpha a.a]. Slowly moving BHs
  at O(v): four potentials after gauge fixing (an ODE system of total order 7 plus two Bianchi constraints); singular
  points at the matter horizon (their coordinates), the spin-0 horizon and the universal horizon (UH). Integration
  outward from the matter horizon; a two-parameter regular family there, one after rescaling; asymptotic flatness with
  the khronon moving at -v then over-determines the problem. Imposing regularity at both the matter and spin-0
  horizons leaves no free constant; imposing it at the spin-0 horizon moves the curvature singularity to the UH (their
  Fig. 2; the abstract says "curvature singularities at the universal horizon"). Numerical point
  (alpha, beta, lambda) = (0.02, 0.01, 0.1), sigma ~ 1e-3 there; small non-zero alpha, beta were not explored. At
  alpha = beta = 0 the khronon is stealth, the BH is boosted Schwarzschild, sensitivities vanish. The summariser did not
  report Frobenius exponents or the power of the divergence.
- Franchini, Herrero-Valea & Barausse 2021 (PRD 103 084012, arXiv:2103.00929): regular slowly moving BHs "require
  alpha and beta to vanish exactly" (citing RB2019); at alpha = beta = 0 spherical collapse forms a regular UH (the
  limiting surface of maximal slicing); nothing on small non-zero alpha, beta.
- Saito & Kobayashi 2024 (arXiv:2408.14004): slowly moving BHs in a higher-order scalar-tensor extension of
  khronometric theory are regular outside the UH (a different theory; context only).
- Bhattacharjee, Mukohyama, Wan & Wang 2018 (arXiv:1806.00142): spherical collapse in Einstein-aether forms regular
  universal horizons (context for the formation argument).
- Barausse, Jacobson & Sotiriou 2011; Blas & Sibiryakov 2011; Barausse & Sotiriou 2012/13: as read for CFG318.

**Not blind.** Before this file, scratch work (not committed; disclosed in the README) did the following:
- derived the test-khronon equations of section 2 in sympy, including the beta term;
- found the Frobenius exponents: at the spin-0 horizon {0, 1, 1, 2} (one logarithm); at the UH, for alpha > 0,
  {-1, 0, s+, s-} with s(s+1)(2 y1^2 s^2 + 2 y1^2 s - (W0^2+1)^2) = 0, s+ ~ 0.63, s- ~ -1.63; at alpha = 0,
  {sqrt2-1, sqrt2-2, -1-sqrt2, -2-sqrt2};
- ran the matching at lambda = 0.05 for alpha = 1e-3 ... 1e-7 (outside the window). No fully regular solution was
  found. With the r_S logarithm and the s- mode removed, the s+ amplitude was O(1) (-2.3 to -3.2 in M units), with no
  clean trend. With the s+ mode removed instead, the s- amplitude was ~alpha.
- found and fixed two bugs: a wrong spin-0-horizon series routine (wrong at 3e-6), and a null-space extraction that
  took the wrong singular vectors.

No window point was computed before this freeze. The decision rule below was written knowing all of the above.

## 1. Chassis and window (CFG318's map)

alpha = c14 = alpha_c, beta = c13 = 0, lambda = c2 = c_2, read from
`real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json` (P1): alpha_c in [9.624e-14, 3.2e-9],
c_2 in [7.2888e-3, 0.0667].

**Scored points W5:**
- the four corners;
- the geometric centre (alpha_c = 1.755e-11, c_2 = 0.02204).

**Readings:**
- the alpha ladder at lambda = 0.05 (1e-3 ... 1e-7);
- the control points in section 4.

## 2. Equations (derived in-lane with sympy)

- **(E1) Test-khronon limit.** The khronon on fixed Schwarzschild (ingoing EF, M = 1), with
  L = sqrt(-g) [-lambda K^2 - beta K_{mu nu}K^{mu nu} + alpha a.a], u_mu = -N d_mu T, K_{mu nu} = grad_mu u_nu + u_mu a_nu.
  - Neglected, and stated as the lane's scope:
    - the metric response (O(alpha) outside the boundary layer of width delta ~ 0.61 M/c_S around the UH);
    - the O(lambda) metric mixing inside that layer (the 2 + 3 lambda in the full c_S).
  - At the UH itself the leading coefficients are pure alpha-terms (section 3). The UH exponents therefore depend on
    the metric only through W0 and y1 (argued, not proven, to make them robust).
- **(E2) Static background.** T = v + H(r), Y = -u.chi, W = -u^r = sqrt(Y^2 - e), e = 1 - 2/r. A second-order ODE in
  Y (equivalently in W) depending on (alpha, lambda + beta).
  - Regularity at the spin-0 horizon r_S, where alpha W^2 = (lambda + beta) Y^2, selects a one-parameter family.
  - The no-growing-K condition at infinity (W ~ C/r^2) fixes it, by two-sided matching.
- **(E3) O(v) system.** T = v + H(r) + v F(r) cos theta, with the khronon moving at -v at infinity: F -> -r.
  - Quadratic Lagrangian, angle-integrated: L2 = sum S_ij F^(i) F^(j) (i, j <= 2).
  - Ostrogradsky first-order 4x4 Hamiltonian system X = (F, F', p1, p2).
  - Singular points: r_S (S22 has a simple zero) and the UH (S22 ~ x^4).
  - Integration: local Taylor series (truncated power series) with error-controlled steps, mpmath at 30+ digits.
    Frobenius series start the solutions at r_S and at the UH.
- **(E4) Conditions.**
  - Infinity: no r^3 mode; the coefficient of r is -1.
  - r_S: no logarithm (exponent 1 is double).
  - UH: classification by the perturbed foliation and the khronon scalars (section 3).
- **(E5) Options at each point.**
  - The R-space (three analytic solutions at r_S) intersected with I-space (three solutions with no r^3 mode) is two
    dimensional. After normalisation it is an affine line.
  - Option C: also remove s-; report the amplitude c_s+.
  - Option C': also remove s+; report c_s-.
  - Fully regular solution exists iff both bad amplitudes vanish together.

## 3. UH regularity classification (computed in-lane per point)

For each UH Frobenius mode x^s (x = r - r_UH) the script computes:
- (a) smoothness of the perturbed foliation function tau = exp(-kappa T), i.e. of x F;
- (b) the power of the linear perturbations dK and d(a.a), from in-lane operators;
- (c) the power of their radial gradients (the khronon stress-energy carries grad K and grad a).

A mode is:
- **regular** if (a) is smooth and (b), (c) are bounded;
- **weakly singular** if dK and d(a.a) are bounded and the gradients diverge as x^p with p > -1 (integrable);
- **strongly singular** otherwise.

## 4. Controls (load-bearing unless marked reading)

- **C1, alpha = 0.** The stealth solution (dK = 0) exists, normalised to F -> -r with no r^3 mode, and solves the
  alpha = 0 Ostrogradsky system (residual < 1e-12). Its UH exponent equals sqrt2 - 1 (the closed form from the
  maximal-slicing sub-equation) to 1e-10, and the metric is boosted Schwarzschild (stealth). This is RB2019's regular
  alpha = beta = 0 case.
- **C2, RB2019's point (0.02, 0.01, 0.1), beta included.**
  - No fully regular solution (both options leave a non-zero bad amplitude, stable under refinement).
  - The r_S-regular option is singular at the UH.
  - This is a qualitative reproduction only (the test-khronon limit at alpha = 0.02).
- **C3, injection.** A toy L = (1/2)(D phi)^2, with D the static l = 1 scalar operator on Schwarzschild, run through
  the same Frobenius, march and match code:
  - exponents at r = 2: {0, 0, 1, 1};
  - the regular, no-r^3, normalised solution is phi = r - 1, recovered at r = 6 to 1e-12.
- **C4, Frobenius.**
  - UH exponents match the closed form s(s+1)(2 y1^2 s^2 + 2 y1^2 s - (W0^2+1)^2) to 1e-10 at every point.
  - r_S exponents {0, 1, 1, 2} to 1e-6.
  - The static background's r_S exponent is 0.
- **C5, numerics at (alpha_max, lambda_min).** Re-run at N 30 -> 40, rho 0.25 -> 0.15, x0 dS/4 -> dS/6, R0 1e6 -> 1e8.
  c_s+ and c_s- change by < 1e-3 relative. A larger change makes the amplitudes readings, and the verdict rests on the
  qualitative structure only. This is disclosed.
- **C6, Hamiltonian check.** The symplectic product of two marched solutions is constant to 1e-12 relative.
- **C7, background.**
  - Two-sided matching residual < 1e-15.
  - The background at r_n from the inward march vs the UH series < 1e-14.
- **C8, the beta = 0 reduction.** The in-lane beta-dependent S_ij at beta = 0 equals the beta-free derivation
  identically.
- **MUTATE** (`CFG319_MUTATE=1`, separate `_MUTATE` outputs): the wrong UH boundary condition. The s+ mode is declared
  admissible, so the count reads "determined" and option C is labelled fully regular. The independent gradient check
  (section 3(c), evaluated on the marched solution near the UH) must flag it, and the run must exit rc = 1.

## 5. Decision rule (frozen)

- **OPEN:** a load-bearing control fails.
- **PASS:**
  - at every W5 point a fully regular solution exists: |c_s+| dS^s+ / max(|c_0|, |c_-1|/dS) < 1e-8 in option C,
    i.e. the bad amplitude is consistent with zero;
  - and the dipole passes (section 6).
- **CONDITIONAL:**
  - at every W5 point there is no fully regular solution;
  - but option C exists, regular everywhere on (r_UH, infinity) including r_S and r = 2M, with its UH content at most
    weakly singular (section 3);
  - and the dipole passes.
  - The conditions are named in the README:
    - (i) acceptance of a weak, integrable singularity on the UH, hidden from signals of any speed;
    - (ii) the full metric coupling (beyond the test-khronon limit);
    - (iii) the UV / collapse-formation arguments.
- **KILL:**
  - at some W5 point no option-C-type solution exists. That is, every admissible solution is singular at some
    r > r_UH, or its UH content is necessarily strongly singular (non-integrable khronon stress-energy);
  - or an exterior observable fails.
- **Owner flag:** under RB2019 / FHB2021's criterion (regular everywhere except r = 0), a CONDITIONAL reads KILL for this
  chassis (alpha_c > 0 is needed). This lane does not make that call; it reports it.

## 6. Dipole and sensitivity

The test-khronon limit has no metric response, so s_BH is not computed.

Reported:
- the khronon's exterior dipole content of option C: r^2 dK at r = 6M, which is zero for the stealth solution. It is a
  proxy, with its alpha scaling;
- the exterior difference between options C and C' at r = 6M.

Dipole scoring:
- CFG318's s_crit (B_dip = 1e-4; min s_crit/alpha_c = 3.2e7), with the rule that the dipole passes if
  |s_BH| <= |proxy| x 10 < s_crit at every W5 point;
- the factor 10 is a declared allowance for the unknown normalisation. That is an argument, disclosed.

## 7. What this lane cannot say

- It works in the test-khronon limit at O(v), beta = 0 in the window, with a stationary, eternal BH.
- It contains no metric back-reaction and no BH sensitivity.
- It does not evolve formation by collapse, and it does not include the UV (Horava higher-derivative) terms.
- It is one condition of one gate on one chassis. It is not "the theory works".

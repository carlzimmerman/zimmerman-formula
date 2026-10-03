# CFG311: strong-field neutron-star sensitivity at alpha_c != 0 in the filtered C-H/K chassis

The criteria were frozen first: `FROZEN_CRITERIA.md` (commit f41011ad5). The script is `cfg311_ns_sensitivity.py`.

| run | output files | checks | exit code |
|---|---|---|---|
| main | `.out`, `_results.json` | 7/8 pass, 0 load-bearing failures (the 8th is the L3 "not available" reading row) | 0 |
| MUTATE (`CFG311_MUTATE=1`) | `_MUTATE.out`, `_results_MUTATE.json` | | 1, as required |

The first run's output is kept as `cfg311_ns_sensitivity_FIRSTRUN.out` (see Disclosures). The script runs from
anywhere in about 30 s.

## Verdict: PASS (at the stated scope). CFG291's condition is discharged for this sector

- **Coverage.** With the computed sensitivity s, every point of the L340 primary window passes. The window is
  alpha_c in [9.6e-14, 3.2e-9] and c_2 in [7.29e-3, 0.0667]: 625 of 625 points. All three pulsars pass, with both the
  computed and the universal wave-zone factor.
- **Margin.** The minimum of s_crit/s over the window and the systems is **4.9e5**, set by the double pulsar under
  CFG291's conservative rule |s1 - s2| = s_NS. With the computed difference |s(1.338) - s(1.249)| = 0.0157 alpha_c it
  is 5.5e6.
- **Effect size.** The largest dipole deviation in Pb-dot is 6.2e-15.
- **Comparison with CFG291.** CFG291's published bracket B2 was 3 x Foster with |Omega/m| = 0.3, i.e. s = 3.3 alpha_c.
  The computed s is 0.31-0.47 alpha_c, so the margin grows from 5.25e4 to 4.9e5.

## The result

**Formula.**
- Units: G = c = 1, TOV background with ds^2 = -e^{2Phi} dt^2 + e^{2Lambda} dr^2 + r^2 dOmega^2.
- At O(v), the khronon of a star moving relative to the khronon frame is T = t + v F(r) cos(theta). F solves the
  maximal-slicing (K = 0) equation, derived in sympy:

  (r^2 e^{2Phi-Lambda} F')' = 2 e^{2Phi+Lambda} F

  - F is proportional to r at the centre, and F/r -> 1 at infinity.
  - Exterior: F = A(r - M/2) + B F_2(r), where r - M/2 is an exact Schwarzschild solution.
- The sensitivity is

  s = alpha_c * sigma1 + O(alpha_c^2, alpha_c^2/lambda), with sigma1 = (1/(8 pi M)) Int_0^inf dr r^2 e^{Phi+Lambda} I_2(r)

  I_2 = (4 pi/3) e^{2Phi-4Lambda} (Phi'/r^3) [ -r^3 F'^2 Phi' - 4 r^2 F'^2 + 4 r F^2 e^{2Lambda} Phi' + 8 r F F' e^{2Lambda} - 4 F^2 e^{2Lambda} ]

- I_2 is the angle-integrated O(v^2) part of a_mu a^mu. It was computed two ways (the lapse formula, and
  u^nu nabla_nu u_mu with Christoffel symbols), which agree symbolically.
- The method is first-order (Hellmann-Feynman) perturbation in alpha about Barausse 2019's exact alpha = beta = 0
  solution: the static GR star plus the maximal-slicing khronon. Then -delta m~(v) = (alpha/16 pi G) Int sqrt(-g) a^2,
  and sigma = 2 dL_2/M.

**s/alpha_c at the pulsar masses** (Read et al. 2009 piecewise polytropes, parameters recalled; see Disclosures):

| star | M (Msun) | SLy | APR4 | MPA1 | scored (max) | strong/Foster |
|---|---|---|---|---|---|---|
| J1738+0333 | 1.46 | 0.3664 | 0.3722 | 0.3465 | 0.3722 | 0.75-0.78 |
| J0348+0432 | 2.01 | 0.4699 | 0.4591 | 0.4242 | 0.4699 | 0.64-0.70 |
| J0737-3039A | 1.338 | 0.3445 | 0.3515 | 0.3274 | 0.3515 | 0.77-0.79 |
| J0737-3039B | 1.249 | 0.3280 | 0.3358 | 0.3129 | 0.3358 | 0.78-0.80 |

**Dependence on compactness** (sweep in `_results.json`, reading).
- s/alpha_c rises from 0.08 at C = 0.02 to 0.48 at C = 0.30. It is nearly EOS-independent at fixed C.
- The strong-field value sits *below* Foster's weak-field (11/3)|Omega_N|/M: by about 5% at C = 0.02, and down to
  0.63 of it at C = 0.30. The record's "realistic stars can exceed the weak-field value by up to 200%" (Yagi et al.,
  for general couplings) does not apply in this alpha << lambda, beta = 0 corner.

**s on the window** (alpha_c from 9.62e-14 to 3.2e-9):

| star | s |
|---|---|
| J1738+0333 | 3.6e-14 to 1.19e-9 |
| J0348+0432 | 4.5e-14 to 1.50e-9 |
| J0737A | 3.4e-14 to 1.12e-9 |
| J0737B | 3.2e-14 to 1.07e-9 |

**Record window W3** (c_2 from 1e-12 to 0.1), reading:
- Radiation passes at every alpha_c for c_2 >= 5.6e-10 with the computed wave-zone factor, and for c_2 >= 4.4e-6
  with the universal factor.
- The first-order result is valid (alpha/lambda <= 1e-3 at every alpha_c) only for c_2 >= 4.4e-6. On the covered
  points, 750 of 750 pass with the computed factor and 702 of 750 with the universal factor.
- Below c_2 ~ 4e-6 this lane computes nothing.

## Controls

| control | result |
|---|---|
| S1 symbolic | K at O(v) is a nonzero prefactor times E1; the flat-space solutions are r and r^-2; the two a^2 routes agree; a^2 has no O(v) term |
| W1 weak-field limit (Foster 2007 eq. 70 at beta = 0) | (a) uniform sphere, sympy: exactly 11/3; (b) Newtonian n = 1 polytrope: 1.00000000; (c) the full strong-field code reaches Foster within 0.15% (n = 1, C = 1e-3) and 0.015% (C = 1e-4), and 0.32% / 0.08% (SLy, C = 9.6e-4 / 3.9e-4). The deviation shrinks in proportion to C. This also tests the no-boundary-term step |
| Z1 alpha -> 0 | s is linear in alpha, so it vanishes at alpha = 0 (Barausse 2019); the K = 0 residual is <= 4.7e-7; Foster's PPN combination equals -11 alpha/3 to 4e-8 over W1 (lambda drops out at this order) |
| T1 TOV | M_max and R_1.4 within 1.2% of the recalled Read et al. values (SLy 2.048/11.71, APR4 2.188/11.32, MPA1 2.456/12.43) |
| N1 convergence | 2N to 4N: 2e-12; rtol x 1e-2: 2e-11; r_out x 2: 5e-8 |
| R1 CFG291 scorer | exec'd read-only, with writes sent to os.devnull; reproduces the committed pass counts and min s_crit/s_B2 = 5.2498e4 exactly; CFG291's directory stays clean |
| L3 literature table (Yagi et al. 2014) | NOT AVAILABLE: the HTML read returned no khronometric table or fit. It is not run and not counted as passed (shown as a failed reading row) |
| MUTATE alpha -> -alpha_c | s flips sign (to -1.19e-9 for J1738 at the top corner) |

More on the MUTATE run:
- The dipole is quadratic in s1 - s2, so the radiation score alone is sign-blind: identical delta. This is disclosed.
- CFG291's scorer refuses alpha < 0, because c0^2 < 0 there (a gradient-unstable khronon).
- The window gate flags all 625 points, and the run exits with rc 1.

## Disclosures

**Two coding errors were fixed after the first run.** That run read OPEN and is kept as `_FIRSTRUN.out`, with only
the home path stripped.
- **(1) A unit error in the n = 1 control polytrope.** The first run had K_cgs = K/KAPPA instead of K x KAPPA, so
  every "low-density" control star came out at C = 0.25, and W1(c) failed. After the fix the control stars sit at
  C = 1e-3 and 1e-4 and pass. The SLy rows of W1(c) were unaffected and passed both times.
- **(2) The K = 0 residual measure was recoded.**
  - In the first run, F'' came from second-order `np.gradient` across the crust-core and piece boundaries, where F'''
    jumps. That measure gave 2e-5 to 8e-5 (peak at r/R 0.89-0.96) and failed the frozen 1e-6.
  - The recoded measure uses a fourth-order central difference of the dense F', with stencils that do not cross a
    piece boundary or the surface. It gives <= 4.7e-7.
  - The old measure is still printed for every star. sigma/alpha itself was identical in both runs.
- **The margin printed on the J0737 "actual difference" reading row was miscomputed.** It used s_NS rather than the
  difference. This was corrected before the final run and is a reading only.
- **The EOS parameters were recalled, not read.** The ar5iv read of Read et al. 2009 returned the dividing densities
  but not Table 3. T1 is therefore a self-consistency test of the recall.
  - The scored s varies by only 7-10% across the three EOS.
  - The margin is 4.9e5.
- **Not blind.** The uniform-sphere weak-field identity (11/3) was derived before the freeze; it is listed in
  FROZEN_CRITERIA sec. 0.
- **Literature values are PROVISIONAL.** They were read through a summarising fetch tool, with no PDF.

## What this lane cannot say

- Its scope is leading order in alpha_c, with beta = 0 and alpha/lambda << 1. It is not a general (alpha, beta, lambda)
  sensitivity.
- Boundary terms in the Hellmann-Feynman step are argued away. They are tested only through the weak-field limit,
  which reproduces Foster exactly. No independent strong-field method (for example the Yagi et al. asymptotic
  extraction) was run, and no tabulated literature point was available.
- The NS sits in the near zone, where CFG291 found the heat filter removes the C-H sector, so the MOND clock inertia
  plays no part in s. CFG291's wave-zone treatment is reused unchanged.
- It is one gate on one chassis. It is not "the theory works". kappa = 1/2 remains FITTED, and the dark sector still
  requires the cold mass.

# CFG311: strong-field neutron-star sensitivity s at alpha_c != 0 in the filtered C-H/K chassis. FROZEN CRITERIA

Lane CFG311 (closes CFG291's single named condition). Written and committed before any CFG311 script exists and before
any numerical neutron-star sensitivity has been computed. Verdict words are the recipe's section 6 words only: PASS,
CONDITIONAL, KILL, OPEN.

Standing rules. kappa = 1/2 is FITTED. No knob scans, no fitting: alpha_c and c_2 are read from committed files and the
EOS parameters are published fits. Nothing here says the theory is closed or that data favour the framework. The cold
mass the CMB needs is untouched by this lane and is still required.

## 0. What was read before freezing, and the not-blind statement

Read: CFG291 (README, FROZEN_CRITERIA, `cfg291_khronon_binary_pulsar.py`, `.out`; commits 9b2bc6fe0, 5f1f07dc2).
Literature through a summarising fetch tool (arXiv abstract pages and ar5iv HTML only; no PDF; PROVISIONAL):
- Barausse 2019 (arXiv:1907.05958) abstract: sensitivities vanish identically at alpha = beta = 0, lambda generic. The
  abstract gives no small-alpha formula or number.
- Yagi, Blas, Barausse & Yunes 2014, PRD 89, 084067 (arXiv:1311.7144): abstract plus an ar5iv summary. Sensitivities
  are computed from O(v) slowly-moving NS solutions. The summary returned no khronometric table or fit, so **no
  tabulated literature s point is available to this lane** (section 5, control L3).
- Read, Lackey, Owen & Friedman 2009 (arXiv:0812.2163) ar5iv: dividing densities rho_1 = 10^14.7 and
  rho_2 = 10^15.0 g/cm^3, with p_1 in dyn/cm^2. Table 3 (the EOS parameters) was NOT returned. The parameter values in
  section 3 are **recalled, not read**. Control T1 tests them against the recalled M_max and R_1.4 of the same table,
  so T1 is a self-consistency test of the recall, not an independent read.

Not blind (analytic work done before this file):
- I derived the method in section 1.
- I did a sympy weak-field calculation for a **uniform-density sphere**: it gives sigma = (11/3) alpha |Omega_N|/M
  exactly, which is Foster's eq. 70 at beta = 0.
- I expect the order of magnitude s ~ 0.5 alpha_c for NSs, from Foster's formula with |Omega|/M ~ 0.15.
- No TOV star was built and no NS s was computed. The decision rule below was written knowing the expected order of
  magnitude, and that CFG291's margin is >= 5e4 in s.

## 1. Formulation (DERIVED in-lane, with what is ADOPTED marked)

Chassis (CFG291 sec. 1): I = I_CH + (1/16 pi G) Int sqrt(-g)[alpha a_mu a^mu - lambda K^2], beta = 0,
mostly-plus signature. Here alpha = alpha_c and lambda = c_2. At NS scales the heat filter removes the C-H sector:
the filter exponent at a NS is -(xi/R_NS)^2 ~ -6e21 (CFG291 N). So the NS sees the BPS khronon with
alpha = alpha_c, beta = 0, lambda = c_2. The MOND clock inertia 2C/(1+C) is filtered out there.

Definition (ADOPTED; Foster 2007, Yagi et al. 2014):
- A body is a point particle with action -Int m~(gamma) d tau, where gamma = -u.U is its Lorentz factor relative to
  the khronon frame.
- sigma = -d ln m~/d ln gamma at gamma = 1, with baryon number and entropy fixed; s = sigma/(1 + sigma).
- In the star's rest frame the on-shell action per unit proper time is -m~(gamma).

Method: first-order perturbation theory (Hellmann-Feynman) in alpha.
- **(M1) The alpha = 0 solution (ADOPTED; Barausse 2019).** Every GR solution with a maximal slicing (K = 0) solves
  the alpha = beta = 0 theory for any lambda. The lambda K^2 term's metric and khronon field equations are each linear
  in K and its derivatives. For a star moving at velocity v relative to the khronon, in the star frame, this solution
  is:
  - the static TOV metric ds^2 = -e^{2 Phi} dt^2 + e^{2 Lambda} dr^2 + r^2 dOmega^2, independent of v;
  - the khronon T = gamma t + v F(r) cos theta + O(v^2), with K = 0, F regular at the centre (F proportional to r) and
    F/r -> 1 at infinity.
- **(M2) The energy shift.** Write S = S_0 + alpha S_1, S_1 = (1/16 pi G) Int sqrt(-g) a^2. Then
  dS_on-shell/d alpha at alpha = 0 equals S_1 evaluated on the alpha = 0 solution, because the bulk terms vanish on
  shell. The boundary terms are argued to vanish with a first-order (Gamma-Gamma) gravitational Lagrangian, since the
  O(alpha) field corrections fall off at least as 1/r. That argument is **tested, not assumed**, by control W1 below.
  - Hence -delta m~(v) = (alpha/16 pi G) Int d^3x sqrt(-g) a^2 = dL_0 + dL_2 v^2 + O(v^4).
  - m~ = M - dL_2 v^2, so **sigma = 2 dL_2 / M**, where M is the gravitational mass.
  - The neglected orders are O(alpha^2/lambda) and O(alpha^2). Validity needs alpha/lambda << 1. Over the L340 window
    alpha/lambda <= 4.4e-7. W3 points with alpha/lambda > 1e-3 are flagged "not covered".
- **(M3) Equations to derive symbolically (sympy, from the metric and khronon ansatz; no hand-coded field equation in
  the numerics):**
  - E1: K = nabla_mu u^mu with u_mu = -N d_mu T, to O(v). This gives the khronon ODE, expected form
    (r^2 e^{2Phi - Lambda} F')' = 2 e^{2Phi + Lambda} F.
  - E2: a^2 = h^{mu nu} d_mu ln N d_nu ln N, expanded to O(v^2) and computed **two ways**, which must agree
    symbolically:
    - (i) from the lapse formula;
    - (ii) directly as a_mu = u^nu nabla_nu u_mu, with Christoffels.
  - E3: the angle-integrated integrand I_2(r), so that dL_2 = (alpha/16 pi G) Int_0^inf dr r^2 e^{Phi + Lambda} I_2(r).
  - The numerics use lambdified sympy output.
  - **Result format:** sigma/alpha = 2 dL_2/(alpha M) is a pure number for each star; s = alpha (sigma/alpha) + O(alpha^2).
- **Weak-field target (ADOPTED, Foster 2007 eq. 70 with the khronometric PPN at beta = 0):**
  s -> (alpha_1 - 2 alpha_2/3) Omega_N/M = (11/3) alpha |Omega_N|/M (since alpha_2 -> -alpha/2 for alpha << lambda),
  with Omega_N = -(1/2) Int rho U d^3x.

## 2. Numerics

- **TOV:** integrate in r from the centre with a series start, out to the surface (p -> 0). Use total energy density
  e(rho) from the piecewise-polytrope first law.
  - Exterior: exact Schwarzschild. Phi is shifted so e^{2Phi} -> 1.
  - Central density: root-found to hit each target gravitational mass.
- **Khronon ODE:** integrate F from the centre (F = r + O(r^3)) through the star and the Schwarzschild exterior to
  r_out. Normalize by the asymptotic r-coefficient, fitted with the two exterior homogeneous solutions (O(r), O(r^-2)).
- **dL_2 integral:** interior plus exterior to r_out. The tail beyond r_out is added from its leading 1/r^2 power law,
  and the size of the tail is reported.
- **Grid:** N = 4000 radial points as the baseline (dense ODE output). Refinement uses N, 2N, 4N and solver tolerances
  rtol 1e-10 / 1e-12.

## 3. Equation-of-state set (published fits; parameters RECALLED, section 0)

Piecewise polytropes of Read et al. 2009:
- Core: three pieces above the crust, dividing densities 10^14.7 and 10^15.0 g/cm^3; parameters (log10 p_1 [dyn/cm^2],
  Gamma_1, Gamma_2, Gamma_3).
  - **SLy** (34.384, 3.005, 2.988, 2.851)
  - **APR4** (34.269, 2.830, 3.445, 3.348)
  - **MPA1** (34.495, 3.446, 3.572, 2.887); third EOS, stiff
- Crust: Read et al.'s four-piece SLy crust fit. K_i is in units with p/c^2 in g/cm^3.
  - (K, Gamma) = (6.80110e-9, 1.58425), (1.06186e-6, 1.28733), (5.32697e1, 0.62223), (3.99874e-8, 1.35692)
  - Boundaries 2.44034e7, 3.78358e11, 2.62780e12 g/cm^3. The crust-core junction is where the pressures match.
- Additional EOS-shape control (not scored): Gamma = 2 polytrope (n = 1).

Stars:
- J1738+0333 pulsar: 1.46 Msun
- J0348+0432 pulsar: 2.01 Msun
- J0737-3039: 1.338185 and 1.248868 Msun
- Also reported: a compactness sweep, M = 0.2 Msun to 0.98 M_max per EOS (a reading of s/alpha versus C = M/R, not a fit)

## 4. Controls (each can fail)

Load-bearing:
- **S1 symbolic consistency:** E2(i) equals E2(ii) to O(v^2) symbolically. E1 reduces to (r^2 F')' = 2F in flat space,
  with solutions r and r^-2.
- **W1 weak-field limit (Foster 2007):**
  - (a) sympy, uniform sphere, leading order in G: sigma/(alpha |Omega_N|/M) = 11/3 exactly.
  - (b) Newtonian n = 1 polytrope, numerical leading-order integrals: ratio 11/3 within 1e-4. This is profile
    independence.
  - (c) The full strong-field code on low-compactness stars (SLy, and the n = 1 polytrope, C <= 1e-3): ratio to
    (11/3)|Omega_N|/M within 1% at C ~ 1e-3, with the deviation shrinking as C decreases.
- **Z1 alpha -> 0 (Barausse 2019):**
  - s(alpha = 0) = 0 identically.
  - The alpha = 0 khronon solution satisfies K = 0: the max |K|/(v/R) residual on the grid is < 1e-6.
  - sigma/alpha is independent of lambda at this order (lambda enters only at O(alpha^2/lambda)): checked by evaluating
    the alpha-corrected PPN combination over the window, as a reading.
- **T1 TOV reproduces the recalled Read et al. numbers:** M_max and R_1.4 within 2%. Recalled values:
  - SLy 2.049 Msun / 11.736 km
  - APR4 2.213 / 11.428
  - MPA1 2.461 / 12.466
  - Also: 2.01 Msun < M_max for every scored EOS.
- **N1 convergence:** sigma/alpha changes by < 1e-4 (relative) between 2N and 4N. Tightening rtol by 100 changes it by
  < 1e-5. Doubling r_out changes it by < 1e-5 (tail included).
- **R1 rescoring reproduces CFG291:** CFG291's committed functions are reused read-only (its file is exec'd with every
  write redirected to os.devnull; no CFG291 file changes). They must reproduce CFG291's committed W1 summary (B0-B2
  pass counts and the minimum s_crit/s_B2 = 5.25e4 to 3 s.f.) before the computed s replaces the bracket. The
  `git status` of CFG291's directory must be clean after the run.

Not load-bearing (reading):
- **L3:** a literature-tabulated s point (Yagi et al. 2014). NOT AVAILABLE (section 0). Reported as not run. It is
  not counted as passed.
- The ratio of the strong-field to the weak-field estimate at each pulsar mass, against Yagi et al.'s "up to 200%".
- **MUTATE** (separate outputs `*_MUTATE*`): alpha -> -alpha_c.
  - s must flip sign: sigma/alpha is unchanged and s < 0.
  - CFG291's dipole is quadratic in (s1 - s2), so the radiation score alone cannot see the sign. This is disclosed.
  - The window gate (alpha_c > 0, L340 P1) must flag it, and the MUTATE run must exit rc = 1.

## 5. Re-scoring and decision rule (frozen)

The computed sensitivity at each window point:
- s_NS = alpha_c * max over EOS (sigma/alpha at the system's NS mass), times 1.0. The EOS spread is the max over the
  three EOS; no further inflation.
- NS-WD systems: s_WD = 0 (a white dwarf has |Omega|/M ~ 1e-4 and a weak field, so its s is 1e-4 alpha_c, below every
  term here).
- J0737-3039 primary: CFG291's conservative rule |s1 - s2| = |s_NS(1.338)|. Reading: the computed difference
  |s(1.338) - s(1.249)|.
- Scored over W1 (25 x 25, CFG291's grid) with the computed and the universal wave-zone factor. W3 (CFG291's record
  grid) is reported as edges, with alpha/lambda <= 1e-3 marked.

Rule:
- **OPEN:** any load-bearing control (S1, W1, Z1, T1, N1, R1) fails.
- **KILL (per point):** a W1 point exceeds any system's 2-sigma limit with the computed s (computed wave-zone factor).
  KILL for the radiative sector if every W1 point does.
- **CONDITIONAL:**
  - every W1 point passes with the computed wave-zone factor, but some fail with the universal factor; or
  - only a sub-window survives.
- **PASS (at the stated scope):** every W1 point passes all three systems with the computed s under both the computed
  and the universal wave-zone factor, and every load-bearing control passes. CFG291's condition is then discharged
  for this sector.
- Also reported: the new sensitivity margin s_crit/s_computed (minimum over W1 and systems).

Every script ends with "N/M checks pass"; main and MUTATE outputs go to separate files.

## 6. What this lane cannot say

- It computes s at leading order in alpha_c (first-order perturbation about Barausse's exact alpha = beta = 0
  solution). It is valid for alpha/lambda << 1 and beta = 0 only. It is not a general (alpha, beta, lambda) result.
- The EOS parameters are recalled published fits (section 0). T1 checks them only for internal consistency.
- No tabulated literature point is reproduced (L3 not available). The method's external anchor is Foster's weak-field
  law (W1).
- It is one gate on one chassis. It is not "the theory works", and the dark sector still requires the cold mass.

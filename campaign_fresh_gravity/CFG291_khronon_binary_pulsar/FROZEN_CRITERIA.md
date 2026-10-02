# CFG291: khronon dipole radiation in binary pulsars over the filtered C-H/K window. FROZEN CRITERIA

Lane CFG291 (orchestrator lane, 10-02; owner's "extra crispy" request). Written and committed before any CFG291 script
exists. Recipe: `qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md`, gates G7 (PPN) and G11/G12
(strong field, radiative). Verdict words are the recipe's section 6 words only: PASS, CONDITIONAL, KILL, OPEN.

Standing rules applied. kappa = 1/2 is FITTED (a0 = 9.3619e-11 canonical, 1.1279e-10 alt footing; both are run).
Nothing here says the theory is closed, that data favour the framework, or that kappa is derived. No new fitted
constant is introduced. The cold mass the CMB needs is untouched by this lane and is still required.

## 0. What was read before freezing, and the not-blind statement

Read: the recipe (top user-decision block of 2026-09-26, sections 1-11);
`real_research/g03_audit_2026/L340_filtered_khronon_completion.py` and its committed `_results.json`;
`L350_chk_cosmological_G_gate.py` (header, verdict, results JSON);
`real_research/extra_crispy_2026/XC1_strong_coupling_chk.py` (header, A3/A4/A9, results JSON);
`data_assembly/DOOR11_LITERATURE_2026-09-29.md` (the record's preferred-frame bounds table).
Literature (arXiv abstract pages and ar5iv HTML only, through a fetch tool that returns a model's summary of the page;
no PDF was fetched; values are PROVISIONAL in the programme's sense and their read status is listed in section 3).

Not blind. While reading the formulas I made rough mental estimates, before this file: that Barausse's dipole
coefficient C scales as alpha^(1/2) lambda^(-3/2) at small (alpha, lambda); that with sensitivities of order alpha_c
the dipole is many orders below the bounds; that the khronon's radiated wavelength at orbital frequencies is of order
the filter scale xi (so the heat filter does NOT obviously screen the wave zone); that a counterfactual sensitivity of
order lambda would sit near the J1738+0333 threshold; and the GR Pb-dot of J0348+0432 (about -0.259e-12) by hand.
No script was run and no window grid was evaluated. The decision rule below was written with these estimates in mind.

## 1. The chassis and its window (from committed files, not memory)

Action (L340 docstring; XC1 header): I_CHK = I_CH + c^3/(16 pi G) Int sqrt(-g) [alpha_c a_mu a^mu - c_2 K^2], beta = 0,
mostly-plus signature, C-H's heat filter S = exp((xi^2/2) Delta) acting on the MOND kernel's argument; L350 G5's
leaf-average form -c_2 (K - <K>)^2 is identical for every k != 0 mode, so radiation sees the same c_2.

| quantity | value used | source |
|---|---|---|
| alpha_c (BPS khronon coefficient, > 0, load-bearing) | [9.624048e-14, 3.2e-9] | L340 results JSON, numbers.P1.alpha_c_min / alpha_c_max |
| c_2 = lambda_K - 1 (L340 window, branch with L350 G5) | [7.288800e-3, 6.666667e-2] | L340 results JSON, numbers.P1.c2_min / c2_max |
| lambda_K record window (recipe sec. 9, "1 < lambda_K <= 1.10") | c_2 in (0, 0.10] | recipe sec. 9 table, G5 row |
| Planck-era c_2 ceilings, plain -c_2 K^2 branch | 6.31e-4 .. 2.95e-3 | L350 results JSON, numbers.G2.rows[].c2_ceiling |
| beta | 0 (c_T = 1) | L340 docstring and P1 |
| xi (heat filter) | >= 0.031 pc / 0.045 pc (recipe I5); committed floors 0.03115, 0.03282, 0.04513, 0.04892 pc | recipe sec. 1 I5; L340 results JSON numbers.S1 |
| kernel | nu_mono: h' = max(h'_RAR, delta h_p/(y + y_p)), delta = 0.05, y_p = 2.5396, h_p = 0.6476 a0, y* = 2.3374 | recipe user-decision block; L340 results JSON numbers.A1 |
| Galactic field at the Sun (sets the wave-zone background) | g = 2.32e-10 m/s^2 (observed); y_N from y nu_mono(y) = g/a0, both footings; XC1's y = 2.3 row also run | L340 S1 (GEXT); XC1 A5 |
| clock inertia in the MOND regime | alpha_eff(k) = alpha_c + 2C/(1+C), C = C_0 e^(-xi^2 k^2), C_0 = C_T or C_L of nu_mono | XC1 A3 and A5 |

Windows scored:
- **W1 (primary):** alpha_c x c_2 over the L340 P1 box, 25 x 25 log-spaced points, endpoints included.
- **W3 (secondary, record window):** the same alpha_c range x c_2 in [1e-12, 0.10], 49 log-spaced points (1e-12 is a
  declared numerical floor of the open edge lambda_K -> 1). The L350 plain-branch ceilings lie inside W3; they are
  marked, not scored separately.

## 2. The map onto the literature parameters (to be checked, not assumed)

The khronometric action of Barausse 2019 (and Yagi et al. 2014 eq. 17, ADM form
(1-beta)/(16 pi G) Int N sqrt(h)[K_ij K^ij - (1+lambda)/(1-beta) K^2 + R/(1-beta) + alpha/(1-beta) a_i a^i]) maps
term by term: **alpha = alpha_c, beta = 0, lambda = c_2 = lambda_K - 1**. Checks in section 5: C3 and C4.

## 3. Formulas (all ADOPTED unless marked DERIVED)

- **F1 flux** (Barausse 2019, PRD 100, 084053, arXiv:1907.05958, eqs. 15, 17-22; read twice, ar5iv v-latest and v4):
  Edot_b/E_b = 2(G m1 m2/r^3){(32/5)(A1 + S A2 + S^2 A3) v^2 + (s1 - s2)^2 [C + (18/5) A3 V_CM^2 + ((6/5) A3 + 36 B)(V_CM.n)^2]},
  A1 = 1/c_T + 3 alpha (Z-1)^2/(2 c0 (2-alpha)), A2 = 2(Z-1)/((alpha-2) c0^3), A3 = 2/(3 alpha (2-alpha) c0^5),
  B = 1/(9 alpha c0^5 (2-alpha)), C = 4/(3 c0^3 alpha (2-alpha)), S = s1 m2/m + s2 m1/m, c_T^2 = 1/(1-beta),
  c0^2 = (lambda+beta)(2-alpha)/(alpha(1-beta)(2+3 lambda+beta)), Z = (alpha1 - 2 alpha2)(1-beta)/(3(2 beta - alpha))
  (Z read once), s_A = sigma_A/(1+sigma_A), G_N = G/(1 - alpha/2).
- **F2** Yagi, Blas, Yunes & Barausse 2014, PRL 112, 161101 (arXiv:1307.6219): Pdot_b/P_b = -(192 pi/5)(2 pi G m/P_b)^(5/3)
  (m1 m2/m^2)(1/P_b) <A>, <A> = [(1-s1)(1-s2)]^(2/3)(A1 + S A2 + S^2 A3) + (5/32)(s1 - s2)^2 A4 (P_b/(2 pi G m))^(2/3)
  (read once). Hence the fractional deviation used here:
  **delta = [(1-s1)(1-s2)]^(2/3)(A1 + S A2 + S^2 A3) - 1 + (5/32)(s1-s2)^2 [C R1 g(e)/f(e) + V-terms R2]/v^2**,
  v^2 = (2 pi G_N m/P_b)^(2/3)/c^2, V_CM = 600 km/s (L340's tracking scale) with (V.n)^2 <= V^2.
- **F3 PPN** (Yagi et al. 2014 PRD 89, 084067 eqs. 48-49 = Barausse 2019; read twice):
  alpha1 = 4(alpha - 2 beta)/(beta - 1), alpha2 = (alpha - 2beta)[-beta^2 + beta(alpha-3) + alpha + lambda(-1-3beta+2alpha)]/((beta-1)(lambda+beta)(alpha-2)).
- **F4 weak-field sensitivity** (Foster 2007, PRD 76, 084033, arXiv:0706.0704, eq. 70; read twice):
  s_A = (alpha1 - (2/3) alpha2) Omega_A/m_A + O(G m/d)^2.
- **F5** (Barausse 2019 abstract and eqs. 29, 39): NS sensitivities vanish identically at alpha = beta = 0, any lambda != 0.
- **F6** (Yagi et al. 2014 PRL text): the low-compactness formula underestimates realistic NS sensitivities "by as much as 200%".
- **F7** Peters-Mathews GR Pb-dot, f(e) = (1 + 73e^2/24 + 37e^4/96)/(1-e^2)^(7/2); T_sun = G M_sun/c^3 = 4.925490947e-6 s
  (standard; not re-read this session).
- **F8** scalar-dipole eccentricity factor g(e) = (1 + e^2/2)/(1-e^2)^(5/2) (standard; not re-read; matters only for
  J0737-3039, where it is <= 3%).
- **F9 DERIVED in-lane: the wave-zone factor.** The decoupling-limit quadratic action (XC1 A1, A5) is
  k^2 [alpha_eff(k) w^2/c^2 - B k^2] |pi|^2 with B = alpha_c c0^2(alpha_c, lambda) (so that C_0 = 0 reproduces F1's c0),
  sourced by the sensitivity coupling J_k ~ k^l (l = 1 dipole, l = 2 quadrupole order). The retarded Green's function
  (Sokhotski-Plemelj) gives a radiated power proportional to k*^(2l)/F'(k*), F(k) = B k^2 - alpha_eff(k) w^2/c^2,
  F(k*) = 0. Relative to the unfiltered UV khronon: **R_l = (k*/k_UV)^(2l-1) * 2 B k*/F'(k*)**, with the dipole at
  w = 2 pi/P_b and quadrupole-order terms at 2w. Bound: R_l <= (alpha_eff(k*)/alpha_c)^((2l-1)/2), and with
  2C/(1+C) < 2 the environment-free bound R_l <= (1 + 2/alpha_c)^((2l-1)/2) ("universal"). The coefficients A1 - 1, S A2,
  S^2 A3 and the V-terms are multiplied by R2's bound (generous); C by R1 computed exactly.
- **Near zone (numbers to report):** y = G m/(a^2 a0) at the orbit; the filter exponent -(xi/a)^2 and -(xi/R_NS)^2;
  the amplitude suppression (mu/m)(a/xi)^2 of the binary's time-varying (quadrupole) part of the filtered source S rho;
  the tensor-GW filter exponent -(xi k_GW)^2.

## 4. Pulsar inputs and thresholds (2 sigma / 95%)

delta = Pdot_b,pred/Pdot_b,GR - 1 (positive = faster decay; a dipole gives delta > 0).

| system | inputs | allowed delta | source, read status |
|---|---|---|---|
| PSR J1738+0333 | P_b = 0.3547907398724 d, e = 3.4e-7, m_p = 1.46, m_c = 0.181 Msun; Pdot_int = -25.9(3.2) fs/s; Pdot_GR = -27.7(+1.5,-1.9) fs/s; Pdot_xs = +2.0(+3.7,-3.6) fs/s | -27.7 delta in [2.0 - 2(3.6), 2.0 + 2(3.7)] fs/s, i.e. delta in [-0.339, +0.188] | Freire et al. 2012, MNRAS 423, 3328 (arXiv:1205.1450): abstract [ABS] + Table 1 via ar5iv [FT]; masses also in Antoniadis et al. 2012 abstract (1.47 / 0.181) |
| PSR J0348+0432 | P_b = 0.102424062722 d, e ~ 2e-6, m_p = 2.01(4), m_c = 0.172(3); Pdot_obs = -0.273(45) ps/s; Pdot_GR = -0.258(+0.008,-0.011) ps/s; ratio 1.05 +/- 0.18 | 1 + delta in 1.05 +/- 0.36: delta in [-0.31, +0.41] | Antoniadis et al. 2013, Science 340, 6131 (arXiv:1304.6875): abstract [ABS] + Table 1 via ar5iv [FT] |
| PSR J0737-3039A/B | e = 0.088, P_b = 2.45 h; masses 1.338185 / 1.248868 Msun, P_b = 0.10225 d (used only for v^2) | \|delta\| <= 1.3e-4 | Kramer et al. 2021, PRX 11, 041050 (arXiv:2112.06795) abstract [ABS] ("1.3 x 10^-4 (95% conf.)"); masses from the MPIfR NS-masses compilation page (one read, secondary) |

## 5. Sensitivity brackets

|Omega/m|_max = 0.3 for every neutron star (a deliberate upper bound, not an EOS calculation); white dwarfs s = 0.
For the NS-NS double pulsar |s1 - s2| <= |s_NS| (as if one star had s = 0: conservative), |S| <= |s_NS|.
- **B0:** s = 0 (F5, the alpha_c -> 0 anchor).
- **B1:** |s_NS| = |alpha1 - (2/3) alpha2| |Omega/m|_max (F4 with F3).
- **B2:** 3 x B1 (F6).
- **B3 (counterfactual stress, NOT published):** |s_NS| = |Omega/m|_max * lambda, i.e. what happens if the khronon
  charge scaled with lambda instead of alpha_c. It contradicts F5 by continuity and is reported as a stress test only.
- Also reported at every point: s_crit, the |s1 - s2| at which the dipole alone reaches each system's 2-sigma limit.

## 6. Controls (each can fail)

- **C1 GR reproduction (published numbers to quoted precision):** F7 with each paper's own masses must give
  J1738+0333 Pdot_GR within its quoted interval (-27.7 +1.5/-1.9 fs/s) and within 1% of 27.7; J0348+0432 within
  (-0.258 +0.008/-0.011 ps/s) and within 1% of 0.258.
- **C2 the published limit (Barausse 2019 text):** sympy: as alpha, beta -> 0 with lambda != 0, A1 -> 1 and
  A2, A3, B, C -> 0; c_T = 1 at beta = 0.
- **C3 record cross-checks:** F1's c0 at XC1's A9 corners reproduces XC1's committed 4.438e2 c and 7.936e5 c to
  4 significant figures; F3 at beta = 0 gives alpha1 = -4 alpha_c exactly and alpha2/(-alpha_c/2) -> 1 within 1e-6
  across W1 (L340 P1's formulas).
- **C4 the map:** the decoupling-limit speed c0^2 = c_2/alpha (XC1 A1) agrees with F1's c0^2 at lambda = c_2 to
  O(alpha, lambda) (ratio -> 1 as both -> 0); the wrong maps lambda = c_2/2 and lambda = 2 c_2 must fail this test.
- **C5 the wave-zone model:** R_l = 1 exactly when C_0 = 0; the model's power exponents d ln P/d ln alpha = (2l-1)/2 and
  d ln P/d ln lambda = -(2l+1)/2 must match F1's C (l = 1: +1/2, -3/2) and A3 (l = 2: +3/2, -5/2) numerically at small
  (alpha, lambda) to 1e-3.
- **C6 alpha_c -> 0 (XC1, P7):** at fixed lambda the B1/B2 khronon flux must vanish as alpha_c -> 0 (with the computed
  and with the universal wave-zone factor), and XC1's strong-coupling momentum sqrt(alpha) M_P c0^(-1/2) must fall
  below 1e3 x the LHC probe momentum: the flux vanishes AND the theory becomes strongly coupled.
- **C7 MUTATE (separate outputs `*_MUTATE*`):** lambda_K = 2 (c_2 = 1). The scorer's window gate must flag it: outside
  L340's c_2 window, and in the plain -c_2 K^2 branch |G_cos/G_N - 1| = |(2 - alpha_c)/(2 + 3 c_2) - 1| > 0.1 (BBN,
  L340 P1 / L350 G1). The MUTATE run must exit rc = 1. The radiation score at lambda_K = 2 is reported as it comes out.
- **C8 injection:** at one W1 point, |s1 - s2| = 1.01 s_crit must be scored FAIL and 0.99 s_crit PASS, for each system.
- **C9 kernel:** the reimplemented nu_mono reproduces L340's committed y_p, h_p, min C_T, min C_L to 1e-4 relative, and
  y* = 2.3374 to 1e-4.

## 7. Decision rule (frozen)

Primary scoring uses the computed wave-zone factor R (the maximum over xi in the committed floors, C_T and C_L, both
footings and XC1's y = 2.3 row); the universal bound is a robustness row.
- **OPEN:** any load-bearing control (C1-C6, C8, C9) fails, or the map (C4) fails.
- **KILL (per point):** the point exceeds any system's 2-sigma limit under B1 or B2. If every W1 point is killed, the
  chassis's radiative sector is KILL.
- **CONDITIONAL:** no W1 point fails under B0-B2 (computed R), but some W1 point fails under B3 (computed R) or under B2
  with the universal bound; or only a sub-window survives B1/B2 (CONDITIONAL on that sub-window, KILL outside it).
  The condition is then named: the NS sensitivities at alpha_c != 0 follow the published brackets (F4-F6).
- **PASS (at the stated scope only):** every W1 point passes under B0-B3 with the computed R and under B0-B2 with the
  universal bound.
- W3 is reported as surviving sub-windows (edges in c_2 for each bracket), with the PPN alpha2 edge alongside.
- PPN consistency (reading, not the verdict): alpha1, alpha2 at the W1 corners against the record's bounds
  (DOOR11 table): |alpha-hat1| < 2.1e-5 (Liu et al. 2020) and -3.5e-5 < alpha-hat1 < 3.3e-5 (Shao & Wex 2012);
  alpha1 = (-0.7 +/- 1.8)e-4 (LLR, secondary); |alpha-hat2| < 1.6e-9 (Shao et al. 2013); |alpha2| < 2.4e-7 (secondary).

Every script ends with "N/M checks pass"; main and MUTATE outputs go to separate files.

## 8. What this lane cannot say

- It does not compute neutron-star sensitivities in the strong field at alpha_c != 0; it brackets them (B0-B3).
- It is not a full C-H/K radiation calculation: the wave zone uses the decoupling-limit quadratic action with a
  homogeneous Galactic background (XC1 A5's clock inertia); metric mixing in the MOND regime (O(1), L340's block) and
  the binary's own filtered field in the wave zone are not included except through the universal bound.
- Leading post-Newtonian order of the flux only; no strong-field preferred-frame orbital effects beyond reporting
  alpha1, alpha2; masses are taken from GR-based timing (O(s) mass shifts ignored; flagged under B3).
- It is not a timing analysis; it uses published summary numbers read through a summarising fetch tool (PROVISIONAL).
- A PASS or CONDITIONAL here is one gate on one chassis; it is not "the theory works", and it says nothing about the
  dark sector, which still requires the cold mass.

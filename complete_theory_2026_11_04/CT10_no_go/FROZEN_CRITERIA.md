# CT10: is the CT5-CT7 failure pattern a theorem? FROZEN statements (written before any script or number)

Lane under owner decision D1 and `../CT_GATES_COMMON.md`. Grading/theorem lane, not an adoption: nothing here is adopted, the cold sector retired 2026-11-01 stays retired, no particle. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled.

Gates restated (CT_GATES_COMMON.md:6-9): G0 health (DOF, no ghost or gradient instability on FRW and static backgrounds, W4b inherited UNDECIDED, CT2_REPORT.md:7); G1 law S within 0.01 dex over 1e-12 < g_b < 1e-8; G2 a0 spread <= 0.015 dex void/field/cluster; G3 d ln a0/d ln rho_DE = 0.5 +- 0.01 and tracking within 0.05 dex at z 1, 1.5, 2.33 in an evolving background. v3s khronon pair condition M_T = g/j >= 1, M_L = 1/(dj/dg) >= 1 (CT5_candidate_A/FROZEN_CRITERIA.md:41).

## The class C (precise)

S = S_GR + S_MOND[metric, khronon; a] + S_DE[Psi] + S_m[metric, matter], with

- (A1) locality: a^2 = A(Psi, d Psi) is a local function of the dark-energy fields Psi and at most their first derivatives (scalar phi with P(X, phi), X = -(1/2)(d phi)^2; a four-form q; or khronon-frame invariants);
- (A2) matter minimally coupled (Psi not in S_m);
- (A3) the MOND sector's static weak-field limit is L_M = (a^2/4 pi G) f(g/a), f(s) = s - ln(1+s) (law S, the G1 gate formula; v3s J term), flux j = a f'(g/a) = g a/(g + a), a0-charge dL_M/d ln a^2 = (a^2/8 pi G) h(s), h = 2f - s f';
- (A4) the MOND sector depends on a only through Y^(3/2) and higher on FRW (Y = 0), as v3s (CT7 S5);
- (A5) tie: on every FRW solution of the DE sector, A = kappa^2 G rho_DE (c = 1), rho_DE the DE energy density, with no bare Lambda.

Write eps = kappa^2/(8 pi) = 0.009947 at kappa = 1/2.

## T1 (frozen statement)

If the DE variable in A responds algebraically to the MOND sector (no gradient term between it and the source, so linear response is local: delta ln a = -sigma eta h(x), x = g/a0), then:
- (T1a) the response strength is fixed by the tie up to one DE-sector stiffness S_E = q^2 P''(q)/E(q) (E the vacuum Legendre energy): eta = eps S_E/2 (S_E = 2 for P = Z q^2/2, which reproduces CT5);
- (T1b) for sigma = +1 (a falls as g rises; the fixed-conjugate four-form/Henneaux-Teitelboim sign), dj/dg < 0, i.e. M_L < 0, on a band x in [x*, x_off] with x* = eta^(-1/2) (1 + O(eta^(1/2))) and x_off ~ 1/eta, for EVERY eta > 0; the band lies inside the G1 range (x <= 106.8 / 88.4) iff eta >~ 1e-4; this is model-independent given A3 (it uses only the law-S tail f'(s) -> 1 - 1/s);
- (T1c) for sigma = -1 (a rises) dj/dg > 0 identically: no M_L band, so T1 as posed is NOT a theorem for that sign;
- (T1d) an algebraic DE variable has no kinetic term, so on FRW it sits at a fixed point of its algebraic equation: w = -1 exactly. A dynamical DE field with gravitational-strength coupling (fixed by the tie) is suppressed locally (response ~ (1+w) Phi_N/c^2, CT7 l.43-55).
Expectation (hand): T1b TRUE, T1c a counterexample confined to w = -1, so "local response + evolving DE" reduces to sigma = +1 or w = -1.

## T2 (frozen statement)

For a locally inert DE scalar with P(X, phi), rho = 2 X P_X - P:
- (T2a) an exact tie with A independent of X requires rho_X = P_X + 2 X P_XX = 0 identically, i.e. P = c(phi) sqrt(X) - V(phi) (cuscuton): rho = V exactly with w != -1 allowed. Any propagating DE scalar (rho_X > 0, no ghost) needs A to depend on X, i.e. include the kinetic energy.
- (T2b) the gradient-sign flip of CT7's C' comes from using the khronon-frame energy T_nn (spatial gradients enter with + sign). With the Lorentz-scalar rest-frame energy rho(X, phi), the static gradient coefficient is P_X + eps h rho_X, which cannot flip if P_X > 0 and rho_X > 0. Expectation (hand): the flip is NOT forced; candidate C'' = "a0^2 = kappa^2 G (2 X P_X - P)" is a counterexample to be graded G0-G3 (G4 report only), stopping at the first failure.
- (T2c) the cuscuton route (A = kappa^2 G V, P = mu^2 sqrt(2X) - V) is listed; its local inertness is checked by order of magnitude only.

## Grading C'' (canonical P = X - V inside v3s, J with bare Lambda 0, phi not in S_m)

- G0 PASS iff: DOF 4 (v3s 3 + phi); FRW quadratic action of phi a-free (A4); in static backgrounds the phi time coefficient K_t and gradient coefficient K_s are both > 0 for x in [1e-3, 1e22] and w in (-1, 1); the phi-khronon mixing does not create a ghost after the khronon constraint is solved; the J-induced mass satisfies |m| R <= 0.1 as CT7. c_s^2 = K_s/K_t is reported; c_s^2 > 1 is recorded as a caveat (khronon theories have a preferred frame), not a fail. W4b inherited UNDECIDED.
- G1/G2 PASS iff the local delta ln a0 (potential channel bounded by CT7's numbers since K_s >= 1; kinetic channel order (r H)^2 eps h) gives <= 0.01 dex law deviation and <= 0.015 dex spread.
- G3 PASS iff slope = 0.5 +- 0.01 and tracking <= 0.05 dex in every realisable background from CT7 (B2, B3, F1); non-realisable ones (crossing) recorded.
- No knob is varied; kappa^2 = xi counted as a TRADE.

## Mutation control
Replace rho(X, phi) by the khronon-frame T_nn: the script must then reproduce CT7's flip at x = 108.9 (ct7_candidate_c.out C' line).

Compute: one sympy/numpy script, single thread, seconds. Commit nothing.

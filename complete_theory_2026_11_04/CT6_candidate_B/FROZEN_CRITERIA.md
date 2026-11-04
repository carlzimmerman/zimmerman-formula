# CT6: candidate B (Lambda-projector khronon), frozen criteria

Written 2026-11-04 before any number of this lane was computed. Lane under CT_GATES_COMMON.md and owner decision D1 ("Yes, grade it"): a go to GRADE, not to adopt. Nothing here is adopted; the cold sector retired 2026-11-01 stays retired. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework.

## Candidate (from CT1_REPORT.md:61-67)

Host: v3s as written in covariant_push_2026_10_22/V3_FULL_PICTURE.md:23-37 (Blanchet-Skordis khronon, J_x, K(Q) = mu_K^2 (Q-1)^2, switched stiffness). Change: the hand-set a_geo^2 = (a0/c^2)^2 inside J_x is replaced by

    a_geo^2 = xi * Qp,   Qp = K^2/3 + (2/3) L_n K,

with K the trace of the extrinsic curvature of the khronon leaves (K = nabla_mu u^mu) and L_n K = u^mu d_mu K. On FRW with GR's Friedmann equations Qp = 3H^2 + 2 Hdot = Lambda - 8 pi G p / c^2 (dust cancels).

## Gates, fastest death first (numbers restated from CT_GATES_COMMON.md / CT1 / CT2 / CT3)

- **G0 health.** PASS needs all of:
  (a) DOF count: either the L_n K dependence is degenerate (no extra DOF), or the extra DOF is removed by a constraint (cuscuton / VCDM / CMC type), or it propagates; in every case the count must be the same on FRW (with matter), on static backgrounds and on galaxy backgrounds (a count that changes between backgrounds = strongly coupled mode = FAIL);
  (b) every propagating scalar has positive kinetic coefficient (no ghost) on FRW with matter and on static backgrounds;
  (c) no UV gradient instability: lim k->inf omega^2/k^2 >= 0 for every mode;
  (d) the action is real and its quadratic action regular (finite coefficients) on those backgrounds;
  (e) any constrained (CMC-locked) variant must not reproduce the record's VCDM + f(a^2) FLRW obstruction (qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/FLRW_OBSTRUCTION.md: f_s(0) = 1 gives negative matter kinetic coefficient and c_UV^2 = -1/(6+9 c_m^2)). If the variant's coefficients match that theorem's premises, the record's result is used, not re-derived.
  W4b (solar-background health of v3s) is inherited UNDECIDED (CT2_REPORT.md:7) and does not decide this gate.
  Frozen-coefficient (WKB) results at frequencies of order H are reported as UNDECIDED, not as pass or fail, because expansion corrections are the same order.
- **G1 weak field.** g_obs = (g_b + sqrt(g_b^2 + 4 g_b a0))/2 within 0.01 dex over 1e-12 < g_b < 1e-8 m/s^2, both footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2, never pooled).
- **G2 local constancy.** a0 varies by at most 0.015 dex between void, field and cluster environments (at r <= 30 kpc, CT1_REPORT.md:80).
- **G3 tie.** d ln a0 / d ln rho_DE = 0.5 +- 0.01; a0(z) tracks sqrt(rho_DE(z)) within 0.05 dex at z 1, 1.5, 2.33 in an evolving background; state what fixes kappa (kappa = sqrt(8 pi xi) in CT1's reading, a TRADE).
- G4-G7 as in CT_GATES_COMMON.md; not reached unless G0-G3 pass.

## Rules

Stop at the first failed gate; record it as hard as a pass; no tuning, no knob scans. Count every hand-set constant. Small symbolic checks only (sympy, single thread). Commit nothing.

## Expected (written before computing)

CT1 expects B to die at G0 or G2. Expectation here: the MOND sector depends on a_geo nonlinearly (deep-MOND scale invariance forces Y^(3/2)/a_geo), so the K-dot dependence is non-degenerate wherever Y > 0; a CMC lock removing it should fall under the VCDM theorem since J_x has dJ/dY = 1 at Y = 0 in the f_s(0) = 1 sense. The unlocked form's extra mode sign is not guessed here.

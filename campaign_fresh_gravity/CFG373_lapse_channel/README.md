# CFG373: the khronon's instantaneous (lapse) mode as carrier and reaction sink of fluid settling

Criteria: `FROZEN_CRITERIA.md`, committed alone first in c3bcfdafa. Analytic, symbolic and order-of-magnitude work; seconds of CPU.

**Verdict: CONDITIONAL.** It is not a derivation: screen Q1 fails, because a0 is an input.

| gate | result |
|---|---|
| **G1 carrier** | **PASS (symbolic, zero constants).** For P2, g^2 + a_L^2 = (g_N + a_L)^2 exactly (a perfect square). So the fluid's target density is a LOCAL functional of the total field, rho_target = div[(abs(g) + a_L - sqrt(g^2 + a_L^2)) g_hat]/4 pi G. It reproduces CFG44's exact point-mass target M(sqrt(1+x^2) - 1), and the total field then obeys the law (the AQUAL form). In the chassis the lapse gradient IS the total field, set by the leaf-elliptic (instantaneous) equation (CFG292). The nonlocality CFG60 demanded is supplied by gravity's own elliptic solve: no baryon-reading switch is needed. |
| G2 relaxation | CITED: this is CFG245's construction (rate, precision, energy and ownership failures stand). The cooling-keyed rate fits the pincer only in the R2 cells (CFG369/370). |
| **G3 reaction sink** | **CONDITIONAL.** Force density needed at the MW anchor (10 kpc): f_req = 1.8-3.0e-34 N/m^3. The khronon's static alpha_c channel can carry only 1e-11 to 5e-7 of it (FAIL across the record window). The K^2 (c_2) channel carries 2.4e2 to 3.7e3 x the need, but ONLY if relaxation induces a congruence expansion K ~ Gamma/c (a local expansion-rate perturbation of order the cooling rate). That is assumed, not derived. |
| G4 energy into the vacuum | PASS: 3e-8 to 1.3e-5 of rho_Lambda c^2 (even CFG70's 318x energy is cosmologically negligible). |
| G5 causality | PASS by citation (CFG292: instantaneous within a leaf, criterion B). |
| G6 local tests | The alpha route would need alpha_c 1e7-1e11 x the window ceiling (excluded). The c_2 route stays inside the window. |
| Screen Q1 | FAIL (expected): kappa is not fixed. |

**What this establishes.**
1. **The missing geometry, part one: found and certified.** The law's hyperbola (p61) inverts EXACTLY into a local rule. The time field's lapse tells each fluid element its target density instantly, with zero new constants.
2. **CFG70's energy objection dissolves** if the exchange energy goes to the vacuum: it is 1e-5 of rho_Lambda or less.
3. **The remaining single assumption:** the reaction is absorbed by the khronon's K^2 sector through K ~ Gamma/c during settling. It is the next thing to DERIVE (does the khronon's own equation produce that K when the fluid relaxes?). If it does not, the sink fails and the record's reaction wall stands.

**Disclosed:** the first run reported G1 as FAIL because sympy did not denest sqrt(x^4 + 4x^2 + 4) = x^2 + 2; the printed "difference" was identically zero. The check now verifies the perfect-square identity by expansion, plus a numeric check. G3 is an order-of-magnitude budget, not a solution of the coupled field equations.
Controls C1 and C2 pass. MUTATE (alpha_c x 1e12) flips G3 to PASS via the alpha channel, rc 1.

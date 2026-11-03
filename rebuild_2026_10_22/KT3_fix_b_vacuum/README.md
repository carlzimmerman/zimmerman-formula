# KT3_fix_b_vacuum: NO FIX. With chi's vacuum sourcing rho_DE, kappa^2 = 2 pi / DU at n = 2, and DU contains the free constant C. kappa = 1/2 needs DU = 8 pi; no listed way of setting C gives it

Criteria: `FROZEN_CRITERIA.md` (6db6a575e0), alone first, confirmed landed before the run, **not blind**. `kt3.py`, `kt3.out`, `kt3.json`, `kt3_MUTATE.out`, `kt3_MUTATE.json`. No download. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Not a no-go theorem outside this action. Register K817.

| Way to set C | DU | kappa | In rho_DE window |
|---|---|---|---|
| C = 0, n = 2 | 3 | 1.447 (a0 = cH/2) | no |
| U = 0 at chi = 1/2 (Y = 1) | 0.136 | 6.79 | no |
| U = 0 at Planck Y_c, 3e61, hbar enters | 280.1 | 0.150 | no |
| C = 0, n = 3 | 1 | 1.671 | no |
| C = 0, n = 4 | 1/3 | 2.171 | no |

Row d of the criteria turned out the same as row b.

**Why it can't fix b.** The action fixes only the combination DU/b^2. Adding a constant to U doesn't change chi's or phi's field equation, and only gravity sees it. This is L226's zero mode, reached again from the kernel side.

**Dynamics.** chi = 1 is an inflection, V'(1) = V''(1) = 0. On de Sitter, delta = 1 - chi = 3H/(A t), with A = 2 s^2/(b^2 K). The sympy residual is zero. An attractor exists for every b and C, so b only sets the decay amplitude. **The line in `kt3.py` saying w's shift falls as t^-4 and can't be tested is my hand scaling, printed as text, not computed.** No usable second prediction, so S4 isn't met.

**Controls.** MUTATE 8 pi G -> 4 pi G halves kappa^2 as expected, exit 1. Scale invariance holds. Input H0 and Omega_L enter only row c's Y_c.

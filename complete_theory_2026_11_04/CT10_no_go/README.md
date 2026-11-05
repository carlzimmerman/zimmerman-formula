# CT10: is the CT5-CT7 pattern a no-go theorem? Partly. T1 holds for one sign; T2 is false: counterexample C''

Theorem lane under D1 and `../CT_GATES_COMMON.md`. Grading only: nothing adopted, the 2026-11-01 retirement stands, no particle. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Statements frozen in `FROZEN_CRITERIA.md` before any number. `ct10_no_go.py` (sympy/numpy, one thread, ~0.17 GB, seconds) -> `ct10_no_go.out` (19/19); `--mutate` (khronon-frame T_nn) -> `ct10_no_go_MUTATE.out` reproduces CT7's flip at x = 108.9.

## T1 (algebraic, locally responding tie)
- Response strength is fixed by the tie up to one stiffness: delta ln a = -eta h(x), eta = (kappa^2/8 pi) S_E/2, S_E = q^2 P''/E (out:14-16; S_E = 2 for CT5).
- Any response: M_L < 0 iff da_loc/dg < -(a_loc/g)^2 (out:17-18).
- Sign "a falls" (fixed-conjugate four-form, CT5): a band exists for EVERY eta > 0, onset x* = eta^(-1/2)(1 + O(eta^1/2)), to x ~ 1/eta (out:20-27); inside the G1 range iff eta >= 8.6e-5 / 1.25e-4, i.e. S_E >= 0.017 / 0.025 (out:28). Model-independent given law S (it uses only the tail h' -> 1).
- Sign "a rises": no band (out:29): T1 is not a theorem for that sign.
- Both signs: an algebraic variable has no kinetic term, so w = -1 on FRW (out:30-32, structural). Local response + evolving DE is empty.

## T2 (locally inert scalar P(X, phi))
- T2a TRUE: an exact tie with A independent of X needs rho_X = 0, i.e. the cuscuton P = c sqrt(X) - V (rho = V, w != -1) (out:37-39). Any propagating DE scalar must put its kinetic energy into a0^2.
- T2b FALSE: the flip is not forced. It comes from CT7's khronon-frame T_nn (gradients with + sign; K_s = 1 - eps h, MUTATE). With the Lorentz-scalar rest-frame energy rho = 2XP_X - P, K_s = P_X + eps h rho_X (out:40-43): no flip whenever the scalar itself is healthy.

## Candidate C'': a0^2 = kappa^2 G (2XP_X - P), canonical phi inside v3s
- G0 PASS (conditional): 4 DOF; FRW plain quintessence (out:56); K_s >= 1, K_t > 0 on x 1e-3..1e22 (out:46-53); khronon constraint adds +B^2/|L_gg| (out:55). CAVEATS: phi is superluminal in high-x regions, c_s^2 -> 2/(1-w) (1.05 at w -0.9; out:54); quasi-static mixing only; W4b UNDECIDED.
- G1/G2 PASS: spread <= 1.6e-9 / 1.8e-9 dex (out:61-63, order-of-magnitude bounds).
- G3 PASS by construction: slope 0.5 exactly, tracking 0 dex in every realisable background (out:64); the DESI crossing backgrounds are not realisable (canonical).
- Not graded here: G4 (expected inherited, as CT7), G5 dust (CT8 fails for every candidate).
- Hand-set: xi (kappa^2 = xi, TRADE), V0, V's shape, phi_i, L*, mu_K, J_x form, dust abundance.

kappa = 1/2 FITTED; not theory closed.

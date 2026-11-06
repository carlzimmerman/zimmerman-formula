# QX6 iter 2: a0 tied to the dark-energy density seen in the khronon frame, f(Q) derived

Derivation (stated before code). a0 = kappa c sqrt(G rho_DE). Read locally, rho_DE is the energy density a static
khronon-frame observer measures. v3s: rho_DE enters as Lambda inside J(Y). A cosmological constant is frame- and
lapse-invariant, so f == 1 exactly, F = 1, and this reduces to QX2 iteration 1. AC2q: the clock phi(t) in unitary
gauge has X = s^2/(2 N^2), with lapse N = 1 - (Q - 1) to first order and V(phi) unchanged in statics. So
rho_loc/rho_bg = 1 + (X_bg/rho_bg)(N^-2 - 1), with X_bg/rho_bg <= 1, because s^2 <= 2 rho_DE gives X <= rho_DE
for V >= 0. Then a0_loc/a0 <= 1/N. Converting proper to coordinate acceleration costs at most one more factor 1/N.
Bound: a0_eff/a0 <= N^-2 <= 1 + 2.1 (Q - 1) for Q - 1 <= 0.01 (Lean-certified). The phantom grows no faster than
a0 (deep law g ~ sqrt(a0 gN); Newtonian-side phantom ~ a0), so F - 1 <= 2.1 (Q - 1).

Graded: X-COP with a0 -> a0 (1 + 2.1 k) at every point, k = QX5's key a. This is the largest boost the tie allows.
Label: DEAD if G-X fails on both footings. Reported: max(F - 1) against the F_req minimum (2.35 / 2.11), as a factor.
MUTATE (power): an amplitude x1e4 (a0 -> a0 (1 + 2.1e4 k)) must move X-COP's mean Delta by <= -0.2.

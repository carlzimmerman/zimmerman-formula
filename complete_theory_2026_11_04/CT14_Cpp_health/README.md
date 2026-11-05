# CT14: full G0 health of C''. G0 FAILS: a gradient-type instability on static backgrounds wherever g/a0 > s*(1+w)

Lane under owner decision D1 and its follow-up ("Yes, grade it"), and `../CT_GATES_COMMON.md`. Grading only: nothing adopted, the 2026-11-01 retirement stands, no particle. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Criteria `FROZEN_CRITERIA.md` were written before any number. Scripts are single-thread and seconds to minutes each, with peak RSS 0.21 GB (the V3X background children use 0.31 GB). Nothing is committed here.

| item | verdict | evidence |
|---|---|---|
| H1 FRW, exact in k (curvature mode psi, dust, lapse, shift, P via c_Y) | **PASS** | `ct14_h1_frw.out`:5, :84-85 |
| H2 static weak field (P sector, stiffness, dust, lapse) | **FAIL** | `ct14_h2_static.out`:14, :18-25, :45-46 |
| H3 W4b (solar background) | **UNDECIDED**, with one named line left | `ct14_h3_w4b.out`:27-29 |
| H4 tracker / freezing branch | **PASS (restricted)** | `ct14_h4_tracker.out`:77-80 |

**G0 is FAIL** because of H2, so the candidate stops at G0.

## H1. FRW
- On exact FRW, L_M's a-dependence first enters at order Y^(3/2), which is cubic in perturbations (out:5). At quadratic order phi is therefore minimally coupled quintessence.
- The ADM quadratic action in the dust's unitary gauge was computed exactly in k.
  - The kinetic matrix of (zeta = psi, delta phi) has det/K_phiphi = [(rho_d + p_d)/c_d^2 + 2 c_Y k^2] a/4H^2 > 0 (out:13-16).
  - It is positive definite in every case: exact FRW, leaf-averaged E up to 5.92e5, and static coefficients up to s = 1e22.
  - The phi branch keeps its own speed K_s/K_t, so mixing produces no CT7 flip (out:84-85).
- Reported, not graded: with c_Y > 0 and a second component with rho + p > 0, the dust branch has a k-independent rate of 0.28-0.93 H (out:78-83).
  - It also appears with E = 0 and a canonical field, so it comes from v3s and not from the tie.
  - It sits below the Hubble friction of 3H/2.

## H2. Static weak field: the new failure
In v3s the khronon acceleration perturbation is delta A = grad(delta Phi - delta sigma_dot). It contains the khronon's velocity, so the phi-A mixing L_{A rho} v phidot enters the **kinetic** matrix.

For k parallel to g, the determinant is L_AA k^2 K_eff with
K_eff = 1 + eps[h - (1+w) s^3/(2(1+s))] (sympy, out:14).
This is the fixed-P coefficient. CT13's R2 treated delta g as a static constraint (+B^2/|L_gg|), which drops exactly this term.

The mutation that restores CT13's quasi-static treatment reproduces CT13's pass, K_t 1.973 against R2b's 1.973 (out:27-32). The full system then grows at |Im omega| = 1.47 k at s = 108.9, 1+w = 0.05. The growth rate scales with k, so this is a UV gradient-type instability (out:28, :45; 1566 of 8736 cases).

Thresholds s* (out:18-25), with g* canonical / alt in m/s^2:

| 1+w | s* | g* |
|---|---|---|
| 0.3 | 29 | 2.7e-9 / 3.3e-9 |
| 0.1 | 55 | 5.1e-9 / 6.2e-9 |
| 0.05 | 85 | 7.9e-9 / 9.6e-9 |
| 1e-2 | 268 | 2.5e-8 / 3.0e-8 |
| 1e-3 | 2084 | 1.9e-7 / 2.4e-7 |
| 1e-4 | 2.0e4 | 1.9e-6 / 2.3e-6 |

The unstable cone is theta < 6-17 deg at 2 s*.

- Inner galaxies outside L* reach these accelerations: the Milky Way at 30-100 pc reaches ~0.7-1.6e-8, and massive ellipticals at 100 pc reach ~6e-8. A realised thawing DE with 1+w0 >= ~0.03 (B2 0.1, B3 0.05) is therefore unstable there.
- Only w = -1 exactly (v = 0) escapes, and that is Lambda, which G3 does not allow.
- The phi gradient coefficient never flips: min K_s = 1 (out:47). The failure is in the kinetic sector.
- At s <= 10 there are no failures (out:35-38). The failures are at s >= 108.9 (out:39-42).

## H3. W4b
In CT2_REPORT.md:7, "W4b" is solar-background health; V3W and V3X call this item W4c.

- V3X's own spectrum was rerun (imported read-only) in float64. It reproduces V3X's 40-digit values to 6.4e-15 and a 30-digit rung at nd 24 to 1.3e-15 (out:27).
- Every omega^2 is positive and the operators stay positive definite on every rung from 12 to 48 cells/decade (out:28).
- The ladder changes by 14.6 %, 7.9 %, 2.0 % and then 1.36 % on the last pair (32 -> 48), which is under the 5 % line (out:12, :29). The PN ladder line is now closed.
- Left open: V3X's relativistic tensor line. The roots sit 1.1e-10 below 1 against a 1e-10 line. This lane did not relax that line; c_T itself is graded by W4a at <= 5.1e-32.
- On the solar background C'' has s ~ 1.8-2.2 (M_lo 3.20 / 2.82), far below s* >= 15.4, so phi adds nothing there.

## H4. Tracker branch
CT13 evaluated E at today's a0. In C'', a0 is tied to rho_phi, so an early-rolling field has a larger a0, a smaller s and a smaller E.

| members | result | out lines |
|---|---|---|
| Thawing T1 (exp, lambda 1), T2 (pNGB) | Survive: late-time change <= 1.3e-7 in ln rho, even though E reaches 1.5e6 | :6-19 |
| Inverse power laws n = 1, 2, 6, tracker or undershoot initial conditions | Survive: late-time change <= 5.3e-8, min K_t = 1. For n = 1 the history above z ~ 1e8 differs and heals on the attractor | :34-75 |
| n = 0.5 | Broken: runaway up the potential at z ~ 1e8-6e8 in 10 of 12 runs | :20-33 |

Reach (G3 at 0.05 dex):
- B2 is reached by T1 (0.012 dex) and T2 (0.042 dex).
- B3 (freezing) is reached by no survivor. The best is n = 1 at 0.070 dex; n = 0.5 would reach it at 0.018 dex but is broken. n between 0.5 and 1 was not graded.
- Restriction recorded: inverse power laws with n >= 1 and the thawing class.

## Hand-set constants
kappa^2 (= xi, a trade), V's shape and scale, phi_i, L*, mu_K, the J_x form, and the dust amount. kappa = 1/2 FITTED; not theory closed.

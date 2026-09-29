# CFG172D — Door 11C-d: V0 (C-H/K) with its region gate replaced by the flow's expansion theta. Phase 2 results

Frozen criteria: `CFG172D_FROZEN_CRITERIA.md` (sha256 e8cc60f39bc110922f6f52e3b6c3df2a45b14a557761c3ed701eeaa1bfff24da, committed before any script). Scripts and outputs are named `CFG172D_*`. Nothing in the repository was edited (imports of `Bcommon.py`, `Gcommon.py`, the L352 constant prefix and the DE12 result JSON are read-only). kappa = 1/2 is FITTED. **A scoped no-go is not a closure**: everything below holds inside the frozen class (V0's action with f = W(t(u_theta)); arms d1, d1-alt, d2 lin/sat; static spherical weak field; c1_3 = 0; nu_mono kernel in the region term; rule T; c2 in L340's window; the declared grid). It does not say the theory is closed, that the timelike-flow reading is refuted outside the class, or that any data favour the framework.

## Read this first

1. **Nothing passes G1, so nothing is flagged for an independent re-derivation as a derived mechanism.** Every arm fails G1-law (strict and edge, against P2 and against nu_mono) in every solve (56 solves per arm; script `CFG172D_A2_static_solve.py`).
2. **The obstruction is NOT removed by the theta replacement, in any arm** (script `CFG172D_A3_obstruction.py`). d1 is stable only because the gate is never on along the continuation branch (MOVED, blind); its alternative S-curve branch switches the gate on only at high acceleration (the wrong end of the law). d2 makes the gate region-selective, but only with a baryon-fluid instability of c_eff = 4e3-9e3 km/s at each cell's smallest region-selective zeta (line 37 km/s); no zeta satisfies O1 and O2 in any of the 96 cells, in any of the four coupling/gate variants.
3. **A process event, kept.** The first A3 run carried a unit error (c_eff in km/s divided by 1000 again) and printed "REMOVED in the joint sense in 2/8 combinations" for the monotone-gate sensitivity. The hand pincer formula disagreed with the number by exactly a factor 1000 (hand 1101 km/s, script 1.098), which is how it was found. The error was fixed and A3 re-run; every number below is from the corrected run. That first output was overwritten and is not in this directory.

## Re-run

    cd <repo>/campaign_fresh_gravity/CFG172D_door11C_d     # or any directory, with ZF_REPO=<repo>
    ZF_REPO=<repo> python3 CFG172D_A1_theta_equation.py         # ~40 s   (sympy)
    ZF_REPO=<repo> python3 CFG172D_A3_obstruction.py            # ~9 min  (writes zeta_min_reference read by A2, A4)
    ZF_REPO=<repo> python3 CFG172D_A2_static_solve.py           # ~2.5 min
    ZF_REPO=<repo> python3 CFG172D_A4_gates_G2_G5_G6_G7.py      # seconds
    ZF_REPO=<repo> python3 CFG172D_A5_stress_energy.py          # seconds
    ZF_REPO=<repo> python3 CFG172D_verdict.py                   # reads the JSONs, prints the table, no physics
    # MUTATE controls (each writes *_MUTATE_<name>.out/.json and exits 1 when the control bites):
    ZF_REPO=<repo> MUTATE=M6 python3 CFG172D_A1_theta_equation.py ; ... MUTATE=M7 ...
    ZF_REPO=<repo> MUTATE=M1 python3 CFG172D_A3_obstruction.py   ; M2 ; M3 ; M4 ; M5
    ZF_REPO=<repo> MUTATE=M2 python3 CFG172D_A2_static_solve.py  ; M3
    ZF_REPO=<repo> MUTATE=M4 python3 CFG172D_A4_gates_G2_G5_G6_G7.py
    ZF_REPO=<repo> MUTATE=M8 python3 CFG172D_A5_stress_energy.py

The scripts find the repo root from `ZF_REPO` or by walking up from `__file__` and print `<repo>/...` only. numpy 1.26, scipy 1.14, sympy 1.13 (python 3.13). Order matters only for A2 and A4, which read A3's `CFG172D_A3_obstruction_results.json` for the reference zeta (the smallest zeta that makes the reference cell 1e11 Msun, z = 0.25, canonical, w = 0.25, c2 = 7.3e-3 region-selective: lin 1.78e-5, sat 3.16e-5). A2's `CFG172D_A1_rest_expr.txt` is written by A1.

Files: `CFG172D_common.py`, `CFG172D_solver.py` (shared machinery, incl. the DE12 layer copy); `CFG172D_A1..A5_*.py`, `CFG172D_verdict.py`; for each `.out` and `_results.json`; `*_MUTATE_<name>.out/.json`; `CFG172D_A1_rest_expr.txt`; this README. (Scratch probes `h1_probe*.py`, `h1_ELq.txt` and the `a*_run.log` files are not part of the lane.)

## Gate table per arm (each cell cites its script; PASS / FAIL / UNDEFINED / NOT ADDRESSED)

Arms: **d1** = gate-sourced compaction, frozen (continuation branch). **d1-alt** = SENSITIVITY: the upper stable S-curve branch of the same equation (added after A3 found alternative roots). **d2 lin, d2 sat** = the explicit source in the FROZEN gate variable u_theta = D(theta)E^-2, D = (thetabar/theta)^2 - 1. **mono lin, mono sat** = SENSITIVITY: the same coupling with a monotone gate (f = 1 for theta <= 0), added after the frozen variable was found band-pass (see wrong expectations). Sensitivities are reported beside, never pooled with the frozen arms. zeta for d2 is the reference-cell zeta_min, the same at every mass, z, footing and profile.

| gate / test | d1 | d1-alt (sens.) | d2 lin | d2 sat | mono lin (sens.) | mono sat (sens.) |
|---|---|---|---|---|---|---|
| O3 plateau identities, background off-plateau, constraint symbols (A1) | PASS | PASS | PASS | PASS | PASS | PASS |
| O2 region-selective (A2, self-consistent) | FAIL: f = 0 in 56/56 | FAIL: f(3 r_M) >= 0.99 in 0/56; gate ON only to ~2-3 r_M | FAIL: 19/56 at 3 r_M; a shell (band-pass) | FAIL: 31/56 | FAIL: 50/56 at 3 r_M, never to 30 r_M | FAIL: 40/56 |
| O1 stable (A3; line c_eff <= 37 km/s, single-valued) | PASS, but blind (c_eff = 0) | NOT ADDRESSED | FAIL: c_eff at zeta_min median 9.1e3 km/s | FAIL: 6.1e3 | FAIL: 5.2e3 | FAIL: 4.2e3 |
| **Obstruction verdict (A3)** | **MOVED (blind)** | NOT ADDRESSED beyond O2 | **STILL PRESENT** | **STILL PRESENT** | STILL PRESENT | STILL PRESENT |
| zeta-interval: zeta_min/zeta_max (>1 = empty) (A3) | n.a. | n.a. | 1.8e3 | 5.6e4-1.8e5 | 1.8e3-5.6e3 | 5.6e4-1.8e5 |
| added reach test (not frozen): gate ON to 30 r_M and O1, some zeta (A3) | n.a. | n.a. | 0/96 | 0/96 | 0/96 | 0/96 |
| G1 law strict, P2 / nu_mono (A2) | FAIL / FAIL (max dev 0.97) | FAIL / FAIL (2.2) | FAIL / FAIL (7.1) | FAIL / FAIL (29) | FAIL / FAIL (2.9) | FAIL / FAIL (3.3) |
| G1 law edge (x <= x_ta), P2 / nu_mono (A2) | FAIL / FAIL | FAIL / FAIL | FAIL / FAIL | FAIL / FAIL | FAIL / FAIL | FAIL / FAIL |
| G1 mechanism | FAIL (nothing to grade) | FAIL | at best M1 "P-declared"; law fails, so no pass | same | same | same |
| G2 growth (A4) | PASS trivially (gate never on; MOND never on either); CMB UNDEFINED | PASS on the web (f_web = 0); CMB UNDEFINED | FAIL: web contact instability, Gamma/H up to 7.7 (line 0.05); CMB UNDEFINED | FAIL: up to 14 | FAIL: 7.7 | FAIL: 14 |
| G3 reaction / energy (A2) | PASS trivially (no coupling, gate off) | NOT ADDRESSED | FAIL: gate force 0.25, contact 5.6e4 x g_law (line 0.10); energy 3.0e4 x orbital (line 1) | FAIL: 5.3, 49; 209 | FAIL: 1.3, 5.6e4; 3.0e4 | FAIL: 1.4, 141; 209 |
| G4 constants (A5 ledger; criteria 1.5) | FAIL strict (inherited V0 constants); new: 0 | same, 0 | FAIL strict; new: 1 (zeta) | new: 1 + h shape | new: 1 | new: 1 + shape |
| G5 (A1, A3, A4) | ghost PASS (c2 > 0); Q2 0 (gate off); criterion B, filtered remainder, MW tide NOT ADDRESSED | NOT ADDRESSED | O1 FAIL => FAIL; Q2 not triggered because the frozen gate is OFF at the Sun (band-pass artefact); B/filtered/MW NOT ADDRESSED | same | Q2 FAIL where the gate is ON at the Sun: 1.3e4 x the bound (isolated, unfiltered) | same |
| G6 (A4) | PASS (inherited V0/KM3 formulas, table below) | PASS (same) | UNDEFINED (the coupling's contribution not derived) | UNDEFINED | UNDEFINED | UNDEFINED |
| G7 (A4) | PASS on record inputs (KM1's D, CV4's dipole not re-derived) | same | UNDEFINED for the coupling's own dipole; a0 part PASS on record inputs | same | same | same |
| S1 / S2 owner's picture (A5) | PASS: no flow rest mass, Q = 0, density a functional of baryons | PASS | PASS (labelled matter-flow coupling) | PASS | PASS | PASS |

G6 outcomes as printed by `CFG172D_A4_gates_G2_G5_G6_G7.py` (KM3's V0 formulas alpha1 = -4 alpha_c, alpha2 = alpha_c(alpha_c - c2)/(2 c2); limits quoted, from memory, unverified): at alpha_c = 1e-13 and 3.2e-9, c2 = 7.3e-3 and 0.067, |alpha1| <= 1.3e-8 passes at 3.4e-5, 3.5e-5 and 2.1e-5 (Liu+2020, as quoted) in all four cases; |alpha2| = 5e-14 (alpha_c = 1e-13) and 1.6000e-9 (alpha_c = 3.2e-9) pass 1.6e-9 with relative margins 1 and 4.4e-7 (c2 = 7.3e-3) / 4.8e-8 (c2 = 0.067): the window edge is borderline by construction. The G6 verdict for d2 is UNDEFINED, not PASS.

## What the scripts showed (by script)

**A1 (sympy, exact).** H-i and H-ii were re-derived from V0's covariant brace, tau = t + eps*pi(t,r) on -N^2 dt^2 + a(t)^2 A(r)^2(dr^2 + r^2 dOmega^2), every leafwise auxiliary a generic function of (t,r), including Delta_h, the projected gradients, the 4-acceleration, eps_d = u u T and the baryon coupling. The theta channel is exactly div[h grad Pi/sqrt(-X)] (difference 0). **H-i holds in the static, non-expanding limit (E-L[REST] = 0) and is FALSE with adot != 0**: E-L[REST] is a degree-2 polynomial in adot with no adot^0 part, an O(H) MOND-sector source of theta. **H-ii holds**: alpha_c enters the remainder only multiplied by adot. Its size (A2, estimate on the original-gate solution, weak field): |delta theta_H|/thetabar <= 4.8e-4 (1e11 and 1e12, z = 0.25), 9.5e-5 (z = 2.5), 2.6e-5 (1e10, z = 4), against the ~0.5 depletion the gate needs. T-d1 (Pi = Pi0 forces the same theta on every plateau) and the d2 pincer c_s^2/c^2 = -zeta^2 eps_b/(3 c2 eps_L) = -3 c2 Delta^2 eps_L/eps_b are confirmed symbolically. O3a: the NR Euler-Lagrange equations (Phi = u + fP, lam = -f Psi, (lap - M^2) w = 4 pi G f rho_b, the P equation) have zero residual with f(r) generic. O3b: the background is off-plateau for both w (max t = -1.5 for w = 0.25, 0 for w = 1, z in [-0.5, 20]). O3c: the local Hessian in (Psi, w, theta) was derived from the Lagrangian; the (Psi, w) constraint block's determinant is -(k^2 + M^2)^2/16 (no f'', no c2, no f'), the theta-theta entry is (-2 c2 + B f'')/4 with B = a0^2 q + Psi(m^2 w - lap(u - v)) + sigma m^2 w^2, and the Schur complement tends to it at high k. C7: W'' extrema +-9.841 at t = 0.218 / 0.782, W'(1/2) = 2.

**A3 (obstruction).** C4: the DE12 re-implementation reproduces all 24 committed cells exactly (relative deviation 0); with V0's original gate min c_gate = 1526 km/s and min Gamma/H = 2.0e4 at z = 0.25. V0's full B = dL/df on the original-gate layers is within 7% of its a0^2 q part (ratio 0.94-1.07), which confirms the record's DE7 statement. d1: on the continuation branch f' = 0 at theta = thetabar, so theta = thetabar and f = 0 at every radius in all 96 cells; but the local equation has alternative roots (S-curve) at some radius in 93/96 cells, and **the stable upper branch turns the gate ON (f > 1/2) only where the local acceleration is high**: outermost radius median 0.78 r_M (max 7.6 r_M), lowest g_N/a0 with f > 1/2: median 1.6, minimum 0.017 (the law needs it down to ~1e-3). d2: zeta_min per cell and the c_eff at it as in the table; the hand pincer sqrt(3 c2 Delta^2 eps_L/eps_b) c = 1101 km/s against the script's 1098 km/s at the reference cell (eps_b/eps_L = 935 at the layer, Delta = 0.76). No zeta gives O1 and O2 in any cell, and none gives O1 with the gate ON to 30 r_M.

**A2 (static solve).** Controls: C1 (P2 identity, 3e-16), C5a plateau g = nu_mono g_N to 3e-5, C5b gate off g = g_N exactly. d1 residual: at 3 r_M V0's original prescribed gate would need theta/thetabar = 0.008-0.11 in every cell, the theta equation gives 1. G1 numbers in the table are the maximum |g/g_target - 1| over x in [0.1, 30]; the best solve of any arm is 0.966 (the fully-off value). The large maxima of the even/sat arms are dominated by the gate force f'P in thin transition layers (grid-resolution limited); the FAIL verdicts do not depend on them. d1-alt: 3/56 solves did not converge (max |df| > 1e-3); half-gate radius 1.8-2.9 r_M. Even-variant arms: the ON region is a shell (density band-pass) with an outer edge at 777-2.7e4 r_M in the solves where it exists.

**A4.** G2: c_s^2 = -zeta^2 eps_b/(3 c2 eps_L) c^2 at the cosmic mean baryon density gives |c_s| = 9.7 km/s (z = 0) to 77 km/s (z = 3) for zeta = 1.78e-5, Gamma/H = 0.014-7.7 over k in [0.1, 30]/Mpc, z in [0, 10] (sat: 0.025-14). G5: the unfiltered isolated Sun at Saturn: g_N/a0 = 6.9e5, h = 1.031, a_anom = 9.7e-11 m/s^2, Q2 = 6.7e-23 s^-2 = 1.3e4 x the bound 5.2e-27 (the record's ~a0 tail). Gate at the solar baryon density (0.1 Msun/pc^3): OFF (theta/thetabar = -777, -8.3) for the frozen even variant, ON for the monotone one. KM1's D/3 control 0.114 / 0.285 reproduced; D/3 = 3.7e-4 (c2 = 7.3e-3), 4.0e-5 (0.067) at 600 km/s.

**A5.** S2(b): h^{0 nu} = 0 for the static/comoving flow, so J^0 = 0: no charge. S2(a): no rest-mass parameter in the theta/khronon sector (the web-screening mass m belongs to V0's auxiliary field, inherited and flagged). S1: the d2 interaction pressure is isotropic and negative, E_int/eps_b = -3.2e-6 at zeta = 1e-3 (z = 0.25, mean baryon density).

## MUTATE outcomes (M1-M8 of the frozen criteria)

| control | script | outcome (exit code) |
|---|---|---|
| M1 restore the original gate | A3 | BITES (rc 1): min c_gate 1526 km/s > 117, Gamma/H 2.0e4 > 1e3 on every z = 0.25 galaxy layer |
| M2 drop the theta coupling (zeta = 0) | A3, A2 | BITES (rc 1 both): O2 fails in every cell (A3); G1-edge fails in every lin/mono solve (A2) |
| M3 flip the sign of the coupling | A3, A2 | BITES (rc 1 both): the gate never turns on |
| M4 c2 x 0.01 | A3 | BITES (rc 1): |c_s| at zeta_min drops ~20x but stays 239 km/s median (> 117) with max 6.0e3 |
| M4 (G7 side) | A4 | **DOES NOT BITE on the primary metric** (rc 0): D = 0.11 crosses 10% but D/3 = 0.037 does not; bites only on D |
| M5 prescribed gate, f not varied | A3 | **DOES NOT BITE** (rc 0): the original prescribed gate passes O2 (f(3 r_M) >= 0.99 and web off) in only 18/48 cells; it reads baryons plus phantom, so it is ON in baryon-poor outskirts by design and fails my baryon-contrast web test |
| M6 drop the leaf-mean offset | A1 | BITES (rc 1): t_bg = 0.276 > 0 for w = 1 |
| M7 c2 -> -c2 (ghost) | A1 | BITES (rc 1): d(theta stiffness)/d c2 changes sign |
| M8 give the flow a charge | A5 | BITES (rc 1): S2(b) flips, rho_Q ~ Q/a^3 |

## Kill table (from what the scripts showed)

| prior kill | escaped? | evidence |
|---|---|---|
| FC-KH (yq)' theorem | NOT ADDRESSED | the radial principal coefficient of the khronon with the gate term present was not computed (frozen 5 asked for it). The gate adds a function of theta, not of a; no script tested it |
| KM1 (a0 tracks CMB-frame speed unless c2 >> 1e-4) | a0 part: escaped on record inputs; d2's coupling dipole: UNDEFINED | A4: D = 1.1e-3 at c2 = 7.3e-3 (control reproduced); the moving-source solve with the added coupling was not derived; edge shift from CV4's K3 number only |
| AeST v9 PPN kill | NOT APPLICABLE / not tested | different action; A4's G6 uses V0's KM3 formulas (PASS for d1; d2's coupling part UNDEFINED) |
| single-metric slip-lock / elliptic pincer | escaped by inheritance, not tested | V0 keeps the khronon; O3a gives Phi = u + fP (baryons and light feel the same Phi); the gate's slip was not computed |
| **V0 region-gate obstruction** | **NOT ESCAPED** | A3: d1 MOVED (blind), d2 STILL PRESENT in 96/96 cells x 4 variants; the pincer -c_s^2/c^2 = 3 c2 Delta^2 eps_L/eps_b reproduced by the script to 0.3% |
| DE12 / DE13 | DE12: reproduced exactly (C4) and, with the replacement, the negative stiffness moves onto the baryons through the coupling (d2) or disappears because the gate is off (d1); DE13: no repair used, its K0 term not computed | A3 |
| DE7 T1 (a flat-flat gate has f'' of both signs) | confirmed | A1 C7; O3c's theta-theta entry carries B f'' |
| CV4 (K-only gate blind) | d1: blind on the continuation branch; the alternative branch is selective only at high acceleration; d2: not blind, unstable | A3, A2 |

## Wrong expectations (kept; nothing repaired)

1. Frozen 3.3: d2 O2 "P 0.85". **Wrong for the frozen variant.** u_theta = D E^-2 is even in theta, so at high density (theta -> large negative) the gate turns OFF again: the frozen d2 gate is a density band-pass shell, and it is OFF at the Sun and in the galaxy centre. The frozen text noted the pole at theta = 0 but missed y -> -infinity. The monotone variant was added as a sensitivity.
2. Frozen 3.1: "bump ~3e-6 (z = 0.25) / 2e-3 (z = 4) if the gate sits at its edge". **Wrong in the inner layers**: up to 4.3e-2 (median 6e-5) when theta is placed at a layer where B = 2 a0^2 q/c^4 is large. T-d1 ("cannot be a region gate") holds for the continuation branch only; the local equation has alternative S-curve roots in 93/96 cells, and the upper branch is a bubble ON at high acceleration. Frozen O1 "d1 P 0.55" held for the wrong reason.
3. H-i "no O(pi) source" (frozen 1.3): true only when static; an O(H) source exists (<= 5e-4 of the needed depletion).
4. Frozen 3.2 hand numbers used eps_b/eps_L = 0.14-14 at the edge and gave |c_s| >= 8e3 km/s and zeta_min ~ 1e-3-0.1. The layer sits at eps_b/eps_L ~ 10^3, so zeta_min = 1.8e-5 and |c_s| at zeta_min ~ 1.1e3 km/s at the reference cell (the formula itself is right to 0.3%). The zeta_min/zeta_max ratio is >= 1.8e3, not the hand >= 30. The conclusion (unstable by a factor 30-500 above the 37-117 km/s gas lines, 5e3 at the median) is unchanged.
5. Frozen 3.3 "P(REMOVED) ~ 0.04": no arm was REMOVED (except the unit-error artefact of the first run, retracted above).
6. M4's G7 side and M5 did not bite as predicted (table above).
7. A hand expectation that V0's B ~ 2 a0^2 q/c^4 was confirmed (0.94-1.07), i.e. DE7's "~10%" holds in this lane's solution.

## Departures from the frozen criteria (disclosed)

1. Two SENSITIVITY constructions were added after seeing failures: the monotone gate and the d1 upper (S-curve) branch, plus an added "reach" test (gate ON to 30 r_M). They are labelled and never pooled with the frozen arms.
2. B in the zeta scan comes from V0's static solution with the prescribed original gate (frozen B, as DE12); in A2 it comes from the self-consistent solution.
3. O1 is the local principal-symbol c_eff (the contact operator is gradient-free, so DE13's half-layer LDL^T count reduces to the local sign); the discretised global-operator eigenvalue count (CV3 G3b) and low-k Schur corrections were not done. DE12's frozen-B approximation (B independent of rho) is kept.
4. Cosmology: L352's constants (Omega_m = 0.3138) via the DE12 construction, not the frozen 0.3153 of the hand table (a 0.5% effect).
5. G1: z = 0 and 0.25, w = 0.25, c2 = 7.3e-3, 1/m = 100 kpc, sigma = 1; background contrast neglected in the w and P solves; the region kernel is sourced by the galaxy only while the theta source includes DE12's gas (generous to d2). The 1/m = 500 kpc variant and the sigma = 0 layer were not run.
6. G7 and G6 use the record's KM1/KM3/CV4 numbers as inputs (not re-derived); G5's filtered remainder, the Milky-Way tide and criterion B are NOT ADDRESSED.
7. Controls not reproduced: C6 (DE1's closed-form edge; 0.873 against this lane's gas-inclusive edge, not the same object), the CFG7 H1 Q2 recipe (C5 of CFG172), and CV1 A5's sigma-layer numbers (1.4 and 0.8 g_N; configuration not specified). Kept as failed/omitted controls.
8. p = 2, x_c0 = 2 and the z-independent gate (u_theta = D) sensitivities, and the simple-kernel and P2-in-q variants, were not run.

## Hypotheses NOT tested

FC-KH's radial coefficient with the gate; KM1's moving-source solve for the d2 coupling and for the gate edge (record inputs only); criterion B causality / characteristic cones of the theta sector; alpha_1, alpha_2 with the d2 coupling; a nonlocal or heat-filtered gate (a new length), a dynamical gate field (CV6), any gradient repair (DE13's K0); the spin-1 (twist) mode, c1_3 != 0; non-spherical baryons; the sigma = 0 hard-edge layer and edge-sensitive lensing; the time-dependent quasi-static assumption for the fields inside H-i (E-L[REST] was evaluated with the fields static in comoving r); lensing slip of the gate; CDM-phantom double counting; CMB (UNDEFINED); the "no-cold" run (cited to CFG172 A8); everything outside the weak-field static limit. The literature values (Liu+2020 and the other PPN limits, Skordis-Zlosnik and related) are from memory or as the record cites them, unverified.

## In-place re-run (orchestrator)

`bash run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`). Exit codes: the five main runs and the verdict script 0; MUTATE M6, M7 (A1), M1-M4 (A3), M2, M3 (A2) and M8 (A5) exit 1 (bite); MUTATE M5 (A3) and M4 (A4) exit 0 (do not bite, as the referee reported). Compared with the agent's outputs: (i) every printed verdict, gate cell and headline number is identical; (ii) timing lines differ; (iii) three `A2` results files differ at the 1e-16 relative level (floating-point ordering); (iv) `CFG172D_A1_rest_expr.txt` (a serialised sympy expression) differs in length by six characters, sympy term ordering, not a different expression; (v) the agent's `MUTATE M4` output of script A4 read an EMPTY `zeta_min_reference` from A3 (that run happened before A3's results existed), while the re-run read A3's values, so that one output differs in its inputs and is the re-run's version here; (vi) the agent's MUTATE outputs carry a trailing 'control BITES / DOES NOT BITE' line that the re-run's do not, because the agent's line came from its own wrapper, the exit code being the record here. The agent's working logs and probe scripts are not lane files and are not included. The frozen criteria are `../CFG172D_FROZEN_CRITERIA.md` (b7c979e15).

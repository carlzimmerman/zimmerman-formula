# CQ7_lstar_dwarf_window: FROZEN CRITERIA (committed alone, before any script or number)

κ = ½ FITTED; not theory closed. Footings (canonical a0 9.3603e-11, alt 1.1312e-10) are never pooled. No particle, no cold sector, no ΛCDM input. Nothing here says the data favour the framework.

## Question
CQ1 found a fixed screening length L★ window [21.7, 27.0] pc (canonical), [22.9, 24.6] pc (alt). The top edge is UGC 4483 under the reading "screening radius ≤ 0.1 r_M". CQ7 replaces that reading with v3s's own static solve for the smallest dwarfs and asks whether the window is open.

## The theory solved (v3s statics)
v3s = v3 with the switched stiffness; V3_FULL_PICTURE §4.7 / X3: statics unchanged wherever D·P ≥ 0, and the record's screened static solves are the C4-literal grad-div form (C6, D10):
(L) ∇²Φ = Kρ + ∇·p, (P_L) ∇Φ + (L★²/2)∇(∇·p) = a0 p/(a0 − |p|); p = v/(1+|v|), v = ∇χ, χ = Φ + (L★²/2)∇·p.
- **Embedded dSphs:** D10's `Solver2D` (2D axisymmetric, Newton, exact Jacobian), imported read-only from `doors_push_2026_10_22/D10_native_Lstar/d10_solver.py`, grid `Grid2D(nper=24, Nt=16)` as D10. Plummer a = r_h. Uniform host field: background v_e = law_v(g_N,e/a0) with g_N,e = G M_MW/D², M_MW = 7e10 M☉ for MW satellites (CZ2/CZ5's E1 Newtonian host field, inverted through the law), isolated (`isolated=True`) otherwise. σ = luminosity-weighted global σ (D10's virial output of `jeans`); this estimator is a frozen reading.
- **Isolated rotation curves (SPARC, LITTLE THINGS):** the radial ODE of D10's `iso_1d`, (L★²/2)(p'' + 2p'/r − 2p/r²) = p²/(1−p) − g_N(r) in a0 units, solved with `solve_bvp` on the tabulated monopole g_N(r) = V_bar²/r (spherical reading, as KT19), linear inside the first point and Keplerian beyond the last; p'(0)-regular inner condition and the law at r_out = 30 × R_last. g_pred = g_N + p.
- The switch: X3 showed D·P ≥ 0 inside the solves that matter; CQ7 does not re-solve the switch. Where a dSph's 2D solve has a D·P < 0 cell, its count is reported (reading only).

## Gates and the record's tolerance for each
- **G-dSph (CZ5 T2):** 24 McConnachie dwarfs, CZ5's selection (σ* error present, M_V ≤ −8, not M32/NGC/Sagittarius). M = Υ L_V + 1.33 M_HI. A dwarf passes if some Υ in [1, 3] gives |σ − σ_obs| ≤ 2 e (Υ grid 1, 1.4, …, 3.0, then cubic in ln Υ on a 201-point grid). **Line: ≥ 15/24.** Gate dwarfs (r_h < 10 L★) are listed; all 24 are solved and counted.
- **G-RC (KT19's lines applied per galaxy):** SPARC (KT19 loader: L[3.6] Υ 0.5 disc / 0.7 bulge, 1.33 M_HI, e_V/V < 0.1) and LITTLE THINGS (p47's loader, V_bar² = V_tot² − V_DM²). Gate galaxies: min(r_M, 1.68 R_d) < 10 L★ for SPARC (r_M = √(G M_b/a0)), r_M < 10 L★ for LITTLE THINGS (M_b from V_bar² R at the last point). Against the same galaxy at L★ = 0: **FAILS** if rms of log10(g_obs/g_pred) rises by > 0.02 dex or the median shifts by > 0.05 dex; HURT 0.005–0.02; else SURVIVES. HURT is not a fail. UGC 4483 is always a gate galaxy.
- **Lower edge (globulars, D10 floor 21.68 / 22.85 pc):** carried as is.

## L★ grid
Graded: the CQ1 window's low edge, midpoint and top edge per footing (21.68 / 24.34 / 27.0 canonical; 22.85 / 23.73 / 24.6 alt). Beside (information, no label): 40, 60, 90 pc. If a graded point fails, the binding gate is bisected between the last pass and the first fail to 0.1 pc.

## Labels (per footing)
- **WINDOW OPEN [lo, hi]**: every graded L★ from lo upward that passes both gates; lo = D10 floor; hi = the CQ1 top edge if all three pass (the beside points say how far it could extend, with CQ1's MW H2 90 pc bound carried), else the bisected edge.
- **WINDOW CLOSED**: the gates fail at the D10 floor itself.
- The binding dwarf is the first dSph or galaxy to fail as L★ rises (across graded and beside points).

## Checks (K) — any FAIL → exit 1, reported, label stands with the failure disclosed
- **K1 (known answer, CQ1 UGC 4483):** the SPARC loader gives UGC 4483 smallest M_b 4.91e7 M☉, r_M 270 / 246 pc, 0.1 r_M = 27.0 / 24.6 pc (rel ≤ 1e-3 against cq1.json).
- **K2 (known answer, C6's Sun):** CQ2's copy of C6's Route F kernel reproduces C6's 24 recorded wide-binary γ − 1 numbers (rel ≤ 1e-6), as in CQ2's K1.
- **K3:** isolated 2D at L★ = 0 equals the algebraic law's σ (rel ≤ 2e-3, D10's K3 line).
- **K4:** the 1D RC solve at L★ → 0 (1e-3 pc) equals the algebraic law at every point (rel ≤ 1e-3).
- **K5:** peak RSS < 1 GB; one thread; `nice -n 10`.
- **MUTATE twin (`--mutate`): no screening, L★ ≡ 0 in every solve.** It must give zero change at every L★ (all rms shifts 0) and the dSph count at L★ = 0; it exits 1 by design.

## Inputs
a0 footings and κ = ½ FITTED (record); McConnachie 2012 csv (RAW + SURVEY-CALIBRATION); SPARC Lelli 2016 (RAW + SURVEY-CALIBRATION); LITTLE THINGS Oh+2015 local copy (RAW, owner-approved 2026-10-05); D10 floor (record). No downloads.

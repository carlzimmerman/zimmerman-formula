# CFG354: a turnaround switch on the tidal eigenvalues of the leaf overdensity potential

Criteria: `FROZEN_CRITERIA.md` (commit bd5ab6223, committed alone before any script). kappa = 1/2 fixed (fitted);
nu_mono; no DM particle (the cold MASS is still required). Owner decision 2026-10-06: the switch may read the cold
component. **Under the original MS1 this reader is NOT ADMISSIBLE.**

**Verdict (frozen primary T3): NO-GO.** T3 fails (c) and (d).

**Best reported rule, T1 (not substituted): PARTIAL, with cost n = 1.** It fails (a') by a theorem: a dense filament
looks the same to it as a host edge. It needs a switch-width constant to be well-posed. This is a scoped result,
not a closure.

## Rules (psi = Phi_d/(4 pi G rho_bar), t = Hessian psi, tau = (Delta_ta - 1)/3)
- **T1:** l2 >= tau. For every sphere l2 = l_t exactly, so the isolated-host edge is exactly r_ta.
- **T2:** l3 >= tau.
- **T3 (primary):** min over e ⊥ grad psi of e.t.e >= tau. It equals l_t on spheres and is exactly 0 in infinite
  cylinders and planes.
- No function of the eigenvalues alone can do T3's job (Lean S7). A sphere with delta = 2 dbar/3 has the same
  triple (c, c, 0) as a filament interior.
- Ordering: l3 <= T3 <= l2.

## Legality and well-posedness
- L1-L4 pass: sympy Euler-Lagrange; leaf scalars; adjoint vs finite difference 2.4e-8; Noether 2.4e-16.
- t = d d lap^-1 delta is order 0 (symbol |k_i k_j/k^2| <= 1). There are no time derivatives, so no momenta and no
  Ostrogradsky degree of freedom.
- **New cost relative to CFG353:**
  - Because the reader is order 0, a sharp H puts a surface-DELTA layer into the matter potential, with coefficient
    c_d = n_s.P.n_s.
  - On a spherical edge the tangential readers (T1, T3) have c_d = 0, which leaves a finite jump. The sup stays at
    1.00 for widths w = 0.05 to 0.005.
  - The radial reader (T2) grows as 1/w (7.1 to 78.8), and so does the 1D leaf (x29.8 for w/33). The identity
    d_i d_j(F n n) = (r^2 F)''/r^2 is sympy-exact.
  - With the LSS tide the edge is not spherical, so c_d is nonzero and the sharp switch is ill-posed. Median c_d per
    host: T1 1.1e-4 to 7.7e-3 (max 0.11); T3 0.04 to 0.84.
  - A width constant fixes this. The needed eps_min is 0.077 for T1 (edge smearing <= 1.6% r_ta) and 1.48 for T3
    (30% r_ta).

## Results
**(a) linear: PASS (all rules).**
- ON = 0 in 4e6 samples at R = 8/20/50 h^-1 Mpc and every z. The chi2 bound is <= 1.1e-77.
- Unsmoothed (k <= 50 Mpc^-1) at z = 1000: sigma 9.1e-3, ON 0.
- Reported, unsmoothed: z = 10, sigma 0.83, ON 0 (bound 2.5e-3); z = 3, T1/T2/T3 3.3e-2/6.1e-4/6.1e-3; z = 0,
  8.4e-2/2.8e-3/1.9e-2. These scales are nonlinear: P(delta_lin >= 1.062) is 0.32 at z = 3 and 0.44 at z = 0, so
  the ON regions are real collapse, not false positives. No smoothing constant is needed for the scored test.

**(a') filaments and sheets (EdS threshold scored):**

| cell | T1 | T2 | T3 |
|---|---|---|---|
| planes delta_w 0.5-3 | 0 | 0 | 0 |
| cylinders delta_f 1, 2 | 0 (max R/tau 0.33, 0.66) | 0 | 0 |
| cylinder delta_f 5 (x5 / x10) | 0.040 / 0.010 (R/tau 1.65) | 0 | 0 |
| cylinder delta_f 10 (x3 / x5 / x10) | 0.111 / 0.040 / 0.010 (R/tau 3.30) | 0 | 0 |

- T1 fires inside every filament with delta_f >= 2 tau = 3.03 (EdS) or 7.20 (z = 0). It FAILS.
- Lean S8: any rule monotone in the eigenvalues that is ON at a host edge (tau, tau, l_r < 0) also fires in such
  filaments.
- Reported, finite uniform ellipsoids:
  - Prolate (aspect 5/10, delta 5/10): T1 ON in the whole volume; T3 ON in 5-32% of the volume, along the axis near
    the tips. T3's zero in filaments needs exact translation invariance.
  - Oblate: all rules OFF.

**(b) hosts (24):**
- T1 and T3: P(ON at 30 kpc) = 1.00 on 24/24.
- Fidelity: a 10% gas compression moves ln m by at most 0.06, against a ln margin of at least 4.2. PASS.
- T2: OFF everywhere. The NFW and isothermal outskirts have l_r < 0. FAIL.
- External field at r_ta:
  - |t_ext|/tau = 0.02-0.15: tides are small.
  - g_ext/g_host = 0.42-6.8: the LSS gradient is NOT small.

**(c) edge:**
- T1: median edge 0.954-0.993 r_ta, offset at most 44 kpc, 24/24. The isolated sphere edge is 0.9998 (grid). The
  edge part passes; well-posedness fails without a width.
- T3: median edge 0.31-0.94 r_ta, 6/24 within 100 kpc (only the z = 4 hosts). FAIL. T3 is not invariant under
  psi -> psi + b.x. The bulk LSS gradient tilts the projection plane, so it picks up the negative radial eigenvalue.
- T2: no edge (0/24).

**(d) data (CFG352 harness, scoring unchanged; KiDS lens-bin median edges):**

| row | edge | KiDS d chi2 (can / alt) | SPARC | growth |
|---|---|---|---|---|
| control | 1.0 | -9.18 / -9.30 | pass | pass |
| T1 min / max | 0.963 / 0.979 | -10.48 / -11.15; -9.78 / -10.40 | pass | pass |
| T3 min / max | 0.362 / 0.687 | **+66.97 / +63.53 FAIL**; -18.23 / -17.65 | pass | pass |
| T2 | 0 (1e-3) | **+1068 / +1076 FAIL** | **FAIL** | pass |

## Tally
- **T3 (primary):** L pass, a pass, a' pass, b pass; **c FAIL** (edge 6/24, c_d != 0); **d FAIL**. **NO-GO.** The
  obstruction is gradient dependence: T3 reads grad psi, and the external bulk gradient is O(1-7) times the host's
  own field at r_ta.
- **T1:** L, a, b and d pass; (c) passes only with the width eps (n = 1); **a' FAIL** (theorem). **PARTIAL (n = 1).**
  The (d) score uses the sharp edges. A 1.6% smearing is well inside the KiDS margin, but the smeared harness was not
  run.
- **T2:** b, c and d fail. **NO-GO.**
- Constants: Delta_ta derived; 0 fitted. T1 needs 1 (width) for well-posedness. The 2 r_L LSS smoothing models the
  environment.

## Controls
- K1 point mass and uniform sphere: T1 = T3 = l_t = (4 pi G/3) rho_enc to 4e-16.
- K2 cylinder and plane: analytic to 2e-16; FD Hessian 1.2e-8.
- K3 FRW OFF.
- K4 Delta_ta 11.806 / 8.893 = CFG4.
- MUTATE (CFG354_MUTATE=1, potential reader = CFG353 E0) reproduces CFG353 exactly: (a) 1.739251e-2; the (a') cells
  are identical; rc 1.

## Lean
`CFG354_tidal_certificates.lean`: 15 theorems, no sorry, standard axioms only, rc 0 (`.out`). They cover:
- sphere g/r = GM/r^3 = (4 pi G/3) rho_enc, and the trace;
- middle-of-three = l_t for every sphere;
- cylinder inside/outside and plane responses;
- the eigenvalue-only T3 no-go;
- the monotone-rule filament no-go;
- 2(9 pi^2/16 - 1)/3 > 3;
- FRW off;
- the Frobenius bound;
- the layer sup >= A/w and its unboundedness;
- c_d = 0 iff n ⊥ e;
- the spherical tangential c_d = 0 vs radial 1.

## Run
```
python3 campaign_fresh_gravity/CFG354_tidal_turnaround_switch/cfg354_tidal_switch.py > campaign_fresh_gravity/CFG354_tidal_turnaround_switch/cfg354_tidal_switch.out   # rc 0, ~25 s
CFG354_MUTATE=1 python3 campaign_fresh_gravity/CFG354_tidal_turnaround_switch/cfg354_tidal_switch.py > campaign_fresh_gravity/CFG354_tidal_turnaround_switch/cfg354_tidal_switch_MUTATE.out   # rc 1 (detected)
python3 campaign_fresh_gravity/CFG354_tidal_turnaround_switch/cfg354_edge_harness.py > campaign_fresh_gravity/CFG354_tidal_turnaround_switch/cfg354_edge_harness.out 2>/dev/null   # after the main script
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG354_tidal_turnaround_switch/CFG354_tidal_certificates.lean
```

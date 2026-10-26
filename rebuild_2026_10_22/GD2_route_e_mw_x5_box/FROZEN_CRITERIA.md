# GD2_route_e_mw_x5_box — FROZEN CRITERIA (committed alone, before any graded number)

κ = ½ FITTED. Footings canonical / alt computed and graded separately, never pooled. Cold dark energy, not matter. No
dark-matter particle. Nothing here says the data favour the framework or ΛCDM. Not "theory closed". One thread, nice 15,
RSS < 1 GB (X48 runs are live).

## Question (owner, 2026-10-26)

GD1 A1 found that the flagship misses V_c(R₀) on McMillan 2017 baryons: OS1 core law, z −6.2 to −4.0. GD1b and IJ1 found no
native core rule that lifts the halo's pull. The open lever is the baryons. **Does any baryon model in X5's frozen
published-prior box let the flagship pass V_c(R₀), K_z and the Ou+24 curve together?** The short-disc corner
(R_d ≤ 2.27 kpc) is the one X5 found the law needs.

## Theory graded (no free number)

- **Route E.** Gravity is Newtonian. The halo is OS1's Burkert with ρ₀r₀ = Σ = Σ_a₀ (σ/σ_ref)^q_f:
  - Σ_a₀ = 106.879 / 129.165 M☉ pc⁻² (X38);
  - σ_ref = 70.50 km/s;
  - q_f = 0.892 / 0.748 (OS1, SPARC only);
  - σ = V_last/√2 (SC1's definition).
- **PRIMARY:** V_last = 172.98 km/s (Ou+24's last point, the literal definition). **VARIANT:** V_last = 229.05 km/s
  (= V_c(R₀)). The variant gets its own graded row; the two are never pooled.
- M200 = 10^(a + b(lg M_b − 10)) from EM1's committed R1 relation. Background A (a 11.18, b 0.9, h 0.6758) is PRIMARY;
  background B is reported only. M_b is the cell's total baryon mass on the solver grid. R200 uses that background's h.
  r₀ is X38's A1 compact root; a saturated halo is counted.

## Baryons

- X5's frozen family and grid, unchanged (`x5_lib.Family`, 5 Σ_b × 5 M_bb × 7 R_d = 175 cells).
- X5's Licquia & Newman tags are carried: tag_Mstar_IN, tag_Rd_IN.
- The Newtonian field comes from P4's `Problem.solve_newton` on P4's `mw_grid`, with P4's `rho_axisym` quadrature (nq 4).
- The halo field is added analytically. In-plane: R g_h(R). Vertically: g_h(r) z/r at r = √(R² + z²).

## Observables per cell (P4 / X5 / S3 conventions)

- V_c(R₀ = 8.122 kpc), in-plane.
- K_z(R, 1.1)/2πG at Bovy & Rix's 43 MAP radii (BR_R, shifted to R₀ as P4). χ²_Kz uses BR_E5 = BR_E ⊕ 5 %.
- K_z(R₀, 1.1)/2πG.
- χ²_Ou over Ou+24's 37 points with S3's error model: random ⊕ 3 % to 22 kpc, ⊕ 15 % beyond.

## Lines (frozen; each cell, each footing)

- **L1 V_c(R₀):** X5's `cell_pass` V part, |v_c − 229.1| ≤ 9.2 AND |v_c − v_E| ≤ 2e_E, with v_E, e_E from X5's
  `eilers_target`.
- **L2a K_z MAPs:** χ²_Kz ≤ 67.459 (99 %, 43 MAPs; X5's line).
- **L2b K_z summary:** |K_z(R₀) − 66.4| ≤ 2 × 2.2 (Bovy & Rix, X5's summary target).
- **L3 Ou+24:** χ²_Ou ≤ 59.893 (99 %, 37 points; no fitted parameter).
- Distance D = max(χ²_Kz/67.459, |v_c − v_E|/(2e_E), χ²_Ou/59.893, |K_z(R₀) − 66.4|/4.4). The best cell is the one with
  minimum D.

## Class per footing (PRIMARY: V_last 172.98, background A), first match wins

1. **FEASIBLE IN PRIORS:** at least one cell passes L1, L2a, L2b and L3 with tag_Rd_IN and tag_Mstar_IN both true.
2. **FEASIBLE (WIDE PRIORS ONLY):** at least one cell passes all four lines, but none with both tags true.
3. **V+K ONLY:** at least one cell passes L1, L2a and L2b, but none passes L3.
4. **INFEASIBLE:** no cell passes L1, L2a and L2b together.

Lane verdict: the class on each footing, printed separately. The VARIANT gets the same rules on its own row, reported
beside PRIMARY, never replacing it. Background B is reported only.

## Checks (all must pass in the normal run)

- **K0:** McMillan 2017 (P4 `rho_mcm`) on this Newtonian path reproduces GD1/S3's baryon-only V_b(R₀) = 177.234 km/s and
  K_z,b(R₀, 1.1)/2πG = 62.024 M☉ pc⁻², each within 1 %.
- **K1:** the cell masses agree with X5's analytic masses (|rel err| < 2e-3), as in X5.
- **K2:** the OS1 Σ factor equals GD1 A1's 1.635 / 1.510 (PRIMARY) and 2.100 / 1.863 (VARIANT) to 1e-3.
- **K3:** the halo raises both v_c and K_z(R₀) in every cell.
- **K4:** peak RSS < 1 GB.
- **MUTATE (`--mutate`):** q = 0 (X38 core). K2 must FAIL (exit 1). Outputs go to `*_MUTATE` files.

## Not done here

No refit of q, of the M200 relation or of any baryon parameter. No grid refinement after results. No AQUAL. No EFE (route
E has none).

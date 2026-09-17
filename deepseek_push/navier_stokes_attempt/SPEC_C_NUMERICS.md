# SPEC_C — equilibrium numerics lane N04b (subagent task)

Write a self-contained evidence lane
`/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/navier_stokes_attempt/N04b_equilibrium.py`
(+ `.out`, `_results.json`, PNG `N04b_equilibrium.png`) — a LARGER and LONGER
3D periodic Galerkin run of the ZNS family, run to viscous equilibrium.

## The system (identical to N04's, spectral Galerkin on [0,2π)³)
    u_t + (u·∇)u = −∇p + νΔu − c_d·|u|·u + f,  div u = 0
Cases: classical (c_d = 0), a0-capped dry drag (|d| ≤ 0.02, N2 class), strong
drag (c_d = 0.3). Forcing f = A·s with sup|s| = 1 done in modes |k| small
(see N04_galerkin.py in the SAME folder for the reference integrator — import
NOTHING from it; copy the working machinery, ADD the 2/3-dealiasing mask which
N04 already has: mask |k| ≤ (2/3)(n/2)).

## Run parameters (motivated: reach equilibrium; N04's T=6 was spin-up only)
n = 32, nu = 2e-2, dt = 2e-3, T = 40, A = 1.0, seed = 7. Dealiased 2/3-rule.
(RK4; record sup‖u‖∞, enstrophy Σ|k|²|û|²/N³, energy, every 25 steps.)
If the run is too slow (>10 min/run), drop T to 30 or dt to 4e-3 (report what
you used). Three runs max; if time is tight, drop the a0cap case LAST.

## Checks (PASS/FAIL prints, JSON results)
- G25 EQUILIBRIUM REACHED per case: last-quarter mean enstrophy within 15% of
  the previous-quarter mean (the spin-up ends; this is the honest analog of N04's
  FAILED gate — the reason is documented in the N04 .out).
- G26 SUPPRESSION ORDERS: sup peaks satisfy classical > a0cap ≥ cd003 > cd03
  (the drag ladder lowers the sup monotonically; the a0-cap class is close to
  classical — its sub-regularizing character).
- G27 THE TRAJECTORY INEQUALITY (window-theorem verification): from stored
  snapshots (every 25 steps) of the CLASSICAL run, compute at each sampled
  grid point the finite-difference material acceleration
  a_mat ≈ (u(t+δ) − u(t))/δ + (u·∇)u(t)  (δ = 25·dt = 0.05)
  and verify pointwise | |u(t+δ)| − |u(t)| | ≤ δ·max|a_mat| + tol on the grid
  (tol = 1e-9·scale) — HOLDING = the elementary inequality behind the window
  theorem is consistent with the discrete dynamics (EVIDENCE ONLY, not a proof).
- G28 THE WINDOW DIAGNOSTIC: report η_flow(t) = ‖(u·∇)u + νΔu‖∞/a0_sim for the
  classical run with a0_sim = 0.02 (as in N04), plus the first-exit time of the
  level η = 3.5 (report 'no exit' if never): the window-exit diagnostic.
- G29 ENERGY CONSERVATION SANITY: with c_d = 0 the energy equation reads
  dE/dt = −2νD + ⟨f,u⟩; verify the discrete identity over the run to ≤ 1%
  (Euler-forward check of E(t+δ) vs E(t) + δ·(−2νZ + ⟨f,u⟩)). This guards the
  integrator itself — a failing integrator would invalidate ALL lanes.

PNG: one figure, 2x2 (sup, energy, enstrophy, eta) with the 3 cases, titled,
gridded, saved at 120 dpi.

## House rules
- EVIDENCE ONLY: the file header and the JSON must say simulations are not proofs.
- Files land ONLY in the navier_stokes_attempt folder. No git. No absolute paths.
  python3 = /opt/homebrew/Caskroom/miniconda/base/bin/python3.
- End: `<N04b_equilibrium> COMPLETE: N/M checks PASS.`
- Report back: per-case timings, the check table, the PNG path, any parameter
  you had to change and why.
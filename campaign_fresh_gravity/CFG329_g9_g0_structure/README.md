# CFG329: recipe gates G9 and G0 on the chassis

The chassis is the filtered C-H/K completion: C-H plus alpha_c a^2 - c_2 (K - <K>_Sigma)^2, with beta = 0, nu_mono and
heat-filter scale xi. The criteria were frozen first (`FROZEN_CRITERIA.md`, commit 50c09b024). The script is
`cfg329_g9_g0.py`. It gives 16/16 checks (rc 0). The MUTATE run gives rc 1 (see below).

**G9 = PASS.**
- Matter couples to g only. The off-shell matter identity is nabla T = E_chi d chi + E_U d U, with residuals of 1e-47.
- In a curved plane-symmetric reduced sector, every chassis term is a scalar density under arbitrary diffeomorphisms
  (Noether II residual 9e-47). This covers R, 2|DU - a|^2, the q kernel, one heat z-slice L(W_z - Delta_h W),
  lambda_0(W - U), alpha_c a^2, and -c_2 (K - F(tau))^2 (the leaf-average proxy). So the generalized Bianchi identity
  holds off shell. On the tau, U, W, L, lambda_0 shell, nabla_mu T^mu_nu = 0 follows exactly, and the clock equation
  is implied.
- At linear order, in the FP2 block, the clock equation is the metric-equation combination plus (d_t rho_s - j_s).
- The extra term is **0** on the solar-system, galaxy and cosmology backgrounds. The leaf average's global stress is
  conserved and carries local weight V_sys/V_leaf: 1e-36 (solar), 3e-16 (galaxy), 0 for k != 0.
- Diagnostics for implementations that are not covariant (these are not the action):
  - Dropping delta S: at most about 6e-11 of the force balance (galaxy).
  - <K> frozen as a coordinate-time function: extra term -2 c_2 sqrt(-g)(K - Kbar) Kbar' xi^t, matched to 5e-41. It
    costs 3 c_2 (1+q0) = 1e-2..9e-2 per Hubble time on FRW. So <K> must be varied as a function of tau.

**G0 = CONDITIONAL.**
- No cross-order cancellation. The kernel q ~ (4/3) s^(3/2), which is eps^(3/2) in deep MOND. delta S is linear in
  psi, so it enters at eps x kernel (1PN). K = 0 on static slices.
- The nonlinear unitary-gauge Lagrangian has no second time derivatives. It has no d_t of N, N^i, U, W, W_z, L or
  lambda_0, so only gamma_ij carries a momentum. The filter's K n(W) term cancels d_t W exactly.
- det M(omega, k) has omega-degree 2: one scalar mode and no Ostrogradsky pair. The filter is omega-independent. The
  leaf average acts only at k = 0.
- The momentum constraint is preserved, through the spatial Noether identity. The lapse/U equations are elliptic,
  with lapse coefficient (2C + alpha_c(1+C))/(1+C) > 0. A frame tilted against the foliation shows the instantaneous
  mode (a 4th-order clock equation), not a propagating ghost.
- CONDITIONAL, by the frozen rule, because nonlinear solvability of the elliptic, leaf-non-local lapse/U/W/L system is
  not proved. FP5's zero-field Hadamard failure is a G4/G5 issue and is not re-run here.

**Controls.** All behave as required:
- GR Bianchi identity: 1e-46. FRW dust is conserved iff rho a^3 = const.
- Plain khronometric theory: residual 4e-47.
- The coordinate-time (d_t U)^2 term is caught: 0.68.
- MUTATE (`CFG329_MUTATE=1`, matter x e^{beta U}): G9 flags it. See `cfg329_g9_g0_MUTATE.out`.

**Scope.** The Noether test runs in a reduced (t, x) sector with one z-slice and an N-weighted proxy for <K>. It is
not a general 4D proof. kappa = 1/2 is FITTED and plays no role here.

Run from the repository root (about 8 min each, single process):

    python3 campaign_fresh_gravity/CFG329_g9_g0_structure/cfg329_g9_g0.py
    CFG329_MUTATE=1 python3 campaign_fresh_gravity/CFG329_g9_g0_structure/cfg329_g9_g0.py

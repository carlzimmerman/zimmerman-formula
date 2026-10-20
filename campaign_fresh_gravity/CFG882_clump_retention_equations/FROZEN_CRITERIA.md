# CFG882 FROZEN CRITERIA: clump retention in the cold-energy equations

Date: 2026-10-19. Written and committed ALONE, before any CFG882 script exists and before any CFG882 run. Nothing below may be
edited after this commit; later changes go in dated disclosures in the README.

κ = ½ is FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) are judged separately and never pooled. Law
g = g_N ν_e(g_N/a0), ν_e(y) = 1/(1 − e^(−√y)). Cold energy is real gravitating mass; no particle species. Framework-native
inputs only. Not "theory closed". Nothing here says the data favour the framework. No constant is added; no knob is scanned.

## 0. Question and what has been seen

**Question.** Can the record's cold-energy equations keep CFG877's finite clump (extra cold mass over the law's phantom, i.e.
overfill) in a dwarf for a Hubble time, while big galaxies stay on the law? Derived from the stated equations; nothing posited.

Seen before freezing: CFG638 (fluid form, K6/K7), CFG639 (gate HG; Part A NOT DIAGNOSTIC, IC-C not steady; Part B VG-1
UNDETERMINED), CFG641, CFG623 (mergers allow α = 0; galaxy side wants α ≳ 0.5), CFG541 (E1–E9; t90 ∝ 1/α, α·t90 = 8.0–10.0 Gyr
over its MW/group/cluster cells), CFG544 (FIX-1, FIX-2, overfill P = 0.30–0.43 at 5 Gyr under FIX-2), CFG554/558, CFG870–872,
CFG876, CFG877 (clump: V_x 10.655 / 10.587 km/s, M_cl 5.25e6 / 4.24e6 M_⊙, r_c 104 pc, cap r_t 199 / 163 pc), CFG878, and
CFG881's result (SPARC bound F_max: CORE1 0.27, CORE3 0.92, BARYON 2.1, FLAT 3.2, canonical medians).

**Pre-freeze hand values (disclosed, not verdict inputs).** Clump central density ρ_x0 = 3V_x²/(4πG r_c²) ≈ 0.58 M_⊙/pc³,
τ(ρ_x0) ≈ 5.5 Myr. Cold-dominated uniform core under the two-sided drift: ρ(t) = ρ0/(1 + αt/2τ0)², hence a central bound
α ≲ 9e-4 (target ρ_x0) or ≈ 1.3e-3 (target ρ_x0/2) for 12 Gyr. Expected α_50 at r_t of a few × 1e-3. Gated, smooth halo:
retention exact by construction. Expected under noise: deficits next to a net overfill are anti-restoring.

## 1. Equations (the record's, unchanged)

- Drift v_s = −α 1_B 1_C τ ∇ψ, τ = (4πG ρ_m)^(−1/2), ρ_m = ρ_b + ρ_c, two-sided deficit ∇²ψ = 4πG(ρ_ph − ρ_c) on B∩C (CFG544
  FIX-1, as written in CFG638). ρ_ph is the round-rule phantom of the host's own baryons (CFG541 E7) with ν_e.
- **Gated variant (CFG639 HG, unchanged):** G = 1 iff d = ρ_ph − ρ_c > 0, else 0, multiplying the drift and the OU rate at each
  cold element's position; ψ, ρ_ph, τ, the OU target unchanged.
- **Density sub-flow.** The test evolves ρ_c under ∂_t ρ_c + ∇·(ρ_c v_s) = 0, spherical, static baryons and static ρ_ph,
  1_B 1_C = 1 inside R_out = 20 kpc, zero flux at R_out. Justification (to be stated in the README, checked by K7): under FIX-2
  the OU target is the Jeans (hydrostatic) dispersion of the current density, and no stationary counter-flow u = −v_s exists in
  CFG638's moment system when overfill is present. The drift-only density evolution is therefore the record's to O(1). No
  kinetic run is made; this is a stated limit, and the verdict margins (§4) are set so an O(1) correction cannot flip V1.

## 2. Inputs (fixed now)

- Clump per footing, read from `CFG877_finite_cold_clump/cfg877_results.json` (read-only): V_x, M_cl, r_t; r_c = 104 pc.
  Cumulative clump mass M_x(<r) = min(V_x² r³/(G(r² + r_c²)), M_cl) (CFG877's shape).
- Hosts (illustrative Plummer baryons, chosen now, not fitted to any dwarf): H1 (M_b 1e4 M_⊙, a 30 pc), H2 (3e5, 200 pc),
  H3 (2e7, 700 pc).
- Initial state: settled halo ρ_c = ρ_ph in every cell inside R_out, plus the clump (cell masses m = m_ph + m_x).
- T_ret = 12 Gyr (primary; lenient: the clump of CFG878 route 2 forms at first atomic cooling, lookback ≳ 12.7 Gyr). 13.5 Gyr
  reported.
- Grid: faces {0} ∪ geomspace(0.5 pc, 20 kpc, 800); first-order upwind donor-cell fluxes with τ and G of the donor cell;
  SSP-RK2 (Heun), CFL 0.3, dt ≤ 10 Myr/α. Retention R(t) = M_ex(<r_t, t)/M_ex(<r_t, 0), M_ex = M_c − M_ph (linear
  interpolation of the face cumulative at r_t).

## 3. K-tests (identities and limits; each PASS/FAIL)

- **K1** gated solver with G ≡ 1 reproduces the two-sided solver bit for bit (max |Δm| = 0): the gated equation is CFG638's
  wherever d > 0.
- **K2** mass conservation |ΔM|/M ≤ 1e-12 in every run.
- **K3** α = 0: max |Δm| = 0.
- **K4** (sympy) spherical cumulative-excess law ∂_t M_ex(<r) = −α 4πG τ ρ_c M_ex(<r) from Poisson + continuity: residual 0.
- **K5** (sympy) centre law ∂_t ρ_ex(0) = −α 4πG τ ρ_c ρ_ex (limit r → 0); uniform cold solution ρ0/(1 + αt/2τ0)² satisfies
  it: residual 0; I(ρ_t) = ∫_{ρ_t}^∞ √(ρ_b + ρ)/(√(4πG) ρ²) dρ equals 2τ(ρ_t) at ρ_b = 0.
- **K6** numerics vs the centre law: uniform cold sphere (ρ0 = ρ_x0, R0 = 100 pc, background baryons ρ_b = 0.01 ρ0, ρ_ph = 0),
  centre-cell density at αt = 4τ0 within 1% of the centre ODE integrated independently.
- **K7** (sympy) no stationary counter-flow: steady CFG638 pressure equation with u = −v_s, isotropic Π = p, gives
  p = ρσ_J²/(1 − q/3) (q = ρ_ex/ρ_m), ≠ hydrostatic ρσ_J² for q > 0.
- **K8** time rescaling: α = 0.5 to T equals α = 1 to T/2 (max relative |Δm| ≤ 1e-9).
- **K9** in every two-sided run the centre-cell overfill never exceeds the initial-condition-free bound ρ*(αt) (defined by
  I(ρ*) = αt with the host's central ρ_b) by more than 1%.

## 4. Verdicts

**V1 two-sided retention (each footing, each host).** α_50 = s_50/T_ret, with s_50 the value of αt at which R first falls to
0.5 in the α = 1 run (exact by K8). α_c = I(ρ_x0/2)/T_ret (central bound, any initial state). Lenient galaxy floor
α_floor = 0.05 (one tenth of CFG623's α ≳ 0.5, allowing realistic infall to settle 10× faster than CFG541's idealised
α·t90 = 8–10 Gyr).
- **EXCLUDED** iff max over hosts of max(α_50, α_c) < α_floor on that footing.
- **TENSION** iff that max lies in [0.05, 0.5).
- **COMPATIBLE** iff some host has α_50 ≥ 0.5.

**V2 gated retention.** Smooth settled halo + clump, α ∈ {0.5, 1, 1.186}, to T_ret. **GATED RETAINS** iff R ≥ 0.5 in every
host × footing × α; else **GATED FAILS** (cells listed).

**Teeth (MUTATE, env CFG882_MUTATE=1, separate outputs `cfg882_MUTATE.out`, `cfg882_results_MUTATE.json`).**
- **M1** inverted gate (G = 1 iff d < 0) in V2's runs: must give R < 0.5 in every host × footing at α = 0.5. If not, V2 is
  **NOT DIAGNOSTIC**.
- **M2** gate removed (G ≡ 1, i.e. the V1 run read at αt = 0.5 T_ret): must give R < 0.5 in every cell; checked in the main run.
- The MUTATE run exits 1 by design when M1 bites.

**Overall class.** RETENTION REQUIRES THE GATE iff V1 EXCLUDED (both footings) and V2 GATED RETAINS with M1 and M2 biting;
TWO-SIDED RETAINS iff V1 COMPATIBLE on both footings; NO RETENTION iff V1 EXCLUDED and V2 GATED FAILS; otherwise MIXED (stated).

## 5. Reported without verdict weight

- D1 noise: gated, α = 1, H2, both footings, settled halo m_ph(1 + εξ) (ξ ~ N(0,1) clipped at 3, seed 882), ε ∈ {0.01, 0.1},
  plus the same noise without the clump (control): R, fraction of cells in (r_t, 2 kpc) emptied, M_ex(<r) at 0.5/1/2 kpc.
- D2 tidal identity radius D_crit = √(2V_h² r_t³/(G m)) (flat host, Jacobi radius = r_t), m = M_cl alone and M_cl + H2's
  baryons + phantom inside r_t; V_h = (G M_b,host a0)^(1/4) for M_b,host 6e10 and 1e11 M_⊙ (estimate).
- D3 single-clump pull Δg/g_law at r ∈ {0.2, 0.5, 1, 2, 5} kpc in point-baryon hosts M_b ∈ {1e7 … 1e11} M_⊙.
- D4 Chandrasekhar sinking time of one clump, t_df = 1.17 r² V_h/(G M_cl lnΛ), lnΛ = 5 (estimate), r ∈ {1, 3, 10} kpc.
- D5 τ, ψ amplitude of the overfill and max |v_s| at α = 1; T_ret = 13.5 Gyr variant of α_50, α_c.
- D6 the big-galaxy condition: under the smooth gate overfill mass is conserved (F_ret = 1), so CFG881's F_max bounds the
  fraction φ of baryons assembled through first-cooling blocks directly (φ ≤ F_max per shape). Stated, not scored.

## 6. Order and rules

This file is committed alone. Then `cfg882.py` (one process, `OMP_NUM_THREADS=1 nice -n 10`, < 10 min, < 2 GB), main and
MUTATE runs, README, one lane commit (own paths only). Footings never pooled. No downloads. No push. No edit of LEDGER.md,
THEORY_CANONICAL*.md or any other lane.

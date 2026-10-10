# CFG541: the cold-energy equations of motion made precise (CFG539 class A)

**Overall label: SPECIFIED WITH OPEN ITEMS.** The equations are complete, mass is exact, and the audit passes. Five things remain
open: the coefficient is free at O(1), the energy sink is only conditionally allowed, the overdamped drift is inconsistent in
diffuse reservoirs, kinetic (temperature) consistency is not supplied, and the PM uses the QUMOND phantom.

κ = ½ is fitted. The footings (9.3603e-11 / 1.1312e-10, written can / alt) are never pooled. The cold energy's mass is still
required. No dark-matter particle. This is not a closed theory. Every number below is read from `cfg541_results.json` or
`cfg541_results_MUTATE.json`.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first in 09e5d0a18.
- **The system:** `EQUATIONS.md`.
- **Script:** `cfg541.py`, sympy plus 1-D spherical drift-only numerics. No PM runs.
  - Run with `OMP_NUM_THREADS=2 nice -n 10 python3 cfg541.py`. It takes about 35 s and exits 0.
  - `CFG541_MUTATE=1` writes `_MUTATE` outputs and exits 1, as designed: all three teeth bite.
  - It imports `cfg515_lib` and `cfg540_bfjr` read-only, and reads CFG540's local VizieR file. Nothing was downloaded.
  - `CFG539_cold_energy_equation_of_motion/` was not touched.

## Results

| item | result | label |
|---|---|---|
| E1 equations | every field defined from the state, with units; constants traced (EQUATIONS §1) | SPECIFIED WITH OPEN ITEMS |
| D1 audit | dimensions consistent; τ built from {G, ρ_m} only | PASS (M3: a hidden constant is flagged) |
| V1 first variation | ∂F/∂ρ_c = ψ on the deficit, the interval [ψ, 0] on filled points | PASS |
| V2 gradient flow | variational form (census edge removed, mobility = deficit region): symmetric, so it **IS** a gradient flow. CFG539's committed form (edge in d, mobility on the catchment): asymmetric, so it **IS NOT** | — |
| V3 Lyapunov | sympy by-parts identity, no boundary term; largest step dF/F₀ ≤ −9e-15 | PASS |
| V4 minimiser | inside-out fill; KKT violation 0; flow r_* equal to the analytic value to ≤ 0.01% (sub-cell) and ≤ 0.9% (literal face) | PASS |
| V5 coefficient | stationary states do not depend on α (profiles agree to 8e-7); t₉₀ ∝ 1/α; t₉₀(α = 0.5) = 16.2–20.0 Gyr | **O(1) FREE; RATE-SENSITIVE (idealised)** |
| T2a edge | exhaustion radius = r_M/ln(1 + f_ret f_b/(1 − f_b)) for a point mass, with no census rule inserted: literal 0.36–0.85% (N = 400), ≤ 0.33% (N = 1600); fill is inside-out by the filled front | **NOT EMERGENT BY THE FROZEN RULE** (the q ≥ 0.5 front recedes; see below). Location emergent; inputs inherited |
| T2b groups | class-A edge at median r_*/Re 1.51 / 1.40; Δ = +0.118 / +0.106 ± 0.021 (census point-mass +0.153 / +0.145; no edge +0.010 / −0.010); 5× / 3× the supply would be needed | **PROBLEM PERSISTS** |
| S0 energy | E_sink/M_cat = 0.24–0.26 V_f² (MW-like), 0.11–0.12 (group-like), 0.32–0.35 (cluster-like); positive everywhere | sink needed |
| S(i) heat | σ² raised 0.14–0.18 dex above the phantom's Jeans value | **EXCLUDED** |
| S(ii) dark energy | cosmic Δρ_DE/ρ_DE 2.2e-6 (Δlog a₀ 4.9e-7 dex); local, leaving at c, ≤ 7e-9; staying (clustering DE), 2e-3 | **ALLOWED** only if dark energy is dynamical, not exact Λ, and does not cluster; Q not derived |
| S(iii) radiation | no EM coupling; GW ≤ 1e-15 of what is needed | **EXCLUDED** |
| S(iv) baryons | the drift force is non-gravitational; the energy is 17–19× the MW baryon K, 3× the group's | **EXCLUDED** (G9) |
| C1 drift speed | max \|v_s\|/c at t = 0: 4.8e-3 / 5.3e-3 (MW), 2.2e-3 / 2.5e-3 (group), **4.3e-2 / 5.2e-2 (cluster)** | **FAILS** the 1e-2 margin (clusters) |
| C2 completions | A0 s = −Γ (k-independent); A1 undamped wave UNSTABLE (Γ/2); A2 damped wave STABLE iff Γτ_ψ < 1 (τ_ψ = τ_ff works in every state); A3 STABLE; A4 UNSTABLE; A5 UNSTABLE for q > ½ at ck ≲ 1.4Γ | **CAUSAL-WITH-τ** (undamped: UNSTABLE) |
| MUTATE | M1 sign-reversed: F rises (+9.1e-3 per step); M2 unlimited reservoir: 1.83 M_cat settled, front at r_ta (cap broken); M3 hidden constant: flagged | all bite |

## The plain reading

1. **Variational origin.**
   - Class A is the Onsager/Wasserstein gradient flow of the deficit field energy F = (1/8πG)∫|∇ψ|², with mobility ρ_c α τ_ff.
   - That holds only if the census edge is **removed** from the deficit, and the mobility region equals the deficit region
     (switch × catchment).
   - CFG539's committed form (edge inside d, drift over the whole catchment) is not a gradient flow of any functional.
2. **What the principle fixes.** It fixes the form of the drift and every stationary state; the stationary states are
   mobility-independent.
   - It does **not** fix the coefficient: α is O(1) FREE, which replaces the "λ = 1 convention".
   - The required robustness (z = 0 insensitive to α ×2) fails in the idealised drift-only model, because settling takes 8–10 Gyr
     at α = 1 there.
   - CFG539 Stage 2's mobility ×0.5 / ×2 runs, which include orbital infall, are the real test.
3. **Edge.**
   - With the edge removed, the flow fills inside-out and stops where the catchment's own cold energy runs out.
   - For a point mass that radius **is** the census formula, because the turnaround catchment at the cosmic ratio holds
     exactly 5.364 M_b/f_ret.
   - So the location is reproduced by the dynamics. The supply amount (A6) reduces to the catchment definition, which is still
     inherited.
4. **Groups.** The class-A edge for an extended (Hernquist) group is the phantom's exhaustion radius. It lies at about 1.4–1.5 Re,
   which does not fix CFG540: +0.118 / +0.106 ± 0.021 remains, the same as CFG540's post-freeze supply-cap variant.
5. **Energy.**
   - Settling must lose 0.1–0.35 V_f² per unit settled mass.
   - Heat, radiation and the baryons are excluded.
   - Only an exchange with *dynamical* dark energy is numerically harmless (cosmic 5e-7 dex in a₀). It is not derived, and it is
     incompatible with an exact Λ.
6. **Causality.**
   - The linear operator is local in time and does not propagate. The only instantaneous piece is ψ's Poisson equation.
   - A retarded, *undamped* ψ makes the system unstable at rate Γ/2.
   - A *damped* ψ wave with damping time τ_ff is stable in every state, because ρ_c < ρ_m, and has front speed c: CAUSAL-WITH-τ,
     with no new constant.
   - The nonlinear drift speed, however, grows as ρ_m^(−1/2). In cluster reservoirs it reaches 4–5% of c at t = 0.

## Corrections and disclosures (dated 2026-10-09; the frozen text is not edited)

- **Correction 1 (numerics and implementation, made before any label was adopted).** On the first run three problems appeared:
  - The trace rule (cells under 1e-14 M_cat moved whole) emptied the tiny innermost cells, so the literal front sat at about
    0.06 kpc. The threshold is now per cell, at 1e-12 of each cell's initial mass, and applies only to draining cells.
  - The settled-mass proxy Σ min(ρ_c, ρ_ph) V was not monotone, which gave NaN or wrong t₉₀. Settled mass is now the cold mass
    inside the analytic r_*.
  - The CFG540 identity control used this lane's 4-digit footings. It now uses CFG540's own a₀ values: |diff| = 0.
  - The first run's outputs were overwritten (not kept).
- **Post-freeze diagnostics** (reported, not verdict inputs):
  - the filled front (q ≥ 0.999);
  - the reservoir radius where ρ_c0 ≥ ρ_ph/2;
  - Π = |v_s| τ/r;
  - a resolution check of T2a at N = 1600.
- **T2a, verified as hard as a pass would be.**
  - The frozen rule's inside-out clause FAILS in every point run: the q ≥ 0.5 front recedes in 8–14 samples, by up to
    0.055 in ln r at N = 400. That holds at N = 1600 too.
  - Diagnosis: the reservoir's own initial density already exceeds ρ_ph/2 beyond 1.57–2.96 r_*.
    - The contiguous q ≥ 0.5 region first extends into that undrained reservoir, peaking at 1.25–1.51 r_*.
    - It then recedes as the reservoir drains.
    - The filled front (q ≥ 0.999) never recedes.
  - So the frozen label is **NOT EMERGENT BY THE FROZEN RULE**. It is reported as frozen, not rounded up. The substance (location
    reproduced, fill inside-out) is stated with its diagnosis.
- **The 1-D model is the drift sub-flow only:** static baryons, cold energy at rest in a top-hat out to r_ta, no orbital motion,
  no expansion.
  - Its times (t₉₀) and its drift speeds are idealised. Orbital infall would bring the reservoir in faster, and at higher density.
  - Π = 10–1300 shows the overdamped reading itself is not valid in the reservoir (open item 3 in EQUATIONS).
- **T2b**
  - It uses the census f_ret to infer M_ta, and so the catchment content, for observed groups.
  - It ignores any pre-existing cold-energy overfill. That only moves r_* inward, so the class-A result is the most favourable case.
  - It inherits CFG540's caveats: hot-gas content of M_bar, and the meaning of Re for groups.
- **The supply-factor scan in T2b is a report, not a fit.** Nothing adopts it.

## Note for CFG539 Stage 2 (read-only observation; that lane is not edited)

CFG539's MUTATE-S (no census edge, s = f_sw × catch) is, by V2, the *variational* form of class A. If the PM catchments hold the
cosmic ratio, its fill should stop at about the same exhaustion radius as the census-edge run. An "indistinguishable" MUTATE-S
would then be consistent with this lane's T2a result, not a failure of the edge.

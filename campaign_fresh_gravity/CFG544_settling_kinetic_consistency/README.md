# CFG544: kinetic consistency of class-A settling (CFG541 open item 5)

**Substantive result: INCONSISTENT as is. The derived fix (two-sided deficit) FAILS. A posited velocity closure (FIX-2) passes
every gate, but it is not derived, so it is reported as a candidate only. Overfill: NOT HANDLED. Q3: CHANGED in the N-body
(the drift-only edge and profiles are UNCHANGED). Full-system Lyapunov: NOT ESTABLISHED.**

**Label as frozen: NO LABEL.** Control C4 misses by 0–0.6e-4 of M_cat (see the disclosures). With C4 read at the toy's
resolution, the rule gives **INCONSISTENT (needs a posited velocity closure; FIX-2 is a candidate, not adopted)**.

κ = ½ is fitted. The footings (9.3603e-11 can / 1.1312e-10 alt) are never pooled. The cold energy's mass is still required.
No dark-matter particle. This is not a closed theory. Every number below is read from `cfg544_results.json`,
`cfg544_results_MUTATE.json` or `cfg544_post.json`.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first in b6eb542c5.
- **Scripts:**
  - `cfg544.py`: sympy, a spherical N-body shell toy (N = 30000; no PM) and a 1-D drift-only model.
    - Run with `OMP_NUM_THREADS=2 nice -n 10 python3 cfg544.py`. It takes about 45 min on 2 processes and exits 0.
    - `CFG544_MUTATE=1` exits 1, as designed: all three teeth bite.
  - `cfg544_post.py`: post-freeze diagnostics only.
- **Inputs:** CFG541's JSON, read only. The CFG539/541/542 folders were not touched. Nothing was downloaded.

## Q1: does class A, as is, settle into the Jeans state?

**Analytic (K1, sympy).** Take the moments of E3. Along u + v_s, the drift enters σ² only as advection:
Dσ²/Dt = −2σ² ∂ₓu − ∂ₓq/ρ, with no ∂ₓv_s term. So the drift compresses the density without compression heating, and the
settled cold energy keeps whatever dispersion it had at its source. CFG541's reservoir is at rest, so drift-only settling
delivers σ = 0, against the required σ_eq² ≈ V_f²/2. Control C1: the deep untruncated σ_eq²/V_f² = 0.5008 (MW-can).

**Toy, as is (one-sided deficit, velocities kept).** The kinetic gate fails in all 4 cells for both initial states.

| cell | IC-C (settled at rest), 5 Gyr: log X / D | first \|D\| > 0.1 | IC-B (infall), 10 Gyr: log X / D | β (IC-B) |
|---|---|---|---|---|
| MW can | −0.028 / **+0.161** | 1.25 Gyr | **−0.156** / −0.007 (not steady) | 0.98 |
| MW alt | −0.062 / **+0.174** | 1.00 Gyr | −0.059 / +0.076 (not steady) | 0.99 |
| cluster can | **−0.124** / +0.051 (not steady) | 1.75 Gyr | **−0.110** / **+0.174** | 0.99 |
| cluster alt | −0.088 / **+0.220** | 1.50 Gyr | −0.041 / **+0.230** (not steady) | 0.99 |

- **What happens to the settled cold halo:** it collapses (contracts) within 1–1.75 Gyr, roughly one free-fall time.
- **The end state is sub-virial and almost purely radial** (β ≈ 0.99). σ²/σ_eq² runs from 1.4–2.0 in the inner shell down to
  0.01–0.15 near 0.9 r_*.
- **The collapse overfills the inner halo, and the one-sided rule never removes that overfill.** T1 equality (ρ_c = ρ_ph) is
  broken by +0.05 to +0.23 dex.
- **Roundness** cannot be tested in a spherical toy.

## Q2: fixes

**FIX-1, the two-sided deficit (derived, no constant).**
- Sympy confirms the structure:
  - dF/dρ_c = ψ everywhere (no interval);
  - the Hessian is the Coulomb kernel, so F is smooth and convex;
  - the by-parts Lyapunov identity holds;
  - ψ = Φ_law − Φ, so v_s = ατ(g_law − g).
- **Kinetically it FAILS in every cell.** The intended "infall and push-back thermostat" overshoots:
  - The outward pushes at fixed velocity pump energy in. Net inflow from the sink is −0.64 to −2.00 V_f² per M_cat on IC-C.
  - The halo puffs up and empties: D = −0.07 to −0.83, and M(<r_*)/M_ph = 0.17–0.82.
  - It is not steady.

**FIX-2 = FIX-1 + Ornstein–Uhlenbeck velocity relaxation** (rate α/τ, target the Jeans dispersion of the current density).
- No new constant. The target temperature is a posited closure.
- **It passes the kinetic gate in all 4 cells, on both initial states:**
  - |log X| ≤ 0.014 and |D| ≤ 0.027;
  - steady to ≤ 0.045 dex;
  - nearly isotropic (β = 0.05–0.26).
- **Energy bookkeeping:**
  - IC-B: a net outflow of +0.25 to +0.31 V_f² per M_cat (COMPATIBLE).
  - IC-C: the cold settled halo has to be heated, a net inflow of −0.51 / −0.52 (MW) and −0.70 / −0.71 (cluster).
- **Post-freeze:** add CFG541's drift-only release (0.77–1.01). The whole-history net is then 0.26 / 0.27 (MW) and
  0.29 / 0.31 (cluster) V_f² per M_cat. That is close to CFG541's E_sink of 0.24 / 0.26 and 0.32 / 0.35.
  - So the sink accounting closes only if the dark-energy exchange runs in both directions: out during settling, back in
    during reheating.

**Full-system Lyapunov (K3): NOT ESTABLISHED.**
- Under Vlasov, dF/dt = ∫ρ u·∇ψ, which is indefinite.
- Under the drift, dE/dt = −α∫ρτ ∇ψ·∇Φ, which is indefinite (it is positive whenever overfill is pushed out).
- E − TS gains +α∫ρτ|∇ψ|² under the drift.
- E_law − F = E + const (sympy), so it is no better than E.
- The OU term is a gradient flow only locally in x. With T = σ_J²(x), no global E − TS is conserved by Vlasov.

**ALT-S (Smoluchowski flow of E − TS at T = V_f²/2; diagnostic only).**
- It has a Lyapunov function, but it destroys T1 and the edge.
- MW-like: the isothermal state at M_cat spreads to r_ta (r_99 = 2.42 / 2.66 r_*), with D = −1.57 / −1.70 dex and
  −3.3 / −3.4 dex at r_M.
- Point mass: no regular state. The Boltzmann cusp puts all the mass at the inner boundary.

## Overfill

The test injects 0.3 M_ph(<0.3 r_*) and pairs each run with a baseline. P is the persistence at 5 Gyr.
- **One-sided rule:** P = +0.90 to +1.23. The overfill persists, as the rule implies.
- **FIX-1:** P = +0.373 (MW can), +0.146 (MW alt), −0.057 and −0.067 (clusters). One cell is above 0.2, so the label is
  **NOT HANDLED**.
- **FIX-2 (post-freeze):** P = +0.30 to +0.43. The two-sided drift removes overfill, but more slowly than 5 Gyr.

## Q3: edge and stationary profiles

- **1-D drift-only (CFG541's setup):** two-sided and one-sided reach the same r_* to |Δ ln r_*| ≤ 2.8e-6. The cumulative
  profiles differ by ≤ 3.2e-6 M_cat. So the drift sub-flow's emergent edge is **unchanged**.
- **N-body (frozen part (b), FIX-1 IC-B):** ln(r_99/r_99,analytic) = +0.24 / +0.28 (MW) and +0.65 / +0.70 (cluster).
  The label is **CHANGED**.
- **Diagnosis (post-freeze):**
  - The equilibrium IC under pure Vlasov alone (C2) already spills to +0.26 to +0.54.
  - FIX-2 end states sit at +0.22 to +0.45.
  - A sharp truncation at r_* cannot be held by an isotropic, pressure-supported halo. Kinetic consistency itself softens
    the edge outward by about 25–55% in r_99.
  - Inside 0.1–0.9 r_* the profile still matches (|D| ≤ 0.027 under FIX-2).

## Controls and MUTATE

- **C1 PASS.**
- **C2 PASS** in all 4 cells: |log X| ≤ 0.021 and D ≤ +0.083 after 2 Gyr of pure Vlasov.
- **C3 PASS:** |ΔE/E| ≤ 7.7e-4.
- **Mass exact** in every run.
- **C4 FAILS as frozen:** |M_ph(<r_*)/M_cat − 1| = 1.04e-4, 1.60e-4, 1.47e-4 and 0.98e-4.
- **MUTATE: all teeth bite.**
  - MV: σ² ×2 at settling, then pure Vlasov. The halo puffs up, D = −0.21 to −0.27 in all 4 cells.
  - MO: overfill under the one-sided rule, P = 0.90–1.23.
  - MT: FIX-2 with the OU target ×2 fails the gate in all 4 cells.

## Corrections and disclosures (dated 2026-10-10; the frozen text is not edited)

- **Correction 1 (integrator, made after run 1 and before any label was adopted).**
  - Run 1 used the frozen fixed step. C3 failed in the clusters (ΔE/E = 0.18).
  - The cold, radial runs (as is, FIX-1) gained 6–100× |E₀| from central passages. Particles were ejected to r_99 = 18–84 r_*.
  - The Vlasov step now uses individual power-of-two substeps (η = 0.03, at most 4096) in the step's frozen enclosed-mass
    profile. The drift work is now computed exactly (W after minus W before), not to first order.
  - Run-1 outputs are kept as `cfg544_run1.out` and `cfg544_results_run1.json`.
  - FIX-2 and the overfill numbers barely moved. Run 1's as-is "puff-up" was an artefact; the corrected runs contract.
  - The remaining integrator error, |E − E₀ − work|/|E₀|, is up to 0.26 (cluster as-is IC-B), 0.06–0.08 (other cold as-is
    runs) and ≤ 0.01 for every FIX-2 run. The as-is fail verdict does not hinge on it: the drift-only analytic σ = 0 and the
    collapse within about one t_ff are robust.
- **C4 (verified as hard as a pass).** CFG541's `r_analytic` is a cell-wise minimiser of max(ρ_ph, ρ_c0) on its 400-cell grid,
  not M_ph(<r) = M_cat. This 1e-4-level definitional offset fails the frozen 1e-4 tolerance. It is about 100× below the toy's
  noise. The frozen label is withheld; the label computed with C4 set aside is given above and in the JSON
  (`kinetic_if_C4_read_at_toy_resolution`).
- **Numerical guard added before any label (1-D model).** The 1-D model needed an empty-cell guard (τ → ∞ at ρ_m = 0 for a point mass).
- **Toy limits:**
  - static baryons and background;
  - spherical symmetry;
  - the initial 0.05 V_f seed dispersion (disclosed);
  - α = 1 (O(1) FREE per CFG541);
  - the drift limiter acted on ≤ 6.4e-4 of the moves.
- **Point-mass phantom.** It is ~0 inside r_M, so FIX-1 pushes out any cold energy there. The cluster cells are an
  idealisation.

## The plain reading

- Class A's drift cannot by itself produce an equilibrium halo. It carries no heat, so the settled cold energy is cold and
  collapses within one free-fall time, overfilling the core. The one-sided rule then locks the overfill in.
- Making the deficit two-sided is derived and costs no constant, but it makes things worse: pushing at fixed velocity heats
  the halo and empties it.
- What works is relaxing the velocities toward the Jeans dispersion at the free-fall rate. It needs no constant, but it
  inserts the equilibrium temperature: the same open question as CFG461 (what sets σ⁴ = G M_b a₀/4). It also requires the
  dark-energy exchange to return about 0.5–0.7 V_f² per settled mass during reheating.
- Even then, an isotropic equilibrium cannot keep a sharp edge at r_*.

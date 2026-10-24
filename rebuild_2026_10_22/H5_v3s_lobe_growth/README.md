# H5_v3s_lobe_growth: do v3s's D·P < 0 lobes produce harmful growth?

## Verdict (frozen rules, FROZEN_CRITERIA §3): BENIGN in every class. Reading: CRISP FINDING, scoped.

| class | layer P (lobe density granted to the crossing fluid) | layer D (the derived flow state) |
|---|---|---|
| (a) outer globulars (4, both footings, L★ floor / 24 / 90) | **BENIGN**: N_path ≤ 0.048 / 0.046 at the PROXY speed; N_cum ≤ 0.38; V_crit ≤ 8.0 km/s, below V_apo,10 ≈ 36 km/s | **NO NEGATIVE LOBE IN THE FLOW STATE** |
| (b) MW satellites (32 with LVD 3-D speeds; 10 have a v3s lobe at the floor, 1 at 90 pc) | **BENIGN**: N_path ≤ 0.013 / 0.012; N_cum ≤ 0.029 | **NO NEGATIVE LOBE IN THE FLOW STATE** |
| (c) worst case | **BENIGN**: pure radial orbit at apocentre N_apo ≤ 0.46 (NGC 2419, deepest path). No system can hold a co-moving lobe (r_cap ≤ 0.25 pc vs lobes at ≥ 171 pc). Co-moving for T_H is posited only: N_TH ≤ 102 | a negative lobe cannot be produced from positive khronon charge (A4) |

**The khronon's velocity relative to the lobe.**
- v3's PN system is Galilean-covariant (A2). So the static branch (v_τ = 0, Ξ = φ + C) holds only in the khronon's own
  rest frame. A system moving at V through its host's held khronon is therefore not in its static branch.
- In the system's frame the host khronon streams through at −V + δv, with |V + δv|² = V² + 2GM_b/r. This is cold flow in
  the baryons' Newtonian potential: ψ = φ − Ξ → φ_N, because the stream's own response is ∝ ρ̄_host (A3) and V ≫ V_*.
  For the outer globulars and satellites, V_* ≤ 0.26 km/s and |δv| ≤ 0.065 km/s.
- **The lobe pattern rides with the system; the fluid stays in the host frame.** A fluid element spends path/V inside a
  lobe: 1–12 Myr for the globulars and 1–25 Myr for the satellites (H4's ℓ/V).
- **The stream carries positive charge through the would-be lobe.**
  - The khronon charge ρ_τ is conserved along v_τ, and its sign is a Lagrangian invariant (A1, A4).
  - The stream's density is ρ_τ/ρ̄_host = u²/(2u − 1) ≥ 1 (Danby–Camm, A5), with u = b/R the ratio of the streamline's
    impact parameter b to its present distance R = r sin θ from the downstream axis.
  - So in the flow state the lobe region has D·P ≈ ρ̄_host > 0. That is the stiff side, where ω² ≥ 0: there is nothing to
    grow.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² (9.36e-11 / 1.13e-10 inside H4's reused code), never pooled. No
dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

**Checks 11/11 PASS, exit 0.** `H5_MUTATE=1` fails A2, A3 and A5 as frozen (7/10, exit 1). Run time 126 s, peak RSS
0.61 GB, one thread, nice 15. No downloads. The live heavy run was not touched.

## Part A: derivation (sympy; JSON `A`)

| check | what | result |
|---|---|---|
| A1 | Euler–Lagrange equations of H4 A1's PN Lagrangian, with the stiffness as a generic F(∇·P) (so the switch is included) | the σ equation is −[∂_tρ_τ + ∇·(ρ_τv_τ)], with ρ_τ = ∇·P − μ_K²Ξ/K and v_τ = −∇σ; the φ equation is Poisson with ρ_m + ρ_τ; D_tv_τ = −∇(φ − Ξ). All residuals 0 |
| A2 | Galilean boost x = x′ + Vt, σ′ = σ + V·x′ + V²t/2 | Ξ′ − Ξ ≡ 0 and v′ = v − V. The khronon rest frame is physical; the static branch lives only there |
| A3 | steady linear response in the system's frame, about the host's (ρ̄ > 0, g_e, stiffness Θ): anisotropic Hessian K[M_L nn + M_T(1 − nn)], Poisson, continuity, Euler | **δρ_τ = δρ_m / [M(k̂) − 1 + Θ L★²k²/2 − (k·V)²/(Kρ̄)]** (residual 0). V = 0 gives exactly D10 Route F's screened kernel (the static lobes). V → ∞ gives −Kρ̄δρ_m/(k·V)², δψ → −Kδρ_m/k² and δv = k δψ/(k·V): the cold wake of the baryons' Newtonian potential, with amplitude ∝ ρ̄ |
| A4 | Jacobi's formula: ρ = ρ₀(X)/det(∂x/∂X) solves Lagrangian continuity | residual 0. A khronon element that enters with ρ_τ > 0 cannot reach ρ_τ < 0 (single stream, before caustics). Multi-stream dust is ≥ 0 by construction |
| A5 | Danby–Camm flow past a point mass: b(r, θ) from the hyperbolic orbit, v_r = −(GM/bV) sin θ + V cos θ, v_θ = −bV/r, ρ/ρ∞ = b²/[R(2b − R)] | steady continuity residual 8e-15 at 200 points; energy relation 7.5e-15; ρ/ρ∞ − 1 = (b − R)²/[R(2b − R)] ≥ 0 (identity). Independent numerical Lagrangian integration matches to 1.0e-6 at 25 points, with min ρ/ρ∞ = 1.0004 |

- **NGC 2419 in its Plummer potential (reported, not gated).** GM/(V²a) = 6.3e-3 at the PROXY speed. Over 84 points at
  r ≥ 9a, ρ/ρ∞ ∈ [1 − 3.7e-9, 1.0044], and the point-mass formula holds to 2.8e-3.
- **Physical content.**
  - The crossover speed is V_* = √(Kρ̄(M − 1) + γ_Lρ̄k²)/k.
  - Above it, the moving system cannot set up its static external-field phantom (lobes included). The stream's response
    is a wake ∝ ρ̄, first order only on the downstream line, where it is positive (focusing). Off that line it is second
    order.
  - Below it (and inside the capture radius r_cap = 2GM_b/V², U1), the static solution can apply.

## Part B: numbers (JSON `rows`, `verdicts`; per system `h5_per_system.csv`)

**B0, the record reproduced first.**
- **B0a.** H4's row `S1_MW-M31|canonical|e0|L*21.7` is reproduced from H4's json region statistics with H4's `rates()`
  (copied verbatim): 18 fields, deviation 0.
- **B0b.** X3's D4 map minima (8 cells: 4 clusters × 2 footings at the floor) are reproduced with D10's solver and X3's `SW`:
  deviation 0.
- **B0c.** S1's host field `x_e_mid` is reproduced for all 64 MW rows, deviation 0. X3's `g_mw` with D10's rounded
  constants differs by 3.9e-5, as expected.
- **Method checks.** B2 (uniform sphere path integral) is good to 0.04 %. B3 (radial-apocentre integral on a slab) is good
  to 0.02 %.

**Maps.**
- These are v3s maps: X3's switched operator solved warm from the unswitched solution, with s_g = the host's phantom at
  the system's distance.
- 152 maps, each with 2 solves. Worst residual 1.0e-10. No lobe touches the box.
- **New fact: the v3s lobes are deeper than the unswitched maps X3 tabulated.** NGC 2419 at the canonical floor is
  −6.07e-3 M☉/pc³ (at 369 pc, θ 129°) against −3.27e-3. Pal 4 is −9.2e-4 against −4.1e-4. Pal 14 is −4.0e-4 against
  −1.5e-4. The deepest cells sit just outside the switch surface, where D·P drops to its AQUAL value (X3 §1: "D·P may jump
  downward across Σ"). So the preliminary co-moving 86 e-folds becomes **102** (local x; 117 with the preliminary's x_e
  convention).

**(a) Outer globulars.** The speed is PROXY: v_c(R_GC) of D10's MW model, 167–175 km/s. GC 3-D velocities are not on
disk (needed: Vasiliev & Baumgardt 2021, or Baumgardt's orbit table).

| footing, L★ | lobe r (pc) | deepest (M☉/pc³) | N_TH (co-moving, posited) | N_ℓ deepest (H4 convention) | N_path | V_crit (km/s) | N_apo | N_cum (n_enc 7–12) |
|---|---|---|---|---|---|---|---|---|
| canonical floor, NGC 2419 | 319–1631 | −6.07e-3 | 102.5 | 0.090 | 0.048 | 8.05 | 0.46 | 0.38 |
| canonical floor, Pal 3 / Pal 4 / Pal 14 | 171–553 | −4.0e-4 to −9.2e-4 | 36–44 | ≤ 0.013 | ≤ 0.010 | ≤ 1.7 | ≤ 0.18 | ≤ 0.073 |
| alt floor, NGC 2419 | 319–1631 | −6.63e-3 | 101.9 | 0.086 | 0.046 | 7.93 | 0.44 | 0.37 |
| alt floor, Pal 3 / Pal 4 / Pal 14 | 207–553 | −3.1e-4 to −7.4e-4 | 30–37 | ≤ 0.010 | ≤ 0.009 | ≤ 1.5 | ≤ 0.15 | ≤ 0.065 |
| 90 pc | NGC 2419 only (757–1482 / 833–1482) | −3.6e-4 / −3.9e-4 | 28 | 0.020 | 0.021 / 0.018 | 3.5 / 3.1 | 0.22 / 0.19 | 0.16 / 0.15 |

- **The missing speeds cannot change the class.**
  - N_path ≥ 1 needs V < V_crit ≤ 8.0 km/s relative to the MW's held frame.
  - The apocentre of a flat-curve orbit with r_a/r_p = 10 still moves at 36 km/s; there N_path ≤ 0.22 (NGC 2419).
  - A pure radial orbit stopping at apocentre, the slowest bound case, gives N_apo ≤ 0.46.
- **Flow state.**
  - The lobe cells (× 16 azimuths, V parallel and perpendicular to g_e) carry ρ_τ/ρ̄_host from 1 to 1 + 1.6e-4.
  - r_cap is 0.005–0.25 pc, against lobe inner radii of 171–833 pc.

**(b) MW satellites.** These are U1's LVD-3D speeds (107–642 km/s). 22 of the 32 have no ρ_τ < 0 cell in v3s or v3 at
either L★: their lobes are shallower than the Galactic phantom at their distance.

| footing, floor | systems with a lobe | deepest | N_TH | N_ℓ deepest | N_path | V_crit (km/s) | N_apo | N_cum |
|---|---|---|---|---|---|---|---|---|
| canonical | CVn II, Cen I, Col I, Eri II, Her, Leo IV, Leo V, Peg III, Peg IV, Psc II | −2.6e-4 (CVn II) | 5.5–18.4 | ≤ 0.021 | ≤ 0.013 (Eri II) | ≤ 2.0 | ≤ 0.16 | ≤ 0.029 |
| alt | the same 10 | −2.3e-4 | 2.3–16.0 | ≤ 0.019 | ≤ 0.012 | ≤ 1.95 | ≤ 0.16 | ≤ 0.025 |

At 90 pc only Eridanus II keeps a lobe: N_path 0.005 / 0.004. Flow state as in (a): ρ_τ/ρ̄_host ≥ 1, and r_cap ≤ 0.041 pc
against lobes at ≥ 234 pc.

**(c) Worst case.**
- **Slowest bound configuration.** A pure radial orbit at apocentre gives N_apo ≤ 0.46. The fluid's relative
  displacement is g_e t²/2 along g_e, both branches, maximised over lines and turning points.
- **Co-moving.**
  - It would need the khronon bound to the system at lobe radii.
  - The capture law allows that nowhere: r_cap ≤ 0.25 pc. At apocentre the relative speed exceeds the escape speed at
    r_in (≤ 4.7 km/s) within ≲ 16 Myr.
  - It would also need negative charge, which positive initial data cannot supply (A4).
  - So N_TH ≤ 102 describes a posited state, not one v3s produces.
- **Nonlinear physics, plainly.** What a hypothetical co-moving system's would-be lobe becomes is not computed here: a
  khronon void at ρ_τ → 0⁺, or a non-static flow. Either way ρ_τ ≥ 0, so the bounded rate √(Kρ_τ(M − 1)) is real-stable
  throughout, at linear order.

## Readings beyond this lane (flagged, not scored)

1. **H4's saddles and X3 qualifier 3.** A4 holds for every ρ_τ < 0 region of a static map, not only these lobes. H4's
   saddles and Mpc lobes, and X3's "bounded instability 0.006–0.20 e-folds", describe backgrounds that v3's khronon flow
   cannot produce from ρ_τ > 0 initial data:
   - in the literal single-stream reading, before caustics;
   - in the multi-stream reading, by construction.

   The same holds for unswitched v3's Hadamard instability, which also needs ρ_τ < 0. Whether that state is reachable by
   any other route (caustics, initial data) is for the H4/X3 owners.
2. **Moving systems' statics.** The frame result (A2, A3) is U1 part (b) applied to every system moving through its
   host's held khronon.
   - **Outer globulars:** r_cap = 0.005–0.25 pc, far inside r_h = 16–28 pc. In the literal reading they hold no external-field
     phantom, so D10's static solution is not their dynamical state, and the L★ floor's leverage from them needs
     re-examination. In the multi-stream reading the outcome is history-dependent.
   - **The Sun:** by the same formula (hand arithmetic), r_cap ≈ 0.03 AU at ~240 km/s through the Galactic frame.
   - Not computed here.

## Execution history (no amendments; no pass line, verdict rule or input changed)

- **Dev check (disclosed).** A scratch driver timed one map block (NGC 2419, Pal 14, canonical floor) before the main run.
  Its numbers equal the main run's.
- **Run 1.** Complete, 11/11. Afterwards I noticed that frozen §1 A5's *reported* Plummer line was missing. I added it,
  then reran main and mutate. Every other output line is byte-identical to run 1; only the run-time lines differ.
- **Constants.** H4's `rates()` uses G = 6.67430e-11, while the globular density conversion uses D10's G = 6.674e-11 (as
  X3). The difference is 4.5e-5 relative and is ignored.

## What this does not show

- No nonlinear time evolution and no caustic physics.
  - The flow state is the steady linear response plus the exact cold flow in the baryons' Newtonian potential. Both
    neglect the stream's own self-gravity and hold response, which are O(V_*²/V²) ≤ 3e-6.
  - The approach to the flow state from a different past is not simulated.
- The globular speeds are PROXY. The verdict stands for any speed above 8 km/s and for any bound orbit down to a radial
  apocentre.
- The maps are D10's axisymmetric uniform-field model with E_mid. The host's tide, the field's rotation along the orbit
  and non-axisymmetry are not modelled.
- Only the MW satellites with LVD-3D speeds are scored; the M31 satellites and Leo T are not.
- The pile-up bound assumes every orbit re-crosses the same fluid element (an upper bound).

## Input ledger (full: `ASSUMPTION_LEDGER.md`)

| input | class |
|---|---|
| PN system, J_x masses, switched stiffness, capture law, positive initial charge | FRAMEWORK-NATIVE (BS24 PN transcription PROVISIONAL) |
| D10 solver (imported), X3 `SW`/`g_mw`/`s_gal`, H4 `rates()`, S1 `g_host` (copied read-only) | METHOD (record code) |
| GC L_V, r_h, R_GC; satellite σ, r_h, d; LVD proper motions and v_los | RAW + SURVEY-CALIBRATION |
| Υ_V 1.6 (GC) / 2 (satellites, via S1), MW Hernquist 6e10 M☉ | SURVEY-CALIBRATION |
| GC speeds v_c(R_GC); orbit bracket V_apo,10; T_H; pile-up n_enc | PROXY / ILLUSTRATIVE / METHOD |
| a₀ footings, κ = ½, L★ | FITTED |

No ΛCDM-processed input, no QUMOND or EFE recipe, no literature value in any check.

## Files and run

- `h5_v3s_lobe_growth.py` writes `h5_v3s_lobe_growth.out`, `h5_v3s_lobe_growth_results.json` and `h5_per_system.csv`.
- `H5_MUTATE=1` writes `*_MUTATE.out` and `*_results_MUTATE.json`.
- Run: `OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/H5_v3s_lobe_growth/h5_v3s_lobe_growth.py` (~2 min,
  0.61 GB). It is deterministic: it re-executes itself with PYTHONHASHSEED = 0.
- Criteria commit: 2cde8548ed (alone, before any script or number).

# C8_instantaneous: is the instantaneous (leaf-elliptic) sector of the C4-literal parent well posed, and is it observable?

## Verdict: WELL-POSED + UNCONSTRAINED (scoped)

- **Well posed (weak-field leaf problem, fully nonlinear in P and W).** On each leaf, the P/lapse equations are the
  Euler–Lagrange equations of one **strictly convex** functional. It has a unique solution for every source, at every
  field strength below the cap.
  - The functional is E[Φ, P] = ∫ |∇Φ − KP|²/2K + g(K|P|) + (γ_L/2)(∇·P)² + ρΦ, with g = W − u²/2K.
  - The conditions are γ_L > 0 and g convex. The record's W has g′ = u²/K(a₀−u) ≥ 0 and g″ = u(2a₀−u)/K(a₀−u)² ≥ 0 on [0, a₀).
  - The cap is a barrier (W → ∞ at u → a₀), so u < a₀ everywhere.
- **No existing data constrain the instantaneous response.**
  - Binary pulsars: the largest effect is 3.2e-14 of the measurement error.
  - α₂-type tests: 1.7e-7 of the bound.
  - GW170817: Δv/c ≤ 6e-32, against a bound of 1e-15.
- **Physical meaning (no spin).** The response is a real infinite-speed influence relative to the khronon's leaves. It
  is not a gauge artefact. It is ordered in τ, so it passes criterion B. It travels faster than light, so it fails
  criterion A. At realistic scales it is about 1e-46 m/s² (see 3).
- **Checks.** 8/8 scored PASS, exit 0. Two checks are reported but not scored: K6 (true by construction) and K10
  (estimates only).
  - `C8_MUTATE=1` (γ_L → −γ_L) breaks K1, K3, K4 and K5 (4/8).
  - Run cost: 76 s, 0.30 GB RSS, single thread, nice 15, no downloads.

Settings: κ = ½ FITTED. Footings 9.36e-11 / 1.13e-10 m/s², never pooled. No dark-matter particle. Not "theory closed".
Nothing here says the data favour the framework.

## 1. Well-posedness

| item | status | result |
|---|---|---|
| Lagrangian = −[convex terms] | DERIVED (sympy, K2) | identity L = −\|a−Kp\|²/2K − g(K\|p\|) − (γ_L/2)ψ² − ρΦ holds with residual 0 |
| Principal symbol | DERIVED + COMPUTED (K1) | The Schur complement of the linearised symbol is K(I − ξ̂ξ̂) + H_g + γ_L ξξᵀ, which is ≥ min(K, γ_L\|ξ\|²). This holds at every u ∈ [0, a₀) and angle (1071 points, mpmath at 50 digits; min ratio = 1). W is algebraic in P, so the nonlinearity never enters the derivative part of the operator. Φ and P_L are second order. P_T is algebraic with coefficient ≥ K (γ_F = 0). |
| Uniqueness | DERIVED (K3) | Take two solutions. E is affine along the segment between them only if ∇δΦ = KδP and ∇·δP = 0, which forces ΔδΦ = 0, so δ = 0 (rank 4). At γ_L = 0 the kernel is 1-dimensional, and uniqueness then rests on the strict convexity of g (AQUAL's case). |
| Existence on a bounded domain | DERIVED (direct method) | E is convex and lower semicontinuous. It is coercive on H¹₀ × {\|P\| < a₀/K, ∇·P ∈ L²}: \|∇Φ\| ≤ \|∇Φ − KP\| + a₀\|B\|^½. So a unique minimiser exists. Boundary data: Φ Dirichlet (or external-field data, as in D7d), natural ∇·P = 0. |
| Whole space, decay at infinity | COMPUTED only (K4) | Far from the source the solution goes to AQUAL: u → √(a₀g_N) (0.982 at 30 max(r_M, L★²/r_M)), P ∝ 1/r and Φ ∝ ln r. So P ∉ L², and the bounded-domain proof does not cover infinite volume. Doubling the domain changes the inner solution by ≤ 1.4e-6. The theorem on infinite volume is **OPEN**. |
| Spherical cases (K4) | COMPUTED | r_M/L★ = 0.3 (screened): from two guesses the solution is the same to 9e-14. u(0.01 L★) = 0.0898 against GM/L★² = 0.09 (A22's hedgehog a_P). r_M/L★ = 3: the core is unscreened (u → a₀; GM/L★² = 9a₀ would exceed the cap); unique to 4e-15. |
| 3D, two unequal masses (K5) | COMPUTED | 26³ grid, L-BFGS. Two guesses (zero, random) agree to 3.7e-8 (∇Φ) and 1.4e-7 (P). Max u/a₀ = 0.40, so the convex extension above 0.99a₀ is inactive. |
| Time dependence | DERIVED (K6, by construction) | At β = η = 0 the action has no Ṅ and no Ṗ, so their momenta vanish. The leaf problem at each τ is **exactly** the static one with the instantaneous sources; the result does not rely on a slow-motion approximation. |

**Not covered (OPEN):**
- strong-field leaves (NS compactness);
- local well-posedness of the coupled system: GR's hyperbolic tensor sector + these leaf constraints + K(Q) dust
  transport, including dust caustics and BS's statement that the ω = 0 mode propagates at nonlinear order;
- the K(Q) term, dropped here because μ_K²r² ≪ 1.

## 2. Observables of instantaneous response

**Binary pulsars (K7).**
- **No radiative channel.** At β = η = 0 there is no propagating non-tensor mode (C5 DOF table). The leaf equations
  have no ∂_t and are T-even. So the force they mediate is −∂E_min/∂x_i of the instantaneous configuration (envelope
  theorem on the convex minimum), and its work per orbit is zero.
  - So there is no monopole or dipole radiation and no extra radiation reaction. The tensor sector is exactly GR's
    (β = 0), so the quadrupole formula is unchanged.
- **Conservative correction.** Inside the screening length, each body's P hedgehog pulls the other with GM/L★²,
  independent of distance. The fractional change in the orbit, and so in the inferred masses and Ṗ_b, is
  ε = (a/L★)². Its nonlinear part is ε·(GM/L★²)/a₀.

| system | a (m) | ε (L★ = 20 / 24 / 90 pc) | Ṗ_b precision (record) | ε / precision (worst) |
|---|---|---|---|---|
| J0737−3039A/B | 8.79e8 | 2.0e-18 / 1.4e-18 / 1.0e-19 | 6.3e-5 (Kramer+2021) | 3.2e-14 |
| B1913+16 | 1.95e9 | 1.0e-17 / 6.9e-18 / 4.9e-19 | 1.6e-3 (Weisberg & Huang 2016) | 6.2e-15 |
| J1738+0333 (dipole test) | 1.73e9 | 7.9e-18 / 5.5e-18 / 3.9e-19 | 0.116 (Freire+2012) | 6.8e-17 |

- The nonlinear piece is 9.4e-24 (canonical) and 7.8e-24 (alt) for J0737 at L★ = 24 pc.
- The Galactic P background is uniform across the binary, so it cancels in the relative orbit.
- Consistent with A82: α̂₁(internal) = 3.0e-24 against 3.5e-5.

**Preferred frame (K8): a new item, and a correction to A22 D5.**
- A field that solves a ∂_t-free equation on the khronon's leaves, sourced by a body moving at w, is f(x′_∥/γ_w, x′_⊥)
  in the body's frame. In that frame the leaf is tilted: its metric along w is 1 − w² (sympy).
- For A22's P potential Φ_c = (GM/L★²)r this gives a **(w·n̂)² anisotropy with coefficient −½**.
  A22 D5 (`deepseek_push/DS_FINAL_2026_10_21/A22_ppn_frames/report.md` L121–127) says the only frame dependence is the
  isotropic factor (1 + 2w²). That misses the leaf tilt.
- It is not a PPN (U-type) term, so A22's α₁ = α₂ = 0 at PPN order stands.
- Size:
  - The α₂-equivalent is (r/L★)² = 4.1e-14 at 1 AU (L★ = 24 pc), which is 1.7e-7 of |α₂| < 2.4e-7.
  - At a neutron-star radius it is 2.6e-28, which is 1.6e-19 of |α̂₂| < 1.6e-9.
  - δa_P = (w²/2)·a_P = 1.8e-22 m/s² for the Sun (w = 369 km/s).
- Consistent with A82's conclusion: the galactic α₁ is bounded, there is no dipole, and the effect is unobservable.

**Light deflection versus dynamics (K10, estimate).**
- Φ = ψ at O(ρ) also when the source varies in time: P's anisotropic stress is O(ρ²) (A22 D3), and the GR traceless
  equation gives no slip. So lensing and dynamics see the same instantaneous potential.
- An instantaneous response and a hypothetical retarded one differ only at O(v²/c², a r/c²):
  - Jupiter-type deflection tests: the P part itself is 9e-21 of the deflection;
  - a merging cluster (illustrative v = 3000 km/s, r = 1 Mpc, t = 0.3 Gyr): about 1e-4.
- No lensing bound at that level was identified. Not scored.

**GW170817 (K9).**
- The tensor principal speed is exactly 1: the K_ijK^ij coefficient is 1 and β = 0 (C5 H1). The P sector has no
  derivative coupling to h_TT at quadratic order (TT gauge).
- Its only effect is a mass from W and the clock term (sympy):
  m₊² = −2K²P₀²a₀²/(K|P₀| − a₀)² − 4KP₀g_b + … ≲ 5e-43 m⁻², even with g_b = 9.81 m/s².
- At 100 Hz this gives Δv/c ≤ 6.2e-32 (alt) and 5.1e-32 (canonical), against the bound of 1e-15. Confirmed: no
  constraint.

## 3. Logical status: what "fails criterion A" means here

- **What is instantaneous.** The lapse of the khronon foliation (A_i = ∂_i ln N) and P are fixed on each τ-leaf by the
  elliptic problem above. Only the two tensor modes propagate, at c. The K(Q) dust is transported along n, with
  c_s² = (Q−1)/Q < 1 (C5).
- **Why this is not GR's harmless kind of constraint.**
  - In GR the Hamiltonian and momentum constraints are also elliptic, and in some slicings so is the lapse. But
    there the slicing is a gauge choice. The constrained quantities are tied to locally conserved charges. And
    gauge-invariant curvature obeys hyperbolic equations, so no observable changes outside the light cone.
  - Here τ is a field. The cones and the leaf-elliptic factor are posed on its leaves, and with respect to any other
    slicing the elliptic factor has non-real roots (CFG292 T7). So no choice of gauge makes the response retarded.
  - The P-sector force on a test body is observable. When a source moves, the P force at distance r changes in the
    same instant of τ.
- **This is the khronometric / Hořava structure.** The record (CFG292) identified the bare k² factor as the
  leaf-elliptic mode.
  - The literature consequence usually quoted is the universal horizon (Blas & Sibiryakov 2011, PRD 84 124043). It is
    cited in the record (`opus_48_extended_research/papers/A_GUIDE_FOR_COSMOLOGISTS.md` L647) but **not verified here**.
- **Criterion A vs B.**
  - **Criterion B (global time, nothing backward in τ, no closed signal loops): satisfied.** Every influence goes
    forward in τ or stays within a leaf, so a causal paradox needs a second preferred time, and the theory has only one.
  - **Criterion A (no influence faster than c): violated in principle, as a real signal and not a gauge artefact.**
  - The size of the signal is the honest qualifier. Moving 1000 kg by 1 m changes the P force 1 km away by
    (Gm/L★²)(Δx/r) = 1.2e-46 m/s² (L★ = 24 pc; 1.8e-46 at 20 pc, 8.7e-48 at 90 pc).
  - Astrophysical cases reach O(1) of the MOND force but change only on dynamical times. The instantaneous–retarded
    difference is then ≤ 1e-4 (K10).
- **Summary.** The theory's departure from relativistic causality is real and permanent. It is not detectable with any
  test identified here.

## Run history (kept)

1. **Run 1** (`*_RUN1.*`): 6/8, exit 1.
   - K1 FAIL by float64 rounding: the bound held to 5e-9 relative at |ξ|L★ = 1e4, against the frozen 1e-10.
   - K4 FAIL: scipy `solve_bvp` hit max_nodes (status 1) in every case.
   - That run peaked at **2.3 GB RSS, over the 1 GB budget** (solve_bvp's collocation arrays). Disclosed.
2. **Fixes made afterwards.** No pass line changed.
   - K1's eigenvalues are now computed in mpmath at 50 digits.
   - K4 is now the minimiser of the spherical reduced functional. Φ is eliminated exactly by Gauss; the Euler–Lagrange
     equation is identical to the frozen ODE. The solver is L-BFGS on artanh(P) followed by Newton.
   - Development runs (printed, not kept) found three solver defects:
     - a truncated-grid natural condition ψ(r_min) = 0 that drove u to the cap. Fixed by a regular [0, r₀] cell plus
       the inner-ball load.
     - r_min = 1e-5, where 1 − u ≈ 1e-11 in the unscreened core is below float resolution. Changed to 1e-4.
     - a Newton-only stall from the flat guess (rel. |∇E| 0.88).
   - These were solver defects, not second solutions. The discrete functional is strictly convex.
3. **A reading made after freezing.** For r_M/L★ = 3, K4(iii)'s hedgehog limit is not applicable, because GM/L★² = 9a₀
   exceeds the cap. The test used there is "u < a₀ in the core". This was coded before run 1.

## Input ledger

| input | class | source |
|---|---|---|
| C4-literal action, W, γ_L = KL★²/2, ξ = 1 | FRAMEWORK-NATIVE | C4 README, C5 script, A33 via A22 D1 |
| L★ = 20 / 24 / 90 pc; a₀ footings | FRAMEWORK-NATIVE / FITTED (κ = ½) | C5, doors BRIEF |
| C5 DOF table, tensor ω² = k², dust c_s² | FRAMEWORK-NATIVE (computed) | `../C5_health/README.md` |
| P stress O(ρ²), hedgehog a_P = GM/L★² | FRAMEWORK-NATIVE (computed) | A22 D3, D4 |
| Ṗ_b ratios: Kramer+2021 0.999963(63); Weisberg & Huang 2016 0.9983(16); Freire+2012 −25.9(32)e-15 vs −27.7e-15 | RAW-derived, **record transcription, not re-verified (no download)** | `real_research/reviews/mi_pulsar_pta_precision_ledger_2026.py` L180–189 |
| pulsar P_b, M_tot | same | same |
| \|α₂\| < 2.4e-7 (Nordtvedt 1987, secondary); \|α̂₂\| < 1.6e-9 (Shao+2013) | record transcription | `data_assembly/DOOR11_LITERATURE_2026-09-29.md` L35, L39 |
| \|c_T − 1\| < 1e-15 | record transcription | `EMPIRICAL_TESTS.md` A6 |
| NS radius 12 km, cluster v/r/t, lab 1000 kg / 1 m / 1 km | ILLUSTRATIVE | — |

No ΛCDM or standard-MOND machinery enters a verdict. AQUAL appears only as the theory's own far-field limit.

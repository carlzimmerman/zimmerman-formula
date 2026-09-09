# L83 — Near-horizon health of the F(Q)Θ scalar-metric strong coupling

**Question (astra's one open concern).** astra's ADM principal gate
(`qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/ACTUAL_PRINCIPAL_GATE.md`) found that the
reduced scalar–metric symplectic form of the F(Q)Θ clock-dust candidate,

    Ω_{ζπ} = (U_nz / Q₀) k²      with   U_nz = −4M²,

**collapses as k → 0**, and that the longitudinal constitutive stiffness
`U_ππ = 2M² G''(y₀)` with `G(y) = y² + 2(1+y)e^{−y} − 2` obeys `G''(y) → 0` as `y → 0⁺`. Because Ω ∝ k²,
the degeneration is worst at the **largest scales**. L83 decides whether that reaches **observable
(sub-horizon)** scales — which would be **fatal** for the CMB — or is confined to super-horizon scales
where the curvature perturbation ζ is causally frozen — **benign**.

**Verdict: BENIGN for the CMB acoustic physics; UNDECIDED (but plausibly benign) for the lowest multipoles.**
Script `L83_near_horizon_health.py`, 18/18 checks PASS, output `L83_near_horizon_health.out`.

## The four load-bearing facts

1. **The degeneration is confined to super-horizon scales.** Ω(k) ∝ k² is strictly monotone, so it is
   worst at k → 0 and improves toward smaller scales. Every *observable* comoving mode has k ≥ k_H0
   (the present horizon); there is no interior worst-case in the observable band. Sub-horizon scales are
   far from the degenerate point: relative to the present-horizon mode, Ω is enhanced **454×** at the
   recombination horizon and **≈5400×** at the first acoustic peak. The scales the CMB actually measures
   are nowhere near the collapse.

2. **The degeneration is not paired with any instability.** astra flagged an exponential instability *if*
   `U_ππ U_zz < 0`. For the exact exponential G, `G''(y) = 2[1 + (y−1)e^{−y}] ≥ 0` for all y ≥ 0 (min 0 at
   y=0, → 2 as y → ∞; verified symbolically and numerically). With `U_zz = 4M² > 0` the product is ≥ 0
   always, so `λ² ≤ 0` — the mode oscillates (gap) or is marginal (y₀=0), **never exponentially unstable**.
   The fatal branch astra left open is empty for this G.

3. **The classical EOM frequency is k-regular.** Both Ω and the reduced Hamiltonian scale as k², so the k²
   cancels in Hamilton's equations: `ω² = U_ππ U_zz / Ω₀²`, independent of k (reproduces astra's
   k-independent characteristic polynomial `λ² + Q₀² U_ππ U_zz / U_nz² = 0`). The symplectic collapse
   carries no small-k classical pathology.

4. **The ζ-conservation shield.** On super-horizon scales, `ζ̇ = −(H/(ρ+p)) δp_nad + O((k/aH)²)`. The L82
   Noether dust is adiabatic (w=0, c_s²=0 ⟹ δp_nad = 0), so ζ̇ → 0 as k/aH → 0, **independently of the
   scalar π's kinetic/symplectic microdynamics**. Moreover ζ is carried by the healthy Einstein sector
   (M²R gives ζ a standard quadratic kinetic term; the MOND operator is cubic — L82 — so it does not touch
   ζ's quadratic action). The degenerate degree of freedom is the *extra* scalar π, which is sequestered
   from CMB observables super-horizon, exactly as in ghost-condensate / khronometric EFTs.

An important reconciliation: the cosmological background *is* astra's zero-field point. y = |V|/a₀ with V
the spatial gradient of φ; on homogeneous FLRW V = 0 so y₀ = 0 exactly, giving G''(0)=0 and U_ππ=0. There
the reduced characteristic polynomial is λ²=0 — a **marginal, positive-kinetic, c_s²=0 mode**, i.e. exactly
the pressureless dust of L82 (grows as δ∝a by gravitational coupling), not a tachyon.

## Key numbers (Planck ΛCDM background; footing-independent)

| quantity | value | note |
|---|---|---|
| present horizon k_H0 | 2.25×10⁻⁴ /Mpc | c/H₀ = 4448 Mpc |
| recombination horizon k_Hrec | 4.79×10⁻³ /Mpc | k_Hrec/k_H0 = 21.3 |
| first acoustic peak k_peak | 1.65×10⁻² /Mpc | ℓ₁≈229, deep sub-horizon |
| a₀ scale (canonical 9.3619e-11) | 3.21×10⁻⁵ /Mpc | k_a0/k_H0 = 0.143 (super-horizon) |
| a₀ scale (alternate 1.1279e-10) | 3.87×10⁻⁵ /Mpc | k_a0/k_H0 = 0.172 (super-horizon) |
| Ω enhancement | 454× (recomb), 5386× (peak) | vs present horizon |

**Both a₀ footings** enter through the framework's own scale: k_a0 = a₀/c² ≈ k_H0/(2π) < k_H0, so the MOND/a₀
scale is itself super-horizon today — it lands in the benign band regardless of footing.

## Honest residual (the genuine open edge — not asserted as PASS)

- The ζ-conservation shield needs the **full** perturbation to be adiabatic. L82 shows the Noether *dust
  alone* is adiabatic. But the complete theory also carries the khronon/aether nᵘ; a relative
  (isocurvature) mode between the khronon sector and the dust could in principle source ζ super-horizon and
  re-expose the small-Ω band at low ℓ. Proving full-system adiabaticity is astra's next unavoidable
  calculation (khronon+scalar+dust ADM on an expanding branch) and is **out of this lane** — recorded as
  UNDECIDED for the lowest multipoles.
- The **absolute** strong-coupling cutoff on the marginal (present-horizon) modes needs the cubic/quartic
  interaction coefficients and the EFT scale M; only the quadratic (kinetic/symplectic) structure is in
  hand. This lane establishes *relative* benignity + super-horizon confinement + the causal shield, which
  is what decides the acoustic physics; the absolute low-ℓ cutoff is not computed here.

**Confidence:** HIGH that the CMB acoustic peaks are unaffected; MODERATE that the lowest multipoles are
safe (pending full-system adiabaticity). This does **not** clear the candidate — the khronon/aether,
vector/tensor principal symbols, and PPN gates astra lists remain decisive.

## Reproduce

```sh
python3 -B fable_independent_2026/L83_near_horizon_health.py
```
Self-contained (sympy + numpy); imports nothing from `qwen_claude_field_theory` (astra's Ω∝k², the
characteristic polynomial, and G'' are reproduced here independently).

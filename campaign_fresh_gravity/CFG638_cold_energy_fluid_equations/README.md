# CFG638: the cold-energy fluid equations (moments of the record's kinetic settling law)

**Bottom line.** The record's settling dynamics (CFG541 E3 drift + CFG544 FIX-2 velocity relaxation, CFG554 momentum-conserving
form) are written as a closed fluid system and checked in sympy. The pressure equation has the causal Israel–Stewart
(Maxwell–Cattaneo) form with relaxation time τ_ff/2α. Navier–Stokes is only its α ≫ 1 limit, and the causality bound α ≲ 1
(CFG542) keeps the cold energy at Knudsen ≈ 0.35/α, so the pressure-tensor system is the faithful closure. In a halo the cold
energy is a very viscous, laminar fluid (Re = 4α). The settled end state does not depend on α or the viscosity (CFG541 V4), so
these equations set **timing** (mergers, young systems) and not the profile that the shear test (CFG596, CFG636) scores.

κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled; none of the checks below uses a footing. The cold
energy's mass is required. No particle species. Not "theory closed". Nothing here says the data favour the framework.

- **Kind of lane:** derivation (identities and limits). No frozen criteria file: every check is an algebraic identity or a
  stated limit, not a gate against data. **Disclosure:** the script was written and run in a scratchpad first (2026-10-12),
  one sympy-integration failure was fixed (below), and it was then copied here and re-run unchanged in content.
- **Script:** `cfg638.py`. Run `OMP_NUM_THREADS=1 nice -n 10 python3 cfg638.py`: a few minutes, one process, < 1 GB, exit 0,
  11/11 PASS → `cfg638.out`, `cfg638_results.json`. `CFG638_MUTATE=1` (relaxation rate 2γ → 3γ, sink sign flipped): K2_pressure
  and K3_energy FAIL, exit 1 as designed → `cfg638_MUTATE.out`, `cfg638_results_MUTATE.json`.
- Nothing downloaded; no other lane touched.

## The system (inside B∩C; outside, v_s = 0 and γ = 0: pressureless Euler, ordinary cold matter)

Kinetic form: ∂ₜf + ∇ₓ·[(v + v_s)f] − ∇Φ·∇ᵥf = γ∇ᵥ·[(v − u)f + σ_J²∇ᵥf], with γ = α/τ, τ = (4πGρ_m)^(−1/2),
v_s = −α 1_B 1_C τ∇ψ, ∇²ψ = 4πG(ρ_ph − ρ_c) (FIX-1 two-sided deficit), ∇²Φ = 4πG(ρ_b + ρ_c).

| equation | form | check |
|---|---|---|
| mass | ∂ₜρ_c + ∇·[ρ_c(u + v_s)] = 0 | K2 PASS (exact) |
| momentum | ∂ₜ(ρ_c u) + ∇·[ρ_c(u + v_s)⊗u + Π] = −ρ_c∇Φ | K2 PASS |
| pressure | ∂ₜΠ_ij + ∇_k[(u+v_s)_kΠ_ij] + Π_ik∂_k u_j + Π_jk∂_k u_i + ∇_k Q_ijk = −(2α/τ)(Π_ij − ρ_cσ_J²δ_ij); no compression by v_s | K2 PASS (1-D Gaussian); K1: the 2γ and 3γ rates are exact for any f |
| energy | ∂ₜE + ∇·F = ρ_c v_s·∇Φ + (α/τ)(3ρ_cσ_J² − tr Π) | K3 PASS (1-D, fixed external Φ). The first term is −Q (CFG542's sink to dark energy), the second the bath exchange; both signs occur (CFG544) |

**Chapman–Enskog (K4):** η = pτ/2α, ζ = pτ/3α (non-zero because σ_J² is a bath target, not set by energy conservation),
q = −(5/6)(pτ/α)∇σ². No constant beyond α.

**Characteristics (K5):** u, u ± √3σ (10-moment Gaussian closure, drift off): hyperbolic, ≪ c. The only parabolic (acausal)
piece is the drift; CFG541 C2's damped ψ wave is the causal completion on record.

**Linear stability (K6),** uniform bound region, ρ_ph held fixed, two-sided deficit, units ω_J = √(4πGρ_c):
- the drift is a k-independent damping Γ = α(ρ_c/ρ_m)√(4πGρ_m) (= CFG541 A0);
- at k = 0.25 k_J the growth rate falls from 0.89 ω_J (α = 0.03) to 0.65 / 0.58 / 0.56 ω_J (α = 1; ρ_c/ρ_m = 0.5 / 0.84 / 0.95).
  The drift slows Jeans clumping of cold energy inside bound regions by about a third at α = 1; it does not stop it.
  Linear cosmic growth (outside B) is untouched.

**Halo scales (K7),** singular isothermal sphere: τ_ff = r/V exactly, τ_π = r/(2αV), ν = η/ρ = Vr/(4α),
**Kn = √2/(4α), Re = 4α**, independent of radius.

| α | Kn | Re | regime |
|---|---|---|---|
| 0.03 | 11.8 | 0.12 | collisionless (CFG623's merger side) |
| 0.5 | 0.71 | 2.0 | transitional |
| 1 | 0.35 | 4.0 | viscous fluid, Navier–Stokes marginal |
| 1.186 (causality max, q = 1 − f_b) | 0.30 | 4.7 | viscous fluid |

## Reading

1. **One α sets both the settling mobility and the viscosity.** The merger–galaxy α tension (CFG623: mergers allow only α = 0;
   galaxies want α ≳ 0.5) is, in fluid language, "collisionless in mergers, fluid in galaxies". A constant α cannot do both.
2. **The equations set timing, not the end state.** Stationary states are mobility-independent (CFG541 V4), and the velocity part
   relaxes to Jeans support of the same density. Viscosity or α therefore cannot fix or cause the CFG596 shear exclusion; that
   is the profile/source question (CFG636, CFG637).
3. **Still open (unchanged):** α free; switch and catchment inputs; σ_J² POSITED (CFG554/558; CFG620 F(E,L) derived candidate);
   overfill not handled; full-system Lyapunov not established; cluster drift speeds 4–5% c (CFG541 C1).
4. **Next test:** CFG639, the deficit-gated mobility (drift and relaxation only where d > 0), which would make settled halos
   collisionless during a merger while galaxies still settle.

## Corrections and disclosures (2026-10-12)

- **Correction 1 (implementation, before any reading).** The first run checked the moment equations by integrating sympy
  `Function` objects; those integrals did not simplify and K2 reported FAIL for all three equations. Redone with explicit chain
  rule (symbols for values and derivatives), the residuals are exactly 0. A separate scratch check (`k2_check.py`, not kept)
  showed the same before the fix was put in the script.
- K6 uses the two-sided deficit with ρ_ph fixed. With the one-sided rule, underdensities are damped and overdensities are not.
- K4's coefficients follow from K1's exact rates by the standard Chapman–Enskog step; the step itself is written out in the
  script's comments, not re-derived symbolically.

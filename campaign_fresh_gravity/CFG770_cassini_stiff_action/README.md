# CFG770: Cassini Q2 for the framework's own one-field action (stiffness on, no basin rule)

**Label: PASS.**
- Q2 is at most 3.5e-6 of the Park et al. (2026) 2σ ceiling: all 3 Galactic fields × both footings, at the window floor
  L* = 5.75 pc.
- The planetary gates pass. The Saturn monopole is at 0.966 of its bound. That gate is what sets L*'s floor (CFG691), so
  it is tight by construction.
- Without stiffness the action fails by 2557× (canonical) / 3091× (alt) from its a₀ tail at 1 AU.

**The stiffness constant is load-bearing.**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (4d35ef158). Block CFG770–779.
- **Script:** `python3 cfg770.py` (seconds, exit 0). MUTATE runs:
  - `CFG770_MUTATE=M1`: stiffness off. T1 and T3 FAIL.
  - `CFG770_MUTATE=M2`: KP term dropped. Q2 ≡ 0.
  - Both exit 1, as designed.

## What was computed
- **The action.**
  L = −|∇Φ − KP|²/2K − ρΦ − W_rem(u) − (γ/2)|∇P|², with R(u) = K W_rem′ = u²/(a₀ − u) and Λ² = γ/K.
- **The Galaxy's background at the Sun.** It comes from the action's own static solution. Its linear response tensor is
  A∥ = R′(u_e) = 6.7–13.6 and A⊥ = R/u = 1.8–2.8.
- **The Sun's perturbation.** It is solved exactly in Fourier space. No basin rule is used.

## Results

| check | result |
|---|---|
| K3 sympy | ∂F/∂P = K diag(R/u, R/u, R′), exact |
| K1 | the background-free pull is GM/L*² to 2e-8, so L*² = 2Λ² |
| K2 | an isotropic background gives Q2 = −1.9e-44, against 1.6e-32 anisotropic |
| K4 | K\|p\|/u_e ≤ 6.6e-5: linear response is valid |
| **T1** | \|Q2\|/ceiling = 2.2–3.5 × 10⁻⁶ (Q2 = −1.1 to −1.8 × 10⁻³² s⁻²). **PASS** |
| T2 | Q2 ∝ L*⁻³: 5.8e-13 of the ceiling at L* = 1 kpc |
| **T3** | sunward pull at 1 AU = 4.22e-15 (0.115 of the bound); Saturn monopole 0.966 of its bound. **PASS** |
| T4 (reported) | Galactic boost at the Sun g_e/g_Ne = 1.35–1.57 |
| C0 (control) | γ = 0: a₀ tail at 1 AU = 2557× / 3091× the bound. FAIL, as expected |

## Reading
1. **The stiffness breaks classical MOND's lock between the Sun's Galactic boost and Q2.**
   - In this action, the stiff P field cannot vary on scales below λ_e ≈ 2.1–2.4 pc.
   - The Sun's whole MOND region (about 0.03 pc) therefore sits inside one screening length, and its perturbation is
     Newtonian.
   - So Park et al.'s "≤ 2% boost at the Sun" inference does not apply here. The action keeps a 35–57% boost and still has
     Q2 about 10⁻⁶ of the ceiling.
2. **This is not unique to the framework.** Any screening length ≳ 0.03 pc does the same. The record's coherence-filter
   chassis also passes (F34/F37).
3. **The price.** The Solar System is fully Newtonian, apart from a constant 4.2e-15 m s⁻² sunward pull. That pull sits at
   97% of the Saturn ephemeris bound by construction of L*_min.
   - A modest tightening of Saturn's monopole bound would push L* up.
   - That stays allowed up to ≳ 1 kpc (CFG691).

## Disclosures
- **Run history.**
  - First run: K2 FAILED from roundoff. 1/S − 1 was formed by subtraction at large k (kept as
    `cfg770_firstrun_K2fail.out`). Its T1 numbers (1.2e-31) were wrong.
  - Fixed by computing 1 − S analytically. Second run: K2 failed only at the 1e-9 precision level (kept as
    `cfg770_secondrun_K2precision.out`).
  - Fixed by subtracting the exact c = 0 constant in each k-shell. No criterion changed.
  - The first MUTATE run combined M1 and M2 in one mode, so M2's zeroing masked M1. They were split into separate modes as
    the criteria list them; that output was deleted, not committed.
- **Scope.**
  - L* is the one extra constant (window 5.75 pc to ≥ 1 kpc), not derived.
  - The Galaxy's background is taken as uniform over λ_e.
  - Jupiter and the planets are not included (their share is 0.05% per Park et al.).
- κ fitted; cold energy mass required; not theory closed.

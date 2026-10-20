# p63: a₀ as a field. Can an identification or a quantisation fix k04's ratio Z/β²? NARROWED

**Verdict (frozen rules): NARROWED.** No candidate is FORCED-IN, so κ = ½ is not derived. **κ = ½ is FITTED.** Not theory
closed.

| candidate | result | class |
|---|---|---|
| C1, saturated dual polarisation (dark energy = cold energy's cosmic bound charge) | κ_Λ = 1.198 today (√(2π/3) = 1.447 in pure de Sitter); a₀ ∝ 1/H(z), so a₀(2.5)/a₀(0) = 0.27 (OTHER); the cosmic state sits at saturation, where W → +∞ | **INCONSISTENT** (premise gate fails) |
| C1b, patch bootstrap | Z = 1, κ_Λ = 2.894 (κ_crit 2.396); tracks √ρ_DE; finite W (u/a₀ = 0.5 at the patch edge) | **FORCED-OUT** (outside the window) |
| C2, flux lattice κ = κ₁/N | with κ₁ = 1, N = 2, 3 and 4 all land in the CFG493 window; null hit rate 0.71 | **MENU**: the lattice does not single out N = 2 |
| C3, Kaloper–Sorbo monodromy | quantisation fixes (f, μ, e) only; κ = √2 β/√Z keeps the free ratio; no ħ | **FREE** |

All four hand expectations disclosed before the freeze were reproduced. The window is CFG493's (erratum 2): κ_Λ ∈ [0.228, 0.606],
κ_crit ∈ [0.189, 0.502].

## Checks and MUTATE

- **Normal run:** 7/7 PASS (`p63_a0_field_coupling.out`).
  - K1 reproduces k04 F2 (Z/β² = 8 − 2b = 7.964).
  - K2 reproduces CFG695 (W → ∞ at u → a₀).
  - T4-C1: √(2π/3).
  - T4-C1b: Z(D) = (4−D)/(D−2).
  - W1: C1 OUT.
  - C2: hits [2, 3, 4].
  - H1: no ħ.
- **MUTATE run** (`MUTATE=1`, `p63_a0_field_coupling_MUTATE.out`): exactly the declared checks fail, and K1, K2 and T4-C1b
  still pass. Exit 1 by design.
  - T4-C1 under M1: κ halves to 0.724.
  - W1 under M2.
  - C2 under M2: hits [1, 2].
  - H1 under M3: ħ^½.

## Provenance

- Criteria: 2a36f4ae5, errata 5e5a10e33 and a1e430de1, and amendment 3 (run condition only).
- The script was written on 2026-10-19 by the session that froze this lane and is run unmodified.
- It was run on 2026-10-20 by a parallel session (the why_4_puzzle lanes) on the owner's instruction to swing every
  remaining κ lane. It ran beside the live NC2x under CFG894 §11: one core, 63 MB, 0.5 s.

    OMP_NUM_THREADS=1 nice -n 10 python3 p63_a0_field_coupling.py > p63_a0_field_coupling.out
    MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 p63_a0_field_coupling.py > p63_a0_field_coupling_MUTATE.out

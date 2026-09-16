# deepseek_moa/lean — toolchain and conventions

## How to compile (the repo's existing build, do NOT rebuild Mathlib)

    cd fable_independent_2026/lean_2026 && lake env lean <abs-path-to>/deepseek_moa/lean/M01_equipartition.lean

(Use the absolute path of the file; the Lean project root is
`fable_independent_2026/lean_2026`, which holds the built Mathlib `.lake`.)

- Toolchain verfied on this machine: Lake 5.0.0-src+6a10ac8, Lean 4.34.0-rc2,
  Mathlib pre-built (no rebuild). Exit 0 = clean.
- Axiom discipline: `#print axioms <thm>` must be subseteq
  {propext, Classical.choice, Quot.sound}. Zero `sorry`, zero `sorryAx`.
- Patterns proven in THIS Mathlib build (copy, don't improvise):
  - `glm53_push/lean/G031_fluid_action.lean` — key_sqrt_composition
    (Real.sqrt_mul hx _, Real.sqrt_mul_self), rho_L_from_a0
    (sq_sqrt + field_simp + linarith), the integral-form chain
    (intervalIntegral.integral_congr_ae, intervalIntegral.integral_const).
  - `glm53_push/lean/G058_omega_from_a0.lean` — omega_from_a0_gen
    (field_simp + ring), the interval theorem with Real.pi_gt_d6/pi_lt_d4.
  - THEME: avoid nested-sqrt nlinarith at all costs; use
    `set u := Real.sqrt (...)` then `Real.sq_sqrt` / `Real.mul_self_sqrt`,
    `field_simp`, `ring`.
- Three-strike rule: any theorem not closed in 3 attempts is DROPPED with the
  exact Mathlib blocker named in a comment. Never commit a struggling proof.
- Every certificate: header docstring with the physical statement, the
  registered lane(s), and the honest scope.
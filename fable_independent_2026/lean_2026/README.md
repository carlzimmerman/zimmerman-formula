# Lean 4 formalization of the F(Q)Θ MOND-completion lemmas

`Mondlean.lean` formalizes, in Lean 4 (toolchain `leanprover/lean4:v4.34.0-rc2`) against mathlib, the
load-bearing **mathematical** lemmas behind the de Sitter–MOND F(Q)Θ completion (lanes L80–L82; astra's
F(Q)Θ construction). It formalizes the mathematics, not the physics.

## Theorems

- `kernel_identity` — the exact-exponential primitive gives the MOND kernel: `Gp y / (2y) = 1 − exp(−y)`,
  where `Gp y = 2y(1 − exp(−y))`. (`Gp = dG/dy` is the symbolically verified derivative from L80/L82.)
- `Gpp_zero` — `G''(0) = 0`: the longitudinal stiffness vanishes at the zero-field point — astra's
  strong-coupling / loss-of-ellipticity obstruction, formalized.
- `Gpp_pos` — `∀ y > 0, G''(y) > 0`: a **stable massive scalar wherever the field is nonzero** (no ghost off
  the zero-field point). This is the exact health dichotomy astra's ADM principal gate found.
- `cubic_leading` — `G(0) = Gp(0) = Gpp(0) = 0`: G's Taylor expansion begins at the **cube**, which is why
  the MOND operator is cubic in the perturbation and drops from the quadratic cosmological action (L82),
  leaving standard gravity + a pressureless dust.
- `affine_degeneracy` — `K_QQ = 3 F_Q²/(2M²) ⟺ 2M²K_QQ − 3F_Q² = 0`: the cuscuton / det-W degeneracy.
- `sound_speed_zero` — gradient coefficient 0 with positive kinetic coefficient ⟹ `c_s² = 0` (the L82
  pressureless-clustering key).

## Build

```
lake exe cache get      # download prebuilt mathlib oleans
lake build Mondlean
```

## Status (2026-09-09) — GREEN, MACHINE-VERIFIED

`lake build Mondlean` compiles **clean (exit 0), zero `sorry`/`admit`**, and `#print axioms` shows every
theorem (`kernel_identity`, `Gpp_pos`, `Gpp_zero`, `cubic_leading`, `affine_degeneracy`, `sound_speed_zero`)
depends only on Lean's three standard foundational axioms `[propext, Classical.choice, Quot.sound]` — no
`sorryAx`. These are complete, sound, machine-checked proofs (Lean 4.34, mathlib).

Build environment note: the compile initially failed with `Too many open files in system` — NOT a proof
error but a saturated macOS **vnode cache** (`kern.num_vnodes == kern.maxvnodes == 263168`); importing
mathlib memory-maps thousands of distinct oleans at once. Fixed by raising it:
`sudo sysctl -w kern.maxvnodes=1000000`. After that the build is green.

These Lean statements formalize the *mathematics*; the physics computations they abstract are independently
verified by the committed sympy lanes (L77/L78/L80/L82 for the kernel, G'' sign, degeneracy and c_s²=0).

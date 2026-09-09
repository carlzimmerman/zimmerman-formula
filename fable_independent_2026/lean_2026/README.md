# Lean 4 formalization of the F(Q)Θ MOND-completion lemmas

> **Scope — what Lean certifies here.** Lean proves *mathematical theorems*, not physical laws. This file
> machine-checks the internal mathematics the F(Q)Θ theory rests on (kernel, health-sign dichotomy, the
> cuscuton degeneracy, the dust/stiff density structure, the MOND limits). Whether the theory is a *law of
> nature* is decided by its falsifiable predictions (dwarf σ–R_gc EFE, flat a₀(z), subdominant scalar GW)
> confronting data — not by Lean, and not while the intrinsic BBN fine-tuning (L84/L87) and astra's open
> ADM/khronon gates stand. A green Lean build guarantees the math is sound; it does not certify the physics.


`Mondlean.lean` formalizes, in Lean 4 (toolchain `leanprover/lean4:v4.34.0-rc2`) against mathlib, the
load-bearing **mathematical** lemmas behind the de Sitter–MOND F(Q)Θ completion (lanes L80–L82; astra's
F(Q)Θ construction). It formalizes the mathematics, not the physics.

## Theorems (all machine-verified: exit 0, zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound})

- `hasDerivAt_G`, `hasDerivAt_Gp` — **Gp = dG/dy and Gpp = d²G/dy² proven as derivatives** (not merely asserted).
- `kernel_identity` — the MOND kernel G'(y)/(2y) = 1 − e^{-y}.
- `Gpp_zero`, `Gpp_pos` — the **health dichotomy**: G''(0)=0 (zero-field obstruction), G''(y) > 0 ∀ y>0 (stable massive scalar, no ghost off zero field).
- `cubic_leading` — G(0)=G'(0)=G''(0)=0 ⇒ MOND term is cubic (drops from the linear cosmological action).
- `affine_degeneracy` — the cuscuton/det-W degeneracy K_QQ = 3F_Q²/(2M²) ⟺ 2M²K_QQ − 3F_Q² = 0.
- `density_affine` — the FLRW density = (Λ-const + back-reaction) + a⁻³ **DUST** cross term + a⁻⁶ **STIFF** term (the L84/L87 structure, an exact identity).
- `stiff_coeff_ne_zero` — the a⁻⁶ stiff coefficient −M²/(3f²) ≠ 0 for M,f ≠ 0 (the intrinsic BBN fine-tuning, L87).
- `sound_speed_zero` — c_s² = 0 (pressureless dust; the L82 clustering key).
- `mu_deep_slope` — deep-MOND: μ(η)=1−e^{-η} has slope 1 at η=0 (μ ≈ η).
- `mu_newton_limit` — EFE/strong-field: μ(η) → 1 as η → ∞ (Newtonisation; the L89 External Field Effect saturating to the GR/DM baseline).

## Build

```
lake exe cache get      # download prebuilt mathlib oleans
lake build Mondlean
```

## Status (2026-09-09) — GREEN, MACHINE-VERIFIED (12 theorems)

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

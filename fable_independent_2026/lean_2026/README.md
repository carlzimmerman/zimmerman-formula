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

- `mu_kernel_deriv`, `mu_kernel_deriv_pos` — the MOND kernel μ(y)=1−e^{-y} has μ'(y)=e^{-y} > 0 (strictly monotone).
- `closure_obstruction` — with A=1/μ, the cubic constraint-bracket coefficient (1/2)A A' = −μ'/(2μ³) (the L95 obstruction).
- `closure_needs_flat_kernel` — the obstruction vanishes iff μ'=0 (a flat, non-MOND kernel).
- `cuscuton_forced` — for the exponential kernel μ'≠0, so the obstruction is nonzero: a p²-kinetic MOND scalar cannot close the constraint algebra; the non-propagating **cuscuton** branch is forced (the machine-checked core of the L95 cuscuton-closure theorem, the *necessity*).
- `obstruction_coeff` — the constraint-bracket obstruction coefficient is (1/2)·A·A' in the p²-kinetic coefficient A.
- `cuscuton_obstruction_vanishes` — **L105 (sufficiency):** a cuscuton has A ≡ 0, so the obstruction (1/2)A A' vanishes **identically**, for any kernel slope.
- `cuscuton_closes_monotone` — **L105:** on the cuscuton branch the obstruction is 0 **and** the kernel stays strictly monotone (μ'=e^{-y}>0) — the two coexist, impossible in the canonical case (`closure_needs_flat_kernel`). This is the positive companion to `cuscuton_forced`: the cuscuton scalar sector escapes the L95 obstruction.
- `csSq_canonical`, `csSq_aqual` — **L106:** the k-essence sound speed of a power-law kinetic term is c_s²(n)=1/(2n−1); n=1 (canonical) is luminal (c_s²=1), n=3/2 (deep-MOND AQUAL, MOND in the kinetic term) gives c_s²=1/2 — a competing subluminal cone that corrupts the {H⊥,H⊥} structure function (the covariant root of L95 and the AeST/aether pathologies).
- `cuscuton_denom_zero` — **L106:** n=1/2 makes the denominator 2n−1 vanish, so c_s² diverges — the infinite-but-causal cuscuton sound speed (no finite competing cone).
- `cuscuton_unique_infinite` — **L106:** 2n−1=0 ⟺ n=1/2, so the cuscuton is the **unique** kinetic power with infinite sound speed; the MOND kernel, sitting in the gradient sector, never enters the causal structure ⇒ the metric-sector structure function stays h^{ij}. This extends the closure result from the scalar sector (L105) to the metric-sector structure function.
- `canonical_scalar_dof` / `cuscuton_scalar_dof` — **L108 (Dirac count):** dof = (P−2F−S)/2; a canonical scalar (phase dim 2, no constraints) has **1** propagating dof (a wave), a cuscuton scalar (second-class pair) has **0** — the machine-checked DOF face of L104/L105/L106.
- `cam_auxiliary_zero_dof` — **L108:** astra's CAM auxiliary sector at finite k (P=6, F=0, S=6) ⇒ **(6−0−6)/2 = 0** physical DOF — no propagating MOND scalar (the scalar-sector closure count). *Lean certifies the count; the constraint structure itself (6 second-class, PB rank 6) is astra's Dirac computation, and the full covariant τ-clock algebra + PPN remain open.*
- `fully_constrained_zero_dof` — general: a fully second-class-constrained sector (S=P, F=0) has 0 dof — the structural reason a cuscuton/constrained sector cannot propagate.
- `cam_total_linear_dof` — **L111:** the full linearized DOF = graviton (2) + CAM scalar (`diracDOF 6 0 6` = 0) = **2**, exactly GR — CAM propagates only the two graviton polarizations, no extra mode, no ghost. (The independent finite-k Dirac reconstruction — termination, rank-6 Poisson matrix, all second-class — is in `L111_independent_cam_dirac_closure.py`.)

## Build

```
lake exe cache get      # download prebuilt mathlib oleans
lake build Mondlean
```

## Status (2026-09-09) — GREEN, MACHINE-VERIFIED (29 theorems)

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

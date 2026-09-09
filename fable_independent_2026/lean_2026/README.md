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

## Status (2026-09-09) — HONEST

The proofs are written in standard mathlib idiom, and every mathlib lemma name used
(`Real.exp_pos`, `Real.exp_zero`, `Real.exp_add`, `Real.add_one_le_exp`, `mul_pos`, `mul_ne_zero`,
`two_ne_zero`, `pow_ne_zero`, `eq_div_iff`) and tactic (`field_simp`, `linear_combination`, `nlinarith`,
`linarith`, `ring`, `simp`) was checked to exist in the pinned mathlib. **They were NOT yet green-compiled**:
the compile was attempted on the host but blocked by a system-wide file-table overflow (macOS `ENFILE`) —
`import`-ing any mathlib file memory-maps ~1900 oleans at once, and the host's kernel file table was
saturated by other processes during this session (an environment limit; no proof error was reported —
every failure was `Too many open files in system`). Run the build above on a less-loaded machine (or after
raising `kern.maxfiles` / quieting Spotlight) to obtain the machine-checked certificate.

Until then, these Lean statements are a *specification*, and the underlying computations are independently
verified by the committed sympy lanes: the derivatives and c_s²=0 in `L80_verify_fqtheta_dust.py` /
`L82_final_gate_dust_clustering.py`, the G'' sign in `L77`/`L78`, and the affine degeneracy in `L80`.

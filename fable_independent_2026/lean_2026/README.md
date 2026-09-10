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
- `cam_auxiliary_zero_dof` — **L108:** the CAM **auxiliary sub-sector** (u,ℓ,Φ) at finite k (P=6,F=0,S=6) ⇒ (6−0−6)/2 = 0 DOF. ⚠️ **Scope corrected (astra 5943d5325 + L115):** this counts only that toy sub-sector; the full ADM additionally **retains a metric-scalar pair (ζ,p)** with a nonzero cubic Hamiltonian, so it does **not** certify the full CAM scalar DOF.
- `fully_constrained_zero_dof` — general: a fully second-class-constrained sector (S=P, F=0) has 0 dof — the structural reason a cuscuton/constrained sector cannot propagate.
- `cam_total_linear_dof` — arithmetic `2 + diracDOF 6 0 6 = 2`. ⚠️ **RETRACTED interpretation (astra 5943d5325 + L115):** originally read as "CAM full linearized DOF = 2 = GR", but that omitted the retained metric-scalar pair (ζ,p) the full ADM keeps (cubic Hamiltonian, health undetermined). Lean certifies only the arithmetic (2+0=2), **not** that CAM's full DOF equals GR's. The independent finite-k Dirac reconstruction (`L111`) is correct for the (u,ℓ,Φ) sub-sector only.

- `clock_structure_function` — **L117 (agent 1):** the cuscuton **clock** sector closes with the GR structure function γ^{xx} (crux identity (∂_pF²)(∂_sF²)/4F² = g p s) — the degree-1 clock kinetic term is **healthy**.
- `cam_conformal_ghost` — **L117 (agent 3):** because H_⊥ is second-class, the GR conformal mode ζ survives with kinetic term −3M²ζ̇²; its homogeneous Hamiltonian **H₀ = −p²/(12M²) < 0** — a **ghost** (unbounded below). The minimal CAM is **not** ghost-free.
- `cam_strong_coupling` — **L117 (agent 3):** the surviving mode's reduced quadratic Hamiltonian M²k²ζ²(1−η)/η **vanishes at η=1** (physical MOND value) ⇒ strong coupling around Minkowski.

- `reduction_master_certificate` — **L124 (capstone):** one theorem conjoining the load-bearing lemmas of the whole parameter-space reduction — health dichotomy, cubic MOND term, the propagating-scalar elimination, the cuscuton survival, transition-health (elliptic AQUAL), the BBN stiff horn, the lapse-sourced ghost, and ghost separability. ⚠️ **Scope:** certifies the *mathematics* of the reduction, **not** a complete physical theory — the honest verdict (L123) is that the viable all-gates theory is healthy MOND + a minimal decoupled dark sector, not pure MOND.

- `kessence_dust_stiff_decomposition` — **L137 (A1):** for a *quadratic* shift-symmetric k-essence K = −2Λ + K₂(Q−Q₀)² with charge dK/dQ = I₀/a³, the density is **exactly** 2Λ + Q₀I₀a⁻³ + [I₀²/(4K₂)]a⁻⁶ — dust **linear**, stiff **quadratic** in I₀ (the published AeST Higgs-phase background = the repo's L84/L87 structure). Scope: quadratic K only; L137 shows cosh/exp K have **no** a⁻⁶ partner (numerical, not certified here).
- `stiff_dust_coefficient_ratio`, `stiff_dust_term_ratio` — **L137 (A2/A3):** the stiff/dust coefficient ratio is I₀/(4K₂Q₀) (= published w₀ = the L84 BBN fine-tuning ratio, one object); the *term* ratio scales as a⁻³ (stiff dominates early).
- `stiff_dust_ratio_vanishes_iff` — **L137:** for quadratic K the ratio vanishes **iff** I₀ = 0 — quadratic K cannot carry dust without stiff (the part of L87 that survives).
- `lv_kessence_sound_speed_scaling`, `lv_kessence_sound_speed_increasing` — **L138 (B3):** for a Lorentz-violating k-essence c_s² = 2c_Y/K_QQ; with K_QQ = K_QQ⁰a⁻³ this is (2c_Y/K_QQ⁰)a³, **strictly increasing** in a (colder at recombination than today). The a⁻³ law for cosh/exp K is L138's numerical result, not certified.
- `particle_sound_speed_decreasing` — **L138 (B1, control):** a free-streaming particle has c_s² = v₀²/a², strictly **decreasing** — the opposite ordering, which is why the L125 velocity lemma is particle-specific, not mechanism-independent.
- `cuscuton_time_kinetic_affine` — **L139 (C2-1):** at zero spatial gradient √((1−2εΨ)(τ̄̇+εδτ̇)²) = √(1−2εΨ)(τ̄̇+εδτ̇) exactly — affine in δτ̇, so the (δτ̇)² coefficient vanishes identically (0-DOF from the action; companion to `cuscuton_stiff_denominator_zero`).
- `cuscuton_slaved_mode_identity` — **L139 (C2-3):** the elliptic constraint solution rewrites exactly as δτ = −(a²τ̄̇S/μ_c²)/(k² + V″a²τ̄̇/μ_c²): the 1/k² sub-horizon suppression is manifest, k²δτ → −a²τ̄̇S/μ_c² (Route 1 obstructed: background dust ≠ clustering dust).
- `cuscuton_elliptic_slaving` — **L139/L129:** (aH/k)⁴ < 1e-4 whenever k/(aH) > 10 (real-number inequality; the identification of the suppression ratio with (aH/k)⁴ is the scaling argument, not certified).
- `leaf_normal_no_frame_drag_source`, `leaf_normal_frame_drag_source_iff` — **L139 (C3-4):** the Route-2 momentum-constraint source −K_Q∂ᵢχ/N vanishes when ∂ᵢχ = 0, and for K_Q ≠ 0 **only** then — gradient-driven, no F² frame-drag term, so AeST's O(1) α₁ source is absent. Scope: the O(w) PPN solve is **not** done.
- `lapse_measured_charge_helmholtz`, `helmholtz_mass_cannot_be_switched_off` — **L139 (C3-8), the inherited cost:** K₂(Q₀(1−Ψ)−Q₀)² = K₂Q₀²Ψ² exactly (AeST's μ²Φ² Helmholtz term), and it is > 0 for K₂ > 0, Q₀, Ψ ≠ 0 — it cannot be switched off.
- `fourth_power_error_budget`, `fourth_power_velocity_binds`, `fourth_power_velocity_threshold` — **L143:** with log a₀ = 4 log v − log M_b and independent errors, σ² = 16σ²_logv + σ²_logM; σ_logv > 0.0335 dex alone exceeds the 0.134 dex budget, and 16·0.0335² = 0.134² exactly (the fourth power binds).

## Build

```
lake exe cache get      # download prebuilt mathlib oleans
lake build Mondlean
```

## Status (2026-09-10) — GREEN, MACHINE-VERIFIED (76 theorems)

`lake build Mondlean` compiles **clean (exit 0), zero `sorry`/`admit`**, and `#print axioms` shows every
theorem (`kernel_identity`, `Gpp_pos`, `Gpp_zero`, `cubic_leading`, `affine_degeneracy`, `sound_speed_zero`)
depends only on Lean's three standard foundational axioms `[propext, Classical.choice, Quot.sound]` — no
`sorryAx`. These are complete, sound, machine-checked proofs (Lean 4.34, mathlib).

> **Correction (2026-09-10, L115):** astra's physical-action audit (5943d5325) found the minimal CAM action has a **nonelliptic lapse for y>1** and a **retained metric-scalar canonical pair** with a nonzero cubic Hamiltonian — so CAM is **not** a complete gravity theory (Blanchet–Marsat khronometric class). The DOF-count theorems above are correct arithmetic for their stated sub-sectors, but do **not** certify full CAM closure. The lanes' CAM-full-DOF (L111), α₁-suppression (L112), and β=1 (L113) claims are retracted; see L115.
>
> **Fleet verdict (2026-09-10, L117, three independent agents + astra):** the cuscuton **clock** sector is healthy (closes with γ^{xx}), but the MOND acceleration operator makes H_⊥ second-class (khronometric) and **liberates the GR conformal mode as a ghost** (H₀=−p²/12M²<0) that is strongly coupled at η=1 — so the **minimal CAM does not close into a healthy, ghost-free theory**. Lean now certifies both the healthy clock identity and the fatal ghost. The obstruction is pinned to the acceleration operator; astra is pursuing curvature-clock / KGB alternatives.

Build environment note: the compile initially failed with `Too many open files in system` — NOT a proof
error but a saturated macOS **vnode cache** (`kern.num_vnodes == kern.maxvnodes == 263168`); importing
mathlib memory-maps thousands of distinct oleans at once. Fixed by raising it:
`sudo sysctl -w kern.maxvnodes=1000000`. After that the build is green.

These Lean statements formalize the *mathematics*; the physics computations they abstract are independently
verified by the committed sympy lanes (L77/L78/L80/L82 for the kernel, G'' sign, degeneracy and c_s²=0).

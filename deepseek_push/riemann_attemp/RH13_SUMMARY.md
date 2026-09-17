# RH13 -- THE DOUBLED COMPLETION: P_l(s) = Ξ(s)·B_l(s), TWO REFLECTION AXES, NO NEW ZERO CONTROL
(deepseek lane, subagent RH13, 2026-09-17)

**FILES: `RH13_doubled_completion.py` + `.out` + `_results.json` (mpmath, 30 digits, all checks PASS),
`lean/RH13L_doubled.lean` — exit 0, zero warnings, ZERO sorry, 17 theorems certified.**

## PRE-REGISTRATION (registered before any computation; outcomes below)
- **K1** = doubled-symmetry identities fail numerically → error in my algebra. → **NOT TRIGGERED**:
  AXIS A and AXIS B residuals ≤ 4e-31 at 30 digits (10 s-values × rungs l ∈ {2, 5/2, 3}); the
  Gamma-cancellation ratio residuals are exactly 0.0. (One numerical subtlety found and fixed
  honestly: with raw Python-float inputs the AXIS-B check picked up a 1-ulp double round-trip
  artifact `l-(l-s) ≠ s`; with exact decimal mpf inputs the residual is exactly 0 — verified at
  dps 30 and 80.)
- **K2** = the honest conclusion is that NO new zero control follows. → **CONFIRMED** (see dispatch).

## WHAT THE DOUBLED COMPLETION IS
- Completed zeta Ξ(s) = s(s−1)π^(−s/2)Γ(s/2)ζ(s), Ξ(s) = Ξ(1−s) (classical FE, sanity-checked numerically at 10 s-values, residual ≤ 3e-31).
- Ladder beta B_l(s) = B(s, l−s) = Γ(s)Γ(l−s)/Γ(l) = Mellin transform of (1+u)^(−l) (verified by quadrature at 12 points, rel. residual ≤ 1e-13; B positive/zero-free on (0,l)).
- P_l(s) = Ξ(s)·B_l(s).

**AXIS A (s → 1−s):** P_l(s) = P_l(1−s)·R_l(s), R_l(s) = B_l(s)/B_l(1−s) = Γ(s)Γ(l−s)/(Γ(1−s)Γ(l−1+s)) — the Γ(l) factors cancel (the certified algebraic core: `gamma_cancellation_ratio`). Certified in its sharpest honest form (`doubled_symmetry_axis12`): holds for **ANY** h with h(1−s)=h(s) — the Ξ/functional-equation factor cancels identically. Involution: R_l(s)·R_l(1−s) = 1.

**AXIS B (s → l−s):** P_l(s)·h(l−s) = P_l(l−s)·h(s) for **ANY** h (no FE needed; B cancels via beta symmetry B_l(s) = B_l(l−s), the kernel's own certified reflection). The two axes coincide exactly at the ladder edge l = 1.

Both identities verified at 10 s-values × 3 rungs at 30 digits (residuals ≤ 4e-31) and certified in Lean (exit 0, zero sorry) as generic h-statements.

## EULER-PRODUCT SIDE (part 1 of the delegation) — exact vs numeric, stated honestly
| statement | status |
|---|---|
| ln ∏_{p∈{2,3,5,7,11,13}}(1−1/p) = Σ_p ln(1−1/p) at σ=1, and ∏ = **192/1001** exactly | **EXACT — Lean-certified** (`log_product_six_primes`, `thirteen_prime_product_exact`) |
| Euler product ln ζ(s) = −Σ ln(1−p^−s) for Re s > 1 | classical, **numerically verified at σ=3/2** (the l=3 ladder axis, inside the convergence region): |ln ζ(3/2) − partial| = 5.7e-5 ≈ predicted tail 6.4e-5; also Σ ln(1+p^−s) = ln ζ(s) − ln ζ(2s) numerically |
| σ = 1/2 (framework edge axis): "= ln ζ(1/2)" | **NOT a real equality**: partial sums DIVERGE (Σ ln(1−p^−1/2) = −14.3, −30.9, −71.9, −321.9 at x = 1e3…4.2e6; +-variant diverges to +∞), and ζ(1/2) = −1.46035… < 0 so ln ζ(1/2) ∉ ℝ |
| σ = 1: "= ln(1/ζ(1))" | **divergence-to-divergence statement**, not an equality of reals: partial sums → −∞ (Mertens: ∏(1−1/p)·ln x → e^−γ = 0.561459, matched to 0.561441 at x=4.2e6), consistent with the pole of ζ at 1. The only exact content at σ=1 is the finite identity above |

## THE HONEST DISPATCH (part 3)
1. **Known zero-free/zero structure of P_l beyond Ξ's: NONE.** B_l is zero-free (Γ zero-free; real and positive on (0,l), min 0.393 on grid); B_l adds **poles** (s ∈ ℤ≤0 ∪ l+ℤ≥0), not zeros. Hence: zeros of P_l = zeros of Ξ (the zeta's trivial zeros at −2,−4,… and the nontrivial zeros), everywhere B_l is finite — verified at ρ₁, ρ₂ (|P_l(ρ)| ~ 1e-50).
2. **Does the doubled symmetry constrain the zeros? NO.** The only zero consequence of AXIS A — the pairing ρ ↔ 1−ρ — is the **classical functional-equation pairing already present in Ξ** (R_l(ρ) ≠ 0 away from the beta poles). Nothing new.
3. **Certified counterexample principle** (RH05L's (s−2)(s+1), extended *into the doubled class itself*): h0(s) = s(1−s) − 1/8 is 1−s-symmetric with roots a0 = (1+√(1/2))/2 ≈ 0.8536, b0 ≈ 0.1464 **off** the critical line; the completed product P_{h0,l} vanishes at both for every l and satisfies the doubled symmetry. All Lean-certified (`h0_root_a0/b0`, `a0_ne_half`, `doubled_class_zero_a0/b0`, `doubled_symmetry_holds_for_h0`, `doubled_class_off_axis_zeros`). Numeric check of P_{h0,3}(a0) = 1.6e-17.
4. **Bottom line: the framework's completed class produces a function with TWO reflection axes and NO new zero control.** The doubled symmetry is a tautology of the construction (any symmetric completion satisfies AXIS A; any completion satisfies AXIS B); the certified h0 member of the class carries its zeros off the axis; P_l's zeros are exactly Ξ's. This IS the deliverable.

## VERDICT
Targets 1–2 certified (finite Euler-log identity exact at σ=1 in Lean; both axes and the Γ-cancellation ratio certified in Lean, numerics at machine zero); target 3 dispatched honestly as a wall: **no zero control follows — no RH claim, in whole or in part.** K1 not triggered; K2 confirmed. Nothing committed.
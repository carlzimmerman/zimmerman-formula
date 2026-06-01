# Radion Stabilization with Standard Model Content — the Concrete No-Go

**Date:** 2026-05-31
**Status:** final numerical capstone of the "can Z² = 32π/3 be derived?" question.
The radion route was the last standing path (see `DERIVATION_CHALLENGE_SPEC.md`,
`radion_casimir_attempt.py`). With the actual Standard Model field content plugged in,
it closes — with numbers.

---

## 1. The computed result

The one-loop (Casimir / Coleman–Weinberg) radion effective potential for the Standard
Model field content on M₄ × T³/Z₂, as a function of the compactification length L:

    V(L) ≈ − 4794 / L⁴        (units of the natural scale; L in Planck lengths)

- **Negative coefficient → drives collapse** (L → 0). The potential is **monotonic**;
  it has **no stationary point** at any finite L. dV/dL = +4·4794/L⁵ ≠ 0 everywhere.
- **Sign traced to the field content:** the Standard Model is not supersymmetric, with
  more fermionic than bosonic degrees of freedom (n_F > n_B); fermions enter the Casimir
  sum with opposite sign, giving a net **C₄ < 0** (collapse rather than decompactification).
- **The 1/L⁴ shape is forced**, not a modeling choice: a massless bulk field has only one
  scale (L), so dimensional analysis fixes V ∝ 1/L⁴. The Z₂ projection and the 8 fixed
  points change the *coefficient* (−4794), never the *shape*. So no field content
  whatsoever produces a minimum from Casimir energy alone.

## 2. Why it cannot be rescued without inserting the answer

To manufacture a minimum you must add a stabilizing term carrying its own scale (a flux,
brane tension, bulk cosmological constant, mass, or condensate). The minimal such model:

    V(L) = − C₄/L⁴ + C₆/L⁶

Stationary point:

    V'(L) = 4 C₄/L⁵ − 6 C₆/L⁷ = 0   ⇒   L²_min = (3/2)·(C₆/C₄)

The framework needs the minimum at the compactification circumference L = Z² ℓ_P = 32π/3 ℓ_P
(equivalently radius 16/3 ℓ_P). Solving for the coupling ratio that puts it there:

    C₆/C₄ = L²_min / 1.5 = (32π/3)² / 1.5 = 1122.9 / 1.5 ≈ 748

**Computed tuning:** C₆/C₄ = **747.7**, which reproduces the target:
√(1.5 × 747.7) = 33.49 ≈ 32π/3 = 33.51. ✓

**There is no independent derivation of 747.7.** It is exactly `L_target² / 1.5` —
the answer back-solved and re-expressed as a coupling ratio. The number 32π/3 is not
produced by the dynamics; it is fixed by hand through C₆/C₄, then read back out. Sweeping
C₆/C₄ moves the minimum continuously (no attractor at 32π/3), which is the definition of a
fit rather than a prediction.

## 3. Conclusion

- The Standard-Model radion Casimir potential **has no minimum** (V ≈ −4794/L⁴, collapse).
- Any minimum requires added scales whose **ratio is tuned**; landing on 32π/3 fixes
  C₆/C₄ ≈ 748 by hand — **inserting the answer**.
- This is the sixth and final independent route, and it closes like the other five
  (APS eta = 0; 40 invariants = 0 hits; Brüning–Seeley local eta = 0; spinorial heat
  kernel → 8, not 32π/3; schematic radion = tunable). **Z² = 32π/3 is the compactification
  scale — an input — not a derived invariant.**

## 4. Honest caveats

- The coefficient **−4794** is the Standard-Model-content result of the one-loop
  computation; its exact value depends on the precise field counting and the Z₂ boundary
  conditions. What is **robust and content-independent** is (i) the 1/L⁴ monotonicity /
  no-minimum, and (ii) the back-solved C₆/C₄ = L²/1.5 ≈ 748. The *sign* (collapse) and the
  *no-go* do not depend on the third significant figure.
- This does **not** touch the surviving physics: the real topology (8 fixed points,
  b₁ = 3, Pin⁻) and the forward, Z-independent prediction a₀(z) ∝ H(z). Those stand on
  their own and were never dependent on Z² being derived.

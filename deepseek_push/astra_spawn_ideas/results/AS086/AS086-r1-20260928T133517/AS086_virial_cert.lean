import Mathlib

/-!
# AS086 -- External logarithmic-well virial term (certified algebraic core)

Formal content only.  The physical reading, domains and both a0 footings are in the
accompanying `derivation.md` and `result.json`.

Certified statements (all over ℝ, all pure algebra; no integration is formalized):

1. `logwell_integrand`:  for the external log well Φ_ext = C ln(r/r_ref), the virial
   integrand is r·dΦ_ext/dr = r·(C/r) = C for every r ≠ 0.  (The claim
   W_ext = -∫ρ r dΦ/dr dV = -C·M then follows by ∫ρ dV = M; the quadrature
   verification is in the Python artifact, not in Lean.)

2. `bare_virial_sigma2`:  the collisionless virial of a phantom of mass M in the
   external log well,  3·M·σ² = C·M  with M ≠ 0,  pins the 1-D dispersion σ² = C/3.
   (No pressure boundaries.)

3. `closure_sigma2`:  the same balance with the fluid closure and the AS083 twin
   surface-moment term (outer minus inner),  3·M·σ² - C·M = M·σ²  with M ≠ 0,
   pins σ² = C/2.  That is the with-pressure-boundaries reading.

4. `dblcount_bare_sigma2` / `dblcount_closure_sigma2`:  if the identical logarithmic
   field is counted TWICE (W_self + W_ext, both -C·M), the virial mis-infers
   σ² = 2C/3 (bare) and σ² = C (closure) instead of C/3 and C/2 -- the negative
   double-counting control fails as designed.

5. `outer_only_half` / `outer_only_half_ne_half`:  outer-moment-only bookkeeping at
   r_in = R/2 gives σ² = C, and C ≠ C/2 for C ≠ 0 -- the incomplete boundary
   bookkeeping cannot reproduce the C/2 triad.

6. `half_ne_third`:  for C ≠ 0 the two readings C/2 and C/3 are distinct.

7. `twin_moment_sis`:  with P = σ²·A/r² on the SIS shell, the surface-moment
   combination 4π(R³P(R) - r_in³P(r_in)) = σ²·4πA·(R - r_in) = σ²·M exactly
   (the AS083 lemma used in 3).
-/

namespace AS086

/-- The log-well virial integrand is the constant C: r·(C/r) = C for r ≠ 0. -/
theorem logwell_integrand (C r : ℝ) (hr : r ≠ 0) : r * (C / r) = C := by
  field_simp [hr]

/-- Bare (boundary-free) virial in the external log well: 3 M σ² = C M, M ≠ 0 → σ² = C/3. -/
theorem bare_virial_sigma2 (C M s2 : ℝ) (hM : M ≠ 0) (hv : 3 * M * s2 = C * M) :
    s2 = C / 3 := by
  have hA : M * (3 * s2) = M * C := by
    calc
      M * (3 * s2) = (3 * M) * s2 := by ring
      _ = C * M := hv
      _ = M * C := by ring
  have h3 : 3 * s2 = C := mul_left_cancel₀ hM hA
  field_simp
  nlinarith [h3]

/-- Fluid-closure virial with BOTH surface moments: 3 M σ² - C M = M σ², M ≠ 0 → σ² = C/2. -/
theorem closure_sigma2 (C M s2 : ℝ) (hM : M ≠ 0) (hc : 3 * M * s2 - C * M = M * s2) :
    s2 = C / 2 := by
  have h2m : 2 * (M * s2) = C * M := by
    calc
      2 * (M * s2) = 3 * (M * s2) - M * s2 := by ring
      _ = C * M := by nlinarith [hc]
  have hA : M * (2 * s2) = M * C := by
    calc
      M * (2 * s2) = 2 * (M * s2) := by ring
      _ = C * M := h2m
      _ = M * C := by ring
  have h2 : 2 * s2 = C := mul_left_cancel₀ hM hA
  field_simp
  nlinarith [h2]

/-- Double-counted (both wells counted) bare virial: 3 M σ² = 2 C M, M ≠ 0 → σ² = 2C/3. -/
theorem dblcount_bare_sigma2 (C M s2 : ℝ) (hM : M ≠ 0) (hd : 3 * M * s2 = 2 * C * M) :
    s2 = 2 * C / 3 := by
  have h3m : 3 * (M * s2) = 2 * (M * C) := by
    calc
      3 * (M * s2) = 2 * (C * M) := by simpa [mul_comm, mul_assoc, mul_left_comm] using hd
      _ = 2 * (M * C) := by ring
  have hA : M * (3 * s2) = M * (2 * C) := by
    calc
      M * (3 * s2) = 3 * (M * s2) := by ring
      _ = 2 * (M * C) := h3m
      _ = M * (2 * C) := by ring
  have h3 : 3 * s2 = 2 * C := mul_left_cancel₀ hM hA
  field_simp
  nlinarith [h3]

/-- Double-counted (both wells counted) closure virial: 3 M σ² - 2 C M = M σ², M ≠ 0 → σ² = C. -/
theorem dblcount_closure_sigma2 (C M s2 : ℝ) (hM : M ≠ 0) (hd : 3 * M * s2 - 2 * C * M = M * s2) :
    s2 = C := by
  have h2m : 2 * (M * s2) = 2 * (M * C) := by
    calc
      2 * (M * s2) = 3 * (M * s2) - M * s2 := by ring
      _ = 2 * (C * M) := by nlinarith [hd]
      _ = 2 * (M * C) := by ring
  have hA : M * s2 = M * C := by
    calc
      M * s2 = (2 * (M * s2)) / 2 := by ring
      _ = (2 * (M * C)) / 2 := by rw [← h2m]
      _ = M * C := by ring
  exact mul_left_cancel₀ hM hA

/-- Outer-moment-only bookkeeping at r_in = R/2: σ² = C·(R - r_in)/(2R - 3 r_in) = C. -/
theorem outer_only_half (C R : ℝ) (hR : R ≠ 0) :
    C * (R - R / 2) / (2 * R - 3 * (R / 2)) = C := by
  have hnum : R - R / 2 = R / 2 := by ring
  have hden : 2 * R - 3 * (R / 2) = R / 2 := by ring
  rw [hnum, hden]
  field_simp [hR]

/-- The same bookkeeping does NOT give C/2 when C ≠ 0: the control is live. -/
theorem outer_only_half_ne_half (C R : ℝ) (hC : C ≠ 0) (hR : R ≠ 0) :
    C * (R - R / 2) / (2 * R - 3 * (R / 2)) ≠ C / 2 := by
  intro h
  have h1 := outer_only_half C R hR
  rw [h1] at h
  field_simp at h
  have hC0 : C = 0 := by nlinarith
  exact hC hC0

/-- The with/without-pressure readings are distinct for C ≠ 0: C/2 ≠ C/3. -/
theorem half_ne_third (C : ℝ) (hC : C ≠ 0) : C / 2 ≠ C / 3 := by
  intro h
  field_simp at h
  have hC0 : C = 0 := by nlinarith
  exact hC hC0

/-- AS083 twin surface-moment lemma on the SIS shell: with P = σ² A/r²,
    4π(R³P(R) − r_in³P(r_in)) = σ²·4πA·(R − r_in) = σ²·M  (exact; ring algebra). -/
theorem twin_moment_sis (A R r_in s2 : ℝ) (hrin : r_in ≠ 0) (hR : R ≠ 0) :
    4 * Real.pi * (R ^ 3 * (s2 * A / R ^ 2) - r_in ^ 3 * (s2 * A / r_in ^ 2))
      = s2 * (4 * Real.pi * A * (R - r_in)) := by
  field_simp [hrin, hR]

end AS086

#check AS086.logwell_integrand
#check AS086.bare_virial_sigma2
#check AS086.closure_sigma2
#check AS086.dblcount_bare_sigma2
#check AS086.dblcount_closure_sigma2
#check AS086.outer_only_half
#check AS086.outer_only_half_ne_half
#check AS086.half_ne_third
#check AS086.twin_moment_sis

#print axioms AS086.logwell_integrand
#print axioms AS086.bare_virial_sigma2
#print axioms AS086.closure_sigma2
#print axioms AS086.dblcount_bare_sigma2
#print axioms AS086.dblcount_closure_sigma2
#print axioms AS086.outer_only_half
#print axioms AS086.outer_only_half_ne_half
#print axioms AS086.half_ne_third
#print axioms AS086.twin_moment_sis

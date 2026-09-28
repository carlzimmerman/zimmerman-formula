import Mathlib

/-!
# AS011 — Alternative footing as a separate hypothesis (certificate)

Framework base (adopted inputs, NOT derived here):
    a0 kappa c G rho  :=  kappa * c * sqrt(G * rho)     (rho : mass density, kg/m^3)
    kappa = 1/2 adopted for the canonical footing; G, c measured/fixed inputs.
    Canonical a0_c = 9.3619e-11 m/s^2; alternative a0_a = 1.1279e-10 m/s^2, a SEPARATE
    hypothesis (not an uncertainty band on one density). Both footings can never hold
    with one shared (kappa, rho) cell — the ratio (a0_a/a0_c)^2 = 1.45148716 is what a
    fixed-kappa comparison forces on the density; a fixed-density comparison instead
    forces the effective kappa shift kappa_a = a0_a/(2 a0_c).

What is certified (real arithmetic identities on the positive domain):

1. `a0_footing_ratio` — a0(rho_a)/a0(rho_c) = (kappa_a/kappa_c) * sqrt(rho_a/rho_c).
2. `footing_factorization` — (a0_a/a0_c)^2 = (kappa_a/kappa_c)^2 * (rho_a/rho_c):
   the squared footing ratio factorizes into the squared kappa ratio times the
   density ratio. This is the master identity behind the two separate interpretations.
3. `fixed_kappa_density_ratio` — if kappa_a = kappa_c then (a0_a/a0_c)^2 = rho_a/rho_c
   (the fixed-kappa branch: the density must differ by exactly (a0_a/a0_c)^2).
4. `fixed_rho_kappa_ratio` — if rho_a = rho_c then a0_a/a0_c = kappa_a/kappa_c
   (the fixed-density branch: a new effective kappa, no longer the adopted 1/2).
5. `alt_kappa_effective` — with the canonical kappa = 1/2 and a shared density,
   kappa_a = a0_a / (2 * a0_c) (the effective kappa shift, numerically
   0.602388404... for the two stated a0 values; the shift is a NEW adopted input,
   not derived).
6. `a0_determines_rho` — at fixed kappa (and fixed G, c), the footing a0 value
   pins the density: a0_a = a0_c implies rho_a = rho_c.
7. `both_fixed_implies_same_a0` — a shared (kappa, rho) cell yields a single a0:
   rho_a = rho_c with the same kappa forces a0_a = a0_c.
8. `different_a0_forces_different_rho` — contrapositive negative control: with the
   same kappa, a0_a ≠ a0_c forces rho_a ≠ rho_c (holding BOTH kappa and rho fixed
   while changing a0 is inconsistent; the numerical pair R_a = 1.2047768... ≠ 1
   therefore cannot share a cell).

These certify the algebra of the two footings only. They do not derive kappa = 1/2,
do not fix the physical rho_Lambda, do not select between the two footings, and do
not establish that either footing's a0 equals the value required by observations.
-/

namespace AS011

open Real

/-- The footing scale: a0 = kappa * c * sqrt(G * rho). -/
noncomputable def a0 (kappa c G rho : ℝ) : ℝ :=
  kappa * c * Real.sqrt (G * rho)

/-- Footing ratio at fixed (G, c) over arbitrary positive kappas/densities:
    a0(kappa_a,rho_a)/a0(kappa_c,rho_c) = (kappa_a/kappa_c)*sqrt(rho_a/rho_c). -/
theorem a0_footing_ratio {kappa_c c G rho_c kappa_a rho_a : ℝ}
    (hG : 0 < G) (hc : 0 < c) (hkc : 0 < kappa_c) (hka : 0 < kappa_a)
    (hrc : 0 < rho_c) (hra : 0 < rho_a) :
    a0 kappa_a c G rho_a / a0 kappa_c c G rho_c =
      (kappa_a / kappa_c) * Real.sqrt (rho_a / rho_c) := by
  unfold a0
  have hkc0 : kappa_c ≠ 0 := ne_of_gt hkc
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hG1 : 0 < G * rho_c := mul_pos hG hrc
  have hs0 : Real.sqrt (G * rho_c) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hG1)
  have hGr2 : 0 ≤ G * rho_a := le_of_lt (mul_pos hG hra)
  have hdiv : (G * rho_a) / (G * rho_c) = rho_a / rho_c := by
    field_simp [ne_of_gt hG, ne_of_gt hrc]
  have hmain : Real.sqrt (G * rho_a) / Real.sqrt (G * rho_c) =
      Real.sqrt (rho_a / rho_c) := by
    rw [← Real.sqrt_div hGr2 (G * rho_c)]
    rw [hdiv]
  calc
    kappa_a * c * Real.sqrt (G * rho_a) / (kappa_c * c * Real.sqrt (G * rho_c))
        = (kappa_a / kappa_c) *
            (Real.sqrt (G * rho_a) / Real.sqrt (G * rho_c)) := by
            field_simp [hkc0, hc0, hs0]
    _ = (kappa_a / kappa_c) * Real.sqrt (rho_a / rho_c) := by rw [hmain]

/-- Master factorization:
    (a0_a / a0_c)^2 = (kappa_a / kappa_c)^2 * (rho_a / rho_c). -/
theorem footing_factorization {kappa_c c G rho_c kappa_a rho_a a0c a0a : ℝ}
    (hG : 0 < G) (hc : 0 < c) (hkc : 0 < kappa_c) (hka : 0 < kappa_a)
    (hrc : 0 < rho_c) (hra : 0 < rho_a)
    (ha0c : a0c = a0 kappa_c c G rho_c)
    (ha0a : a0a = a0 kappa_a c G rho_a) :
    (a0a / a0c) ^ 2 = (kappa_a / kappa_c) ^ 2 * (rho_a / rho_c) := by
  have h1 : a0 kappa_a c G rho_a / a0 kappa_c c G rho_c =
      (kappa_a / kappa_c) * Real.sqrt (rho_a / rho_c) :=
    a0_footing_ratio hG hc hkc hka hrc hra
  rw [ha0a, ha0c]
  rw [h1]
  have hnn : 0 ≤ rho_a / rho_c := div_nonneg (le_of_lt hra) (le_of_lt hrc)
  rw [mul_pow, Real.sq_sqrt hnn]

/-- Fixed kappa: the squared footing ratio equals the density ratio. -/
theorem fixed_kappa_density_ratio {kappa_c c G rho_c kappa_a rho_a a0c a0a : ℝ}
    (hG : 0 < G) (hc : 0 < c) (hkc : 0 < kappa_c) (hka : 0 < kappa_a)
    (hrc : 0 < rho_c) (hra : 0 < rho_a)
    (hkap : kappa_a = kappa_c)
    (ha0c : a0c = a0 kappa_c c G rho_c)
    (ha0a : a0a = a0 kappa_a c G rho_a) :
    (a0a / a0c) ^ 2 = rho_a / rho_c := by
  have hf := footing_factorization hG hc hkc hka hrc hra ha0c ha0a
  rw [hkap] at hf
  simpa [div_self (ne_of_gt hkc)] using hf

/-- Fixed density: the footing ratio equals the kappa ratio. -/
theorem fixed_rho_kappa_ratio {kappa_c c G rho_c kappa_a rho_a a0c a0a : ℝ}
    (hG : 0 < G) (hc : 0 < c) (hkc : 0 < kappa_c) (hka : 0 < kappa_a)
    (hrc : 0 < rho_c) (_hra : 0 < rho_a)
    (hrho : rho_a = rho_c)
    (ha0c : a0c = a0 kappa_c c G rho_c)
    (ha0a : a0a = a0 kappa_a c G rho_a) :
    a0a / a0c = kappa_a / kappa_c := by
  rw [ha0a, ha0c, hrho]
  unfold a0
  field_simp [ne_of_gt hkc, ne_of_gt hc,
              ne_of_gt (Real.sqrt_pos.2 (mul_pos hG hrc))]

/-- Effective kappa of the alternative footing when the canonical kappa is the
    adopted 1/2 and the density is shared:
    kappa_a = a0_a / (2 * a0_c). -/
theorem alt_kappa_effective {c G rho a0c a0a kappa_a : ℝ}
    (hG : 0 < G) (hc : 0 < c) (hrho : 0 < rho) (hka : 0 < kappa_a)
    (ha0c : a0c = a0 (1 / 2) c G rho)
    (ha0a : a0a = a0 kappa_a c G rho) :
    kappa_a = a0a / (2 * a0c) := by
  have h1 : a0a / a0c = kappa_a / (1 / 2) := by
    exact fixed_rho_kappa_ratio (kappa_c := 1 / 2) (rho_c := rho) (rho_a := rho)
      hG hc (by norm_num) hka hrho hrho rfl ha0c ha0a
  have ha0c0 : a0c ≠ 0 := by
    rw [ha0c]
    unfold a0
    exact ne_of_gt (mul_pos (mul_pos (by norm_num : (0 : ℝ) < 1 / 2) hc)
      (Real.sqrt_pos.2 (mul_pos hG hrho)))
  have h2 : a0a / a0c = 2 * kappa_a := by
    rw [h1]
    field_simp [(by norm_num : (1 / 2 : ℝ) ≠ 0)]
  have h3 : a0a = 2 * kappa_a * a0c := by
    calc
      a0a = (a0a / a0c) * a0c := by field_simp [ha0c0]
      _ = (2 * kappa_a) * a0c := by rw [h2]
  rw [h3]
  field_simp [(by norm_num : (2 : ℝ) ≠ 0), ha0c0]

/-- At fixed kappa (and G, c), the a0 value pins the density:
    a0_a = a0_c implies rho_a = rho_c. -/
theorem a0_determines_rho {kappa c G rho_c rho_a a0c a0a : ℝ}
    (hG : 0 < G) (hc : 0 < c) (hk : 0 < kappa)
    (hrc : 0 < rho_c) (hra : 0 < rho_a)
    (ha0c : a0c = a0 kappa c G rho_c)
    (ha0a : a0a = a0 kappa c G rho_a)
    (ha0eq : a0a = a0c) :
    rho_a = rho_c := by
  rw [ha0a, ha0c] at ha0eq
  unfold a0 at ha0eq
  rw [mul_assoc, mul_assoc] at ha0eq
  have h1 : c * Real.sqrt (G * rho_a) = c * Real.sqrt (G * rho_c) :=
    mul_left_cancel₀ (ne_of_gt hk) ha0eq
  have h2 : Real.sqrt (G * rho_a) = Real.sqrt (G * rho_c) :=
    mul_left_cancel₀ (ne_of_gt hc) h1
  have h3 : (Real.sqrt (G * rho_a)) ^ 2 = (Real.sqrt (G * rho_c)) ^ 2 := by
    rw [h2]
  have h4 : G * rho_a = G * rho_c := by
    rwa [Real.sq_sqrt (le_of_lt (mul_pos hG hra)),
         Real.sq_sqrt (le_of_lt (mul_pos hG hrc))] at h3
  exact mul_left_cancel₀ (ne_of_gt hG) h4

/-- A shared (kappa, rho) cell yields a single a0: rho_a = rho_c (same kappa)
    forces a0_a = a0_c. -/
theorem both_fixed_implies_same_a0 {kappa c G rho_c rho_a a0c a0a : ℝ}
    (_hG : 0 < G) (_hc : 0 < c) (_hk : 0 < kappa)
    (_hrc : 0 < rho_c) (_hra : 0 < rho_a)
    (hrho : rho_a = rho_c)
    (ha0c : a0c = a0 kappa c G rho_c)
    (ha0a : a0a = a0 kappa c G rho_a) :
    a0a = a0c := by
  rw [ha0a, ha0c, hrho]

/-- Negative control, Lean form: with the same kappa, different a0 values force
    different densities — holding BOTH kappa and rho fixed while changing a0 is
    inconsistent. -/
theorem different_a0_forces_different_rho {kappa c G rho_c rho_a a0c a0a : ℝ}
    (_hG : 0 < G) (_hc : 0 < c) (_hk : 0 < kappa)
    (_hrc : 0 < rho_c) (_hra : 0 < rho_a)
    (ha0c : a0c = a0 kappa c G rho_c)
    (ha0a : a0a = a0 kappa c G rho_a)
    (hne : a0a ≠ a0c) :
    rho_a ≠ rho_c := by
  intro hrho
  apply hne
  rw [ha0a, ha0c, hrho]

#print axioms a0_footing_ratio
#print axioms footing_factorization
#print axioms fixed_kappa_density_ratio
#print axioms fixed_rho_kappa_ratio
#print axioms alt_kappa_effective
#print axioms a0_determines_rho
#print axioms both_fixed_implies_same_a0
#print axioms different_a0_forces_different_rho

end AS011
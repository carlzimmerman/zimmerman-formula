import Mathlib
import Mathlib.Tactic

open scoped Topology

/-!
AS060 -- The PD08 quadratic OR expansion -- Lean 4 certificate.

Seed: deepseek_push/astra_spawn_ideas/AS060_the_pd08_quadratic_or_expansion.md
(sha256 5b6caaa70e850d76d649402c9463a07a41746a30c3592297dc33fba3d890ecd5)

Certified content (all on the declared CORE-coefficient / conditional MU_n
branch; framework base a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 ADOPTED):

  1. or_poly_id     exact OR composition identity at the completion ansatz
                    p(y) = y + c2 y^2 + c3 y^3:
                    mu(y) = 1-(1-p)^2
                          = 2y + (2c2-1)y^2 + (2c3-2c2)y^3
                            - (2c3 + c2^2) y^4 - 2 c2 c3 y^5 - c3^2 y^6.
                    The Y^1..Y^3 coefficients are exactly the seed object;
                    the PD08 explanatory text prints (2c2+1) -- the true
                    quadratic coefficient is 2c2-1 (A1/A2 of the run).
  2. or_slope       mu'(0) = 2 for EVERY completion (c2, c3): the deep slope
                    is the channel count, completion-independent (A3).
  3. or_slope_lam, kappa_lam
                    diagnostic counterexamples at per-channel slope
                    lam = p'(0): mu'(0) = 2*lam and the spherical matching
                    forces kappa = a0/s = 1/(2*lam); at lam = 1/2, 1, 2:
                    kappa = 1, 1/2, 1/4 (A3b).
  4. member_sq, member_pow, member_mu_n, mu2_quadratic_coeff
                    the member engagement p = Y/(1+Y) gives EXACTLY the MU_n
                    family 1-(1+Y)^(-n); n=2 is MU2 with quadratic
                    coefficient -3 = 2*(-1) - 1 (A4/A5).
  5. neg_control    (2c2+1) - (2c2-1) = 2 for every c2: the printed
                    coefficient is wrong by +2 at every completion, with no
                    hiding value (C2/C2b negative control).
  6. deep_poisson_algebra, kappa_half, kappa_half_value
                    spherical deep matching: from the first integral
                    2 g^2 r^2 / s = G M (mu ~ 2g/s) follows g^2 = (s/2) g_N,
                    hence a0 = s/2 and kappa = a0/s = 1/2 (D1).

All statements are real-valued algebra; no sqrt is needed because the
matching is certified in the squared g^2 form. The leading kappa implication
uses only the slope (item 2); the quadratic coefficient (items 1, 5) does not
enter it.
-/

namespace AS060

/- 1. Exact OR polynomial identity at the completion ansatz -/
theorem or_poly_id (y c2 c3 : ℝ) :
    1 - (1 - (y + c2 * y ^ 2 + c3 * y ^ 3)) ^ 2 =
      2 * y + (2 * c2 - 1) * y ^ 2 + (2 * c3 - 2 * c2) * y ^ 3 -
        (2 * c3 + c2 ^ 2) * y ^ 4 - 2 * c2 * c3 * y ^ 5 - c3 ^ 2 * y ^ 6 := by
  ring

/- 1b. The exact remainder against the seed's O(Y^3) truncation: it vanishes
       at orders Y^1..Y^3 and is O(Y^4) -- the precise content of the seed's
       O(Y^3) big-O notation. -/
theorem or_poly_cubic_remainder (y c2 c3 : ℝ) :
    1 - (1 - (y + c2 * y ^ 2 + c3 * y ^ 3)) ^ 2 -
      (2 * y + (2 * c2 - 1) * y ^ 2 + (2 * c3 - 2 * c2) * y ^ 3) =
      -(2 * c3 + c2 ^ 2) * y ^ 4 - 2 * c2 * c3 * y ^ 5 - c3 ^ 2 * y ^ 6 := by
  ring

/- 2. Deep slope: mu'(0) = 2, independent of the completion -/
theorem or_slope (c2 c3 : ℝ) :
    HasDerivAt (fun y : ℝ => 1 - (1 - (y + c2 * y ^ 2 + c3 * y ^ 3)) ^ 2) 2 0 := by
  let F : ℝ → ℝ := fun y : ℝ => y + c2 * y ^ 2 + c3 * y ^ 3
  have hF : HasDerivAt F 1 0 := by
    have hi : HasDerivAt (fun y : ℝ => y) 1 0 := hasDerivAt_id 0
    have h2 : HasDerivAt (fun y : ℝ => c2 * y ^ 2) 0 0 := by
      simpa using ((hasDerivAt_id 0).pow (2 : ℕ)).const_mul c2
    have h3 : HasDerivAt (fun y : ℝ => c3 * y ^ 3) 0 0 := by
      simpa using ((hasDerivAt_id 0).pow (3 : ℕ)).const_mul c3
    have hsum : HasDerivAt ((fun y : ℝ => y) + (fun y : ℝ => c2 * y ^ 2) +
        (fun y : ℝ => c3 * y ^ 3)) (1 + 0 + 0) 0 := (hi.add h2).add h3
    have hfun : F = ((fun y : ℝ => y) + (fun y : ℝ => c2 * y ^ 2)) +
          (fun y : ℝ => c3 * y ^ 3) := by
      funext y
      dsimp [F]
    rw [← hfun] at hsum
    norm_num at hsum
    exact hsum
  have hG : HasDerivAt (fun u : ℝ => 1 - (1 - u) ^ 2) 2 0 := by
    have hc : HasDerivAt (fun u : ℝ => 1 + -u) (-1) 0 := by
      simpa using ((hasDerivAt_id 0).neg).const_add (1 : ℝ)
    have hc2 : HasDerivAt ((fun u : ℝ => 1 + -u) ^ 2) (-2) 0 := by
      simpa using hc.pow (2 : ℕ)
    have hneg : HasDerivAt (fun u : ℝ => -((1 + -u) ^ 2)) 2 0 := by
      have hnegp : HasDerivAt (-((fun u : ℝ => 1 + -u) ^ 2)) (-(-2)) 0 := hc2.neg
      have hfun : (fun u : ℝ => -((1 + -u) ^ 2)) =
          -((fun u : ℝ => 1 + -u) ^ 2) := by
        funext u
        rfl
      rw [← hfun] at hnegp
      norm_num at hnegp
      exact hnegp
    have hG1 : HasDerivAt (fun u : ℝ => 1 + -((1 + -u) ^ 2)) 2 0 :=
      hneg.const_add (1 : ℝ)
    have hfun : (fun u : ℝ => 1 - (1 - u) ^ 2) =
        (fun u : ℝ => 1 + -((1 + -u) ^ 2)) := by
      funext u
      ring
    rw [← hfun] at hG1
    exact hG1
  have hF0 : F 0 = 0 := by
    simp [F]
  have hGc : HasDerivAt (fun u : ℝ => 1 - (1 - u) ^ 2) 2 (F 0) := by
    convert hG using 1
  have hd : HasDerivAt ((fun u : ℝ => 1 - (1 - u) ^ 2) ∘ F) 2 0 := by
    simpa using (HasDerivAt.scomp 0 hGc hF)
  have hfun : (fun y : ℝ => 1 - (1 - (y + c2 * y ^ 2 + c3 * y ^ 3)) ^ 2) =
      (fun u : ℝ => 1 - (1 - u) ^ 2) ∘ F := by
    funext y
    dsimp [F]
  rw [← hfun] at hd
  exact hd

/- 3a. General per-channel slope: mu'(0) = 2 * lam -/
theorem or_slope_lam (c2 lam : ℝ) :
    HasDerivAt (fun y : ℝ => 1 - (1 - (lam * y + c2 * y ^ 2)) ^ 2) (2 * lam) 0 := by
  let F : ℝ → ℝ := fun y : ℝ => lam * y + c2 * y ^ 2
  have hF : HasDerivAt F lam 0 := by
    have h1 : HasDerivAt (fun y : ℝ => lam * y) lam 0 := by
      simpa using (hasDerivAt_id 0).const_mul lam
    have h2 : HasDerivAt (fun y : ℝ => c2 * y ^ 2) 0 0 := by
      simpa using ((hasDerivAt_id 0).pow (2 : ℕ)).const_mul c2
    have hsum : HasDerivAt ((fun y : ℝ => lam * y) + (fun y : ℝ => c2 * y ^ 2))
        (lam + 0) 0 := h1.add h2
    have hfun : F = (fun y : ℝ => lam * y) + (fun y : ℝ => c2 * y ^ 2) := by
      funext y
      dsimp [F]
    rw [← hfun] at hsum
    norm_num at hsum
    exact hsum
  have hG : HasDerivAt (fun u : ℝ => 1 - (1 - u) ^ 2) 2 0 := by
    have hc : HasDerivAt (fun u : ℝ => 1 + -u) (-1) 0 := by
      simpa using ((hasDerivAt_id 0).neg).const_add (1 : ℝ)
    have hc2 : HasDerivAt ((fun u : ℝ => 1 + -u) ^ 2) (-2) 0 := by
      simpa using hc.pow (2 : ℕ)
    have hneg : HasDerivAt (fun u : ℝ => -((1 + -u) ^ 2)) 2 0 := by
      have hnegp : HasDerivAt (-((fun u : ℝ => 1 + -u) ^ 2)) (-(-2)) 0 := hc2.neg
      have hfun : (fun u : ℝ => -((1 + -u) ^ 2)) =
          -((fun u : ℝ => 1 + -u) ^ 2) := by
        funext u
        rfl
      rw [← hfun] at hnegp
      norm_num at hnegp
      exact hnegp
    have hG1 : HasDerivAt (fun u : ℝ => 1 + -((1 + -u) ^ 2)) 2 0 :=
      hneg.const_add (1 : ℝ)
    have hfun : (fun u : ℝ => 1 - (1 - u) ^ 2) =
        (fun u : ℝ => 1 + -((1 + -u) ^ 2)) := by
      funext u
      ring
    rw [← hfun] at hG1
    exact hG1
  have hF0 : F 0 = 0 := by
    simp [F]
  have hGc : HasDerivAt (fun u : ℝ => 1 - (1 - u) ^ 2) 2 (F 0) := by
    convert hG using 1
  have hd : HasDerivAt ((fun u : ℝ => 1 - (1 - u) ^ 2) ∘ F) (2 * lam) 0 := by
    simpa [mul_comm] using (HasDerivAt.scomp 0 hGc hF)
  have hfun : (fun y : ℝ => 1 - (1 - (lam * y + c2 * y ^ 2)) ^ 2) =
      (fun u : ℝ => 1 - (1 - u) ^ 2) ∘ F := by
    funext y
    dsimp [F]
  rw [← hfun] at hd
  exact hd

/- 3b. Spherical matching at slope 2*lam: kappa = a0/s = 1/(2*lam) -/
theorem kappa_lam (s a0 lam gN : ℝ) (hs : s ≠ 0) (hl : lam ≠ 0) (hgN : gN ≠ 0)
    (hm : g ^ 2 = a0 * gN) (hdeep : g ^ 2 = s / (2 * lam) * gN) :
    a0 / s = 1 / (2 * lam) := by
  have hh : a0 * gN = s / (2 * lam) * gN := by rw [← hm, hdeep]
  have ha : a0 = s / (2 * lam) := mul_right_cancel₀ hgN hh
  rw [ha]
  field_simp [hs, hl]

/- 3c. The three diagnostic rows of the seed (lam = 1/2, 1, 2) -/
theorem kappa_lam_half : (1 : ℝ) / (2 * (1 / 2 : ℝ)) = 1 := by norm_num
theorem kappa_lam_one : 1 / (2 * (1 : ℝ)) = 1 / 2 := by norm_num
theorem kappa_lam_two : 1 / (2 * (2 : ℝ)) = 1 / 4 := by norm_num

/- 4a. Member engagement p = y/(1+y): the n=2 composition is MU2 exactly -/
theorem member_sq (y : ℝ) (hy : y ≠ -1) :
    1 - (1 - y / (1 + y)) ^ 2 = (2 * y + y ^ 2) / (1 + y) ^ 2 := by
  have hy1 : 1 + y ≠ 0 := by
    intro hz
    apply hy
    linarith
  have hf : 1 - y / (1 + y) = 1 / (1 + y) := by
    field_simp [hy1]
    ring
  rw [hf, div_pow, one_pow]
  field_simp [hy1]
  rw [pow_two]
  ring

/- 4b. Member power: (1 - y/(1+y))^n = (1+y)^(-n) -/
theorem member_pow (y : ℝ) (n : ℕ) (hy : y ≠ -1) :
    (1 - y / (1 + y)) ^ n = 1 / (1 + y) ^ n := by
  have hy1 : 1 + y ≠ 0 := by
    intro hz
    apply hy
    linarith
  have hfrac : 1 - y / (1 + y) = 1 / (1 + y) := by
    field_simp [hy1]
    ring
  rw [hfrac]
  induction n with
  | zero => simp
  | succ m ih =>
      rw [pow_succ, pow_succ, ih]
      field_simp [hy1]

/- 4c. The conditional MU_n statistical response at the member -/
theorem member_mu_n (y : ℝ) (n : ℕ) (hy : y ≠ -1) :
    1 - (1 - y / (1 + y)) ^ n = 1 - 1 / (1 + y) ^ n := by
  rw [member_pow y n hy]

/- 4d. mu_2's quadratic coefficient at the member is -3 = 2*c2 - 1 with the
       member's c2 = -1 (the explicit coefficient-level check A5) -/
theorem mu2_quadratic_coeff : (2 * (-1 : ℝ) - 1) = -3 := by norm_num

/- 5. Negative control: the printed form (2c2+1) and the true form (2c2-1)
       differ by exactly 2 for EVERY c2 -- no completion hides the typo -/
theorem neg_control (c2 : ℝ) : (2 * c2 + 1) - (2 * c2 - 1) = 2 := by ring

/- 6a. Deep Poisson first integral: mu ~ 2 g/s, spherical point mass -/
theorem deep_poisson_algebra (g r s M G : ℝ) (hr : r ≠ 0) (hs : s ≠ 0)
    (hfirst : 2 * g ^ 2 * r ^ 2 / s = G * M) :
    g ^ 2 = (s / 2) * (G * M / r ^ 2) := by
  calc
    g ^ 2 = (s / 2) * ((2 * g ^ 2 * r ^ 2 / s) / r ^ 2) := by
      field_simp [hs, hr]
    _ = (s / 2) * (G * M / r ^ 2) := by rw [hfirst]

/- 6b. Matching the a0-line g^2 = a0 g_N: a0 = s/2 (lam = 1 row) -/
theorem kappa_half (s a0 gN : ℝ) (hgN : gN ≠ 0)
    (hm : g ^ 2 = a0 * gN) (hdeep : g ^ 2 = (s / 2) * gN) :
    a0 = s / 2 := by
  have hh : a0 * gN = (s / 2) * gN := by rw [← hm, hdeep]
  exact mul_right_cancel₀ hgN hh

/- 6c. kappa = a0/s = 1/2 on the adopted footing -/
theorem kappa_half_value (s : ℝ) (hs : s ≠ 0) : (s / 2) / s = 1 / 2 := by
  field_simp [hs]

end AS060
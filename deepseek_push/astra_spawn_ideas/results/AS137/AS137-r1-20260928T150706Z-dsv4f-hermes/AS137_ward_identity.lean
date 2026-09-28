import Mathlib

/-!
# AS137 — ordinary-matter Ward identity: negative-control witness algebra

Tier-0 certificate of the component algebra behind the AS137 verification.
Theory being certified (flat 2D Minkowski, coordinates (t, r), g = diag(-1, 1)):

    S_b = ∫ [ -(1/2) g^{μν} ∂_μψ ∂_νψ - V(ψ) ] dt dr ,   V = 0
    E_ψ = □ψ - V'(ψ)                    (Euler-Lagrange expression)
    T^{μν} = (∂^μψ)(∂^νψ) - (1/2) g^{μν} (∂ψ)² - g^{μν} V     (stress)

Witness ψ(r) = r² (depends on r only):
    E_ψ = 2                      (off shell: □(r²) = ∂_r²(r²) = 2)
    T^{tt} = 2r²,  T^{rr} = 2r²
    ∂_r T^{rr} = 4r = 2·(2r) = E_ψ · ∂^rψ      (the off-shell Ward identity)

Negative control (diagnostic nonmetric coupling)  S_b' = S_b + z0·ψ²·Z,
Z(r) = -1/(z0·r²):
    E'_ψ = E_ψ + 2·z0·Z·ψ = 2 + 2·z0·(-1/(z0 r²))·r² = 0   (ON the baryon shell)
    T'^{tt} = 3r²,  T'^{rr} = r²
    ∂_t T'^{tt} = 0,  ∂_r T'^{rr} = 2r ≠ 0

=> the baryon equation holds (E'_ψ = 0) yet div T' = (0, 2r) ≠ 0: the
   coupling term z0·ψ²·Z prevents the on-shell conservation statement
   (the negative control of the Ward identity — it must and does fail).

Every theorem below is a real-number identity verified by computation;
the file compiles with axioms subseteq {propext, Classical.choice, Quot.sound}.
-/

open scoped BigOperators

/- Derivative of r ↦ r² is r ↦ 2r (unconditional field lemma). -/
lemma deriv_sq : deriv (fun x : ℝ => x ^ 2) = fun x : ℝ => 2 * x := by
  funext x
  rw [deriv_pow_field]
  ring_nf

/- Derivative of r ↦ 2r² is r ↦ 4r. -/
lemma deriv_two_sq : deriv (fun x : ℝ => 2 * x ^ 2) = fun x : ℝ => 4 * x := by
  funext x
  rw [deriv_const_mul_field'] -- deriv (fun x => 2 * x^2) = fun x => 2 * deriv (fun x => x^2) x
  rw [deriv_sq]
  ring_nf

/- [plain, off shell] E_ψ = 2 ≠ 0: the plain action equation is NOT satisfied
   by ψ = r² (this is what makes the plain on-shell statement inapplicable). -/
theorem plain_euler_lagrange_nonzero : (fun r : ℝ => 2) ≠ 0 := by
  intro h
  have h0 := congrFun h 0
  norm_num at h0

/- [plain, off-shell Ward identity at this witness] ∂_r T^{rr} = E_ψ · ∂^rψ,
   i.e. deriv (2 r²) = 2 · (2 r).  The identity holds OFF shell, feeding E_ψ
   on the right:  div T = E_ψ grad ψ. -/
theorem plain_ward_flat :
    deriv (fun r : ℝ => 2 * r ^ 2) = fun r : ℝ => 2 * (2 * r) := by
  rw [deriv_two_sq]
  funext r
  ring

/- [negative control, on shell] E'_ψ = 2 + 2·z0·(-1/(z0 r²))·r² = 0 for r ≠ 0
   and z0 ≠ 0. -/
theorem control_on_shell (z0 : ℝ) (hz0 : z0 ≠ 0) :
    ∀ r : ℝ, r ≠ 0 → 2 + 2 * z0 * (-(1 / (z0 * r ^ 2))) * r ^ 2 = 0 := by
  intro r hr
  field_simp [hr, hz0]; ring

theorem control_on_shell_alt (z0 : ℝ) (hz0 : z0 ≠ 0) :
    ∀ r : ℝ, r ≠ 0 → 2 + 2 * z0 * (-(1 / (z0 * r ^ 2))) * r ^ 2 = 0 := by
  intro r hr
  have hzr : z0 * r ^ 2 ≠ 0 := mul_ne_zero hz0 (pow_ne_zero 2 hr)
  field_simp [hr]; ring

/- [negative control] T'^{tt} = T^{tt} + z0·g^{tt}·Z·ψ² = 2r² + (-1)·z0·Z·r⁴
   with Z = -1/(z0 r²) simplifies to 3r² (r ≠ 0). -/
theorem control_Ttt (z0 : ℝ) (hz0 : z0 ≠ 0) :
    ∀ r : ℝ, r ≠ 0 → 2 * r ^ 2 + z0 * (-1) * (-(1 / (z0 * r ^ 2))) * r ^ 4 = 3 * r ^ 2 := by
  intro r hr
  field_simp [hr, hz0]; ring

/- [negative control] T'^{rr} = T^{rr} + z0·g^{rr}·Z·ψ² = 2r² + z0·Z·r⁴
   simplifies to r² (r ≠ 0). -/
theorem control_Trr (z0 : ℝ) (hz0 : z0 ≠ 0) :
    ∀ r : ℝ, r ≠ 0 → 2 * r ^ 2 + z0 * (-(1 / (z0 * r ^ 2))) * r ^ 4 = r ^ 2 := by
  intro r hr
  field_simp [hr, hz0]; ring

/- [negative control] the t-component of div T' vanishes exactly (∂_t of a
   function of r only). -/
theorem divTp_t (r t : ℝ) : deriv (fun _ : ℝ => 3 * r ^ 2) t = 0 := by
  simp [deriv_const]

/- [negative control] div T'^r = ∂_r T'^{rr} = ∂_r(r²) = 2r. -/
theorem divTp_r : deriv (fun r : ℝ => r ^ 2) = fun r : ℝ => 2 * r := by
  exact deriv_sq

/- [the prevented identity — the control is capable of failing] with the
   coupling active, the baryon equation holds (E'_ψ = 0) yet the divergence
   of the stress does NOT vanish: at r = 3, ∂_r T'^{rr} = 6 ≠ 0. -/
theorem on_shell_yet_div_nonzero (z0 : ℝ) (hz0 : z0 ≠ 0) :
    (∀ r : ℝ, r ≠ 0 → 2 + 2 * z0 * (-(1 / (z0 * r ^ 2))) * r ^ 2 = 0) ∧
      ¬ deriv (fun r : ℝ => r ^ 2) = 0 := by
  constructor
  · exact control_on_shell z0 hz0
  · intro h
    have h3 : deriv (fun r : ℝ => r ^ 2) 3 = 0 := congrFun h 3
    rw [deriv_sq] at h3
    norm_num at h3

/- Explicit witness point: E'_ψ(3) = 0 and div T'^r(3) = 6, side by side. -/
theorem witness_point (z0 : ℝ) (hz0 : z0 ≠ 0) :
    (2 + 2 * z0 * (-(1 / (z0 * 3 ^ 2))) * 3 ^ 2 = 0) ∧
      deriv (fun r : ℝ => r ^ 2) 3 = 6 := by
  constructor
  · field_simp [hz0]; ring
  · rw [deriv_sq]
    norm_num
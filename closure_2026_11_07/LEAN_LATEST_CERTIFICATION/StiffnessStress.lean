import Mathlib
open Filter
namespace StiffnessStress

/-- QX17D's scalar chain-rule leaf: scaling Pi to Pi/lambda produces
Pi F'(Pi), independently of any assumption of quadratic homogeneity. This is
not a covariant metric-variation theorem. -/
theorem inverse_scale_hasDerivAt (F : ℝ → ℝ) (p d : ℝ)
    (hF : HasDerivAt F d p) :
    HasDerivAt (fun l : ℝ => F (p/l)) (-p*d) 1 := by
  have hquot : HasDerivAt (fun l : ℝ => p/l) (-p) (1 : ℝ) := by
    convert! (hasDerivAt_const (1 : ℝ) p).div (hasDerivAt_id (1 : ℝ)) (by norm_num) using 1 <;> norm_num
  have hcomp : HasDerivAt (fun l : ℝ => F (p/l)) (d*(-p)) (1 : ℝ) := by
    have hF1 : HasDerivAt F d (p/(1 : ℝ)) := by simpa using hF
    exact hF1.comp (1 : ℝ) hquot
  convert! hcomp using 1 <;> ring

/-- Including the minus sign of the stiffness energy gives +Pi F'(Pi)
under the same inverse scaling. -/
theorem negative_energy_scale_hasDerivAt (F : ℝ → ℝ) (p d : ℝ)
    (hF : HasDerivAt F d p) :
    HasDerivAt (fun l : ℝ => -F (p/l)) (p*d) 1 := by
  exact (inverse_scale_hasDerivAt F p d hF).neg.congr_deriv (by ring)

noncomputable def raw (p : ℝ) : ℝ := p^2/2
noncomputable def sixth (A p : ℝ) : ℝ := A*p^6
noncomputable def generic (p : ℝ) : ℝ := p^2/2+(3/10)*p^4-(1/7)*p^6

theorem raw_hasDerivAt (p : ℝ) : HasDerivAt raw p p := by
  unfold raw
  convert! (hasDerivAt_pow 2 p).div_const (2 : ℝ) using 1 <;> norm_num <;> ring

theorem sixth_hasDerivAt (A p : ℝ) : HasDerivAt (sixth A) (6*A*p^5) p := by
  unfold sixth
  convert! (hasDerivAt_pow 6 p).const_mul A using 1 <;> norm_num <;> ring

theorem generic_hasDerivAt (p : ℝ) :
    HasDerivAt generic (p+(6/5)*p^3-(6/7)*p^5) p := by
  unfold generic
  convert! (((hasDerivAt_pow 2 p).div_const (2 : ℝ)).add
    ((hasDerivAt_pow 4 p).const_mul (3/10 : ℝ))).sub
      ((hasDerivAt_pow 6 p).const_mul (1/7 : ℝ)) using 1 <;> norm_num <;> ring

/-- The old 2F coefficient agrees for the quadratic control only. -/
theorem raw_euler (p : ℝ) : p*deriv raw p = 2*raw p := by
  rw [(raw_hasDerivAt p).deriv]
  unfold raw
  ring

theorem sixth_euler (A p : ℝ) : p*deriv (sixth A) p = 6*sixth A p := by
  rw [(sixth_hasDerivAt A p).deriv]
  unfold sixth
  ring

theorem sixth_stress_discrepancy (A p : ℝ) :
    p*deriv (sixth A) p-2*sixth A p = 4*sixth A p := by
  rw [sixth_euler]
  ring

theorem sixth_stress_ne_old {A p : ℝ} (hA : 0 < A) (hp : p ≠ 0) :
    p*deriv (sixth A) p ≠ 2*sixth A p := by
  have hf : 0 < sixth A p := by unfold sixth; positivity
  rw [sixth_euler]
  linarith

theorem generic_stress_discrepancy (p : ℝ) :
    p*deriv generic p-2*generic p = (3/5)*p^4-(4/7)*p^6 := by
  rw [(generic_hasDerivAt p).deriv]
  unfold generic
  ring

/-- Concrete counterexample to retaining 2F in the general stress term. -/
theorem generic_counterexample : (1 : ℝ)*deriv generic 1 ≠ 2*generic 1 := by
  rw [(generic_hasDerivAt 1).deriv]
  norm_num [generic]

/-- The first branch's integrated coefficient matches CK2's form. -/
theorem first_piece_second_derivative_coefficient :
    (30 : ℝ)*(122363904/44610575) = 734183424/8922115 := by norm_num

/-- Both stiffness and the recorded first-derivative profile approach zero
at the switch. Continuity excludes a finite latent jump in this energy term;
it does not exclude all possible dynamical energy transfer. -/
noncomputable def switchedSixth (A p : ℝ) : ℝ := A*(max p 0)^6
noncomputable def switchedSlope (A p : ℝ) : ℝ := 6*A*(max p 0)^5

theorem switch_values (A : ℝ) : switchedSixth A 0 = 0 ∧ switchedSlope A 0 = 0 := by
  simp [switchedSixth,switchedSlope]

theorem switch_energy_tends_zero (A gamma : ℝ) :
    Tendsto (fun p => gamma*switchedSixth A p) (nhds 0) (nhds 0) := by
  have h : Continuous (fun p => gamma*switchedSixth A p) := by
    unfold switchedSixth
    fun_prop
  simpa [switchedSixth] using h.continuousAt.tendsto (x := 0)

theorem switch_slope_tends_zero (A : ℝ) :
    Tendsto (switchedSlope A) (nhds 0) (nhds 0) := by
  have h : Continuous (switchedSlope A) := by unfold switchedSlope; fun_prop
  simpa [switchedSlope] using h.continuousAt.tendsto (x := 0)

theorem no_latent_jump (gamma leftF rightF : ℝ) (hl : leftF = 0) (hr : rightF = 0) :
    gamma*(rightF-leftF) = 0 := by rw [hl,hr]; ring

/-- The switched sixth-power function itself is differentiable at the branch
point, with derivative zero; this is not merely a named slope profile. -/
theorem switchedSixth_hasDerivAt_zero (A : ℝ) :
    HasDerivAt (switchedSixth A) 0 (0 : ℝ) := by
  have hL : HasDerivWithinAt (switchedSixth A) 0 (Set.Iic 0) (0 : ℝ) := by
    apply (hasDerivAt_const (0 : ℝ) (0 : ℝ)).hasDerivWithinAt.congr
    · intro x hx
      simp only [Set.mem_Iic] at hx
      simp [switchedSixth,max_eq_right hx]
    · simp [switchedSixth]
  have hpow : HasDerivAt (sixth A) 0 (0 : ℝ) := by
    simpa using sixth_hasDerivAt A 0
  have hR : HasDerivWithinAt (switchedSixth A) 0 (Set.Ici 0) (0 : ℝ) := by
    apply hpow.hasDerivWithinAt.congr
    · intro x hx
      simp only [Set.mem_Ici] at hx
      simp [switchedSixth,sixth,max_eq_left hx]
    · simp [switchedSixth,sixth]
  have hcover : Set.Iic (0 : ℝ) ∪ Set.Ici 0 = Set.univ := by
    ext x
    simp only [Set.mem_union,Set.mem_Iic,Set.mem_Ici,Set.mem_univ]
    exact ⟨fun _ => trivial,fun _ => le_total x 0⟩
  have h := hL.union hR
  rw [hcover] at h
  exact hasDerivWithinAt_univ.mp h

theorem switchedSixth_deriv_zero (A : ℝ) : deriv (switchedSixth A) 0 = 0 :=
  (switchedSixth_hasDerivAt_zero A).deriv

end StiffnessStress
#print axioms StiffnessStress.inverse_scale_hasDerivAt
#print axioms StiffnessStress.raw_hasDerivAt
#print axioms StiffnessStress.sixth_hasDerivAt
#print axioms StiffnessStress.generic_hasDerivAt
#print axioms StiffnessStress.raw_euler
#print axioms StiffnessStress.sixth_euler
#print axioms StiffnessStress.sixth_stress_discrepancy
#print axioms StiffnessStress.sixth_stress_ne_old
#print axioms StiffnessStress.generic_stress_discrepancy
#print axioms StiffnessStress.generic_counterexample
#print axioms StiffnessStress.first_piece_second_derivative_coefficient
#print axioms StiffnessStress.switch_values
#print axioms StiffnessStress.switch_energy_tends_zero
#print axioms StiffnessStress.switch_slope_tends_zero
#print axioms StiffnessStress.no_latent_jump

#print axioms StiffnessStress.negative_energy_scale_hasDerivAt

#print axioms StiffnessStress.switchedSixth_hasDerivAt_zero
#print axioms StiffnessStress.switchedSixth_deriv_zero

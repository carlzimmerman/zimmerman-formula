import Mathlib

/-! Conditional algebra for the nonlinear external-field tail.
The PDE, existence of an asymptotic expansion, and observational identifications
are NOT formalized here. They are explicit physical/mathematical inputs. -/
namespace NonlinearExternalTail
noncomputable section

def asymmetry (d B o r : ℝ) : ℝ := 2*d/r^3 + 3*B/r^4 + 4*o/r^5

theorem angular_axis_cancellation (L A : ℝ) :
    (A-L/2) + (3*L/2-A) = L := by ring

theorem harmonic_axis_cancellation (L A : ℝ) :
    2*(L+A)/5 + (3*L-2*A)/5 = L := by ring

theorem two_radius_filter (d B o r : ℝ) (hr : r ≠ 0) :
    asymmetry d B o r - 8*asymmetry d B o (2*r) =
      3*B/(2*r^4) + 3*o/r^5 := by
  unfold asymmetry
  field_simp
  ring

theorem three_radius_filter (d B o r : ℝ) (hr : r ≠ 0) :
    asymmetry d B o r - 40*asymmetry d B o (2*r) +
      256*asymmetry d B o (4*r) = -3*B/(2*r^4) := by
  unfold asymmetry
  field_simp
  ring

theorem aqual_orbital_relation {L β : ℝ}
    (horbit : (1+L)*(1-2*β)=2) : L*(1-2*β)=1+2*β := by
  nlinarith [horbit]

theorem qumond_orbital_relation {L k β : ℝ}
    (horbit : (1+L)*(1-2*β)=2) (hdual : (1+L)*(1+k)=1) :
    2*(-k)=1+2*β := by
  have hn : 1+L ≠ 0 := by intro hz; rw [hz] at hdual; norm_num at hdual
  have hh : (1+L)*(2*(1+k)-(1-2*β))=0 := by nlinarith [horbit, hdual]
  have hh' := (mul_eq_zero.mp hh).resolve_left hn
  linarith

theorem deep_separation {L k : ℝ}
    (horbit : (1+L)*(1-2*(0:ℝ))=2) (hdual : (1+L)*(1+k)=1) :
    L=1 ∧ -k=1/2 := by
  constructor
  · nlinarith [horbit]
  · have := qumond_orbital_relation horbit hdual
    linarith

theorem no_aqual_retuning {N β : ℝ} (hbad : N*(1-2*β) ≠ 1+2*β) :
    ¬ ∃ L : ℝ, N=L ∧ (1+L)*(1-2*β)=2 := by
  rintro ⟨L, hN, hβ⟩
  apply hbad
  rw [hN]
  exact aqual_orbital_relation hβ

#print axioms angular_axis_cancellation
#print axioms harmonic_axis_cancellation
#print axioms two_radius_filter
#print axioms three_radius_filter
#print axioms aqual_orbital_relation
#print axioms qumond_orbital_relation
#print axioms deep_separation
#print axioms no_aqual_retuning

end
end NonlinearExternalTail

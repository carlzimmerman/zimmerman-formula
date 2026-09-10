import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/- Conditional quadratic certificates, not a nonlinear field-theory proof.
The action-to-coefficient bridge is checked separately in SymPy. -/
namespace EntropyClockAllScales

theorem background_e_negative (q m O : ℝ) (hq : 0<q) (hm : 0<m)
    (hO : O≤1) : q*m/(1+m)*(3/2*O-2)<0 := by
  have hp : 0<q*m/(1+m) := by positivity
  have hn : 3/2*O-2<0 := by linarith
  exact mul_neg_of_pos_of_neg hp hn

theorem all_wavelength_kinetic (B e f H D p : ℝ)
    (hB : 0<B) (he : e<0) (hf : 0<f) (hH : 0<H)
    (hD : 0<D) (hp : 0≤p) :
    e*f-p*D/H^2<0 ∧ B < B-f^2/(e*f-p*D/H^2) ∧
    0 < B-f^2/(e*f-p*D/H^2) := by
  have hneg : e*f<0 := mul_neg_of_neg_of_pos he hf
  have hn : 0≤p*D/H^2 := by positivity
  have hd : e*f-p*D/H^2<0 := by linarith
  have hsq : 0<f^2 := by positivity
  have hr : f^2/(e*f-p*D/H^2)<0 := div_neg_of_pos_of_neg hsq hd
  exact ⟨hd, by linarith, by linarith⟩

theorem finite_bracket_regular (a A B f H D p : ℝ)
    (ha : 0<a) (hA : 0<A) (hB : 0<B) (hf : 0<f)
    (hH : 0<H) (hD : 0<D) (hp : 0≤p) :
    0 < a^3*(3*A*f/B+p*D/H^2) ∧
    0 < (a^3*(3*A*f/B+p*D/H^2))^2 := by
  constructor <;> positivity

theorem homogeneous_basis_regular (H f B : ℝ)
    (hH : 0<H) (hf : 0<f) (hB : 0<B) : 0<H^2*f/B := by
  positivity

#print axioms background_e_negative
#print axioms all_wavelength_kinetic
#print axioms finite_bracket_regular
#print axioms homogeneous_basis_regular
end EntropyClockAllScales

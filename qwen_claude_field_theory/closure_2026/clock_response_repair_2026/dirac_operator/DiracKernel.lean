import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity

namespace ClockDiracKernel

/- The genuine bracket has this triangular elimination order. Unknown higher
blocks cannot create a kernel if the computed lapse block D is injective.
This does not assume that the physical global D is injective. -/
theorem bracket_kernel_trivial {V : Type*} [AddCommGroup V]
    (D G H J K L : V → V) (hD : Function.Injective D)
    (d0 : D 0=0) (g0 : G 0=0) (h0 : H 0=0)
    (j0 : J 0=0) (k0 : K 0=0) (l0 : L 0=0)
    (n c t e : V)
    (he : D e=0) (ht : -D t+G e=0) (hc : D c+H e=0)
    (hn : D n+J c+K t+L e=0) : n=0 ∧ c=0 ∧ t=0 ∧ e=0 := by
  have e0 : e=0 := hD (he.trans d0.symm)
  simp only [e0,g0,add_zero,neg_eq_zero] at ht
  have t0 : t=0 := hD (ht.trans d0.symm)
  simp only [e0,h0,add_zero] at hc
  have c0 : c=0 := hD (hc.trans d0.symm)
  simp only [c0,t0,e0,j0,k0,l0,add_zero] at hn
  exact ⟨hD (hn.trans d0.symm),c0,t0,e0⟩

theorem homogeneous_gap (a A H B v : ℝ)
    (ha : 0<a) (hA : 0<A) (hH : 0<H) (hB : 0<B) (hv : v<1) :
    0 < 9*a^3*A^2*H^2*(1-v)/B := by
  have : 0<1-v := sub_pos.mpr hv
  positivity

#print axioms bracket_kernel_trivial
#print axioms homogeneous_gap
end ClockDiracKernel

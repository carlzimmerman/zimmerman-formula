import Mathlib
noncomputable section
namespace TrackingMassExtension

theorem feedback_positive (E M xi lam phi h : ℝ)
    (he : 0 < E) (hm : 0 < M) (hx : 0 < xi) (hl : 0 < lam) (hh : 0 ≤ h) :
    0 < E*(M^2+xi*(1+2*xi)*phi^2) +
      h*phi^2/2*(M^2*(1+2*xi)+xi*(1+4*xi)*phi^2) +
      lam*phi^4/4*(M^2*(1+4*xi)+xi*(1+6*xi)*phi^2) := by positivity

#print axioms feedback_positive
end TrackingMassExtension

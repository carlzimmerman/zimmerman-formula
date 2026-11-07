import Std
namespace ParameterSelection
variable {F : Type} [Lean.Grind.Field F]

-- Absolute vacuum offsets are absent from a contrast-only model.
theorem common_shift (inside outside shift : F) :
    (outside + shift) - (inside + shift) = outside - inside := by grind

-- Denominator-cleared rescaling: v'=s*v, lambda'*s^4=lambda,
-- y'*s=y. Endpoint barrier and squared mass gap remain invariant.
theorem phase_deformation (s v l lp y yp : F)
    (hl : lp*s^4=l) (hy : yp*s=y) :
    lp*(s*v)^4=l*v^4 ∧ yp^2*(s*v)^2=y^2*v^2 := by grind

-- The leading thin-wall squared-tension formula scales as s^2.
theorem tension_deformation (s v l lp sigma : F)
    (hl : lp*s^4=l) (ht : 72*sigma^2=l*v^6) :
    72*(s*sigma)^2=lp*(s*v)^6 := by grind

-- Force balance plus a zero radial derivative, for P proportional to R^-alpha.
theorem marginal_pressure (p delta sigma r alpha : F)
    (force : (p+delta)*r=2*sigma)
    (marginal : alpha*p*r=2*sigma) (hr : r ≠ 0) :
    delta=(alpha-1)*p := by grind

-- Charge neutrality only fixes the net inventory after total charge is supplied.
theorem charge_inventory (qtotal qb nb nchi : F)
    (charge : qtotal=qb*nb+nchi) : nchi=qtotal-qb*nb := by grind

-- t is the positive square root in the physical interpretation; positivity
-- is unnecessary for this polynomial implication, not proved here.
theorem detector_response (t g a gn beta : F)
    (temperature : t^2=g^2+a^2) (response : gn=beta*(t-a)) :
    beta^2*g^2=gn^2+a*beta*gn := by grind

-- If kappa*beta=2*d, exact kappa=1/2 demands beta=4*d.
theorem half_requires_response (kappa beta d : F)
    (scale : kappa*beta=2*d) (half : 2*kappa=1) :
    beta=4*d := by grind

-- Conditional singular-isothermal tail matching. p is P/(rho_DE*c^2).
theorem half_requires_inventory_pressure (kappa pi eta p : F)
    (tail : kappa^2=8*pi*eta^2*p) (half : 2*kappa=1) :
    32*pi*eta^2*p=1 := by grind

#print axioms common_shift
#print axioms phase_deformation
#print axioms tension_deformation
#print axioms marginal_pressure
#print axioms charge_inventory
#print axioms detector_response
#print axioms half_requires_response
#print axioms half_requires_inventory_pressure
end ParameterSelection

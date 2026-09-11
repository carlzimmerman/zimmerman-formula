import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/- Exact real-jet algebra of the scalar metric constraints in
FIRST_ORDER_HANDOFF.md. Physical interpretation assumes smooth fields,
p = k²/a², p_dot = -2Hp, constant M2, and the independently derived
stress/Einstein equations. This file does NOT formalize those PDEs,
their variation, solution existence, stability, MOND, or observed spectra. -/
namespace CosmologicalConstraint
noncomputable section

structure Jets where
  M2 : ℝ
  H : ℝ
  Hd : ℝ
  p : ℝ
  z : ℝ
  zd : ℝ
  K : ℝ
  Kd : ℝ
  alpha : ℝ
  rhoDot : ℝ
  enthalpy : ℝ
  drho : ℝ
  drhod : ℝ
  dp : ℝ
  J : ℝ

def ham (x : Jets) : ℝ := 2*x.M2*(x.p*x.z+x.H*x.K)-x.drho
def hamRate (x : Jets) : ℝ :=
  2*x.M2*(-2*x.H*x.p*x.z+x.p*x.zd+x.Hd*x.K+x.H*x.Kd)-x.drhod
def traceResidual (x : Jets) : ℝ :=
  2*x.M2*(x.Kd-3*x.Hd*x.alpha+x.p*x.alpha+2*x.H*x.K)+x.drho+3*x.dp
def energyResidual (x : Jets) : ℝ :=
  x.drhod-x.alpha*x.rhoDot+3*x.H*(x.drho+x.dp)+x.enthalpy*x.K+x.p*x.J
def rayResidual (x : Jets) : ℝ := 2*x.M2*x.Hd+x.enthalpy
def backgroundEnergy (x : Jets) : ℝ := x.rhoDot+3*x.H*x.enthalpy
def momentum (x : Jets) : ℝ := 2*x.M2*(x.zd-x.H*x.alpha)+x.J

/-- Off shell: no Einstein or matter equation is assumed. -/
theorem residual_identity (x : Jets) :
    x.p*momentum x =
      hamRate x+2*x.H*ham x-x.H*traceResidual x+energyResidual x
      +x.alpha*backgroundEnergy x-rayResidual x*(x.K+3*x.H*x.alpha) := by
  unfold momentum hamRate ham traceResidual energyResidual backgroundEnergy rayResidual
  ring

/-- Reconstructing the Hamiltonian AND its derivative recovers momentum
only at nonzero physical squared wavenumber. -/
theorem recover_momentum (x : Jets) (hp : x.p ≠ 0)
    (hC : ham x = 0) (hCd : hamRate x = 0)
    (hR : traceResidual x = 0) (hE : energyResidual x = 0)
    (hB : rayResidual x = 0) (hU : backgroundEnergy x = 0) :
    momentum x = 0 := by
  have h := residual_identity x
  rw [hC, hCd, hR, hE, hB, hU] at h
  have hm : x.p*momentum x = 0 := by simpa using h
  exact (mul_eq_zero.mp hm).resolve_left hp

/-- Algebraic rate of a² C, using a_dot=aH. No global ODE/PDE
existence or zero-derivative-to-constancy theorem is asserted here. -/
theorem weighted_constraint_rate (x : Jets) (a : ℝ)
    (hM : momentum x = 0)
    (hR : traceResidual x = 0) (hE : energyResidual x = 0)
    (hB : rayResidual x = 0) (hU : backgroundEnergy x = 0) :
    2*a*(a*x.H)*ham x+a^2*hamRate x = 0 := by
  have h := residual_identity x
  rw [hM, hR, hE, hB, hU] at h
  have rate : hamRate x = -2*x.H*ham x := by nlinarith [h]
  rw [rate]
  ring

/-- Counterexample to dropping hp in recover_momentum, at the jet-algebra
level. The momentum amplitude has no spatial meaning at k=0; this is
not a claim of a physical solution violating Einstein's equations. -/
theorem zero_mode_requires_separate_analysis :
    ∃ x : Jets, x.M2 > 0 ∧ x.p = 0 ∧
      ham x = 0 ∧ hamRate x = 0 ∧ traceResidual x = 0 ∧
      energyResidual x = 0 ∧ rayResidual x = 0 ∧
      backgroundEnergy x = 0 ∧ momentum x = 1 := by
  refine ⟨⟨1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1⟩, ?_⟩
  norm_num [ham, hamRate, traceResidual, energyResidual,
    rayResidual, backgroundEnergy, momentum]

#print axioms residual_identity
#print axioms recover_momentum
#print axioms weighted_constraint_rate
#print axioms zero_mode_requires_separate_analysis

end
end CosmologicalConstraint

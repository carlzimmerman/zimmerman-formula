import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/- Continuum constraint-residual energy, not energy of physical perturbations.
   Z = C_M / A; C = C_H; g = N_r / A; T is the clock-constraint residual.
   balance.py derives the weighted divergence identity from action Noether
   identities and checks the on-shell dust Ward contribution in SymPy.
   Neither that variational bridge nor PDE integration is formalized here. -/
namespace ClockConstraintEnergy
noncomputable section

def energy (C Z : ℝ) : ℝ := C^2+Z^2

def balance (N k h g C Z T : ℝ) : ℝ :=
  -3*N*(k+2*h)*C^2-N*(3*k+2*h)*Z^2+6*g*C*Z-2*T*C

def radialFlux (V N A C Z : ℝ) : ℝ := 2*V*N/A*C*Z

theorem energy_zero_iff (C Z : ℝ) : energy C Z = 0 ↔ C=0 ∧ Z=0 := by
  unfold energy
  constructor
  · intro hz
    constructor <;> nlinarith [sq_nonneg C,sq_nonneg Z]
  · rintro ⟨rfl,rfl⟩
    ring

/-- The characteristic roots of the eta=1 constraint subsystem, not DOFs. -/
theorem characteristic_factorization (lambda N A : ℝ) :
    lambda^2-N^2/A^2 = (lambda-N/A)*(lambda+N/A) := by
  ring

/-- Homogeneous expanding coefficients damp the constraint-energy balance.
The physical application also requires vanishing clock residual, on-shell
matter and the derived spatial evolution equations. No boundary flux is
silently assumed zero; balance is time derivative minus flux divergence. -/
theorem expanding_balance_bound (N H C Z : ℝ)
    (hN : 0 ≤ N) (hH : 0 ≤ H) :
    balance N H H 0 C Z 0 ≤ -5*N*H*energy C Z := by
  unfold balance energy
  have hprod : 0 ≤ N*H*C^2 := mul_nonneg (mul_nonneg hN hH) (sq_nonneg C)
  nlinarith only [hprod]

/-- At an outer radial boundary, C+Z is the incoming eta=1 characteristic.
This proves the sign of the derived flux, not existence of a compatible
boundary condition for the complete metric/clock initial-boundary problem. -/
theorem no_incoming_flux (V N A C Z : ℝ)
    (hV : 0 ≤ V) (hN : 0 ≤ N) (hA : 0 < A) (hin : C+Z=0) :
    radialFlux V N A C Z ≤ 0 := by
  have hZ : Z = -C := by linarith
  rw [radialFlux,hZ]
  have hp : 0 ≤ (2*V*N/A)*C^2 := by positivity
  nlinarith only [hp]

#print axioms energy_zero_iff
#print axioms characteristic_factorization
#print axioms expanding_balance_bound
#print axioms no_incoming_flux
end
end ClockConstraintEnergy

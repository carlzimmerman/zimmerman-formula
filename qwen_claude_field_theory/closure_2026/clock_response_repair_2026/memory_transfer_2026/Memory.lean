import Mathlib.Analysis.Complex.Exponential
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace ClockMemory

-- Algebraic derivative of det M for M' = [[a,b],[c,-a]] M.
theorem determinant_rate_zero (a b c w x y z : ℝ) :
    (a*w+b*y)*z+w*(c*x-a*z)-(a*x+b*z)*y-x*(c*w-a*y)=0 := by ring

theorem invertible_memory (w x y z u v : ℝ)
    (hdet : w*z-x*y=1) (h1 : w*u+x*v=0) (h2 : y*u+z*v=0) :
    u=0 ∧ v=0 := by
  have hu : (w*z-x*y)*u=0 := by nlinarith [congrArg (fun t => t*z) h1, congrArg (fun t => t*x) h2]
  have hv : (w*z-x*y)*v=0 := by nlinarith [congrArg (fun t => t*w) h2, congrArg (fun t => t*y) h1]
  rw [hdet] at hu hv
  constructor <;> linarith

#print axioms determinant_rate_zero
#print axioms invertible_memory

theorem memory_norm_floor (w x y z : ℝ) (hdet : w*z-x*y=1) :
    2 ≤ w^2+x^2+y^2+z^2 := by
  nlinarith [sq_nonneg (w-z),sq_nonneg (x+y)]

#print axioms memory_norm_floor
end ClockMemory

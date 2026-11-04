import Std
namespace AZ25
theorem asymptotic_control : (1:Rat)/9/18^2=1/2916 := by decide +kernel
theorem widths_distinct : (1:Rat)/2916 ≠ 2^2/2916 := by decide +kernel
end AZ25
#print axioms AZ25.asymptotic_control
#print axioms AZ25.widths_distinct

import Std
namespace AZ22
abbrev stationary (xi bSquared : Rat) : Prop := 1-2*xi*bSquared=0

theorem new_root : stationary (1/6) 3 := by decide +kernel

theorem old_root_rejected : ¬ stationary (1/6) 2 := by decide +kernel
end AZ22
#print axioms AZ22.new_root
#print axioms AZ22.old_root_rejected

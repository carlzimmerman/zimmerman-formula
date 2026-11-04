import Std
namespace AZ21
abbrev stationary4 (xi bSquared : Rat) : Prop := 3*xi*bSquared = 1

theorem conformal_benchmark : stationary4 (1/6) 2 := by decide +kernel

theorem benchmark_not_unit : ¬ stationary4 (1/6) 1 := by decide +kernel

theorem tuned_comparator : stationary4 (1/3) 1 := by decide +kernel
end AZ21
#print axioms AZ21.conformal_benchmark
#print axioms AZ21.benchmark_not_unit
#print axioms AZ21.tuned_comparator

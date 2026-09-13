import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination

namespace SourceADMIdentity

/- Real-algebra consequences of the displayed ADM rows. Time derivatives,
action variation, gauge reconstruction, background field equations, dust
conservation and existence of a differentiable solution are NOT formalized.
The variables with suffix d below denote independently supplied real jets. -/

theorem momentum_from_shift
    (M v theta n W sigma ell : ℝ)
    (hshift : 2*M*v-2*theta*n+W*sigma=0) :
    -6*M*v+6*theta*n+2*M*ell-3*W*sigma=2*M*ell := by
  linear_combination -3*hshift

theorem shift_evolution_from_variational_rows
    (M H r z v vd n nd theta thetad W Wd sigma sigmad ell elld : ℝ)
    (hM : M ≠ 0)
    (hshift : 2*M*v-2*theta*n+W*sigma=0)
    (hdshift : 2*M*vd-2*thetad*n-2*theta*nd+Wd*sigma+W*sigmad=0)
    (hzeta : -6*M*vd+6*thetad*n+6*theta*nd+2*M*elld-3*Wd*sigma-3*W*sigmad
      +3*H*(-6*M*v+6*theta*n+2*M*ell-3*W*sigma)-2*M*r*(z+n)=0) :
    elld+3*H*ell=r*(z+n) := by
  have hzero : (2*M)*(elld+3*H*ell-r*(z+n))=0 := by
    linear_combination hzeta+3*hdshift+9*H*hshift
  have hcoef : 2*M ≠ 0 := mul_ne_zero (by norm_num) hM
  exact sub_eq_zero.mp ((mul_eq_zero.mp hzero).resolve_left hcoef)

theorem no_slip_from_shift_evolution
    (r H n z ell elld : ℝ) (hr : r ≠ 0)
    (hevolution : elld+3*H*ell=r*(z+n)) :
    n-elld/r-2*H*ell/r = -z+H*ell/r := by
  field_simp
  linear_combination -hevolution

#print axioms momentum_from_shift
#print axioms shift_evolution_from_variational_rows
#print axioms no_slip_from_shift_evolution

end SourceADMIdentity

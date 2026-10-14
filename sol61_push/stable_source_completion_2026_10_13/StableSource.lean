import Mathlib
namespace StableSource
-- Generic real parameters avoid silently assuming a QFT implementation.
theorem square_identity (a b l R y : ℝ) :
 a*R^2 + 2*a*b*R*y + l*y^2 =
 a*(R+b*y)^2 + (l-a*b^2)*y^2 := by ring

theorem messenger_identity (c d eta R s : ℝ) :
 (c^2+2*c*d*R+(d^2+eta)*R^2)*s =
 (c+d*R)^2*s+eta*R^2*s := by ring

theorem potential_nonnegative
 (m2 x2 q a b l c d eta h ls R y z s : ℝ)
 (hm : 0 ≤ m2) (hx : 0 ≤ x2) (hq : 0 ≤ q)
 (ha : 0 ≤ a) (hl : 0 ≤ l-a*b^2) (he : 0 ≤ eta)
 (hh : 0 ≤ h) (hls : 0 ≤ ls)
 (hy : 0 ≤ y) (hz : 0 ≤ z) (hs : 0 ≤ s) :
 0 ≤ m2*y+x2*z+q+a*R^2+2*a*b*R*y+l*y^2+
 (c^2+2*c*d*R+(d^2+eta)*R^2)*s+h*y*s+ls*s^2 := by
 have identity :
  m2*y+x2*z+q+a*R^2+2*a*b*R*y+l*y^2+
  (c^2+2*c*d*R+(d^2+eta)*R^2)*s+h*y*s+ls*s^2 =
  m2*y+x2*z+q+a*(R+b*y)^2+(l-a*b^2)*y^2+
  (c+d*R)^2*s+eta*R^2*s+h*y*s+ls*s^2 := by ring
 rw [identity]
 positivity
end StableSource
#print axioms StableSource.square_identity
#print axioms StableSource.messenger_identity
#print axioms StableSource.potential_nonnegative

# Single-clock near-saturation radial obstruction

Freeze before computation. Use the exact static equations and constrained
radial symbol in STATIC_RESULT.md and RADIAL_RESULT.md. No new action,
boundary fit or acceleration coefficient is proposed. This is distinct
from the independent-clock fixed-metric obstruction in DERIVATION.md.

At a regular radial point take r,N,B,X,V,b,K,gamma>0, rho=X+V, d=0,
0<p<a, and s=p/(a-p). The claim to check is that for every fixed positive
choice of these parameters there exist finite large s with Mt>0, Num>0,
D0<0. Thus the formal classical radial squared speed Num/D0 is negative.
Show a sufficient finite threshold using 0<h(s)<s and
s^3/(1+s)>=s^2/2 for s>=1. Exact local static ODE existence must be separated
from a globally sourced solution; finite-s parameters make the right-hand
side smooth. Cite the conditional covariant reconstruction already given
in RADIAL_RESULT.md, not an independently verified stress tensor.

Checks: h bounds via derivatives; exact D0 and speed-comparison identity;
large-s D0/s^2 limit; explicit quadratic upper bound and threshold; positive
Num and Mt at d=0. A diagnostic fixture X=V=1,b=1/10,K=1/2,gamma=1/4,s=100
is evaluated at40/80 digits for implementation agreement <=1e-30 relative
to max(1,absolute value), not for a physical fit. The negative control omits
the negative density-portal s^3 term and must fail the asymptotic coefficient
and fixture-sign comparisons. No all-angle, physical-galaxy, cutoff-valid
instability or global continuation claim. The conclusion concerns the
formal classical action over its unrestricted 0<p<a state domain.

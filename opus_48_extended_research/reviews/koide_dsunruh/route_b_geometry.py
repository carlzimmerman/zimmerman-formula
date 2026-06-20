#!/usr/bin/env python3
"""
ROUTE B -- the GEOMETRIC route to Koide Q=2/3.

Question: does S3/Spin(8)-triality + the framework's forced sqrt(8pi/3)=Z geometry
FORCE the magnitude r=sqrt(2)  (equivalently cos^2 theta = 3/4 of the sqrt-mass vector
to the democratic axis, the 45-deg-class "Koide angle")?

We test, sympy-exact and with PDG numbers:
 (a) the EXACT geometry: Q as a function of the Koide amplitude r and of the angle theta;
     where r=sqrt(2) would have to come from.
 (b) whether ANY framework geometric quantity (Z=sqrt(32pi/3), 8pi/3, sqrt(2/Z)=(3/8pi)^(1/4),
     the cube/gauge 8/12) FORCES r=sqrt(2) -- or leaves r free.
 (c) the decisive cross-fermion check: does the same democratic-angle geometry give
     Q=2/3 for QUARKS and NEUTRINOS too (=> FALSIFIED) or is there a lepton-specific reason?

BOTH WAYS + QUARANTINE: a derivation is valid only if it (1) does NOT input 2/3 / r=sqrt(2)
by hand, and (2) passes cross-fermion falsification.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("ROUTE B  --  GEOMETRIC derivation attempt for Koide Q=2/3 / r=sqrt(2) / theta=45deg")
print("="*78)

# ---------------------------------------------------------------------------
# (a) THE EXACT GEOMETRY
# ---------------------------------------------------------------------------
print("\n[a] EXACT GEOMETRY  (sympy, no numbers smuggled)\n"+"-"*70)

# Koide's circulant ansatz: sqrt(m_i) = M ( 1 + r cos(2 pi i/3 + delta) ), i=0,1,2
M, r, delta = sp.symbols('M r delta', positive=True)
i = sp.symbols('i', integer=True)
phases = [2*sp.pi*0/3 + delta, 2*sp.pi*1/3 + delta, 2*sp.pi*2/3 + delta]
sqrt_m = [M*(1 + r*sp.cos(ph)) for ph in phases]

S1 = sp.simplify(sum(sqrt_m))            # sum sqrt(m_i)
S2 = sp.simplify(sum(s**2 for s in sqrt_m))  # sum m_i
Q = sp.simplify(S2 / S1**2)
Q = sp.simplify(sp.expand_trig(Q))
# The famous identity: sum cos = 0, sum cos^2 = 3/2  => Q = (3/2)(1+ r^2/2) / (3/2 * ... )
# Compute directly:
Q_simpl = sp.simplify(Q.rewrite(sp.cos))
print("Q(r,delta) raw       =", Q)
# force the trig identities sum cos(2pi i/3+d)=0 , sum cos^2 = 3/2
Q_of_r = sp.nsimplify(sp.simplify(Q.subs(delta, sp.Rational(0))) )  # delta=0 representative
print("Q at delta=0         =", sp.simplify(Q.subs(delta,0)))
# General closed form: Q = (1 + r^2/2)/( ... ). Let's get the delta-independent closed form:
# sum sqrt = 3M ; sum m = M^2 sum(1+r cos)^2 = M^2 (3 + 0 + r^2 * 3/2)
S1c = 3*M
S2c = M**2*(3 + r**2*sp.Rational(3,2))
Qc = sp.simplify(S2c/S1c**2)
print("Q closed form        = (3 + (3/2) r^2)/9  =", Qc, "  = 1/3 + r^2/6")
assert sp.simplify(Qc - (sp.Rational(1,3)+r**2/6))==0
print("  => Q = 1/3 + r^2/6   (DELTA-INDEPENDENT: Q depends ONLY on amplitude r, never phase)")

# Solve Q=2/3 for r:
r_sol = sp.solve(sp.Eq(Qc, sp.Rational(2,3)), r)
print("  Q=2/3  <=>  r =", r_sol, "  => r = sqrt(2)")

# Angle form (Foot). v=(sqrt m_i), n=(1,1,1).  sum sqrt(m)=v.n , sum m=|v|^2.
#   Q = |v|^2/(v.n)^2 ;  cos^2 theta = (v.n)^2/(|v|^2 |n|^2) = (v.n)^2/(3|v|^2)
#   => Q = 1/(3 cos^2 theta).   Q=2/3 <=> cos^2 theta = 1/2 <=> theta = 45deg  (FOOT).
costh2 = sp.symbols('c', positive=True)  # cos^2 theta
Q_angle = 1/(3*costh2)
cth_sol = sp.solve(sp.Eq(Q_angle, sp.Rational(2,3)), costh2)
print("  Q = 1/(3 cos^2 theta); Q=2/3 <=> cos^2 theta =", cth_sol, " => 1/2  => theta = 45 deg")
print("     (FOOT 1994: the sqrt-mass vector sits at exactly 45deg to the democratic axis (1,1,1).)")

# relation r <-> cos^2 theta
# |v|^2 = sum m = S2c ; (v.n)^2 = S1c^2 ; |n|^2 = 3
costh2_of_r = sp.simplify(S1c**2/(S2c*3))
print("  cos^2 theta(r) =", costh2_of_r, "  (=> r=sqrt2 gives", costh2_of_r.subs(r,sp.sqrt(2)),"=1/2 check)")
assert sp.simplify(costh2_of_r.subs(r,sp.sqrt(2)) - sp.Rational(1,2))==0
# and consistency Q=1/(3 cos^2theta) with Q=1/3+r^2/6:
assert sp.simplify((1/(3*costh2_of_r)) - Qc)==0
print("  CONSISTENCY: Q=1/(3 cos^2 theta(r)) == 1/3 + r^2/6  (sympy-verified)")

print("""
  KEY STRUCTURAL FACT (the crux of the whole route):
  ---------------------------------------------------
  Q is a smooth monotone function of r with NO distinguished point at r=sqrt(2).
  Q(0)=1/3 (degenerate masses), Q(r)->oo as r->oo. r=sqrt(2) gives Q=2/3 but is an
  ORDINARY INTERIOR value: it is NOT a boundary, NOT a positivity limit, NOT an
  extremum, NOT a rep-theory dimension. So ANY mechanism that sets Q=2/3 MUST
  separately supply the single real number r=sqrt(2). The question is whether the
  framework geometry forces THAT NUMBER.
""")

# Positivity bounds on r (so all sqrt(m_i)>0 real): 1 + r cos(...) > 0 for all i
# worst case cos=-1 => r<1 for strict positivity of EVERY entry... but Koide allows
# the smallest sqrt to be small/zero. Let's get the boundary where smallest entry =0.
print("[a'] Is r=sqrt(2) a positivity boundary?  (the only candidate 'forcing' from geometry)")
# min over phase of (1 + r cos) = 1 - r  (at cos=-1). =0 at r=1.
# But the REAL leptons: do they hit cos=-1? Find delta from data later. For r>1 one entry
# of (1+r cos) goes negative for SOME phase, but Koide's delta is chosen so the three
# SAMPLED phases avoid it. r=sqrt(2)>1 => NOT the all-positive boundary r=1.
print("  All-entries-positive for ALL phases requires r<=1. r=sqrt(2)=1.414>1.")
print("  => r=sqrt(2) is NOT a positivity-forced boundary; it sits in the regime where")
print("     the ansatz only stays positive for a RESTRICTED delta window. NOT forced by")
print("     positivity. (Confirms banked: r free, interior point.)")

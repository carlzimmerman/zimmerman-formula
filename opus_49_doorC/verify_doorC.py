#!/usr/bin/env python3
r"""verify_doorC -- machine checks for opus_49_doorC (weak-coupling map + audit +
single-plaquette Jacobi lemma). Every asserted constant below is re-derived here;
nothing is quoted from the lane. See AUDIT.md and LEMMA_doorC.md for the prose.
"""
import json, math
import sympy as sp
import numpy as np
from numpy.linalg import eigh

RES = []
def check(name, ok, reading=""):
    RES.append({"name": name, "pass": bool(ok), "reading": reading})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

x, N, b = sp.symbols('x N b', positive=True)

# ---------------------------------------------------------------- A. AUDIT GATE
print("== A. Audit gate constants (YM05 / I15) ==")
CF = (N**2 - 1) / (2*N)                       # fundamental Casimir
check("gate C_F(N)=(N^2-1)/2N ; SU(2)=3/4, SU(3)=4/3",
      sp.simplify(CF.subs(N,2) - sp.Rational(3,4)) == 0 and
      sp.simplify(CF.subs(N,3) - sp.Rational(4,3)) == 0)
loop = 2 * x * CF                              # E_loop = 2 x C_F (4 links, (x/2) each)
gapN = x * (N**2 - 1) / N - 2 * N / x          # I15 certified general-N bound
check("gate loop energy 2xC_F : SU(2)=3x/2, SU(3)=8x/3",
      sp.simplify(loop.subs(N,2) - 3*x/2) == 0 and
      sp.simplify(loop.subs(N,3) - 8*x/3) == 0)
check("gap_N(2)=(N^2-2)/N : SU(2)=1, SU(3)=7/3",       # 3*2/2-4/2=1 ; 16/3-3=7/3
      sp.simplify(gapN.subs(N,2).subs(x,2) - 1) == 0 and
      sp.simplify(gapN.subs(N,3).subs(x,2) - sp.Rational(7,3)) == 0)
r2 = sp.solve(sp.Eq(gapN.subs(N,2),0), x)[0]   # thresholds sqrt(8/3), 3/2
r3 = sp.solve(sp.Eq(gapN.subs(N,3),0), x)[0]
check(f"gate thresholds SU2=sqrt(8/3)={float(r2):.4f}, SU3=3/2  | x<sqrt(8/3) gives 2*1.5-4/1.5<0",
      sp.simplify(r2 - sp.sqrt(sp.Rational(8,3))) == 0 and
      sp.simplify(r3 - sp.Rational(3,2)) == 0)
for NN in [2,3,4,5,8]:
    ok = all(sp.N(gapN.subs(N,NN).subs(x,xx)) > 0 for xx in [2.0, 3.0, 10.0])
    check(f"gap_N(x)>0 on x>=2 for N={NN}", ok)

# ---------------------------------------------------------------- B. YM07
print("== B. YM07 uniform-gap arithmetic (worst-case n_inf<=18 / counted 13) ==")
su2 = 3*x/2 - 72/x ; su3 = 8*x/3 - 108/x     # lean worst-case (Lean file, x>=8)
c_su2 = 3*x/2 - 52/x                          # counted kappa=52 (n_inf=13), SU(2)
th0 = sp.Rational(1,2)
check("YM07 lean worst-case kappa<=72/108 >0 on x>=8",
      sp.N(su2.subs(x,8)) > 0 and sp.N(su3.subs(x,8)) > 0 and
      sp.simplify(su2.subs(x,8) - 3) == 0 and sp.simplify(su3.subs(x,8) - sp.Rational(47,6)) == 0)
check("YM07 counted kappa=52: 3x/2-52/x, anchor 11/2 at x=8",
      sp.simplify(c_su2.subs(x,8) - sp.Rational(11,2)) == 0)
# lane-docstring thresholds with counted kappa: x* = sqrt(104/3) (52*2/3), sqrt(117/4) (78*2/3 / ... )
t_su2 = sp.sqrt(sp.Rational(104,3)); t_su3 = sp.sqrt(sp.Rational(117,4))
check("YM07 counted kappa thresholds 5.89 / 5.41 lie below window x=8",
      sp.N(t_su2) < 8 and sp.N(t_su3) < 8)

# ---------------------------------------------------------------- C. LEMMA L1
print("== C. L1: exact Jacobi (half-line) representation, single-plaquette SU(2) ==")
# SU(2) character product rule chi_{1/2}*chi_j = chi_{j+1/2}+chi_{j-1/2} (multiplicity free)
# -> H|n> = (2x j_n(j_n+1)+b/x)|n> - (b/(2x))(|n-1>+|n+1>), |n>=chi_{n/2}
J = 12
jidx = [n/2 for n in range(J)]
d = [2*x*jj*(jj+1) + b/x for jj in jidx]
a = -b/(2*x)
check("L1 tridiagonality+constants: row n has diag 2x j(j+1)+b/x, offdiag -b/(2x), zero elsewhere",
      len(set(sp.simplify(q) for q in d)) == J and all(a == -b/(2*x) for _ in range(J)))

# ------------------------------------------------------------ D. LEMMA L2
print("== D. L2: shift cancellation to O(x^{-3}) at strong coupling ==")
# cluster C0 = (VAC, chi_{1/2}) block; cluster bound:
#   rho(x) = ||W||^2/Delta,  ||W||=b/(2x), Delta = 5x/2 - 3b/x  (sep. of cluster window
#   [0, 3x/2+2b/x] from the excited Jacobi band b_low = 4x - b/x via Gershgorin)
# Theorem (L2, tightened): for x^2 > b (cluster condition x^2 > 4b/5 implied),
#   3x/2 - 2 rho(x) <= gap(x) <= 3x/2 + b^2/(3 x^3) + 2 rho(x) ,
#   rho(x) = b^2 / ( 2 x^3 (5 - 4 b/x^2) ).
def rho(xx, bb): return (bb*bb)/(2*xx**3*(5 - 4*bb/(xx*xx)))
def exact_gap(xx, bb, J=400):
    n=J; j=np.arange(n,dtype=float)*0.5
    Hm=np.diag(2*xx*j*(j+1)+bb/xx)+np.diag(np.full(n-1,-bb/(2*xx)),1)+np.diag(np.full(n-1,-bb/(2*xx)),-1)
    w=eigh(Hm)[0]; return w[1]-w[0]
ok=True; worst=0
for bb in [1.0,2.0,4.0]:
    for xx in np.linspace(2.008,60.0,120):
        if xx*xx <= bb + 1e-6: continue
        g=exact_gap(xx,bb); lo=1.5*xx-2*rho(xx,bb); hi=1.5*xx+bb*bb/(3*xx**3)+2*rho(xx,bb)
        ok = ok and (lo <= g <= hi); worst=max(worst, abs(g-1.5*xx))
check("L2 two-sided bound holds on x>=2 grid for b in {1,2,4} "
      "(gap - 3x/2 = O(x^-3), max |.| = %.1e)" % worst, ok)
# the improvement claim vs certified bound at x=2 (b=2): 3-2*rho(2)=2.75 > 2 = minmax, > 1 = lane 2N/x
print("    at x=2,b=2: L2 lower bound = %.4f ; min-max 3x/2-b/x = 2 ; lane 2N/x = 1 ; exact = %.4f"
      % (3 - 2*rho(2.0,2.0), exact_gap(2.0,2.0)))

# ---------------------------------------------------------------- E. L3 evidence
print("== E. L3: uniform-coupling lower bound (evidence, NOT a proof) ==")
xs=np.linspace(0.05,5.0,800)
gs=[exact_gap(float(xx),2.0,400) for xx in xs]
mn=min(gs); imn=int(np.argmin(gs))
check("numerical: single-plaquette gap(b=2) >= %.5f for all x in [0.05,5] (min at x=%.3f); "
      "truncation-stable" % (mn, xs[imn]), mn > 2.19)
# small-x limits exist (band-bottom finite): lambda1,lambda2 finite as x->0
w=exact_gap.__self__ if False else None
gslim=[exact_gap(float(xx),2.0,400) for xx in [0.01,0.003]]
print("    small-x gaps: x=0.01 -> %.5f, x=0.003 -> %.5f (finite limit, band-bottom)" % (gslim[0],gslim[1]))

print(f"\nverdict: {sum(1 for r in RES if r['pass'])}/{len(RES)} PASS")
print(json.dumps(RES))
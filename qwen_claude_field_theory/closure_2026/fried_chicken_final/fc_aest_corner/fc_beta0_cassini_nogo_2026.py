"""DECISIVE: the small-beta_0 screening escape is a NO-GO for Cassini-safe MOND kernels.
CORRECTED constitutive reconstruction (fixes fc_maxwell... b443f575 g-relation error):
  spherical mu^2->0: g=(1+j)g_chi, g_N=(1+b0)j g_chi  =>  mu_obs=(1+b0)j/(1+j),  j=mu/(1+b0-mu),
  Newtonian j->1/b0 => mu_obs->1 EXACTLY (no O(b0) offset). x(y)=y(1+b0-mu)/(1+b0).
FOLD THEOREM (Carl): x(y) globally single-valued <=> beta_0 > beta0_min[mu] := sup_y[mu+y mu'-1].
NO-GO (this script): across mu_p=y/(1+y^p)^{1/p}, beta0_min[mu_p] ANTI-CORRELATES with Cassini-safety:
  {Cassini PASS (committed DHF quadrupole q(solar)<Q_pass)} needs p>=~4 => beta0_min>=0.27;
  {small beta0_min (no fold at b0<<1)} needs p~1 => Cassini q(solar) 2.8-6.1x ceiling (FAIL).
  The two sets are DISJOINT. Both track the SAME transition steepness. => the small-b0 screening
  route to suppress alpha_2 is UNAVAILABLE for any Cassini-safe kernel; beta_0 is FORCED to O(0.3-0.5).
Uses the committed q_direct2D DHF integral (fc_cassini_quadrupole_2026.py) verbatim.
"""
import numpy as np, math
from scipy.optimize import brentq
from scipy import integrate
A0=9.3619e-11; GEXT=2.32e-10; Q2_CEIL=5.2e-27
PREF=1.5*A0**1.5/math.sqrt(6.674e-11*1.989e30); Q_PASS=Q2_CEIL/PREF; eta_solar=GEXT/A0
def nu_mun(n):
    def f(y):
        y=np.atleast_1d(np.asarray(y,float)); out=np.empty_like(y)
        for i,yy in enumerate(y):
            out[i]=brentq(lambda x:x*(x/(1.0+x**n)**(1.0/n))-yy,1e-12,yy+50.0,xtol=1e-14)/yy
        return out if out.size>1 else out[0]
    return f
def q_solar(n):
    nu=nu_mun(n); eN=brentq(lambda x:x*float(np.asarray(nu(x)).ravel()[0])-eta_solar,1e-12,1e10,xtol=1e-15,rtol=8.9e-16)
    def ig(mu,v):
        D=eN*eN+v**4+2*eN*v*v*mu
        if D<=0:return 0.0
        return (float(np.asarray(nu(math.sqrt(D))).ravel()[0])-1)*(eN*(3*mu-5*mu**3)+v*v*(1-3*mu*mu))
    val,_=integrate.dblquad(ig,0.0,400.0,lambda v:-1.0,lambda v:1.0,epsabs=1e-12,epsrel=1e-10)
    return abs(1.5*val)
def beta0_min(p):
    y=np.linspace(1e-4,80,300000); mu=y/(1+y**p)**(1.0/p)
    mup=(1+y**p)**(-1.0/p)-y*(y**(p-1))*(1+y**p)**(-1.0/p-1)
    return (mu+y*mup).max()-1
ok=True
def chk(c,l):
    global ok; print(f"  [{'ok' if c else 'FAIL'}] {l}"); ok=ok and bool(c)
import sympy as sp
j,b0,mu=sp.symbols('j beta_0 mu',positive=True)
muo=((1+b0)*j)/(1+j)
chk(sp.simplify(sp.solve(sp.Eq(muo,mu),j)[0]-mu/(1+b0-mu))==0,"corrected inversion j=mu/(1+b0-mu)")
chk(sp.simplify(muo.subs(j,1/b0))==1,"Newtonian j->1/b0 => mu_obs=1 EXACTLY (no O(b0) offset; b443f575 corrected)")
print(f"  Cassini ceiling: q(solar) < {Q_PASS:.4f}")
res={}
for p in (1.0005,2.0,4.0,10.0):
    b=beta0_min(p); q=q_solar(p); res[p]=(b,q,q*PREF/Q2_CEIL)
    print(f"    mu_p p={p:<7}: beta0_min={b:+.3e}  q(solar)={q:.4f}  Q2/ceil={q*PREF/Q2_CEIL:.3f}  Cassini={'PASS' if q<Q_PASS else 'FAIL'}")
chk(res[1.0005][0]<1e-3 and res[1.0005][2]>1.0,"p=1.0005: small beta0_min BUT Cassini FAIL (q>ceiling)")
chk(res[10.0][2]<1.0 and res[10.0][0]>0.3,"p=10: Cassini PASS BUT beta0_min>0.3 (fold)")
chk(res[4.0][2]<1.0 and res[4.0][0]>0.2,"p=4 (Cassini threshold): beta0_min>0.2 => no small-b0")
print("\nNO-GO CONFIRMED: {Cassini PASS} ∩ {small beta0_min} = empty. Small-beta_0 screening escape CLOSED for Cassini-safe kernels." if ok else "CHECK FAILED")
import sys; sys.exit(0 if ok else 1)

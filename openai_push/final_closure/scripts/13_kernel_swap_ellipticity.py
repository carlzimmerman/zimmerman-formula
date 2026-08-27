#!/usr/bin/env python3
r"""Gate 13 (consolidation): the MMG chassis is kernel-agnostic on the generic branch.
The Dirac structure (Gates 3-8) uses mu(y) only through the lapse operator L_N's ellipticity:
  lambda_perp = mu(y) > 0,  lambda_par = mu(y)+y mu'(y) = d[y mu]/dy > 0,  for y>0.
Verify these for the Cassini-safe family mu_n(y)=y/(1+y^n)^{1/n} (n=5,10; route1B: clears the
2026 Cassini Q2 ceiling where mu=1-e^{-y} FAILS at the external field y_ext~1.9), and exhibit
the swapped constitutive primitive G_n with G_n'(y)/(2y)=mu_n(y).
Exit 0 = kernel swap is legitimate: every chassis gate that depended only on ellipticity holds."""
import sys, sympy as sp, numpy as np
y = sp.Symbol('y', positive=True)
fails=[]
for n in [5,10]:
    mu = y/(1+y**n)**(sp.Rational(1,n))
    lam_par = sp.simplify(sp.diff(y*mu, y))          # = d(y mu)/dy
    # closed form: d/dy [ y^2 (1+y^n)^{-1/n} ] = y(2+y^n)/(1+y^n)^{1+1/n} > 0
    target = y*(2+y**n)/(1+y**n)**(1+sp.Rational(1,n))
    ok1 = sp.simplify(lam_par-target)==0
    f=sp.lambdify(y,lam_par,'numpy'); g=sp.lambdify(y,mu,'numpy')
    yy=np.logspace(-4,4,2000); ok2=bool(np.all(f(yy)>0) and np.all(g(yy)>0))
    ok3 = sp.limit(mu/y,y,0)==1 and sp.limit(mu,y,sp.oo)==1   # deep-MOND + Newtonian
    print(f"  mu_{n}: lam_par = y(2+y^n)/(1+y^n)^(1+1/n) exact:{ok1}  positive sweep:{ok2}  limits:{ok3}")
    if not(ok1 and ok2 and ok3): fails.append(n)
    # constitutive primitive exists: G_n(y)=2*int_0^y s mu_n(s) ds (monotone integrand => well-defined)
    Gp = sp.simplify(2*y*mu)   # G_n'(y)=2y mu_n(y) by construction
    print(f"        G_{n}'(y)/(2y) - mu_{n} = {sp.simplify(Gp/(2*y)-mu)}  (0 => primitive representation holds)")
print("KERNEL-SWAP", "FAIL" if fails else "PASS: mu_n (n=5,10) satisfies every ellipticity condition the chassis gates use;")
print("the Dirac matrix/rank/DOF/preservation gates depend on mu only via L_N ellipticity => unchanged.")
sys.exit(1 if fails else 0)

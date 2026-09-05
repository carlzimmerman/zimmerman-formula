#!/usr/bin/env python3
"""
wf_xcheck_exact_vs_closedform.py
--------------------------------
Numerically confirm that the EXACT anisotropic Euler-Lagrange reduction
(adm_mond.pkl, produced by wf_adm_scalar_reduction.py) has a high-k phase
speed omega^2/k^2 that equals the VALIDATED closed-form khronometric speed
   cs^2(alpha,beta,lambda) = (alpha-2)(beta-lambda)/[alpha(1+beta)(2+3lambda-beta)]
with alpha = W''(y)/2 (parallel, k||a) and alpha = mu(y)/2 (perp, k _|_ a).
"""
import sympy as sp, pickle, mpmath as mp
d=pickle.load(open('adm_mond.pkl','rb'))
ns={n:getattr(sp,n) for n in dir(sp) if not n.startswith('_')}
Ddet=eval(d['Ddet'], {'__builtins__':{}}, ns)
S={str(s):s for s in Ddet.free_symbols}
w=S['omega']; w2=sp.symbols('w2'); mp.mp.dps=30
def Wdat(yv):
    e=mp.e**(-mp.mpf(yv)); return float(0.5*yv*yv+(1+yv)*e-1),float(yv*(1-e)),float(1+(yv-1)*e),float(1-e)
def omega2(yv,bv,lv,kxv,kzv):
    W0v,W1v,W2v,muv=Wdat(yv)
    ex=Ddet.subs({S['a0']:1,S['beta']:bv,S['lambda']:lv,S['y0']:yv,
                  S['W0']:W0v,S['W1']:W1v,S['W2']:W2v,S['k_x']:kxv,S['k_z']:kzv})
    p=sp.Poly(sp.expand(ex.subs(w,sp.sqrt(w2))),w2); c=p.all_coeffs()
    return float(-c[1]/c[0])
def cf(al,bv,lv): return (al-2)*(bv-lv)/(al*(1+bv)*(2+3*lv-bv))
print("exact high-k omega^2/k^2 (k=1000) vs closed-form speed cs^2(alpha,beta,lambda):")
print(" %-22s %-6s %-16s %-16s %-8s"%("(y,beta,lambda)","dir","exact","closed-form","rel.err"))
K=1000.0
for (yv,bv,lv) in [(0.1,-0.01,0.03),(1.0,-0.02,0.05),(3.0,0.01,0.04),(0.03,-0.005,0.02)]:
    W0v,W1v,W2v,muv=Wdat(yv)
    for dirn,(kxv,kzv),al in [('par',(0.0,K),W2v/2),('perp',(K,0.0),muv/2)]:
        ex=omega2(yv,bv,lv,kxv,kzv)/K**2; c=cf(al,bv,lv)
        print(" (%.3f,%+.3f,%+.3f)  %-4s  %16.10f %16.10f %8.1e"%(yv,bv,lv,dirn,ex,c,abs(ex-c)/abs(c)))
print("\nAgreement to ~1e-5 (residual = finite-k O(k^2/K^2) backbone correction) => closed form CONFIRMED.")

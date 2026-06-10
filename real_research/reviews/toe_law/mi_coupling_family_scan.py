#!/usr/bin/env python3
"""
Trilemma calc #1b: scan the bath-response -> inertia COUPLING FAMILY against the spec sheet
(MI_BATH_TAIL_CONSTRAINT.md): (i) deep-MOND limit mu ~ x as x->0, (ii) ephemeris-safe tail
(delta_a(Saturn) < 1e-14 m/s^2, Folkner), (iii) the implied a0 vs the SPARC-fitting framework value.

Family (all built from the SAME physics: thermal UDW response in the Deser-Levin bath, T_eff = T_dS*sqrt(1+x^2),
T_U = T_dS*x, x = a/cH; gap eps = E/(k_B T_dS); n(z) = 1/(e^z - 1)):
  F1 gapless difference   : mu = [sqrt(1+x^2)-1]/x                         (Milgrom-99 ansatz; the one killed)
  F2 gapped diff, norm A  : mu = [n(eps/sqrt(1+x^2)) - n(eps)] / n(eps/x)  (normalize by the GAPPED flat response)
  F3 gapped diff, norm B  : mu = eps*[n(eps/sqrt(1+x^2)) - n(eps)] / x     (normalize by the GAPLESS flat response)
  F4 susceptibility       : mu = dT_eff/da / (dT_eff/da)|_flat = x/sqrt(1+x^2)   (differentiate, don't subtract)
Checks: sympy limits where clean; numeric deep-slope (mu/x at x=1e-3) and tail coefficient (x*(1-mu) at large x);
the Saturn anomaly per coupling vs the pinned bounds; the eps* threshold where F2's tail would pass; the a0 row.
Inline, no swarms.  C. Zimmerman 2026-06-10.
"""
import numpy as np, sympy as sp

def n(z):
    z=np.asarray(z,dtype=float)
    out=np.empty_like(z)
    big=z>500; out[big]=np.exp(-z[big])
    out[~big]=1.0/np.expm1(z[~big])
    return out

c=2.998e8; a0_fw=9.36e-11; Z=np.sqrt(32*np.pi/3); cH=Z*a0_fw     # rho_DE footing (kill was footing-robust)
GMsun=1.327e20; r_sat=9.58*1.496e11; gN=GMsun/r_sat**2
BOUND=1e-14   # Folkner, Cassini radiometric (pinned)

# ---------- sympy limits for F1, F4 ----------
x=sp.symbols('x',positive=True); u=sp.symbols('u',positive=True)
F1=(sp.sqrt(1+x**2)-1)/x; F4=x/sp.sqrt(1+x**2)
print("F1 deep:",sp.series(F1,x,0,3).removeO(),"  F1 tail(u=1/x):",sp.expand(sp.series(((sp.sqrt(1+1/u**2)-1)*u),u,0,3).removeO()))
print("F4 deep:",sp.series(F4,x,0,4).removeO(),"  F4 tail(u=1/x):",sp.expand(sp.series(1/sp.sqrt(1+u**2),u,0,4).removeO()))

# ---------- numeric family scan ----------
def mu_F1(xv): return (np.sqrt(1+xv**2)-1)/xv
def mu_F2(xv,eps): return (n(eps/np.sqrt(1+xv**2))-n(eps))/n(eps/xv)
def mu_F3(xv,eps): return eps*(n(eps/np.sqrt(1+xv**2))-n(eps))/xv
def mu_F4(xv): return xv/np.sqrt(1+xv**2)

xd=1e-3; xt=1e6
print("\ncoupling          eps | deep mu/x (want O(1)) | tail x*(1-mu) (want ->0) | Saturn delta_a (bound 1e-14)")
rows=[("F1 gapless-diff",None,mu_F1)]
for eps in (1.0,5.0,13.5,20.0):
    rows.append((f"F2 gapped/normA",eps,lambda xv,e=eps:mu_F2(xv,e)))
for eps in (1.0,5.0,13.5):
    rows.append((f"F3 gapped/normB",eps,lambda xv,e=eps:mu_F3(xv,e)))
rows.append(("F4 susceptibility",None,mu_F4))
xsat=gN/cH
for lab,eps,f in rows:
    deep=f(np.array([xd]))[0]/xd
    tail=xt*(1-f(np.array([xt]))[0])
    # Saturn: solve mu(a/cH)*a = gN by iteration
    a=gN
    for _ in range(200): a=gN/f(np.array([a/cH]))[0]
    da=a-gN
    flag="SAFE" if abs(da)<BOUND else f"DEAD x{abs(da)/BOUND:,.0f}"
    print(f"{lab:17s} {str(eps):>5s} |    {deep:9.3g}       |   {tail:10.4g}          | {da:9.3g}  {flag}")

# ---------- F2's tail threshold eps* (where eps*n(eps)=BOUND/cH) and what it costs the deep end ----------
from scipy.optimize import brentq
eps_star=brentq(lambda e:e*n(np.array([e]))[0]-BOUND/cH,5,40)
print(f"\nF2 tail-safe threshold: eps* = {eps_star:.2f}  (eps*n(eps*) = {BOUND/cH:.3g})")
print(f"   ...but F2 deep-slope at eps*: mu/x|_(x=1e-3) = {mu_F2(np.array([xd]),eps_star)[0]/xd:.3g}  (deep MOND destroyed)")

# ---------- the a0 row ----------
print(f"\nimplied a0:  F1: 2cH = {2*cH:.3e} (= {2*cH/a0_fw:.1f}x framework)")
print(f"             F4:  cH = {cH:.3e} (= {cH/a0_fw:.2f}x framework = Z)")
print(f"             SPARC-fitting framework value: {a0_fw:.3e}")
print("""
READING: within the difference-family, deep-MOND and an ephemeris-safe tail are MUTUALLY EXCLUSIVE (the gap
that suppresses the tail kills the deep limit, and vice versa) -- a see-saw no-go. The single escape inside
the bath family is the SUSCEPTIBILITY coupling F4 (m_eff prop dT_eff/da): it derives mu_standard = x/sqrt(1+x^2)
parameter-free, passes Saturn by 4x margin (quadratic tail), keeps the deep limit -- and lands a0 = cH, i.e.
a factor Z (5.79) above the SPARC value instead of 2Z. The coefficient gap is UNCHANGED in kind (Z remains
data-selected, not derived); what changed is that the tail kill no longer applies to the whole bath route.
F4 is SELECTED by the spec sheet, not derived from first principles -- construction, not derivation.""")

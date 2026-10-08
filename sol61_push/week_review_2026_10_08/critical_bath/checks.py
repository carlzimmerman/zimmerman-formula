#!/usr/bin/env python3
"""Finite checks of an inverse-square threshold bath and domain controls."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gamma, gammaincc, hyp1f1, jv

p=argparse.ArgumentParser()
p.add_argument("--output",required=True)
p.add_argument("--mutate",choices=["none","boundary","jacobian"],default="none")
a=p.parse_args()
checks=[]; rows=[]
def check(name,ok):
    checks.append({"name":name,"passed":bool(ok)})
def close(x,y,tol=2e-8):
    return abs(x-y)<=tol*max(abs(y),1e-8)
def N(nu):
    return math.sqrt(2/gamma(1-nu))
def minus_f(k,nu):
    return N(nu)*k**(.5-nu)*math.exp(-k*k/2)
def plus_f(k,nu):
    return N(nu)*2**(-nu)/gamma(1+nu)*k**(.5+nu)*hyp1f1(1,1+nu,-k*k/2)
def density(E,nu):
    f=plus_f(math.sqrt(E),nu) if a.mutate=="boundary" else minus_f(math.sqrt(E),nu)
    return f*f if a.mutate=="jacobian" else f*f/(2*math.sqrt(E))
def log_integral(f):
    return quad(f,-90,35,epsabs=2e-10,epsrel=2e-10,limit=250)[0]
def I(e,nu):
    return e**(-nu)*math.exp(e)*gamma(nu)*gammaincc(nu,e)
def Iregular(e,nu):
    return log_integral(lambda t:plus_f(math.exp(t/2),nu)**2/(2*math.exp(t/2))*math.exp(t)/(math.exp(t)+e))

for nu in [.2,1/3,.45]:
    # The tested transform is computed from the coordinate wavefunction and Bessel kernel.
    order=nu if a.mutate=="boundary" else -nu
    for k in [.01,.2,1,3]:
        direct=quad(lambda r:N(nu)*math.sqrt(k)*r**(1-nu)*math.exp(-r*r/2)*jv(order,k*r),
                    0,20,epsabs=1e-11,epsrel=1e-11,limit=250)[0]
        check("Bessel_transform_{}_{}".format(nu,k),close(direct,minus_f(k,nu)))
        regular=quad(lambda r:N(nu)*math.sqrt(k)*r**(1-nu)*math.exp(-r*r/2)*jv(nu,k*r),
                     0,20,epsabs=1e-11,epsrel=1e-11,limit=250)[0]
        check("regular_transform_{}_{}".format(nu,k),close(regular,plus_f(k,nu)))
    norm=log_integral(lambda t:density(math.exp(t),nu)*math.exp(t))
    check("spectral_norm_{}".format(nu),close(norm,1))
    for E in [.001,.1,1,5]:
        check("density_{}_{}".format(nu,E),close(density(E,nu),E**(-nu)*math.exp(-E)/gamma(1-nu)))
    for t in [0,1,10,1e3,1e6]:
        # Rescale E by 1+t for long-time quadrature.
        corr=quad(lambda x:density(x/(1+t),nu)*math.exp(-t*x/(1+t))/(1+t),
                  0,60,epsabs=1e-11,epsrel=1e-9,limit=250)[0]
        check("correlator_{}_{}".format(nu,t),close(corr,(1+t)**(-(1-nu)),2e-7))
    chi=(2**(1-nu)-1)/nu
    check("regular_susceptibility_{}".format(nu),close(Iregular(0,nu),chi))
    rows.append({"nu":nu,"regular_chi":chi,"regular_chi_numeric":Iregular(0,nu)})

nu=1/3
A=gamma(nu)**(1/(1+nu))
for d in [1e-2,1e-4,1e-6,1e-8]:
    power=2/(1+nu)
    def calc_i(e):
        if a.mutate=="none":
            return I(e,nu)
        return log_integral(lambda t:density(math.exp(t),nu)*math.exp(t)/(math.exp(t)+e))
    r=brentq(lambda r:r-d**(2-power)*calc_i(r*d**power),1e-10,3*A,xtol=1e-13)
    eps=r*d**power
    check("root_residual_{}".format(d),abs(eps-d*d*calc_i(eps))/eps<1e-7)
    direct=log_integral(lambda t:math.exp((1-nu)*t-math.exp(t))/(gamma(1-nu)*(math.exp(t)+eps)))
    check("resolvent_formula_{}".format(d),close(I(eps,nu),direct,2e-8))
    eps_regular=brentq(lambda r:r-Iregular(r*d*d,nu),.01,5,xtol=1e-12)*d*d
    chi=(2**(1-nu)-1)/nu
    if d==1e-8:
        check("deep_coefficient",close(r,A,2e-4))
        check("regular_quadratic_response",close(eps_regular/(d*d),chi,1e-4))
    rows.append({"D":d,"epsilon":eps,"epsilon_over_D_three_halves":r,
                 "ratio_to_A":r/A,"regular_epsilon_over_D_squared":eps_regular/d**2})

# Domain mixing: exact Bessel overlaps and continuum normalization.
def mix_density(E,zeta):
    k=math.sqrt(E)
    t=zeta*(2/k)**(2*nu)*gamma(1+nu)/gamma(1-nu)
    amp=(minus_f(k,nu)+t*plus_f(k,nu))/math.sqrt(1+2*t*math.cos(math.pi*nu)+t*t)
    return amp*amp/(2*k)
def slope(E,zeta):
    return math.log(mix_density(10*E,zeta)/mix_density(E,zeta))/math.log(10)
check("critical_domain_density_exponent",abs(slope(1e-12,0)+nu)<1e-8)
for zeta in [.01,.1,1]:
    eb=4*(zeta*gamma(1+nu)/gamma(1-nu))**(1/nu)
    t=zeta*(2/math.sqrt(eb))**(2*nu)*gamma(1+nu)/gamma(1-nu)
    check("boundary_scale_{}".format(zeta),close(t,1))
    check("mixed_domain_low_energy_exponent_{}".format(zeta),abs(slope(eb*1e-12,zeta)-nu)<1e-3)
    rows.append({"zeta":zeta,"boundary_energy":eb,"low_energy_density_slope":slope(eb*1e-12,zeta)})

for ell in [0,1,2]:
    centrifugal=(ell+3.5)**2-.25
    interaction=1/9-(ell+3.5)**2
    check("radial_potential_match_{}".format(ell),abs(centrifugal+interaction+5/36)<1e-13)

# Symbolic/rational identities and finite identity-shift control.
from fractions import Fraction
check("critical_potential_exact",Fraction(1,3)**2-Fraction(1,4)==-Fraction(5,36))
H=np.array([[0,-.2,-.1],[-.2,.4,0],[-.1,0,1.3]])
H0=np.diag([0,.4,1.3])
for shift in [-3,.7,10]:
    response=np.linalg.eigvalsh(H)[0]-np.linalg.eigvalsh(H0)[0]
    shifted=np.linalg.eigvalsh(H+shift*np.eye(3))[0]-np.linalg.eigvalsh(H0+shift*np.eye(3))[0]
    check("vacuum_shift_{}".format(shift),abs(response-shifted)<1e-13)

result={"mutate":a.mutate,"passed":all(c["passed"] for c in checks),"checks":checks,
        "summary":{"total":len(checks),"failed":sum(not c["passed"] for c in checks)},
        "A":A,"toy_a0_eta_one":2.25*A*A,"rows":rows,
        "non_claims":["No BFSS spectrum","No selected critical coupling or boundary","No physical vacuum coefficient","No full MONO theory"]}
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result["summary"]))
raise SystemExit(0 if result["passed"] else 1)

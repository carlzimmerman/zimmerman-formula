#!/usr/bin/env python3
"""Finite-halo response scout. No observational fits or physical units selected."""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad_vec
from scipy.interpolate import PchipInterpolator
from scipy.special import gamma,hyp1f1

p=argparse.ArgumentParser()
p.add_argument("--output",required=True)
p.add_argument("--mutate",choices=["none","density_sign"],default="none")
a=p.parse_args()
nu=1/3
N=math.sqrt(2/gamma(1-nu))
A=gamma(nu)**.75
budget=5.364
checks=[]; cases=[]
def check(name,ok):
    checks.append({"name":name,"passed":bool(ok)})
def rho(t,zeta):
    E=math.exp(t); k=math.sqrt(E)
    fm=N*k**(.5-nu)*math.exp(-E/2)
    fp=N*2**(-nu)/gamma(1+nu)*k**(.5+nu)*hyp1f1(1,1+nu,-E/2)
    mix=zeta*(2/k)**(2*nu)*gamma(1+nu)/gamma(1-nu)
    amplitude=(fm+mix*fp)/math.sqrt(1+2*mix*math.cos(math.pi*nu)+mix*mix)
    return amplitude*amplitude/(2*k)
def moments(e,zeta):
    def f(t):
        E=math.exp(t); w=rho(t,zeta)*E/(E+e); u=e/(E+e)
        return w*np.array([1,u,u*u])
    val,err=quad_vec(f,-140,40,epsabs=1e-10,epsrel=3e-9,limit=300)
    return val
for zeta in [.001,.01,.1,1.,10.]:
    chi=(2**(1-nu)-1)/nu+2**(-2*nu)*gamma(1-nu)/(nu*zeta)
    chi_num=moments(0,zeta)[0]
    norm=quad_vec(lambda t:rho(t,zeta)*math.exp(t),-140,40,epsabs=1e-10,epsrel=3e-9)[0]
    check("norm_{}".format(zeta),abs(norm-1)<2e-7)
    check("chi_{}".format(zeta),abs(chi_num/chi-1)<2e-7)
    eta=budget/(2*chi)  # Explicit calibration to the current input budget, not a derivation.
    a0=2.25*eta*eta*A*A
    data=[]
    for e in np.logspace(-20,4,81):
        I,ej,ek=moments(e,zeta)
        D=math.sqrt(e/I)
        xp=(I+ej)/(I*I)
        xpp=2*((ej-ek)*I+ej*ej)/(e*I**3)
        S=2*eta/xp
        DSprime=-4*eta*D*D*xpp/xp**3
        if a.mutate=="density_sign":
            DSprime=-DSprime
        check("mass_monotonic_{}_{}".format(zeta,e),DSprime<=1e-9)
        check("extended_profile_{}_{}".format(zeta,e),S+DSprime>=-2e-8*max(1,S))
        data.append({"epsilon":float(e),"D":D,"y":D/a0,"mass_ratio":S,
                     "D_Sprime":DSprime,"extended_mass_coefficient":S+DSprime})
    check("finite_mass_{}".format(zeta),abs(data[0]["mass_ratio"]/budget-1)<3e-3)
    check("high_field_small_excess_{}".format(zeta),data[-1]["mass_ratio"]<1e-3)
    logy=np.log([r["y"] for r in data])
    logS=np.log([r["mass_ratio"] for r in data])
    interp=PchipInterpolator(logy,logS,extrapolate=False)
    comparison=[]
    for y in [.001,.003,.01,.03,.1,.3,1,3,10,30,100]:
        actual=math.exp(float(interp(math.log(y))))
        target=min(budget,1/math.expm1(math.sqrt(y)))
        dex=math.log10((1+actual)/(1+target))
        comparison.append({"y":y,"model_extra_ratio":actual,"capped_RAR_extra_ratio":target,
                           "total_force_log10_ratio":dex})
    maxdex=max(abs(r["total_force_log10_ratio"]) for r in comparison)
    cases.append({"zeta":zeta,"eta_calibrated":eta,"chi":chi,"chi_numeric":chi_num,
                  "a0_toy":a0,"normalization":norm,"max_force_error_dex":maxdex,
                  "illustrative_005dex_gate":maxdex<=.05,"comparison":comparison,"curve":data})

result={"passed":all(r["passed"] for r in checks),"mutate":a.mutate,"checks":checks,
        "summary":{"total":len(checks),"failed":sum(not r["passed"] for r in checks)},
        "cases":cases,"non_claims":["No selected cold supply","No actual cold matter stress tensor",
          "No observational fit","No full filtered MONO","No derivation of 32pi squared"]}
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result["summary"]))
print(json.dumps([{"zeta":c["zeta"],"max_force_error_dex":c["max_force_error_dex"]} for c in cases]))
raise SystemExit(0 if result["passed"] else 1)

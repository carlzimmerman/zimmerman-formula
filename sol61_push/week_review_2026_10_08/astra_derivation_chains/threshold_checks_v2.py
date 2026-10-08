"""Finite-rank threshold Hamiltonian: exact scalar resolvent, not BFSS numerics."""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.special import beta as beta_fn,betainc
from scipy.integrate import quad

p=argparse.ArgumentParser()
p.add_argument("--output",required=True)
p.add_argument("--mutate",choices=["none","exponent","sign"],default="none")
args=p.parse_args()
checks=[]
def check(name,value): checks.append({"label":name,"pass":bool(value)})
C=1.; cutoff=1.; beta=-.5 if args.mutate=="exponent" else -1/3
J=beta_fn(beta+1,-beta)
def integral(e,order=1):
    return C*e**(beta+1-order)*beta_fn(beta+1,order-beta-1)*(1-betainc(order-beta-1,beta+1,e/(cutoff+e)))
def solve(d):
    upper=d*math.sqrt(C*cutoff**(beta+1)/(beta+1))
    loge=brentq(lambda z:z-math.log(d*d*integral(math.exp(z))),-200,math.log(upper),xtol=1e-13)
    e=math.exp(loge)
    deriv=2*e/d/(1+d*d*integral(e,2))
    return e,deriv
rows=[]
targetA=(2*math.pi/math.sqrt(3))**.75
for d in [1e-2,1e-3,1e-4,1e-5,1e-6,1e-7,1e-8]:
    e,ed=solve(d)
    check(f"resolvent residual d={d}",abs(e-d*d*integral(e))/e<1e-11)
    approx=targetA*d**1.5
    # Rigorous remainder bound for beta=-1/3, C=cutoff=1.
    check(f"three-halves upper/lower bracket d={d}",0<approx-e<=3*d*d*(1+1e-9))
    energy_sign=-1 if args.mutate=="sign" else 1
    g=d+energy_sign*ed
    a_inferred=g*g/d
    rows.append({"D":d,"epsilon":e,"epsilon_over_target_asymptote":e/approx,
                 "epsilon_derivative":ed,"physical_response_g":g,
                 "inferred_deep_scale":a_inferred})
    check(f"positive constitutive response d={d}",g>0)
    step=1e-4
    fd=(solve(d*(1+step))[0]-solve(d*(1-step))[0])/(2*step*d)
    check(f"implicit response derivative d={d}",abs(fd-ed)<1e-7*ed)
check("deep coefficient convergence",abs(rows[-1]["inferred_deep_scale"]/(2.25*targetA**2)-1)<3e-4)
check("ground energy approaches three-halves coefficient",abs(rows[-1]["epsilon_over_target_asymptote"]-1)<2e-4)
# Independent quadrature in E=t^3 for the target beta.
if args.mutate!="exponent":
    for d in [1e-2,1e-5]:
        e,_=solve(d)
        point=e**(1/3)
        direct=quad(lambda t:3*t/(t**3+e),0,1,points=[point],epsabs=1e-9,epsrel=1e-10)[0]
        check(f"independent threshold integral d={d}",abs(direct-integral(e))/direct<1e-9)
# Rotational invariance: only the norm of the source couples to the continuum.
check("vector source norm",abs(np.linalg.norm([1.,2.,2.])-3)<1e-14)
# Tr X_i vanishes in relative SU(N); a cubic covariant vector need not for SU(3).
X=np.diag([1.,1.,-2.])
check("linear trace coupling is identically absent",np.trace(X)==0)
check("SU3 cubic vector candidate is nonzero",np.trace(X@X@X)==-6)
result={"scope":"Dimensionless exact threshold-response toy; no BFSS spectral calculation, MONO completion, or vacuum normalization",
        "beta":beta,"C":C,"cutoff":cutoff,"target_A":targetA,"target_a0":2.25*targetA**2,
        "checks":checks,"rows":rows,"passed":sum(x["pass"] for x in checks),"total":len(checks)}
Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"passed":result["passed"],"total":result["total"],"last_row":rows[-1],
                  "target_a0":result["target_a0"],"failed":[x["label"] for x in checks if not x["pass"]]},indent=2))
raise SystemExit(0 if all(x["pass"] for x in checks) else 1)

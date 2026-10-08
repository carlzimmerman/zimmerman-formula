"""Conditional cosmological bridge and theory filters; no observational fit."""
import argparse
import json
import math
from pathlib import Path
import sympy as s
from scipy.integrate import quad

p = argparse.ArgumentParser()
p.add_argument("--output", required=True)
p.add_argument("--mutate", choices=["none", "sign", "normalization"], default="none")
args = p.parse_args()
checks = []

def check(label, condition):
    checks.append({"label": label, "pass": bool(condition)})

a, w0, wa = s.symbols("a w0 wa", real=True, positive=False)
# a>0 is imposed when evaluating; log derivative uses the algebraic log ratio.
log_ratio = -s.Rational(3, 2)*(1+w0+wa)*s.log(a) - s.Rational(3, 2)*wa*(1-a)
derivative = s.simplify(a*s.diff(log_ratio, a))
check("continuity logarithmic slope", s.simplify(derivative+s.Rational(3,2)*(1+w0+wa*(1-a))) == 0)
check("Lambda gives constant acceleration", s.simplify(log_ratio.subs({w0:-1,wa:0})) == 0)
astar = 1+(1+w0)/wa
check("stationary point coincides with w=-1", s.simplify(derivative.subs(a,astar)) == 0)

def ratio(z, v0, va):
    sign = 1 if args.mutate == "sign" else -1
    return math.exp(1.5*(1+v0+va)*math.log1p(z)+sign*1.5*va*z/(1+z))

models = {
    "Lambda": (-1., 0.),
    "DES_multiprobe_May_2026": (-.82, -.63),
    "Unite_September_2026": (-.861, -.60),
}
rows = []
for name,(v0,va) in models.items():
    for z in [0., .1, .3, .5, 1., 2., 3.]:
        r = ratio(z,v0,va)
        # Independent integration of the continuity equation in redshift.
        log_integral = quad(lambda t: 1.5*(1+v0+va*t/(1+t))/(1+t),0,z,epsabs=1e-12)[0]
        check(f"continuity quadrature {name} z={z}", abs(math.log(r)-log_integral)<1e-11)
        # Hubble-tracking comparator uses the SAME flat CPL background, no radiation.
        om = .305
        hubble = math.sqrt(om*(1+z)**3+(1-om)*r*r)
        rows.append({"model":name,"z":z,"density_tracking_a0_ratio":r,
                     "fixed_mass_deep_MOND_speed_ratio":r**.25,
                     "H_tracking_ratio_flat_CPL_Om_0_305":hubble})
peaks = []
for name,(v0,va) in models.items():
    if va:
        aa=1+(1+v0)/va
        if 0<aa<1:
            z=1/aa-1
            rr=ratio(z,v0,va)
            check(f"local maximum {name}",rr>ratio(z-.001,v0,va) and rr>ratio(z+.001,v0,va))
            peaks.append({"model":name,"z_peak":z,"a0_ratio":rr})

k,c,G,rho=s.symbols("k c G rho", positive=True)
acc=k*c*s.sqrt(G*rho)
area=s.pi*c**4/acc**2
Lambda=8*s.pi*G*rho/c**2
check("comparison area coefficient",s.simplify(area*Lambda-8*s.pi**2/k**2)==0)
testk=s.Rational(1,3) if args.mutate=="normalization" else s.Rational(1,2)
check("32 pi squared requires k=1/2",s.simplify((area*Lambda).subs(k,testk)-32*s.pi**2)==0)
check("k=1/3 counterexample has 72 pi squared",s.simplify((area*Lambda).subs(k,s.Rational(1,3))-72*s.pi**2)==0)

dimension,delta,exponent=s.symbols("dimension delta exponent", positive=True)
delta_needed=s.solve(s.Eq(exponent,dimension/(dimension-delta)),delta)[0]
filters=[]
for D in [3,4]:
    for power in [s.Rational(3,2),s.Integer(3)]:
        dd=delta_needed.subs({dimension:D,exponent:power})
        filters.append({"dimension":D,"response_power":str(power),
                        "required_primary_dimension":str(dd),"vector_lower_bound":D-1,
                        "passes_dimension_bound":bool(dd>=D-1)})
check("4D cubic vector source fails CFT bound",s.Rational(8,3)<3)
check("4D three-halves vector source fails CFT bound",s.Rational(4,3)<3)
check("3D cubic saturates vector current bound",s.Integer(2)==3-1)

X,P,PX,PXX=s.symbols("X P PX PXX", real=True)
energy=2*X*PX-P
check("minimal scalar NEC identity",s.expand(energy+P-2*X*PX)==0)
check("scalar sound-speed identity",s.simplify((PX+2*X*PXX)*(PX/(PX+2*X*PXX))-PX)==0)
result={"scope":"Conditional identities and central-value illustrations, not data likelihood or TOE proof",
        "mutation":args.mutate,"checks":checks,"passed":sum(x["pass"] for x in checks),
        "total":len(checks),"curves":rows,"peaks":peaks,"CFT_filters":filters,
        "primary_input":"https://arxiv.org/abs/2609.05053v2",
        "older_comparator":"https://arxiv.org/abs/2605.27221v2"}
Path(args.output).write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"passed":result["passed"],"total":result["total"],"peaks":peaks,
                  "failed":[x["label"] for x in checks if not x["pass"]]},indent=2))
raise SystemExit(0 if all(x["pass"] for x in checks) else 1)

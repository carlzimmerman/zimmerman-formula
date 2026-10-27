"""Supplementary exact controls; continuum claims are proved in OCCUPIED_ACTION.md."""
import json
import sys
from pathlib import Path
import sympy as s

checks = []


def zero(name, expression):
    result = s.factor(expression)
    if result != 0:
        raise AssertionError((name, str(result)))
    checks.append({"name": name, "kind": "exact_identity", "pass": True})


def truth(name, predicate, kind="exact_inequality"):
    if not bool(predicate):
        raise AssertionError(name)
    checks.append({"name": name, "kind": kind, "pass": True})


r = s.symbols("r", positive=True)
a, G, h, k = s.symbols("a0 G h kappa", positive=True)
u = s.Function("u")(r)
dv = s.diff(u, r, 2) + 2*s.diff(u, r)/r - 2*u/r**2
rho = (s.diff(u, r) + 2*u/r)/(4*s.pi*G)
zero("quadratic EOS longitudinal stiffness", s.diff(k*rho, r)-k*dv/(4*s.pi*G))
V = -u**2/2-a*u-a*a*s.log(1-u/a)
W = -a*u-a*a*s.log(1-u/a)
us = s.symbols("us", positive=True)
zero("full W radial derivative", s.diff(W.subs(u, us), us)-a*us/(a-us))
zero("residual V radial derivative", s.diff(V.subs(u, us), us)-us**2/(a-us))
zero("residual Hessian", s.diff(V.subs(u, us), us, 2)-us*(2*a-us)/(a-us)**2)

# Direct radial functional derivative, including the EOS rather than copying
# the proposed differential equation into the check.
m = s.Function("m")(r)
q = s.Function("Q")(r)
uu = G*m/r**2
rrho = s.diff(m, r)/(4*s.pi*r**2)
R = lambda x: x*x/(a-x)
lag = (r*r/G)*(-uu*uu/2-a*uu-a*a*s.log(1-uu/a)
       +h*(s.diff(uu, r)**2+2*uu*uu/r**2)/2-G*q*uu/r**2)
lag += 4*s.pi*r*r*k*rrho*rrho/2
el = s.diff(lag, m)-s.diff(s.diff(lag, s.diff(m, r)), r)
dvu = s.diff(uu, r, 2)+2*s.diff(uu, r)/r-2*uu/r**2
zero("radial energy Euler derivative", el-(R(uu)-G*q/r**2-(h+k/(4*s.pi*G))*dvu))
zero("radial boundary momentum", s.diff(lag, s.diff(m, r))-(h*s.diff(uu, r)+k*rrho))

# Exact manufactured regular source and occupied state, G=a0=E=1.
stock = s.Rational(1, 10)
hh = s.Rational(1, 200)
kk = s.pi/50
H = hh+kk/(4*s.pi)
mi = stock*(5*r**3/s.Integer(2)-3*r**5/s.Integer(2))
ui = r/4-3*r**3/20
ni = s.Rational(3,16)/s.pi*(1-r*r)
li = s.Rational(3,800)*(1-r*r)
Ri = ui*ui/(1-ui)
Qi = r*r*Ri+s.Rational(3,200)*r**3
di = s.diff(ui, r, 2)+2*s.diff(ui, r)/r-2*ui/r**2
zero("witness mass dictionary", mi-r*r*ui)
zero("witness density divergence", s.diff(mi, r)/(4*s.pi*r*r)-ni)
zero("witness multiplier chemical potential", li-kk*ni)
zero("witness vector Laplacian", di+3*r/2)
zero("witness positive EOS effective stiffness", H-s.Rational(1,100))
zero("witness occupied bulk", -H*di+Ri-Qi/r**2)
zero("witness P reciprocal equation", Ri-hh*di-Qi/r**2-s.diff(li,r))
zero("witness fluid Euler equation", s.diff(li,r)-kk*s.diff(ni,r))
zero("witness total stock integral", s.integrate(4*s.pi*r*r*ni,(r,0,1))-stock)
zero("witness mass derivative factor", s.diff(mi,r)-s.Rational(3,4)*r*r*(1-r*r))
zero("witness central baryon coefficient", s.limit(Qi/r**3,r,0)-s.Rational(3,200))
zero("witness central source density coefficient", s.limit(s.diff(Qi,r)/r**2,r,0)-s.Rational(9,200))
zero("witness baryon total", Qi.subs(r,1)-s.Rational(47,1800))
zero("witness u maximum", ui.subs(r,s.sqrt(5)/3)-s.sqrt(5)/18)
truth("witness sub-saturation bound", s.Rational(5,324)<s.Rational(1,64))
zero("lower-u positivity factor", ui-s.Rational(1,10)-(1-r)*(3*r*r+3*r-2)/20)
zero("baryon derivative decomposition", s.diff(Qi,r)/r**2-(2*Ri/r+s.diff(R(us).subs(a,1),us).subs(us,ui)*s.diff(ui,r)+s.Rational(9,200)))
zero("continuum baryon positive lower bound arithmetic", s.Rational(1,50)-s.Rational(3,49)+s.Rational(9,200)-s.Rational(37,9800))
truth("continuum lower bound strictly positive", s.Rational(37,9800)>0)

uo = stock/r**2
lo_prime = uo*uo/(1-uo)-s.Rational(47,1800)/r**2
zero("edge value matching", ui.subs(r,1)-uo.subs(r,1))
zero("edge normal derivative matching", s.diff(ui,r).subs(r,1)-s.diff(uo,r).subs(r,1))
zero("edge density zero", ni.subs(r,1))
zero("edge lambda zero", li.subs(r,1))
zero("edge pressure zero", (kk*ni**2/2).subs(r,1))
zero("exterior vector Laplacian", s.diff(uo,r,2)+2*s.diff(uo,r)/r-2*uo/r**2)
zero("exterior mass exact", r*r*uo-stock)
zero("exterior reciprocal equation", uo*uo/(1-uo)-s.Rational(47,1800)/r**2-lo_prime)
truth("exterior threshold strict", s.Rational(1,90)<s.Rational(47,1800))
zero("exterior outward multiplier decreases at edge", lo_prime.subs(r,1)+s.Rational(3,200))
# Negative control: the freely varied full-W exterior has a nonzero residual.
truth("omitted multiplier negative control", (uo*uo/(1-uo)-s.Rational(47,1800)/r**2).subs(r,2) != 0)

# These rational samples are implementation controls only; (16) proves
# continuum baryon density positivity independently.
for j in range(1,101):
    point = s.Rational(j,100)
    truth("sample baryon density positivity "+str(point), s.diff(Qi,r).subs(r,point)>0, "rational_sample")
    truth("sample exterior vacuum derivative "+str(j), lo_prime.subs(r,1+s.Rational(j,10))<0, "rational_sample")

out = {
    "claim_id": "CE-CONT-OCC-EXACT-2026-10-18",
    "status": "completed",
    "all_pass": all(c["pass"] for c in checks),
    "n_checks": len(checks),
    "n_symbolic_identities": sum(c["kind"] == "exact_identity" for c in checks),
    "n_exact_inequalities": sum(c["kind"] == "exact_inequality" for c in checks),
    "n_rational_samples": sum(c["kind"] == "rational_sample" for c in checks),
    "checks": checks,
    "scope": "Exact radial action reduction and finite manufactured profile controls; analytic proof supplies continuum positivity and KKT minimization. No formation, conversion, microscopic or relativistic theorem.",
}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({key:value for key,value in out.items() if key != "checks"},indent=2))

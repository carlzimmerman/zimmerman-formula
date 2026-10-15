#!/usr/bin/env python3
"""Bounded exact controls for VC3-VAC-001; the uniform proofs are in PROOF.md."""
import json
import sys
from pathlib import Path
import sympy as s


checks = []


def equal(name, expression):
    reduced = s.factor(s.cancel(expression))
    assert reduced == 0, (name, reduced)
    checks.append(name)


x, delta, D0, h, E, beta, H, eta, weight = s.symbols(
    "x delta D0 h E beta H eta weight", positive=True
)
t = 1 - x
p = t**2
hc = E**2 * x
F = p - beta - E**2 * (t - beta)**2 / (h + E**2 * (t - beta))
N = h * (p - beta) - E**2 * (t - beta) * (t - p)
equal("cone numerator", F * (h + E**2 * (t - beta)) - N)
beta_L = p * delta / (delta + x)
N_R = N.subs(h, hc * (1 + delta))
equal("exact beta ceiling", N_R.subs(beta, beta_L))
equal("negative numerator slope", s.diff(N_R, beta) + hc * (delta + x))
equal("ceiling deficit", 1-beta_L - (delta*(2*x-x**2)+x)/(delta+x))
equal("near threshold x-squared path", beta_L.subs(delta, x**2)-p*x/(1+x))
equal("vanishing ceiling counterlimit", s.limit(beta_L.subs(delta, x**2),x,0))
k=s.symbols("k",positive=True)
equal("finite delta-over-x ceiling",s.limit(beta_L.subs(delta,k*x),x,0)-k/(k+1))
beta_star=beta_L/(1+x)
equal("strict parent separation",beta_L-beta_star-beta_L*x/(1+x))
equal("wedge parent Maxwell limit",s.limit(beta_star,x,0)-1)
e=s.symbols("e",positive=True)
equal("linear t lower bound",1/(1+e)-(1-e)-e**2/(1+e))
equal("linear p lower bound",1/(1+e)**2-(1-2*e)-e**2*(3+2*e)/(1+e)**2)
etaH=H/(1+H)
a=etaH/16
equal("blend E-square-over-h bound",a**2/H-etaH/(256*(1+H)))
equal("safe blend margin",eta/2-2*eta/16-eta/256-95*eta/256)
equal("blend below threshold",(a**2/H)*a-etaH**2/(4096*(1+H)))
b1,b2=s.symbols("b1 b2")
equal("affine cone blending",N.subs(beta,weight*b1+(1-weight)*b2)-weight*N.subs(beta,b1)-(1-weight)*N.subs(beta,b2))
equal("Lorentz vacuum speed",(t/p).subs(x,E/(D0+E))-(1+E/D0))
Le=D0*E-D0**2*s.log(1+E/D0)
equal("constitutive D derivative",s.diff(Le,E)-D0*E/(D0+E))
Hin=D0**2*(-x-s.log(1-x))
tv=s.symbols("tv",positive=True)
legendre=(E*D0*x-Le).subs({E:D0*(1-tv)/tv,x:1-tv})-Hin.subs(x,1-tv)
equal("electric Legendre transform",s.expand_log(s.simplify(legendre),force=False))
gap=Hin-D0**2*x**2/2
equal("positive gap derivative",s.diff(gap,x)-D0**2*x**2/(1-x))
equal("gap zero at origin",s.limit(gap,x,0))
R,Q,sigma,P=s.symbols("R Q sigma P",positive=True)
Db=Q/(4*s.pi*R**2)
Hinside=s.Function("Hin")
# Radius variation at fixed enclosed Q, with local boundary energy densities.
shape=4*s.pi*R**2*(Hinside(Db)-Db**2/2-P)+s.diff(4*s.pi*sigma*R**2,R)
equal("reciprocal pressure balance",shape/(4*s.pi*R**2)-(Hinside(Db)-Db**2/2-P+2*sigma/R))
r=s.symbols("r",positive=True)
outside=s.integrate(4*s.pi*r**2*(Db*R**2/r**2)**2/2,(r,R,s.oo))
equal("finite Maxwell exterior energy",outside-2*s.pi*Db**2*R**3)
Pw=s.log(2)-s.Rational(5,8)
equal("interface state gap",gap.subs({x:s.Rational(1,2),D0:1})-Pw)
equal("polytropic effective inertia",(1+6*Pw)*(1-(s.Rational(6,5)*Pw)/(1+6*Pw))-(1+s.Rational(24,5)*Pw))
equal("rigorous log witness margin",s.Rational(2,3)-s.Rational(5,8)-s.Rational(1,24))

parent_controls=[]
for xv in (s.Rational(1,1000),s.Rational(1,10),s.Rational(1,2),s.Rational(9,10)):
    for dv in (s.Rational(1,10),s.Integer(1),s.Integer(10)):
        ev=xv/(1-xv)
        hv=ev**2*xv*(1+dv)
        bv=beta_star.subs({x:xv,delta:dv})
        fv=s.factor(F.subs({x:xv,E:ev,h:hv,beta:bv}))
        assert 0<bv<(1-xv) and fv>0
        parent_controls.append({"x":str(xv),"delta":str(dv),"F":str(fv)})

blend_controls=[]
for Hv in (s.Rational(1,10**6),s.Integer(1),s.Integer(10**6)):
    etav=Hv/(1+Hv)
    av=etav/16
    for ratio in (s.Rational(1,4),s.Rational(3,4),s.Integer(1)):
        ev=av*ratio
        xv=ev/(1+ev)
        dv=Hv/(ev**2*xv)-1
        bsv=beta_star.subs({x:xv,delta:dv})
        b0v=1-etav/2
        for wv in (s.Integer(0),s.Rational(1,3),s.Rational(2,3),s.Integer(1)):
            bv=wv*b0v+(1-wv)*bsv
            fv=s.factor(F.subs({x:xv,E:ev,h:Hv,beta:bv}))
            assert 0<bv<(1-xv) and fv>0
            blend_controls.append({"H":str(Hv),"E_over_a":str(ratio),"weight":str(wv),"F_positive":True})

result={
    "claim_id":"VC3-VAC-001",
    "symbolic_identities":len(checks),
    "identity_names":checks,
    "exact_parent_controls":len(parent_controls),
    "parent_controls":parent_controls,
    "exact_blend_controls":len(blend_controls),
    "blend_controls":blend_controls,
    "interface_witness":{"D0":1,"rho_b":1,"x":"1/2","P":"log(2)-5/8","h_eff":"1+(24/5)*(log(2)-5/8)","hc":"1/2","pressure_positive_reason":"log(2)=2*atanh(1/3)>2/3>5/8"},
    "non_claims":["Finite controls do not replace uniform proofs.","No global interface equilibrium or stability calculation.","No full vacuum-frame, nonlinear, Einstein, or observational completion."]
}
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({key:result[key] for key in ("claim_id","symbolic_identities","exact_parent_controls","exact_blend_controls")}))

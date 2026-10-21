#!/usr/bin/env python3
"""Exact checks of W4-02's scoped countermodels, never a coefficient selector.

Normal: python3 why_4_puzzle/W4_02_independent_portal_audit/checks.py
Control: W4_02_MUTATE=1 python3 why_4_puzzle/W4_02_independent_portal_audit/checks.py
No measurements, fitted coefficients, numerical scans, or target values enter.
"""
import hashlib
import json
import os
from pathlib import Path
import sys

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
MUTATE = os.environ.get("W4_02_MUTATE", "0") == "1"
CHECKS = []


def check(name, condition, value):
    passed = bool(condition)
    CHECKS.append({"name": name, "passed": passed, "value": str(value)})
    print(f"{'PASS' if passed else 'FAIL'} {name}: {value}")


def zero(expr):
    return s.simplify(expr) == 0


u, a, K, xi, G, eps, rho, c = s.symbols("u a K xi G eps rho c", positive=True)
g, lam, eta, nu = s.symbols("g lam eta nu", positive=True)
t = s.symbols("t", positive=True)
W = a**2 / K * (-u/a - s.log(1-u/a) - u**2/(2*a**2))
Wp = s.factor(s.diff(W, u))
Wpp = s.factor(s.diff(W, u, 2))
check("C01 constitutive derivative", zero(Wp-u**2/(K*(a-u))), Wp)
check("C02 radial Hessian formula", zero(Wpp-u*(2*a-u)/(K*(a-u)**2)), Wpp)
check("C03 transverse Hessian formula", zero(Wp/u-u/(K*(a-u))), s.factor(Wp/u))
check("C04 strict radial convexity on 0<t<1", zero(Wpp.subs(u, a*t)-t*(2-t)/(K*(1-t)**2)), "t(2-t)/(K(1-t)^2)>0; analytic domain 0<t<1")
check("C05 zero vacuum value", zero(W.subs(u, 0)), W.subs(u, 0))
W_source = W.subs(a, s.sqrt(xi*G*eps))
source = s.diff(W_source, eps)
check("C06 zero background density source", zero(source.subs(u, 0)), source.subs(u, 0))
check("C07 no linear background force", zero(Wp.subs(u, 0)), Wp.subs(u, 0))
b = s.Integer(2) if MUTATE else s.Integer(1)
constitutive_g = u+b*K*Wp
u_of_g = a*g/(a+g)
check("C08 simple-mu constitutive elimination", zero(constitutive_g.subs(u,u_of_g)-g), s.factor(constitutive_g.subs(u,u_of_g)-g))
check("C09 simple-mu spherical force", zero(g-u_of_g-g**2/(a+g)), g-u_of_g)
portal = s.sqrt(xi*G*rho*c**2)
check("C10 observable coefficient free", zero(portal**2/(G*rho*c**2)-xi), s.factor(portal**2/(G*rho*c**2)))
scaled = portal.subs({G:lam*G, rho:eta*rho, c:nu*c}, simultaneous=True)
check("C11 G rho c scaling", zero(scaled-nu*s.sqrt(lam*eta)*portal), scaled/portal)
check("C12 nonzero response to portal coupling", zero(s.diff(portal,xi)-portal/(2*xi)), s.diff(portal,xi))

# Independent preferred-frame toy: physical Phi, fixed source normalization.
E = (g**2/2-a*g+a**2*s.log(1+g/a))/K
mu = g/(a+g)
transverse = s.factor(K*s.diff(E,g)/g)
longitudinal = s.factor(K*s.diff(E,g,2))
check("C13 toy static force", zero(K*s.diff(E,g)-g*mu), K*s.diff(E,g))
check("C14 transverse cone", zero(transverse-mu), transverse)
check("C15 longitudinal cone", zero(longitudinal-(1-a**2/(a+g)**2)), longitudinal)
check("C16 cone range by factorization", zero(1-transverse-a/(a+g)) and zero(1-longitudinal-a**2/(a+g)**2), "0<mu<1 and 0<1-a^2/(a+g)^2<1 for a,g>0")
check("C17 toy vacuum and source vanish", zero(E.subs(g,0)) and zero(s.diff(E.subs(a,s.sqrt(xi*G*eps)),eps).subs(g,0)), E.subs(g,0))
check("C18 deep response normalization", s.limit(mu/g,g,0)==1/a, s.limit(mu/g,g,0))
check("C19 strong response normalization", s.limit(mu,g,s.oo)==1, s.limit(mu,g,s.oo))

Y, B = s.symbols("Y B",positive=True)
p = s.Integer(2) if MUTATE else s.Integer(3)
f = B*Y**(p/2)
cs2 = s.factor((s.diff(f,Y)+2*Y*s.diff(f,Y,2))/s.diff(f,Y))
check("C20 Lorentz cubic cone", cs2==2, cs2)
check("C21 cone ignores amplitude", zero(s.diff(cs2,B)), s.diff(cs2,B))

n = s.symbols("n",integer=True,positive=True)
Omega = 2*s.pi**(n/2)/s.gamma(n/2)
check("C22 dimensional portal", tuple(s.simplify(x) for x in (n+2-n,-1+1,-2-2))==(2,0,-4), "[G_n epsilon]=(L^n M^-1 T^-2)(M L^(2-n) T^-2)=L^2 T^-4")
check("C23 Gauss spheres", Omega.subs(n,3)==4*s.pi and Omega.subs(n,4)==2*s.pi**2, (Omega.subs(n,3),Omega.subs(n,4)))
check("C24 Gauss normalization cancels", zero(s.factor(((Omega*G)*Wp).subs({K:Omega*G}))-u**2/(a-u)), "K_n W'=u^2/(a-u) for every n")

# Source-dependent equations, checked against the pinned v3 source in REPORT.md.
q, mass, tension, gamma, beta, rratio = s.symbols("q mass tension gamma beta rratio",positive=True)
Mpl = 1/s.sqrt(8*s.pi*G)
rdbi2 = beta*mass/(4*s.pi*Mpl*s.sqrt(tension))
amon = s.factor(rratio**2*G*mass/rdbi2)
xi_dbi = s.factor(amon**2/(G*tension*gamma))
check("C25 screening radius bridge", zero(amon-rratio**2*s.sqrt(tension)/(2*beta*Mpl)), amon)
check("C26 DBI retains two couplings", zero(xi_dbi-2*s.pi*rratio**4/(beta**2*gamma)), xi_dbi)
v = s.symbols("v", real=True)
Ldbi = -tension*s.sqrt(1+v**2/tension)
kinetic = s.factor(s.diff(Ldbi,v,2))
check("C27 DBI time Hessian negative", zero(kinetic+(1+v**2/tension)**s.Rational(-3,2)), kinetic)

inputs = [
    "why_4_puzzle/README.md",
    "why_4_puzzle/W4_02_independent_portal_audit/FROZEN_CRITERIA.md",
    "FRAMEWORK_EQUATIONS_2026-10-15.md",
    "campaign_fresh_gravity/CFG911_kappa_constructive_coupling/README.md",
    "campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CAMPAIGN_RULES.md",
]
hashes = {path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in inputs}
hashes["checks.py"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
result = {"mode":"MUTATE" if MUTATE else "normal", "sympy":s.__version__,
          "checks":CHECKS, "input_sha256":hashes,
          "non_claims":["No coefficient is predicted", "Static toy is not a full relativistic theory", "Symbolic identities do not prove full-system stability"]}
out = HERE/("results_MUTATE.json" if MUTATE else "results.json")
out.write_text(json.dumps(result,indent=2)+"\n")
failed = [r["name"] for r in CHECKS if not r["passed"]]
print(f"{len(CHECKS)-len(failed)}/{len(CHECKS)} PASS; failures={failed}; mode={result['mode']}")
sys.exit(1 if failed else 0)

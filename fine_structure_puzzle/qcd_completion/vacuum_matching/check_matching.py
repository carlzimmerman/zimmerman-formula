#!/usr/bin/env python3
"""Exact source-to-target algebra, plus finite high-precision diagnostics. No fit."""
import json
import pathlib
import platform
import sys

import mpmath as mp
import sympy as s

out = pathlib.Path(sys.argv[1])
source = json.loads(pathlib.Path(__file__).with_name("source_equations.json").read_text())
D, a, b, nu = s.symbols("D a b nu", positive=True)
q, v, T, r, R, r0, adef = s.symbols("q v T r R r0 adef", positive=True)
c = 74/(9*s.pi)+8*s.EulerGamma/(3*s.pi)-23*s.pi/54
A = 1/a+1/b
F = (A-c-4/(3*s.pi)*s.log(a*b*D**2/s.pi**2))/D
derivative_source = (4/(3*s.pi)*s.log(a*b*D**2/s.pi**2)-A+50/(9*s.pi)+8*s.EulerGamma/(3*s.pi)-23*s.pi/54)/D**2
checks = {}
checks["eq55_derivative_matches_eq54"] = s.simplify(s.diff(F,D)-derivative_source) == 0
# J contains precisely 1+2*pi/(a*b*D), and a+b=2*pi.
checks["jacobian_inverse_core_masses"] = s.simplify((A-2*s.pi/(a*b)).subs(b,2*s.pi-a)) == 0
W = s.expand(-F+A/D)
expected = (4/(3*s.pi)*s.log(a*b*D**2/s.pi**2)+c)/D
checks["core_inverse_masses_cancel"] = s.simplify(W-expected) == 0
Wnu = s.expand_log(expected.subs({a:2*s.pi*nu,b:2*s.pi*(1-nu)}),force=True)
checks["center_weight_correction"] = s.simplify(Wnu.subs(nu,s.Rational(1,2))-(8*s.log(D)/(3*s.pi)+c)/D) == 0
P=q**2*(2*s.pi*T-q)**2/(12*s.pi**2*T)
U=4*adef*T**3*s.cos(q/(2*T))**2
P2=s.simplify(s.diff(P,q,2).subs(q,s.pi*T))
V2=s.simplify(s.diff(P+U,q,2).subs(q,s.pi*T))
V4=s.simplify(s.diff(P+U,q,4).subs(q,s.pi*T))
checks["GPY_center_curvature"] = s.simplify(P2+T/3) == 0
checks["deformed_center_curvature"] = s.simplify(V2-T*(2*adef-s.Rational(1,3))) == 0
checks["deformed_fourth_derivative"] = s.simplify(V4-(2/s.pi**2-2*adef)/T) == 0
# A quartic potential makes the Coulomb-tail radial primitive exact.
radial_integrand=s.expand(4*s.pi*r**2*(P.subs(q,v-1/r)-P.subs(q,v)))
primitive=(-2*s.pi*s.diff(P,q).subs(q,v)*r**2
           +2*s.pi*s.diff(P,q,2).subs(q,v)*r
           -2*s.pi*s.diff(P,q,3).subs(q,v)*s.log(r)/3
           -s.pi*s.diff(P,q,4).subs(q,v)/(6*r))
checks["quartic_potential_tail_primitive"] = s.simplify(s.diff(primitive,r)-radial_integrand) == 0
center_tail=s.simplify(primitive.subs({r:R,v:s.pi*T}))
checks["GPY_center_tail"] = s.simplify(center_tail-(-2*s.pi*T*R/3-1/(3*s.pi*T*R))) == 0
# Center symmetry removes odd derivatives; only the R and R^-1 terms are asserted.
deformed_tail=s.simplify(2*s.pi*V2*R-s.pi*V4/(6*R))
checks["deformed_center_tail"] = s.simplify(deformed_tail-(2*s.pi*T*(2*adef-s.Rational(1,3))*R+(s.pi*adef/3-1/(3*s.pi))/(T*R))) == 0
checks["center_caloron_growth"] = s.simplify((-2*s.pi*D*(s.Rational(2,3)-4*nu*(1-nu))).subs(nu,s.Rational(1,2))-2*s.pi*D/3) == 0
assert all(checks.values()), checks
mp.mp.dps=60
cn=mp.mpf(74)/(9*mp.pi)+8*mp.euler/(3*mp.pi)-23*mp.pi/54
rows=[]
for n in [10,30,100]:
    dn=mp.mpf(n)
    rows.append({"D":n,"center_log_weight_correction":str((8*mp.log(dn)/(3*mp.pi)+cn)/dn)})
# Orthogonal coefficient check: numerical integration of the quartic potential,
# against the independently differentiated closed primitive; no asymptotic fit.
quad_rows=[]
for n in [3,10,30]:
    pn=lambda x: x*x*(2*mp.pi-x)**2/(12*mp.pi**2)
    numerical=mp.quad(lambda rr: 4*mp.pi*rr*rr*(pn(mp.pi-1/rr)-pn(mp.pi)),[2,n])
    prim=lambda rr: -2*mp.pi*rr/3-1/(3*mp.pi*rr)
    exact=prim(mp.mpf(n))-prim(mp.mpf(2))
    rel=abs(numerical-exact)/max(1,abs(exact))
    assert rel<mp.mpf("1e-50")
    quad_rows.append({"T":1,"v":"pi","r0":2,"R":n,"relative_discrepancy":str(rel)})
result={"assertion_tested":"Exact algebra and declared finite quadratures for the extracted neutral-caloron asymptotic and local-potential tail; no determinant is newly evaluated.","checks":checks,"c":str(cn),"finite_diagnostics":rows,"orthogonal_quadratures":quad_rows,"formulae":{"center_weight_correction":str((8*s.log(D)/(3*s.pi)+c)/D),"deformed_center_tail":str(deformed_tail),"higgs_mass_squared":"g^2*T^2*(2*adef-1/3)"},"software":{"python":platform.python_version(),"sympy":s.__version__,"mpmath":mp.__version__},"input_source_id":source["primary_source"]["id"],"non_claims":["No finite-wall all-mode determinant", "No new proof of DGPS Green-function calculation", "No curved-space or strong-QCD stress", "No fitted coefficient", "No electromagnetic-alpha identification"]}
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))

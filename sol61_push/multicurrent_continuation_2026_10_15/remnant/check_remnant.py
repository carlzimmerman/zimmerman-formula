"""Exact identities and finite quadrature checks for a dilute remnant.

Run with an output JSON path. Scientific domains are in contract.json and PROOF.md.
No source simulation or finite-abundance backreaction is implemented here.
"""
import json
import sys
from pathlib import Path

import mpmath as mp
import sympy as sp


checks = []


def exact(name, expression):
    residual = sp.simplify(expression)
    if residual != 0:
        raise AssertionError((name, residual))
    checks.append({"name": name, "residual": "0"})


r, s, b, u, g = sp.symbols("r s b u g", positive=True)
re = sp.sqrt(s + s**2)
u0 = (sp.sqrt(1 + 4*r*r) - 1)/(2*r*r)
g0 = 1/r**2 + u0
primitive = sp.asinh(2*r) - (1 + sp.sqrt(1 + 4*r*r))/(2*r)
aout = -(1+s)/r**2 + b*s/(r**2-s)
numerator = ((b-1)*s-1)*r**2+s*(1+s)
exact("static constitutive equation", u0*u0/(1-u0)-1/r**2)
exact("interior remnant acceleration", -g + b*g - (b-1)*g)
exact("two-dust force difference", (-g+b*u)-(-g+u)-(b-1)*u)
exact("interior gravity primitive", sp.diff(primitive,r)-g0)
exact("edge supply normalization", s/re**2-1/(1+s))
exact("edge force balance", -((1+s)/re**2)+s/(re**2-s))
exact("exterior acceleration numerator", aout-numerator/(r**2*(r**2-s)))
exact("uniform positivity lower bound", aout-(((b-1)*s-1)/r**2+b*s*s/(r**2*(r**2-s))))
tail_antiderivative = (1+s)/r-sp.sqrt(s)*b*sp.atanh(sp.sqrt(s)/r)
exact("exterior work derivative", sp.diff(tail_antiderivative,r)-aout)
exact("matching of interior/exterior acceleration", aout.subs(r,re)-(b-1)*(1+s)/re**2)
mc, ms, f, mass = sp.symbols("mchi mS f M",positive=True)
exact("same-charge coproduct counts original Gauss mass", (mc/ms)*(f*mass*ms/mc)-f*mass)
exact("rest-mass to Gauss-mass difference", f*mass-f*mass*ms/mc-f*mass*(1-ms/mc))
ratio = sp.Rational(93906542194,100000000)
assert ratio > 939 and ratio < 940
checks.append({"name":"assigned mass ratio", "value":str(ratio)})

mp.mp.dps=60
beta=mp.mpf(str(ratio.evalf(65)))
cases=[]
for supply in [mp.mpf(1),mp.mpf(5),mp.mpf(20)]:
    edge=mp.sqrt(supply+supply*supply)
    assert (beta-1)*supply-1>0
    for fraction in [mp.mpf('0.1'),mp.mpf('0.3'),mp.mpf('0.8')]:
        start=fraction*edge
        def gravity(x):
            return (1+mp.sqrt(1+4*x*x))/(2*x*x)
        def primitive_mp(x):
            return mp.asinh(2*x)-(1+mp.sqrt(1+4*x*x))/(2*x)
        win=(beta-1)*(primitive_mp(edge)-primitive_mp(start))
        wout=beta*mp.sqrt(supply)*mp.atanh(mp.sqrt(supply)/edge)-(1+supply)/edge
        total=win+wout
        # Independent reciprocal-radius quadrature includes the infinite tail.
        quad_in=mp.quad(lambda x:(beta-1)*gravity(x),[start,edge])
        quad_out=mp.quad(lambda y:-(1+supply)+beta*supply/(1-supply*y*y),[0,1/edge])
        residual=abs(total-quad_in-quad_out)
        assert residual < mp.mpf('1e-45')*max(mp.mpf(1),abs(total))
        assert total>0 and wout>0
        # The original chi has zero interior acceleration and positive exterior binding.
        chi_work=mp.sqrt(supply)*mp.atanh(mp.sqrt(supply)/edge)-(1+supply)/edge
        assert chi_work<0
        # One illustrative physical scaling, not a measured candidate parameter.
        v_over_c=mp.mpf('200000')/mp.mpf('299792458')
        v_final_over_c=mp.sqrt(2*total)*v_over_c
        assert v_final_over_c<mp.mpf('0.1')
        for radius in [edge,2*edge,10*edge,1000*edge]:
            acceleration=-(1+supply)/(radius*radius)+beta*supply/(radius*radius-supply)
            assert acceleration>0
        cases.append({"supply_over_baryon":str(supply),"start_over_edge":str(fraction),
          "edge_over_mond_radius":mp.nstr(edge,20),"work_over_Vf2":mp.nstr(total,25),
          "interior_work_over_Vf2":mp.nstr(win,25),"exterior_work_over_Vf2":mp.nstr(wout,25),
          "quadrature_absolute_residual":mp.nstr(residual,12),
          "original_chi_tail_work_over_Vf2":mp.nstr(chi_work,20),
          "example_Vf_m_s":"200000", "example_final_speed_over_c":mp.nstr(v_final_over_c,15)})

result={"claim_id":"MC-REMNANT-001", "symbolic_checks":checks,"finite_cases":cases,
 "max_quadrature_absolute_residual":str(max(mp.mpf(c['quadrature_absolute_residual']) for c in cases)),
 "scope":"Dilute test remnant, prescribed pure-chi finite halo; no conversion rate or collective energy accounting."}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(f"PASS: {len(checks)} exact/parameter controls and {len(cases)} finite quadrature cases; 60-digit arithmetic.")
print("Scope: frozen-background test-particle work; full medium/conversion/metric remains open.")

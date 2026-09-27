#!/usr/bin/env python3
"""Radial exact-law jets and the symmetric globally C2 penalty completion."""
import argparse,json
from pathlib import Path
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
checks={}
def exact(name,expr):
    value=S.factor(S.simplify(expr));checks[name]={'residual':str(value),'passed':value==0}
    assert value==0,(name,value)
x,C,t,wl,wt,r,d=S.symbols('x C t w_L w_T r delta',real=True)
x=S.symbols('x',positive=True)
F=lambda y:2*(1-C)*y*y+4*C*(1-(1+y)*S.exp(-y))
G=x*x+2*(1+x)*S.exp(-x)-2
ET=2*(1-C*(1-S.exp(-x)))
EL=2*(1-C*(1+(x-1)*S.exp(-x)))
exact('exact_static_primitive',-2*x*x+F(x)+2*C*G)
exact('radial_hessian_tangent',S.diff(F(x),x)/x-2*ET)
exact('radial_hessian_longitudinal',S.diff(F(x),x,2)-2*EL)
exact('hessian_integrability',EL-ET-x*S.diff(ET,x))
rho_plus=S.sqrt((x+t*wl)**2+t*t*wt*wt)
rho_minus=S.sqrt((x-t*wl)**2+t*t*wt*wt)
sym=F(rho_plus)+F(rho_minus)-2*F(x)
exact('symmetric_penalty_static_zero',sym.subs(t,0))
exact('symmetric_penalty_first_variation_zero',S.diff(sym,t).subs(t,0))
second=S.simplify(S.diff(sym,t,2).subs(t,0)/2)
exact('symmetric_penalty_second_variation',second-2*(ET*wt*wt+EL*wl*wl))
exact('matched_directional_penalty',-r*r*second/(2*d*d)+r*r*(ET*wt*wt+EL*wl*wl)/(d*d))
series=S.series(F(x),x,0,5).removeO()
exact('radial_origin_expansion',series-(2*x*x-S.Rational(4,3)*C*x**3+C*x**4/2))
exact('continuous_zero_hessian_tangent',S.limit(2*ET,x,0,dir='+')-4)
exact('continuous_zero_hessian_longitudinal',S.limit(2*EL,x,0,dir='+')-4)
# Directional counterexample to differentiability of raw Hessian penalty:
# perpendicular Hessian along a=t e1 has derivative -4C at t=0+ and +4C at t=0-.
right_slope=S.limit(S.diff(2*ET,x),x,0,dir='+')
exact('raw_hessian_right_slope',right_slope+4*C)
assert right_slope.subs(C,S.Rational(1,2))==-2
checks['raw_hessian_cusp_negative_control']={'C':'1/2','right_slope':'-2','left_slope':'2','passed':True}
out={'result':'Symmetric integrated penalty realizes exact directional Hessian coefficients and avoids raw-Hessian off-shell first-variation cusp.',
 'checks':checks,
 'primitive':'F_C(a)=2(1-C)|a|²+4C a0²[1-(1+x)e^-x]',
 'preferred_penalty':'-r²/(2delta²)[F_C(a+w)+F_C(a-w)-2F_C(a)], w=DU+a',
 'scope':'Exact radial derivatives and Taylor coefficients; global C2 and convexity argument in REPORT.md uses continuity of the radial Hessian and a direct positive integral.',
 'non_claims':['No full Hamiltonian constraint closure','No full gravitational finite-background propagation calculation','No claim of C3 regularity at zero acceleration']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

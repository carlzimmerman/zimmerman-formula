#!/usr/bin/env python3
"""Degenerate kinetic repair and conserved-source tidal response, same action."""
import argparse
import json
from pathlib import Path
import sympy as s

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
checks={}
def exact(name,expr):
    rr=s.factor(s.simplify(expr));checks[name]={'residual':str(rr),'passed':rr==0};assert rr==0,(name,rr)

p,f,u,be,dp,du,k,E,z,B,R,w=s.symbols('p f u be dp du k E z B R omega',real=True)
kap=2*(2+3*B)/B
L=(-6*dp**2+4*k**2*be*dp+2*k**2*p**2-4*k**2*f*p+E*k**2*f**2-z*k**2*(u+f)**2
   -B*(3*dp-k**2*be)**2-2*(2+3*B)*(3*dp-k**2*be)*du-3*(2+3*B)*du**2)
v,dv=s.symbols('v vdot',real=True)
Lv=s.expand(L.subs({p:v-u,dp:dv-du}))
aux=s.solve([s.diff(Lv,zz) for zz in [f,be,u]], [f,be,u],dict=True)[0]
reduced=s.factor(Lv.subs(aux))
exact('full_joint_auxiliary_reduction',reduced-(kap*dv**2-2*z/(2-z)*k**2*v**2))
exact('remaining_du_cancels',s.diff(reduced,du))
auxmat=s.hessian(Lv,[f,be,u])
exact('joint_auxiliary_determinant',auxmat.det()-8*B*k**8*(E-2)*(z-2))
exact('causal_wave_witness',(2*z/((2-z)*kap)).subs({z:s.Rational(1,4),B:s.Rational(2,5)})-s.Rational(1,56))
D=-s.I*w
stress=w**2/k**2*R
eq=[s.diff(L,p)-D*s.diff(L,dp)-stress,s.diff(L,f)-R,s.diff(L,be)+D*R,s.diff(L,u)-D*s.diff(L,du)]
eq=[s.expand(q.subs({dp:D*p,du:D*u})) for q in eq]
M=s.Matrix([[s.diff(q,zz) for zz in [p,f,be,u]]for q in eq])
src=s.Matrix([-q.subs({p:0,f:0,be:0,u:0})for q in eq])
sol=M.inv()*src
delta=[s.factor(q-q.subs(E,0))for q in sol]
expected=E*(k**2+w**2)*R/(4*k**4*(E-2))
for name,val,target in [('psi',delta[0],expected),('phi',delta[1],expected),('shift',delta[2],0),('U',delta[3],-expected)]:
    exact('source_delta_'+name,val-target)
exact('source_delta_propagating_v',delta[0]+delta[3])
tidal=-k**2*(delta[1]+D*delta[2])-w**2*delta[0]
exact('gauge_invariant_tidal_difference',tidal+E*(k**2+w**2)**2*R/(4*k**4*(E-2)))
ff=s.symbols('F',real=True)
source_tidal=s.factor(tidal.subs(R,-k**2*ff))
exact('compact_generator_tidal',source_tidal-E*(k**2+w**2)**2*ff/(4*k**2*(E-2)))
polynomial=s.Poly(s.factor(tidal/R),w)
assert polynomial.degree()==4
checks['no_temporal_wave_denominator']={'degree_in_omega':4,'passed':True}
result={'result':'degenerate kinetic healthy wave plus nonlocal instantaneous modified tidal sector',
        'checks':checks,'Lphys':str(reduced),'auxiliary_determinant':str(s.factor(auxmat.det())),
        'conserved_source':{'R':'-k^2 F','j':'-i omega R','stress':'omega^2/k^2 R',
                            'generator':'T00=partial_x^2 F,T0x=-partial_t partial_x F,Txx=partial_t^2 F'},
        'modified_tidal':str(s.factor(tidal)),
        'modified_tidal_from_compact_generator':str(source_tidal),
        'non_claims':['Only constant-coefficient nonzero-mode response on the displayed quadratic action',
                      'Source can be a signed perturbation around a background; no positive isolated-mass source theorem',
                      'No full nonlinear constraint-data existence or global covariance result',
                      'Healthy scalar wave does not imply causal MOND force']}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

#!/usr/bin/env python3
"""Exact homogeneous fixed-charge transition identities; no dynamical relaxation claim."""
import argparse,json
from pathlib import Path
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
u,q,m2,mu2,lr,ls,g2=S.symbols('u q m2 mu2 lr ls g2',positive=True)
a=m2+g2*mu2/ls;b=lr-g2*g2/ls;ut=mu2/g2
E0=q*q/(2*u)+m2*u/2+lr*u*u/4
E1=q*q/(2*u)+a*u/2+b*u*u/4-mu2*mu2/(4*ls)
checks={}
def eq(n,e):
 e=S.factor(e);assert e==0,(n,e);checks[n]='exact zero'
eq('piecewise energy joins',(E0-E1).subs(u,ut))
eq('first derivative joins',S.diff(E0-E1,u).subs(u,ut))
eq('unbroken energy curvature',S.diff(E0,u,2)-(q*q/u**3+lr/2))
eq('broken energy curvature',S.diff(E1,u,2)-(q*q/u**3+b/2))
eq('unbroken charge stationarity',2*u*u*S.diff(E0,u)-(u*u*(m2+lr*u)-q*q))
eq('broken charge stationarity',2*u*u*S.diff(E1,u)-(u*u*(a+b*u)-q*q))
eq('threshold charge agrees',(u*u*(m2+lr*u)-u*u*(a+b*u)).subs(u,ut))
omega2=a+b*u;energy=E1.subs(q*q,u*u*omega2);pressure=u*omega2-energy
peq=b*u*u/4+mu2*mu2/(4*ls)
eq('broken pressure',pressure-peq)
eq('broken pressure joins',(peq-lr*u*u/4).subs(u,ut))
eq('adiabatic sound',S.diff(peq,u)/S.diff(energy,u)-b*u/(2*a+3*b*u))
v=S.symbols('v',positive=True)
eq('charge polynomial monotonicity factor',(v*v*(a+b*v)-u*u*(a+b*u))/(v-u)-(a*(v+u)+b*(v*v+v*u+u*u)))
out={'result':'fixed-charge homogeneous ground-state identities accepted','check_count':len(checks),'checks':checks,'analytic_hypotheses':['q>0,m²>=0,mu²>0,g²>0,lambda_s>0,lambda_R lambda_s>g⁴','piecewise energy considered on u>0'],'non_claims':['No dynamical equilibration','No halo clearing','No exact single-fluid approximation at the gapless threshold']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

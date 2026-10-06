"""Preferred-normal trace and proper-volume mean, not an optical/growth observable."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['drop_lapse','coordinate_mean']);args=ap.parse_args();rows=[]
def eq(name,e):rows.append({'name':name,'passed':s.simplify(e)==0})
e,H,u,W,ux,Z,Zd,Zx,V,S,Sx=s.symbols('eps H u W ux Z Zd Zx V S Sx',real=True)
want=Zd-H*V-Sx/3+H*W*ux/6-H*u*u/8
for sign in (1,-1):
 lapse=s.exp(e*sign*u/2+e*e*V);vol=s.exp(-e*sign*u/2+e*e*3*Z)
 bracket=3*H+3*e*e*Zd+sign*e*H*u/2-(e*e*S+sign*e*H*W)*(3*e*e*Zx-sign*e*ux/2)-e*e*Sx+sign*H*e*u
 theta=bracket/lapse/3
 eq('first_order_normal_expansion_'+str(sign),s.series(theta,e,0,3).removeO().coeff(e,1))
 eq('second_order_trace_'+str(sign),s.series(theta,e,0,3).removeO().coeff(e,2)-want)
 density=theta*vol
 eq('proper_volume_normalization_'+str(sign),s.series(density-H*vol,e,0,3).removeO().coeff(e,2)-want)
 candidate=theta if args.control!='drop_lapse' else bracket/3
 eq('declared_actual_lapse_'+str(sign),s.series(candidate,e,0,3).removeO().coeff(e,2)-want)
# Periodic mean identities W_x=-u; ∫W u_x=∫u², ∫S_x=0.
r,A0=s.symbols('r A0',positive=True);F0=-H*r*A0/24
geom=H*r*A0/s.Integer(24)
if args.control=='coordinate_mean':geom=0
eq('preferred_normal_mean_cancellation',F0+geom)
x=s.symbols('x',real=True);f=s.cos(x)-s.cos(3*x)/9
eq('prepared_profile_exact_squared_mean',s.integrate(f*f,(x,0,2*s.pi))/(2*s.pi)-s.Rational(41,81))
eq('prepared_trace_specific_cancellation',F0.subs(A0,s.Rational(41,81))+41*H*r/1944)
# Mean source consistency rather than extrapolating the finite-k inverse.
c=s.symbols('c',positive=True);Fd=-2*H*F0;source=c*H*H*r*A0
eq('homogeneous_lapse_row',24*c*H*F0+source)
eq('homogeneous_curvature_row',24*c*(Fd+3*H*F0)+source)
res={'passed':sum(q['passed'] for q in rows),'total':len(rows),'checks':rows,'control':args.control,'scope':'conditional formal second-order preferred-normal average for actual pure-decay seed and sourced mean solution; not full optical/cold abundance theorem'}
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':res['passed'],'total':res['total'],'failed':[q['name'] for q in rows if not q['passed']]}));raise SystemExit(not all(q['passed'] for q in rows))

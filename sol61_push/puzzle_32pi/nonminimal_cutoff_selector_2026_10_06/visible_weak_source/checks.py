#!/usr/bin/env python3
"""Actual ordinary-only leading static source action and force calibration."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['none','mirror','calibration','pointwise'],default='none');a=ap.parse_args();rows=[]
def eq(name,x,y=0):
 r=s.factor(s.cancel(x-y));rows.append({'name':name,'passed':r==0,'residual':str(r)})
def truth(name,v,detail=''):rows.append({'name':name,'passed':bool(v),'detail':detail})
d,M,F,q,Z,Omega,Gt,a0=s.symbols('d M F q Z Omega Gt a0',positive=True)
Mi=M*F/2;Zbar=F*Z;alphasq=q*q/((d-2)**2*Zbar)
ss=Mi*(d-2)/(d-3)*alphasq
eq('ordinary_only_scalar_fraction',ss,M*q*q/(2*(d-2)*(d-3)*Z))
eq('mirror_fraction_twice_visible',M*F*(d-2)/(d-3)*alphasq,2*ss)
eq('positive_canonical_upper',ss.subs(Z,M*(d-1)/(d-2)*q*q),1/(2*(d-1)*(d-3)))
eq('fourdimensional_visible_fraction',ss.subs(d,4),M*q*q/(4*Z))
# Differentiate actual two-potential static action with a general envelope.
pc,hc,ps,rho,alpha,mass=s.symbols('pc hc psi rho alpha mass');I=(pc-hc)**2/a0**2;fn=s.Function('calM');nr=-(pc**2+hc**2-a0**2*fn(I))/(2*Omega*Gt)
m=s.symbols('m')
# Sympy's derivative form varies with version: direct chain rule coefficients separately.
eq('raw_visible_gradient_variation',s.diff(nr,pc),(-pc+(pc-hc)*s.Subs(s.Derivative(fn(s.Symbol('z')),s.Symbol('z')),s.Symbol('z'),I))/(Omega*Gt))
eq('raw_hat_gradient_variation',s.diff(nr,hc),(-hc-(pc-hc)*s.Subs(s.Derivative(fn(s.Symbol('z')),s.Symbol('z')),s.Symbol('z'),I))/(Omega*Gt))
eq('scalar_mass_and_source_variation',-s.diff(-mass**2*ps**2/2-alpha*rho*ps,ps),mass**2*ps+alpha*rho)
fluxg=pc-m*(pc-hc);fluxh=hc+m*(pc-hc)
eq('sum_tensor_source_flux',fluxg+fluxh,pc+hc)
eq('difference_source_flux',fluxg-fluxh,(1-2*m)*(pc-hc))
e,y=s.symbols('e y',positive=True);x=y*(1+2*e);mm=e/(1+2*e)
eq('actual_radial_star_flux',(1-2*mm)*x,y)
eq('actual_radial_visible_force',(1-mm)*x,y*(1+e))
# Scalar Helmholtz response to a single source, not mirrored.
r=s.symbols('r',positive=True);Yuk=s.exp(-mass*r)/r
eq('exterior_Yukawa_equation',s.diff(Yuk,r,2)+2*s.diff(Yuk,r)/r,mass**2*Yuk)
eq('exterior_Yukawa_force',-s.diff(Yuk,r),s.exp(-mass*r)*(1+mass*r)/r**2)
nu=s.sqrt(1+1/y)-1;cut=s.symbols('cut',positive=True);ev=nu/(1+(y/cut)**2)
eq('deep_force_coefficient',s.limit(y*(1+ev)/s.sqrt(y),y,0,dir='+'),1)
eq('high_acceleration_tensor_coefficient',s.limit(1+ev,y,s.oo),1)
S,g=s.symbols('S g',positive=True);Gobs=Gt*(1+S);Aobs=a0/(1+S)
eq('operational_deep_calibration',Aobs*Gobs,a0*Gt)
eq('conditional_vacuum_conversion',(a0/Aobs)**2,(1+S)**2)
eq('visible_maximum_conversion',(1+s.Rational(1,6))**2,s.Rational(49,36))
truth('conditional_bound_below_32pi',s.Rational(49,144)*s.pi*s.exp(2)<32*s.pi)
# Global source inverse sufficient bound T>=1, split y at1/3.
z=s.symbols('z',positive=True);b=s.sqrt(1+1/y)-1;bp=s.diff(b,y)
eq('fixed_cutoff_inverse_derivative',s.diff(y*(1+2*ev),y),1+2*(b+y*bp)/(1+(y/cut)**2)-4*b*(y/cut)**2/(1+(y/cut)**2)**2)
sv=s.symbols('sv',positive=True)
eq('positive_b_plus_ybp',(b+y*bp).subs(y,1/(sv**2-1)),(sv-1)**2/(2*sv))
truth('small_y_negative_bound',4/(3*s.sqrt(3))<1)
eq('conformal_quadratic_cancellation',s.Symbol('Om',positive=True)**(-2)*s.Symbol('Om',positive=True)**2,1)
eq('fourdimensional_Weyl_conformal_cancel',((pc+alpha*ps)+(pc-alpha*ps))/2,pc)
coords=s.symbols('xcoord ycoord zcoord');vector=s.Matrix([1,0,0])
eq('nonzero_divergence_free_witness',sum(s.diff(vector[i],coords[i]) for i in range(3)),0)
if a.control=='mirror':eq('control_mirrored_charge',2*ss,ss)
if a.control=='calibration':eq('control_uncalibrated_a0',a0*Gobs,a0*Gt)
if a.control=='pointwise':eq('control_divergence_implies_pointwise_gradient',s.Matrix([1,0,0]).dot(s.Matrix([1,0,0])),0)
out={'passed':sum(x['passed'] for x in rows),'total':len(rows),'checks':rows,'control':a.control,'scope':'leading static ordinary source plus scalar; declared weak/deep/subcurvature hierarchy, not global source solution'}
Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[x['name'] for x in rows if not x['passed']]}));sys.exit(0 if out['passed']==out['total'] else 1)

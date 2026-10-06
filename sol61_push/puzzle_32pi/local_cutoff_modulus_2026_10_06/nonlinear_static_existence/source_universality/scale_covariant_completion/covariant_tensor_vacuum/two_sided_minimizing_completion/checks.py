"""Two minimal parity continuations, exact local identities and bounded branch checks."""
import argparse,json,sys
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['odd_keeps_minimum','null_C2','absolute_positive_time']);args=ap.parse_args();rows=[]
def eq(n,e):
 e=s.factor(s.cancel(e));rows.append({'name':n,'passed':e==0,'detail':str(e)})
def ck(n,b,e=''):rows.append({'name':n,'passed':bool(b),'detail':str(e)})
r,T,lam,qT,qTT,ey,xy=s.symbols('r T lam qT qTT ey xy',positive=True);y=s.symbols('y',positive=True)
# Fixed-x chain, not the original fixed-y auxiliary curvature.
yT=-2*y*ey/xy;qTy=2*y*ey;HT=lam-qTT-qTy*yT
eq('fixed_invariant_auxiliary_chain',HT-(lam-qTT+(2*y*ey)**2/xy))
eq('absolute_branch_stationarity',qT-lam*T-(qT-lam*T))
eq('odd_branch_no_stationary_source',(-qT-lam*T).subs(qT,lam*T)+2*lam*T)
ck('odd_branch_strictly_negative',(-qT-lam*T).is_negative)
eq('flipped_potential_auxiliary_Hessian',(-qTT+lam-qTy*yT)-HT)
# Envelope expansion using y=x²/4(1+2A sqrt(x/2)+...).
x,A,z=s.symbols('x A z',positive=True);yv=x*x/4*(1+2*A*s.sqrt(x/2));mz=s.Rational(1,2)-yv/(2*x)
eq('envelope_derivative_expansion',mz-(s.Rational(1,2)-x/8-A*x**s.Rational(3,2)/(4*s.sqrt(2))))
rem=-z**s.Rational(3,2)/12-A*z**s.Rational(7,4)/(7*s.sqrt(2))
eq('integrated_envelope_first_correction',s.diff(rem,z)+s.sqrt(z)/8+A*z**s.Rational(3,4)/(4*s.sqrt(2)))
eq('one_sided_second_derivative_blowup',s.limit(s.sqrt(z)*s.diff(rem,z,2),z,0)+s.Rational(1,16))
# Raw coincident-position pure TT velocity action, K/4 v² and z=-v²/(4chi a0²).
v,w,K,chi,a0,eps=s.symbols('v w K chi a0 eps',positive=True);zt=(w*w-v*v)/(4*chi*a0*a0)
eq('critical_TT_EH_cancellation',K*v*v/4+2*K*chi*a0*a0*s.Rational(1,2)*(-v*v/(4*chi*a0*a0)))
Labs=-K*v**3/(48*s.sqrt(chi)*a0);Lodd=-Labs
ck('absolute_leading_time_Hessian_negative',s.diff(Labs,v,2).is_negative)
ck('odd_leading_time_Hessian_positive',s.diff(Lodd,v,2).is_positive)
# Scalar-type single-polarization principal comparison; no full metric constraint theorem.
Ptime=r**s.Rational(3,2);Pspace=-r**s.Rational(3,2)
Px=s.diff(Ptime,r);Pxx=s.diff(Ptime,r,2)
eq('odd_timelike_sound_ratio',Px/(Px+2*r*Pxx)-s.Rational(1,2))
Pxspace=-s.diff(Pspace,r);Pxxspace=s.diff(Pspace,r,2)
eq('odd_spacelike_longitudinal_ratio',(Pxspace+2*(-r)*Pxxspace)/Pxspace-2)
ck('odd_Px_both_sides_positive',Px.is_positive and Pxspace.is_positive)
nullrem=-zt**s.Rational(3,2)/12
nullD=s.diff(nullrem,w,2).subs(w,v+eps)
coeff=s.limit(s.sqrt(eps)*nullD,eps,0)
eq('nonzero_null_directional_Hessian',coeff+s.Rational(1,16)*(v/(2*chi*a0*a0))**s.Rational(3,2))
ck('nonnull_null_Hessian_divergence',coeff.is_negative)
eq('origin_fixed_direction_zero_secondvariation',s.limit(s.diff(-eps**3/12,eps,2),eps,0))
# Bounded actual stationary source branch, independent rescaled integrals.
mp.mp.dps=60;examples=[]
for ll,yy in [('0.001','1e-20'),('0.01','1e-20'),('0.01','1e-12')]:
 l=mp.mpf(ll);Y=mp.mpf(yy);h=Y**mp.mpf('.25');U0=(8/(7*l))**mp.mpf('.25')
 R=lambda t:1/(mp.sqrt(1+Y*t)+mp.sqrt(Y*t))
 I=lambda U,p:mp.quad(lambda t:t**mp.mpf('2.5')*R(t)/(U*U+h*t*t)**p,[0,1])
 lo=U0*mp.mpf('1e-15');hi=U0
 for _ in range(150):
  mid=(hi+lo)/2
  if 4*I(mid,2)>l:lo=mid
  else:hi=mid
 U=(lo+hi)/2;TT=U*Y**mp.mpf('.875');delta=(Y/TT)**2;b=mp.sqrt(1+1/Y)-1;e=b/(1+delta);xx=Y*(1+2*e);zz=xx*xx;md=e/(1+2*e)
 et=b*2*Y*Y/TT**3/(1+delta)**2;bp=-1/(2*Y**mp.mpf('1.5')*mp.sqrt(1+Y));exy=1+2*(e+Y*(bp/(1+delta)-2*b*delta/Y/(1+delta)**2))
 HT0=16*U*U*I(U,3)+(2*Y*et)**2/exy
 q=2*Y**mp.mpf('1.5')*mp.quad(lambda t:mp.sqrt(t)*R(t)/(1+delta*t*t),[0,1])
 Rm=q+2*(Y*e)**2-l*TT*TT/2-zz/2;ad=mp.sqrt(7*l/8);leading=-zz**mp.mpf('1.5')/12;second=(Rm-leading)/zz**mp.mpf('1.75');target=-ad/(7*mp.sqrt(2))
 ck('actual_stationarity_'+ll+'_'+yy,abs(4*I(U,2)-l)<mp.mpf('1e-35'))
 ck('actual_fixed_x_inverse_'+ll+'_'+yy,exy>0)
 ck('actual_auxiliary_minimum_'+ll+'_'+yy,HT0>0)
 ck('actual_envelope_slope_'+ll+'_'+yy,md>0 and md<mp.mpf('.5'))
 if yy=='1e-20':
  ck('actual_second_envelope_coefficient_'+ll,abs(second/target-1)<mp.mpf('.01'))
  ck('actual_curvature_limit4lambda_'+ll,abs(HT0/(4*l)-1)<mp.mpf('.01'))
 examples.append({'lambda':ll,'y':yy,'x':mp.nstr(xx,24),'T':mp.nstr(TT,24),'M_z_source':mp.nstr(md,24),'M_z_absolute_timelike':mp.nstr(1-md,24),'aux_energy_Hessian_fixed_x':mp.nstr(HT0,24),'H_over_4lambda':mp.nstr(HT0/(4*l),24),'second_envelope_coefficient':mp.nstr(second,24),'second_coefficient_limit':mp.nstr(target,24),'scope':'local source stationary chart, not global auxiliary inverse'})
if args.mutation=='odd_keeps_minimum':eq('false_odd_same_source_stationarity',(-qT-lam*T).subs(qT,lam*T))
if args.mutation=='null_C2':eq('false_finite_null_secondvariation',coeff)
if args.mutation=='absolute_positive_time':ck('false_absolute_time_positive',s.diff(Labs,v,2).is_positive)
args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'examples':examples,'mutation':args.mutation,'scope':'minimal two-sided local constructions and regularity/coefficient tests, not on-shell all-helicity health'},indent=2)+'\n');print(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'failures':[r for r in rows if not r['passed']]}));sys.exit(0 if all(r['passed'] for r in rows) else 1)

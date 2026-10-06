"""Dust+radiation exact identities and bounded roots, not a CMB or mode-transfer fit."""
import argparse,json
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--dust-charge',action='store_true');ap.add_argument('--dust-early-sign',action='store_true');ap.add_argument('--cap-enhancement',action='store_true');args=ap.parse_args()
checks=[]
def ck(n,b):checks.append({'name':n,'passed':bool(b)})
def eq(x):return s.simplify(x)==0
eta,af,rf,aa,D,R,j,h,x,u=s.symbols('eta af rf aa D R j h x u',positive=True)
df=1-4*rf/3;dval=df*af**3;rval=rf*af**4;jcrit=eta*af**3*s.exp(eta/2-rf/3)
f=(h*h-1)/(2*eta)-(h-1)-s.log(h-1);B=D/aa**3+R/aa**4+3*s.log(aa)-s.log(j)
ck('minimum_derivative',eq((aa*s.diff(B,aa)).subs({aa:af,D:dval,R:rval},simultaneous=True)))
ck('source_minimum_curvature',eq((aa*s.diff(aa*s.diff(B,aa),aa)).subs({aa:af,D:dval,R:rval},simultaneous=True)-(9+4*rf)))
used=eta*af**3*s.exp(eta/2) if args.dust_charge else jcrit
ck('charge_matches_minima',eq(B.subs({aa:af,D:dval,R:rval,j:used},simultaneous=True)-f.subs(h,1+eta)))
source=df*(x**-3-1)+rf*(x**-4-1)+3*s.log(x)
L=lambda y:y-s.log(y)-1
ck('normalized_fold_equation',eq((B-f.subs(h,1+eta)).subs({aa:af*x,D:dval,R:rval,j:jcrit},simultaneous=True)-source))
ck('field_signed_square_root',eq(f.subs(h,1+eta*u)-f.subs(h,1+eta)-L(u)-eta*(u-1)**2/2))
ck('fold_slope_squared',eq(s.diff(f,h,2).subs(h,1+eta)*eta**2*(9+4*rf)/(1+eta)-(9+4*rf)))
E=s.exp(eta/2-rf/3)/df
ck('late_enhancement_normalization',eq(jcrit/(eta*dval)-E))
ck('enhancement_monotone_rf',eq(s.diff(s.log(E),rf)-(-s.Rational(1,3)+s.Rational(4,3)/df)))
ck('dust_limit',eq(E.subs(rf,0)-s.exp(eta/2)))
alpha=s.sqrt(2*eta*R);beta=eta*D/alpha;gamma=eta-beta*beta/(2*alpha)
ck('early_radiation_leading',eq(alpha**2/(2*eta)-R))
ck('early_dust_subleading',eq(alpha*beta/eta-D))
ck('early_constant_term',eq((beta*beta+2*alpha*gamma)/(2*eta)-alpha))
M,Hs,k,kappa=s.symbols('M Hs k kappa',positive=True)
Ac=M*(3*eta*(1+eta-h)+kappa*(k/(aa*Hs))**2)/(h-eta)**2
leading=s.limit(Ac.subs(h,alpha/aa**2+beta/aa+gamma)/aa**2,aa,0,dir='+')
ck('comoving_early_kinetic_leading',eq(leading-M*(kappa*k*k/Hs**2-3*eta*alpha)/alpha**2))
critical=s.simplify(Ac.subs(k*k,3*eta*alpha*Hs**2/kappa).subs(h,alpha/aa**2+beta/aa+gamma))
ck('critical_early_dust_correction',eq(s.limit(critical/aa**3,aa,0,dir='+')+3*M*eta*beta/alpha**2))
# Regular radiation field P(Y)=C Y^2 is on-shell rho=3P, cs²=1/3.
Y,C=s.symbols('Y C',positive=True);P=C*Y**2;rho=2*Y*s.diff(P,Y)-P
ck('radiation_equation_of_state',eq(rho-3*P))
ck('radiation_sound_speed',eq(s.diff(P,Y)/(s.diff(P,Y)+2*Y*s.diff(P,Y,2))-s.Rational(1,3)))
A,d,Cd,Cr=s.symbols('A d Cd Cr',positive=True);zd,vd,vr=s.symbols('zd vd vr',real=True)
vel= A*zd**2+Cd*(vd-d*zd)**2+Cr*(vr-d*zd)**2
KM=s.hessian(vel,[zd,vd,vr])/2
ck('two_fluid_velocity_determinant',eq(KM.det()-A*Cd*Cr))
# Bounded global roots normalized to af=1; analytic proof handles allpositive x.
mp.mp.dps=60;rows=[]
def lm(t):return t-mp.log(t)-1
def root(ee,rr,xx):
 if xx==1:return mp.mpf(1)+ee
 dd=1-4*rr/3;target=dd*(xx**-3-1)+rr*(xx**-4-1)+3*mp.log(xx)
 lo=mp.mpf('1e-120') if xx>1 else mp.mpf(1);hi=mp.mpf(1) if xx>1 else max(mp.mpf(2),xx**-2*20)
 for _ in range(600):
  mid=(lo+hi)/2;val=lm(mid)+ee*(mid-1)**2/2
  if (val>target)==(xx>1):lo=mid
  else:hi=mid
 return 1+ee*(lo+hi)/2
for rt in ['0','.25','.7']:
 rr=mp.mpf(rt);ee=mp.mpf('.5');xxs=[mp.mpf(t) for t in ['1e-5','.1','.999','1','1.001','10','1e5']];hh=[root(ee,rr,xx) for xx in xxs]
 dd=1-4*rr/3;jj=ee*mp.exp(ee/2-rr/3)
 res=max(abs(lm((hi-1)/ee)+ee*((hi-1)/ee-1)**2/2-(dd*(xx**-3-1)+rr*(xx**-4-1)+3*mp.log(xx)))/(1+abs(dd*(xx**-3-1)+rr*(xx**-4-1)+3*mp.log(xx))) for hi,xx in zip(hh,xxs))
 ck('bounded_roots_rf'+rt,res<mp.mpf('1e-40'))
 ck('monotone_H_rf'+rt,all(hi>hj for hi,hj in zip(hh,hh[1:])))
 ck('late_q_normalization_rf'+rt,abs(xxs[-1]**3*(hh[-1]-1)/jj-1)<mp.mpf('1e-12'))
 if rr>0:ck('early_radiation_rf'+rt,abs(hh[0]**2/(2*ee*rr*xxs[0]**-4)-1)<mp.mpf('.001'))
 enhancement=mp.exp(ee/2-rr/3)/dd
 rows.append({'rf':rt,'df':str(dd),'j_critical_af1':str(jj),'enhancement':str(enhancement),'scaled_residual':str(res),'h_samples':[str(i) for i in hh]})
cap_test=mp.mpf(rows[-1]['enhancement'])<=mp.sqrt(mp.e) if args.cap_enhancement else mp.mpf(rows[-1]['enhancement'])>mp.sqrt(mp.e)
ck('large_radiation_fold_exceeds_dust_bound',cap_test)
# Early coefficients at eta=.5,R=.25 imply alpha=.5 and kcrit²=.75.
early=[]
for kk in [mp.mpf('.1'),mp.mpf('1')]:
 coeff=kk*kk-mp.mpf('.75');early.append({'k_over_Hstar':str(kk),'early_Kc_over_Ma2':str(4*coeff)})
small_coefficient=mp.mpf(early[0]['early_Kc_over_Ma2'])
if args.dust_early_sign:small_coefficient=abs(small_coefficient)
ck('small_comoving_mode_negative_early',small_coefficient<0)
ck('large_comoving_mode_positive_early',mp.mpf(early[1]['early_Kc_over_Ma2'])>0)
out={'checks':checks,'summary':{'passed':sum(t['passed'] for t in checks),'total':len(checks)},'background_rows':rows,'early_kinetic_rows':early,'scope':'Conserved dust+radiation flatFRW background; exact velocity Schur and earlycomoving coefficient only. No radiation/dust mode-transfer, crossing singularity theorem, atomic recombination or CMB fit.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']));raise SystemExit(0 if all(t['passed'] for t in checks) else 1)

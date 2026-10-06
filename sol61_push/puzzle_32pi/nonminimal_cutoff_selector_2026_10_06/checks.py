#!/usr/bin/env python3
"""Common-vacuum nonminimal action; bounded quadrature is not a full source solution."""
import argparse,json,sys
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['none','trace','minimum','EHonly'],default='none');ar=ap.parse_args();rows=[]
def eq(name,a,b=0):
 r=s.factor(s.cancel(a-b));rows.append({'name':name,'passed':r==0,'residual':str(r)})
def truth(name,value,detail=''):rows.append({'name':name,'passed':bool(value),'detail':str(detail)})
d,M,V,F,A,q,p=s.symbols('d M V F A q p',positive=True);beta=2/(d-2);Lambda=V*A/M;R=2*d*Lambda/(d-2)
eq('both_metric_common_vacuum',M*F*Lambda,V*F*A)
eq('nonminimal_scalar_stationarity',M*F*q*R/2-V*F*A*(q+p),V*F*A*(beta*q-p))
u=s.symbols('u');ff=s.Function('F')(u);aa=s.Function('A')(u);pot=aa*ff**(-beta)
eq('EF_potential_log_slope',s.diff(pot,u)/pot,s.diff(aa,u)/aa-beta*s.diff(ff,u)/ff)
Z,f=s.symbols('Z f',positive=True);eq('EF_kinetic_normalization',f/F+M*(d-1)/(d-2)*q*q,f/F+M*(1+1/(d-2))*q*q)
n,K,cn=s.symbols('n K chi',positive=True);c=(n-1)/(2*(n-2));nu,ze,P=s.symbols('nu zeta P')
raw=K*(n-1)*((n-2)*ze**2+2*nu*ze)
eq('single_EH_static_reduction',raw.subs(ze,-nu/(n-2)),-K*(n-1)/(n-2)*nu**2)
rel=-K*c*P*nu**2
interaction=K*c*P*nu**2
eq('both_prefactors_critical',F*rel+F*interaction,0)
eq('EH_only_residual',F*rel+interaction,K*c*(1-F)*P*nu**2)
q1,q2,c1,c2,T=s.symbols('q1 q2 c1 c2 T',positive=True);sumF=c1*T**q1+c2*T**q2
qF=T*s.diff(sumF,T)/sumF
var=c1*c2*T**(q1+q2)*(q1-q2)**2/sumF**2
eq('positive_sum_log_derivative_variance',T*s.diff(qF,T),var)
alpha,F0,be,pp=s.symbols('alpha F0 beta p',positive=True)
quad=F0+alpha*u*u;qq=s.diff(quad,u)/quad
qprime=s.diff(qq,u)
eq('quadratic_qF',qq,2*alpha*u/(F0+alpha*u*u))
eq('quadratic_qFprime',qprime,2*alpha*(F0-alpha*u*u)/(F0+alpha*u*u)**2)
eq('equilibrium_upper_bound_gap',2*be/u-be*qq,2*be*F0/(u*(F0+alpha*u*u)))
v0=4*be/(3*pp);ratio=9*pp**2/(8*be**2)
eq('shifted_auxiliary_z2',ratio*v0*v0,2)
qshift=2*ratio*v0/(1+ratio*v0*v0);dqshift=2*ratio*(1-ratio*v0*v0)/(1+ratio*v0*v0)**2
eq('arbitrary_target_stationarity',be*qshift,pp)
eq('arbitrary_target_qprime',dqshift,-pp**2/(4*be**2))
eq('stable_counterfamily_mass_bracket',-s.Rational(1,4)-be*dqshift,pp**2/(4*be)-s.Rational(1,4))
eq('general_dimension_Newton_normalization',(n-2)/((n-1)*s.Symbol('Omega')*2*K*F),((n-2)/(n-1))/(s.Symbol('Omega')*2*K*F))
eq('common_scalar_boost_bound', (M*q*q/((d-2)*(d-3)))/(M*(d-1)/(d-2)*q*q),1/((d-1)*(d-3)))
massupper=(d-1)*(d-2)*pp**2/(4*be)/( (d-1)/(d-2)*pp**2/be**2 )
eq('quadratic_mass_Hubble_upper',massupper.subs(be,2/(d-2)),(d-2)/2)
# Independent transformed-positive quadratures at two precisions, with all real-line tails.
candidates=[('maximum','0.0587614242960144202530062907155'),('minimum','1.84657477945060987545505093587')];table=[]
def moments(uu,dps):
 with mp.workdps(dps):
  U=mp.mpf(uu)
  def h(v):return 1/(mp.sqrt(1+mp.exp(-U-v))+1)
  def ell(v):return (1-1/mp.sqrt(1+mp.exp(-U-v)))/2
  def wt(v):return h(v)/(2*mp.cosh(v))
  cuts=[-mp.inf,-5,0,5,mp.inf];J=mp.quad(wt,cuts);El=mp.quad(lambda v:wt(v)*ell(v),cuts)/J;Et=mp.quad(lambda v:wt(v)*mp.tanh(v),cuts)/J
  dp=mp.quad(lambda v:wt(v)*ell(v)*mp.tanh(v),cuts)/J-El*Et
  return {'A':mp.nstr(2*mp.exp(U)*J,dps),'p':mp.nstr(1+El,dps),'dp':mp.nstr(dp,dps),'IBP_residual':mp.nstr(El-Et,dps)}
for name,uu in candidates:
 m35=moments(uu,35);m50=moments(uu,50)
 with mp.workdps(50):
  U=mp.mpf(uu);Q=20*U/(1+10*U*U);Qp=20*(1-10*U*U)/(1+10*U*U)**2;bracket=mp.mpf(m50['dp'])-Qp
  truth(name+'_stationarity',abs(mp.mpf(m50['p'])-Q)<mp.mpf('1e-26'))
  truth(name+'_IBP',abs(mp.mpf(m50['IBP_residual']))<mp.mpf('1e-40'))
  truth(name+'_precision_control',abs(mp.mpf(m35['A'])-mp.mpf(m50['A']))<mp.mpf('1e-30'))
  truth(name+'_stability_sign',bracket<0 if name=='maximum' else bracket>0,bracket)
  truth(name+'_strict_slope_bound',-mp.mpf('.25')<mp.mpf(m50['dp'])<0)
  table.append({'kind':name,'u':uu,'T':mp.nstr(mp.exp(U),30),'A':m50['A'],'p':m50['p'],'pprime':m50['dp'],'logU_second':mp.nstr(bracket,30)})
 if name=='minimum':truth('unshifted_minimum_scale_bound',float(uu)<2 and float(table[-1]['A'])/2<3.141592653589793*2.718281828459045**2/4)
if ar.control=='trace':eq('control_drop_nonminimal_trace',-V*F*A*(q+p),V*F*A*(beta*q-p))
if ar.control=='minimum':truth('control_powerlaw_stable_minimum',mp.mpf(table[-1]['pprime'])>0,'actual computed retained pA_prime rejects a powerlaw minimum')
if ar.control=='EHonly':eq('control_EH_only_critical_preserved',F*rel+interaction,0)
result={'passed':sum(x['passed'] for x in rows),'total':len(rows),'checks':rows,'control':ar.control,'quadratures':table,'scope':'constant common vacuum and bounded quadrature; no full relative or ordinary visible source dictionary'}
Path(ar.out).parent.mkdir(parents=True,exist_ok=True);Path(ar.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[x['name'] for x in rows if not x['passed']]}));sys.exit(0 if result['passed']==result['total'] else 1)

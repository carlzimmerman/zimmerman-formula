from pathlib import Path
import hashlib,json,resource,signal,time
import numpy as np
import mpmath as mp
from mpmath import iv
import sympy as sp
resource.setrlimit(resource.RLIMIT_CPU,(120,120));signal.alarm(150)
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'group_derivative_001';paths=[Path(__file__),run/'results.json',run/'group_derivative_evidence.npz',p/'group_interval_001/results.json',p/'group_interval_001/group_interval_evidence.npz',p/'group_preflight_001/results.json',p/'group_preflight_001/group_native_evidence.npz',p/'group_preflight_001/selected_groups.json'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in paths};read=lambda i:json.loads(paths[i].read_text());d=read(1);de=dict(np.load(paths[2]));data=read(3);ev=dict(np.load(paths[4]));pre=read(5);native=dict(np.load(paths[6]));groups=read(7);mp.mp.dps=70;iv.dps=70;parse=lambda s:iv.mpf([v.strip() for v in s.strip('[]').split(',')]);J=lambda v:iv.mpf(float(v));M=lambda v:mp.mpf(float(v));mid=lambda s:sum(map(mp.mpf,s.strip('[]').split(',')))/2;B=lambda x:mp.log1p(x*x)+2*mp.log1p(x)-2*mp.atan(x);H=lambda x,b:4*x**3/((1+x)*(1+x*x)*b);t0=time.monotonic();checks={};refs=[];radial_cross=0
# Verify the truncation cases used by the local derivative enclosure.
for idx,cell in enumerate(data['records']):
 a=parse(cell['a']);R=parse(data['root_brackets'][2*idx]['R'])
 for x in native['XG']:
  rr=J(x)*a
  if rr.a<R.b and rr.b>=R.a:radial_cross+=1
checks['no_uncertain_radial_truncations']=radial_cross==0
for gi in [0,31,62]:
 for di in range(3):
  idx=3*gi+di;cell=data['records'][idx];rr=data['root_brackets'][2*idx];parent,R,Sigma0=[mid(rr[k]) for k in ['M','R','Sigma']];Mb,a=mid(cell['Mb']),mid(cell['a']);L0=mp.mpf('3.5')
  def evaluate(L,with_derivative=False):
   Sigma=Sigma0*(L/L0)**mp.mpf('1.25');target=parent/(mp.pi*Sigma*R**2);lo,hi=mp.mpf(1),mp.mpf(1e7)
   for _ in range(210):
    x=(lo+hi)/2
    if B(x)/x**2>target:lo=x
    else:hi=x
   x=(lo+hi)/2;root=R/x;bx=B(x);hx=H(x,bx);total=mp.mpf(0);num=mp.mpf(0)
   for k in range(3000):
    radius=M(native['XG'][k])*a
    if radius>=R:mh=parent;elasticity=mp.mpf(0)
    else:
     arg=radius/root;bb=B(arg);mh=parent*bb/bx;elasticity=(H(arg,bb)-hx)/(2-hx)
    total+=M(native['kernel'][k])*(Mb*M(native['M_H'][k])+mh)
    if with_derivative:num+=M(native['kernel'][k])*mh*elasticity
   velocity=mp.log10(M(pre['source_constants']['G540'])/a*total)/2-3
   return (velocity,5/(8*L*mp.log(10))*num/total) if with_derivative else velocity
  _,analytic=evaluate(L0,True);step=mp.mpf('1e-6');large=(evaluate(L0+step)-evaluate(L0-step))/(2*step);small=(evaluate(L0+step/2)-evaluate(L0-step/2))/step;rich=(4*small-large)/3;err=abs(rich/analytic-1);assert err<mp.mpf('1e-8');lo,hi=de['velocity_derivative_bounds'][gi,di];assert M(lo)<=analytic<=M(hi);assert analytic>0 and abs((-analytic-rich)/rich)>1;refs.append(dict(group=gi,offset_index=di,analytic=str(analytic),Richardson=str(rich),relative_difference=str(err)))
checks['nine_independent_derivatives']=len(refs)==9;V=ev['velocity_bounds'];P=de['velocity_derivative_bounds'];D=[J(groups[i]['ls'])-iv.mpf(list(V[i,0])) for i in range(63)];DP=[-iv.mpf(list(P[i,0])) for i in range(63)];S=[(iv.mpf(list(V[i,1]))-iv.mpf(list(V[i,2])))/J(.02) for i in range(63)];SP=[(iv.mpf(list(P[i,1]))-iv.mpf(list(P[i,2])))/J(.02) for i in range(63)];mu=sum(D,iv.mpf(0))/63;mup=sum(DP,iv.mpf(0))/63;var=sum(((D[i]-D[j])**2 for i in range(63) for j in range(i+1,63)),iv.mpf(0))/(63*62);sm=sum(S,iv.mpf(0))/63;smp=sum(SP,iv.mpf(0))/63;T=var/63+J(.10)**2*sm**2;Tp=2*sum(((D[i]-mu)*DP[i] for i in range(63)),iv.mpf(0))/(63*62)+2*J(.10)**2*sm*smp;num=mup*T-mu*Tp/2;Zp=num/(T*iv.sqrt(T));values=dict(mu=mu,mu_prime=mup,variance=var,mean_slope=sm,mean_slope_prime=smp,T=T,T_prime=Tp,numerator=num,Z_prime=Zp);checks['complete_statistic_recomposition']=all(parse(d['statistics'][k]).a<=v.a and parse(d['statistics'][k]).b>=v.b for k,v in values.items());x=sp.symbols('x');u=sp.Function('u')(x);t=sp.Function('t')(x);checks['symbolic_Z_identity']=sp.simplify(sp.diff(u/sp.sqrt(t),x)-(sp.diff(u,x)*t-u*sp.diff(t,x)/2)/t**sp.Rational(3,2))==0;checks['same_local_sign']=bool(Zp.b<0)==d['local_negative_sign'];checks['finite_arrays']=bool(np.isfinite(P).all());checks['original_controls']=all(d['checks'].values());checks['input_hashes']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,selected_derivatives=refs,radial_truncation_uncertainties=radial_cross,review_Z_prime=str(Zp),local_negative_sign=bool(Zp.b<0),runtime_seconds=time.monotonic()-t0,input_sha256=hashes,scope='Independent normalized-root/Richardson controls and full local statistic recomposition; not regional monotonicity or original floating certificate');(p/'group_derivative_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'Zprime',str(Zp));assert all(checks.values())

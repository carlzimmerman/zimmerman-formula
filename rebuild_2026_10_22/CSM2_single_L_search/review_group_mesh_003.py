from pathlib import Path
import hashlib,json,resource,signal,time,sys
import numpy as np
import mpmath as mp
from mpmath import iv
import sympy as sp
resource.setrlimit(resource.RLIMIT_CPU,(120,120));signal.alarm(150)
p=Path(__file__).resolve().parent;r=p.parents[1];tile=int(sys.argv[1]);assert tile in (4,5);run=p/'group_mesh_003'/f'tile_{tile:03d}';paths=[Path(__file__),run/'results.json',run/'group_regional_evidence.npz',run/'results.json',run/'group_regional_evidence.npz',p/'group_preflight_001/results.json',p/'group_preflight_001/group_native_evidence.npz',p/'group_preflight_001/selected_groups.json'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in paths};read=lambda i:json.loads(paths[i].read_text());d=read(1);de=dict(np.load(paths[2]));data=read(3);ev=dict(np.load(paths[4]));pre=read(5);native=dict(np.load(paths[6]));groups=read(7);mp.mp.dps=70;iv.dps=70;parse=lambda s:iv.mpf([v.strip() for v in s.strip('[]').split(',')]);J=lambda v:iv.mpf(float(v));M=lambda v:mp.mpf(float(v));mid=lambda s:sum(map(mp.mpf,s.strip('[]').split(',')))/2;B=lambda x:mp.log1p(x*x)+2*mp.log1p(x)-2*mp.atan(x);H=lambda x,b:4*x**3/((1+x)*(1+x*x)*b);t0=time.monotonic();checks={};refs=[];radial_cross=0
BI=lambda x:iv.log(1+x*x)+2*iv.log(1+x)-2*iv.atan2(x,iv.mpf(1))
root_signs=0
for root in d['root_brackets']:
 lo,hi,target=[parse(root[k]) for k in ['x_lower','x_upper','target']]
 assert (BI(lo)/lo**2-target).a>0 and (BI(hi)/hi**2-target).b<0
 root_signs+=1
checks['378_root_signs']=root_signs==378
checks['189_halo_branches']=len(d['records'])==189 and all(parse(c['column_lower']).a>parse(c['floor']).b for c in d['records'])
checks['fixed_parent_R']=all(d['root_brackets'][2*j]['M']==d['root_brackets'][2*j+1]['M'] and d['root_brackets'][2*j]['R']==d['root_brackets'][2*j+1]['R'] for j in range(189))
# Verify the truncation cases used by the local derivative enclosure.
for idx,cell in enumerate(data['records']):
 a=parse(cell['a']);R=parse(data['root_brackets'][2*idx]['R'])
 for x in native['XG']:
  rr=J(x)*a
  if rr.a<R.b and rr.b>=R.a:radial_cross+=1
checks['no_uncertain_radial_truncations']=radial_cross==0
for gi in [0,31,62]:
 for di in range(3):
  idx=3*gi+di;cell=data['records'][idx];rr=data['root_brackets'][2*idx];parent,R,Sigma0=[mid(rr[k]) for k in ['M','R','Sigma']];Mb,a=mid(cell['Mb']),mid(cell['a']);L0=mid(d['domain'][0])
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
  velocity,analytic=evaluate(L0,True);vlo,vhi=ev['endpoint_velocity_bounds'][idx,0];assert M(vlo)<=velocity<=M(vhi);step=mp.mpf('1e-6');large=(evaluate(L0+step)-evaluate(L0-step))/(2*step);small=(evaluate(L0+step/2)-evaluate(L0-step/2))/step;rich=(4*small-large)/3;err=abs(rich/analytic-1);assert err<mp.mpf('1e-8');lo,hi=de['velocity_derivative_bounds'][gi,di];assert M(lo)<=analytic<=M(hi);assert analytic>0 and abs((-analytic-rich)/rich)>1;refs.append(dict(group=gi,offset_index=di,analytic=str(analytic),Richardson=str(rich),relative_difference=str(err)))
checks['nine_independent_derivatives']=len(refs)==9;V=ev['velocity_bounds'];P=de['velocity_derivative_bounds'];D=[J(groups[i]['ls'])-iv.mpf(list(V[i,0])) for i in range(63)];DP=[-iv.mpf(list(P[i,0])) for i in range(63)];S=[(iv.mpf(list(V[i,1]))-iv.mpf(list(V[i,2])))/J(.02) for i in range(63)];SP=[(iv.mpf(list(P[i,1]))-iv.mpf(list(P[i,2])))/J(.02) for i in range(63)];mu=sum(D,iv.mpf(0))/63;mup=sum(DP,iv.mpf(0))/63;var=sum(((D[i]-D[j])**2 for i in range(63) for j in range(i+1,63)),iv.mpf(0))/(63*62);sm=sum(S,iv.mpf(0))/63;smp=sum(SP,iv.mpf(0))/63;T=var/63+J(.10)**2*sm**2;Tp=2*sum(((D[i]-mu)*DP[i] for i in range(63)),iv.mpf(0))/(63*62)+2*J(.10)**2*sm*smp;num=mup*T-mu*Tp/2;Zp=num/(T*iv.sqrt(T));values=dict(mu=mu,mu_prime=mup,variance=var,mean_slope=sm,mean_slope_prime=smp,T=T,T_prime=Tp,numerator=num,Z_prime=Zp,Z=mu/iv.sqrt(T),total=iv.sqrt(T));checks['complete_statistic_recomposition']=all(parse(d['statistics'][k]).a<=v.a and parse(d['statistics'][k]).b>=v.b for k,v in values.items());x=sp.symbols('x');u=sp.Function('u')(x);t=sp.Function('t')(x);checks['symbolic_Z_identity']=sp.simplify(sp.diff(u/sp.sqrt(t),x)-(sp.diff(u,x)*t-u*sp.diff(t,x)/2)/t**sp.Rational(3,2))==0;checks['same_regional_sign']=bool(Zp.b<0)==d['regional_negative_sign'];checks['finite_arrays']=bool(np.isfinite(P).all());checks['original_controls']=all(d['checks'].values());checks['input_hashes']=all(sha(r/f)==h for f,h in hashes.items());failure=bool(values['Z'].a>=2 or values['Z'].b<=-2 or values['total'].a>iv.mpf('.045').b);checks['same_necessary_failure']=failure==d['common_scope_interval_failure'];checks['same_inconclusive_verdict']=(bool(Zp.b>=0 and Zp.a<=0) and not d['regional_negative_sign']) or bool(Zp.b<0);result=dict(checks=checks,selected_derivatives=refs,radial_truncation_uncertainties=radial_cross,review_Z_prime=str(Zp),regional_negative_sign=bool(Zp.b<0),runtime_seconds=time.monotonic()-t0,input_sha256=hashes,scope='Independent70digit root signs/branch checks, nine admissible midpoint-coefficient normalized-root velocities/Richardson derivatives and whole-region statistic recomposition; no global or original floating certificate');(p/f'group_mesh_003_review_{tile:03d}.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'Zprime',str(Zp));assert all(checks.values())

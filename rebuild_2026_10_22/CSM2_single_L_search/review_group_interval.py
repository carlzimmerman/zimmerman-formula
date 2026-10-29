from pathlib import Path
import bisect,hashlib,json,resource,signal,time
import numpy as np
import mpmath as mp
from mpmath import iv
resource.setrlimit(resource.RLIMIT_CPU,(120,120));signal.alarm(150);p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'group_interval_001';paths=[Path(__file__),run/'results.json',run/'group_interval_evidence.npz',p/'group_preflight_001/results.json',p/'group_preflight_001/group_native_evidence.npz',p/'group_preflight_001/selected_groups.json',p.parent/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in paths};read=lambda i:json.loads(paths[i].read_text());d=read(1);assert 'statistics' in d;ev=dict(np.load(paths[2]));pre=read(3);z=dict(np.load(paths[4]));groups=read(5);c=pre['source_constants'];shape=[read(6)['cf_by_mass'][k] for k in ['1e+12','1e+13','1e+14']];mp.mp.dps=70;iv.dps=70;M=lambda v:mp.mpf(float(v));J=lambda v:iv.mpf(float(v));parse=lambda s:iv.mpf([v.strip() for v in s.strip('[]').split(',')]);B=lambda x:mp.log1p(x*x)+2*mp.log1p(x)-2*mp.atan(x);BI=lambda x:iv.log(1+x*x)+2*iv.log(1+x)-2*iv.atan2(x,iv.mpf(1));checks={};signs=0;t0=time.monotonic()
for root in d['root_brackets']:
 lo,hi,target=[parse(root[k]) for k in ['x_lower','x_upper','target']];assert (BI(lo)/lo**2-target).a>0 and (BI(hi)/hi**2-target).b<0;signs+=1
checks['378_independent_root_signs']=signs==378

def interp(v,xs,ys):
 if v<=xs[0]:return M(ys[0])
 if v>=xs[-1]:return M(ys[-1])
 i=bisect.bisect_right(xs,v)-1;return M(ys[i])+(M(ys[i+1])-M(ys[i]))*(v-M(xs[i]))/(M(xs[i+1])-M(xs[i]))

rhoc=3*(100*M(c['background']['h'])*1000/M(c['MPCE']))**2/(8*mp.pi*M(c['G540']));eps=lambda k:z['A_c2b_refit_'+k];refs=[]
for gi in [0,31,62]:
 for di,shift in enumerate([0.,.01,-.01]):
  lm=M(groups[gi]['lM'])+M(shift);Mb=mp.power(10,lm)*M(c['MS540']);parent=mp.power(10,M(c['background']['a'])+M(c['background']['b'])*(lm-10))*M(c['MS540']);R=mp.root(3*parent/(4*mp.pi*200*rhoc),3);a=M(groups[gi]['Re'])*M(c['KP540'])/M(1.8153);sel=parent/M(c['MSUNE']);svar=interp(mp.log10(sel/2),list(eps('lMg')),eps('s2'))-interp(mp.log10(sel),list(eps('lMg')),eps('s2'));Df=M(1.686)/(M(1.686)+M(.974)*mp.sqrt(svar));zf=interp(-Df,list(-eps('Dg')),eps('zg'));rho=18*mp.pi**2*M(float(eps('rhom0')))*(1+zf)**3;rf=mp.root(3*(sel/2)/(4*mp.pi*rho),3);coll=rho*rf/M(1e12);cfbase=interp(mp.log10(sel),[12.,13.,14.],shape)/M(shape[2])
  for ei,L in enumerate([mp.mpf('3.5'),max(mp.mpf('3.5001'),M(3.5001))]):
   Sigma=4/(3*(3*mp.log(2)-mp.pi/2))*(L*cfbase)**mp.mpf('1.25')*coll*M(c['MSUNE'])/M(3.0857e16)**2;target=parent/(mp.pi*Sigma*R**2);xl,xh=mp.mpf(1),mp.mpf(1e7)
   for _ in range(210):
    mid=(xl+xh)/2
    if B(mid)/mid**2>target:xl=mid
    else:xh=mid
   root=R/((xl+xh)/2);den=B(R/root);s2=mp.mpf(0)
   for k in range(3000):
    mass=Mb*M(z['M_H'][k])+parent*B(min(M(z['XG'][k])*a,R)/root)/den;s2+=M(z['kernel'][k])*mass
   v=mp.log10(M(c['G540'])/a*s2)/2-3;lo,hi=ev['endpoint_velocity_bounds'][3*gi+di,ei];assert M(lo)<=v<=M(hi);refs.append(dict(group=gi,dlM=shift,endpoint=ei,velocity=str(v)))
checks['18_independent_velocities']=len(refs)==18;V=ev['velocity_bounds'];D=[J(groups[i]['ls'])-iv.mpf(list(V[i,0])) for i in range(63)];s=[(iv.mpf(list(V[i,1]))-iv.mpf(list(V[i,2])))/J(.02) for i in range(63)];mean=sum(D,iv.mpf(0))/63;var=sum(((D[i]-D[j])**2 for i in range(63) for j in range(i+1,63)),iv.mpf(0))/(63*62);se=iv.sqrt(var/63);system=J(.10)*sum(s,iv.mpf(0))/63;tot=iv.sqrt(se**2+system**2);Z=mean/tot;review=dict(mean=mean,variance=var,se=se,sys=system,total=tot,Z=Z);checks['statistic_recomposition']=all(parse(d['statistics'][k]).a<=v.a and parse(d['statistics'][k]).b>=v.b for k,v in review.items());failure=bool(Z.a>=2 or Z.b<=-2 or tot.a>iv.mpf('.045').b);checks['same_verdict']=failure==d['common_scope_interval_failure'];checks['fixed_parent_and_R']=all(d['root_brackets'][2*j]['M']==d['root_brackets'][2*j+1]['M'] and d['root_brackets'][2*j]['R']==d['root_brackets'][2*j+1]['R'] for j in range(189));checks['increasing_columns']=all(parse(d['root_brackets'][2*j]['Sigma']).b<parse(d['root_brackets'][2*j+1]['Sigma']).a for j in range(189));checks['finite_arrays']=all(np.isfinite(v).all() for v in ev.values());checks['original_controls']=all(d['checks'].values());checks['input_hashes']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,root_signs=signs,reference_velocities=refs,review_statistics={k:str(v) for k,v in review.items()},common_scope_interval_failure=failure,runtime_seconds=time.monotonic()-t0,input_sha256=hashes,scope='Independent70digit compact-root/velocity and interval-statistic checks in fixed EPS/quadrature analytic scope; no globalL/original floating certificate');(p/'group_interval_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'Z',str(Z),'failure',failure);assert all(checks.values())

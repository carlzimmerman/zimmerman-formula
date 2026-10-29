import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,time
import numpy as np
from mpmath import iv
iv.dps=50;p=Path(__file__).resolve().parent;r=p.parents[1];ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);out.mkdir(parents=True,exist_ok=True);t0=time.monotonic();paths=[Path(__file__),p/'GROUP_REGIONAL_CRITERIA.md',p/'group_regional_contract.json',p/'group_preflight_001/results.json',p/'group_preflight_001/group_native_evidence.npz',p/'group_preflight_001/selected_groups.json',p/'group_preflight_review.json',p.parent/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json',p.parent/'P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py',p.parent/'CSM1_consistent_core_switch/heldout/MW_BURKERT_MONOTONICITY.md',p/'GROUP_REGIONAL_ROUTE.md',p/'group_derivative_001/results.json',p/'group_derivative_001/group_derivative_evidence.npz',p/'group_derivative_review.json',p/'group_interval_001/group_interval_evidence.npz'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in paths};read=lambda i:json.loads(paths[i].read_text());pre=read(3);z=dict(np.load(paths[4]));groups=read(5);c=pre['source_constants'];J=lambda x:iv.mpf(float(x));q=lambda f:iv.mpf(f.numerator)/iv.mpf(f.denominator);log10=lambda x:iv.log(x)/iv.log(10);pow10=lambda x:iv.exp(x*iv.log(10));B=lambda x:iv.log(1+x*x)+2*iv.log(1+x)-2*iv.atan2(x,iv.mpf(1));h=lambda x:4*x**3/((1+x)*(1+x*x)*B(x));L0=q(min(F('2.62'),F(2.62)));L1=q(max(F('3.5001'),F(3.5001)));shape=[read(7)['cf_by_mass'][k] for k in ['1e+12','1e+13','1e+14']];X=list(map(J,z['XG']));MH=list(map(J,z['M_H']));K=list(map(J,z['kernel']));a0=J(c['A0']['canonical']);floor=a0/(2*iv.pi*J(c['GE']));bg=c['background'];rho_c=3*(100*J(bg['h'])*1000/J(c['MPCE']))**2/(8*iv.pi*J(c['G540']));eps=lambda k:z['A_c2b_refit_'+k];lmgrid=eps('lMg');s2grid=eps('s2');negD=-eps('Dg');zg=eps('zg');rhom=J(float(eps('rhom0')));checks={};ck=lambda k,v:checks.update({k:bool(v)});ck('inherited_preflight',all(pre['checks'].values()) and all(read(6)['checks'].values()));ck('compact_monotone_domain',h(iv.mpf(1)).b<2 and all(v.a>0 for v in K));conversion=True

def cast(v):
 global conversion
 lo=float(np.nextafter(float(v.a),-np.inf));hi=float(np.nextafter(float(v.b),np.inf));assert np.isfinite([lo,hi]).all();conversion &= bool(J(lo)<=v.a and J(hi)>=v.b);return lo,hi

def interp(v,xs,ys):
 # Split only if an interval touches a knot; adjacent expressions enclose it.
 if v.b<=xs[0]:return J(ys[0])
 if v.a>=xs[-1]:return J(ys[-1])
 near=[]
 for i in range(len(xs)-1):
  if v.b>=xs[i] and v.a<=xs[i+1]:near.append(J(ys[i])+(J(ys[i+1])-J(ys[i]))/(J(xs[i+1])-J(xs[i]))*(v-J(xs[i])))
 assert near;return iv.mpf([min(a.a for a in near),max(a.b for a in near)])

V=np.empty((63,3,2));endpoint=np.empty((189,2,2));records=[];root_records=[];uncertain=[];source_misses=0;source_dev=0.
for gi,g in enumerate(groups):
 for di,shift in enumerate([0.,.01,-.01]):
  lm=J(g['lM'])+J(shift);Mb=pow10(lm)*J(c['MS540']);M=pow10(J(bg['a'])+J(bg['b'])*(lm-10))*J(c['MS540']);R=(3*M/(4*iv.pi*200*rho_c))**(iv.mpf(1)/3);a=J(g['Re'])*J(c['KP540'])/J(1.8153);Msel=M/J(c['MSUNE']);svar=interp(log10(Msel/2),lmgrid,s2grid)-interp(log10(Msel),lmgrid,s2grid);assert svar.a>0;S=iv.sqrt(svar);Df=J(1.686)/(J(1.686)+J(.974)*S);assert Df.b<1;zf=interp(-Df,negD,zg);rho=18*iv.pi**2*rhom*(1+zf)**3;rf=(3*(Msel/2)/(4*iv.pi*rho))**(iv.mpf(1)/3);coll=rho*rf/J(1e12);cfbase=interp(log10(Msel),np.array([12.,13.,14.]),np.array(shape))/J(shape[2]);cols=[4/(3*(3*iv.log(2)-iv.pi/2))*(lev*cfbase)**(iv.mpf(5)/4)*coll*J(c['MSUNE'])/J(3.0857e16)**2 for lev in [L0,L1]];idx=3*gi+di
  if cols[0].a<=floor.b:uncertain.append(dict(group=gi,dlM=shift,reason='Not certified on halo branch'));continue
  velocities=[]
  for ei,Sigma in enumerate(cols):
   target=M/(iv.pi*Sigma*R**2);xl=iv.mpf(1);xh=iv.mpf(1e7);assert (B(xl)/xl**2-target).a>0 and (B(xh)/xh**2-target).b<0
   for _ in range(120):
    mid=(xl+xh)/2;v=B(mid)/mid**2-target
    if v.a>0:xl=mid
    elif v.b<0:xh=mid
    else:break
   rl=R/xh;rh=R/xl;root_records.append(dict(cell=idx,endpoint=ei,x_lower=str(xl),x_upper=str(xh),target=str(target),M=str(M),R=str(R),Sigma=str(Sigma),r0_lower=str(rl),r0_upper=str(rh)));total=iv.mpf(0)
   for k in range(3000):
    rr=X[k]*a;tt=iv.mpf([min(rr.a,R.a),min(rr.b,R.b)]);lo=Mb*MH[k]+iv.pi*Sigma*rl**2*B(tt/rh);hi=Mb*MH[k]+iv.pi*Sigma*rh**2*B(tt/rl);mass=iv.mpf([lo.a,hi.b]);assert mass.a>0;total+=K[k]*mass
   s2=J(c['G540'])/a*total;v=log10(s2)/2-3;velocities.append(v);endpoint[idx,ei]=cast(v)
  combined=iv.mpf([velocities[0].a,velocities[1].b]);V[gi,di]=cast(combined)
  records.append(dict(cell=idx,group=g['id'],dlM=shift,Mb=str(Mb),a=str(a),column_lower=str(cols[0]),column_upper=str(cols[1]),floor=str(floor),velocity=str(combined)))
if uncertain:
 result=dict(checks=checks,status='INCONCLUSIVE_BRANCH',uncertain=uncertain,input_sha256=hashes,interval_exclusion=False);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0)
D=[J(groups[i]['ls'])-iv.mpf(list(V[i,0])) for i in range(63)];slopes=[(iv.mpf(list(V[i,1]))-iv.mpf(list(V[i,2])))/J(.02) for i in range(63)];mean=sum(D,iv.mpf(0))/63;var=sum(((D[i]-D[j])**2 for i in range(63) for j in range(i+1,63)),iv.mpf(0))/(63*62);se=iv.sqrt(var/63);sys=J(.10)*sum(slopes,iv.mpf(0))/63;tot=iv.sqrt(se**2+sys**2);Z=mean/tot;exclusion=bool(Z.a>=2 or Z.b<=-2 or tot.a>iv.mpf('.045').b);ck('coverage',len(records)==189 and len(root_records)==378);ck('finite_outward',conversion and np.isfinite(V).all() and np.isfinite(endpoint).all());ck('mass_order',np.all(endpoint[:,0,0]<=endpoint[:,1,1]));ck('statistic_finite',all(np.isfinite([float(v.a),float(v.b)]).all() for v in [mean,var,se,sys,tot,Z]));ck('wrong_velocity_mutation',abs(pre['statistic']['mean']-float((mean+iv.mpf('.01')).a))>1e-4);ck('input_hashes',all(sha(r/f)==h for f,h in hashes.items()));
# New whole-region derivative propagation; this is not an extrapolated local sign.
parse=lambda s:iv.mpf([v.strip() for v in s.strip('[]').split(',')])
BI=B;HI=lambda x,b:4*x**3/((1+x)*(1+x*x)*b);exp10=pow10
L=iv.mpf([L0.a,L1.b]);kernel=K;derivatives=np.empty((63,3,2));moments=[];radial_uncertainties=0
for idx,cell in enumerate(records):
 a=parse(cell['a']);Mb=parse(cell['Mb']);rlo,rhi=root_records[2*idx:2*idx+2];M=parse(rlo['M']);R=parse(rlo['R']);Sigma=iv.mpf([parse(rlo['Sigma']).a,parse(rhi['Sigma']).b]);r0=iv.mpf([parse(rhi['r0_lower']).a,parse(rlo['r0_upper']).b]);xl=parse(rlo['x_lower']).a;xh=parse(rhi['x_upper']).b;hx=iv.mpf([HI(xh,BI(xh)).a,HI(xl,BI(xl)).b]);assert hx.a>0 and hx.b<2;total=iv.mpf(0);visited=0
 for k,xx in enumerate(X):
  rr=xx*a
  if rr.a<R.b and rr.b>=R.a:radial_uncertainties+=1
  if rr.a>=R.b:continue
  arg=rr/r0;lo,hi=arg.a,arg.b;bl,bh=BI(lo),BI(hi);hin=iv.mpf([HI(hi,bh).a,HI(lo,bl).b]);E=(hin-hx)/(2-hx);assert E.b>=0;E=iv.mpf([max(E.a,iv.mpf(0).a),E.b]);ml=iv.pi*Sigma.a*r0.a**2*bl;mh=iv.pi*Sigma.b*r0.b**2*bh;mass=iv.mpf([ml.a,mh.b]);assert mass.a>0;total+=kernel[k]*mass*E;visited+=1
 gi,di=divmod(idx,3);v=iv.mpf(list(V[gi,di]));s2=exp10(2*(v+3));vp=5/(8*L*iv.log(10))*J(pre['source_constants']['G540'])/a*total/s2;derivatives[gi,di]=cast(vp);moments.append(dict(cell=idx,numerator=str(total),velocity_derivative=str(vp),active_radii=visited,outer_h=str(hx),r0_range=str(r0)))

ck('no_uncertain_radial_truncations',radial_uncertainties==0)
ck('inherited_derivative_review',all(read(13)['checks'].values()))
localV=dict(np.load(paths[14]))['velocity_bounds'];localP=dict(np.load(paths[12]))['velocity_derivative_bounds']
ck('local_velocity_containment',np.all(V[:,:,0]<=localV[:,:,0]) and np.all(V[:,:,1]>=localV[:,:,1]))
ck('local_derivative_containment',np.all(derivatives[:,:,0]<=localP[:,:,0]) and np.all(derivatives[:,:,1]>=localP[:,:,1]))
DP=[-iv.mpf(list(derivatives[i,0])) for i in range(63)];SP=[(iv.mpf(list(derivatives[i,1]))-iv.mpf(list(derivatives[i,2])))/J(.02) for i in range(63)]
mu=mean;mup=sum(DP,iv.mpf(0))/63;sm=sum(slopes,iv.mpf(0))/63;smp=sum(SP,iv.mpf(0))/63;T=var/63+J(.10)**2*sm**2
Tp=2*sum(((D[i]-mu)*DP[i] for i in range(63)),iv.mpf(0))/(63*62)+2*J(.10)**2*sm*smp
numerator=mup*T-mu*Tp/2;Zp=numerator/(T*iv.sqrt(T));negative=bool(Zp.b<0)
stats=dict(mu=mu,mu_prime=mup,variance=var,mean_slope=sm,mean_slope_prime=smp,T=T,T_prime=Tp,numerator=numerator,Z_prime=Zp,Z=Z,total=tot)
ck('finite_derivatives_statistic',np.isfinite(derivatives).all() and all(np.isfinite([float(v.a),float(v.b)]).all() for v in stats.values()))
ck('positive_velocity_derivatives',np.all(derivatives[:,:,0]>0));ck('outward_conversion',conversion);ck('final_hashes',all(sha(r/f)==h for f,h in hashes.items()))
np.savez_compressed(out/'group_regional_evidence.npz',velocity_bounds=V,endpoint_velocity_bounds=endpoint,velocity_derivative_bounds=derivatives)
result=dict(checks=checks,domain=[str(L0),str(L1)],records=records,root_brackets=root_records,moments=moments,statistics={k:str(v) for k,v in stats.items()},regional_negative_sign=negative,common_scope_interval_failure=exclusion,status='REGIONAL_NECESSARY_FAILURE' if exclusion else ('REGIONAL_NEGATIVE_SIGN' if negative else 'INCONCLUSIVE'),radial_truncation_uncertainties=radial_uncertainties,global_L_exclusion=False,original_floating_evaluator_certified=False,runtime_seconds=time.monotonic()-t0,input_sha256=hashes,scope='One unsplit canonical region; analytic fixed-EPS/quadrature only. No global or original floating certificate')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'status',result['status'],'Z',str(Z),'Zprime',str(Zp));assert all(checks.values())

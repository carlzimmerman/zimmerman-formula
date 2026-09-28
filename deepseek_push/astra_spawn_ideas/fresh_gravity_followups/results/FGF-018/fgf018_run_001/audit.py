import sys,json,csv,math,itertools,argparse
from pathlib import Path
from fractions import Fraction
sys.dont_write_bytecode=True
import numpy as np
from astropy.io import fits
R=Path.cwd();sys.path.insert(0,str(R))
from campaign_fresh_gravity_astra.stage_03.cluster_precision.constraint import force as registered_force
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);O=ap.parse_args().out;O.mkdir(parents=True,exist_ok=True)
DATA=R/'real_research/data/xcop';NAMES=['A1795','A2029','A2142','A2319','A644','A85','ZW1215'];G,MSUN,KPC=6.67430e-11,1.98847e30,3.085677581491367e19
zdata=json.loads((DATA/'xcop_r500_ettori2019.json').read_text())
old=list(csv.DictReader((R/'campaign_fresh_gravity_astra/stage_03/cluster_precision/run_003/shell_constraints.csv').open()));old={(x['name'],float(x['radius_kpc']),x['footing'],x['scaling'],x['kernel']):x for x in old}
oldint=list(csv.DictReader((R/'campaign_fresh_gravity_astra/stage_03/cluster_precision/run_003/continuity_intervals.csv').open()))
checks=[]
def check(n,v,t,ok):checks.append(dict(name=n,observed=v,tolerance=t,pass_=bool(ok)))
def F(b,a,k):
 if k=='Q':return math.sqrt(b)*math.sqrt(b+a)
 if k=='R':return b/-math.expm1(-math.sqrt(b/a))
 return float(registered_force(b,a,'M'))
def read(n,kind,ext,c,l,h,errors):
 with fits.open(DATA/n/(n+'_'+kind+'.fits')) as f:
  t=f[ext];ru=t.columns['RADIUS'].unit;scale={'kpc':1,'Mpc':1000}.get(ru,t.header.get('R500') if ru=='R/R500' else None);assert scale
  x=np.asarray(t.data['RADIUS'],float)*scale
  assert np.all(np.diff(x)>0)
  for k in (c,l,h):assert t.columns[k].unit in ('Msun','M_sun')
  m,lo,hi=[np.asarray(t.data[k],float) for k in (c,l,h)]
  L,U=(m-lo,m+hi) if errors else (lo,hi)
  assert np.all(m>0) and np.all(L<=m) and np.all(U>=m)
  lm=np.maximum.accumulate(L);um=np.minimum.accumulate(U[::-1])[::-1]
  return dict(r=x,m=m,L=L,U=U,lmono=lm,umono=um,loerr=lo,hierr=hi,kind=kind,monotone_feasible=bool(np.all(lm<=um)),all_L_positive=bool(np.all(L>0)),central_monotone=bool(np.all(np.diff(m)>=0)),metadata=dict(radius_unit=ru,radius_scale_to_kpc=scale,mass_unit=t.columns[c].unit,errors_are_magnitudes=errors,n_knots=len(x)))
def at(p,r,y):
 x=p['r'];assert x[0]<=r<=x[-1]
 j=min(max(int(np.searchsorted(x,r,side='right'))-1,0),len(x)-2);w=math.log(r/x[j])/math.log(x[j+1]/x[j]);assert -1e-12<=w<=1+1e-12
 # A zero/negative lower mass endpoint has infimum zero after positivity.
 if y[j]<=0 or y[j+1]<=0:return 0.
 return float(y[j]*(y[j+1]/y[j])**w)
def witness(p,i):
 if not p['monotone_feasible'] or not np.all(np.diff(p['m'])>0):return None
 L,U=p['lmono'],p['umono'];rr=p['r'][i+1]/p['r'][i]
 low=max(0.,math.log(max(L[i+1],1e-300)/U[i])/math.log(rr));high=math.log(U[i+1]/max(L[i],1e-300))/math.log(rr)
 if low>=1 or high<=0:return None
 target=(low+min(1.,high))/2;q=rr**target
 left=max(L[i],L[i+1]/q);right=min(U[i],U[i+1]/q)
 if left>right*(1+1e-13):return None
 x=(left+right)/2;y=q*x
 m=L.copy();m[i]=x;m[i+1:]=np.maximum(m[i+1:],y)
 # Strictly increasing central profile is a feasible interior direction.
 lam=1e-6;m=(1-lam)*m+lam*p['m'];s=math.log(m[i+1]/m[i])/math.log(rr)
 assert np.all(m>=p['L']*(1-1e-13)) and np.all(m<=p['U']*(1+1e-13)) and np.all(m>0) and np.all(np.diff(m)>0) and 0<s<1
 return dict(gas_knots_msun=m.tolist(),slope=s,endpoint_indices=[i,i+1],min_relative_lower_slack=float(np.min((m-p['L'])/p['m'])),min_relative_upper_slack=float(np.min((p['U']-m)/p['m'])),min_adjacent_mass_increment=float(np.min(np.diff(m))))
# Exact rational controls: s>1 iff m2/m1>r2/r1, all quantities positive.
synthetic=[]
for label,r1,r2,L1,U1,L2,U2,expected in [('positive',1,2,3,4,9,10,True),('boundary',1,2,3,4,8,10,False),('fails',1,2,2,4,3,8,False)]:
 test=Fraction(L2,U1)>Fraction(r2,r1);assert test==expected;synthetic.append(dict(label=label,exact_mass_ratio=str(Fraction(L2,U1)),exact_radius_ratio=str(Fraction(r2,r1)),strict_certificate=test))
check('exact rational synthetic slope signs',synthetic,'exact',True)
intervals=[];shells=[];witnesses=[];profilemeta=[];max_old_s=max_old_f=max_corner=0.;min_delta=math.inf;max_sensitivity=0.
for n in NAMES:
 g=read(n,'fgas_profile',1,'MGAS','MGAS_LO','MGAS_HI',True);h=read(n,'hydro_mass',1,'M_FORW','EM_FORW','EM_FORW',True);s=read(n,'mstar',2,'MSTAR','MSTAR_LO','MSTAR_HI',False)
 assert g['all_L_positive'] and g['monotone_feasible'] and np.all(np.diff(g['m'])>0)
 profilemeta.append(dict(name=n,profiles={k:dict(metadata=p['metadata'],all_L_positive=p['all_L_positive'],monotone_feasible=p['monotone_feasible'],central_monotone=p['central_monotone'],min_lower_mass=float(min(p['L'])),max_monotone_box_violation=float(max(p['lmono']-p['umono']))) for k,p in [('gas',g),('hydro',h),('star',s)]}))
 knots=[]
 for i in range(len(g['r'])-1):
  r1,r2=g['r'][i:i+2]
  if r1>=1000 or r2<=100:continue
  lo=max(100.,r1);hi=min(1000.,r2);rr=r2/r1
  sc=math.log(g['m'][i+1]/g['m'][i])/math.log(rr);sl=math.log(g['L'][i+1]/g['U'][i])/math.log(rr);sm=max(0.,math.log(g['lmono'][i+1]/g['umono'][i])/math.log(rr))
  wi=witness(g,i) if sl<=1+1e-10 else None
  if wi is not None:
   wi.update(name=n,interval_index=i);witnesses.append(wi)
  intervals.append(dict(name=n,interval_index=i,original_r1_kpc=float(r1),original_r2_kpc=float(r2),clip_lo_kpc=float(lo),clip_hi_kpc=float(hi),central_slope=sc,box_s_min=sl,gas_monotone_s_min=sm,box_strict_slope_survives=sl>1+1e-10,monotone_strict_slope_survives=sm>1+1e-10,strict_positive_counterwitness=wi is not None))
  knots.append((math.sqrt(lo*hi),'interval_midpoint',i))
 # 3 original shells are interior to the original gas knots, not derivative evaluations at knots.
 for rr in [100.,300.,1000.]:
  i=int(np.searchsorted(g['r'],rr))-1;assert g['r'][i]<rr<g['r'][i+1];knots.append((rr,'original_shell',i))
 for radius,kind,i in knots:
  rec=next(x for x in intervals if x['name']==n and x['interval_index']==i)
  cg,ch,cs=[at(p,radius,p['m']) for p in [g,h,s]]
  gh=at(g,radius,g['U']);sh=at(s,radius,s['U']);hl=at(h,radius,h['L']);C=G*MSUN/(radius*KPC)**2
  # Cartesian endpoint interpolation control, covering each distinct native grid.
  for p,which in [(g,'U'),(h,'L'),(s,'U')]:
   j=min(max(int(np.searchsorted(p['r'],radius,side='right'))-1,0),len(p['r'])-2)
   if p['L'][j]<=0 or p['L'][j+1]<=0:continue
   vals=[]
   for v1,v2 in itertools.product([p['L'][j],p['U'][j]],[p['L'][j+1],p['U'][j+1]]):
    arr=p['m'].copy();arr[j]=v1;arr[j+1]=v2;vals.append(at(p,radius,arr))
   bound=at(p,radius,p[which]);extreme=max(vals) if which=='U' else min(vals);max_corner=max(max_corner,abs(bound/extreme-1))
  for footing,a0 in [('canonical',9.3619e-11),('alternative',1.1279e-10)]:
   for scale in ['vacuum','H']:
    a=a0*(1 if scale=='vacuum' else math.sqrt(.315*(1+zdata[n]['z'])**3+.685))
    for k in ['Q','R','M']:
     dc=C*ch-F(C*(cg+cs),a,k);dl=C*hl-F(C*(gh+sh),a,k);min_delta=min(min_delta,dl)
     # Tight gas monotonic envelopes are always feasible. Other profiles only tighten if nonempty.
     gm=at(g,radius,g['umono']);hm=at(h,radius,h['lmono']) if h['monotone_feasible'] else hl;stm=at(s,radius,s['umono']) if s['monotone_feasible'] else sh
     dm=C*hm-F(C*(gm+stm),a,k)
     separate_h=max(0.,ch-at(h,radius,h['loerr']));separate_g=cg+at(g,radius,g['hierr']);ds=C*separate_h-F(C*(separate_g+sh),a,k);max_sensitivity=max(max_sensitivity,abs(ds-dl))
     if kind=='original_shell':
      oldr=old[n,radius,footing,scale,k];max_old_s=max(max_old_s,abs(rec['central_slope']-float(oldr['enclosed_gas_mass_log_slope'])));max_old_f=max(max_old_f,abs(F(C*(cg+cs),a,k)/(C*ch)-float(oldr['predicted_over_hydro'])))
     shells.append(dict(name=n,radius_kpc=radius,shell_kind=kind,gas_interval_index=i,footing=footing,scaling=scale,kernel=k,a_m_s2=a,central_s=rec['central_slope'],box_s_min=rec['box_s_min'],monotone_s_min=rec['gas_monotone_s_min'],central_delta_m_s2=dc,box_delta_min_m_s2=dl,monotone_delta_min_m_s2=dm,separate_error_interpolation_delta_min_m_s2=ds,box_sign_certificate=rec['box_s_min']>1+1e-10 and dl>1e-20,monotone_sign_certificate=rec['gas_monotone_s_min']>1+1e-10 and dm>1e-20,slope_counterwitness=rec['strict_positive_counterwitness']))
# Compare the exact same original intervals to old central results.
for x,y in zip(intervals,oldint):
 assert x['name']==y['name'] and abs(x['clip_lo_kpc']-float(y['radius_inner_kpc']))<1e-10 and abs(x['clip_hi_kpc']-float(y['radius_outer_kpc']))<1e-10
 max_old_s=max(max_old_s,abs(x['central_slope']-float(y['enclosed_gas_mass_log_slope'])))
check('189 original gas intervals reproduced',len(intervals),189,len(intervals)==189)
check('central slopes agree with previous profiles',max_old_s,1e-11,max_old_s<1e-11)
check('252 original force ratios agree',max_old_f,1e-12,max_old_f<1e-12)
check('positive knot interpolation corner extrema',max_corner,1e-13,max_corner<1e-13)
check('at least one explicit slope counterwitness when any interval fails',len(witnesses),'nonzero if needed',len(witnesses)>0 or all(x['box_strict_slope_survives'] for x in intervals))
summary=[]
for n in NAMES:
 for foot,sc,k in itertools.product(['canonical','alternative'],['vacuum','H'],['Q','R','M']):
  rows=[x for x in shells if (x['name'],x['footing'],x['scaling'],x['kernel'])==(n,foot,sc,k)];orig=[x for x in rows if x['shell_kind']=='original_shell'];mid=[x for x in rows if x['shell_kind']=='interval_midpoint']
  summary.append(dict(name=n,footing=foot,scaling=sc,kernel=k,original_shell_count=len(orig),original_certified_radii_kpc=[x['radius_kpc'] for x in orig if x['box_sign_certificate']],midpoint_count=len(mid),midpoint_certificates=sum(x['box_sign_certificate'] for x in mid),any_box_certificate=any(x['box_sign_certificate'] for x in rows),any_monotone_certificate=any(x['monotone_sign_certificate'] for x in rows),delta_failures=sum(x['box_delta_min_m_s2']<=1e-20 for x in rows),min_box_delta_m_s2=min(x['box_delta_min_m_s2'] for x in rows)))
def csvout(name,rows):
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csvout('interval_certificates.csv',intervals);csvout('shell_certificates.csv',shells)
for file,obj in [('branch_summary.json',summary),('gas_counterwitnesses.json',witnesses),('profile_box_audit.json',profilemeta)]: (O/file).write_text(json.dumps(obj,indent=2)+'\n')
result=dict(checks=checks,intervals=len(intervals),intervals_slope_survives=sum(x['box_strict_slope_survives'] for x in intervals),intervals_monotone_slope_survives=sum(x['monotone_strict_slope_survives'] for x in intervals),counterwitness_count=len(witnesses),shell_branch_evaluations=len(shells),original_shell_certificates=sum(x['box_sign_certificate'] for x in shells if x['shell_kind']=='original_shell'),midpoint_certificates=sum(x['box_sign_certificate'] for x in shells if x['shell_kind']=='interval_midpoint'),cluster_branch_combinations_with_certificate=sum(x['any_box_certificate'] for x in summary),total_cluster_branch_combinations=len(summary),minimum_delta_lower_bound_m_s2=min_delta,separate_error_interpolation_max_delta_shift_m_s2=max_sensitivity,all_checks_pass=all(x['pass_'] for x in checks),shared_kernel='M registered implementation only; Q/R independently evaluated',statistical_interpretation='none')
(O/'checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_checks_pass']

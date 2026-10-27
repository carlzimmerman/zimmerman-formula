#!/usr/bin/env python3
"""Independent read-only finite checker; never imports or executes project scripts."""
import csv, hashlib, json, math, pathlib, platform, sys, time
import numpy as np
start=time.monotonic()
S=pathlib.Path('/private/tmp/zimmerman_empirical_host_20261019_gcjfj1az')
prov=json.loads((S/'source_provenance.json').read_text()); B=pathlib.Path(prov['original_root'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hashes_before={f:sha(B/f) for f in prov['sha256']}
assert hashes_before==prov['sha256']
assert {f:sha(S/f) for f in prov['sha256']}==prov['sha256']
packet=json.loads((S/'PACKET_SHA256.json').read_text())
assert all(sha(S/f)==h for f,h in packet.items())
r24=json.loads((B/'campaign_fresh_gravity/CFG824_dwarf_age_fossil/cfg824_results.json').read_text())['rows']
r27=json.loads((B/'campaign_fresh_gravity/CFG827_dwarf_age_sfh_ml/cfg827_results.json').read_text())['rows']
r28=json.loads((B/'campaign_fresh_gravity/CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json').read_text())
r56=json.loads((B/'campaign_fresh_gravity/CFG856_universal_extra_speed/cfg856_results.json').read_text())
r57=json.loads((B/'campaign_fresh_gravity/CFG857_extra_speed_size/cfg857_results.json').read_text())
saved=json.loads((S/'run/result.json').read_text())['footings']
robust=json.loads((S/'robustness_run/result.json').read_text())
lvd={};dupes=[]
for name in ['mw','m31','local_field']:
 for r in csv.DictReader((B/f'real_research/data/dsph/lvd_dwarf_{name}.csv').open()):
  if r['name'] in lvd:dupes.append(r['name'])
  lvd[r['name']]=r
exclude={'WLM','NGC 6822','IC 1613','Leo A','Sagittarius dIrr','Pegasus dIrr','M 32'}
expected=set(r27)-exclude
O={'software':{'python':sys.version.split()[0],'numpy':np.__version__,'platform':platform.platform()},'source_hashes_match':True,'packet_hashes_match':True,'source_duplicate_names':dupes,'footings':{}}
# Find every derivative sign-changing root on a log1p grid, refine by bisection,
# and compare all roots plus boundary; independent of saved golden search.
max_roots=0;max_score_discrep=0.;max_param_discrep=0.
def params(train):
 global max_roots
 v=np.array([r['s2'] for r in train]); o=np.array([r['so']**2 for r in train]);lv=np.log(o)
 upper=max(0.,float(max(o-v)))
 def der(a):return float(np.sum((np.log(v+a)-lv)/(v+a)))
 def loss(a):return float(np.mean((np.log10(o)-np.log10(v+a))**2)/4)
 roots=[]
 if upper:
  g=np.expm1(np.linspace(0.,math.log1p(upper),4097));d=np.array([der(a) for a in g])
  for i in np.where(d[:-1]*d[1:]<0)[0]:
   lo,hi=float(g[i]),float(g[i+1]);flo=der(lo)
   for _ in range(75):
    mid=(lo+hi)/2;fm=der(mid)
    if fm*flo>0:lo=mid;flo=fm
    else:hi=mid
   roots.append((lo+hi)/2)
 max_roots=max(max_roots,len(roots))
 candidates=[0.,upper]+roots;a=min(candidates,key=loss)
 q=max(1.,math.exp(float(np.mean(lv-np.log(v)))))
 return a,q

def score(train,test):
 a,q=params(train);v=np.array([r['s2'] for r in test]);yo=np.log10([r['so'] for r in test])
 return {'additive':yo-.5*np.log10(v+a),'multiplicative':yo-.5*np.log10(q*v)},(a,q)
def pooled(rows,cross):
 err={'additive':[],'multiplicative':[]}; folds={}
 pairs=[([r for r in rows if r['host']==h1],[r for r in rows if r['host']==h2],h1+'_to_'+h2) for h1,h2 in [('mw','m_031'),('m_031','mw')]] if cross else [(rows[:i]+rows[i+1:],[r],r['name']) for i,r in enumerate(rows)]
 for train,test,label in pairs:
  e,p=score(train,test);folds[label]={'N_train':len(train),'N_test':len(test),'A':p[0],'Q':p[1]}
  for k in err:err[k].extend(e[k])
 return {k:float(np.sqrt(np.mean(np.array(v)**2))) for k,v in err.items()},folds
for f,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 raw=r28[f+'|nu_e']['rows'];assert len(raw)==len(expected)==29;assert len({r['name'] for r in raw})==29;assert {r['name'] for r in raw}==expected
 rows=[];max_delta=0.;max_row=0.
 savedrows={r['name']:r for r in saved[f]['rows']}
 for src in raw:
  n=src['name'];l=lvd[n];radius=4*float(l.get('rhalf_sph_physical') or l['rhalf_physical'])/3*3.0857e16
  mass=r27[n]['ups']*10**(.4*(4.83-float(l['M_V'])))
  baryon=6.674e-11*mass*1.989e30/(2*radius*radius)
  law=baryon/(-math.expm1(-math.sqrt(baryon/a0)));s2=law*radius/(3*1e6)
  so=float(l['vlos_sigma']);assert so==r24[n]['so']
  delta=math.log10(so*so/s2);max_delta=max(max_delta,abs(delta-src['delta']),abs(math.log10(baryon)-src['lgbar']))
  d={'name':n,'host':l.get('host') or 'field','s2':s2,'so':so,'delta':delta,'lgbar':math.log10(baryon),'logM':math.log10(mass),'lr':math.log10(radius/3.0857e19/.3),'lVl':.5*math.log10(law*radius/1e6)}
  if delta>.05:
   d['lVx']=math.log10(math.sqrt(3*(so*so-s2)));d['normalized']=.5*math.log10(math.expm1(delta*math.log(10)))
  for k,v in d.items():
   if k not in ('name','host','s2'):max_row=max(max_row,abs(v-savedrows[n][k]))
  max_row=max(max_row,abs(d['s2']-savedrows[n]['sl2']))
  rows.append(d)
 s=[r for r in rows if r['delta']>.05];mw=[r for r in s if r['host']=='mw'];m31=[r for r in s if r['host']=='m_031']
 gaps={k:float(np.mean([r[k] for r in m31])-np.mean([r[k] for r in mw])) for k in ['lVx','lVl','normalized','logM','delta']}
 X=np.array([[1.,r['lr'],float(r['host']=='m_031')] for r in s]);assert np.linalg.matrix_rank(X)==3
 # Solve normal equations as an orthogonal implementation vs source lstsq.
 beta={k:np.linalg.solve(X.T@X,X.T@np.array([r[k] for r in s])) for k in ['lVx','lVl','normalized']}
 max_beta=max(abs(beta[k][j]-saved[f]['same_design_host_decomposition'][k][v]) for k in beta for j,v in enumerate(['intercept','size_slope','host_coefficient']))
 assert max_delta<1e-12 and max_row<1e-10 and max_beta<1e-12
 assert max(abs(beta['lVx']-beta['lVl']-beta['normalized']))<1e-12
 assert abs(beta['lVx'][2]-r57[f]['host_offset'])<1e-12
 assert abs(10**np.mean([r['lVx'] for r in mw])-r56[f]['Vx0_kms'])<1e-12
 satellites=[r for r in s if r['host']!='field'];T=np.array([[1.,r['lr'],float(r['host']=='m_031')] for r in satellites]);pure=np.linalg.solve(T.T@T,T.T@np.array([r['lVx'] for r in satellites]))
 slopes={k:float(np.cov([r['logM'] for r in s],[r[k] for r in s],ddof=0)[0,1]/np.var([r['logM'] for r in s])) for k in beta}
 assert max(abs(slopes[k]-robust[f]['pooled_logM_slope_decomposition'][k]) for k in slopes)<1e-12
 scores={}
 subsets={'all_satellites':[r for r in rows if r['host']!='field'],'low_g_satellites':[r for r in rows if r['host']!='field' and r['lgbar']<-11.9],'all_29':rows,'low_g_all':[r for r in rows if r['lgbar']<-11.9]}
 for label,sub in subsets.items():
  z,folds=pooled(sub,label.endswith('satellites'));e,p=score(sub,sub)
  scores[label]={'N':len(sub),'pooled_rmse':z,'full_A':p[0],'full_Q':p[1]}
  for m in z:max_score_discrep=max(max_score_discrep,abs(z[m]-saved[f]['scores'][label]['pooled_rmse_log_sigma'][m]))
  for ix,m in enumerate(['additive','multiplicative']):max_param_discrep=max(max_param_discrep,abs(p[ix]-saved[f]['scores'][label]['full_fit'][m]['parameter']))
  for fold,v in folds.items():
   if label.endswith('satellites'):
    for ix,m in enumerate(['additive','multiplicative']):max_param_discrep=max(max_param_discrep,abs(v[['A','Q'][ix]]-saved[f]['scores'][label]['folds'][fold]['models'][m]['parameter']))
 low=subsets['low_g_satellites'];jack=[];max_jack=0.
 for check in robust[f]['jackknife']:
  n=check['excluded'];z,_=pooled([r for r in low if r['name']!=n],True)
  max_jack=max(max_jack,abs(z['additive']-check['additive_rmse']),abs(z['multiplicative']-check['multiplicative_rmse']))
  if n=='Hercules':jack.append({'excluded':n,**z})
 assert len(robust[f]['jackknife'])==len(low)==16 and {x['excluded'] for x in robust[f]['jackknife']}=={x['name'] for x in low}
 herc=next(r for r in rows if r['name']=='Hercules')
 O['footings'][f]={'N':len(rows),'N_selected':len(s),'excluded':[r['name'] for r in rows if r['delta']<=.05],'max_reconstructed_delta_lgbar_error':max_delta,'max_reconstructed_saved_row_error':max_row,'max_ols_coefficient_error':max_beta,'raw_M31_minus_MW_gaps':gaps,'same_design_coefficients':{k:beta[k].tolist() for k in beta},'satellites_only_host_coefficient_lVx':float(pure[2]),'pooled_mass_slopes':slopes,'scores':scores,'max_jackknife_rmse_error':max_jack,'Hercules_deletion':jack,'Hercules':{**herc,'law_sigma':math.sqrt(herc['s2']),'sigma_error_CFG824':r24['Hercules']['eso'],'vlos_sigma_ep':lvd['Hercules']['vlos_sigma_ep'],'vlos_sigma_em':lvd['Hercules']['vlos_sigma_em']}}
assert max_score_discrep<1e-7 and max_param_discrep<1e-4
hashes_after={f:sha(B/f) for f in prov['sha256']};assert hashes_after==hashes_before
O.update({'max_forward_rmse_error_dex':max_score_discrep,'max_parameter_discrepancy':max_param_discrep,'maximum_derivative_roots_per_fit_on_4097_point_grid':max_roots,'source_hashes_after_equal_before':True,'bootstrap_rerun':False,'runtime_seconds':time.monotonic()-start})
print(json.dumps(O,indent=2))

#!/usr/bin/env python3
"""Bounded exploratory finite re-score; no project mutation or source script imports.
Models minimize equal-object MSE in log10 observed LOS dispersion.
Additive: sigma_pred^2 = sigma_law^2 + A, A >= 0.
Multiplicative: sigma_pred^2 = Q sigma_law^2, Q >= 1.
No measurement weighting: object scatter dominates; this is prediction scoring, not a likelihood.
"""
import csv,json,math,pathlib,sys,time,platform
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent
G,MSUN,PC=6.674e-11,1.989e30,3.0857e16
A0={'canonical':9.3603e-11,'alt':1.1312e-10}
read=lambda p:json.loads((ROOT/p).read_text())
R24=read('campaign_fresh_gravity/CFG824_dwarf_age_fossil/cfg824_results.json')['rows']
R27=read('campaign_fresh_gravity/CFG827_dwarf_age_sfh_ml/cfg827_results.json')['rows']
R28=read('campaign_fresh_gravity/CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json')
REF56=read('campaign_fresh_gravity/CFG856_universal_extra_speed/cfg856_results.json')
REF57=read('campaign_fresh_gravity/CFG857_extra_speed_size/cfg857_results.json')
LVD={}
for fn in ('lvd_dwarf_mw.csv','lvd_dwarf_m31.csv','lvd_dwarf_local_field.csv'):
 for r in csv.DictReader((ROOT/'real_research/data/dsph'/fn).open()): LVD[r['name']]=r

def regression_coeff(rows,y):
 X=np.array([[1.,r['lr'],float(r['host']=='m_031')] for r in rows])
 return np.linalg.lstsq(X,np.array([r[y] for r in rows]),rcond=None)[0]

def golden(f,lo,hi):
 t=(math.sqrt(5)-1)/2
 c=hi-t*(hi-lo);d=lo+t*(hi-lo);fc=f(c);fd=f(d)
 for _ in range(120):
  if fc<fd: hi,d,fd=d,c,fc;c=hi-t*(hi-lo);fc=f(c)
  else: lo,c,fc=c,d,fd;d=lo+t*(hi-lo);fd=f(d)
 x=(lo+hi)/2
 return 0. if f(0.)<=f(x) else x

def fit_predict(train,test,model):
 so=np.array([r['so'] for r in train]);sl2=np.array([r['sl2'] for r in train]);tl2=np.array([r['sl2'] for r in test])
 if model=='additive':
  f=lambda a:float(np.mean((np.log10(so)-.5*np.log10(sl2+a))**2))
  p=golden(f,0.,10*max(float(so.max()**2),1.))
  pred=.5*np.log10(tl2+p)
 else:
  p=max(1.,10**float(np.mean(2*np.log10(so)-np.log10(sl2))))
  pred=.5*np.log10(p*tl2)
 err=np.log10([r['so'] for r in test])-pred
 return {'parameter':float(p),'rmse_log_sigma':float(np.sqrt(np.mean(err**2))),'bias_log_sigma':float(err.mean())},err

out={'contract':'exploratory host scale decomposition and equal-object forward-dispersion cross-host prediction','software':{'python':sys.version.split()[0],'numpy':np.__version__,'platform':platform.platform()},'randomness':{'generator':'numpy PCG64','seed':20261019,'draws':2000},'footings':{}}
for foot,a0 in A0.items():
 rows=[]
 for r in R28[foot+'|nu_e']['rows']:
  n=r['name'];l=LVD[n];rh=4/3*float(l.get('rhalf_sph_physical') or l['rhalf_physical'])*PC
  ms=R27[n]['ups']*10**(.4*(4.83-float(l['M_V'])))
  gb=G*ms*.5*MSUN/rh**2;gl=gb/(-math.expm1(-math.sqrt(gb/a0)))
  sl2=gl*rh/3/1e6;so=R24[n]['so'];de=math.log10(so**2/sl2)
  assert abs(de-r['delta'])<1e-10 and abs(math.log10(gb)-r['lgbar'])<1e-10
  d={'name':n,'host':l.get('host') or 'field','delta':de,'lgbar':r['lgbar'],'logM':math.log10(ms),'lr':math.log10(rh/PC/1000/.3),'sl2':sl2,'so':so,'lVl':.5*math.log10(3*sl2)}
  if de>.05:
   d['lVx']=.5*math.log10(3*(so**2-sl2));d['normalized']=.5*math.log10(10**de-1)
   assert abs(d['lVx']-d['lVl']-d['normalized'])<1e-12
  rows.append(d)
 selected=[r for r in rows if r['delta']>.05]
 cf={k:regression_coeff(selected,k) for k in ('lVx','lVl','normalized','logM')}
 assert np.max(abs(cf['lVx']-cf['lVl']-cf['normalized']))<1e-12
 assert abs(cf['lVx'][2]-REF57[foot]['host_offset'])<1e-10
 mw=[r for r in selected if r['host']=='mw'];m31=[r for r in selected if r['host']=='m_031']
 assert abs(10**np.mean([r['lVx'] for r in mw])-REF56[foot]['Vx0_kms'])<1e-10
 rng=np.random.default_rng(20261019)
 strata=[[r for r in selected if r['host']==h] for h in ('mw','m_031','field')]
 bs=[]
 for _ in range(2000):
  sample=[group[i] for group in strata for i in rng.integers(0,len(group),len(group))]
  bs.append([regression_coeff(sample,k)[2] for k in ('lVx','lVl','normalized')])
 se=np.std(bs,axis=0)
 result={'N_all':len(rows),'N_selected':len(selected),'selection_excluded':[r['name'] for r in rows if r['delta']<=.05],
 'selected_host_counts':{h:sum(r['host']==h for r in selected) for h in ('mw','m_031','field')},
 'same_design_host_decomposition':{k:{'intercept':float(cf[k][0]),'size_slope':float(cf[k][1]),'host_coefficient':float(cf[k][2]),'host_bootstrap_se':float(se[i]) if i<3 else None} for i,k in enumerate(('lVx','lVl','normalized','logM'))},
 'selected_means':{h:{k:float(np.mean([r[k] for r in selected if r['host']==h])) for k in ('lVx','lVl','normalized','logM','delta')} for h in ('mw','m_031','field')},'scores':{}}
 for label,subset in [('all_satellites',[r for r in rows if r['host'] in ('mw','m_031')]),('low_g_satellites',[r for r in rows if r['host'] in ('mw','m_031') and r['lgbar']<-11.9]),('all_29',rows),('low_g_all',[r for r in rows if r['lgbar']<-11.9])]:
  cv={};allerr={model:[] for model in ('additive','multiplicative')}
  if label.endswith('satellites'):
   for trhost,tehost in [('mw','m_031'),('m_031','mw')]:
    train=[r for r in subset if r['host']==trhost];test=[r for r in subset if r['host']==tehost]
    scored={}
    for model in ('additive','multiplicative'):
     score,err=fit_predict(train,test,model);allerr[model].extend(err.tolist());scored[model]=score
    cv[trhost+'_to_'+tehost]={'N_train':len(train),'N_test':len(test),'models':scored}
  else:
   for i in range(len(subset)):
    train=subset[:i]+subset[i+1:];test=[subset[i]]
    for model in ('additive','multiplicative'):
     _,err=fit_predict(train,test,model);allerr[model].append(float(err[0]))
  pooled={m:float(np.sqrt(np.mean(np.array(err)**2))) for m,err in allerr.items()}
  full={m:fit_predict(subset,subset,m)[0] for m in ('additive','multiplicative')}
  result['scores'][label]={'N':len(subset),'folds':cv,'pooled_rmse_log_sigma':pooled,'full_fit':full}
 result['rows']=rows
 out['footings'][foot]=result
path=ROOT/'run'/'result.json';path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({f:{k:v for k,v in r.items() if k not in ('rows',)} for f,r in out['footings'].items()},indent=2))

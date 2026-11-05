"""HC-005: group-held-out hot-halo prediction and independent rotation measurements.
Command: python horizon_cluster_2026_11_05/continuation.py FRESH_OUTPUT
"""
import json,sys,re,csv
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.optimize import minimize
from scipy.stats import pearsonr
B=Path(__file__).resolve().parent;O=Path(sys.argv[1]);O.mkdir(parents=True,exist_ok=True)
rng=np.random.default_rng(32007);checks=[]
def ck(s,b):
 assert b,s
 checks.append(s)
def fit(X,y):
 b=np.linalg.lstsq(X,y,rcond=None)[0];e=y-np.sum(X*b,axis=1)
 assert np.isfinite(b).all() and np.isfinite(e).all()
 return b,e
def loo(X,y):
 pred=np.zeros(len(y))
 for i in range(len(y)):
  take=np.arange(len(y))!=i;b,_=fit(X[take],y[take]);pred[i]=X[i]@b
 return float(np.sqrt(np.mean((pred-y)**2)))
def partial(X,y,t):
 return float(pearsonr(fit(X,y)[1],fit(X,t)[1]).statistic)
def envclass(e):
 for pre in ['BCG','BGG','BFG']:
  if e.startswith(pre):return pre
 return 'isolated' if e=='isolated' else 'satellite'
gp=json.loads((B/'data/gaspari.json').read_text());hot={r['name']:r for r in gp['xray_table']}
rows=[dict(r,environment=hot[r['name']]['environment'],logTx=hot[r['name']]['logTx_g'],err_logTx=hot[r['name']]['err_logTx_g']) for r in gp['optical_table']]
# Explicit source-host alias map; no position/mass-based grouping or outcome-dependent changes.
aliases={'N4486/N4472':'Virgo','N4258(M106)':'CVnI','N3607(LeoII)':'LeoII',
 'N4594(M104)':'Sombrero','N7619(Pegasus)':'Pegasus','N1316(ForA)':'FornaxA',
 'N3842':'A1367','N1275(Perseus)':'Perseus'}
groups=[]
for r in rows:
 e=r['environment']
 group=('isolated_'+r['name']) if e=='isolated' else e.split(':')[-1].strip()
 groups.append(aliases.get(group,group))
groups=np.array(groups);ug=np.unique(groups);counts=Counter(groups)
ck('Virgo central and satellite grouping',sum(groups=='Virgo')==12)
ck('M106 host alias grouping',sum(groups=='CVnI')==4)
classes=['BCG','BGG','BFG','isolated','satellite']
X=np.array([[1,r['logSigma'],r['logLK'],r['logRe_opt_kpc'],np.log10(r['distance_Mpc'])]+[float(envclass(r['environment'])==c) for c in classes[1:]] for r in rows])
y=np.array([r['logMBH'] for r in rows]);t=np.array([r['logTx'] for r in rows]);Xt=np.c_[X,t]
res={'group_count':len(ug),'group_members':{str(g):[r['name'] for r,gg in zip(rows,groups) if gg==g] for g in ug},'alias_map':aliases}
pred0=np.zeros(len(y));pred1=np.zeros(len(y));pergroup=[]
for g in ug:
 test=groups==g;train=~test
 ck('group disjoint '+g,not set(groups[test])&set(groups[train]))
 ck('full-rank group fold '+g,np.linalg.matrix_rank(Xt[train])==Xt.shape[1])
 b0,_=fit(X[train],y[train]);b1,_=fit(Xt[train],y[train]);pred0[test]=X[test]@b0;pred1[test]=Xt[test]@b1
 pergroup.append({'group':str(g),'n':int(test.sum()),'mse_baseline':float(np.mean((y[test]-pred0[test])**2)),'mse_temperature':float(np.mean((y[test]-pred1[test])**2))})
res['leave_group_out_object_weighted_RMSE']=[float(np.sqrt(np.mean((y-p)**2))) for p in [pred0,pred1]]
res['leave_group_out_equal_group_RMSE']=[float(np.sqrt(np.mean([r[k] for r in pergroup]))) for k in ['mse_baseline','mse_temperature']]
res['per_group_predictions']=pergroup
weights=np.array([1/counts[g] for g in groups]);b,_=fit(Xt*np.sqrt(weights[:,None]),y*np.sqrt(weights))
res['equal_group_weight_temperature_coefficient']=float(b[-1])
boot=[];delta=[]
indices={g:np.where(groups==g)[0] for g in ug}
for _ in range(2000):
 chosen=rng.choice(ug,len(ug));ix=np.concatenate([indices[g] for g in chosen])
 if np.linalg.matrix_rank(Xt[ix])==Xt.shape[1]:boot.append(fit(Xt[ix],y[ix])[0][-1])
 # Uncertainty in existing group-held-out squared-error difference; not a new external test.
 chosen_i=rng.integers(0,len(pergroup),len(pergroup))
 delta.append(float(np.mean([pergroup[i]['mse_baseline']-pergroup[i]['mse_temperature'] for i in chosen_i])))
res['group_bootstrap_temperature_coefficient_95pct']=np.quantile(boot,[.025,.5,.975]).tolist();res['group_bootstrap_full_rank_draws']=len(boot)
res['group_bootstrap_MSE_improvement_95pct']=np.quantile(delta,[.025,.5,.975]).tolist()
mask=groups!='Virgo';res['without_Virgo']={'n':int(mask.sum()),'partial_r':partial(X[mask],y[mask],t[mask]),'temperature_coefficient':float(fit(Xt[mask],y[mask])[0][-1])}

# Conditional effective-variance likelihood; does not specify a latent population or selection.
sy=np.array([r['err_logMBH'] for r in rows]);sx=np.zeros_like(Xt)
for j,k in [(1,'err_logSigma'),(2,'err_logLK'),(3,'err_logRe_opt_kpc'),(9,'err_logTx')]:sx[:,j]=[r[k] for r in rows]
sd=np.array([r['err_distance_Mpc']/r['distance_Mpc']/np.log(10) for r in rows]);sx[:,4]=sd
ck('finite quoted errors',np.isfinite(sx).all() and np.isfinite(sy).all())
dcap=np.minimum.reduce([sd,sy,sx[:,2]/2,sx[:,3]])
def evfit(shared):
 def obj(theta):
  b=theta[:-1];s=np.exp(theta[-1]);v=sy**2+np.sum((sx*b)**2,axis=1)+s*s
  if shared:
   # y,distance,L,R distance powers =1,1,2,1. Add covariances without changing diagonals.
   v+=dcap**2*((1-2*b[2]-b[3]-b[4])**2-1-4*b[2]**2-b[3]**2-b[4]**2)
  if np.any(v<=0):return 1e100
  e=y-Xt@b
  return .5*np.sum(np.log(v)+e*e/v)
 init=fit(Xt,y)[0];fits=[]
 for start in [-2.,-1.,-3.]:
  out=minimize(obj,np.r_[init,start],method='L-BFGS-B',bounds=[(None,None)]*len(init)+[(-6,1)],options={'maxiter':4000,'ftol':1e-12,'gtol':1e-7,'maxls':40})
  fits.append(out)
 best=min(fits,key=lambda q:q.fun)
 ck('effective variance converged '+str(shared),best.success and np.isfinite(best.fun))
 ck('effective variance multi-start agreement '+str(shared),max(q.fun for q in fits)-min(q.fun for q in fits)<1e-4)
 return {'temperature_coefficient':float(best.x[-2]),'intrinsic_scatter_dex':float(np.exp(best.x[-1])),'objective':float(best.fun),'success':bool(best.success),'logscatter_bound_hit':bool(abs(best.x[-1]+6)<.01 or abs(best.x[-1]-1)<.01)}
res['effective_variance_diagonal']=evfit(False);res['effective_variance_shared_distance']=evfit(True)
res['effective_variance_warning']='Sensitivity models, not full latent-population regression; shared distance component capped by all quoted marginal errors. No selection model, covariance with temperature, or cluster random effect.'

# Rotational velocities measured independently of the BH mass; implied halo masses NOT used.
dv=json.loads((B/'data/davis.json').read_text())['rows'];sizes=json.loads((B/'data/galaxies.json').read_text())['rows']
def canon(s):
 m=re.fullmatch(r'(NGC|IC)\s*0*(\d+)',s)
 return m[1]+str(int(m[2])) if m else s.replace(' ','')
massmap={canon(r['name']):r for r in sizes};matched=[]
for r in dv:
 q=massmap.get(canon(r['name']))
 if q is not None and r['vmax_km_s'] is not None:
  matched.append(dict(r,logMgal=q['logMgal'],logMsph=q['logMsph'],Re_sph_kpc=q['Re_sph_kpc'],author_excluded=q['author_excluded'],upper_limit_2023=q['upper_limit'],logMBH_2023=q['logMBH']))
ck('48 rotation source rows',len(dv)==48)
ck('42 finite velocities',sum(r['vmax_km_s'] is not None for r in dv)==42)
rot={'source_rows':48,'finite_velocities':42,'mass_matches':len(matched),'matched_rows':matched,'fits':{}}
allrot=[r for r in dv if r['vmax_km_s'] is not None and not r['limit_vmax']]
vr=np.log10([r['vmax_km_s'] for r in allrot]);br=np.array([r['logMBH'] for r in allrot])
rot['raw_logv_logBH_r']=float(pearsonr(vr,br).statistic)
def eligible(r):return not r['author_excluded'] and not r['upper_limit_2023']
for label,rr in [('all_mass_matches',matched),('source_clean',[r for r in matched if eligible(r)]),('inclination_30_to_80',[r for r in matched if eligible(r) and r['inclination_deg'] is not None and 30<=r['inclination_deg']<=80])]:
 v=np.log10([r['vmax_km_s'] for r in rr]);m=np.array([r['logMgal'] for r in rr]);bh=np.array([r['logMBH'] for r in rr])
 xx=np.c_[np.ones(len(v)),m-11];xxb=np.c_[xx,bh-8]
 b,e=fit(xxb,v);boots=[]
 for _ in range(2000):
  ii=rng.integers(0,len(v),len(v));boots.append(fit(xxb[ii],v[ii])[0][-1])
 modern=np.array([r['logMBH_2023'] for r in rr]);xmodern=np.c_[xx,modern-8]
 record={'n':len(rr),'partial_BH_rotation_r_at_fixed_stellar_mass':partial(xx,v,bh),'BH_coefficient':float(b[-1]),'BH_coefficient_bootstrap_95pct':np.quantile(boots,[.025,.5,.975]).tolist(),'LOOCV_logv_RMSE_baseline_and_BH':[loo(xx,v),loo(xxb,v)],'updated_2023_BH_coefficient':float(fit(xmodern,v)[0][-1]),'updated_2023_BH_LOOCV':loo(xmodern,v)}
 if all(r['Re_sph_kpc'] is not None for r in rr):
  reff=np.log10([r['Re_sph_kpc'] for r in rr]);xs=np.c_[xx,reff]
  record['mass_and_size_controls']={'partial_r':partial(xs,v,bh),'LOOCV_baseline_and_BH':[loo(xs,v),loo(np.c_[xs,bh-8],v)]}
 rot['fits'][label]=record
clean=[r for r in matched if eligible(r)]
ck('upper limits excluded from primary rotation test',not any(r['upper_limit_2023'] for r in clean))
rot['exclusions']=[{'name':r['name'],'author_excluded':r['author_excluded'],'upper_limit_2023':r['upper_limit_2023']} for r in matched if not eligible(r)]
rot['additional_controls']={}
for label,fields in [('mass_size',['logMgal','Re_sph_kpc']),('mass_bulge',['logMgal','logMsph']),('mass_sigma',['logMgal','sigma_km_s']),('mass_bulge_size_sigma',['logMgal','logMsph','Re_sph_kpc','sigma_km_s'])]:
 rr=[r for r in clean if all(r[k] is not None and (r[k]>0 if k in ['Re_sph_kpc','sigma_km_s'] else True) for k in fields)]
 v=np.log10([r['vmax_km_s'] for r in rr]);bh=np.array([r['logMBH'] for r in rr])
 cov=np.array([[np.log10(r[k]) if k in ['Re_sph_kpc','sigma_km_s'] else r[k] for k in fields] for r in rr]);cov-=cov.mean(axis=0)
 xx=np.c_[np.ones(len(rr)),cov];xb=np.c_[xx,bh-8]
 slopes=[]
 for _ in range(2000):
  ii=rng.integers(0,len(rr),len(rr));slopes.append(fit(xb[ii],v[ii])[0][-1])
 xm=np.c_[np.ones(len(rr)),np.array([r['logMgal'] for r in rr])-11]
 rot['additional_controls'][label]={'n':len(rr),'partial_r':partial(xx,v,bh),'BH_coefficient':float(fit(xb,v)[0][-1]),'bootstrap_95pct':np.quantile(slopes,[.025,.5,.975]).tolist(),'LOOCV_baseline_and_BH':[loo(xx,v),loo(xb,v)],'same_sample_mass_only_LOOCV_baseline_and_BH':[loo(xm,v),loo(np.c_[xm,bh-8],v)]}
# Countermodel family: latent stellar mass drives BH and velocity, no BH->velocity arrow.
# This is an illustrative sensitivity construction, not a fitted causal explanation.
null=[]
for sm in [0,.1,.2,.3]:
 vals=[]
 for _ in range(1000):
  mt=rng.normal(0,.55,28);mobs=mt+rng.normal(0,sm,28)
  bh=2*mt+rng.normal(0,.45,28);vv=.25*mt+rng.normal(0,.04,28)
  vals.append(fit(np.c_[np.ones(28),mobs,bh],vv)[0][-1])
 null.append({'stellar_mass_error_dex':sm,'BH_coefficient_95pct':np.quantile(vals,[.025,.5,.975]).tolist()})
rot['no_BH_force_synthetic_countermodel']=null
rot['countermodel_assumptions']='28 iid objects per draw; latent mass SD=.55 dex; logBH=2m+Gaussian(.45 dex); logv=.25m+Gaussian(.04 dex); independent observed mass error scanned. Not calibrated to selection or a fit to latent data.'
rot['nonclaim']='vmax is not vflat or an acceleration at a known radius. Gas masses and full profiles absent; stellar-mass-conditioned association is not a dark-mass residual.'
res['rotation']=rot
res['virial_alternative']={'assumptions':['kT proportional to halo velocity scale squared','MBH proportional to a velocity scale to power p','stellar/halo velocity mapping needs independent validation'],'implication':'MBH proportional to T^(p/2); p=4..6 gives exponent 2..3 without introducing horizons. This is an alternative scaling construction, not a causal proof.'}
ck('finite output serialization',bool(json.dumps(res,allow_nan=False)))
(O/'results.json').write_text(json.dumps(res,indent=2,allow_nan=False)+'\n')
(O/'checks.json').write_text(json.dumps({'count':len(checks),'checks':checks},indent=2)+'\n')
print(json.dumps({k:res[k] for k in ['group_count','leave_group_out_object_weighted_RMSE','leave_group_out_equal_group_RMSE','group_bootstrap_temperature_coefficient_95pct','without_Virgo','effective_variance_diagonal','effective_variance_shared_distance']},indent=2))
print(json.dumps(rot['fits'],indent=2))

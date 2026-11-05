"""HC-007: Gaussian latent-population sensitivity for the 27 rotation matches.
Not selection-corrected. Modern BH/stellar masses share a distance convention.
python horizon_cluster_2026_11_05/rotation_latent.py OUTPUT
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
B=Path(__file__).resolve().parent;O=Path(sys.argv[1]);O.mkdir(parents=True,exist_ok=True)
prev=json.loads((B/'continuation003/results.json').read_text())['rotation']
rr=[r for r in prev['matched_rows'] if not r['author_excluded'] and not r['upper_limit_2023']]
sizes=json.loads((B/'data/galaxies.json').read_text())['rows']
def key(name):return name.replace(' ','').replace('NGC0','NGC')
lookup={key(r['name']):r for r in sizes}
rows=[]
for r in rr:
 q=lookup[key(r['name'])]
 rows.append({'name':r['name'],'m':q['logMgal'],'h':q['logMBH'],'v':np.log10(r['vmax_km_s']),
 'em':q['err_logMgal'],'eh':q['err_logMBH'],'ev':r['err_vmax']/r['vmax_km_s']/np.log(10),
 'ed':q['distance_err_Mpc']/q['distance_Mpc']/np.log(10)})
assert len(rows)==27
Y=np.array([[r[k] for k in ['m','h','v']] for r in rows]);center=Y.mean(axis=0);Y-=center
err=np.array([[r[k] for k in ['em','eh','ev']] for r in rows]);assert np.isfinite(err).all() and np.all(err>0)
checks=[]
def model(p):
 # p: mean 3; Cholesky Sxx logd1,l21,logd2; slopes mass,BH; log intrinsic scatter.
 L=np.array([[np.exp(p[3]),0],[p[4],np.exp(p[5])]])
 S=L@L.T;b=p[6:8];cov=np.zeros((3,3));cov[:2,:2]=S
 cov[:2,2]=S@b;cov[2,:2]=cov[:2,2];cov[2,2]=b@S@b+np.exp(2*p[8])
 return p[:3],cov
results={}
for label,scale,shared in [('quoted_diagonal',1,False),('quoted_shared_distance',1,True),('half_errors',.5,False),('no_errors',0,False)]:
 E=np.array([np.diag(e*e*scale**2) for e in err])
 if shared:
  dcap=np.array([min(r['ed'],r['em']/2,r['eh']) for r in rows])
  E[:,0,1]=2*dcap**2;E[:,1,0]=2*dcap**2
 assert np.linalg.eigvalsh(E).min()>=-1e-12
 def objective(p):
  mean,S=model(p);C=S[None,:,:]+E
  sign,ld=np.linalg.slogdet(C)
  if not np.all(sign>0):return 1e90
  e=Y-mean
  sol=np.linalg.solve(C,e[:,:,None])[:,:,0]
  return float(.5*np.sum(ld+np.sum(e*sol,axis=1)))
 sample=np.cov(Y[:,:2],rowvar=False,ddof=0);L=np.linalg.cholesky(sample)
 b=np.linalg.lstsq(np.c_[np.ones(len(Y)),Y[:,:2]],Y[:,2],rcond=None)[0]
 initial=np.r_[np.zeros(3),np.log(L[0,0]),L[1,0],np.log(L[1,1]),b[1:],np.log(.03)]
 bounds=[(-2,2)]*3+[(-8,2),(-5,5),(-8,2),(-2,2),(-2,2),(-10,0)]
 fits=[]
 for slope in [b[2],0,.1]:
  start=initial.copy();start[7]=slope
  fits.append(minimize(objective,start,method='L-BFGS-B',bounds=bounds,options={'maxiter':3000,'ftol':1e-12,'gtol':1e-6,'maxls':40}))
 good=[f for f in fits if f.success];assert good,label
 best=min(good,key=lambda q:q.fun)
 assert max(f.fun for f in good)-best.fun<1e-3,(label,[f.fun for f in good])
 checks.append('multi-start convergence '+label)
 # Fixed zero BH coefficient: nested fit under same latent-population model.
 def expand(z):return np.r_[z[:7],0,z[7:]]
 null=minimize(lambda z:objective(expand(z)),np.delete(best.x,7),method='L-BFGS-B',bounds=bounds[:7]+bounds[8:],options={'maxiter':3000,'ftol':1e-12,'gtol':1e-6,'maxls':40})
 assert null.success,label
 assert null.fun>=best.fun-1e-5
 checks.append('nested zero-BH likelihood '+label)
 results[label]={'mass_coefficient':float(best.x[6]),'BH_coefficient':float(best.x[7]),'intrinsic_velocity_scatter_dex':float(np.exp(best.x[8])),
  'minus_log_likelihood':float(best.fun),'twice_loglikelihood_improvement_over_zero_BH':float(2*(null.fun-best.fun)),
  'scatter_near_lower_bound':bool(best.x[8]<-9.5),'successful_starts':len(good),'successful_objective_range':float(max(f.fun for f in good)-best.fun),
  'null_BH_mass_coefficient':float(expand(null.x)[6])}
 # No formal chi-square p-value: small selected sample and possible boundary solutions.
checks.append('27 finite-error eligible galaxies')
out={'n':27,'model':'Latent bivariate Gaussian (log stellar mass, log BH mass), linear Gaussian conditional log velocity; known heteroscedastic measurement covariance. Full 3D marginal likelihood.',
 'center':center.tolist(),'rows':rows,'results':results,'checks':checks,'count':len(checks),
 'limitations':['No sample selection function','Gaussian latent population is an assumption','Quoted mass errors and their distance decomposition may not describe true systematics','No gas mass, matched radius or acceleration discrepancy','Not a causal model identification; profile intervals not computed','Modern BH mass replaces the 2019 value for a common distance convention']}
(O/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(results,indent=2))

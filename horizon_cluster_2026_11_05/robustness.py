"""HC-004: independent numerical checks, environmental confounding, SPARC feasibility.
Command: python horizon_cluster_2026_11_05/robustness.py OUTPUT_DIRECTORY
"""
import json,csv,re,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad

B=Path(__file__).resolve().parent;ROOT=B.parent;O=Path(sys.argv[1]);O.mkdir(parents=True,exist_ok=True)
G=6.67430e-11;MS=1.98847e30;KPC=3.085677581491367e19
rng=np.random.default_rng(32006);checks=[]
def ck(name,yes):
 assert yes,name
 checks.append(name)
def fit(X,y):
 b=np.linalg.lstsq(X,y,rcond=None)[0];e=y-X@b
 assert np.linalg.matrix_rank(X)==X.shape[1]
 Q,_=np.linalg.qr(X,mode='reduced');h=np.sum(Q*Q,axis=1)
 assert np.isfinite(b).all() and np.isfinite(h).all() and np.all(h<1)
 return {'n':len(y),'coefficients':b.tolist(),'loocv_rmse':float(np.sqrt(np.mean((e/(1-h))**2)))},e

# Independent adaptive integral uses Cartesian vector geometry instead of radial formulas.
flux=list(csv.DictReader((B/'run002/collective_flux.csv').open()))
for row in flux:
 if row['kernel']!='quadrature':continue
 off=float(row['offset_over_R']);y=float(row['y_boundary'])
 def integrand(mu):
  point=np.array([np.sqrt(1-mu*mu),0,mu]);vec=np.zeros(3)
  for z in [-off,off]:
   d=point-np.array([0,0,z]);vec+=.5*d/np.linalg.norm(d)**3
  return np.dot(vec,point)*np.sqrt(1+1/(y*np.linalg.norm(vec)))/2
 val,err=quad(integrand,-1,1,epsabs=1e-10,epsrel=1e-10,limit=200)
 reference=float(row['apparent_mass_ratio_to_smooth'])*np.sqrt(1+1/y)
 ck(f'adaptive vs Gauss-Legendre y={y} off={off}',abs(val-reference)<1e-8*abs(val))
 ck(f'adaptive error estimate y={y} off={off}',err<1e-8*abs(val))

gp=json.loads((B/'data/gaspari.json').read_text());hot={r['name']:r for r in gp['xray_table']}
rows=[dict(r,environment=hot[r['name']]['environment'],logTx=hot[r['name']]['logTx_g']) for r in gp['optical_table']]
def envclass(e):
 if e.startswith('BCG'):return 'cluster_central'
 if e.startswith('BGG'):return 'group_central'
 if e.startswith('BFG'):return 'field_central'
 if e=='isolated':return 'isolated'
 return 'satellite'
for r in rows:r['class']=envclass(r['environment'])
classes=['cluster_central','group_central','field_central','isolated','satellite']
X=np.array([[1,r['logSigma'],r['logLK'],r['logRe_opt_kpc']] for r in rows]);y=np.array([r['logMBH'] for r in rows]);t=np.array([r['logTx'] for r in rows])
env=np.array([[r['class']==c for c in classes[1:]] for r in rows],float)
dist=np.log10([r['distance_Mpc'] for r in rows])
Xbase=np.c_[X,dist,env];Xplus=np.c_[Xbase,t]
res={}
res['environment_counts']={c:sum(r['class']==c for r in rows) for c in classes}
res['optical_distance_environment'],ry=fit(Xbase,y)
res['optical_distance_environment_temperature'],_=fit(Xplus,y)
_,rt=fit(Xbase,t)
res['temperature_partial_r_with_distance_environment']=float(np.corrcoef(ry,rt)[0,1])
# Actual refitting after every deletion; prior run's residual-deletion range is weaker.
loo=[];pred=[]
for i in range(len(y)):
 mask=np.arange(len(y))!=i
 b=np.linalg.lstsq(Xplus[mask],y[mask],rcond=None)[0];pred.append(Xplus[i]@b)
 _,ey=fit(Xbase[mask],y[mask]);_,et=fit(Xbase[mask],t[mask])
 loo.append(np.corrcoef(ey,et)[0,1])
explicit=float(np.sqrt(np.mean((y-np.array(pred))**2)))
ck('explicit refit LOOCV equals hat-matrix formula',np.isclose(explicit,res['optical_distance_environment_temperature']['loocv_rmse'],rtol=1e-10))
res['partial_r_refit_leave_one_out_range']=[float(min(loo)),float(max(loo))]
boot=[]
for _ in range(2000):
 ix=rng.integers(0,len(y),len(y))
 if np.linalg.matrix_rank(Xplus[ix])==Xplus.shape[1]:boot.append(np.linalg.lstsq(Xplus[ix],y[ix],rcond=None)[0][-1])
res['temperature_coefficient_bootstrap_95pct']=np.quantile(boot,[.025,.5,.975]).tolist()
res['bootstrap_full_rank_draws']=len(boot)
res['subgroups']={}
for c in classes:
 mask=np.array([r['class']==c for r in rows]);xx=t[mask];yy=y[mask]
 res['subgroups'][c]=fit(np.c_[np.ones(len(xx)),xx],yy)[0]
# Deliberately remove named potentially unusual/old measurements and giant BH leverage.
for label,mask in [('without_N7331',np.array([r['name']!='N7331' for r in rows])),('without_mass_above_1e10',y<10)]:
 res[label]=fit(Xplus[mask],y[mask])[0]

# Crossmatch EVERY local SPARC filename, using declared whitespace/NGC normalization only.
sizes=json.loads((B/'data/galaxies.json').read_text())['rows']
known={r['name'].replace(' ',''):dict(r,source='Graham_Sahu_table') for r in sizes}
for r in rows:
 key='NGC'+r['name'][1:] if re.fullmatch(r'N\d+',r['name']) else r['name']
 known.setdefault(key,dict(r,source='Gaspari_table'))
files=sorted((ROOT/'real_research/data/sparc_data').glob('*_rotmod.dat'))
ck('SPARC 175 files coverage',len(files)==175)
cross=[]
for f in files:
 name=f.stem.replace('_rotmod','')
 if name not in known:continue
 q=known[name];arr=np.loadtxt(f);D=float(re.search(r'Distance = ([\d.]+)',f.read_text())[1])
 # Dynamical BH masses scale linearly with adopted distance. Diagnostic only.
 M=10**q['logMBH']*D/q['distance_Mpc']
 v2=G*M*MS/(arr[:,0]*KPC)/1e6
 ratio=v2/arr[:,1]**2
 outer=arr[:,0]>=.5*max(arr[:,0])
 excluded=bool(q.get('author_excluded',False))
 cross.append({'name':name,'source':q['source'],'source_excluded':excluded,
  'BH_Msun_rescaled_to_SPARC_distance':M,'SPARC_distance_Mpc':D,
  'radial_points':len(arr),'outer_points':int(outer.sum()),
  'BH_v2_over_observed_v2_outer_range':[float(min(ratio[outer])),float(max(ratio[outer]))],
  'status':'excluded: source flags BH mass' if excluded else 'single-object diagnostic; original BH mass method requires audit'})
ck('only two exact-name SPARC overlaps',{r['name'] for r in cross}=={'NGC5055','NGC7331'})
res['sparc_crossmatch']=cross
res['population_discrepancy_test']='Not identifiable from this overlap; do not regress two objects or count radial bins as independent galaxies.'
res['limits']=['Exploratory OLS and bootstrap, not errors-in-variables or selection-corrected inference','Environment labels are from source; correlated group membership remains','Temperature is not an independent missing-mass measurement','SPARC BH mass source validity unresolved for NGC7331; NGC5055 excluded']
(O/'robustness.json').write_text(json.dumps(res,indent=2)+'\n')
(O/'checks.json').write_text(json.dumps({'checks':checks,'count':len(checks)},indent=2)+'\n')
print(json.dumps({'checks':len(checks),'environment_counts':res['environment_counts'],'partial_r':res['temperature_partial_r_with_distance_environment'],'sparc':cross},indent=2))

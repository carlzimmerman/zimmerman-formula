import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS']: os.environ[k]='1'
import json,hashlib,time,datetime,platform,sys,subprocess
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import nnls
ROOT=Path('/Users/carlzimmerman/new_physics/zimmerman-formula')
OUT=Path('/tmp/x53_lensing_audit_20261026')
X=ROOT/'rebuild_2026_10_22/X53_outer_lensing_law_vs_halos'
D=ROOT/'real_research/data/lensing_rar/brouwer2021_rar'
files=[X/'x53_outer_lensing.py',X/'x53_diag_A1.py',X/'x53_outer_lensing_results.json',X/'x53_diag_A1_results.json',ROOT/'rebuild_2026_10_22/EM1_emergent_dust_law/em1_emergent.py',ROOT/'rebuild_2026_10_22/EM1_emergent_dust_law/em1_emergent_results.json',ROOT/'rebuild_2026_10_22/EM1_emergent_dust_law/em1_emergent_results_UPS05.json',ROOT/'rebuild_2026_10_22/X48_native_cf_zoom/x48_analyze_results_ng48.json',ROOT/'rebuild_2026_10_22/X43_collapse_core_floor/x43_collapse_core_results.json',ROOT/'rebuild_2026_10_22/F2_outer_lensing/f2_aqual.py',ROOT/'rebuild_2026_10_22/F2_outer_lensing/f2_outer_lensing.py',D/'Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt']+[D/f'Fig-3_Lensing-rotation-curves_Massbin-{b}.txt' for b in range(1,5)]+[Path(__file__)]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
hashes={str(p):sha(p) for p in files}
t0=time.time(); start=datetime.datetime.now(datetime.timezone.utc).isoformat()
j=json.loads((X/'x53_outer_lensing_results.json').read_text()); a=json.loads((X/'x53_diag_A1_results.json').read_text())
data=[np.loadtxt(D/f'Fig-3_Lensing-rotation-curves_Massbin-{b}.txt') for b in range(1,5)]
r=data[0][:,0]; y=np.array([v[:,1]/v[:,4] for v in data]); cs=np.loadtxt(files[11]); labs=sorted(set(cs[:,0])); C=np.zeros((60,60))
for row in cs:
 b,c=labs.index(row[0]),labs.index(row[1]);i,k=np.abs(r-row[2]).argmin(),np.abs(r-row[3]).argmin();C[15*b+i,15*c+k]=row[4]/row[6]
f=(.679/.70)*1.0128;C*=f*f;y*=f
res={'covariance_symmetry_max':float(np.max(np.abs(C-C.T))),'covariance_min_eigenvalue':float(np.linalg.eigvalsh(C).min()),'footings':{}}
for foot,z in j['footings'].items():
 p=z['profiles']; z2={};T=(np.array(p['H2H'])-np.array(p['H']))/np.array(z['all']['H2H']['b'])[:,None]
 for label,idx in [('primary',np.flatnonzero(r<=.31)),('all',np.arange(15))]:
  sel=np.concatenate([15*b+idx for b in range(4)]); Csel=C[np.ix_(sel,sel)];L=np.linalg.cholesky(Csel);scores={};errors={}
  A=np.zeros((60,4))
  for b in range(4): A[15*b:15*b+15,b]=T[b]
  Aw=np.linalg.solve(L,A[sel])
  for model in ['L','H']:
   residual=(y-np.array(p[model])).ravel()[sel];rw=np.linalg.solve(L,residual);scores[model]=float(rw@rw)
   coef,_=nnls(Aw,rw);q=rw-Aw@coef;scores[model+'2H']=float(q@q)
  errors={k:abs(v-z[label][k]['chi2']) for k,v in scores.items()};z2[label]={'independent_chi2':scores,'max_abs_error':max(errors.values())}
 base=z['all']['dchi2_H2H_minus_L2H'];tr=a['footings'][foot]['truncated']['all'];un=a['footings'][foot]['untruncated(100 R200)']['all']
 z2['all_radius_decomposition']={'initial_delta':base,'fraction_gap_removed_by_one_mass_shift':1-tr['dchi2_common_vs_L2H']/base,'edge_improvement_after_common_mass_fit':tr['chi2_common']-un['chi2_common'],'remaining_delta_extended':un['dchi2_common_vs_L2H']}
 i=7 # 0.311 Mpc native radius
 radi=float(p['R'][1][i]);ds=float(p['data'][1][i]);h=float(p['H'][1][i]);newt=float(p['Newt'][1][i]);
 z2['bin2_Rindex7']={'R_Mpc':radi,'data_DS':ds,'H_DS':h,'data_to_H':ds/h,'minimum_cyl_total_mass_solar':np.pi*(radi*1e6)**2*ds,'point_mass_equivalent_deficit_solar':np.pi*(radi*1e6)**2*(ds-h)}
 assert max(v['max_abs_error'] for k,v in z2.items() if k in ['primary','all'])<1e-8
 assert np.max(np.abs(y-np.array(p['data'])))<1e-12
 res['footings'][foot]=z2
res['status']='completed';out=OUT/'result.json';out.write_text(json.dumps(res,indent=2))
manifest={'schema_version':2,'claim_id':'X53_INDEPENDENT_STATISTIC_AUDIT','repository':{'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'dirty':bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True))},'command':['python3',str(Path(__file__))],'environment':{'software':[{'name':'Python','version':platform.python_version()},{'name':'NumPy','version':np.__version__},{'name':'SciPy','version':scipy.__version__}],'hardware':platform.platform()},'mathematics':{'assertion_tested':'Reconstruct X53 chi-square and nonnegative two-halo fits from released covariance and saved model predictions, independently of production scoring code. Quantify reported mass/edge decomposition.','coefficient_domain':'IEEE754 double','conventions':'B21 K-corrected covariance; native factor (0.679/0.70)*1.0128; four bins; nonnegative per-bin amplitudes','inputs':['Four 15-point profiles and 60x60 covariance','Saved X53 predictions and A1 reported chi-square values'],'bounds':{'n_bins':4,'n_radii':15,'fit_ranges':['R_B21<=0.31 Mpc','all']} ,'non_claims':['Does not rerun or independently validate halo construction, catalogue weighting, or the astrophysical model.','Template inferred from saved H2H predictions; not an independent construction.','Mass normalization and boundary components are conditional diagnostics, not unique causal decomposition.']},'randomness':{'used':False,'generator':'','seed':None},'run':{'started_at':start,'runtime_seconds':time.time()-t0,'exit_status':0,'status':'completed','resource_limits':{'memory_bytes':None,'cpu_seconds':None,'max_cores':None,'max_threads':1}},'outputs':[{'path':str(out.resolve()).lstrip('/'),'sha256':sha(out),'kind':'result'}],'checks':[{'name':'independent_chi_square','passed':True},{'name':'native_data_values','passed':True}],'result':'Finite scoring assertion verified to 1e-8 absolute chi-square. No complete production rerun.','residual_risks':['Live repository; inputs hashed before and after','Outside bounded runner; no explicit hard resource limits'],'input_artifacts':[{'path':str(p.resolve()).lstrip('/'),'sha256':hashes[str(p)],'sha256_after':sha(p)} for p in files],'declared_results':[str(out.resolve()).lstrip('/')]}
assert all(v['sha256']==v['sha256_after'] for v in manifest['input_artifacts'])
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(res,indent=2)); print('MANIFEST',OUT/'manifest.json')

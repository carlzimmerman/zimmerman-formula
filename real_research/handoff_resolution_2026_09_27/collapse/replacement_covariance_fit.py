#!/usr/bin/env python3
"""New full-covariance nuisance fit; same mass bounds and supplied Moster endpoints.
Piecewise-linear interpolation of original mass-grid profiles, with multi-start bounded least squares.
MUTATE deliberately drops covariance cross terms; full-covariance identity control must fail.
"""
import os,sys,pathlib,json,math,time
sys.dont_write_bytecode=True
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import numpy as np
from scipy.optimize import least_squares
from scipy.linalg import cholesky
HERE=pathlib.Path(__file__).resolve().parent;REPO=HERE.parents[2];sys.path.insert(0,str(REPO/'campaign_fresh_gravity'))
import CFG4_common as C
from scipy import __version__ as scipyversion
start=time.monotonic();MUT=os.environ.get('MUTATE')=='1';out={'mutate':MUT,'checks':{},'rows':[],'runtime':{'python':sys.version,'numpy':np.__version__,'scipy':scipyversion},'assumptions':['same Mb=10^9.8--10^11.8 Msun bounds and inherited twohalo template','full covariance fixed to supplied KiDS table','linear interpolation of original .05dex mass-grid profiles','no prior beyond declared bounds; Moster endpoints not fitted','deterministic multistart finds candidate minima, not proof of global optimum']}
def ck(n,b,v):out['checks'][n]={'ok':bool(b),'value':v};print(n,b,v,flush=True)
GK={'np':np,'math':math,'os':os,'REPO':str(REPO),'G_SI':C.G_SI,'_trap':C._trap}
GK,_=C.exec_slices(str(REPO/'real_research/derivation_chain_2026/FP1_static_sector.py'),[("# ---- KiDS: L355's machinery",'w0 = np.zeros(len(ES)); w0[0] = 1.0')],ns=GK)
s=(REPO/'campaign_fresh_gravity/CFG3_common.py').read_text();ns={'np':np};exec(s[s.index('def mstar_of_mh('):],ns);mh=ns['mh_of_mstar']
rr=GK['rrK'];LM=GK['LM'];MS=GK['MS'];FIX=C.ESDFix(rr,GK['Rp'],GK['PCm2'],MS);nb=GK['npb'];D=np.concatenate(GK['Ed']);Ci=GK['Ci'];U=cholesky(np.diag(np.diag(Ci)) if MUT else Ci,lower=False)
probe=np.linspace(-2,3,len(D));true=float(probe@Ci@probe);got=float(np.sum((U@probe)**2));ck('full_covariance_whitening',abs(got/true-1)<1e-12,{'ratio':got/true,'eigen_min':float(np.linalg.eigvalsh(Ci).min())})
Acol=np.zeros((len(D),4))
for b in range(4):Acol[b*nb:(b+1)*nb,b]=GK['T2H'][b]
rng=np.random.default_rng(20260927)
for foot,a0 in C.A0.items():
 baseline=None
 for fac in [1.,1.4,2.]:
  raw=json.loads((HERE/('replacement_joint_results'+('_FAC'+str(fac) if fac!=1.4 else '')+'.json')).read_text())['kids'][foot]['scores']
  for model in ['P2','cap']:
   if model=='P2' and baseline is not None:continue
   grid=np.zeros((4,len(LM),nb))
   for im,lm in enumerate(LM):
    mb=10**lm*MS;ph=mb*(C.nu_p2(C.G_SI*mb/rr**2/a0)-1)
    if model=='cap':ph=np.minimum(ph,float(mh(10**lm/fac,.25))*MS-mb)
    ds=FIX(mb+ph,mb)
    for b in range(4):grid[b,im]=np.interp(GK['Rd'][b],GK['Rp']/GK['MPCm'],ds)
   w=np.zeros(len(GK['ES']));w[0]=1;T=np.zeros((len(w),len(LM),4,nb));T[0]=grid.transpose(1,0,2)
   oldval=GK['kfit']({foot:T},foot,w,2.)[0];ck(f'inherited_reproduction/{foot}/{fac}/{model}',abs(oldval-raw[model]['2.0']['chi2'])<1e-9,oldval)
   for mode in ['zero','fixed1','free2']:
    free=mode=='free2';amp=np.zeros(4) if mode=='zero' else np.ones(4)
    def model_jac(x):
     pred=np.empty(len(D));jac=np.zeros((len(D),8 if free else 4))
     for b in range(4):
      i=min(max(int(np.searchsorted(LM,x[b],side='right')-1),0),len(LM)-2);t=(x[b]-LM[i])/(LM[i+1]-LM[i]);sl=slice(b*nb,(b+1)*nb)
      pred[sl]=(1-t)*grid[b,i]+t*grid[b,i+1];jac[sl,b]=(grid[b,i+1]-grid[b,i])/(LM[i+1]-LM[i])
     pred+=Acol@(x[4:] if free else amp)
     if free:jac[:,4:]=Acol
     return pred,jac
    fun=lambda x:U@(model_jac(x)[0]-D)
    jac=lambda x:U@model_jac(x)[1]
    lo=np.r_[np.full(4,LM[0]),np.zeros(4)] if free else np.full(4,LM[0]);hi=np.r_[np.full(4,LM[-1]),np.full(4,2.)] if free else np.full(4,LM[-1])
    prior=raw[model]['2.0' if free else '0.0'];mseed=np.array([x['logMb'] for x in prior['selected_mass_edge']]);aseed=np.array(raw[model]['2.0']['profiled_A'])
    starts=[np.r_[mseed,aseed] if free else mseed,np.r_[mseed,np.ones(4)] if free else np.full(4,10.8)]
    if free:
     fixedrow=next(r for r in reversed(out['rows']) if r['foot']==foot and r['model']==model and r['mode']=='fixed1' and r['fac']==(fac if model=='cap' else None))
     starts.append(np.r_[fixedrow['logMb'],np.ones(4)])
    starts += [rng.uniform(lo,hi) for _ in range(198)]
    trials=[]
    for x in starts:
     sol=least_squares(fun,np.clip(x,lo,hi),jac=jac,bounds=(lo,hi),ftol=1e-11,xtol=1e-11,gtol=1e-9,max_nfev=1500)
     trials.append({'chi2':float(np.sum(sol.fun**2)),'x':sol.x.tolist(),'success':bool(sol.success),'optimality':float(sol.optimality),'nfev':int(sol.nfev)})
    best=min(trials,key=lambda t:t['chi2']);x=np.array(best['x']);pred,_=model_jac(x);actual=float((pred-D)@Ci@(pred-D))
    ck(f'score_identity/{foot}/{fac}/{model}/{mode}',abs(actual-best['chi2'])<1e-8,actual-best['chi2'])
    # Compare an actual stored admissible point, including fixed A=1 inside free A bounds.
    inherited=raw[model]['2.0' if free else ('fixed1' if mode=='fixed1' else '0.0')]['chi2']
    ck(f'no_worse_than_inherited/{foot}/{fac}/{model}/{mode}',best['chi2']<=inherited+1e-7,{'new':best['chi2'],'inherited':inherited})
    row={'foot':foot,'fac':fac if model=='cap' else None,'model':model,'mode':mode,'chi2':best['chi2'],'actual_full_chi2':actual,'logMb':best['x'][:4],'A':best['x'][4:] if free else amp.tolist(),'trials':trials,'n_trials_within_1e-5':sum(abs(t['chi2']-best['chi2'])<1e-5 for t in trials)};out['rows'].append(row)
    print('RESULT', {k:v for k,v in row.items() if k!='trials'},flush=True)
   if model=='P2':baseline=True
   (HERE/('replacement_covariance_partial'+('_MUTATE' if MUT else '')+'.json')).write_text(json.dumps(out,indent=2))
for row in out['rows']:
 if row['model']=='cap':
  base=next(r['chi2'] for r in out['rows'] if r['foot']==row['foot'] and r['model']=='P2' and r['mode']==row['mode']);base0=next(r['chi2'] for r in out['rows'] if r['foot']==row['foot'] and r['model']=='P2' and r['mode']=='zero')
  row.update(delta_chi2_same_nuisance=row['chi2']-base,delta_chi2_baseline_no2halo=row['chi2']-base0,within9_same_nuisance=row['chi2']-base<=9,within9_baseline_no2halo=row['chi2']-base0<=9)
out['runtime_s']=time.monotonic()-start;out['controls_pass']=all(v['ok'] for v in out['checks'].values());(HERE/('replacement_covariance_results'+('_MUTATE' if MUT else '')+'.json')).write_text(json.dumps(out,indent=2));print('DONE',out['runtime_s']);sys.exit(0 if out['controls_pass'] else 1)

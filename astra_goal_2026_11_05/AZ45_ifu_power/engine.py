"""AZ45 declared synthetic population; no cosmological/SED setup calls."""
import hashlib,itertools,json,math,os,sys
from pathlib import Path
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FN3=ROOT/'finish_2026_11_04/FN3_musedark_law_refit'
sys.path.insert(0,str(FN3))
import fn3_common as C
import fn3_cube as F
FOOTS={'canonical':9.3603e-11,'alt':1.1312e-10}
TEMPLATES=[dict(id=i,z=z,logM=lm,inc=inc) for i,(z,lm,inc) in enumerate(itertools.product([.6,1.,1.4],[9.5,10.5],[35.,65.]))]
def hashes():
    files=[HERE/'FROZEN_CRITERIA.md',Path(__file__),FN3/'fn3_common.py',FN3/'fn3_cube.py']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
def atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:json.dump(obj,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def setup(tid,rung):
    t=TEMPLATES[tid];z=t['z'];lm=t['logM']
    lam=.5*(F.L1+F.L2)*(1+z)+(np.arange(25)-12)*1.25
    cm=F.CubeModel(25,25,lam,.2,5.,.6,2.8,os=3 if rung==1 else 4,ngh=8 if rung==1 else 12)
    cm.Rgrid=np.geomspace(.01,80.,300 if rung==1 else 600)
    geo=dict(x0=12.,y0=12.,lc=(F.L1*(1+z)-lam[0])/1.25,flux=1000.,rhalf=.4,n=1.,inc=t['inc'],pa=30.,rline=.7,sig0=25.)
    return t,cm,geo,.3*10**lm
def bounds(g,lm,fixed):
    lo=[g['x0']-2,g['y0']-2,g['lc']-2,g['flux']*.3,g['rhalf']*.5,.5,max(g['inc']-5,10),g['pa']-30,.3,0.,lm-1.5,0.]
    hi=[g['x0']+2,g['y0']+2,g['lc']+2,g['flux']*3,g['rhalf']*2,4.,min(g['inc']+5,85),g['pa']+30,1.5,120.,lm+1.5,15.]
    return np.array(lo[:11] if fixed else lo),np.array(hi[:11] if fixed else hi)
def starts(g,lm,fixed):
    first=np.array([g[k] for k in F.GEO]+[g['sig0'],lm]+([] if fixed else [6.]))
    second=first.copy();second[:3]+=[.2,-.2,.2];second[3]*=.9;second[4]*=1.1
    second[5:11]=[1.1,g['inc']+2,g['pa']+3,.8,30.,lm+.2]
    if not fixed:second[11]=8.
    return [first,second]
def random_draw(tid,rep):
    rng=np.random.default_rng(np.random.SeedSequence([20261105,45,tid,rep]))
    while True:
        gas=6*10**rng.normal(0,.15)
        if 0<gas<15:break
    return gas,rng.normal(size=(25,25,25))
def truth(tid,rung,foot,rep,scenario,noiseless=False):
    t,cm,g,mh2=setup(tid,rung)
    gas,noise=random_draw(tid,rep)
    if noiseless:gas=6.
    delta=0. if scenario=='flat' else .60*(t['z']-1)
    theta=np.array([g[k] for k in F.GEO]+[g['sig0'],t['logM']+delta,gas])
    gen=F.Fitter(cm,None,np.ones((25,25,25)),F.LawMass(mh2,FOOTS[foot]),'law')
    model=gen.model(theta)
    return t,cm,g,mh2,delta,gas,noise,model

class YieldRequested(Exception):pass
class StoppableFitter(F.Fitter):
    stop=lambda self:False
    def resid(self,th):
        if self.stop():raise YieldRequested()
        return super().resid(th)

def fit_case(tid,rung,foot,rep,scenario,snr,hi,mode='main',step=.01,stop=lambda:False):
    noiseless=mode in ['reference','double','plus','minus']
    t,cm,g,mh2,delta,gas,noise,model=truth(tid,rung,foot,rep,scenario,noiseless)
    sigma=float(np.linalg.norm(model))/snr
    data=model if noiseless else model+sigma*noise
    factor={'main':1.,'mutate':2.,'reference':1.,'double':2.,'plus':10**step,'minus':10**(-step)}[mode]
    fixed=hi=='fixed';lo,up=bounds(g,t['logM'],fixed)
    fitter=StoppableFitter(cm,data,np.full(model.shape,sigma*sigma),F.LawMass(mh2,FOOTS[foot]*factor),'law',sighi_fixed=6. if fixed else None)
    fitter.stop=stop;fits=[]
    for start in starts(g,t['logM'],fixed):
        fit=fitter.fit(start,lo,up,max_nfev=400)
        fits.append(dict(parameters=fit['x'].tolist(),errors=fit['err'].tolist(),chi2=fit['chi2'],dof=fit['dof'],
                         chi2_red=fit['chi2_red'],nfev=fit['nfev'],status=int(fit['status'])))
    finite=[f for f in fits if np.isfinite(f['chi2']) and np.all(np.isfinite(f['parameters']))]
    if not finite:raise RuntimeError('No finite fit')
    best=min(finite,key=lambda f:f['chi2'])
    spread=abs(fits[0]['parameters'][10]-fits[1]['parameters'][10])
    resolved=len(finite)==2 and all(f['status']>0 for f in finite) and spread<=.05
    par=np.array(best['parameters']);edge=np.minimum((par-lo)/(up-lo),(up-par)/(up-lo))
    # A nonfinite covariance is a diagnostic rather than invalid JSON.
    for f in fits:f['errors']=[float(x) if np.isfinite(x) else None for x in f['errors']]
    return dict(template=t,rung=rung,footing=foot,replicate=rep,scenario=scenario,snr=snr,hi_case=hi,mode=mode,step=step,
                true_delta=delta,true_gas=gas,sigma=sigma,a0_factor=factor,delta=best['parameters'][10]-t['logM'],
                resolved=bool(resolved),start_delta_spread=spread,boundary_names=[fitter.names()[i] for i in np.flatnonzero(edge<=1e-4)],
                best_start=fits.index(best),fits=fits,scope='kappa = 1/2 FITTED; not theory closed')

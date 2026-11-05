"""Frozen covariance-aware G3 diagnostics; no search/adoption logic."""
import hashlib,json,math,os,sys
from pathlib import Path
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[k]='1'
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];BK=ROOT/'rebuild_2026_10_22/BK2_dimensional_law_search'
sys.path.insert(0,str(BK));import bk2_lib as B
SCATTER_HASH='07ab94b63fa6e9cb030c4c6408aa6ce5b2e48f548b08ec13b0dbf7e917e83adb'
if hashlib.sha256((HERE/'scatter.json').read_bytes()).hexdigest()!=SCATTER_HASH:raise RuntimeError('Frozen scatter changed')
SCATTER=json.loads((HERE/'scatter.json').read_text())
CINT=np.array(SCATTER['intrinsic_psd_covariance']);LOO=[np.array(r['intrinsic_psd_covariance']) for r in SCATTER['leave_one_out']]
FOOTS={'canonical':9.3603e-11,'alt':1.1312e-10}
def dataset(foot,mode,old=False):
    T=B.xcop(B.A0S[foot] if old else FOOTS[foot],0)
    if mode=='control':
        p=np.random.default_rng(20261102).permutation(len(T['gb']));frac=(T['gg']/T['gb'])[p]
        T['gg']=frac*T['gb'];T['gs']=T['gb']-T['gg']
        for k in ['r','Sig','rho','Phi']:T[k]=T[k][p]
    return T
def legacy(d,T,extra=None):
    m=float(np.mean(d));rm=float(np.sqrt(np.mean(d*d)));groups=np.unique(T['gid'])
    cm=np.array([np.mean(d[T['gid']==g]) for g in groups]);Zm=m/math.hypot(float(cm.std(ddof=1))/math.sqrt(len(groups)),.12)
    var=T['se']**2+T['sm']**2
    if extra is not None:var=var+np.tile(np.diag(extra),len(groups))
    Q=float(np.sum((d-m)**2/var));df=len(d)-1;Z=(Q-df)/math.sqrt(2*df)
    return dict(mean=m,rms=rm,Zm=Zm,Zs=Z,Q=Q,line=abs(m)<=.05 and rm<=.10,err=abs(Zm)<=2 and Z<=2)
class Shape:
    def __init__(self,T,C):
        groups=np.unique(T['gid']);n=len(T['gid']);self.V=np.zeros((n,n));self.W=np.zeros((n,n))
        for g in groups:
            ix=np.flatnonzero(T['gid']==g)
            if len(ix)!=5:raise RuntimeError('Incomplete cluster block')
            V=np.diag(T['se'][ix]**2+T['sm'][ix]**2)+C
            self.V[np.ix_(ix,ix)]=V;self.W[np.ix_(ix,ix)]=np.linalg.inv(V)
        self.one=np.ones(n);self.weights=self.W@self.one;self.den=float(self.one@self.weights);self.df=n-1
    def score(self,d):
        mu=float(self.weights@d/self.den);r=d-mu;Q=float(r@self.W@r)
        return dict(GLS_intercept=mu,Q=Q,Z_cov=(Q-self.df)/math.sqrt(2*self.df))
def evaluate(formula,T,mutate=False):
    v=B.ev(formula,T)
    if not np.all(np.isfinite(v)&(v>0)):return dict(valid=False)
    d=np.log10(T['go']/v);old=legacy(d,T);C=np.zeros_like(CINT) if mutate else CINT
    diag=legacy(d,T,C);full=Shape(T,C).score(d);flag=abs(old['Zm'])<=2 and full['Z_cov']<=2
    leave=[]
    for cov in ([np.zeros_like(CINT)]*len(LOO) if mutate else LOO):
        r=Shape(T,cov).score(d);r['conditional_err']=abs(old['Zm'])<=2 and r['Z_cov']<=2;leave.append(r)
    return dict(valid=True,legacy=old,diagonal=diag,covariance=full,conditional_err=flag,
                stable=all(r['conditional_err']==flag for r in leave),leave_one_out=leave)
def atomic(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:json.dump(obj,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

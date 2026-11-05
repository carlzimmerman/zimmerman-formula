#!/usr/bin/env python3
"""Cluster-level empirical scatter; no candidate formula regrade."""
import hashlib,json,os,platform,resource,sys,time
from pathlib import Path
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[k]='1'
import numpy as np
import mpmath as mp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
BK=ROOT/'rebuild_2026_10_22/BK2_dimensional_law_search'
sys.path.insert(0,str(BK));import bk2_lib as B
np.seterr(all='warn')
start=time.time();checks=[]
def check(name,passed,value):checks.append(dict(name=name,passed=bool(passed),value=value))
def cov(a):
    d=a-a.mean(axis=0);return d.T@d/(len(a)-1)
def psd(a):
    e,v=np.linalg.eigh(a);return (v*np.maximum(e,0))@v.T,e
fixture=np.array([[1,0],[-1,0],[0,2],[0,-2]],float)
check('symmetric_diagonal_fixture',np.max(abs(cov(fixture)-np.diag([2/3,8/3])))<1e-12,cov(fixture).tolist())
offset=np.arange(4.)[:,None]*np.ones((1,5))
check('rank_one_offset_fixture',np.linalg.matrix_rank(cov(offset),tol=1e-12)==1,cov(offset).tolist())
check('common_radial_trend_invariance',np.max(abs(cov(offset+np.arange(5.)**2)-cov(offset)))<1e-12,None)
check('cluster_order_invariance',np.max(abs(cov(fixture[::-1])-cov(fixture)))<1e-12,None)
P=np.eye(5)-np.ones((5,5))/5
check('centering_annihilates_constant',np.max(abs(P@np.ones(5)))<1e-12,None)
pos=np.array([[2.,.3],[.3,1.]])
check('PSD_positive_fixture',np.max(abs(psd(pos)[0]-pos))<1e-12,None)
check('PSD_negative_eigenvalue_fixture',np.max(abs(psd(np.diag([-1.,2.]))[0]-np.diag([0.,2.])))<1e-12,None)
rows=B.xcop_raw();names=sorted(set(r['name'] for r in rows));xs=[.1,.2,.3,.5,.7]
clusters=[]
for name in names:
    rr=sorted((r for r in rows if r['name']==name),key=lambda r:r['x'])
    if [r['x'] for r in rr]!=xs:
        clusters.append(dict(name=name,j=rr[0]['j'],complete=False,available_x=[r['x'] for r in rr]));continue
    y=[float(np.log10(r['go']/(r['gs']+r['gg']))) for r in rr]
    clusters.append(dict(name=name,j=rr[0]['j'],complete=True,y=y,se=[r['se'] for r in rr],sm=[r['sm'] for r in rr]))
train=[r for r in clusters if r['j']%2==0 and r['complete']]
missing=[r['name'] for r in clusters if not r['complete']]
Y=np.array([r['y'] for r in train]);D=np.array([np.array(r['se'])**2+np.array(r['sm'])**2 for r in train])
S=cov(Y);meanD=np.diag(D.mean(axis=0));intrinsic,eig=psd(S-meanD)
outer=sum(np.outer(y,y) for y in Y)-len(Y)*np.outer(Y.mean(0),Y.mean(0));outer/=len(Y)-1
check('direct_vs_outer_products',np.max(abs(S-outer))<=1e-12,float(np.max(abs(S-outer))))
mpcov=[]
for precision in [40,80]:
    with mp.workdps(precision):
        yy=[[mp.mpf(str(x)) for x in row] for row in Y];means=[sum(r[j] for r in yy)/len(yy) for j in range(5)]
        cc=[[sum((r[i]-means[i])*(r[j]-means[j]) for r in yy)/(len(yy)-1) for j in range(5)] for i in range(5)]
        mpcov.append(np.array([[float(v) for v in r] for r in cc]))
check('40_80_digit_pair',np.max(abs(mpcov[0]-mpcov[1]))<=1e-12,float(np.max(abs(mpcov[0]-mpcov[1]))))
check('float_vs_80_digit',np.max(abs(S-mpcov[1]))<=1e-12,float(np.max(abs(S-mpcov[1]))))
leave=[]
for i,row in enumerate(train):
    keep=np.arange(len(Y))!=i;s=cov(Y[keep]);v,e=psd(s-np.diag(D[keep].mean(0)))
    leave.append(dict(omitted=row['name'],empirical_covariance=s.tolist(),empirical_sigma=np.sqrt(np.diag(s)).tolist(),
                      intrinsic_psd_covariance=v.tolist(),intrinsic_sigma=np.sqrt(np.maximum(np.diag(v),0)).tolist()))
sig=np.sqrt(np.diag(S));corr=S/np.outer(sig,sig)
inputs=[HERE/'MEASUREMENT_PROTOCOL.md',Path(__file__),BK/'bk2_lib.py']
for name in names:
    inputs+=list((ROOT/'real_research/data/xcop'/name).glob(name+'*.fits'))
sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
out=dict(status='Scatter measured before candidate regrade; not a physical-law verdict',radii=xs,clusters=clusters,train_names=[r['name'] for r in train],
         holdout_names=[r['name'] for r in clusters if r['j']%2==1],missing_coverage=missing,n_train=len(Y),
         mean_radial_log_mass_ratio=Y.mean(0).tolist(),empirical_covariance=S.tolist(),empirical_sigma=sig.tolist(),empirical_correlation=corr.tolist(),
         empirical_rank=int(np.linalg.matrix_rank(S,tol=1e-12)),measurement_diagonal_mean=np.diag(meanD).tolist(),
         intrinsic_unclipped_eigenvalues=eig.tolist(),intrinsic_psd_covariance=intrinsic.tolist(),intrinsic_sigma=np.sqrt(np.maximum(np.diag(intrinsic),0)).tolist(),
         PSD_clipping_frobenius=float(np.linalg.norm(intrinsic-(S-meanD))),leave_one_out=leave,checks=checks,
         source_hashes=sources,versions=dict(python=platform.python_version(),numpy=np.__version__,mpmath=mp.__version__),
         footing_scope='Mass-ratio scatter is independent of a0; later formula regrade must separate both footings',
         limitations=['Unknown within-cluster measurement covariance','Small train-cluster sample','PSD clipping is an estimation assumption','No candidate graded'],
         scope='kappa = 1/2 FITTED; not theory closed')
(HERE/'scatter.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
(HERE/'scatter_runtime.json').write_text(json.dumps(dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['n_train','train_names','holdout_names','missing_coverage','empirical_sigma','empirical_rank','intrinsic_sigma','intrinsic_unclipped_eigenvalues','checks']},indent=2))
raise SystemExit(int(not all(c['passed'] for c in checks)))

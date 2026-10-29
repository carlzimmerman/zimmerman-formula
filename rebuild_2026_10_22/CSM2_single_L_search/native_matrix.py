import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'): os.environ[k]='1'
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];REB=HERE.parent
sys.path.insert(0,str(HERE))
from projection_operator import operator
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
data=ROOT/'real_research/data/lensing_rar';b21=data/'brouwer2021_rar'
files=[Path(__file__),HERE/'NATIVE_MATRIX_CRITERIA.md',HERE/'projection_operator.py',REB/'F2_outer_lensing/f2_outer_lensing.py',REB/'F2_outer_lensing/f2_aqual.py',REB/'CSM1_consistent_core_switch/calibration/run_003_audited/results.json',data/'lr_lenses.npz',data/'cfg110_perlens.npz',b21/'Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt',*[b21/f'Fig-3_Lensing-rotation-curves_Massbin-{b}.txt' for b in range(1,5)]]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={str(p.relative_to(ROOT)):sha(p) for p in files}
files.append(REB/'CSM1_consistent_core_switch/calibration/run_004_replay/results.json');hashes={str(p.relative_to(ROOT)):sha(p) for p in files}
checks={};finite=[]
def arr(x):
 x=np.asarray(x,dtype=float);assert np.all(np.isfinite(x));finite.append(x.size);return x
def ck(k,v): checks[k]=bool(v)
def chi(z,C):return float(z@np.linalg.solve(C,z))
def ch(z,om):
 zz=np.linspace(0,1,4001);e=np.sqrt(om*(1+zz)**3+1-om);return np.interp(z,zz,np.r_[0,np.cumsum(.5*(1/e[1:]+1/e[:-1])*np.diff(zz))])
raw=[np.loadtxt(b21/f'Fig-3_Lensing-rotation-curves_Massbin-{b}.txt') for b in range(1,5)]
R=arr([d[:,0] for d in raw]);Y=arr([d[:,1]/d[:,4] for d in raw]);c=np.loadtxt(files[8]);mins=sorted(set(c[:,0]));C=np.zeros((60,60))
for row in c:
 m,n=mins.index(row[0]),mins.index(row[1]);i,j=[int(np.argmin(abs(R[0]-r))) for r in row[2:4]];C[m*15+i,n*15+j]=row[4]/row[6]
h=.679;f=(h/.70)*1.0128;Cn=arr(C*f*f);W=arr(np.linalg.solve(np.linalg.cholesky(Cn),np.eye(60)))
ln=np.load(data/'lr_lenses.npz');pl=np.load(data/'cfg110_perlens.npz');lm=arr(ln['logM']);z=arr(ln['z']);w=arr(pl['WW'].sum(axis=1));bins=np.digitize(lm,[8.5,10.3,10.6,10.8,11.0001])-1
q=arr(ch(z,.3085)/ch(z,.3));grid=np.round(np.arange(6.8,11.81,.02),2);weights=[];Rn=[];inventory=[]
for b in range(4):
 s=bins==b;ww=w[s];x=arr(lm[s]+2*np.log10(.70/h)+2*np.log10(q[s]));ids=np.clip(np.searchsorted(grid,x,side='right')-1,0,len(grid)-2);t=np.clip((x-grid[ids])/(grid[ids+1]-grid[ids]),0,1);wt=np.zeros(len(grid));np.add.at(wt,ids,ww*(1-t)/ww.sum());np.add.at(wt,ids+1,ww*t/ww.sum());weights.append(arr(wt));zeff=float(ww@z[s]/ww.sum());Rn.append(R[b]*(.70/h)*ch(zeff,.3085)/ch(zeff,.2793));v=np.sin(grid)
 ck(f'weights_{b}',np.all(ww>=0) and np.all(wt>=0) and abs(wt.sum()-1)<1e-12 and abs(wt@v-np.interp(x,grid,v)@ww/ww.sum())<1e-12)
 inventory.append(dict(bin=b,n=int(s.sum()),positive_nodes=int((wt>0).sum()),zeff=zeff))
Rn=arr(Rn);weights=arr(weights);saved=json.loads(files[5].read_text())['levels'];saved.update(json.loads((REB/'CSM1_consistent_core_switch/calibration/run_004_replay/results.json').read_text())['levels']);saved={str(float(k)):v for k,v in saved.items()};records=[]
base=saved['3.75']['lens']['result'];T2=arr(base['_computed_T2'])*f;T=np.zeros((60,4))
for b in range(4):T[b*15:(b+1)*15,b]=T2[b]
A=arr(W@T);Q,rr=np.linalg.qr(A);P=arr(np.eye(60)-Q@Q.T);B=arr(P@W)
ck('projector',np.linalg.matrix_rank(A)==4 and np.max(abs(P-P.T))<1e-9 and np.max(abs(P@P-P))<1e-9 and np.max(abs(P@A))<1e-9)
mutation=[]
for level in ('3.75','3.9','4.0'):
 for foot in ('canonical','alt'):
  obj=saved[level]['lens']['result'][foot];prof=obj['profiles'];y=arr(prof['data']).ravel();m=arr(prof['H']).ravel();sig=arr(prof['sigma']).ravel()
  ck(f'native_{level}_{foot}',np.max(abs(arr(prof['R'])-Rn))<1e-10 and np.max(abs(y-(Y*f).ravel()))<1e-10 and np.max(abs(sig-np.sqrt(np.diag(Cn))))<1e-10)
  scores={}
  for key in ('H2H','L2H'):
   residual=y-arr(prof[key]).ravel();score=chi(residual,Cn);expected=obj['all'][key]['chi2'];scores[key]=score
   ck(f'score_{level}_{foot}_{key}',abs(score-expected)<1e-6);mutation.append(abs(chi(residual,Cn*1.01)-expected)>1e-6)
  r=arr(W@(y-m));bfit=arr(np.linalg.lstsq(A,r,rcond=None)[0]);free=float(np.sum(arr(B@(y-m))**2));ind=float(np.sum(arr(r-A@bfit)**2))
  ck(f'free_{level}_{foot}',abs(free-ind)<=1e-9*max(1,free) and free<=scores['H2H']+1e-6)
  records.append(dict(L=level,foot=foot,constrained=scores['H2H'],law=scores['L2H'],free=free,least_squares=ind,unrestricted_amplitudes=bfit.tolist()))
ns=dict(__name__='readonly',__file__=str(files[4]));exec(compile(files[4].read_text(),str(files[4]),'exec'),ns);rg=np.logspace(1,10,3601);errors=[]
for b in range(4):
 for tail in ('const','linear'):
  M=arr(operator(Rn[b]*1e6,rg,ns['TT'],tail))
  for mass in (np.ones_like(rg),rg,rg**2/(rg+1e5)):
   expected=arr(ns['delta_sigma'](Rn[b]*1e6,rg,mass,tail));got=arr(M@mass);errors.append(float(np.max(abs(got-expected))/max(np.max(abs(expected)),1e-300)))
ck('native_operator',np.all(np.isfinite(errors)) and len(errors)==24 and max(errors)<1e-10);ck('mutation_detected',all(mutation));ck('stable_inputs',all(sha(ROOT/p)==hh for p,hh in hashes.items()))
np.savez_compressed(out/'native_matrices.npz',R=Rn,C=Cn,W=W,P=P,T=T,weights=weights,LMG=grid)
result=dict(checks=checks,records=records,inventory=inventory,distinct_positive_nodes=int(np.any(weights>0,axis=0).sum()),operator_cases=24,max_operator_relative_error=max(errors),finite_arrays_checked=len(finite),input_sha256=hashes,scope='Native discrete score and stacking validation; no continuous-L exclusion')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(checks.values()) else 1)

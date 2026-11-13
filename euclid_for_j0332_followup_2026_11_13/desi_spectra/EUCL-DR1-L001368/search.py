from pathlib import Path
import json,hashlib,time,sys
import numpy as np
from scipy.ndimage import median_filter,convolve1d
from scipy.signal import find_peaks
P=Path(__file__).resolve().parent;O=Path(sys.argv[1]) if len(sys.argv)>1 else P;O.mkdir(exist_ok=True);I=P;s=np.load(I/'spectrum.npz');m=np.load(P/'model.npz');C=json.loads((P/'contract.json').read_text());zs=np.arange(C['search_z_min'],C['search_z_max']+.000001,C['dz']);sky=np.array([5577,5890,6300,6364,7246,7914,8344,8827,8919,9439]);zl=C['foreground_z'];cameras={}
for band in ['b','r','z']:
 w=s[band+'_origwave'];f=s[band+'_origflux0'];n=s[band+'_orignoise0'];mod=np.interp(w,m['model_wave'],m['model_flux']);res=f-mod;res-=median_filter(res,size=151,mode='nearest');valid=np.isfinite(res)&np.isfinite(n)&(n>0)
 for line in np.r_[sky,np.array([3728.48,4862.683,4960.295,5008.239,6564.614])*(1+zl)]:valid&=abs(w-line)>8
 valid&=~(((w>6860)&(w<6950))|((w>7580)&(w<7700)));ivar=np.zeros_like(n);ivar[valid]=1/n[valid]**2;cameras[band]=dict(w=w,f=f,n=n,mod=mod,res=res,valid=valid,ivar=ivar)

def scan(residuals):
 scans=[]
 for sig in C['observed_gaussian_sigma_A']:
  per={}
  for band,d in cameras.items():
   dw=np.median(np.diff(d['w']));x=np.arange(-int(np.ceil(5*sig/dw)),int(np.ceil(5*sig/dw))+1)*dw;t=np.exp(-.5*(x/sig)**2);num=convolve1d(residuals[band]*d['ivar'],t,mode='constant');den=convolve1d(d['ivar'],t*t,mode='constant');coverage=convolve1d(d['valid'].astype(float),t*t,mode='constant')/(t*t).sum();per[band]=(num,den,coverage)
  def line_at(rest):
   lam=rest*(1+zs);num=np.zeros(len(zs));den=np.zeros(len(zs))
   for band,d in cameras.items():
    nn,dd,cv=per[band];coverage=np.interp(lam,d['w'],cv,left=0,right=0);ok=coverage>.8;num+=np.where(ok,np.interp(lam,d['w'],nn,left=0,right=0),0);den+=np.where(ok,np.interp(lam,d['w'],dd,left=0,right=0),0)
   return num,den
  ns=[];ds=[]
  for group,lines in C['groups_vacuum_A'].items():
   nn,dd=line_at(lines[-1])
   if len(lines)>1:
    nn2,dd2=line_at(lines[0]);ratio=C['OIII_4959_to_5007_ratio'];nn+=ratio*nn2;dd+=ratio*ratio*dd2
   ns.append(nn);ds.append(dd)
  ns=np.array(ns);ds=np.array(ds);sn=np.divide(ns,np.sqrt(ds),out=np.zeros_like(ns),where=ds>0);score=np.sum(np.maximum(sn,0)**2,axis=0);avail=(ds>0).sum(axis=0);ng=(sn>=3).sum(axis=0);qual=(ng>=3)&(sn.max(axis=0)>=5)&(avail>=3);scans.append(dict(sig=sig,snr=sn,score=score,qual=qual,n3=ng,available=avail))
 return scans
scans=scan({k:d['res'] for k,d in cameras.items()});candidates=[];allpeaks=[]
for r in scans:
 peaks=find_peaks(r['score'],distance=20)[0];peaks=sorted(peaks,key=lambda i:r['score'][i],reverse=True)[:12]
 for i in peaks:
  rec=dict(z=float(zs[i]),sigma_A=r['sig'],score=float(r['score'][i]),snr_groups={k:float(v) for k,v in zip(C['groups_vacuum_A'],r['snr'][:,i])},passes_predeclared_rule=bool(r['qual'][i]),groups_available=int(r['available'][i]));allpeaks.append(rec)
  if r['qual'][i]:candidates.append(rec)
rng=np.random.default_rng(7419);null=[]
for it in range(100):
 rr={}
 for band,d in cameras.items():
  sign=np.repeat(rng.choice([-1,1],size=(len(d['w'])+49)//50),50)[:len(d['w'])];rr[band]=d['res']*sign
 result=scan(rr);null.append(max([float(r['score'][r['qual']].max()) if np.any(r['qual']) else 0. for r in result]))
print('candidates',candidates,flush=True)
allpeaks.sort(key=lambda x:x['score'],reverse=True);out=dict(candidate_count=len(candidates),candidates=candidates,strongest_diagnostic_peaks=allpeaks[:12],null_realizations=100,null_passing_realizations=int(np.sum(np.array(null)>0)),null_max_qualifying_scores=null,claim='No verified source redshift; candidate multiplets only if rule passes',bins_retained={k:int(d['valid'].sum()) for k,d in cameras.items()});(O/'result.json').write_text(json.dumps(out,indent=2));np.savez_compressed(O/'scan_arrays.npz',z=zs,**{f'snr_width{r["sig"]}':r['snr'] for r in scans});np.savez_compressed(O/'residuals.npz',**{band+'_'+k:v for band,d in cameras.items() for k,v in d.items()})
(O/'computation_trace.json').write_text(json.dumps({'contract_sha256':hashlib.sha256((P/'contract.json').read_bytes()).hexdigest(),'inputs':{str(f.relative_to(I)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [I/'spectrum.npz',I/'viewer.html',P/'model.npz']},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2));print(out['strongest_diagnostic_peaks'][:3])

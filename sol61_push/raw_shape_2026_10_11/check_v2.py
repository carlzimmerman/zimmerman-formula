import json,sys,os
from pathlib import Path
import numpy as np
from astropy.io import fits
try:
 os.nice(10)
except PermissionError:
 print("OS denied optional nice adjustment; one numerical thread and CPU cap remain active.",flush=True)
D=Path('real_research/data/lensing_rar'); checks=[]
def check(name,ok):
 checks.append([name,bool(ok)])
 if not ok: print('FAIL',name,flush=True)
L=np.load(D/'lr_lenses.npz'); pl=np.load(D/'cfg110_perlens.npz')
WG=pl['WG']; WW=pl['WW']; patch=np.load(D/'lr_esd_jackknife.npz')['patch']; F=np.load(D/'cfg96_isoflags.npz')['f30'].astype(bool)
# Match catalogue coordinates using the exact existing CFG585 key convention.
with fits.open(D/'KiDS_DR4_brightsample.fits',memmap=True) as h:
 ra=np.array(h[1].data['RAJ2000'],float); dec=np.array(h[1].data['DECJ2000'],float)
with fits.open(D/'KiDS_DR4_brightsample_LePhare.fits',memmap=True) as h:
 ur=np.array(h[1].data['MAG_ABS_u']-h[1].data['MAG_ABS_r'],float)
key=lambda r,d:np.round(r*1e6).astype(np.int64)*10**9+np.round((d+90)*1e6).astype(np.int64)
kb=key(ra,dec); o=np.argsort(kb); kl=key(L['ra'],L['dec']); ix=np.clip(np.searchsorted(kb[o],kl),0,len(kb)-1)
check('all coordinates matched',np.all(kb[o][ix]==kl)); U=ur[o[ix]]
C=F & (L['typ'].astype(int)==1); lm=L['logM'].astype(float)
check('colour type reproduced',np.all((U>2)==(L['typ'].astype(int)==1)))
q=np.quantile(lm[C],np.linspace(0,1,11)); q[-1]+=1e-9
idxs=[np.where(C & (lm>=q[i]) & (lm<q[i+1]))[0] for i in range(10)]
def masks(rng=None):
 t=np.full(len(U),-1)
 for idx in idxs:
  dc=U[idx]-np.median(U[idx]); dc=dc if rng is None else rng.permutation(dc)
  order=np.argsort(dc,kind='stable'); n=len(idx)
  for k in range(3): t[idx[order[k*n//3:(k+1)*n//3]]]=k
 return t==0,t==2
KG=1.98847e30/(3.0857e16)**2
positive=True
def esd(mask,scale=None):
 global positive
 g=WG[mask].copy(); w=WW[mask]; p=patch[mask]
 if scale is not None:g*=scale
 pg=np.stack([np.bincount(p,weights=g[:,k],minlength=50) for k in range(15)],axis=1)
 pw=np.stack([np.bincount(p,weights=w[:,k],minlength=50) for k in range(15)],axis=1)
 tg=pg.sum(0); tw=pw.sum(0)
 positive &= bool(np.all(tw>0) and np.all(tw-pw>0))
 return tg/tw/KG,(tg-pg)/(tw-pw)/KG
allv,allo=esd(C); dev=allo-allo.mean(0); cov=49/50*dev.T@dev; W=1/np.diag(cov)
bands=[list(range(6,15)),[12,13,14],[9,10,11],[6,7,8]]
def amplitudes(y,o,scale=None):
 global positive
 dv,dl=esd(o,scale); yv,yl=esd(y)
 a=[]; al=[]
 for b in bands:
  nums=[W[b]@dv[b],W[b]@yv[b],dl[:,b]@W[b],yl[:,b]@W[b]]
  positive &= all(np.all(x>0) for x in nums)
  a.append(np.log10(nums[0]/nums[1])); al.append(np.log10(nums[2]/nums[3]))
 return np.array(a),np.array(al).T,dv,yv
Y,O=masks(); a,al,ov,yv=amplitudes(Y,O)
ref=json.loads(Path('campaign_fresh_gravity/CFG700_raw_esd_age/cfg700_results.json').read_text())
check('counts',int(Y.sum())==ref['N']['young'] and int(O.sum())==ref['N']['old'])
check('ESD reproduction',max(np.max(abs(ov-ref['esd_old'])),np.max(abs(yv-ref['esd_young'])))<1e-10)
check('amplitude reproduction',max(abs(a-np.array([ref['A'][b]['A'] for b in ['K9','K-in','K-mid','K-out']])))<1e-10)
s=float(a[1]-a[3]); ad=al-al.mean(0); acov=49/50*ad.T@ad
sj=float(np.sqrt(acov[1,1]+acov[3,3]-2*acov[1,3])); sind=float(np.sqrt(acov[1,1]+acov[3,3]))
uniform=amplitudes(Y,O,np.full(15,.8))[0]
check('MUTATE uniform shift',np.max(abs(uniform-a-np.log10(.8)))<1e-10)
check('MUTATE uniform shape invariant',abs(uniform[1]-uniform[3]-s)<1e-10)
scale=np.ones(15);scale[12:15]=10**.2
injected=amplitudes(Y,O,scale)[0]
check('MUTATE inner shape recovery',abs(injected[1]-injected[3]-s-.2)<1e-10)
rng=np.random.default_rng(700); null=[]
for i in range(200):
 y,o=masks(rng); null.append(amplitudes(y,o)[0])
null=np.array(null); sn=null[:,1]-null[:,3]; sd=float(sn.std()); z=s/sd
check('CFG700 null sigma reproduced',abs(null[:,0].std()-ref['null']['K9']['sd'])<1e-10)
check('positive weighted totals',positive)
check('finite',np.all(np.isfinite(null)) and np.all(np.isfinite(acov)))
result=dict(S=s,sigma_jackknife=sj,Z_jackknife=s/sj,sigma_independent_bands_wrong=sind,covariance_bands=acov.tolist(),sigma_null=sd,Z_null=z,p_two_sided_plus_one=float((1+np.sum(abs(sn)>=abs(s)))/201),null_mean=float(sn.mean()),null_amplitudes=null.tolist(),jackknife_amplitudes=al.tolist(),A=a.tolist(),checks=checks,interpretation='post-hoc shape hint' if abs(z)>=2 else 'shape unresolved by this diagnostic',caveat='Permutation null is no association, not the composite amplitude-only null. Acceleration-indexed stacks, not common physical radii.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['null_amplitudes','jackknife_amplitudes','covariance_bands']},indent=2))
assert all(ok for _,ok in checks)

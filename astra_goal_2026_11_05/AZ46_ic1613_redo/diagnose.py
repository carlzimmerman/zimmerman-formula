#!/usr/bin/env python3
"""Pre-freeze diagnosis only; no new observational pass/fail label."""
import hashlib,json,math,os,re,resource,time
from pathlib import Path
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[k]='1'
import numpy as np
from astropy.io import fits
from scipy.optimize import least_squares
from scipy.special import expit
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DATA=ROOT.parent/'_external_data/fn4a_ic1613_2026_11'
OLD=ROOT/'finish_2026_11_04/FN4_galaxy_rows_data/FN4a_ic1613_cube_model'
start=time.time();checks=[]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def check(name,passed,value):checks.append(dict(name=name,passed=bool(passed),value=value))
def meta(name):
    with fits.open(DATA/name,memmap=True,lazy_load_hdus=True) as h:
        hd=h[0].header.copy();offset=h.fileinfo(0)['datLoc']
    assert hd['BITPIX']==-32 and hd.get('BSCALE',1)==1 and hd.get('BZERO',0)==0
    lines=[x for x in hd.get('HISTORY',[]) if 'CLEAN BMAJ=' in x]
    m=re.search(r'BMAJ=\s*([\d.E+-]+) BMIN=\s*([\d.E+-]+) BPA=\s*([\d.E+-]+)',lines[-1])
    beam=[float(x) for x in m.groups()];beam[:2]=[x*3600 for x in beam[:2]]
    return hd,offset,beam
def readmap(name):
    hd,off,beam=meta(name)
    with (DATA/name).open('rb') as f:
        f.seek(off);a=np.frombuffer(f.read(hd['NAXIS1']*hd['NAXIS2']*4),dtype='>f4').reshape(hd['NAXIS2'],hd['NAXIS1']).astype('f8')
    return a,hd,beam
name='IC1613_NA_X0_P_R.FITS';hd,offset,beam=meta(name)
chunkrows=[]
for chunk in [32,64]:
    signed=np.longdouble(0);positive=np.longdouble(0);count=0
    with (DATA/name).open('rb') as f:
        f.seek(offset)
        for lo in range(0,hd['NAXIS2'],chunk):
            n=min(chunk,hd['NAXIS2']-lo)*hd['NAXIS1']
            x=np.frombuffer(f.read(n*4),dtype='>f4').astype(np.longdouble)
            x=x[np.isfinite(x)];signed+=x.sum();positive+=np.maximum(x,0).sum();count+=len(x)
    chunkrows.append(dict(chunk=chunk,signed_map_sum=float(signed),positive_map_sum=float(positive),finite_pixels=count))
check('row_chunk_pair',all(math.isclose(chunkrows[0][k],chunkrows[1][k],rel_tol=1e-10,abs_tol=0.) for k in ['signed_map_sum','positive_map_sum']),chunkrows)
mom0,h0,beam=readmap(name);mom0/=1000
with fits.open(DATA/name,memmap=True,lazy_load_hdus=True) as h:
    sample=np.asarray(h[0].section[0,0,900:905,900:905],dtype='f8').squeeze()/1000
check('independent_astropy_section',np.allclose(sample,mom0[900:905,900:905],rtol=0.,atol=0.,equal_nan=True),dict(shape=list(sample.shape)))
pixarea=abs(hd['CDELT1']*hd['CDELT2'])*3600**2
mass=[]
for label,factor in [('original_1.1331',1.1331),('exact_Gaussian',math.pi/(4*math.log(2)))]:
    beam_pixels=factor*beam[0]*beam[1]/pixarea
    for sign,total in [('positive',chunkrows[0]['positive_map_sum']),('signed',chunkrows[0]['signed_map_sum'])]:
        flux=total/1000/beam_pixels;MHI=2.356e5*.7**2*flux
        mass.append(dict(convention=label,sum=sign,beam_pixels=beam_pixels,flux_Jykms=flux,MHI=MHI,
                         ratio_to_Oh2015=(MHI/(5.93e7/1.4)),ratio_to_Hunter2012_robust=MHI/10**7.53))
beams={}
for name2 in ['IC1613_NA_ICL001.FITS','IC1613_R_ICL001.FITS',name]:
    h,off,b=meta(name2)
    beams[name2]=dict(beam_arcsec_deg=b,unit=h['BUNIT'],header_sha256=hashlib.sha256(h.tostring().encode()).hexdigest(),
                     primary_beam_history=[s for s in h.get('HISTORY',[]) if s.startswith('PBCOR')])
old=json.loads((OLD/'fn4a_s0.json').read_text());crop=old['crop'];n=crop['size'];binning=crop['bin'];nb=n//binning
def cropbin(a):
    sub=a[crop['y_lo']:crop['y_lo']+n,crop['x_lo']:crop['x_lo']+n]
    with np.errstate(invalid='ignore'):
        return np.nanmean(sub.reshape(nb,binning,nb,binning).transpose(0,2,1,3).reshape(nb,nb,-1),axis=2)
m0=cropbin(mom0);del mom0
m1=cropbin(readmap('IC1613_NA_XMOM1.FITS')[0]/1000)
m2=cropbin(readmap('IC1613_NA_XMOM2.FITS')[0]/1000)
with np.load(OLD/'cache/prep.npz',allow_pickle=False) as ck:
    XE=ck['XE'];YN=ck['YN'];mask=ck['mask'].any(0)
pa=math.radians(73.7);inc=math.radians(48.)
major=XE*math.sin(pa)+YN*math.cos(pa);minor=(-XE*math.cos(pa)+YN*math.sin(pa))/math.cos(inc)
R=np.hypot(major,minor);cth=major/np.maximum(R,1e-9)
rc=(np.arange(80)+.5)*13.2;vr=np.full(80,np.nan);sg=vr.copy();Sg=vr.copy()
for k in range(80):
    ring=(R>=k*13.2)&(R<(k+1)*13.2);good=ring&np.isfinite(m1)&mask&(abs(cth)>=.5)
    if good.sum()>=8:vr[k]=np.sum((m1[good]+232.2)*cth[good])/(math.sin(inc)*np.sum(cth[good]**2))
    use=ring&mask&np.isfinite(m2)
    if use.sum()>=8:sg[k]=np.mean(m2[use]);Sg[k]=np.mean(np.nan_to_num(m0[ring]))
def sm3(a):
    b=a.copy();b[1:-1]=(a[:-2]+a[1:-1]+a[2:])/3;return b
smoothsg=sm3(sg);q=sm3(Sg)*smoothsg**2
der=np.gradient(np.log(np.clip(q,1e-30,None)),np.log(rc))
drift2=-smoothsg**2*der;vc=np.sqrt(np.maximum(vr**2+drift2,0))
Rmax=2.71e3/(.7e6*math.pi/(180*3600));good=np.isfinite(vr)&np.isfinite(vc)
vu=float(np.interp(Rmax,rc[good],vr[good]));vv=float(np.interp(Rmax,rc[good],vc[good]))
check('old_ring_velocity_reproduced',abs(vu-old['S0b']['V_rot_uncorrected'])<1e-8,vu-old['S0b']['V_rot_uncorrected'])
check('old_drift_velocity_reproduced',abs(vv-old['S0b']['V_c_corrected'])<1e-8,vv-old['S0b']['V_c_corrected'])
sel=np.isfinite(q)&(q>0)&(rc<=Rmax);rr=rc[sel];lq=np.log(q[sel])
# log q = log I0 + log(1+R0) - log(R0+exp(alpha R)).
def logq(th,r):
    li,lr,la=th;return li+np.logaddexp(0,lr)-np.logaddexp(lr,np.exp(la)*r)
fits0=[]
for r0 in [1.,100.]:
    fit=least_squares(lambda th:logq(th,rr)-lq,[float(lq.max()),math.log(r0),math.log(.002)],bounds=([-30,-20,math.log(1e-5)],[30,20,math.log(.1)]),max_nfev=2000)
    fits0.append(fit)
best=min(fits0,key=lambda f:float(f.fun@f.fun));li,lr,la=best.x;alpha=math.exp(la)
smooth_drift2=rc*smoothsg**2*alpha*expit(alpha*rc-lr)
vsmooth=np.sqrt(np.maximum(vr**2+smooth_drift2,0));valid=np.isfinite(vsmooth)&np.isfinite(vr)
smooth_v=float(np.interp(Rmax,rc[valid],vsmooth[valid]))
def serial(a):return [float(x) if np.isfinite(x) else None for x in a]
inputs=[DATA/name,DATA/'IC1613_NA_XMOM1.FITS',DATA/'IC1613_NA_XMOM2.FITS',OLD/'cache/prep.npz',OLD/'fn4a_s0.json',Path(__file__),HERE/'DIAGNOSTIC_PLAN.md']
out=dict(status='PRE-FREEZE DIAGNOSIS ONLY; no new physical grade',mass=mass,header_evidence=beams,checks=checks,
         drift=dict(Rmax_arcsec=Rmax,old_Vrot=vu,old_Vcorrected=vv,smooth_q_Vcorrected=smooth_v,
                    smooth_fit=dict(I0=math.exp(li),R0=math.exp(lr),alpha_per_arcsec=alpha,log_q_rms=float(np.sqrt(np.mean(best.fun**2))),status=int(best.status),
                                    start_costs=[float(f.fun@f.fun) for f in fits0]),
                    profiles=dict(radius=serial(rc),Vrot=serial(vr),sigma=serial(sg),density=serial(Sg),q=serial(q),old_drift2=serial(drift2),smooth_drift2=serial(smooth_drift2))),
         inputs={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else '../_external_data/'+str(p.relative_to(ROOT.parent/'_external_data')):sha(p) for p in inputs},
         scope='kappa = 1/2 FITTED; not theory closed')
(HERE/'diagnosis.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
(HERE/'diagnosis_runtime.json').write_text(json.dumps(dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
print(json.dumps(dict(checks=checks,mass=mass,drift={k:v for k,v in out['drift'].items() if k!='profiles'}),indent=2))
raise SystemExit(int(not all(c['passed'] for c in checks)))

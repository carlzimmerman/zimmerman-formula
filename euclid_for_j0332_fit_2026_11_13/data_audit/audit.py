from pathlib import Path
import numpy as np,json,csv,hashlib
from astropy.io import fits
from scipy.special import gammaincinv
from scipy.signal import fftconvolve
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;I=P.parent/'inputs';out={}
h=fits.open(next((I/'dataset').glob('Tile*.fits')));d=h['VIS_BGSUB'].data.astype(float);rms=h['VIS_RMS'].data.astype(float);psf=h['VIS_PSF'].data.astype(float);m=fits.open(I/'results/model.fits');p=fits.open(I/'results/pre_psf.fits');model=m['VIS_GALAXY_0'].data+m['VIS_GALAXY_1'].data;pre=p['VIS_GALAXY_0'].data.astype(float)
yy,xx=np.indices(d.shape);x=(xx-49.5)*.1;yn=(yy-49.5)*.1;ys=-yn
info=json.loads((I/'dataset/info.json').read_text());circle=(ys-info['mask_centre'][0])**2+(x-info['mask_centre'][1])**2<info['mask_radius']**2
seg={f.stem:fits.getdata(f).astype(float) for f in (I/'dataset/segmentation').glob('*.fits')};valid=circle&(rms>0)&np.isfinite(d)&(seg['artefact_binary']==0)
z=(d-model)/rms
out['psf']={'sum':float(psf.sum()),'min':float(psf.min()),'argmax':list(map(int,np.unravel_index(psf.argmax(),psf.shape)))}
out['regions']={}
for name,mask in [('circle',circle),('circle_no_artefact',valid),('source',valid&(seg['source_binary']>0)),('lens',valid&(seg['lens_binary']>0)),('background',valid&(seg['source_binary']==0)&(seg['lens_binary']==0))]:
 v=z[mask];out['regions'][name]={'n':int(mask.sum()),'chi2':float((v*v).sum()),'chi2_per_pixel':float(np.mean(v*v)),'resid_mean':float(v.mean()),'resid_std':float(v.std())}
# Outer image empirical correlation, avoiding lens/source and 3sigma outliers.
bg=valid&(seg['source_binary']==0)&(seg['lens_binary']==0)&(np.hypot(x+.2,yn+.3)>2)&(abs(z)<3)
out['background_corr']={}
for dy,dx in [(0,1),(1,0),(1,1),(0,2),(2,0)]:
 a=z[:100-dy,:100-dx];b=z[dy:,dx:];mask=bg[:100-dy,:100-dx]&bg[dy:,dx:]
 out['background_corr'][str((dy,dx))]={'n':int(mask.sum()),'pearson':float(np.corrcoef(a[mask],b[mask])[0,1])}
# Test Sersic convention allowing scalar amplitude but no structural optimization.
r=next(csv.DictReader(open(I/'results/lens_sersic.csv')));cy,cx=float(r['centre_0']),float(r['centre_1']);e0,e1=float(r['ell_comps_0']),float(r['ell_comps_1']);q=(1-np.hypot(e0,e1))/(1+np.hypot(e0,e1));phi=.5*np.arctan2(e0,e1);re=float(r['effective_radius']);n=float(r['sersic_index']);bn=gammaincinv(2*n,.5)
out['sersic_convention_tests']=[]
for ysign in [1,-1]:
 for flipsign in [1,-1]:
  # Equivalent major/minor coordinates with q<1 along major X.
  Y=ys*ysign-cy;X=x-cx;ang=phi*flipsign;Xr=X*np.cos(ang)+Y*np.sin(ang);Yr=-X*np.sin(ang)+Y*np.cos(ang)
  for convention,R in [('major',np.sqrt(Xr**2+Yr**2/q**2)),('geometric_mean',np.sqrt(q*Xr**2+Yr**2/q))]:
   S=np.exp(-bn*((R/re)**(1/n)-1));mask=(np.hypot(X,Y)>.3)&(np.hypot(X,Y)<3)&(pre>0);amp=np.sum(S[mask]*pre[mask])/np.sum(S[mask]**2);err=np.sqrt(np.mean(((amp*S[mask]-pre[mask])/pre[mask])**2));out['sersic_convention_tests'].append(dict(y_sign=ysign,phi_sign=flipsign,radius=convention,amplitude=float(amp),relative_rms=float(err)))
# Exact map pre-PSF to convolved discrepancy test.
out['convolution_tests']={}
for i in [0,1]:
 for norm in [False,True]:
  conv=fftconvolve(p[f'VIS_GALAXY_{i}'].data,psf/(psf.sum() if norm else 1),mode='same');tar=m[f'VIS_GALAXY_{i}'].data;mask=valid
  out['convolution_tests'][f'galaxy{i}_normalize{norm}']={'relative_l2':float(np.linalg.norm((conv-tar)[mask])/np.linalg.norm(tar[mask]))}
fig,ax=plt.subplots(2,3,figsize=(12,8));panels=[(d,'VIS observed'),(model,'Released model sum'),(z,'Residual / supplied RMS'),(seg['source_binary'],'Source mask'),(seg['artefact_binary'],'Artefact mask'),(valid,'Circle excluding artefacts')]
for a,(im,title) in zip(ax.flat,panels):
 v=3 if title.startswith('Residual') else None;a.imshow(im,origin='lower',cmap='RdBu_r' if v else 'viridis',vmin=-v if v else None,vmax=v);a.set_title(title);a.set_xlabel('column: west →');a.set_ylabel('row: north →')
fig.tight_layout();fig.savefig(P/'vis_diagnostics.png',dpi=160);plt.close(fig)
out['input_sha256']={str(f.relative_to(I)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [next((I/'dataset').glob('Tile*.fits')),I/'results/model.fits',I/'results/pre_psf.fits',I/'results/deflections.fits',I/'results/lens_sersic.csv',I/'results/coolest.json']}
(P/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))

from inversion import setup
from pathlib import Path
import numpy as np,json,time,os
os.environ['MPLCONFIGDIR']='/private/tmp/forj0332-mpl'
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astropy.io import fits
P=Path(__file__).resolve().parent;I=P.parent/'inputs';c=json.loads((I/'results/coolest.json').read_text());p=c['lensing_entities'][0]['mass_model'][0]['parameters'];v=lambda p,k:p[k]['point_estimate']['value'];q=v(p,'q');a=np.pi/2+np.deg2rad(v(p,'phi'));cx=v(p,'center_x');cn=v(p,'center_y');b=v(p,'theta_E')/np.sqrt(q);g=c['lensing_entities'][2]['mass_model'][0]['parameters'];gg=v(g,'gamma_ext');ag=np.pi/2+np.deg2rad(v(g,'phi_ext'));g1=gg*np.cos(2*ag);g2=gg*np.sin(2*ag)
def sie(X,N):
 dx=X-cx;dy=N-cn;u=np.cos(a)*dx+np.sin(a)*dy;vv=-np.sin(a)*dx+np.cos(a)*dy;f=np.sqrt(1-q*q);psi=np.sqrt(q*q*u*u+vv*vv);au=b*q/f*np.arctan(f*u/psi);av=b*q/f*np.arctanh(f*vv/psi);return np.cos(a)*au-np.sin(a)*av+g1*X+g2*N,np.sin(a)*au+np.cos(a)*av+g2*X-g1*N
out=[]
for ns,h,ss in [(25,.04,1),(33,.03,1),(25,.04,2)]:
 t=time.time();obj=setup(nsource=ns,source_pixel=h,supersample=ss);r=obj.optimize_regularization(sie);pred=(obj.fullB@r['source'].ravel()).reshape(100,100)+r['lens_amplitude']*obj.lens+r['sky'];z=(obj.data-pred)/obj.noise
 row={k:v for k,v in r.items() if not isinstance(v,np.ndarray)};row.update(nsource_side=ns,source_pixel=h,supersample=ss,total_seconds=time.time()-t,source_chi2=float(np.sum(z[obj.mask&obj.source_mask]**2)));out.append(row);np.savez(P/f'baseline_{ns}_ss{ss}.npz',source=r['source'],model=pred,residual=z,mask=obj.mask)
 if ns==25 and ss==1:
  fig,ax=plt.subplots(1,3,figsize=(12,4));ax[0].imshow(pred,origin='lower');ax[0].set_title('Independent SIE inversion');ax[1].imshow(z,origin='lower',vmin=-3,vmax=3,cmap='RdBu_r');ax[1].set_title('Residual / supplied RMS');ax[2].imshow(r['source'],origin='lower',extent=[-.51,.45,-.53,.43]);ax[2].set_title('Posterior mean source');fig.tight_layout();fig.savefig(P/'baseline.png',dpi=150);plt.close(fig)
 print(row,flush=True)
(P/'benchmark.json').write_text(json.dumps(out,indent=2)+'\n')
# Counterimage holdout: remove its segmentation pixels from training, predict them.
obj=setup();hold=obj.mask&obj.source_mask&(obj.N<-.4)&(obj.X<0);orig=obj.mask.copy();obj.mask&=~hold;r=obj.optimize_regularization(sie);pred=(obj.fullB@r['source'].ravel()).reshape(100,100)+r['lens_amplitude']*obj.lens+r['sky'];z=(obj.data-pred)/obj.noise;cv={k:v for k,v in r.items() if not isinstance(v,np.ndarray)};cv.update(holdout_pixels=int(hold.sum()),holdout_chi2=float(np.sum(z[hold]**2)),holdout_mean=float(z[hold].mean()),holdout_std=float(z[hold].std()));(P/'counterimage_holdout.json').write_text(json.dumps(cv,indent=2)+'\n');print('CV',cv,flush=True)

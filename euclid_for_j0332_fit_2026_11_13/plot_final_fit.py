"""Display actual data and matched source reconstructions; no statistical verdict."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import AsinhNorm
BASE=Path(__file__).resolve().parent
runs=BASE/'image_fit_02';out=BASE/'figures';out.mkdir(exist_ok=True)
archive=np.load(BASE/'image_robustness/run_03/images_sources.npz');a={'source':archive['compact25_h004_gate0.3_high_source'],'model_valid':archive['compact25_h004_gate0.3_high_model_valid'],'mask':archive['mask'],'data':archive['data'],'noise':archive['noise']};s={'source':archive['compact25_h004_SIE_source'],'model_valid':archive['compact25_h004_SIE_model_valid']};mask=a['mask'];data=a['data'];noise=a['noise']
def full(z):
    m=np.full(data.shape,np.nan);m[mask]=z['model_valid'];return m
ma=full(a);ms=full(s);fig,axs=plt.subplots(2,3,figsize=(12,7),constrained_layout=True)
norm=AsinhNorm(linear_width=.003,vmin=-.003,vmax=.08)
extent=[-5,5,-5,5]
for ax,im,title in zip(axs[0],[data,ms,ma],['Euclid VIS data','SIE control + fitted source','Unscreened AQUAL + fitted source']):
    p=ax.imshow(im,origin='lower',extent=extent,cmap='magma',norm=norm)
    ax.set_title(title,fontsize=11);ax.set_xlim(-3,3);ax.set_ylim(-3,3);ax.set_xlabel('West offset (arcsec)');ax.set_ylabel('North offset (arcsec)')
fig.colorbar(p,ax=axs[0],label='ADU/s per image pixel',shrink=.8)
for ax,im,title in zip(axs[1,:2],[(data-ms)/noise,(data-ma)/noise],['SIE residual / released RMS','AQUAL residual / released RMS']):
    p=ax.imshow(im,origin='lower',extent=extent,cmap='RdBu_r',vmin=-4,vmax=4)
    ax.set_title(title,fontsize=11);ax.set_xlim(-3,3);ax.set_ylim(-3,3);ax.set_xlabel('West offset (arcsec)');ax.set_ylabel('North offset (arcsec)')
fig.colorbar(p,ax=axs[1,:2],label='Residual / RMS',shrink=.8)
im=a['source'];p=axs[1,2].imshow(im,origin='lower',extent=[-.53,.47,-.55,.45],cmap='magma',vmin=0,vmax=np.max(im))
axs[1,2].set_title('AQUAL reconstructed source',fontsize=11);axs[1,2].set_xlabel('West source offset (arcsec)');axs[1,2].set_ylabel('North source offset (arcsec)')
fig.suptitle('FOR J0332: conditional VIS image fit\nMultiple-image association enforced; fixed light shape, fitted mass/shear/source',fontsize=12)
fig.savefig(out/'for_j0332_final_fit.png',dpi=180);plt.close(fig)
print(out/'for_j0332_final_fit.png')

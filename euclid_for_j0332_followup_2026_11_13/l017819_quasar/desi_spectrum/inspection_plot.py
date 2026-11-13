"""Qualitative known-redshift inspection, without fitting or significance claims."""
from pathlib import Path
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
P=Path(__file__).resolve().parent;x=np.load(P/'target_coadd.npz')
fig,axes=plt.subplots(3,1,figsize=(12,8))
for b in 'BRZ':
    w=x[b+'_WAVELENGTH'];f=x[b+'_FLUX'][0];good=(x[b+'_IVAR'][0]>0)&(x[b+'_MASK'][0]==0)
    # Interpolation is only for this display; original data are unchanged.
    smooth=gaussian_filter1d(np.interp(w,w[good],f[good]),2)
    for ax in axes:ax.plot(w,smooth,lw=.7,label=b)
for ax,limits in zip(axes,[(3600,9824),(4050,4400),(5900,6450)]):
    ax.set_xlim(*limits)
    for label,rest in [('CIII]',1908.73),('MgII',2798.75),('[OII]',3727.4)]:
        w=rest*2.210
        if limits[0]<w<limits[1]:
            ax.axvline(w,color='red',ls='--',lw=.7)
            ax.text(w,1.01,label,transform=ax.get_xaxis_transform(),ha='center')
    ax.set_ylabel(r'flux [$10^{-17}$ erg s$^{-1}$ cm$^{-2}$ A$^{-1}$]');ax.grid(alpha=.2)
axes[-1].set_xlabel('vacuum wavelength [Angstrom]')
fig.suptitle('L017819 DESI DR1 — known-source-z=1.210 markers; display smoothing only')
fig.tight_layout(rect=[0,0,1,.97]);fig.savefig(P/'spectrum_check.png',dpi=150)

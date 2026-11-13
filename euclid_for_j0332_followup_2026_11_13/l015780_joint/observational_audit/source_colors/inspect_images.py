from pathlib import Path
import numpy as np,json,hashlib
from astropy.io import fits
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import binary_dilation
p=Path('euclid_for_j0332_followup_2026_11_13/l015780_inputs');o=Path('euclid_for_j0332_followup_2026_11_13/l015780_joint/observational_audit/source_colors')
f=p/'dataset/Tile102159966RA1514073110655DEC0675075428182.fits'; h=fits.open(f); m=fits.open(p/'results/model.fits')
s=fits.getdata(p/'dataset/segmentation/source_binary.fits').astype(bool); a=fits.getdata(p/'dataset/segmentation/artefact_binary.fits').astype(bool)
print('model HDUs',[(x.name,None if x.data is None else x.data.shape) for x in m]);print('masks',s.sum(),a.sum())
g=h['HSC_G_BGSUB'].data.astype(float);l=m['HSC_G_GALAXY_0'].data.astype(float);t=m['HSC_G_GALAXY_1'].data.astype(float);r=h['HSC_G_RMS'].data.astype(float); ps=h['HSC_G_PSF'].data.astype(float)
fig,ax=plt.subplots(2,3,figsize=(13,8));v=np.percentile(g,[5,99]);lims=(float(v[0]),float(v[1]));
for q,img,title in zip(ax.flat,[g,l,t,g-l,g-l-t,r],['RAW HSC g','Released lens template','Released source template','Data minus released lens','Full-model residual','Supplied RMS']):
 im=q.imshow(img,origin='lower',extent=(-5,5,-5,5),vmin=lims[0] if title!='Supplied RMS' else None,vmax=lims[1] if title!='Supplied RMS' else None,cmap='magma');q.contour(s,levels=[.5],extent=(-5,5,-5,5),colors='cyan',linewidths=.5);q.contour(a,levels=[.5],extent=(-5,5,-5,5),colors='lime',linewidths=.5);q.set_title(title);q.set_xlabel('West [arcsec]');q.set_ylabel('North [arcsec]');fig.colorbar(im,ax=q)
fig.suptitle('Diagnostic only: cyan VIS source mask; green contaminant mask; no independent source-z likelihood');fig.tight_layout();fig.savefig(o/'raw_g_diagnostic.png',dpi=160)
Y,X=np.indices(ps.shape);rr=np.hypot(X-(ps.shape[1]-1)/2,Y-(ps.shape[0]-1)/2)*.1;pn=ps/ps.sum();en={str(rad):float(pn[rr<=rad].sum()) for rad in [.3,.5,.75,1,1.5,2]}
record={'purpose':'Data diagnostic, not significance test or redshift estimate','input_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest(),str(p/'results/model.fits'):hashlib.sha256((p/'results/model.fits').read_bytes()).hexdigest()},'g_psf_sum':float(ps.sum()),'g_psf_encircled_energy_normalized':en,'source_mask_pixels':int(s.sum()),'artifact_mask_pixels':int(a.sum()),'warning':'Source mask is VIS reference; g offset is about .025arcsec; model templates already band-aligned. Supplied RMS is diagonal only. No fitted coefficients or formal detection significance.'}
(o/'diagnostic_metadata.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))

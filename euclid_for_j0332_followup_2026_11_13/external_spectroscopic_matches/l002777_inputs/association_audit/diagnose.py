from pathlib import Path
import json,numpy as np
from astropy.io import fits
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path('euclid_for_j0332_followup_2026_11_13/external_spectroscopic_matches/l002777_inputs');out=p/'association_audit/run_01';h=fits.open(next((p/'dataset').glob('Tile*.fits')));bands=['VIS','NIR_Y','NIR_J','NIR_H','HSC_G','MEGACAM_R','PANSTARRS_I','HSC_Z'];record={};points={'A common':[-.15,-.65],'B current':[-1.05,.25],'C current':[.65,-.05],'D old north':[.55,1.35],'E old':[-1.05,-.65]};fig,ax=plt.subplots(2,4,figsize=(16,9))
s=fits.getdata(p/'dataset/segmentation/source_binary.fits').astype(bool);a=fits.getdata(p/'dataset/segmentation/artefact_binary.fits').astype(bool)
for q,b in zip(ax.flat,bands):
 im=h[b+'_BGSUB'].data.astype(float);ps=h[b+'_PSF'].data.astype(float);yy,xx=np.indices(ps.shape);rr=np.hypot(xx-(ps.shape[1]-1)/2,yy-(ps.shape[0]-1)/2)*.1;ind=np.argsort(rr.ravel());cs=np.cumsum(ps.ravel()[ind])/ps.sum();rad=rr.ravel()[ind];record[b]={'psf_sum':float(ps.sum()),'r50_arcsec':float(rad[np.searchsorted(cs,.5)]),'r80_arcsec':float(rad[np.searchsorted(cs,.8)]),'negative_psf_fraction_abs':float(-ps[ps<0].sum()/abs(ps).sum())};lo,hi=np.percentile(im,[5,99.5]);q.imshow(np.arcsinh((im-lo)/(hi-lo)*5),origin='lower',extent=(-5,5,-5,5),cmap='magma',vmin=0,vmax=np.arcsinh(5));q.contour(s,levels=[.5],extent=(-5,5,-5,5),colors='cyan',linewidths=.4);q.contour(a,levels=[.5],extent=(-5,5,-5,5),colors='lime',linewidths=.4)
 for name,(x,y) in points.items():q.scatter(x,y,s=30,facecolors='none',edgecolors='white');q.text(x+.07,y+.07,name[0],color='white',fontsize=8)
 q.set(xlim=(-3,3),ylim=(-3,3),title=b+' independently scaled',xlabel='West [arcsec]',ylabel='North [arcsec]')
fig.suptitle('Raw images; cyan source mask; green artifact mask. All old/current marker sites retained; colors not PSF-matched');fig.tight_layout();fig.savefig(out/'eight_band_markers.png',dpi=160)
(out/'result.json').write_text(json.dumps({'purpose':'Finite PSF support/morphology diagnostic, not association classification or photometry','bands':record,'point_union_west_north_arcsec':points,'source_mask_pixels':int(s.sum()),'artifact_mask_pixels':int(a.sum()),'coordinates':'pixel centers Xwest=(col-49.5)*.1,Nnorth=(row-49.5)*.1; release positions south,west converted to west,north','non_claims':['Separate band stretches cannot establish color equality','PSF EEF computed from finite stamp, no outside-wing correction','No identity or source-redshift inference']},indent=2));print(json.dumps(record,indent=2))

from pathlib import Path
import numpy as np,json,csv,hashlib
from astropy.io import fits
from scipy.optimize import least_squares
from scipy.special import gammaincinv,gammainc
P=Path(__file__).resolve().parent;I=P.parent/'inputs';h=fits.open(I/'results/pre_psf.fits');c=json.loads((I/'results/coolest_sersic.json').read_text())['lensing_entities'][0]['light_model'][0]['parameters'];v=lambda k:c[k]['point_estimate']['value'];yy,xx=np.indices((100,100));X=(xx-49.5)*.1;N=(yy-49.5)*.1;start=[v('center_x'),v('center_y'),np.log(v('theta_eff')),np.log(v('n')),v('q'),np.pi/2+np.deg2rad(v('phi')),np.log(v('I_eff'))];rows=[]
for hd in h[1:]:
 if not hd.name.endswith('GALAXY_0'):continue
 d=hd.data.astype(float);mask=(np.hypot(X-start[0],N-start[1])>.3)&(np.hypot(X-start[0],N-start[1])<3)&(d>0);weight=np.maximum(d,.0001*d.max());p0=np.array(start);p0[-1]=np.log(np.median(d[mask]/h['VIS_GALAXY_0'].data[mask])*v('I_eff'))
 def pred(p):
  cx,cn,lr,ln,q,a,li=p;dx=X-cx;dn=N-cn;u=np.cos(a)*dx+np.sin(a)*dn;w=-np.sin(a)*dx+np.cos(a)*dn;R=np.sqrt(q*u*u+w*w/q);n=np.exp(ln);return np.exp(li)*np.exp(-gammaincinv(2*n,.5)*((R/np.exp(lr))**(1/n)-1))
 fit=least_squares(lambda p:((pred(p)-d)/weight)[mask],p0,max_nfev=100);p=fit.x;rows.append(dict(band=hd.name,cx=float(p[0]),cn=float(p[1]),Re_circularized=float(np.exp(p[2])),n=float(np.exp(p[3])),q=float(p[4]),phi_from_west_rad=float(p[5]),fractional_rms=float(np.sqrt(np.mean(((pred(p)-d)/d)[mask]**2))),success=bool(fit.success)))
(P/'map_shape_fits.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
# Enclosed-flux fractions; illustrates n/Re degeneracy, not independent massmeasurement.
curves=[]
for R in [.3,.5,1.,1.497,2.,3.]:
 frac=lambda n,re:float(gammainc(2*n,gammaincinv(2*n,.5)*(R/re)**(1/n)))
 curves.append(dict(R_arcsec=R,Euclid_free_n=frac(v('n'),v('theta_eff')),Cabanac_Rc_n4=frac(4,.36),Cabanac_H_n4=frac(4,.43),Cabanac_Ks_n4=frac(4,.50)))
(P/'sersic_enclosed_light_comparison.json').write_text(json.dumps(curves,indent=2));(P/'input_hashes.json').write_text(json.dumps({str(f.relative_to(I)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [I/'results/pre_psf.fits',I/'results/coolest_sersic.json',I/'results/lens_sersic.csv']},indent=2))

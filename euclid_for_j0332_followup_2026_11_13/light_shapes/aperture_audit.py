"""Audit the finite modelling-circle SED flux versus infinite Sersic mass.
This changes only normalization under the adopted constant-M/L model.
Shape-summary variation is sensitivity, not a joint posterior or a refit.
"""
import argparse,io,json,sys,time
from pathlib import Path
from zipfile import ZipFile
sys.dont_write_bytecode=True
import numpy as np
import csv
class Row(dict):
 def __getattr__(self,k):return self[k]
def read_csv(file):
 def conv(v):
  try:return float(v)
  except (TypeError,ValueError):return v
 return [Row({k:conv(v) for k,v in r.items()}) for r in csv.DictReader(file)]
from scipy.special import gammainc,gammaincinv,gammaln
from scipy.integrate import quad
from scipy.stats import norm,qmc
from astropy.io import fits
from fit_light_shapes import Renderer
ROOT=Path(__file__).resolve().parents[2]
I=ROOT/'euclid_for_j0332_fit_2026_11_13/inputs'

def fraction(regeom,n,q,phi,cx,cy,maskx,masky,radius,order=256):
 arrays=np.broadcast_arrays(*[np.atleast_1d(v).astype(float) for v in [regeom,n,q,phi,cx,cy]])
 regeom,n,q,phi,cx,cy=arrays
 z,w=np.polynomial.legendre.leggauss(order);t=(z+1)*np.pi;w=w*np.pi
 co=np.cos(t);si=np.sin(t);dot=(cx-maskx)[:,None]*co+(cy-masky)[:,None]*si
 rmax=-dot+np.sqrt(dot*dot+radius*radius-((cx-maskx)**2+(cy-masky)**2)[:,None])
 ct=np.cos(t[None,:]-phi[:,None]);st=np.sin(t[None,:]-phi[:,None]);metric=ct*ct+st*st/q[:,None]**2
 major=regeom/np.sqrt(q);arg=gammaincinv(2*n,.5)[:,None]*(rmax*np.sqrt(metric)/major[:,None])**(1/n[:,None])
 return np.sum(w*gammainc(2*n[:,None],arg)/(2*np.pi*q[:,None]*metric),axis=1)

def quant(x):return dict(zip(['q025','q16','median','q84','q975'],map(float,np.quantile(x,[.025,.16,.5,.84,.975]))))

def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);started=time.monotonic()
 c=json.loads((I/'results/coolest_sersic.json').read_text())['lensing_entities'][0]['light_model'][0]['parameters'];v=lambda k:c[k]['point_estimate']['value']
 info=json.loads((I/'dataset/info.json').read_text());maskx=info['mask_centre'][1];masky=-info['mask_centre'][0];radius=info['mask_radius'];pix=info['pixel_scale']
 re,n,q,phi,cx,cy=v('theta_eff'),v('n'),v('q'),np.pi/2+np.deg2rad(v('phi')),v('center_x'),v('center_y')
 bn=gammaincinv(2*n,.5)
 # I_eff is sampled native per-image-pixel intensity; division by pixel area
 # turns it into a surface brightness per square arcsec for analytic integration.
 Finf=v('I_eff')/pix**2*2*np.pi*re**2*n*np.exp(bn+gammaln(2*n)-2*n*np.log(bn))
 f=float(fraction(re,n,q,phi,cx,cy,maskx,masky,radius)[0]);f512=float(fraction(re,n,q,phi,cx,cy,maskx,masky,radius,512)[0])
 # Independent adaptive angular integration; exact radial gamma primitive.
 def integrand(t):
  dot=(cx-maskx)*np.cos(t)+(cy-masky)*np.sin(t);rmax=-dot+np.sqrt(dot*dot+radius**2-(cx-maskx)**2-(cy-masky)**2)
  metric=np.cos(t-phi)**2+np.sin(t-phi)**2/q**2
  return gammainc(2*n,bn*(rmax*np.sqrt(metric)/(re/np.sqrt(q)))**(1/n))/(2*np.pi*q*metric)
 fad=quad(integrand,0,2*np.pi,epsabs=1e-11,epsrel=1e-11,limit=100)[0]
 assert abs(f-f512)<1e-10 and abs(f-fad)<1e-10
 yy,xx=np.indices((100,100));X=(xx-49.5)*pix;N=(yy-49.5)*pix
 circle=(X-maskx)**2+(N-masky)**2<radius**2
 artifact=fits.getdata(I/'dataset/segmentation/artefact_binary.fits')>0
 pars=np.array([cx,cy,np.log(re/np.sqrt(q)),np.log(n),q,phi]);unit=Renderer(np.ones((1,1)),fine=True).render(pars)
 f_pixels=float(unit[circle].sum());mag=read_csv((I/'results/magnitudes.csv').open())
 sums=[]
 with fits.open(I/'results/pre_psf.fits') as pre,fits.open(I/'results/model.fits') as con,fits.open(I/'dataset/Tile102034383RA0532498193624DECNEG0359643115588.fits') as hd:
  for row in mag:
   band=row.waveband.upper();a=np.array(pre[band+'_GALAXY_0'].data,float);b=np.array(con[band+'_GALAXY_0'].data,float);zp=hd[band+'_BGSUB'].header['MAGZERO'];conversion=3631e6*10**(-.4*zp)
   native=float(a[circle].sum());uJy=native*conversion
   sums.append({'band':band,'native_units':hd[band+'_BGSUB'].header.get('BUNIT'),'MAGZERO':float(zp),'native_to_microJy':float(conversion),
      'unconvolved_circle_native':native,'unconvolved_circle_microJy':uJy,'catalogue_lens_flux_median_microJy':float(row.lens_flux),'catalogue_lens_flux_max_lh_microJy':float(row.lens_flux_max_lh),
      'circle_map_to_catalogue_max_lh_ratio':uJy/row.lens_flux_max_lh,'whole_cutout_to_circle_ratio':float(a.sum()/native),
      'artifact_excluded_circle_microJy':float(a[circle&~artifact].sum()*conversion),'convolved_circle_microJy':float(b[circle].sum()*conversion),'outside_circle_nonzero_pixels':int(np.count_nonzero(a[~circle]))})
 vis=next(x for x in sums if x['band']=='VIS');mapfrac=vis['unconvolved_circle_native']/Finf
 with ZipFile(ROOT/'euclid_eclipse_screen_2026_11_13/inputs/ECLIPSE_D_dr1_redshifts_and_physical_properties.zip') as z:
  sed=read_csv(io.TextIOWrapper(z.open('eclipse_dr1_catalogue_key_v20261103.csv')))
 sed=next(r for r in sed if r.unique_identifier=='EUCL-DR1-L014994')
 central={'sersic_shape_point':{'Re_geometric_arcsec':re,'Re_major_arcsec':re/np.sqrt(q),'n':n,'q':q,'PA_from_west_rad':phi,'center_west_arcsec':cx,'center_north_arcsec':cy,'I_eff_native_per_pixel':v('I_eff')},
          'modelling_circle':{'center_west_arcsec':maskx,'center_north_arcsec':masky,'radius_arcsec':radius,'included_pixel_centers':int(circle.sum())},
          'fraction_continuous_geometric_circle':f,'fraction_pixel_integrated_circle':f_pixels,'fraction_released_map_over_COoLEST_infinite_flux':mapfrac,
          'infinite_flux_COOLEST_VIS_native':float(Finf),'correction_total_over_aperture_continuous':1/f,'log10_mass_correction_continuous_dex':float(-np.log10(f)),
          'correction_total_over_aperture_released_map':1/mapfrac,'log10_mass_correction_released_map_dex':float(-np.log10(mapfrac)),
          'catalogue_logM_aperture':float(sed.eclipse_log_survived_mass_med),'catalogue_logM_error_lower':float(sed.eclipse_log_survived_mass_low),'catalogue_logM_error_upper':float(sed.eclipse_log_survived_mass_upp),
          'logM_infinite_if_constant_ML_continuous':float(sed.eclipse_log_survived_mass_med-np.log10(f)),'logM_infinite_if_constant_ML_released_map':float(sed.eclipse_log_survived_mass_med-np.log10(mapfrac)),
          'geometry_integral_abs_256_vs_512':abs(f-f512),'geometry_integral_abs_vs_adaptive':abs(f-fad),
          'pixel_vs_continuous_fraction_difference':f_pixels-f,'released_map_vs_pixel_model_fraction_difference':mapfrac-f_pixels}
 (out/'central.json').write_text(json.dumps(central,indent=2)+'\n');print(json.dumps({'central':central,'band_flux_checks':sums},indent=2),flush=True)
 # Exact published median and 1sigma endpoint sensitivity; covariance is absent.
 light=read_csv((I/'results/lens_sersic.csv').open())[0]
 median_n=light.sersic_index;median_re=light.effective_radius;e0=light.ell_comps_0;e1=light.ell_comps_1;medq=(1-np.hypot(e0,e1))/(1+np.hypot(e0,e1))
 # Pipeline phi=.5atan2(e0,e1), sky west/north reverses pipeline y.
 medphi=-.5*np.arctan2(e0,e1);medcx=light.centre_1;medcy=-light.centre_0
 fm=float(fraction(median_re,median_n,medq,medphi,medcx,medcy,maskx,masky,radius)[0])
 z=norm.ppf(qmc.Sobol(6,scramble=True,seed=20261113).random_base2(13));sens=[]
 def sample(name,Z):
  m=float(light[name]);lo=m-float(light[name+'_lower_1_sigma']);hi=float(light[name+'_upper_1_sigma'])-m
  return m+Z*np.where(Z<0,lo,hi)
 for corr in [-.9,0.,.9]:
  nn=sample('sersic_index',z[:,0]);rr=sample('effective_radius',corr*z[:,0]+np.sqrt(1-corr*corr)*z[:,1])
  ee0=sample('ell_comps_0',z[:,2]);ee1=sample('ell_comps_1',z[:,3]);qq=(1-np.hypot(ee0,ee1))/(1+np.hypot(ee0,ee1));angle=-.5*np.arctan2(ee0,ee1)
  xx=sample('centre_1',z[:,4]);yy=-sample('centre_0',z[:,5]);assert np.all((nn>0)&(rr>0)&(qq>0)&(qq<=1))
  ff=fraction(rr,nn,qq,angle,xx,yy,maskx,masky,radius,128)
  sens.append({'assumed_latent_correlation_n_Re':corr,'samples':len(ff),'fraction_quantiles':quant(ff),'log10_correction_quantiles':quant(-np.log10(ff))})
 result={'assertion_tested':'Determine constant-M/L infinite-Sersic normalization relative to ECLIPSE-D finite unconvolved modelling-circle flux for FOR J0332; verify against per-band released maps and flux table; show shape-summary sensitivity only.',
         'central':central,'band_flux_checks':sums,'catalogue_median_shape_fraction':fm,'catalogue_median_shape_log10_correction':float(-np.log10(fm)),
         'shape_summary_sensitivity':sens,'seconds':time.monotonic()-started,
         'primary_source':{'url':'https://eceb.astro.uni-bonn.de/public/dr1/nersesian.pdf','cached_pdf':'euclid_for_j0332_fit_2026_11_13/light_profile_audit/nersesian.pdf','sections':['3.1: total flux is unconvolved model summed within circular modelling mask','3.2: same finite-mask total flux feeds physical-property SED fit','6.1: flux outside mask and underestimated masses acknowledged']},
         'non_claims':['Correction assumes the same infinite single-Sersic shape and spatially constant stellar M/L adopted by the mass library.','No independent measurement of actual light or stellar mass in unobserved outer wings.','Shape-summary simulations are covariance sensitivity, not native joint shape uncertainty and not a joint mass/lensing refit.','Changing n/Re also changes the deflection field; do not apply f-only sensitivity as a complete image-fit uncertainty.','No SED refit, IMF change, spectroscopic-redshift transport or environmental correction is included.']}
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'median_shape_fraction':fm,'sensitivity':sens},indent=2),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)

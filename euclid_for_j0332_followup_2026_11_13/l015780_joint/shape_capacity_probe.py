"""Finite n/Re endpoint stress test with aperture normalization recomputed.
An independent orthogonal-projection necessary condition eliminates arbitrary
source centre and external shear. No continuous shape-box claim is made.
"""
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
from astropy.io import fits

ROOT=Path(__file__).resolve().parents[2]
B=Path(__file__).resolve().parent
I=B.parent/'l015780_inputs'
sys.path.insert(0,str(ROOT/'euclid_for_j0332_fit_2026_11_13'))
sys.path.insert(0,str(B.parent/'light_shapes'))
from aqual_lensing import make_field,projected_deflection,geometry
from fit_light_shapes import Renderer


def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 c=json.loads((B/'dynamics/run_01/central.json').read_text());a=c['aperture']
 rows=list(csv.DictReader((I/'results/lens_sersic.csv').open()));s=rows[0]
 raw=json.loads((I/'dataset/positions.json').read_text())['arguments']['values']['array']
 raw=np.asarray(raw);theta=np.column_stack([raw[:,1],-raw[:,0]])
 q,cx,cy,phi=[a[k] for k in ['q','center_west_arcsec','center_north_arcsec','phi_west_radians']]
 co,si=np.cos(phi),np.sin(phi);X,N=theta.T
 u=co*(X-cx)+si*(N-cy);v=-si*(X-cx)+co*(N-cy)
 info=a['mask'];yy,xx=np.indices((100,100));xx=(xx-49.5)*.1;yy=(yy-49.5)*.1
 mask=(xx-info['mask_centre'][1])**2+(yy+info['mask_centre'][0])**2<info['mask_radius']**2
 # Source-centre and both shear directions are nuisance columns.
 d1=np.column_stack([np.ones(4),np.zeros(4)]).ravel();d2=np.column_stack([np.zeros(4),np.ones(4)]).ravel()
 g1=np.column_stack([X,-N]).ravel();g2=np.column_stack([N,X]).ravel()
 T=np.column_stack([d1,d2,g1,g2]);Q=np.linalg.qr(T)[0];P=np.eye(8)-Q@Q.T
 assert np.max(abs(P@T))<1e-14
 assert np.max(abs(P@P-P))<1e-14
 yp=P@theta.ravel()
 scale,ratio=geometry(c['zl'],3.)
 specs=[('point',a['Re_geometric_arcsec'],a['n'])]
 for rn in ['lower','upper']:
  for nn in ['lower','upper']:
   specs.append((rn+'_Re_'+nn+'_n',float(s['effective_radius_'+rn+'_3_sigma']),float(s['sersic_index_'+nn+'_3_sigma'])))
 renderer=Renderer(np.ones((1,1)),fine=True);records=[]
 for name,re,n in specs:
  f=float(renderer.render(np.array([cx,cy,np.log(re/np.sqrt(q)),np.log(n),q,phi]))[mask].sum())
  for mass_errors in [0.,3.]:
   maperture=c['logM_aperture_SED_median']+mass_errors*c['SED_error_upper'];m=maperture-np.log10(f)
   for inc in [90.,50.]:
    qi=np.sqrt((q*q-np.cos(np.deg2rad(inc))**2)/np.sin(np.deg2rad(inc))**2)
    field=make_field(10**m,re/np.sqrt(q)*scale,n,qi,nr=320,nt=64)
    au,av=projected_deflection(field,u,v,inclination=inc,zl=c['zl'],zs=3.,nlos=256)
    alpha=np.column_stack([co*au-si*av,si*au+co*av])/ratio
    ap=P@alpha.ravel();beta=float(np.clip(yp@ap/(ap@ap),0,1.))
    residual=yp-beta*ap;sse=float(residual@residual)
    # For four vectors: centred SSE = (1/4) sum_pair separation² <=1.5 diameter².
    # Orthogonal projection cannot increase SSE. Thus diameter>=sqrt(SSE/1.5).
    bound=float(np.sqrt(sse/1.5))
    rec=dict(shape=name,n=n,Re_geometric_arcsec=re,aperture_fraction=f,
             mass_above_SED_median_in_upper_error_units=mass_errors,
             log10_aperture_mass=maperture,log10_total_mass=m,inclination=inc,
             beta_at_minimum_projected_SSE=beta,projected_SSE=sse,
             source_diameter_necessary_lower_bound_arcsec=bound,
             violates_point3_gate=bool(bound>.3),field_residual=field['residual'],
             deposited_mass_ratio=field['deposited_mass']/10**m)
    records.append(rec);print(json.dumps(rec),flush=True)
 result=dict(assertion_tested='Actual four-position association necessary condition at COOLEST point and four reported3sigma n/Re endpoint combinations, with fixed q/centre, two inclinations, median and+3upperSEDerror mass fixtures; beta<=1 and unbounded external shear',
             records=records,non_claims=['Finite endpoint tests do not bound the whole continuous shape region',
             'Reported shape endpoints are not a native joint probability contour','No external convergence or spatial M/L gradients',
             'Not a calibrated significance or full physical theory exclusion','Numerical field values are not interval-certified'])
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)

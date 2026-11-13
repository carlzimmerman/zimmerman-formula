"""Independent direct-field versus interpolated-field check near gate crossings."""
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
B=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'euclid_for_j0332_fit_2026_11_13'))
from aqual_lensing import make_field,projected_deflection,geometry

def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 f=np.load(B/'field_grid_01/positions_deflections.npz');X,N=f['theta_sky'];cx,cy=f['center'];phi=float(f['phi_west_to_north']);co,si=np.cos(phi),np.sin(phi)
 u=co*(X-cx)+si*(N-cy);v=-si*(X-cx)+co*(N-cy)
 re,n,q,zl=[float(f[k]) for k in ['re_geom_arcsec','n','q_projected','zl']];scale,ratio=geometry(zl,3.)
 # Candidate transitions from the preceding pair-capacity exploration;
 # these values choose independent numerical evaluation points, not priors.
 cases=[(90.,12.1806966),(60.,12.1879328),(50.,12.1986599),
        (90.,12.1097616),(60.,12.1177009),(50.,12.1293085),
        (90.,11.926878886134908)]
 records=[];direct=[]
 for inc,m in cases:
  j=int(np.where(f['inclination']==inc)[0][0]);k=int(np.searchsorted(f['logmass'],m)-1);frac=(m-f['logmass'][k])/(f['logmass'][k+1]-f['logmass'][k])
  interp=(1-frac)*f['alpha_hat_sky'][j,k]+frac*f['alpha_hat_sky'][j,k+1]
  qi=np.sqrt((q*q-np.cos(np.deg2rad(inc))**2)/np.sin(np.deg2rad(inc))**2)
  field=make_field(10**m,re/np.sqrt(q)*scale,n,qi,nr=320,nt=64)
  au,av=projected_deflection(field,u,v,inclination=inc,zl=zl,zs=3.,nlos=256)
  exact=np.stack([co*au-si*av,si*au+co*av])/ratio;direct.append(exact)
  delta=exact-interp
  error=float(np.max(np.linalg.norm(delta,axis=0)/np.linalg.norm(exact,axis=0)))
  # For any beta<=1, any shear and kappa, pair differences change by
  # <= max_ij|delta_alpha_i-delta_alpha_j|. This bounds the change of
  # the optimized minimum diameter on the same nuisance parameter domain.
  pair=float(np.max(np.linalg.norm(delta[:,:,None]-delta[:,None,:],axis=0)))
  assert error<.001 and pair<.003
  records.append(dict(inclination=inc,logmass=m,interpolation_max_relative_vector_error=error,
                      maximum_pair_deflection_difference_arcsec=pair,field_residual=field['residual']))
  print(json.dumps(records[-1]),flush=True)
 np.savez_compressed(out/'direct_fields.npz',cases=np.array(cases),alpha_hat_sky=np.array(direct),theta_sky=f['theta_sky'])
 (out/'result.json').write_text(json.dumps(dict(assertion_tested='Direct nonlinear fields versus linear-mass-grid interpolation at seven finite points; pair-deflection norm bounds sensitivity of the source-diameter objective for beta<=1',records=records,
    non_claims=['No continuum interpolation error theorem','No certification of floating PDE solution','No new model or stellar-mass posterior']),indent=2)+'\n')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)

"""Combine conditional capacity floors with existing stellar/dynamics scans.
Tail integrals are conditional mass-distribution summaries, not theory p-values.
"""
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'geometry_audit'))
from capacity import capacity,exact_null_basis

def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 g=json.loads((HERE/'geometry_audit/run_01/result.json').read_text())
 d=json.loads((HERE/'dynamics/run_01/result.json').read_text());c=d['central']
 rows=list(csv.DictReader((HERE/'dynamics/run_01/mass_scan.csv').open()))
 scan={k:np.array([float(r[k]) for r in rows]) for k in rows[0]};x=scan['log10_total_mass']
 recs=[]
 for r in g['interpolated_gate_crossings']:
  m=r['interpolated_gate_crossing_logmass'];ma=m+np.log10(c['aperture']['fraction_pixel_union'])
  scenarios=[]
  for s in d['scenarios']:
   beta,seeing=s['beta'],s['seeing_fwhm_arcsec'];key=f'beta{beta}_seeing{seeing}'
   sigma=float(np.interp(m,x,scan['sigma_'+key]))
   tails={}
   for version in ['v21','v30']:
    density=scan[version+'_posterior_'+key];density=density/np.trapz(density,x)
    cdf=cumulative_trapezoid(density,x,initial=0)
    tails[version]=max(0.,float(1-np.interp(m,x,cdf)))
   scenarios.append(dict(beta_anisotropy=beta,seeing_FWHM_arcsec=seeing,
        sigma_at_lensing_mass_kms=sigma,
        observed_v21_error_units=(sigma-c['observations']['v21']['sigma'])/c['observations']['v21']['error'],
        conditional_SED_plus_spherical_dynamics_mass_tail=tails))
  recs.append(dict(inclination=r['inclination'],geometry_cap_name=r['geometry_cap_name'],
       interpolated_log10_total_mass=m,log10_aperture_mass=ma,
       total_mass_Msun=10**m,aperture_mass_Msun=10**ma,
       required_mass_over_SED_median=10**(m-c['logM_infinite_SED_median']),
       offset_in_quoted_upper_SED_error_units=(m-c['logM_infinite_SED_median'])/c['SED_error_upper'],
       certified_scanned_mass_bracket=r['field_mass_bracket'],scenarios=scenarios))
 # Use separately solved fields at the interpolated roots, so the actual
 # finite PDE solve checks the source-position calculation at those masses.
 f=np.load(HERE/'interpolation_check_01/direct_fields.npz');theta=f['theta_sky'].T;basis=exact_null_basis(theta)
 direct=[]
 for k,((inc,m),alpha) in enumerate(zip(f['cases'],f['alpha_hat_sky'])):
  caps=[g['beta_infinity']] if k<3 else [1.] if k<6 else [g['beta_infinity'],1.]
  for cap in caps:
   rr=capacity(theta,alpha.T,cap,.3,basis)
   direct.append(dict(inclination=float(inc),logmass=float(m),beta_max=cap,
        minimum_source_diameter_arcsec=rr['minimum_diameter_primal_arcsec'],
        numerical_dual_lower_bound_arcsec=rr['dual_lower_bound_arcsec'],
        primal_dual_gap_arcsec=rr['primal_dual_gap_arcsec']))
 result=dict(assertion_tested='Conditional lensing source-capacity mass requirements mapped into same-aperture SED and spherical DESI dynamical constraints; independently solved fields evaluated at interpolation crossings',
       aperture_fraction=c['aperture']['fraction_pixel_union'],SED_aperture_logmass=c['logM_aperture_SED_median'],
       SED_infinite_logmass=c['logM_infinite_SED_median'],lensing_mass_requirements=recs,
       direct_field_capacity_checks=direct,non_claims=[
       'Conditional posterior-tail integrals are not theory p-values or calibrated discovery significance',
       'Spherical dynamics is not the same as the flattened rotating lens; all anisotropy/seeing cases are fixtures',
       'Interpolated roots are approximate, brackets and direct checks retain their finite scopes',
       'No environmental-convergence measurement; a zero-convergence result does not exclude the full theory',
       'No joint image/SED/kinematic data likelihood or full physical systematic marginalization'])
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 for r in recs:
  print(json.dumps({k:v for k,v in r.items() if k!='scenarios'}),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)

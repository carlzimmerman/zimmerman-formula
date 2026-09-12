#!/usr/bin/env python3
"""Fixed-a0 DF2 field/virial study; no tuned halo and no empirical PASS flag."""
import argparse
import json
from pathlib import Path
import sys
import time
import numpy as np
import sympy as sp

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from solver import solve,invert_mu,mu,spherical_virial,jacobian_check
from stellar.profile import Sersic,aperture_second_moment

A0=9.3619e-11
G=6.67430e-11
MSUN=1.98847e30
KPC=3.085677581491367e19


def geometry(df2_distance,host_distance,host_mass=1e11,mass_to_light=2.):
    data=json.loads((HERE/'data/inputs.json').read_text())
    coords=data['coordinates']
    ra1,dec1=np.deg2rad([coords['df2']['ra_deg'],coords['df2']['dec_deg']])
    ra2,dec2=np.deg2rad([coords['ngc1052']['ra_deg'],coords['ngc1052']['dec_deg']])
    cos_angle=np.sin(dec1)*np.sin(dec2)+np.cos(dec1)*np.cos(dec2)*np.cos(ra1-ra2)
    angle=np.arccos(np.clip(cos_angle,-1,1))
    separation=np.sqrt((host_distance-df2_distance)**2+
                       2*host_distance*df2_distance*(1-cos_angle))*1000
    cos_los=(host_distance*cos_angle-df2_distance)*1000/separation
    phot=data['projected_stellar_profile']
    re=phot['effective_radius_major_arcsec']/206264.80624709636*df2_distance*1000*np.sqrt(phot['axis_ratio_projected'])
    norm=data['stellar_normalization']
    mass=norm['luminosity_V_Lsun']*mass_to_light*(df2_distance/norm['reference_distance_Mpc'])**2
    eta=G*mass*MSUN/(A0*(re*KPC)**2)
    external_newtonian=G*host_mass*MSUN/(A0*(separation*KPC)**2)
    external=float(invert_mu(external_newtonian))
    return dict(df2_distance_Mpc=df2_distance,host_distance_Mpc=host_distance,
                separation_kpc=float(separation),angular_separation_arcmin=float(np.rad2deg(angle)*60),
                los_cosine=float(cos_los),stellar_mass_Msun=mass,circularized_Re_kpc=float(re),
                eta=float(eta),a0_m_s2=A0,host_mass_Msun=host_mass,mass_to_light_V=mass_to_light,
                external_Newtonian_over_a0=float(external_newtonian),external_over_a0=external,
                host_uniformity_Re_over_separation=float(re/separation),
                host_mass_status='fixed sensitivity assumption, not a measured mass posterior',
                rho_Lambda_status='a0 input, no per-galaxy vacuum-density adjustment')


def dimensional_result(result,geo):
    factor=A0*geo['circularized_Re_kpc']*KPC/1e6
    c=geo['los_cosine']
    los=(1-c*c)*result['virial_perpendicular']+c*c*result['virial_parallel']
    return dict(sigma_global_los_km_s=float(np.sqrt(los*factor)),
                sigma_global_perpendicular_km_s=float(np.sqrt(result['virial_perpendicular']*factor)),
                sigma_global_parallel_km_s=float(np.sqrt(result['virial_parallel']*factor)))


def symbolic_checks():
    y=sp.symbols('y',positive=True)
    primitive=y*y+2*(1+y)*sp.exp(-y)-2
    checks={'primitive_derives_mu':sp.simplify(sp.diff(primitive,y)/(2*y)-(1-sp.exp(-y)))==0}
    x,z=sp.symbols('x z',real=True)
    radius=sp.sqrt(x*x+z*z)
    vec=sp.Matrix([x,z]);flux=(1-sp.exp(-radius))*vec
    expected=(1-sp.exp(-radius))*sp.eye(2)+sp.exp(-radius)/radius*(vec*vec.T)
    checks['flux_jacobian_from_variation']=all(sp.simplify(v)==0 for v in flux.jacobian(vec)-expected)
    checks['parallel_principal']=sp.simplify((1-sp.exp(-y)+y*sp.exp(-y))-(1+(y-1)*sp.exp(-y)))==0
    assert all(checks.values())
    return checks


def efd_reference(eta,external):
    mm=float(mu(external));L=external*np.exp(-external)/mm;k=np.sqrt(L)
    base=np.pi*eta/32
    return (base*3*((1+k*k)*np.arctan(k)-k)/(2*mm*k**3),
            base*3*(k-np.arctan(k))/(mm*k**3))


def run(fine_nr=97):
    started=time.perf_counter()
    profile=Sersic(.6)
    coarse_nr=(fine_nr+1)//2
    cases=[]
    # Alternative distance methods are scenarios, not independent posterior draws.
    definitions=[('JWST_DF2_SBF_host',17.6,21.3),
                 ('JWST_DF2_PNLF_host',17.6,17.9),
                 ('close_association_control',17.6,17.6),
                 ('legacy_20Mpc_association',20.,20.)]
    for label,dd,dh in definitions:
        geo=geometry(dd,dh)
        fields=[]
        for nr in (coarse_nr,fine_nr):
            field=solve(geo['eta'],geo['external_over_a0'],nr=nr,nz=2*nr-1,profile=profile)
            field.update(dimensional_result(field,geo));fields.append(field)
        if label in ('JWST_DF2_SBF_host','close_association_control'):
            # Preserve approximate central spacing when doubling outer extent.
            extent=2*fields[-1]['extent']
            nr=round((fine_nr-1)*np.arcsinh(extent)/np.arcsinh(fields[-1]['extent']))+1
            domain=solve(geo['eta'],geo['external_over_a0'],nr=nr,nz=2*nr-1,extent=extent,profile=profile)
            domain.update(dimensional_result(domain,geo))
        else:domain=None
        row=dict(label=label,geometry=geo,field_refinement=fields,domain_extension=domain,
                 refinement_relative_sigma=abs(fields[0]['sigma_global_los_km_s']/fields[1]['sigma_global_los_km_s']-1))
        cases.append(row)
        print(json.dumps(dict(label=label,separation_kpc=geo['separation_kpc'],
              external=geo['external_over_a0'],global_los_km_s=fields[-1]['sigma_global_los_km_s'],
              residual=fields[-1]['residual_relative'],refinement=row['refinement_relative_sigma'])),flush=True)
    benchmarks=[]
    for label,eta,e,newt in [('newtonian',.06,.1,True),('isolated',.06,0.,False),('linear_EFD',1e-5,.5,False)]:
        out=solve(eta,e,nr=fine_nr,nz=2*fine_nr-1,extent=32,newtonian=newt)
        expected=efd_reference(eta,e) if label=='linear_EFD' else (spherical_virial(eta,newt),)*2
        out.update(label=label,analytic_perpendicular=expected[0],analytic_parallel=expected[1],
                   error_perpendicular=out['virial_perpendicular']/expected[0]-1,
                   error_parallel=out['virial_parallel']/expected[1]-1)
        benchmarks.append(out)
    geo=cases[0]['geometry'];factor=A0*geo['circularized_Re_kpc']*KPC/1e6
    aperture=[]
    for mass_to_light in (1.,2.,4.):
        g=geometry(17.6,21.3,mass_to_light=mass_to_light)
        for law in ('newtonian','aqual'):
            for radius in (.5,1.,1.5,np.inf):
                moment=aperture_second_moment(profile,g['eta'],radius,law)
                aperture.append(dict(mass_to_light=mass_to_light,law=law,
                       aperture_Re='global' if np.isinf(radius) else radius,
                       sigma_km_s=float(np.sqrt(factor*moment))))
    all_fields=[f for c in cases for f in c['field_refinement']+([c['domain_extension']] if c['domain_extension'] else [])]+benchmarks
    checks=dict(all_nonlinear_solves_converged=all(f['converged'] for f in all_fields),
                benchmark_virial_errors_below_one_percent=all(max(abs(b['error_perpendicular']),abs(b['error_parallel']))<.01 for b in benchmarks),
                mesh_sigma_changes_below_one_percent=all(c['refinement_relative_sigma']<.01 for c in cases),
                domain_sigma_changes_below_one_percent=all(abs(c['domain_extension']['sigma_global_los_km_s']/c['field_refinement'][-1]['sigma_global_los_km_s']-1)<.01 for c in cases if c['domain_extension']),
                global_a0_unchanged=all(c['geometry']['a0_m_s2']==A0 for c in cases))
    result=dict(status='conditional_static_diagnostic_not_same_relativistic_action_closure',
                kernel='mu(x)=1-exp(-x), x=physical_total_gradient/a0; not the separate empirical RAR nu function',
                symbolic_checks=symbolic_checks(),jacobian_check=jacobian_check(),
                numerical_checks=checks,cases=cases,benchmarks=benchmarks,
                isolated_spherical_circular_apertures=aperture,
                empirical_likelihood=None,empirical_pass=None,
                non_claims=['No derivation from relativistic P/W/gamma action.',
                 'Global virial moments are necessary equilibrium moments, not existence of a positive stellar distribution function.',
                 'Isolated isotropic circular apertures are not the actual KCWI/MUSE masks and are not external-field aperture predictions.',
                 'The host-only uniform field omits other environmental sources, tides and dynamical history.',
                 'Host mass, spherical deprojection and stellar M/L are declared assumptions, not fitted likelihood parameters.',
                 'Central distance-method scenarios do not encode a joint distance posterior.',
                 'No kappa derivation, CMB, lensing or relativistic DOF certificate.'],
                runtime_seconds=time.perf_counter()-started)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--fine-nr',type=int,default=97)
    args=parser.parse_args()
    result=run(args.fine_nr)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(numerical_checks=result['numerical_checks'],runtime=result['runtime_seconds']),indent=2))
    raise SystemExit(0 if all(result['numerical_checks'].values()) else 1)

"""Fixed-mass a0 sensitivity, NOT a mass-profiled gravity likelihood ratio."""
import argparse,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from run_jeans_v4 import make_model,astrometry,TARGET,ROOT
from aqual_lensing import make_field,projected_deflection,geometry


def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    fit=json.loads((TARGET/'aqual_host/operator_01/run_04/result.json').read_text())
    light=np.array(fit['light']);mass=fit['ss6_mass_msun'];scale,_=geometry(.32022095721117494,1.210)
    shape=dict(center_west_arcsec=float(light[0]),center_north_arcsec=float(light[1]),
               Re_major_arcsec=float(np.exp(light[2])),n=float(np.exp(light[3])),q=float(light[4]),
               PA_from_west_deg=float(np.rad2deg(light[5])))
    astro=astrometry(shape);offset=np.array(astro['relative_major_minor_arcsec'])*scale
    records=[];fields={}
    for label,factor,mfactor,newton in [('Newton_stars_only',1.,1.,True),('a0_half',.5,1.,False),
                                      ('a0_fixed',1.,1.,False),('a0_twice',2.,1.,False),
                                      ('homology_double_mass_a0',2.,2.,False)]:
        f=make_field(mass*mfactor,np.exp(light[2])*scale,np.exp(light[3]),light[4],
                     a0=9.3603e-11*factor,nr=320,nt=64,mu_one=newton)
        g=f['grid'];file=out/(label+'_field.npz')
        np.savez_compressed(file,xc=g.xc,tc=g.tc,gr=f['gr'],gt=f['gt'],phi=f['phi'],
                            logmass=np.log10(mass*mfactor),light=light,zl=.32022095721117494,
                            zs=1.210,a0=f['a0'],mu_one=newton)
        j=make_model(file)
        aperture=j.aperture(.75*scale,1.2/2.354820045*scale,offset=offset,bs=[1.])
        u=np.array([.2,.5,1.,2.,3.,0.,0.,0.,0.,0.]);v=np.array([0.,0.,0.,0.,0.,.2,.5,1.,2.,3.])
        au,av=projected_deflection(f,u,v,zl=.32022095721117494,zs=1.210,nlos=192)
        record=dict(label=label,mass_msun=mass*mfactor,a0_m_s2=f['a0'],mu_one=newton,
                    field_residual=f['residual'],deposited_mass_fraction=f['deposited_mass']/f['mass'],
                    aperture=aperture,deflection_probes=dict(u=u.tolist(),v=v.tolist(),au=au.tolist(),av=av.tolist()))
        records.append(record);fields[label]=f;print(json.dumps(record),flush=True)
    base=fields['a0_fixed'];double=fields['homology_double_mass_a0']
    homology=max(float(np.max(abs(double[k]-2*base[k]))/np.max(abs(2*base[k]))) for k in ['phi','gr','gt'])
    b=records[2]['aperture']['raw_second_moment_kms2'][0];d=records[4]['aperture']['raw_second_moment_kms2'][0]
    assert homology<1e-5 and abs(d/(2*b)-1)<1e-5,(homology,d/(2*b)-1)
    result=dict(records=records,physical_light=shape,astrometry=astro,
                homology_max_array_relative=homology,homology_second_moment_relative=d/(2*b)-1,
                assertion_tested='Fixed stellar mass/shape a0 sensitivity of same-field lensing probes and aperture moments; finite homology numerical control.',
                non_claims=['No refit of mass or foreground for alternate a0; no statistical preference or Bayes factor.',
                            'Newton stars-only is a diagnostic, not a fit of dark-matter cosmology.',
                            'No full screened theory, environment, observed seeing or DF verification.'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)

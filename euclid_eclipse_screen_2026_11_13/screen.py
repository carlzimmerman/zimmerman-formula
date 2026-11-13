"""Reproducible ECLIPSE availability and a0-sensitivity SCREEN, not a theory fit.

Uses an isolated spherical, stellar-only, unscreened simple-mu diagnostic.
Sersic 3D mass uses the explicitly approximate Lima Neto et al. prescription.
No generic isothermal lens mass is treated as a measured baryonic mass.
"""
import argparse
import io
import json
import math
from functools import lru_cache
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.special import gammainc, gammaincinv, ellipe, gammaln

ROOT = Path(__file__).resolve().parent
G, C, MSUN, MPC = 6.67430e-11, 299792458.0, 1.98847e30, 3.085677581491367e22
ARCSEC = np.pi / (180 * 3600)
A0 = 9.3603e-11
A0_ALT = 1.1312e-10
H0, OM = 67.74, 0.3089  # ECLIPSE-D fiducial distance convention ONLY.


@lru_cache(maxsize=10000)
def distance(z):
    """Angular diameter distance; flat fiducial cosmology, not a DE measurement."""
    if not np.isfinite(z) or z <= 0:
        return np.nan
    chi = C / (H0 * 1000 / MPC) * quad(
        lambda x: 1 / np.sqrt(OM * (1+x)**3 + 1-OM), 0, z,
        epsabs=1e-10, epsrel=1e-10)[0]
    return chi / (1+z)


def nodes(order):
    x, w = np.polynomial.legendre.leggauss(order)
    t = (x + 1) * np.pi / 4
    return 1 / np.cos(t), w * np.pi / 4


def fraction_ps(x, n):
    p = 1 - 0.6097 / n + 0.05463 / n**2
    return gammainc(n*(3-p), gammaincinv(2*n, 0.5) * x**(1/n))


def diagnostics(mass, radius, re, n, a0=A0, order=128):
    """Broadcast arrays; unreduced deflection at fixed R and its log derivative."""
    mass, radius, re, n = [np.atleast_1d(np.asarray(x, float)) for x in (mass, radius, re, n)]
    sec, w = nodes(order)
    r = radius[:, None] * sec
    mfrac = fraction_ps(r / re[:, None], n[:, None])
    gn = G * mass[:, None] * mfrac / r**2
    g = 0.5 * (gn + np.sqrt(gn**2 + 4*a0*gn))
    sg = 0.5 * (1-np.sqrt(gn/(gn+4*a0)))
    terms = g * sec * w
    alpha = 4*radius/C**2 * terms.sum(axis=1)
    sensitivity = (terms*sg).sum(axis=1) / terms.sum(axis=1)
    gn_R = G*mass*fraction_ps(radius/re, n)/radius**2
    return alpha, sensitivity, gn_R/a0


def exact_mass_fraction(x, n):
    """Independent Abel-deprojection integral, not the approximation used to rank."""
    b = gammaincinv(2*n, .5)
    t0 = b*x**(1/n)
    shape = 2*n+1
    def integrand(t):
        u = min(1., (t0/t)**n)
        # Stable small-u expansion of asin(u)-u sqrt(1-u^2).
        bracket = (2*u**3/3 + u**5/5 + 3*u**7/28) if u < .01 else (
            np.arcsin(u)-u*np.sqrt(max(0.,1-u*u)))
        return (2/np.pi)*bracket*np.exp((shape-1)*np.log(t)-t-gammaln(shape))
    return gammainc(shape,t0) + quad(integrand,t0,np.inf,epsabs=1e-9,epsrel=1e-7)[0]


def validate_numerics():
    checks = {}
    # Point mass: quadrature agrees with independent complete elliptic expression.
    errors=[]; fd=[]
    sec,w=nodes(256)
    for y in [.01,.1,1,10,100,1000]:
        gn=y/sec**2
        g=(gn+np.sqrt(gn*gn+4*gn))/2
        boost=np.sum(g*sec*w)/y
        exact=.5*(1+np.sqrt(1+4/y)*ellipe(1/(1+4/y)))
        errors.append(abs(boost/exact-1))
        s=np.sum(g*sec*w*.5*(1-np.sqrt(gn/(gn+4))))/np.sum(g*sec*w)
        h=1e-5
        aa=[]
        for a in [np.exp(-h),np.exp(h)]:
            gg=.5*(gn+np.sqrt(gn*gn+4*a*gn));aa.append(np.sum(gg*sec*w))
        fd.append(abs((np.log(aa[1])-np.log(aa[0]))/(2*h)-s))
    checks['point_mass_max_relative_error']=max(errors)
    checks['sensitivity_max_fd_error']=max(fd)
    assert max(errors)<1e-8 and max(fd)<1e-7
    # Validate the approximate mass against independent Abel deprojection over a grid.
    errs=[]
    for n in [.6,1,2,4,6,8,9.8]:
        for x in [.05,.1,.3,1,3,10,30]:
            exact=exact_mass_fraction(x,n)
            approx=float(fraction_ps(x,n))
            errs.append({'n':n,'r_over_re':x,'relative_mass_error':approx/exact-1})
    checks['mass_approximation_grid']=errs
    checks['mass_approximation_max_abs_relative_error']=max(abs(x['relative_mass_error']) for x in errs)
    return checks


def read_inputs():
    inp=ROOT/'inputs'
    with ZipFile(inp/'ECLIPSE_object_catalogue.zip') as z:
        obj=pd.read_csv(z.open('ECLIPSE_object_catalogue/ECLIPSE_object_catalogue.csv'),low_memory=False)
    with ZipFile(inp/'ECLIPSE_D_dr1_redshifts_and_physical_properties.zip') as z:
        sed=pd.read_csv(z.open('eclipse_dr1_catalogue_key_v20261103.csv'),low_memory=False)
    with ZipFile(inp/'ECLIPSE_lens_models.zip') as z:
        with ZipFile(io.BytesIO(z.read('ECLIPSE_lens_models/catalogue_csvs.zip'))) as zz:
            models=pd.read_csv(zz.open('dr1_catalogue_v5_full/csv/dr1_catalogue_15072_master.csv'),low_memory=False)
    assert len(obj)==26662 and len(sed)==15072 and len(models)==15072
    for df,key in [(obj,'Unique_Identifier'),(sed,'unique_identifier'),(models,'unique_identifier')]:
        assert df[key].is_unique and df[key].notna().all()
    # Numerical -99 sentinel is missing; never zero-fill missing data.
    for df in [sed,models]:
        num=df.select_dtypes(include=np.number).columns
        df[num]=df[num].mask(df[num]==-99)
    d=obj.merge(sed,left_on='Unique_Identifier',right_on='unique_identifier',validate='one_to_one')
    fields=['unique_identifier','lens_light_ell_comps_0','lens_light_ell_comps_1',
            'mass_shear_gamma_1','mass_shear_gamma_2','tile_id','vis_pix_completed',
            'double_source_plane_lens_votes','multi_galaxy_lens_votes']
    d=d.merge(models[fields],on='unique_identifier',validate='one_to_one')
    assert len(d)==15072
    return obj,d


def slacs_overlap(obj):
    """Reproduce the bounded 85-object external-catalogue overlap search."""
    path=ROOT/'inputs'/'external_slacs_auger2009.tsv'
    lines=[x for x in path.read_text().splitlines() if x and not x.startswith('#')]
    table=pd.read_csv(io.StringIO('\n'.join([lines[0]]+lines[3:])),sep='\t')
    assert len(table)==85
    def sexagesimal(s,ra=False):
        vals=str(s).strip().split()
        sign=-1 if vals[0].startswith('-') else 1
        a,b,c=map(float,vals)
        return sign*(abs(a)+b/60+c/3600)*(15 if ra else 1)
    ra=np.deg2rad(obj.RA_obj.to_numpy());dec=np.deg2rad(obj.DEC_obj.to_numpy())
    xyz=np.array([np.cos(dec)*np.cos(ra),np.cos(dec)*np.sin(ra),np.sin(dec)]).T
    rows=[]
    for _,r in table.iterrows():
        ar,dr=np.deg2rad([sexagesimal(r.RAJ2000,True),sexagesimal(r.DEJ2000)])
        v=np.array([np.cos(dr)*np.cos(ar),np.cos(dr)*np.sin(ar),np.sin(dr)])
        chord=np.linalg.norm(xyz-v,axis=1);j=int(np.argmin(chord))
        sep=2*np.arcsin(min(1,chord[j]/2))/ARCSEC
        rows.append({'slacs_name':r.SDSS,'nearest_eclipse_id':obj.iloc[j].Unique_Identifier,
                     'separation_arcsec':sep,'within_10arcsec':sep<=10})
    return pd.DataFrame(rows)


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    obj,d=read_inputs()
    slacs=slacs_overlap(obj)
    validation=validate_numerics()
    e=np.hypot(d.lens_light_ell_comps_0,d.lens_light_ell_comps_1)
    d['axis_ratio_proxy']=(1-e)/(1+e)
    d['external_shear_amplitude']=np.hypot(d.mass_shear_gamma_1,d.mass_shear_gamma_2)
    # Leave the published non-circularized Re intact in baseline; sqrt(q) variant
    # is explicitly a shape-bracketing diagnostic, not a 3D shape reconstruction.
    d['distance_photoz_m']=d.eclipse_median_phz.map(distance)
    d['einstein_radius_kpc_proxy']=d.eclipse_effective_einstein_radius*ARCSEC*d.distance_photoz_m/(MPC/1000)
    d['effective_radius_kpc_proxy']=d.eclipse_effective_radius*ARCSEC*d.distance_photoz_m/(MPC/1000)
    d['ssfr_proxy']=d.eclipse_sfr_med / 10**d.eclipse_log_survived_mass_med
    valid=(d.eclipse_log_survived_mass_med.between(8,14) &
           d.eclipse_sersic_index.between(.6,10) &
           (d.eclipse_effective_radius>0) & (d.eclipse_effective_einstein_radius>0) &
           d.eclipse_median_phz.between(.01,4))
    d['numerically_rankable']=valid
    idx=d.index[valid]
    mass=10**d.loc[idx,'eclipse_log_survived_mass_med'].to_numpy()*MSUN
    radius=d.loc[idx,'einstein_radius_kpc_proxy'].to_numpy()*MPC/1000
    re=d.loc[idx,'effective_radius_kpc_proxy'].to_numpy()*MPC/1000
    n=d.loc[idx,'eclipse_sersic_index'].to_numpy()
    alpha,s,y=diagnostics(mass,radius,re,n)
    d.loc[idx,'alpha_unreduced_arcsec_proxy']=alpha/ARCSEC
    d.loc[idx,'S_alpha_proxy']=s
    d.loc[idx,'gN_RE_over_a0_proxy']=y
    for label,factor in [('half',.5),('double',2),('alt',A0_ALT/A0)]:
        aa,ss,_=diagnostics(mass,radius,re,n,A0*factor)
        d.loc[idx,'deflection_fraction_'+label+'_a0']=aa/alpha-1
        if label=='alt':d.loc[idx,'S_alpha_alt_proxy']=ss
    # 256-node convergence, derivative and fixed-mass monotonicity check all rows.
    a256,s256,_=diagnostics(mass,radius,re,n,order=256)
    validation['all_ranked_max_relative_quadrature_error']=float(np.max(abs(a256/alpha-1)))
    validation['all_ranked_max_sensitivity_quadrature_error']=float(np.max(abs(s256-s)))
    assert validation['all_ranked_max_relative_quadrature_error']<2e-5
    assert np.all((s>=0)&(s<=.5))
    d.loc[idx,'mass_error_dex_conditional']=np.maximum(
        d.loc[idx,'eclipse_log_survived_mass_low'],d.loc[idx,'eclipse_log_survived_mass_upp'])
    d.loc[idx,'mass_only_sigma_ln_a0_proxy']=(1-s)/s*np.log(10)*d.loc[idx,'mass_error_dex_conditional']
    d.loc[idx,'imf_0p2dex_equivalent_ln_a0']=(1-s)/s*np.log(10)*.2
    q=d.loc[idx,'axis_ratio_proxy'].to_numpy()
    shape_ok=np.isfinite(q)&(q>0)&(q<=1)
    ac,sc,_=diagnostics(mass[shape_ok],radius[shape_ok],re[shape_ok]*np.sqrt(q[shape_ok]),n[shape_ok])
    d.loc[idx[shape_ok],'S_alpha_circularized_proxy']=sc
    d.loc[idx[shape_ok],'radius_convention_deflection_fraction']=ac/alpha[shape_ok]-1
    for label,fac in [('lower_imf',10**(-.25)),('higher_mass',10**.2)]:
        _,st,_=diagnostics(mass*fac,radius,re,n)
        d.loc[idx,'S_alpha_'+label+'_proxy']=st
    d['strict_photometry_model_quality']=(valid & d.final_sample & d.lens_model_success &
        (d.Expert_Grade=='A') & ~d.large_system_warning & ~d.disc_deflector)
    d['simple_geometry_priority']=(d.strict_photometry_model_quality &
        (d.axis_ratio_proxy>=.7)&(d.external_shear_amplitude<.1)&
        (d.eclipse_sersic_index<9.5)&(d.ssfr_proxy<1e-11))
    d['lens_specz_available']=d.desi_deflector_specz.notna()
    d['lens_photo_spec_delta_normalized']=abs(d.desi_deflector_specz-d.eclipse_median_phz)/(1+d.desi_deflector_specz)
    d['raw_sensitivity_bin']=np.select([d.S_alpha_proxy>=.1,d.S_alpha_proxy>=.05,d.S_alpha_proxy.notna()],
                                     ['stronger','intermediate','weak'],default='not_computed')
    # External source-z is never manufactured from a portal placeholder.
    ext=ROOT/'external_verified_redshifts.csv'
    if ext.exists():
        pairs=pd.read_csv(ext)
        pairs=pairs.rename(columns={'Unique_Identifier':'unique_identifier',
                                    'z_lens':'z_lens_verified','z_source':'z_source_verified'})
        # Published provisional/photo-z pairs remain visible but do not count as
        # independently verified spectroscopic geometry.
        pairs['external_pair_verified']=pairs.status.eq('verified_pair')
        d=d.merge(pairs,on='unique_identifier',how='left',validate='one_to_one')
    else:
        for col in ['external_name','z_lens_verified','z_source_verified','reference_url']:
            d[col]=np.nan
        d['external_pair_verified']=False
    d['verified_pair_available']=d.external_pair_verified.fillna(False)&(pd.to_numeric(d.z_lens_verified,errors='coerce')>0)&(
        pd.to_numeric(d.z_source_verified,errors='coerce')>pd.to_numeric(d.z_lens_verified,errors='coerce'))
    d['pair_photo_spec_delta_normalized']=abs(pd.to_numeric(d.z_lens_verified,errors='coerce')-d.eclipse_median_phz)/(1+pd.to_numeric(d.z_lens_verified,errors='coerce'))
    d['source_geometry_ratio']=np.nan
    d['alpha_over_thetaE_proxy_at_photo_mass']=np.nan
    for i,row in d[d.verified_pair_available & d.numerically_rankable].iterrows():
        zl,zs=float(row.z_lens_verified),float(row.z_source_verified)
        ratio=1-distance(zl)*(1+zl)/(distance(zs)*(1+zs))
        dl=distance(zl)
        args=(10**row.eclipse_log_survived_mass_med*MSUN,
              row.eclipse_effective_einstein_radius*ARCSEC*dl,
              row.eclipse_effective_radius*ARCSEC*dl,row.eclipse_sersic_index)
        ap,sp,_=diagnostics(*args)
        d.loc[i,'source_geometry_ratio']=ratio
        d.loc[i,'S_alpha_at_verified_z_photo_mass']=float(sp[0])
        d.loc[i,'alpha_over_thetaE_proxy_at_photo_mass']=float(ap[0]*ratio/(row.eclipse_effective_einstein_radius*ARCSEC))
    # Availability tier, not a scientific pass/fail or statistical detection.
    d['availability_tier']='missing_source_redshift_or_external_match'
    d.loc[d.verified_pair_available,'availability_tier']='paired_redshifts_needs_mass_or_image_work'
    trial=(d.verified_pair_available & d.strict_photometry_model_quality &
           (d.pair_photo_spec_delta_normalized<.02)&(d.S_alpha_proxy>=.05))
    d.loc[trial,'availability_tier']='candidate_for_dedicated_forward_fit'
    # Every parent A/B row retained, including exclusions and missing-data reason.
    d.to_csv(out/'screen_all_15072.csv',index=False)
    pairs=d[d.verified_pair_available].sort_values('S_alpha_proxy',ascending=False)
    pairs.to_csv(out/'verified_redshift_candidates.csv',index=False)
    d[d.status.notna()].to_csv(out/'named_targets.csv',index=False)
    slacs.to_csv(out/'slacs_overlap.csv',index=False)
    shortlist=d[d.strict_photometry_model_quality].sort_values(
        ['lens_specz_available','simple_geometry_priority','S_alpha_proxy'],ascending=False)
    shortlist.head(30).to_csv(out/'followup_shortlist.csv',index=False)
    counters={
        'parent_objects':len(obj),'grade_counts':obj.Expert_Grade.value_counts().to_dict(),
        'ab_objects_screened':len(d),'published_final_sed_sample':int(d.final_sample.sum()),
        'rankable_all_ab':int(d.numerically_rankable.sum()),
        'strict_photometry_model_quality':int(d.strict_photometry_model_quality.sum()),
        'simple_geometry_priority':int(d.simple_geometry_priority.sum()),
        'desi_lens_z_parent':int(obj.desi_deflector_specz.notna().sum()),
        'desi_lens_z_ab':int(d.lens_specz_available.sum()),
        'verified_external_pairs':int(d.verified_pair_available.sum()),
        'external_slacs_objects_checked':len(slacs),
        'external_slacs_matches_within_10arcsec':int(slacs.within_10arcsec.sum()),
        'dedicated_forward_fit_candidates':int(trial.sum()),
        'availability_counts':d.availability_tier.value_counts().to_dict(),
        'strict_sample_raw_sensitivity_counts':d.loc[d.strict_photometry_model_quality,'raw_sensitivity_bin'].value_counts().to_dict(),
        'ready_decisive_a0_density_tests_established':0,
        'note':'Zero established decisive tests is an audit status, not proof none can be made. Source-z literature search is bounded, not complete.',
        'cosmology_role':'ECLIPSE-D fiducial geometry only, not measured dark-energy density',
        'model_role':'spherical stellar-only unscreened triage; no v3s forward fit, no model selection',
        'a0_canonical':A0,'a0_alt':A0_ALT,
    }
    (out/'summary.json').write_text(json.dumps(counters,indent=2)+'\n')
    (out/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps(counters,indent=2))
    print(pairs[['unique_identifier','external_name','z_lens_verified','z_source_verified',
                 'lens_model_consensus_75','final_sample','S_alpha_proxy','availability_tier']].to_string(index=False))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    main(p.parse_args().output)

"""FOR J0332 spherical radius diagnostic, explicitly not an image/theory fit.

Run through the bounded command recorded in contract.json and README.md.
Uncertainties are approximate marginal distributions reconstructed from summaries;
independence and tail shapes are assumptions, not supplied catalogue posteriors.
"""
import argparse
import io
import json
import math
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gammainc, gammaincinv, gammaln
from scipy.stats import norm, qmc

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT/'euclid_eclipse_screen_2026_11_13/inputs'
UID = 'EUCL-DR1-L014994'
G, C, MSUN, MPC = 6.67430e-11, 299792458., 1.98847e30, 3.085677581491367e22
ARCSEC = np.pi/(180*3600)
H0, OM = 67.74, .3089
A0S = {'baseline': 9.3603e-11, 'alternative': 1.1312e-10}


def read_inputs():
    with ZipFile(INPUT/'ECLIPSE_D_dr1_redshifts_and_physical_properties.zip') as z:
        sed = pd.read_csv(z.open('eclipse_dr1_catalogue_key_v20261103.csv'), low_memory=False)
    with ZipFile(INPUT/'ECLIPSE_lens_models.zip') as z:
        with ZipFile(io.BytesIO(z.read('ECLIPSE_lens_models/catalogue_csvs.zip'))) as zz:
            master = pd.read_csv(zz.open('dr1_catalogue_v5_full/csv/dr1_catalogue_15072_master.csv'), low_memory=False)
            tables = {name: pd.read_csv(zz.open('dr1_catalogue_v5_full/csv/'+name+'.csv'), low_memory=False)
                      for name in ['lens_sersic', 'lens_mass']}
    assert all(df.unique_identifier.eq(UID).sum() == 1 for df in [sed, master, *tables.values()])
    sed, master = [df.loc[df.unique_identifier.eq(UID)].iloc[0] for df in [sed, master]]
    tables = {k:df.loc[df.unique_identifier.eq(UID)].iloc[0] for k,df in tables.items()}
    spec = pd.read_csv(ROOT/'euclid_eclipse_screen_2026_11_13/external_verified_redshifts.csv')
    key = 'Unique_Identifier' if 'Unique_Identifier' in spec else 'unique_identifier'
    spec = spec.loc[spec[key].eq(UID)].iloc[0]
    return sed, master, tables, spec


def angular_distance(z):
    z = np.asarray(z, dtype=float)
    nodes, weights = np.polynomial.legendre.leggauss(48)
    q = (nodes+1)*z[...,None]/2
    chi = C/(H0*1000/MPC)*z/2*np.sum(weights/np.sqrt(OM*(1+q)**3+1-OM), axis=-1)
    return chi/(1+z)


def abel_scalar(x,n):
    t0 = gammaincinv(2*n,.5)*x**(1/n)
    shape = 2*n+1
    def tail(t):
        u=min(1.,(t0/t)**n)
        b=2*u**3/3+u**5/5+3*u**7/28 if u<.01 else math.asin(u)-u*math.sqrt(max(0,1-u*u))
        return 2/math.pi*b*math.exp((shape-1)*math.log(t)-t-gammaln(shape))
    return float(gammainc(shape,t0)+quad(tail,t0,np.inf,epsabs=1e-12,epsrel=1e-10,limit=200)[0])


def abel_vector(x,n,order=128):
    """Same exact Abel integral, v=sqrt(t-t0) regularizes endpoint cusp.

    Tail ends at t0+100; omitted gamma probability is checked separately.
    Broadcasting arrays; final dimension reserved for Abel quadrature.
    """
    x,n=np.broadcast_arrays(np.asarray(x),np.asarray(n))
    t0=gammaincinv(2*n,.5)*x**(1/n)
    shape=2*n+1
    v,w=np.polynomial.legendre.leggauss(order)
    v=(v+1)*5
    w=w*5
    t=t0[...,None]+v*v
    u=np.minimum(1.,(t0[...,None]/t)**n[...,None])
    b=np.where(u<.01,2*u**3/3+u**5/5+3*u**7/28,
               np.arcsin(u)-u*np.sqrt(np.maximum(0.,1-u*u)))
    tail=np.sum(w*2*v*2/np.pi*b*np.exp((shape[...,None]-1)*np.log(t)-t-gammaln(shape[...,None])),axis=-1)
    return gammainc(shape,t0)+tail


def los_cache(theta,re,n,zl,zs,order=128,abel_order=128):
    theta,re,n,zl,zs=np.broadcast_arrays(*[np.atleast_1d(x).astype(float) for x in (theta,re,n,zl,zs)])
    dl,ds=angular_distance(zl),angular_distance(zs)
    ratio=1-dl*(1+zl)/(ds*(1+zs))
    radius=theta*ARCSEC*dl
    x,w=np.polynomial.legendre.leggauss(order)
    t=(x+1)*np.pi/4
    sec=1/np.cos(t)
    w=w*np.pi/4
    massfrac=abel_vector(theta[:,None]/re[:,None]*sec,n[:,None],abel_order)
    gn_unit=G*MSUN*massfrac/(radius[:,None]*sec)**2
    return radius,ratio,sec,w,gn_unit


def alpha_logmass(logmass,a0,cache):
    radius,ratio,sec,w,gn_unit=cache
    gn=gn_unit*10**np.atleast_1d(logmass)[:,None]
    g=.5*(gn+np.sqrt(gn*gn+4*a0*gn))
    return 4*radius/C**2*np.sum(g*sec*w,axis=1)*ratio/ARCSEC


def required_mass(theta,a0,cache):
    theta=np.atleast_1d(theta)
    low=np.full(len(theta),9.)
    high=np.full(len(theta),14.)
    assert np.all(alpha_logmass(low,a0,cache)<theta)
    assert np.all(alpha_logmass(high,a0,cache)>theta)
    for _ in range(44):
        mid=(low+high)/2
        smaller=alpha_logmass(mid,a0,cache)<theta
        low=np.where(smaller,mid,low)
        high=np.where(smaller,high,mid)
    return (low+high)/2


def adaptive_alpha(logmass,a0,theta,re,n,zl,zs):
    dl,ds=angular_distance(zl),angular_distance(zs)
    ratio=1-dl*(1+zl)/(ds*(1+zs))
    radius=theta*ARCSEC*dl
    def f(t):
        sec=1/math.cos(t)
        gn=G*10**logmass*MSUN*abel_scalar(theta/re*sec,n)/(radius*sec)**2
        return .5*(gn+math.sqrt(gn*gn+4*a0*gn))*sec
    return 4*radius/C**2*quad(f,0,np.pi/2,epsabs=1e-17,epsrel=1e-9,limit=100)[0]*ratio/ARCSEC


def transform_summary(z,median,low,high,low3=None,high3=None):
    if low3 is None:
        return median+z*np.where(z<0,median-low,high-median)
    values=np.interp(z,[-3,-1,0,1,3],[low3,low,median,high,high3])
    values=np.where(z< -3,low3+(z+3)*(low-low3)/2,values)
    values=np.where(z>3,high3+(z-3)*(high3-high)/2,values)
    return values


def summary(x):
    return {'q025':float(np.quantile(x,.025)),'q16':float(np.quantile(x,.16)),
            'median':float(np.median(x)),'q84':float(np.quantile(x,.84)),
            'q975':float(np.quantile(x,.975)),'mean':float(np.mean(x)),
            'std':float(np.std(x,ddof=1))}


def mass_survival(required,median,low_error,high_error):
    # Exact p16/p50/p84 match for the SED summary. Not a standard split-normal
    # (which gives different probability on either side of its mode).
    scale=np.where(required<median,low_error,high_error)/norm.ppf(.84)
    return norm.sf((required-median)/scale)


def main(out,power):
    sed,master,tables,spec=read_inputs()
    zl,zs=float(spec.z_lens),float(spec.z_source)
    zle,zse=float(spec.z_lens_error),float(spec.z_source_error)
    theta=float(sed.eclipse_effective_einstein_radius)
    re=float(sed.eclipse_effective_radius)
    n=float(sed.eclipse_sersic_index)
    lm=float(sed.eclipse_log_survived_mass_med)
    lmlo=float(sed.eclipse_log_survived_mass_low)
    lmhi=float(sed.eclipse_log_survived_mass_upp)
    base=np.array([theta,re,n,zl,zs])
    e=np.hypot(master.lens_light_ell_comps_0,master.lens_light_ell_comps_1)
    q=(1-e)/(1+e)
    checks={}
    gauss=[]
    for x in [.01,.1,1.,10.]:
        actual=abel_vector(x,.5)
        analytic=gammainc(1.5,np.log(2)*x*x)
        gauss.append(float(actual/analytic-1))
    checks['gaussian_max_relative_mass_error']=max(map(abs,gauss))
    assert checks['gaussian_max_relative_mass_error']<1e-7
    grid=[(xx,nn) for xx in [.3,1.,2.,10.,100.] for nn in [3.5,5.663353614972559,7.5]]
    errs=[float(abel_vector(xx,nn)/abel_scalar(xx,nn)-1) for xx,nn in grid]
    checks['abel_vector_vs_adaptive_max_relative_error']=max(map(abs,errs))
    assert checks['abel_vector_vs_adaptive_max_relative_error']<1e-7
    cache=los_cache(*base)
    cache2=los_cache(*base,order=256,abel_order=192)
    central={}
    for name,a0 in A0S.items():
        req=float(required_mass(theta,a0,cache)[0])
        alpha=float(alpha_logmass(lm,a0,cache)[0])
        exact=adaptive_alpha(req,a0,*base)
        more=float(required_mass(theta,a0,cache2)[0])
        assert abs(exact/theta-1)<1e-7
        assert abs(more-req)<1e-7
        central[name]={'a0_m_s2':a0,'log10_required_mass_Msun':req,'required_mass_Msun':10**req,
                       'required_to_SED_median_mass_ratio':10**(req-lm),'delta_log10_mass_dex':req-lm,
                       'alpha_reduced_at_SED_median_arcsec':alpha,'alpha_over_observed_thetaE':alpha/theta,
                       'one_sided_SED_survival_at_central_required_mass':float(mass_survival(req,lm,lmlo,lmhi)),
                       'adaptive_required_radius_residual_fraction':float(exact/theta-1),
                       'doubled_quadrature_required_mass_difference_dex':more-req}
    # Orthogonal Newtonian check: projected Sersic enclosed mass has analytic gamma form.
    newton=alpha_logmass(lm,0.,cache)[0]
    dl,ratio=angular_distance(zl),cache[1][0]
    projected=gammainc(2*n,gammaincinv(2*n,.5)*(theta/re)**(1/n))
    analytic=4*G*10**lm*MSUN*projected/(C*C*theta*ARCSEC*dl)*ratio/ARCSEC
    checks['newtonian_analytic_projected_mass_relative_error']=float(newton/analytic-1)
    assert abs(newton/analytic-1)<1e-7
    # Available +/-3 sigma summaries assess how sensitive results are to extrapolated tails.
    pars=[('lens_mass','effective_einstein_radius'),('lens_sersic','effective_radius'),('lens_sersic','sersic_index')]
    distributions={}
    for key,p in pars:
        row=tables[key]
        distributions[p]={s:float(row[p+s]) for s in ['', '_lower_1_sigma','_upper_1_sigma','_lower_3_sigma','_upper_3_sigma']}
    allruns={}
    arrays={}
    for shape_mode in ['one_sigma_piecewise_normal','one_and_three_sigma_quantile_interpolation']:
        reps=[]
        for seed in [20261113,20261114]:
            z=norm.ppf(qmc.Sobol(5,scramble=True,seed=seed).random_base2(power))
            vals=np.empty_like(z)
            for j,(_,p) in enumerate(pars):
                d=distributions[p]
                extra={} if shape_mode.startswith('one_sigma') else {'low3':d['_lower_3_sigma'],'high3':d['_upper_3_sigma']}
                vals[:,j]=transform_summary(z[:,j],d[''],d['_lower_1_sigma'],d['_upper_1_sigma'],**extra)
            vals[:,3]=zl+zle*z[:,3]
            vals[:,4]=zs+zse*z[:,4]
            assert np.all(vals>0) and np.all(vals[:,4]>vals[:,3])
            reqs={k:[] for k in A0S}
            for start in range(0,len(vals),128):
                v=vals[start:start+128]
                cc=los_cache(*v.T)
                for name,a0 in A0S.items():
                    reqs[name].append(required_mass(v[:,0],a0,cc))
            record={}
            for name in A0S:
                r=np.concatenate(reqs[name]); survival=mass_survival(r,lm,lmlo,lmhi)
                tail=float(np.mean(survival))
                record[name]={'required_logmass':summary(r),'mean_SED_upper_tail_probability':tail,
                              'one_sided_normal_equivalent_z':float(norm.isf(tail)),
                              'conditional_interpretation':'Upper-tail probability of approximate Salpeter SED mass distribution exceeding required spherical mass, averaged over independent measurement-summary surrogates. Not a calibrated goodness-of-fit p-value or theory exclusion.'}
                arrays[shape_mode+'_'+str(seed)+'_'+name]=r
            reps.append(record)
        allruns[shape_mode]={'samples_per_replicate':2**power,'seeds':[20261113,20261114],'replicates':reps,
                             'replicate_tail_absolute_difference':{k:abs(reps[0][k]['mean_SED_upper_tail_probability']-reps[1][k]['mean_SED_upper_tail_probability']) for k in A0S}}
    # Isolate conditional inputs' effects and radius conventions without calling these systematics a posterior.
    oned={}
    for j,label in enumerate(['thetaE','Re','sersic_n','z_lens','z_source']):
        for side in ['lower','upper']:
            v=base.copy()
            if j<3:
                d=distributions[pars[j][1]]; v[j]=d['_'+side+'_1_sigma']
            else: v[j]+=(-1 if side=='lower' else 1)*[zle,zse][j-3]
            cc=los_cache(*v)
            oned[label+'_'+side]={k:float(required_mass(v[0],a,cc)[0])-central[k]['log10_required_mass_Msun'] for k,a in A0S.items()}
    variants={}
    for label,fac in [('table_Re_times_sqrt_q',np.sqrt(q)),('table_Re_over_sqrt_q',1/np.sqrt(q))]:
        v=base.copy(); v[1]*=fac; cc=los_cache(*v)
        variants[label]={'radius_factor':fac,**{k:{'log10_required_mass_Msun':float(required_mass(theta,a,cc)[0])} for k,a in A0S.items()}}
    # Luminosity-distance-only transport is diagnostic, not a spectroscopic-redshift SED refit.
    lum_shift=2*np.log10(angular_distance(zl)*(1+zl)**2/(angular_distance(.98)*(1+.98)**2))
    result={'target':UID,'external_name':'FOR J0332-3557','assertion_tested':'Numerical spherical isolated simple-mu AQUAL required stellar mass and marginal-summary uncertainty propagation for this one named target.',
            'outcome':'Conditional on numerical quadrature and approximate independent marginal uncertainty distributions; finite numerical checks passed.',
            'inputs':{'thetaE_arcsec':theta,'Re_table_arcsec':re,'sersic_n':n,'z_lens':zl,'z_lens_sigma':zle,'z_source':zs,'z_source_sigma':zse,'log10_SED_mass_Msun':lm,'log10_SED_mass_lower_error':lmlo,'log10_SED_mass_upper_error':lmhi,'SED_redshift_fixed_at':.98,'SED_IMF':'Salpeter','q_from_light':float(q),'Dls_Ds':float(ratio),'Re_kpc_at_specz':float(re*ARCSEC*dl/(MPC/1000))},
            'measurement_summaries':distributions,'central':central,'uncertainty_propagation':allruns,
            'one_at_a_time_1sigma_required_logmass_shifts_dex':oned,'radius_convention_diagnostics_only':variants,
            'luminosity_distance_only_SED_mass_shift_dex':float(lum_shift),'numerical_checks':checks,
            'limitations':['No image likelihood, source reconstruction, or non-spherical AQUAL field solution.','Effective Einstein radius is inherited from SIE+external shear model and is model-dependent.','Independent marginal surrogates, not native joint posterior samples; no recovered mass-light/redshift correlations.','SED mass conditional on fixed photo-z .98, Salpeter IMF, adopted SPS/SFH/dust and frozen deblending mass model.','No IMF, stellar-population, M/L gradient, gas, extra baryon, line-of-sight/external-convergence, screening, external-field, cosmology or 3D geometry systematics in reported tails.','The lensing-potential identification is an assumed relativistic completion, not implied by nonrelativistic AQUAL alone.','Both Re*sqrt(q) and Re/sqrt(q) are labelled convention diagnostics; neither is asserted as the correct 3D conversion.','A one-sided normal-equivalent value is a summary of this conditional surrogate, not a detection significance or definitive failure.']}
    out.mkdir(parents=True,exist_ok=True)
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(out/'required_mass_samples.npz',**arrays)
    print(json.dumps({'central':central,'checks':checks,'uncertainty':allruns,'luminosity_distance_only_SED_mass_shift_dex':float(lum_shift)},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--power',type=int,default=13)
    a=p.parse_args();assert 8<=a.power<=15;main(a.output,a.power)

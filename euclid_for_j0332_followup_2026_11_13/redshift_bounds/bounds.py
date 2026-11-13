"""Source-redshift-free spherical lensing bounds; not an oblate/action fit."""
import argparse,csv,json,math
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ellipe,gammainc,gammaincinv,gammaln
from scipy.stats import norm,qmc
from astropy.io import fits

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
G,C,MSUN,MPC=6.67430e-11,299792458.,1.98847e30,3.085677581491367e22
ARC=np.pi/(180*3600)
H0,OM,A0=67.74,.3089,9.3603e-11
H=H0*1000/MPC
NODES,WEIGHTS=np.polynomial.legendre.leggauss(64)
Q84=norm.ppf(.84)


def number(x):
    try:return float(x)
    except (ValueError,TypeError):return np.nan


def comoving_integral(z):
    z=np.asarray(z)
    tmin=1/np.sqrt(1+z)
    t=tmin[...,None]+(NODES+1)/2*(1-tmin[...,None])
    return (1-tmin)*np.sum(WEIGHTS/np.sqrt(OM+(1-OM)*t**6),axis=-1)


IINF=float(comoving_integral(np.inf))


def dl(z):return C/H*comoving_integral(z)/(1+np.asarray(z))
def beta_inf(z):return 1-comoving_integral(z)/IINF
def beta(zl,zs):return 1-comoving_integral(zl)/comoving_integral(zs)
def lum_distance(z):return dl(z)*(1+np.asarray(z))**2


def point_alpha(logmass,radius,a0=A0):
    mass=10**np.asarray(logmass)*MSUN
    gn=G*mass/np.asarray(radius)**2
    if a0==0:return 4*G*mass/(C*C*np.asarray(radius))
    y=gn/a0
    boost=.5*(1+np.sqrt(1+4/y)*ellipe(1/(1+4/y)))
    return 4*G*mass/(C*C*np.asarray(radius))*boost


def algebraic_upper_alpha(logmass,radius,a0=A0):
    mass=10**np.asarray(logmass)*MSUN
    return 4*G*mass/(C*C*np.asarray(radius))+2*np.pi*np.sqrt(G*mass*a0)/(C*C)


def point_mass_floor(theta,zl,beta_limit=None):
    theta,zl=np.broadcast_arrays(np.asarray(theta),np.asarray(zl))
    radius=theta*ARC*dl(zl)
    target=theta*ARC/(beta_inf(zl) if beta_limit is None else beta_limit)
    low=np.full(theta.shape,7.)
    high=np.full(theta.shape,15.)
    for _ in range(50):
        mid=(low+high)/2
        small=point_alpha(mid,radius)<target
        low=np.where(small,mid,low);high=np.where(small,high,mid)
    return (low+high)/2


def algebraic_mass_floor(theta,zl):
    radius=theta*ARC*dl(zl)
    target=theta*ARC/beta_inf(zl)
    aa=4*G/(C*C*radius)
    bb=2*np.pi*np.sqrt(G*A0)/(C*C)
    root=2*target/(np.sqrt(bb*bb+4*aa*target)+bb)
    return np.log10(root*root/MSUN)


def abel_vector(x,n,order=128):
    x=np.asarray(x)
    t0=gammaincinv(2*n,.5)*x**(1/n)
    shape=2*n+1
    v,w=np.polynomial.legendre.leggauss(order)
    v=(v+1)*5;w=w*5
    t=t0[...,None]+v*v
    u=np.minimum(1.,(t0[...,None]/t)**n)
    bracket=np.where(u<.01,2*u**3/3+u**5/5+3*u**7/28,
        np.arcsin(u)-u*np.sqrt(np.maximum(0.,1-u*u)))
    tail=np.sum(w*2*v*2/np.pi*bracket*
        np.exp((shape-1)*np.log(t)-t-gammaln(shape)),axis=-1)
    return gammainc(shape,t0)+tail


def sersic_cache(theta,re,n,zl,order=128,abel_order=128):
    z,w=np.polynomial.legendre.leggauss(order)
    t=(z+1)*np.pi/4;w=w*np.pi/4
    sec=1/np.cos(t)
    radius=theta*ARC*float(dl(zl))
    mf=abel_vector(theta/re*sec,n,abel_order)
    assert np.all((mf>=0)&(mf<=1+1e-10))
    return radius,sec,w,G*MSUN*mf/(radius*sec)**2


def sersic_alpha(logmass,cache,a0=A0):
    r,sec,w,unit=cache
    gn=unit*10**logmass
    g=gn if a0==0 else .5*(gn+np.sqrt(gn*gn+4*a0*gn))
    return 4*r/(C*C)*np.sum(g*sec*w)


def needed_z(zl,required):
    if required<=0:return {'zs':None,'status':'nonpositive_required_geometry'}
    if required>=float(beta_inf(zl)):
        return {'zs':None,'status':'no_finite_source_z_in_adopted_cosmology',
                'required_beta':float(required)}
    target=float(comoving_integral(zl))/(1-required)
    def integral_t(t):
        z=np.inf if t==0 else 1/t**2-1
        return float(comoving_integral(z))-target
    tt=brentq(integral_t,0,1/np.sqrt(1+zl),xtol=1e-14)
    return {'zs':float(1/tt**2-1),'status':'unique_finite_source_z',
            'required_beta':float(required)}


def minimum_a0(theta,zl,logmass,alpha_fn):
    goal=theta*ARC/float(beta_inf(zl))
    if alpha_fn(logmass,0.)>=goal:return 0.
    root=brentq(lambda la:alpha_fn(logmass,10**la)-goal,-15,-6,xtol=1e-11)
    return float(10**root)


def quantiles(x):
    return {str(q):float(np.quantile(x,q)) for q in [.025,.16,.5,.84,.975]}


def clean(value):
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,list):return [clean(v) for v in value]
    if isinstance(value,np.generic):return clean(value.item())
    if isinstance(value,float) and not np.isfinite(value):return None
    return value


def main(output):
    output.mkdir(parents=True,exist_ok=True)
    screen=ROOT/'euclid_eclipse_screen_2026_11_13/run_02/screen_all_15072.csv'
    matches=ROOT/'euclid_for_j0332_fit_2026_11_13/desi_crossmatch/matches_1arcsec.csv'
    with screen.open() as f:catalog={r['unique_identifier']:r for r in csv.DictReader(f)}
    with matches.open() as f:targets=list(csv.DictReader(f))
    targets.append({'Unique_Identifier':'EUCL-DR1-L014994','Z':.986,'ZERR':.001,
                    'TARGETID':'','control_source_redshift':3.773})
    with fits.open(ROOT/'euclid_for_j0332_fit_2026_11_13/desi_crossmatch/desi-sl-vac-v1.fits') as h:
        vac={int(r['TARGETID']):float(r['LOGMSTAR']) for r in h[1].data}
    uniform=qmc.Sobol(2,scramble=True,seed=13613).random_base2(11)
    standard=norm.ppf(uniform)
    records=[]
    for target in targets:
        uid=target['Unique_Identifier'];row=catalog[uid]
        zl=number(target['Z']);ze=number(target['ZERR'])
        theta=number(row['eclipse_effective_einstein_radius'])
        re=number(row['eclipse_effective_radius']);n=number(row['eclipse_sersic_index'])
        q=number(row['axis_ratio_proxy'])
        lm=number(row['eclipse_log_survived_mass_med']);zph=number(row['eclipse_median_phz'])
        shift=2*np.log10(lum_distance(zl)/lum_distance(zph)) if np.isfinite(zph) else np.nan
        median=lm+shift
        low=number(row['eclipse_log_survived_mass_low']);high=number(row['eclipse_log_survived_mass_upp'])
        radius=theta*ARC*float(dl(zl));bmax=float(beta_inf(zl))
        floor=float(point_mass_floor(theta,zl))
        samples_z=zl+ze*standard[:,0]
        tl=theta-number(row['eclipse_effective_einstein_radius_lower_1_sigma'])
        tu=number(row['eclipse_effective_einstein_radius_upper_1_sigma'])-theta
        samples_theta=theta+standard[:,1]*np.where(standard[:,1]<0,tl,tu)/Q84
        floors=point_mass_floor(samples_theta,samples_z)
        corrected_medians=lm+2*np.log10(lum_distance(samples_z)/lum_distance(zph)) if np.isfinite(lm) else np.full(len(floors),np.nan)
        offset=floors-corrected_medians
        conditional_sf=norm.sf(Q84*offset/np.where(offset<0,low,high))
        result={'unique_identifier':uid,'name':row['euclj_name'],'z_lens':zl,
            'z_lens_error':ze,'z_photo':zph,'theta_effective_arcsec':theta,
            'Re_catalog_arcsec':re,'sersic_n':n,'q_projected':q,
            'model_consensus':row['lens_model_consensus_75'],'final_SED_sample':row['final_sample'],
            'stellar_logmass_photo':lm,'flux_only_photo_to_spec_shift_dex':float(shift),
            'stellar_logmass_flux_only_spec':float(median),'stellar_error_lower_dex':low,'stellar_error_upper_dex':high,
            'beta_infinity':bmax,'point_mass_logM_floor':floor,
            'point_mass_logM_floor_using_only_beta_le_one':float(point_mass_floor(theta,zl,1.)),
            'algebraic_upper_bound_logM_floor':float(algebraic_mass_floor(theta,zl)),
            'point_mass_floor_geometry_quantiles':quantiles(floors),
            'point_mass_floors_at_finite_source_redshifts':{
                str(zs):float(point_mass_floor(theta,zl,float(beta(zl,zs))))
                for zs in [1.,2.,3.,4.,6.,10.] if zs>zl},
            'point_floor_minus_SED_median_dex':float(floor-median),
            'point_floor_offset_in_quoted_upper_errors':float((floor-median)/high),
            'conditional_SED_survival_above_point_floor':float(np.mean(conditional_sf)),
            'no_exclusion_probability_claim':'Survival is conditional on reconstructed mass-quantile surrogate, independent geometry errors, flux-only redshift rescaling and fixed IMF/SPS; not a theory p-value',
            'profiles':[]}
        scenarios=[('SED_median',median),('SED_upper_quantile',median+high),
            ('SED_plus_0p2dex',median+.2),('SED_plus_0p25dex',median+.25),
            ('SED_plus_0p3dex',median+.3),('SED_plus_0p5dex',median+.5)]
        tid=target.get('TARGETID','')
        if tid and int(tid) in vac:
            raw=vac[int(tid)]
            at_h=raw-2*np.log10(H0/100)
            result['DESI_logmass_raw_h1_Chabrier']=raw
            result['DESI_logmass_flux_scaling_h06774_Chabrier']=float(at_h)
            result['DESI_mass_conversion_caveat']='Official docs state h=1,Chabrier; -2logh assumes flux mass scaling. +.2/.25dex IMF shifts are illustrative assumptions, not a matched deblended mass measurement.'
            scenarios.extend([('DESI_hscaled_Chabrier',at_h),
                ('DESI_hscaled_plus_0p2dex',at_h+.2),('DESI_hscaled_plus_0p25dex',at_h+.25)])
        if np.isfinite(median):
            maxpoint=point_alpha(median,radius)*bmax/ARC
            result['nominal_max_point_reduced_deflection_arcsec']=float(maxpoint)
            result['nominal_point_deflection_enhancement_needed']=float(theta/maxpoint-1)
            result['nominal_point_external_kappa_needed_at_infinity']=float(max(0.,1-maxpoint/theta))
            result['point_a0_min_at_SED_median']=minimum_a0(theta,zl,median,
                lambda mass,a:point_alpha(mass,radius,a))
        profile_specs=[('spherical_scale_equals_catalog_Re',re),
                       ('spherical_scale_equals_major_axis_Re',re/np.sqrt(q))]
        for label,reff in profile_specs:
            cache=sersic_cache(theta,reff,n,zl)
            fine=sersic_cache(theta,reff,n,zl,order=256,abel_order=192)
            massfloor=brentq(lambda mass:sersic_alpha(mass,cache)*bmax-theta*ARC,7,15)
            profile={'radius_convention':label,'Re_spherical_arcsec':reff,
                'minimum_logmass_any_source_redshift':float(massfloor),
                'massfloor_minus_SED_median_dex':float(massfloor-median),
                'scenarios':[]}
            for name,mass in scenarios:
                if not np.isfinite(mass):continue
                alpha=sersic_alpha(mass,cache)
                point=point_alpha(mass,radius)
                assert alpha<=point*(1+1e-9)
                profile['scenarios'].append({'mass_scenario':name,'logmass':float(mass),
                    'unreduced_sersic_deflection_arcsec':float(alpha/ARC),
                    'max_reduced_sersic_arcsec':float(alpha*bmax/ARC),
                    'required_z_source_sersic':needed_z(zl,theta*ARC/alpha),
                    'required_z_source_point_envelope':needed_z(zl,theta*ARC/point)})
            checkmass=median if np.isfinite(median) else massfloor
            error=sersic_alpha(checkmass,cache)/sersic_alpha(checkmass,fine)-1
            profile['128_vs256_LOS_Abel_relative_deflection_error']=float(error)
            assert abs(error)<2e-7
            if np.isfinite(median):
                profile['a0_min_at_SED_median']=minimum_a0(theta,zl,median,
                    lambda mass,a:sersic_alpha(mass,cache,a))
            result['profiles'].append(profile)
        records.append(result)
        print(json.dumps(clean({k:result[k] for k in ['unique_identifier','point_mass_logM_floor',
            'point_floor_minus_SED_median_dex','conditional_SED_survival_above_point_floor',
            'nominal_max_point_reduced_deflection_arcsec'] if k in result})),flush=True)
    # Independent point-mass quadrature and limiting-case checks.
    checks=[]
    for y in [1e-10,.01,1.,10.,1000.,1e10]:
        val=.5*quad(lambda t:np.cos(t)+np.sqrt(np.cos(t)**2+4/y),0,np.pi/2,
                    epsabs=1e-10,epsrel=1e-11)[0]
        analytic=.5*(1+np.sqrt(1+4/y)*ellipe(1/(1+4/y)))
        assert abs(val/analytic-1)<1e-9
        assert analytic<=1+np.pi/(2*np.sqrt(y))+1e-12
        assert analytic>=max(1.,np.pi/(2*np.sqrt(y)))*(1-1e-12)
        if y==1e-10:assert abs(analytic/(np.pi/(2*np.sqrt(y)))-1)<1e-4
        if y==1e10:assert abs(analytic-1)<1e-8
        checks.append({'y':y,'elliptic_vs_adaptive_relative_error':float(val/analytic-1),
            'boost':float(analytic),'deep_limit_boost_pi_over_2sqrt_y_ratio':float(analytic/(np.pi/(2*np.sqrt(y))))})
    output_data={'assertion_tested':'Under isolated spherical unscreened simple-mu and flat matter+Lambda geometry, compute source-independent point-mass/algebraic necessary mass floors and exact-Sersic diagnostics for five DESI matches plus FORcontrol',
        'non_claims':['No non-spherical exclusion','No full screened-v3s test','No measured source redshift from these calculations','No calibrated theory p-value','Radiation omitted in adopted background'],
        'geometry':{'H0':H0,'Omega_m':OM,'comoving_integral_infinity':IINF,
            'horizon_distance_Mpc':C/H*IINF/MPC,'radiation_included':False},
        'a0':A0,'geometry_uncertainty_samples':2048,'Sobol_seed':13613,
        'geometry_quantile_model':'Independent Gaussian spectroscopic error and median-matched two-half-normal theta summary; stellar tails are reconstructed conditional quantile surrogates, not supplied joint posterior',
        'point_mass_formula_checks':checks,'targets':records,'status':'completed'}
    (output/'result.json').write_text(json.dumps(clean(output_data),indent=2,allow_nan=False)+'\n')
    with (output/'summary.csv').open('w') as f:
        names=['unique_identifier','name','z_lens','theta_effective_arcsec','stellar_logmass_flux_only_spec',
               'point_mass_logM_floor','point_floor_minus_SED_median_dex',
               'point_floor_offset_in_quoted_upper_errors','conditional_SED_survival_above_point_floor',
               'nominal_max_point_reduced_deflection_arcsec','nominal_point_external_kappa_needed_at_infinity']
        writer=csv.DictWriter(f,fieldnames=names);writer.writeheader()
        for row in records:writer.writerow({k:clean(row.get(k)) for k in names})


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)

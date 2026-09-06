#!/usr/bin/env python
"""Independent X-COP units/kernel/pressure audit, not a gravity certification.

No NEW halo fit, cosmic baryon fraction, or dark-matter abundance is imposed in
the primary acceleration comparison. Published modelling is inherited, including
the gas file's NFW-derived R500 used to decode its normalized radius.
Published M_FORW is a thermal hydrostatic reconstruction,
NOT raw data or a direct lensing measurement. Distances and profile modelling are
inherited. NFW columns serve ONLY to cross-check the gas radius conversion.
"""
import argparse
import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import astropy
import numpy as np
import scipy
import sympy as sp
from astropy.io import fits
from scipy.integrate import cumulative_trapezoid, trapezoid
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT / 'real_research/data/xcop'
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = {'canonical': 9.3619e-11, 'alt': 1.1279e-10}
RADII = np.array([30.,40.,50.,75.,100.,150.,200.,300.,420.,750.,1000.])
RELAXED = ('A1795','A2029','A2142')  # Kelleher & Lelli 2024, Table 1.


def loginterp(x, xp, fp):
    x, xp, fp = map(lambda a: np.asarray(a, dtype=float), (x,xp,fp))
    if np.any(xp <= 0) or np.any(fp <= 0) or np.any(np.diff(xp) <= 0):
        raise ValueError('Log interpolation requires ordered, positive profiles')
    return np.exp(np.interp(np.log(x), np.log(xp), np.log(fp), left=np.nan, right=np.nan))


def radius_kpc(r, unit, header):
    factors={'kpc':1., 'Mpc':1000.}
    if unit == 'R/R500':
        if 'R500' not in header or float(header['R500']) <= 0:
            raise ValueError('Normalized radius requires its own positive R500 in kpc')
        scale=float(header['R500'])
    elif unit in factors:
        scale=factors[unit]
    else:
        raise ValueError('Unrecognized radius unit: '+str(unit))
    return np.asarray(r, dtype=float)*scale


def exact_y(b):
    """Solve y*(1-exp(-y))=b; brackets follow 0<=y-b<=1/e."""
    b=np.asarray(b,dtype=float)
    if np.any(~np.isfinite(b)) or np.any(b<0):
        raise ValueError('Nonnegative finite baryonic field required')
    def solve(x):
        if x == 0: return 0.
        return brentq(lambda y:y*(-np.expm1(-y))-x, x, x+1/np.e,
                      xtol=1e-25, rtol=1e-14)
    return np.vectorize(solve, otypes=[float])(b)


def route_a_y(b):
    b=np.asarray(b,dtype=float)
    return b/(-np.expm1(-np.sqrt(b)))


def carrier_y(b):
    b=np.asarray(b,dtype=float)
    return np.where(b <= 1-1/np.e, exact_y(b), b+1/np.e)


def source_ratio(yobs, mh, mb):
    return (-np.expm1(-np.asarray(yobs)))*np.asarray(mh)/np.asarray(mb)


def static_gravity(gthermal, pressure_nt_derivative, rho):
    return gthermal-pressure_nt_derivative/rho


def pressure_boundary(r, rho, gh, gm):
    """Pnt(r)=Pnt(R)-integral_r^R rho*(gh-gm) ds. No outer prior imposed."""
    integrand=rho*(gh-gm)
    forward=cumulative_trapezoid(integrand,r,initial=0)
    suffix=forward[-1]-forward
    need=max(0.,float(np.max(suffix)))
    thermal=float(trapezoid(rho*gh,r))
    return {'required_outer_pressure':need,
            'inner_pressure_if_outer_zero':float(-suffix[0]),
            'fraction_of_thermal_pressure_drop':need/thermal,
            'all_deficit_positive':bool(np.all(gh>gm))}


def rest_baryon_fraction(cluster_mass_fraction, local_fraction, cosmic_fraction):
    return (cosmic_fraction-cluster_mass_fraction*local_fraction)/(1-cluster_mass_fraction)


def load_cluster(name):
    p=DATA/name
    with fits.open(p/(name+'_hydro_mass.fits')) as f:
        d=f[1].data
        c={'name':name,'rh':radius_kpc(d['RADIUS'],f[1].columns['RADIUS'].unit,f[1].header)}
        for k in ('M_FORW','EM_FORW','M_NFW','M_EIN'):
            c[k]=np.array(d[k],float)
    with fits.open(p/(name+'_fgas_profile.fits')) as f:
        d=f[1].data
        c.update(rg=radius_kpc(d['RADIUS'],f[1].columns['RADIUS'].unit,f[1].header),
                 rg_legacy=np.array(d['RADIUS'],float)*1000.,
                 R500=float(f[1].header['R500']), gas_unit=f[1].columns['RADIUS'].unit,
                 mg=np.array(d['MGAS'],float), gas_nfw=np.array(d['M_NFW'],float))
    star=p/(name+'_mstar.fits')
    c['has_star']=star.exists()
    if c['has_star']:
        with fits.open(star) as f:
            d=f[2].data
            c.update(rs=radius_kpc(d['RADIUS'],f[2].columns['RADIUS'].unit,f[2].header),
                     ms=np.array(d['MSTAR'],float))
    return c


def mass_alignment(c, legacy=False):
    rg=c['rg_legacy'] if legacy else c['rg']
    other=loginterp(rg,c['rh'],c['M_NFW'])
    return float(np.nanmedian(abs(c['gas_nfw']/other-1)))


def profiles(clusters, radii, legacy=False, model='M_FORW'):
    gas=np.array([loginterp(radii,c['rg_legacy'] if legacy else c['rg'],c['mg']) for c in clusters])
    stars=np.array([loginterp(radii,c['rs'],c['ms']) if c['has_star'] else np.full(len(radii),np.nan)
                    for c in clusters])
    import_ratio=np.nanmedian(stars/gas,axis=0)
    for i,c in enumerate(clusters):
        if not c['has_star']: stars[i]=gas[i]*import_ratio
    mh=np.array([loginterp(radii,c['rh'],c[model]) for c in clusters])
    return gas,stars,mh


def symbolic_checks():
    y=sp.symbols('y', positive=True)
    excess=y*sp.exp(-y)
    d=sp.factor(sp.diff(excess,y))
    assert sp.simplify(d-(1-y)*sp.exp(-y)) == 0
    critical=sp.solve(d,y)
    assert critical == [sp.Integer(1)]
    assert sp.limit(excess,y,0)==0 and sp.limit(excess,y,sp.oo)==0
    r=sp.symbols('r'); rho=sp.Function('rho')(r)
    gh,gm=sp.Function('gh')(r),sp.Function('gm')(r)
    # Differentiate the implied thermal and nonthermal pressure gradients.
    pth_prime=-rho*gh
    pnt_prime=rho*(gh-gm)
    assert sp.simplify(-(pth_prime+pnt_prime)/rho-gm)==0
    return {'excess_derivative':str(d),'stationary_y':str(critical[0]),
            'maximum_excess_over_a0':str(excess.subs(y,critical[0])),
            'pressure_balance_residual':'0'}


def run():
    clusters=[load_cluster(p.name) for p in sorted(DATA.iterdir()) if p.is_dir()]
    measured=np.array([c['has_star'] for c in clusters])
    relaxed=np.array([c['name'] in RELAXED for c in clusters])
    report={'scope':'central tabulated hydrostatic profiles, not a covariance-aware fit',
            'radii_kpc':RADII.tolist(),'a0_m_s2':A0,'symbolic':symbolic_checks(),
            'radius_audit':[{ 'name':c['name'],'gas_unit':c['gas_unit'],'own_R500_kpc':c['R500'],
                'first_gas_radius_kpc':float(c['rg'][0]),'stellar_file_present':c['has_star'],
                'mass_alignment_corrected':mass_alignment(c),
                'mass_alignment_legacy':mass_alignment(c,True)} for c in clusters],
            'kernels':{}, 'rows':[], 'pressure':[]}
    for legacy in (True,False):
        gas,stars,mh=profiles(clusters,RADII,legacy)
        mb=gas+stars; gb=G*mb*MSUN/(RADII*KPC)**2
        for foot,a0 in A0.items():
            for label,law in [('route_a',route_a_y),('exact_mu',exact_y),('g03r_carrier',carrier_y)]:
                # Keep unsupported radii absent: root solver must not turn NaN into a boundary value.
                pred=np.full_like(gb,np.nan); ok=np.isfinite(gb)
                pred[ok]=a0*law(gb[ok]/a0)
                gh=G*mh*MSUN/(RADII*KPC)**2; eta=gh/pred
                key=f"{'legacy' if legacy else 'corrected'}_{foot}_{label}"
                report['kernels'][key]={
                    'all_12_median':np.nanmedian(eta,axis=0).tolist(),
                    'stellar_file_subset_median':np.nanmedian(eta[measured],axis=0).tolist(),
                    'relaxed_3_median':np.nanmedian(eta[relaxed],axis=0).tolist(),
                    'valid_all':np.sum(np.isfinite(eta),axis=0).tolist(),
                    'valid_stellar_file_subset':np.sum(np.isfinite(eta[measured]),axis=0).tolist()}
                if not legacy and label=='exact_mu':
                    q=source_ratio(gh/a0,mh,mb)
                    for i,c in enumerate(clusters):
                        for j,r in enumerate(RADII):
                            if not np.isfinite(eta[i,j]): continue
                            yobs=gh[i,j]/a0; b=gb[i,j]/a0
                            report['rows'].append({'cluster':c['name'],'footing':foot,'r_kpc':r,
                                'stellar_file_present':c['has_star'],'relaxed_subset':c['name'] in RELAXED,
                                'g_hse_over_a0':yobs,'g_baryon_over_a0':b,'eta_acceleration':eta[i,j],
                                'required_source_mass_ratio':q[i,j],
                                'missing_source_mass_Msun':(q[i,j]-1)*mb[i,j],
                                'excess_bound_ratio':np.e*(yobs-b),
                                'required_outward_acceleration_m_s2':gh[i,j]-pred[i,j],
                                'HSE_multiplicative_factor_for_exact_match':1/eta[i,j],
                                'a0_required_over_adopted':-yobs/np.log1p(-b/yobs) if yobs>b else None})
    # Distinguish reconstruction sensitivity from a statistically calibrated error.
    report['mass_reconstruction_sensitivity_300kpc']={}
    for model in ('M_FORW','M_NFW','M_EIN'):
        gas,stars,mh=profiles(clusters,np.array([300.]),model=model)
        gb=G*(gas+stars)*MSUN/(300*KPC)**2
        eta=G*mh*MSUN/(300*KPC)**2/(A0['canonical']*exact_y(gb/A0['canonical']))
        report['mass_reconstruction_sensitivity_300kpc'][model]=dict(zip([c['name'] for c in clusters],eta[:,0]))
    # A pressure-gradient diagnostic over fixed physical radii. Piecewise log-linear
    # cumulative gas has analytic positive density on each tabulated interval.
    for c in clusters:
        if c['name'] not in RELAXED: continue
        for n in (400,1600):
            rk=np.geomspace(50.,1000.,n); rm=rk*KPC
            mg=loginterp(rk,c['rg'],c['mg']); ms=loginterp(rk,c['rs'],c['ms'])
            mh=loginterp(rk,c['rh'],c['M_FORW'])
            if np.any(~np.isfinite(mg+ms+mh)): raise ValueError('Pressure grid outside profile support')
            idx=np.clip(np.searchsorted(c['rg'],rk,side='right')-1,0,len(c['rg'])-2)
            slope=np.diff(np.log(c['mg']))/np.diff(np.log(c['rg']))
            rho=slope[idx]*mg*MSUN/(4*np.pi*rm**3)
            if np.any(rho<=0): raise ValueError('Nonpositive reconstructed gas density')
            gh=G*mh*MSUN/rm**2; gb=G*(mg+ms)*MSUN/rm**2
            gm=A0['canonical']*exact_y(gb/A0['canonical'])
            entry=pressure_boundary(rm,rho,gh,gm)
            entry.update(cluster=c['name'],grid=n,range_kpc=[50.,1000.],units='Pa')
            report['pressure'].append(entry)
    # Exact counterexample to a universal local-composition ceiling (NOT observed data).
    report['cosmic_ceiling_counterexample']={
        'cluster_fraction_of_total_mass':.02, 'cluster_baryon_fraction':.5,
        'global_baryon_fraction':.16,'rest_baryon_fraction':rest_baryon_fraction(.02,.5,.16),
        'interpretation':'An inventory identity, not a proposed cosmology or hidden-baryon detection'}
    return report


def json_safe(x):
    if isinstance(x,dict): return {k:json_safe(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [json_safe(v) for v in x]
    if isinstance(x,np.generic): x=x.item()
    if isinstance(x,float) and not np.isfinite(x): return None
    return x


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write',action='store_true',help='Write results and computation manifest beside script')
    p.add_argument('--require-central-profile-agreement',action='store_true')
    args=p.parse_args(); start=time.monotonic(); stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    report=run()
    for r in (100,300,1000):
        rows=[x for x in report['rows'] if x['footing']=='canonical' and x['stellar_file_present'] and x['r_kpc']==r]
        print(r,'kpc: N=',len(rows),'median eta=',np.median([x['eta_acceleration'] for x in rows]),
              'median required-source ratio=',np.median([x['required_source_mass_ratio'] for x in rows]))
    selected=[x for x in report['rows'] if x['footing']=='canonical' and x['relaxed_subset'] and x['r_kpc']==300]
    agrees=all(abs(x['eta_acceleration']-1)<1e-6 for x in selected)
    report['central_profile_agreement']={'passes':agrees,'tolerance':1e-6,
        'scope':'three relaxed clusters at 300 kpc, central values; NOT an observational confidence test'}
    print('Central-profile agreement:',agrees)
    status=2 if args.require_central_profile_agreement and not agrees else 0
    if args.write:
        result=HERE/'results.json'; result.write_text(json.dumps(json_safe(report),indent=2,allow_nan=False)+'\n')
        inputs=sorted(DATA.glob('*/*.fits'))
        source_paths=[Path(__file__),HERE/'test_cluster_audit.py',result,
                      ROOT/'hunt_2026/h67b_xcop_core_eta.py',ROOT/'hunt_2026/hunt_lib.py',
                      ROOT/'qwen_claude_field_theory/closure_2026/g03r_converged_collapse_adaptive_shells.py']
        hashed=lambda f:{'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
        manifest={'schema_version':1,'claim_id':'cluster-units-kernel-pressure-audit-2026-09-06',
          'repository':{'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                        'dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True))},
          'command':'OPENBLAS_NUM_THREADS=1 '+str(Path(sys.executable))+' -B '+str(Path(__file__).relative_to(ROOT))+' '+ ' '.join(sys.argv[1:]),
          'environment':{'software':[platform.python_version(),'numpy '+np.__version__,'scipy '+scipy.__version__,
                                      'sympy '+sp.__version__,'astropy '+astropy.__version__],
                         'hardware':platform.machine()},
          'mathematics':{'assertion_tested':'Unit-aware reconstruction, same-mass comparison of three kernels, exact exponential pressure budget',
             'coefficient_domain':'SymPy exact algebra; IEEE754 float64 numerical profiles',
             'conventions':'SI accelerations, kpc radii, Msun masses; own gas FITS R500; no extrapolation',
             'inputs':[hashed(f) for f in inputs], 'bounds':{'radii_kpc':RADII.tolist(),'pressure_grids':[400,1600]},
             'non_claims':['No full theory closure','No statistical rejection from central values','No raw X-ray/SZ re-reduction',
                           'No new mass fit or NFW prior on primary acceleration','No lensing test','No discovery of missing baryons']},
          'randomness':{'used':False,'generator':'','seed':None},
          'run':{'started_at':stamp,'runtime_seconds':time.monotonic()-start,'exit_status':status},
          'outputs':[hashed(f) for f in source_paths],
          'checks':[{'name':'exact symbolic excess bound and pressure identity','passed':True},report['central_profile_agreement']],
          'result':'Conditional central-profile discrepancy survives; prior units/kernel comparison invalid',
          'residual_risks':['Hydrostatic equilibrium, distance and profile systematics','No radial covariance',
                            'Five clusters have imputed stars; seven stellar files are not a proven complete baryon census',
                            'Published distance, NFW radius normalization and stellar modelling are inherited',
                            '30kpc has uneven interpolation support; use >=40kpc comparisons']}
        (HERE/'manifest.json').write_text(json.dumps(json_safe(manifest),indent=2,allow_nan=False)+'\n')
    return status


if __name__=='__main__':
    raise SystemExit(main())

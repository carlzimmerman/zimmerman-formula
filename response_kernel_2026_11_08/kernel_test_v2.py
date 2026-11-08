#!/usr/bin/env python3
"""Amendment A1: fit target amplitudes on the full native graded interval."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar
import kernel_test as base


def main(output, omit_redshift):
    checks = base.exact_checks()
    # n_bar denotes a frozen background; b=-dot(n_bar) in D_i delta n.
    A,z,q,n,b=sp.symbols('A z q n b', positive=True)
    B=A+z*q*q; C=z*b*q*q; D=n*q*q+z*b*b*q*q
    determinant=sp.expand(B*D-C*C)
    assert sp.simplify(determinant-(A*n*q*q+z*n*q**4+A*z*b*b*q*q))==0
    checks['FRW_projected_gradient_frozen_Hessian_determinant']=str(determinant)
    zrec,kcom=1100.,0.3
    qrec=kcom*(1 if omit_redshift else 1+zrec)
    J50=(.05*qrec)**4; bmax=1/J50
    assert abs(((50*base.KPC)*(kcom*(1+zrec)/base.MPC))**4/(.05*kcom*(1+zrec))**4-1)<1e-14
    kernel={'z':zrec,'kcom_max_Mpc_inverse':kcom,'qphysical_max_Mpc_inverse':qrec,
            'physical_wavelength_kpc':[2*math.pi/(k*(1+zrec))*1000 for k in (.3,.03)],
            'Jcap_ell_50kpc':J50,'Jcap_ell_100kpc':(.1*qrec)**4,
            'ell_max_cold_kpc':1000/qrec,'ell_max_10x_gravity_kpc':1000*10**.25/qrec,
            'correct_redshift_check':qrec==330.3}
    clusters=[base.load_cluster(name) for name in base.NAMES]
    results={}
    for footing,a0 in base.A0.items():
        cases={};results[footing]=cases
        for rc_kpc in (50.,75.,100.):
            rc=rc_kpc*base.KPC; per={};pp=[];dd=[];all_residuals=[]
            for cl in clusters:
                rl,mbl,mol=cl['last']; go=base.G*mol*base.MS/(rl*base.KPC)**2
                inferred_outer=(go*go/(go+a0)*(rl*base.KPC)**2/base.G/base.MS-mbl)/mbl
                rnorm=.7*cl['r500_kpc']*base.KPC
                mbnorm=float(cl['baryons'](rnorm/base.KPC))*base.MS
                shapenorm=float(base.enclosed(rnorm,rc,1.))
                def predict(logF,retrows=False):
                    rho0=math.exp(logF)*mbnorm/shapenorm
                    residuals=[];rows=[]
                    for row in cl['rows']:
                        rm=row['r_kpc']*base.KPC; me=float(base.enclosed(rm,rc,rho0))/base.MS
                        mp=float(base.glaw(base.G*(row['Mb_Msun']+me)*base.MS/rm**2,a0))*rm**2/base.G/base.MS
                        d=math.log10(row['Mhse_Msun']/mp);residuals.append(d)
                        rows.append(dict(row,MX_Msun=me,Mpred_Msun=mp,delta_dex=d))
                    return (rho0,np.array(residuals),rows) if retrows else float(np.mean(np.array(residuals)**2))
                opt=minimize_scalar(predict,bounds=(-8.,math.log(30.)),method='bounded',options={'xatol':1e-10})
                assert opt.success
                rho0,residuals,rows=predict(opt.x,True);all_residuals.extend(residuals)
                r=np.geomspace(20.,.7*cl['r500_kpc'],120)*base.KPC
                mb=cl['baryons'](r/base.KPC,extrapolate=True)*base.MS
                mx=base.enclosed(r,rc,rho0)
                g=base.glaw(base.G*(mb+mx)/r**2,a0)
                _,p,_,d=base.density_functions(r,rc,rho0)
                p=base.AREF*p/g;d=base.ZREF*d/g;pp.extend(p);dd.extend(d)
                free=base.fit_support(p,d);bounded=base.fit_support(p,d,bmax)
                free['Jcap_recombination']=free['zeta_over_Zref']*J50
                bounded['Jcap_recombination']=bounded['zeta_over_Zref']*J50
                conc=float(base.enclosed(.25*cl['r500_kpc']*base.KPC,rc,rho0)/base.enclosed(rnorm,rc,rho0))
                per[cl['name']]={'F_at_0p7R500':math.exp(opt.x),'normalization_radius_kpc':rnorm/base.KPC,
                    'MX_at_0p7R500_Msun':math.exp(opt.x)*mbnorm/base.MS,
                    'original_outer_radius_kpc':rl,'original_outer_inferred_F':inferred_outer,
                    'target_mass_rms_dex':float(np.sqrt(np.mean(residuals**2))),
                    'concentration':conc,'rho0_kg_m3':rho0,'free_fit':free,'CMB_bounded_fit':bounded,
                    'max_cap_fraction_at_CMB_bound':float(np.max(abs(bmax*d))),
                    'max_cap_fraction_at_10x_gravity_bound':float(10*np.max(abs(bmax*d))),
                    'full_native_mass_rows':rows}
            pp,dd=np.array(pp),np.array(dd)
            free,bounded=base.fit_support(pp,dd),base.fit_support(pp,dd,bmax)
            free['Jcap_recombination']=free['zeta_over_Zref']*J50
            bounded['Jcap_recombination']=bounded['zeta_over_Zref']*J50
            b10=.1/np.max(abs(dd))
            cases[str(int(rc_kpc))]={'common_free_fit':free,'common_CMB_bounded_fit':bounded,
                'Jcap_for_10percent_cap_force_somewhere':float(b10*J50),
                'ell_for_10percent_cap_force_somewhere_kpc':50*b10**.25,
                'target_mass_rms_dex':float(np.sqrt(np.mean(np.array(all_residuals)**2))),
                'native_mass_points':len(all_residuals),'inverse_equilibrium_points':len(pp),'clusters':per}
    cases=[c for f in results.values() for c in f.values()]
    maximum=max(p['max_cap_fraction_at_CMB_bound'] for c in cases for p in c['clusters'].values())
    minimum_J=min(c['Jcap_for_10percent_cap_force_somewhere'] for c in cases)
    summary={'largest_cap_fraction_under_CMB_bound':maximum,
             'least_Jcap_for_10percent_change':minimum_J,
             'prescreen_relevance_line':.1,'coldness_line':1.,
             'constant_coefficient_prescreen_survives':maximum>=.1,
             'mutation_omits_redshift':omit_redshift,
             'coverage':{'clusters':7,'footings':2,'core_radii':3,'target_profiles':42,
                         'inverse_equilibrium_points':sum(c['inverse_equilibrium_points'] for c in cases),
                         'native_mass_rows_across_core_grid':sum(c['native_mass_points'] for c in cases)}}
    hashes=[]
    for name in base.NAMES:
        for suffix in ('hydro_mass','fgas_profile','mstar'):
            path=base.DATA/name/f'{name}_{suffix}.fits'
            hashes.append({'path':str(path.relative_to(base.ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    result={'assertion_tested':'CONTRACT.txt as amended by CONTRACT_V2.txt; necessary inverse equilibrium only',
            'controls':checks,'kernel':kernel,'profiles':results,'summary':summary,'raw_inputs':hashes}
    (base.ROOT/output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'kernel':kernel,'summary':summary},indent=2))
    for ft, cs in results.items():
        for rc,c in cs.items():
            print(ft,rc,json.dumps({'free':c['common_free_fit'],'CMB_bounded':c['common_CMB_bounded_fit'],
                                   'target_mass_rms_dex':c['target_mass_rms_dex']}))
    assert kernel['correct_redshift_check'] != omit_redshift


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--omit-redshift',action='store_true');args=parser.parse_args()
    main(args.output,args.omit_redshift)

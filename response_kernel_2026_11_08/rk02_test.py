#!/usr/bin/env python3
"""RK02: exact auxiliary portal and its complete capillary force."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp
from kernel_test_v3 import scalar_fit
import kernel_test as base


def symbolic_checks():
    B,m,g,n,lam,p=sp.symbols('B m g n lam p',positive=True)
    L=(m*m+g*n)*B*B/2-lam*B*p
    Bs=lam*p/(m*m+g*n)
    assert sp.simplify(L.subs(B,Bs)+lam*lam*p*p/(2*(m*m+g*n)))==0
    # Convex perspective Hessian in (rho, one gradient component).
    r,t,a,b=sp.symbols('r t a b',positive=True)
    E=p*p/(2*(1+r/t))
    H=sp.hessian(E,(r,p))
    v=sp.Matrix([a,b])
    expected=(b-p*a/(t+r))**2/(1+r/t)
    assert sp.simplify((v.T*H*v)[0]-expected)==0
    x,rc,r0,z0=sp.symbols('x rc r0 z0',positive=True)
    rho=r0/(1+x*x); first=sp.diff(rho,x)/rc
    second=sp.diff(first,x)/rc;lap=second+2*first/(rc*x)
    z=z0/(1+rho/t);zp=-z0/t/(1+rho/t)**2;zpp=2*z0/t**2/(1+rho/t)**3
    mu=-z*lap-zp*first*first/2
    full=z*sp.diff(lap,x)/rc+zp*first*(lap+second)+zpp*first**3/2
    assert sp.simplify(-sp.diff(mu,x)/rc-full)==0
    mutation=sp.simplify(full-z*sp.diff(lap,x)/rc)
    mutation_value=float(mutation.subs({x:1,rc:1,r0:1,t:1,z0:1}))
    assert abs(mutation_value)>1e-4
    # rho_t->0 at fixed zeta0*rho_t = kappa gives Fisher pressure.
    kapp=sp.symbols('kapp',positive=True)
    fisher=sp.limit(full.subs(z0,kapp/t),t,0,dir='+')
    assert sp.simplify(fisher-24*kapp*x/(rc**3*(1+x*x)**3))==0
    return {'auxiliary_elimination':True,'positive_gradient_Hessian':str(expected),
            'complete_force_identity':True,'omitted_density_derivatives_mutation':mutation_value,
            'Fisher_limit_force':str(fisher)}


def main(out):
    folder=Path(__file__).resolve().parent
    targets=json.loads((folder/'run_v3/results.json').read_text())
    fitpaths=[base.ROOT/'closure_2026_11_07/F1A_primary_cmb_audit/parts'/f'fit_B2_{f}_cold.json' for f in ('canonical','alt')]
    omega_b=[json.loads(p.read_text())['pars']['ob'] for p in fitpaths]
    rhoc100=3*(1e5/base.MPC)**2/(8*math.pi*base.G)
    rhorec=[5.4*o*rhoc100*1101**3 for o in omega_b]
    qrec=330.3;Jref=(.05*qrec)**4
    clusters={name:base.load_cluster(name) for name in base.NAMES}
    controls=symbolic_checks();cases={}
    for foot,cs in targets['profiles'].items():
        cases[foot]={};a0=base.A0[foot]
        for rcstr,target in cs.items():
            rc=float(rcstr)*base.KPC
            allrho=[];allp=[];allsecond=[];alllap=[];alllapprime=[];allgrav=[]
            for name,clt in target['clusters'].items():
                cl=clusters[name];r=np.geomspace(20.,.7*cl['r500_kpc'],120)*base.KPC
                rho0=clt['rho0_kg_m3'];x=r/rc
                rho,negp,lap,lp=base.density_functions(r,rc,rho0);p=-negp
                second=2*rho0*(3*x*x-1)/(rc*rc*(1+x*x)**3)
                mb=cl['baryons'](r/base.KPC,extrapolate=True)*base.MS
                mx=base.enclosed(r,rc,rho0);grav=base.glaw(base.G*(mb+mx)/r**2,a0)
                for accumulator,values in [(allrho,rho),(allp,p),(allsecond,second),(alllap,lap),(alllapprime,lp),(allgrav,grav)]:
                    accumulator.extend(values)
            rho,p,second,lap,lp,grav=map(np.array,(allrho,allp,allsecond,alllap,alllapprime,allgrav))
            pp=-base.AREF*p/grav
            rows=[]
            for rt in np.geomspace(1e-30,1e-19,45):
                den=1+rho/rt
                cap=lp/den-p*(lap+second)/(rt*den**2)+p**3/(rt**2*den**3)
                dd=base.ZREF*cap/grav
                bmax=(1+max(rhorec)/rt)/Jref
                free=scalar_fit(pp,dd);bounded=scalar_fit(pp,dd,bmax)
                for fit in (free,bounded):
                    bcoef=fit['zeta_over_Zref']
                    fit['Jcap_recombination_bracket']=[bcoef*Jref/(1+rr/rt) for rr in rhorec]
                rows.append({'rho_t_kg_m3':float(rt),'free':free,'CMB_bounded':bounded})
            # Frozen asymptotic controls: constant and Fisher-force shapes.
            const=scalar_fit(pp,base.ZREF*lp/grav)
            expected=target['common_free_fit']
            assert abs(const['A_over_Aref']-expected['A_over_Aref'])<1e-10
            assert abs(const['zeta_over_Zref']-expected['zeta_over_Zref'])<1e-10
            best=min(rows,key=lambda row:row['CMB_bounded']['fractional_support_rms'])
            cases[foot][rcstr]={'best_on_grid':best,'rows':rows,
                               'constant_limit_matches_RK01':True,
                               'fractional_force_tolerance':.10,
                               'passes_inverse_equilibrium_prescreen':best['CMB_bounded']['fractional_support_rms']<=.10}
    allcases=[c for cs in cases.values() for c in cs.values()]
    summary={'rho_t_grid_size':45,'parameter_core_footing_cells':45*len(allcases),
             'best_fractional_support_rms':min(c['best_on_grid']['CMB_bounded']['fractional_support_rms'] for c in allcases),
             'passing_cases':sum(c['passes_inverse_equilibrium_prescreen'] for c in allcases),
             'all_free_fits_choose_zero_capillary':all(row['free']['zeta_over_Zref']==0 for c in allcases for row in c['rows']),
             'status':'finite_target_family_test; not a proof for every rho_t or every allowed cluster profile'}
    result={'controls':controls,'native_omega_b_interval':omega_b,'rho_X_recombination_kg_m3_bracket':rhorec,
            'profiles':cases,'summary':summary}
    (base.ROOT/out).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'controls':controls,'rho_X_recombination_kg_m3_bracket':rhorec,'summary':summary},indent=2))
    for foot,cs in cases.items():
        for rc,c in cs.items():print(foot,rc,json.dumps(c['best_on_grid']))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)

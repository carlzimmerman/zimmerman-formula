#!/usr/bin/env python3
"""RK03 boundary refinement and defect-controlled nonlinear galaxies."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
import rk03_test as m
from rk03_run import numpy_scalar


def nonlinear(gal,fit,lam,rt,rhomean,ngrid=800):
    s2=fit['s2_over_SREF']*m.SREF;v2=fit['v2_over_VREF']*m.VREF
    r=np.r_[0.,np.geomspace(.01,max(20*lam,1500.),ngrid-1)]
    dep=np.interp(r,gal['rgrid'],gal['depth'],left=gal['depth'][0],right=0.)
    pinf=rt/(rt+rhomean);m2=1/lam**2
    z=r[1:-1]*pinf;zlast=r[-1]*pinf
    lo,di,up=m.radial_matrix(r,np.full_like(r,m2))
    status='iteration_limit';last_effect=None
    for it in range(150):
        p=z/r[1:-1]
        ex=(dep[1:-1]-.5*v2*(pinf*pinf-p*p))/s2
        if np.max(ex)>500:return {'status':'exponent_range','iterations':it}
        rho=rhomean*np.exp(ex)
        residual=(di+m2*rho/rt)*z+lo*np.r_[0.,z[:-1]]+up*np.r_[z[1:],zlast]-m2*r[1:-1]
        jac=di+m2*rho/rt*(1+v2*p*p/s2)
        step=m.band_solve(lo,jac,up,-residual)
        effect=float(np.max(abs(v2*p*step/(s2*r[1:-1]))))
        field=float(np.max(abs(step)/np.maximum(abs(z),r[1:-1]*1e-10)))
        last_effect=effect
        if effect<1e-8 and field<1e-8:
            z+=step;status='converged';break
        # Monotone scalar equation: damp only to retain 0<p<=1 and control
        # the maximum change in log density, not the ill-conditioned FD sum.
        fraction=min(1.,2./max(effect,1e-100))
        for _ in range(50):
            trial=z+fraction*step;pt=trial/r[1:-1]
            if np.min(pt)>0 and np.max(pt)<=1:
                et=(dep[1:-1]-.5*v2*(pinf*pinf-pt*pt))/s2
                if np.max(et)<500:
                    z=trial;break
            fraction*=.5
        else:return {'status':'bounds_line_search_failed','iterations':it,'density_correction':effect}
    if status!='converged':return {'status':status,'iterations':it,'density_correction':last_effect}
    pp=np.r_[z[0]/r[1],z/r[1:-1],pinf]
    logrho=(dep-.5*v2*(pinf*pinf-pp*pp))/s2
    density=rhomean*np.exp(logrho)
    independent,_,er=m.vector_field(r,density,lam,rt,rhomean)
    defect=float(np.max(abs(.5*v2*(independent**2-pp**2)/s2)))
    if defect>1e-5:return {'status':'independent_field_defect','defect_logrho':defect,'iterations':it}
    mass=cumulative_trapezoid(4*math.pi*(r*m.base.KPC)**2*(density-rhomean),r*m.base.KPC,initial=0.)
    ratios={key:float(np.interp(rad,r,mass))/(5.4*gal['Mb_Msun']*m.base.MS)
            for key,rad in [('disc',gal['last_kpc']),('halo100',100.),('halo300',300.)]}
    return {'status':'converged','iterations':it,'defect_logrho':defect,
            'mass_ratios':ratios,'grid_points':ngrid,'central_overdensity':float(density[0]/rhomean)}


def setup():
    here=Path(__file__).resolve().parent
    target=json.loads((here/'run_v3/results.json').read_text())
    paths=[m.base.ROOT/'closure_2026_11_07/F1A_primary_cmb_audit/parts'/f'fit_B2_{f}_cold.json' for f in ('canonical','alt')]
    ob=[json.loads(p.read_text())['pars']['ob'] for p in paths]
    rhoc=3*(1e5/m.base.MPC)**2/(8*math.pi*m.base.G)
    means=[5.4*x*rhoc for x in ob]
    cls={n:m.base.load_cluster(n) for n in m.base.NAMES}
    return target,means,cls


def evaluate(foot,rc,lam,rt,target,rhomean,cls,ngrid=800):
    t=target['profiles'][foot][str(int(rc))];a0=m.base.A0[foot]
    rmax=max(20*lam,max(5*c['r500_kpc'] for c in cls.values()))
    grid=np.r_[0.,np.geomspace(.01,rmax,ngrid-1)]
    allp=[];alld=[];per={};columns={}
    for name,ct in t['clusters'].items():
        cl=cls[name];r=np.geomspace(20.,.7*cl['r500_kpc'],120);r0=ct['rho0_kg_m3']
        mb=cl['baryons'](r,extrapolate=True)*m.base.MS
        mx=m.base.enclosed(r*m.base.KPC,rc*m.base.KPC,r0)
        grav=m.base.glaw(m.base.G*(mb+mx)/(r*m.base.KPC)**2,a0)
        bulk=m.SREF*2*r/((rc*rc+r*r)*m.base.KPC)/grav
        dens=np.where(grid<=2*cl['r500_kpc'],r0/(1+(grid/rc)**2)+rhomean,rhomean)
        pf,dp,er=m.vector_field(grid,dens,lam,rt,rhomean)
        force=m.VREF*np.interp(r,grid,pf*dp)/m.base.KPC/grav
        allp.extend(bulk);alld.extend(force);per[name]=m.boxfit(bulk,force)
        columns[name]=(bulk,force)
    fit=m.boxfit(np.array(allp),np.array(alld))
    # Per-host residuals under the common fitted coefficients, not per-host fits.
    fit['per_cluster_fractional_rms']={name:float(np.sqrt(np.mean((fit['s2_over_SREF']*p+fit['v2_over_VREF']*d-1)**2))) for name,(p,d) in columns.items()}
    return {'footing':foot,'rc_kpc':rc,'lambda0_kpc':lam,'rho_t_kg_m3':float(rt),
            'common_fit':fit,'per_cluster_diagnostic_fits':per,'grid_points':ngrid}


def main(output):
    target,means,cls=setup();rhomean=min(means)
    gals=m.sparc_inputs();gps={f:m.galaxy_potentials(gals,a) for f,a in m.base.A0.items()}
    cells=[]
    for f in m.base.A0:
        for rc in (50.,75.,100.):
            for lam in (1000.,2000.,3000.,6000.,10000.,20000.,30000.):
                for rt in np.geomspace(1e-26,1e-22,17):
                    c=evaluate(f,rc,lam,rt,target,rhomean,cls)
                    c['cmb_bracket']=[m.cmb_test(c['common_fit'],lam,rt,r) for r in means]
                    c['galaxy_lower_bound']=m.galaxy_lower_bounds(gps[f],c['common_fit'],rt,rhomean)
                    cells.append(c)
    selected=[]
    for f in m.base.A0:
        best=min((c for c in cells if c['footing']==f),key=lambda c:c['common_fit']['fractional_force_rms'])
        ref=[evaluate(f,best['rc_kpc'],best['lambda0_kpc'],best['rho_t_kg_m3'],target,rhomean,cls,n) for n in (1600,3200)]
        # Use finest audited coefficients for all galaxy calculations.
        fit=ref[-1]['common_fit'];galrows=[]
        for gal in gps[f]:
            sol=nonlinear(gal,fit,best['lambda0_kpc'],best['rho_t_kg_m3'],rhomean)
            galrows.append({'name':gal['name'],'Mb_Msun':gal['Mb_Msun'],'solution':sol})
        worst={}
        for key in ('disc','halo100','halo300'):
            eligible=[g for g in galrows if g['solution']['status']=='converged' and (key=='disc' or g['Mb_Msun']>=1e10)]
            worst[key]=max(eligible,key=lambda g:g['solution']['mass_ratios'][key]) if eligible else None
        refinements={}
        for name in sorted({g['name'] for g in worst.values() if g is not None}):
            gal=next(g for g in gps[f] if g['name']==name)
            refinements[name]=[nonlinear(gal,fit,best['lambda0_kpc'],best['rho_t_kg_m3'],rhomean,n) for n in (1600,3200)]
        selected.append({'best_coarse_case':best,'cluster_refinements':ref,'nonlinear_galaxies':galrows,
                         'worst_galaxies':worst,'galaxy_refinements':refinements})
    summary={'cells':len(cells),'best_cluster_force_rms':min(c['common_fit']['fractional_force_rms'] for c in cells),
             'cluster_passing_cells':sum(c['common_fit']['fractional_force_rms']<=.1 for c in cells),
             'galaxy_counts_by_footing':{s['best_coarse_case']['footing']:{status:sum(g['solution']['status']==status for g in s['nonlinear_galaxies']) for status in sorted({g['solution']['status'] for g in s['nonlinear_galaxies']})} for s in selected}}
    result={'summary':summary,'selected':selected,'cases':cells,
            'scope':'same action, refined parameter grid; fixed-potential galaxy equilibria, not formation'}
    (m.base.ROOT/output).write_text(json.dumps(result,indent=2,allow_nan=False,default=numpy_scalar)+'\n')
    print(json.dumps(summary,indent=2,default=numpy_scalar))
    for s in selected:
        print(json.dumps({'best':s['best_coarse_case'],'cluster_refinements':s['cluster_refinements'],
                          'worst_galaxies':s['worst_galaxies'],'galaxy_refinements':s['galaxy_refinements']},indent=2,default=numpy_scalar))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    main(p.parse_args().output)

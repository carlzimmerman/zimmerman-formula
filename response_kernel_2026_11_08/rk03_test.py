#!/usr/bin/env python3
"""RK03 classical current-coupled vector; static/quasistatic prescreens."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import cumulative_trapezoid
from scipy.linalg import solve_banded
import kernel_test as base

SREF=(500e3)**2
VREF=(1000e3)**2
C=299792458.


def boxfit(p,d):
    p,d=np.asarray(p),np.asarray(d)
    dot=lambda a,b:math.fsum(float(x)*float(y) for x,y in zip(a,b))
    pp,dd,pd=dot(p,p),dot(d,d),dot(p,d)
    py,dy=math.fsum(p),math.fsum(d)
    alo,ahi,blo,bhi=(10/500)**2,(3000/500)**2,0.,(10000/1000)**2
    cand=[]
    clamp=lambda x,l,h:max(l,min(h,x))
    for a in (alo,ahi):cand.append((a,clamp((dy-a*pd)/dd,blo,bhi)))
    for b in (blo,bhi):cand.append((clamp((py-b*pd)/pp,alo,ahi),b))
    det=pp*dd-pd*pd
    if det>1e-12*pp*dd:
        a=(py*dd-dy*pd)/det;b=(dy*pp-py*pd)/det
        if alo<=a<=ahi and blo<=b<=bhi:cand.append((a,b))
    def loss(ab):return math.fsum((ab[0]*float(x)+ab[1]*float(y)-1)**2 for x,y in zip(p,d))
    a,b=min(cand,key=loss)
    support=a*p+b*d
    return {'s2_over_SREF':a,'v2_over_VREF':b,'sigma_km_s':500*math.sqrt(a),
            'v_km_s':1000*math.sqrt(b),'fractional_force_rms':math.sqrt(loss((a,b))/len(p)),
            'log10_force_rms':float(np.sqrt(np.mean(np.log10(support)**2))) if np.all(support>0) else None}


def radial_matrix(r,k2):
    hp=r[1:-1]-r[:-2];hn=r[2:]-r[1:-1]
    lower=-2/(hp*(hp+hn));upper=-2/(hn*(hp+hn))
    diag=2/(hp*hn)+k2[1:-1]
    return lower,diag,upper


def band_solve(lower,diag,upper,rhs):
    ab=np.zeros((3,len(diag)));ab[0,1:]=upper[:-1];ab[1]=diag;ab[2,:-1]=lower[1:]
    return solve_banded((1,1),ab,rhs,check_finite=True)


def vector_field(r,rho,lam,rt,rhomean):
    # p=1-u; z=r*p. (-d_r^2 + k^2) z=m0^2*r.
    m2=1/lam**2;k2=m2*(1+rho/rt)
    lower,diag,upper=radial_matrix(r,k2)
    pinf=rt/(rt+rhomean);zlast=r[-1]*pinf
    rhs=m2*r[1:-1];rhs[-1]-=upper[-1]*zlast
    zi=band_solve(lower,diag,upper,rhs)
    z=np.r_[0.,zi,zlast];p=np.empty_like(r);p[1:]=z[1:]/r[1:];p[0]=p[1]
    dp=np.gradient(p,r,edge_order=2)
    resid=diag*zi+lower*np.r_[0.,zi[:-1]]+upper*np.r_[zi[1:],zlast]-m2*r[1:-1]
    denominator=np.abs(diag*zi)+np.abs(lower*np.r_[0.,zi[:-1]])+np.abs(upper*np.r_[zi[1:],zlast])+np.abs(m2*r[1:-1])
    err=float(np.max(abs(resid)/np.maximum(denominator,1e-100)))
    assert err<1e-10
    assert np.min(p)>-1e-8 and np.max(p)<1+1e-6
    return p,dp,err


def exact_checks():
    rho,m,e,eta,q=sp.symbols('rho m e eta q',positive=True)
    b=e*rho/(m*m+eta*rho)
    energy=e*e*rho*rho/(2*(m*m+eta*rho))
    h=e*b-eta*b*b/2
    assert sp.simplify(sp.diff(energy,rho)-h)==0
    e_eff=e-eta*b
    assert sp.simplify(sp.diff(h,rho)-e_eff**2/(m*m+eta*rho))==0
    assert sp.simplify(e_eff-e*m*m/(m*m+eta*rho))==0
    wrong=sp.simplify(sp.diff(e*b,rho)-sp.diff(h,rho))
    assert float(wrong.subs({rho:1,m:1,e:1,eta:1}))!=0
    rr=np.r_[0.,np.geomspace(.01,10000.,799)]
    pp,dp,er=vector_field(rr,np.full_like(rr,2e-27),100.,1e-26,2e-27)
    err=float(np.max(abs(pp-1/1.2)))
    assert err<1e-6
    return {'homogeneous_energy_derivative':True,'effective_charge_identity':True,
            'homogeneous_hessian':str(sp.factor(sp.diff(h,rho))),
            'omitted_mass_derivative_mutation':float(wrong.subs({rho:1,m:1,e:1,eta:1})),
            'uniform_field_max_absolute_error':err,'uniform_matrix_residual':er}


def sparc_inputs():
    data=base.ROOT/'real_research/data';quality={};inclination={}
    for line in (data/'SPARC_Lelli2016c.mrt').read_text().splitlines():
        t=line.split()
        if len(t)<18:continue
        try:quality[t[0]]=int(t[17]);inclination[t[0]]=float(t[5])
        except ValueError:continue
    out=[]
    for path in sorted((data/'sparc_data').glob('*_rotmod.dat')):
        name=path.name[:-11]
        if name not in quality or quality[name]>2 or inclination[name]<30:continue
        z=np.atleast_2d(np.loadtxt(path,comments='#'))
        r,v,ev,vg,vd,vb=(z[:,i] for i in range(6))
        vb2=np.sign(vg)*vg**2+.5*np.sign(vd)*vd**2+.7*np.sign(vb)*vb**2
        ok=(v>0)&(ev/np.maximum(v,1e-9)<=.1)&(vb2>0)&(r>0)
        if np.sum(ok)<2:continue
        r=r[ok];v=v[ok];vb2=vb2[ok]
        mb=float(vb2[-1]*1e6*r[-1]*base.KPC/base.G/base.MS)
        out.append({'name':name,'r_kpc':r,'gobs':v*v*1e6/(r*base.KPC),
                    'Mb_Msun':mb,'last_kpc':float(r[-1]),'path':str(path.relative_to(base.ROOT))})
    return out


def galaxy_potentials(gals,a0):
    ans=[]
    for gal in gals:
        r=np.geomspace(min(.1,gal['r_kpc'][0]),300.,240)
        observed=np.interp(np.log(r),np.log(gal['r_kpc']),np.log(gal['gobs']))
        gn=base.G*gal['Mb_Msun']*base.MS/(r*base.KPC)**2
        gravity=np.where(r<=gal['last_kpc'],np.exp(observed),base.glaw(gn,a0))
        gravity=np.where(r<gal['r_kpc'][0],0.,gravity) # omit unresolved inner depth, favor exclusion
        integrated=cumulative_trapezoid(gravity,r*base.KPC,initial=0.)
        depth=integrated[-1]-integrated
        ans.append(dict(gal,rgrid=r,depth=depth))
    return ans


def galaxy_lower_bounds(gals,fit,rt,rhomean):
    s2=fit['s2_over_SREF']*SREF;v2=fit['v2_over_VREF']*VREF
    barrier=.5*v2*(rt/(rt+rhomean))**2
    worst={'disc':(-1e300,None),'halo100':(-1e300,None),'halo300':(-1e300,None)}
    failures={k:0 for k in worst};n={k:0 for k in worst}
    for gal in gals:
        r=gal['rgrid'];exponent=(gal['depth']-barrier)/s2
        # If clipped, the bound is still a lower bound, never an optimistic density cap.
        rho=rhomean*np.exp(np.minimum(exponent,100.))
        integrand=4*math.pi*(r*base.KPC)**2*(rho-rhomean)
        mass=cumulative_trapezoid(integrand,r*base.KPC,initial=0.)
        mass-=4*math.pi/3*(r[0]*base.KPC)**3*rhomean
        for key,aperture in [('disc',gal['last_kpc']),('halo100',100.),('halo300',300.)]:
            if key!='disc' and gal['Mb_Msun']<1e10:continue
            val=float(np.interp(aperture,r,mass))/(5.4*gal['Mb_Msun']*base.MS)
            n[key]+=1;failures[key]+=val>.01
            if val>worst[key][0]:worst[key]=(val,gal['name'])
    return {'barrier_m2_s2':barrier,'max_lower_bound_ratio':{k:v[0] for k,v in worst.items()},
            'worst_names':{k:v[1] for k,v in worst.items()},'failures':failures,'counts':n,
            'scope':'only failures of the lower bound reject; passing is not a nonlinear galaxy pass'}


def cmb_test(fit,lam,rt,rhomean):
    rhorec=rhomean*1101**3;q=330.3/base.MPC;m2=1/(lam*base.KPC)**2
    s2=fit['s2_over_SREF']*SREF;v2=fit['v2_over_VREF']*VREF
    alphaeff=v2*m2/(4*math.pi*base.G*rt)/(1+rhorec/rt)**2
    Jbulk=s2*q*q/(4*math.pi*base.G*rhorec)
    Jrep=alphaeff*q*q/(q*q+m2*(1+rhorec/rt))
    Jold=(330.3/8.89e6)**2
    fraction=.5*v2/C**2*rhorec/(rhorec+rt)
    return {'Jbulk':Jbulk,'Jrepulsive':Jrep,'Joriginal':Jold,'Jtotal':Jbulk+Jrep+Jold,
            'homogeneous_vector_energy_fraction':fraction,
            'coldness_pass':Jbulk+Jrep+Jold<=1,'background_fraction_pass':fraction<=.01,
            'scope':'quasistatic necessary test, no CMB spectrum'}


def nonlinear_galaxy(gal,fit,lam,rt,rhomean,ngrid=800):
    s2=fit['s2_over_SREF']*SREF;v2=fit['v2_over_VREF']*VREF
    rr=np.r_[0.,np.geomspace(.01,max(20*lam,1500.),ngrid-1)]
    depth=np.interp(rr,gal['rgrid'],gal['depth'],left=gal['depth'][0],right=0.)
    pinf=rt/(rt+rhomean);m2=1/lam**2
    zi=rr[1:-1]*pinf;zlast=rr[-1]*pinf
    lo,di,up=radial_matrix(rr,np.full_like(rr,m2))
    lastnorm=None
    for it in range(100):
        p=zi/rr[1:-1]
        exponent=(depth[1:-1]-.5*v2*(pinf*pinf-p*p))/s2
        if np.max(exponent)>500:
            return {'status':'density_exponent_exceeds_numeric_range','iterations':it}
        rho=rhomean*np.exp(exponent)
        residual=(di+m2*rho/rt)*zi+lo*np.r_[0.,zi[:-1]]+up*np.r_[zi[1:],zlast]-m2*rr[1:-1]
        scale=np.maximum(abs(di*zi)+abs(lo*np.r_[0.,zi[:-1]])+abs(up*np.r_[zi[1:],zlast])+m2*rr[1:-1],1e-100)
        norm=float(np.max(abs(residual)/scale))
        if norm<1e-10:break
        jac=di+m2*rho/rt*(1+v2*p*p/s2)
        step=band_solve(lo,jac,up,-residual)
        fraction=1.
        for _ in range(40):
            trial=zi+fraction*step;pt=trial/rr[1:-1]
            if np.min(pt)>=0 and np.max(pt)<=1:
                et=(depth[1:-1]-.5*v2*(pinf*pinf-pt*pt))/s2
                if np.max(et)<500:
                    rhot=rhomean*np.exp(et)
                    res=(di+m2*rhot/rt)*trial+lo*np.r_[0.,trial[:-1]]+up*np.r_[trial[1:],zlast]-m2*rr[1:-1]
                    if np.max(abs(res)/scale)<norm:
                        zi=trial;break
            fraction*=.5
        else:return {'status':'line_search_failed','iterations':it,'residual':norm}
    else:return {'status':'iteration_limit','iterations':100,'residual':norm}
    pp=np.r_[zi[0]/rr[1],zi/rr[1:-1],pinf]
    logrho=(depth-.5*v2*(pinf*pinf-pp*pp))/s2
    density=rhomean*np.exp(logrho)
    mass=cumulative_trapezoid(4*math.pi*(rr*base.KPC)**2*(density-rhomean),rr*base.KPC,initial=0.)
    ratios={key:float(np.interp(rad,rr,mass))/(5.4*gal['Mb_Msun']*base.MS)
            for key,rad in [('disc',gal['last_kpc']),('halo100',100.),('halo300',300.)]}
    return {'status':'converged','iterations':it,'residual':norm,'mass_ratios':ratios,
            'grid_points':ngrid,'central_overdensity':float(density[0]/rhomean),
            'scope':'fixed native potential with a conservative 300-kpc truncation; not formation or self-gravity evolution'}


def main(output):
    here=Path(__file__).resolve().parent
    target=json.loads((here/'run_v3/results.json').read_text())
    fitpaths=[base.ROOT/'closure_2026_11_07/F1A_primary_cmb_audit/parts'/f'fit_B2_{f}_cold.json' for f in ('canonical','alt')]
    ob=[json.loads(p.read_text())['pars']['ob'] for p in fitpaths]
    rhoc=3*(1e5/base.MPC)**2/(8*math.pi*base.G);rhobars=[5.4*x*rhoc for x in ob]
    rhomean=min(rhobars) # favorable lower bound on galaxy accumulation
    controls=exact_checks()
    cls={n:base.load_cluster(n) for n in base.NAMES};gals=sparc_inputs()
    galpot={f:galaxy_potentials(gals,a) for f,a in base.A0.items()}
    cases=[];worstmat=0.
    for foot,cs in target['profiles'].items():
        a0=base.A0[foot]
        for rcstr,targ in cs.items():
            rc=float(rcstr);packed={}
            for name,clt in targ['clusters'].items():
                cl=cls[name];r=np.geomspace(20.,.7*cl['r500_kpc'],120)
                rho0=clt['rho0_kg_m3'];rho=rho0/(1+(r/rc)**2)
                mb=cl['baryons'](r,extrapolate=True)*base.MS
                mx=base.enclosed(r*base.KPC,rc*base.KPC,rho0)
                grav=base.glaw(base.G*(mb+mx)/(r*base.KPC)**2,a0)
                bulk=SREF*2*r/((rc*rc+r*r)*base.KPC)/grav
                packed[name]=(cl,r,rho0,grav,bulk)
            for lam in (1.,3.,10.,30.,100.,300.,1000.,3000.):
                rmax=max(20*lam,max(5*c['r500_kpc'] for c in cls.values()))
                grid=np.r_[0.,np.geomspace(.01,rmax,799)]
                for rt in np.geomspace(1e-29,1e-20,10):
                    allp=[];alld=[];per={}
                    for name,(cl,r,rho0,grav,bulk) in packed.items():
                        dens=np.where(grid<=2*cl['r500_kpc'],rho0/(1+(grid/rc)**2)+rhomean,rhomean)
                        pf,dp,er=vector_field(grid,dens,lam,rt,rhomean);worstmat=max(worstmat,er)
                        force=VREF*np.interp(r,grid,pf*dp)/base.KPC/grav
                        allp.extend(bulk);alld.extend(force)
                        per[name]=boxfit(bulk,force)
                    fit=boxfit(np.array(allp),np.array(alld))
                    cm=[cmb_test(fit,lam,rt,rb) for rb in rhobars]
                    gal=galaxy_lower_bounds(galpot[foot],fit,rt,rhomean)
                    cases.append({'footing':foot,'rc_kpc':rc,'lambda0_kpc':lam,'rho_t_kg_m3':float(rt),
                                  'common_fit':fit,'per_cluster_diagnostic_fits':per,'cmb_bracket':cm,
                                  'galaxy_lower_bound':gal,'cluster_prescreen_pass':fit['fractional_force_rms']<=.1})
    selected=[]
    for foot in base.A0:
        best=min((c for c in cases if c['footing']==foot),key=lambda x:x['common_fit']['fractional_force_rms'])
        probes=[]
        # Probe the strongest potential, the largest baryon mass, and the worst
        # lower-bound disc/halo objects, de-duplicated, under the SAME parameters.
        gp=galpot[foot]
        names={max(gp,key=lambda g:g['depth'][0])['name'],max(gp,key=lambda g:g['Mb_Msun'])['name']}
        names.update(best['galaxy_lower_bound']['worst_names'].values())
        for name in sorted(names):
            gal=next(g for g in gp if g['name']==name)
            sol=nonlinear_galaxy(gal,best['common_fit'],best['lambda0_kpc'],best['rho_t_kg_m3'],rhomean)
            probes.append({'name':name,'Mb_Msun':gal['Mb_Msun'],'solution':sol})
        selected.append({'best_case':best,'nonlinear_galaxy_probes':probes})
    controls['worst_radial_matrix_residual']=worstmat
    summary={'cells':len(cases),'galaxies':len(gals),'cluster_passing_cells':sum(c['cluster_prescreen_pass'] for c in cases),
             'best_fractional_cluster_force_rms':min(c['common_fit']['fractional_force_rms'] for c in cases),
             'cells_passing_cluster_CMB_and_galaxy_lower_bound_only':sum(c['cluster_prescreen_pass'] and all(x['coldness_pass'] and x['background_fraction_pass'] for x in c['cmb_bracket']) and c['galaxy_lower_bound']['failures']['disc']==0 and c['galaxy_lower_bound']['failures']['halo300']==0 for c in cases),
             'scope':'no lower-bound galaxy pass is credited; no full Boltzmann or formation solution'}
    result={'controls':controls,'rho_mean_interval_kg_m3':rhobars,'summary':summary,'selected':selected,'cases':cases}
    (base.ROOT/output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'controls':controls,'summary':summary},indent=2))
    for sel in selected:
        b=sel['best_case']
        print(json.dumps({'best':{k:v for k,v in b.items() if k!='per_cluster_diagnostic_fits'},'nonlinear_probes':sel['nonlinear_galaxy_probes']},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    main(p.parse_args().output)

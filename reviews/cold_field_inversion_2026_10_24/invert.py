"""Spherical field inversions; distinguish literal khronon from extra source."""
import argparse, importlib.util, json, csv, os
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

PARENT=Path('reviews/matched_clumping_2026_10_24/compare.py')
spec=importlib.util.spec_from_file_location('matched',PARENT)
base=importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
G,MSUN,PC=base.G,base.MSUN,base.PC
MPC=1e6*PC
FOOTINGS={'canonical':9.3603e-11,'alternative':1.1312e-10}

def forward(gn,a0): return .5*(gn+np.sqrt(gn*gn+4*a0*gn))
def inverse(g,a0): return g*g/(a0+g)

def potential_function(r,g):
    """Phi(r[0])=0; integrate piecewise power-law g exactly."""
    power=np.diff(np.log(g))/np.diff(np.log(r))
    def integ(i,x):
        p=power[i]+1; z=x/r[i]
        return g[i]*r[i]*(np.log(z) if abs(p)<1e-10 else np.expm1(p*np.log(z))/p)
    totals=np.array([integ(i,r[i+1]) for i in range(len(power))]); prefix=np.r_[0,np.cumsum(totals)]
    def phi(x):
        i=min(max(int(np.searchsorted(r,x)-1),0),len(power)-1)
        return prefix[i]+integ(i,x)
    return phi

def analyze(rows,a0,mutate=False):
    radial=[]; shells=[]; dynamical=[]; systems=[]
    for name in sorted({r['name'] for r in rows}):
        rr=sorted([r for r in rows if r['name']==name],key=lambda r:r['radius_m'])
        r=np.array([x['radius_m'] for x in rr]); go=np.array([x['gobs'] for x in rr]); gb=np.array([x['gbar'] for x in rr]); mg=np.array([x['mgas'] for x in rr]); xr=np.array([x['xradius'] for x in rr])
        mc=(inverse(go,a0)-gb)*r*r/(G*MSUN)
        if mutate: mc*=2
        reconstructed=forward(gb+G*mc*MSUN/r**2,a0)
        assert np.allclose(reconstructed/go,1,rtol=1e-12,atol=0), f'source inversion failed: {name}'
        u=go-gb; m=u/a0
        xi=np.full(len(r),np.nan); valid=(m>=0)&(m<1); xi[valid]=a0*m[valid]/(1-m[valid]); psi=go-xi
        tau=u*r*r/(G*MSUN); law=forward(gb,a0)
        q=mc/mg
        for i in range(len(r)):
            radial.append(dict(name=name,xradius=float(xr[i]),r_m=float(r[i]),gbar=float(gb[i]),gobs=float(go[i]),g_law=float(law[i]),cold_aqual_msun=float(mc[i]),cold_aqual_over_gas=float(q[i]),tau_poisson_msun=float(tau[i]),hold_fraction=float(m[i]),hold_cap_failure=bool(m[i]>=1),xi_prime=float(xi[i]) if valid[i] else None,psi_prime=float(psi[i]) if valid[i] else None,outward_native_force=bool(valid[i] and psi[i]<0)))
        vol=4*np.pi/3*np.diff(r**3); rho=np.diff(mc)*MSUN/vol
        centers=np.sqrt(r[:-1]*r[1:]); phi=potential_function(r,go)
        phic=np.array([phi(x) for x in centers])
        phiavg=np.array([3*quad(lambda t:phi(r[i]+t*(r[i+1]-r[i]))*((r[i]+t*(r[i+1]-r[i]))/r[i+1])**2,0,1,epsabs=1e-3,epsrel=1e-10)[0]*(r[i+1]-r[i])*r[i+1]**2/(r[i+1]**3-r[i]**3) for i in range(len(r)-1)])
        for i in range(len(r)-1):
            shells.append(dict(name=name,inner_x=float(xr[i]),outer_x=float(xr[i+1]),shell_cold_msun=float(np.diff(mc)[i]),rho_kg_m3=float(rho[i]),phi_mean_m2_s2=float(phiavg[i])))
        sigma_values=[]; mu_values=[]
        for i in range(len(rho)-1):
            dphi=phiavg[i+1]-phiavg[i]; assert dphi>0
            mu2=-4*np.pi*G*(rho[i+1]-rho[i])/dphi
            mu= np.sqrt(mu2)*MPC if mu2>=0 else None
            sigma2=None; reason='nonpositive shell density'
            if rho[i]>0 and rho[i+1]>0:
                dlog=np.log(rho[i+1]/rho[i])
                if abs(dlog)>1e-14:
                    sigma2=-(phic[i+1]-phic[i])/dlog
                    reason='positive' if sigma2>0 else 'requires negative sigma squared'
                else: reason='constant density with nonzero gravity'
            sigma=np.sqrt(sigma2)/1000 if sigma2 is not None and sigma2>0 else None
            if sigma is not None: sigma_values.append(float(sigma))
            if mu is not None: mu_values.append(float(mu))
            dynamical.append(dict(name=name,shell_pair=i,inner_center_x=float(centers[i]/r[-1]),outer_center_x=float(centers[i+1]/r[-1]),sigma2_m2_s2=float(sigma2) if sigma2 is not None else None,sigma_iso_kms=float(sigma) if sigma is not None else None,sigma_status=reason,muK2_Mpc_minus2=float(mu2*MPC**2),muK_Mpc_minus1=float(mu) if mu is not None else None,muK_bound_pass=bool(mu2>=0 and mu2*MPC**2<.01)))
        systems.append(dict(name=name,cold_at_R500_msun=float(mc[-1]),Q_inner=float(q[0]),Q_outer=float(q[-1]),Q_slope=float(np.polyfit(np.log(r),np.log(q),1)[0]) if np.all(q>0) else None,cap_failures=int(np.sum(m>=1)),outward_valid=int(np.sum(valid&(psi<0))),negative_shells=int(np.sum(rho<0)),sigma_iso_range_kms=[min(sigma_values),max(sigma_values)] if sigma_values else None,muK_range_Mpc_minus1=[min(mu_values),max(mu_values)] if mu_values else None))
    summary=dict(systems=len(systems),radial_points=len(radial),positive_aqual_mass_points=sum(x['cold_aqual_msun']>0 for x in radial),native_cap_failures=sum(x['hold_cap_failure'] for x in radial),native_outward_valid=sum(x['outward_native_force'] for x in radial),negative_mass_shells=sum(x['shell_cold_msun']<0 for x in shells),shells=len(shells),muK_pairs=len(dynamical),muK_positive_pairs=sum(x['muK2_Mpc_minus2']>0 for x in dynamical),muK_bound_pass_pairs=sum(x['muK_bound_pass'] for x in dynamical),median_Q_inner=float(np.median([x['Q_inner'] for x in systems])),median_Q_outer=float(np.median([x['Q_outer'] for x in systems])),median_Mc_R500_msun=float(np.median([x['cold_at_R500_msun'] for x in systems])))
    return dict(summary=summary,systems=systems,radial=radial,shells=shells,dynamics=dynamical)

def checks():
    for a0 in FOOTINGS.values():
        for g in np.geomspace(1e-14,1e-8,30):
            assert np.isclose(forward(inverse(g,a0),a0)/g,1,rtol=1e-12)
            root=brentq(lambda z:z*z/(1+z)-inverse(g,a0)/a0,0,1e5,xtol=1e-14)
            assert np.isclose(root*a0/g,1,rtol=1e-8)
        gb=np.geomspace(1e-13,1e-9,20); g0=forward(gb,a0)
        assert np.allclose(inverse(g0,a0)/gb,1,rtol=1e-12)
        u=g0-gb
        assert np.allclose((a0*u/(a0-u))/g0,1,rtol=1e-11)
    r=np.array([1.,2.,4.]); phi=potential_function(r,3/r)
    assert np.isclose(phi(3),3*np.log(3))
    rho=7.; mass=4*np.pi/3*r**3*rho
    assert np.allclose(np.diff(mass)/(4*np.pi/3*np.diff(r**3)),rho)
    mu2=4.; kval=2.; phimean=np.array([1.,3.,6.]); offset=17.
    density=-mu2*(phimean+offset)/kval
    assert np.allclose(-kval*np.diff(density)/np.diff(phimean),mu2)
    # Native outward force occurs precisely above the static law, below the cap.
    a0=1.; gb=.05; go=forward(gb,a0)*1.2; u=go-gb
    assert 0<u<1 and go-a0*u/(a0-u)<0
    return ['AQUAL analytic forward/inverse grid','independent numerical root grid','zero added source galaxy limit','native equilibrium identity','power-law potential integral','uniform-density shell fixture','potential-zero cancellation fixture','native force sign fixture','actual source forward reconstruction']

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('--mutate',action='store_true'); args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    cc=checks(); result={'checks':cc,'footings':{}}
    variants=[('baseline',0,1),('HSE_bias_0.2',.2,1),('HSE_bias_0.3',.3,1),('stars_0.5',0,.5),('stars_2',0,2)]
    # Check loader identity against the committed previous empirical run.
    baseline=base.clusters()[0]
    with open('reviews/matched_clumping_2026_10_24/run/targets.csv') as f:
        old={(r['name'],float(r['xradius'])):r for r in csv.DictReader(f) if r['kind']=='cluster'}
    assert len(old)==len(baseline)==42
    for r in baseline:
        for key in ['gobs','gbar','mgas','radius_m']: assert np.isclose(r[key]/float(old[(r['name'],r['xradius'])][key]),1,rtol=1e-12)
    cc.append('42 input rows reproduce previous committed empirical run')
    for footing,a0 in FOOTINGS.items():
        result['footings'][footing]={}
        for label,bias,star in variants:
            result['footings'][footing][label]=analyze(base.clusters(bias,star)[0],a0,args.mutate)
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for table in ['radial','shells','dynamics']:
        rows=[]
        for footing,cells in result['footings'].items():
            for variant,cell in cells.items(): rows += [dict(footing=footing,variant=variant,**r) for r in cell[table]]
        base.write_csv(out/f'{table}.csv',rows)
    os.environ.setdefault('MPLCONFIGDIR','/tmp/matched_clumping_mpl')
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(1,2,figsize=(11,4.6),layout='constrained')
    cell=result['footings']['canonical']['baseline']
    for name in sorted({r['name'] for r in cell['radial']}):
        rr=[r for r in cell['radial'] if r['name']==name]
        axs[0].plot([r['xradius'] for r in rr],[r['cold_aqual_over_gas'] for r in rr],'.-',label=name)
        dd=[r for r in cell['dynamics'] if r['name']==name and r['muK_Mpc_minus1'] is not None]
        axs[1].plot([np.sqrt(r['inner_center_x']*r['outer_center_x']) for r in dd],[r['muK_Mpc_minus1'] for r in dd],'.-')
    axs[0].set(xlabel=r'$r/R_{500}$',ylabel=r'$M_c(<r)/M_{gas}(<r)$',title='Independent AQUAL source: inferred, not predicted')
    axs[0].legend(fontsize=7,ncol=2)
    axs[1].axhline(.1,color='black',ls='--',label='Inherited galaxy upper bound')
    axs[1].set(xlabel=r'Adjacent-shell scale / $R_{500}$',ylabel=r'Required $\mu_K$ [Mpc$^{-1}$]',yscale='log',title='Static mass term: potential zero cancels')
    axs[1].legend(fontsize=8)
    fig.suptitle('Canonical footing; published central profiles; no new fit',fontsize=11)
    fig.savefig(out/'inversion.png',dpi=180)
    print(json.dumps({f:{v:c['summary'] for v,c in cells.items()} for f,cells in result['footings'].items()},indent=2))

if __name__=='__main__': main()

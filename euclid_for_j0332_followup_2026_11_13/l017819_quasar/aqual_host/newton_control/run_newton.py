"""Fair light-centred Newtonian stars-only versus fixed-a0 AQUAL host control.

Same nonnegative source, SS6 operator, nuisance priors and fixed ln(lambda)=2.
No dark matter halo, cosmological model comparison or evidence calculation.
"""
import sys,json,time,argparse,os
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;BASE=P.parent
sys.path.insert(0,str(BASE))
import run_host as rh
from positive_profiles import PositiveState
import numpy as np
from scipy import optimize
from scipy.special import gammainc,gammaincinv
import matplotlib.pyplot as plt

def newton_field(light,m,nr=320,nt=64):
    return rh.al.make_field(10**m,np.exp(light[2])*rh.SCALE,np.exp(light[3]),light[4],
        a0=rh.A0,nr=nr,nt=nt,mu_one=True)

def snapshot(dest,name,ff,m,light):
    g=ff['grid'];np.savez_compressed(dest/(name+'.npz'),phi=ff['phi'],gr=ff['gr'],gt=ff['gt'],
        xf=g.xf,xc=g.xc,tf=g.tf,tc=g.tc,rf=g.rf,rc=g.rc,mu_one=True,logmass=m,light=light,
        zl=rh.ZL,zs=rh.ZS,a0=rh.A0)
    rh.save(dest/(name+'_config.json'),dict(**rh.field_metadata(ff),mu_one=True,
        law='Newtonian stars-only; a0 metadata is ignored by mu_one=True',logmass=m,light=light.tolist(),
        nr=g.nr,nt=g.nt,rmin_Re=1e-5,rmax_Re=500.,inclination=90.,zl=rh.ZL,zs=rh.ZS,
        kpc_per_arcsec=rh.SCALE,Dls_over_Ds=rh.BETA,mass_definition='infinite-total Sersic',
        potential_units='(km/s)^2, zero on outer sphere',gradient_units='(km/s)^2/kpc'))

def sphere_benchmark():
    light=np.array([0.,0.,0.,np.log(4.),1.,0.]);m=11.4;f=newton_field(light,m)
    theta=np.array([.2,.5,1.,2.,3.]);au,av=rh.al.projected_deflection(f,theta,np.zeros(5),zl=rh.ZL,zs=rh.ZS,nlos=256)
    projected_fraction=gammainc(8.,gammaincinv(8.,.5)*theta**.25)
    expected=4*rh.al.G*10**m*projected_fraction/(rh.al.C**2*theta*rh.SCALE)*rh.BETA*rh.al.ARCSEC
    relative=au/expected-1
    assert max(abs(relative))<.015 and max(abs(av))<1e-6
    return dict(theta=theta.tolist(),field_deflection=au.tolist(),analytic_projected_Sersic_deflection=expected.tolist(),
        relative_difference=relative.tolist(),minor_deflection=av.tolist(),field=rh.field_metadata(f))

def plot(obj,nr,aq,path):
    fig,axes=plt.subplots(2,3,figsize=(12,8));stretch=np.percentile(obj.data[obj.mask],99)/8
    for row,(label,r) in enumerate([('Newton stars-only',nr),('fixed-a0 AQUAL',aq)]):
        im=np.full(obj.data.shape,np.nan);im[obj.mask]=r['model']
        for j,(ax,img,title) in enumerate(zip(axes[row],[np.arcsinh(im/stretch),np.where(obj.mask,(obj.data-im)/obj.noise,np.nan),r['source']],
            [label+' model',label+' residual/RMS',label+' nonnegative source'])):
            ax.imshow(img,origin='lower',extent=[-5,5,-5,5] if j<2 else [-.63,.63,-.63,.63],
                cmap='RdBu_r' if j==1 else 'magma',vmin=-4 if j==1 else None,vmax=4 if j==1 else None)
            ax.set_title(title)
            if j<2:ax.set_xlim(-3.1,3.1);ax.set_ylim(-3.1,3.1)
            ax.set_xlabel('West (arcsec)' if j<2 else 'Source west relative to quasar (arcsec)');ax.set_ylabel('North (arcsec)')
    fig.suptitle('Same light-centred oblate density and physical source constraints; fixed ln(lambda)=2')
    fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(path,dpi=140);plt.close(fig)

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);start=time.time();results=[];benchmark=sphere_benchmark()
    rh.save(out/'spherical_benchmark.json',benchmark)
    for tag in ['run_04','run_03']:
        dest=out/tag;dest.mkdir();light,_=rh.light_for(tag);anchor_mass=11.4;field=newton_field(light,anchor_mass)
        amap=rh.project_map(field);anchor_fn=rh.mapped(light,amap)
        np.savez_compressed(dest/'anchor_map.npz',rad=rh.RAD,angle=rh.ANG,alpha=amap,logmass=anchor_mass,
            light=light,zl=rh.ZL,zs=rh.ZS,a0=rh.A0,mu_one=True)
        snapshot(dest,'anchor_field',field,anchor_mass,light)
        def pure(m):
            factor=10**(float(m)-anchor_mass)
            def fn(x,y):
                ax,ay=anchor_fn(x,y);return factor*ax,factor*ay
            return fn
        obj=rh.FieldAdapter(light,ns=21,step=.06,supersample=6);cache=[]
        def evaluate(m,arrays=False):
            got=[s for k,s in cache if k==float(m)]
            if got:st=got[0]
            else:
                st=PositiveState(obj,pure(m));cache.append((float(m),st))
                if len(cache)>8:cache.pop(0)
            return st.evaluate(2.,arrays)
        profile=[]
        def scan(grid):
            for mass in grid:
                if any(abs(x['logmass']-mass)<1e-8 for x in profile):continue
                r=evaluate(mass);profile.append(dict(logmass=float(mass),**r));rh.save(dest/'mass_profile.json',profile)
        initial=np.round(np.arange(11.1,11.70001,.01),8);scan(initial)
        coarse=min(profile,key=lambda r:r['penalized_MAP_objective']);expanded=coarse['logmass'] in (initial[0],initial[-1])
        if expanded:scan(np.round(np.arange(10.7,12.10001,.02),8))
        profile.sort(key=lambda r:r['logmass']);local=[i for i,r in enumerate(profile) if (i==0 or r['penalized_MAP_objective']<=profile[i-1]['penalized_MAP_objective']) and (i==len(profile)-1 or r['penalized_MAP_objective']<=profile[i+1]['penalized_MAP_objective'])]
        local=sorted(local,key=lambda i:profile[i]['penalized_MAP_objective'])[:3];opts=[]
        for i in local:
            lo=profile[max(i-1,0)]['logmass'];hi=profile[min(i+1,len(profile)-1)]['logmass']
            if lo==hi:continue
            o=optimize.minimize_scalar(lambda m:evaluate(m)['penalized_MAP_objective'],bounds=(lo,hi),method='bounded',options={'xatol':1e-5,'maxiter':40})
            opts.append(dict(logmass=float(o.x),objective=float(o.fun),success=bool(o.success),nfev=int(o.nfev),bounds=[lo,hi]))
        node=min(profile,key=lambda r:r['penalized_MAP_objective']);opts.append(dict(logmass=node['logmass'],objective=node['penalized_MAP_objective'],scope='exact finite-grid node'))
        best=min(opts,key=lambda r:r['objective']);m=best['logmass'];nr=evaluate(m,True)
        # Fresh exact-mass solve both retains the final field and checks the
        # linear Newtonian mass scaling instead of assuming array normalization.
        exact=newton_field(light,m);snapshot(dest,'best_field',exact,m,light)
        factor=10**(m-anchor_mass)
        scaling={key:float(np.linalg.norm(exact[key]-factor*field[key])/max(np.linalg.norm(exact[key]),1e-100)) for key in ['phi','gr','gt']}
        assert max(scaling.values())<1e-9
        exact_map=rh.project_map(exact);exact_fn=rh.mapped(light,exact_map)
        dr=PositiveState(obj,exact_fn).evaluate(2.)
        refined=newton_field(light,m,nr=448,nt=80);snapshot(dest,'best_field_refined',refined,m,light)
        rad=np.geomspace(.002,8.,192);ang=np.linspace(0,np.pi/2,97);highmap=rh.project_map(refined,rad,ang,nlos=256)
        high_fn=rh.mapped(light,highmap,rad,ang);hr=PositiveState(obj,high_fn).evaluate(2.)
        alt=rh.FieldAdapter(light,ns=21,step=.06,supersample=8);ar8=PositiveState(alt,pure(m)).evaluate(2.)
        # Reproduce the AQUAL case under exactly these constraints, rather than
        # contrast fields with the displaced SIE mass center or Gaussian source.
        ac=json.loads((BASE/'positive_01'/tag/'lnlambda_2/result.json').read_text())
        lib=np.load(BASE/'run_01'/tag/'library.npz')
        aq_fn=rh.mapped(light,lib['alpha'],lib['rad'],lib['angle'],lib['logmass'],ac['logmass_total'])
        aq=PositiveState(obj,aq_fn).evaluate(2.,True)
        assert abs(aq['chi2']-ac['aqual']['chi2'])<1e-6 and abs(aq['penalized_MAP_objective']-ac['aqual']['penalized_MAP_objective'])<1e-6
        probes=np.vstack([obj.A,obj.C,light[:2]+np.array([.4,.3]),light[:2]+np.array([-1.3,.7]),light[:2]+np.array([2.,-1.5])])
        co=np.cos(light[5]);si=np.sin(light[5]);d=probes-light[:2];u=co*d[:,0]+si*d[:,1];v=-si*d[:,0]+co*d[:,1]
        au,av=rh.al.projected_deflection(refined,u,v,zl=rh.ZL,zs=rh.ZS,nlos=512);direct=np.array([co*au-si*av,si*au+co*av])
        mapvalues=np.array(pure(m)(*probes.T));refvalues=np.array(high_fn(*probes.T))
        result=dict(fixture=tag,light=light.tolist(),mu_one=True,loglambda=2.,logmass_total=m,mass_msun=10**m,
            aqual_logmass_total=ac['logmass_total'],newton=rh.compact(nr),aqual=rh.compact(aq),
            delta_chi2_newton_minus_aqual=nr['chi2']-aq['chi2'],
            delta_penalized_MAP_newton_minus_aqual=nr['penalized_MAP_objective']-aq['penalized_MAP_objective'],
            optimizer_trials=opts,expanded_grid=expanded,mass_boundary=bool(min(m-profile[0]['logmass'],profile[-1]['logmass']-m)<.001),
            linear_scaling_relative_error=scaling,exact_mass_standard_grid=rh.compact(dr),refined_field_map=rh.compact(hr),ss8=rh.compact(ar8),
            exact_mass_delta_chi2=dr['chi2']-nr['chi2'],refined_delta_chi2=hr['chi2']-nr['chi2'],ss8_delta_chi2=ar8['chi2']-nr['chi2'],
            max_map_direct_probe_delta_arcsec=float(np.max(np.linalg.norm(mapvalues-direct,axis=0))),
            max_refined_map_direct_probe_delta_arcsec=float(np.max(np.linalg.norm(refvalues-direct,axis=0))),
            anchor_field=rh.field_metadata(field),best_field=rh.field_metadata(exact),refined_field=rh.field_metadata(refined))
        rh.save(dest/'result.json',result);np.savez_compressed(dest/'reconstruction.npz',source=nr['source'],model_valid=nr['model'],coefficient=nr['coef'],
            aqual_source=aq['source'],aqual_model_valid=aq['model'],mask=obj.mask,data=obj.data,noise=obj.noise)
        plot(obj,nr,aq,dest/'matched_positive_comparison.png');results.append(result)
        rh.save(out/'progress.json',dict(seconds=time.time()-start,fixtures=results))
        print(json.dumps(dict(fixture=tag,logmass=m,newton_chi2=nr['chi2'],aqual_chi2=aq['chi2'],gamma=nr['shear_magnitude'],seconds=time.time()-start)),flush=True)
    rh.save(out/'result.json',dict(assertion_tested='Light-centred Newtonian stars-only versus fixed-a0 AQUAL physical-source conditional MAP at commonlnlambda2, SS6 and identical fixed oblate light/mass shape.',
        seconds=time.time()-start,benchmark=benchmark,fixtures=results,
        non_claims=['No GR-plus-dark-matter or cosmological model comparison','No gravity exclusion or Bayes factor',
                    'Both retain foreground/source/noise residuals; fixed deblend profiles, edge-on q, constantM/L, zero convergence',
                    'Finite mass scan/local minimization; no globaloptimizer proof','No stellar-mass prior or full screened action test']))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)

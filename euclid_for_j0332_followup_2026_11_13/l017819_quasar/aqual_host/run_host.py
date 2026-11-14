"""Bounded conditional fixed-a0, edge-on oblate AQUAL host experiment.

Uses exact L017819 distance geometry, shared light/mass center, infinite-total
Sersic mass. Fixed SIE-deblend fixtures are sensitivity cases, not priors.
"""
import sys,os,json,time,argparse
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;T=P.parent;ROOT=T.parents[1]
os.environ.setdefault('MPLCONFIGDIR',str(P/'.mplcache'))
sys.path[:0]=[str(T/'host_control'),str(ROOT/'euclid_for_j0332_fit_2026_11_13')]
import numpy as np
from scipy import optimize,linalg
from scipy.interpolate import RegularGridInterpolator
from scipy.integrate import cumulative_trapezoid
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from arbitrary_field_adapter import FieldAdapter
from fit_host_v4 import Host
from lens_models import sie_deflection
import aqual_lensing as al

ZL=.32022095721117494;ZS=1.210;A0=9.3603e-11
MASS=np.round(np.arange(11.,11.80001,.04),8)
RAD=np.geomspace(.002,8.,128);ANG=np.linspace(0,np.pi/2,65)
SCALE,BETA=al.geometry(ZL,ZS)

def save(path,x):path.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def compact(r):return {k:v for k,v in r.items() if not isinstance(v,np.ndarray)}
def light_for(tag):
    d=json.loads((T/'host_control'/tag/'result.json').read_text())['chosen']
    old=json.loads((T/'light_01/result.json').read_text())['fits'][0]['parameters']
    return np.r_[old[:2],d['params'][:4]],d

def field_for(light,m,nr=320,nt=64,rmax=500.,qi=None):
    return al.make_field(10**m,np.exp(light[2])*SCALE,np.exp(light[3]),light[4] if qi is None else qi,
                         a0=A0,nr=nr,nt=nt,rmax_re=rmax)
def field_metadata(f):
    return {k:float(f[k]) for k in ['mass','re','n','qi','a0','residual','iterations','deposited_mass']}

def project_map(field,rad=RAD,angle=ANG,nlos=192):
    u=rad[:,None]*np.cos(angle);v=rad[:,None]*np.sin(angle)
    return np.array(al.projected_deflection(field,u,v,inclination=90.,zl=ZL,zs=ZS,nlos=nlos))

def mapped(light,maps,rad=RAD,angle=ANG,masses=None,mass=None):
    """Odd quadrants, rotation light major->sky, linear log-r and mass axes."""
    co=np.cos(light[5]);si=np.sin(light[5])
    grid=(np.log(rad),angle) if masses is None else (masses,np.log(rad),angle)
    interps=[RegularGridInterpolator(grid,maps[k] if masses is None else maps[:,k],bounds_error=True) for k in [0,1]]
    def fn(x,y):
        x,y=np.broadcast_arrays(x,y);dx=x-light[0];dy=y-light[1]
        u=co*dx+si*dy;v=-si*dx+co*dy;r=np.hypot(u,v)
        if np.max(r)>rad[-1]+1e-9:raise ValueError('map outer radius exceeded')
        lr=np.log(np.maximum(r,rad[0]));ang=np.arctan2(abs(v),abs(u))
        coords=np.column_stack([lr.ravel(),ang.ravel()])
        if masses is not None:coords=np.column_stack([np.full(r.size,mass),coords])
        au=interps[0](coords).reshape(r.shape)*np.sign(u)
        av=interps[1](coords).reshape(r.shape)*np.sign(v)
        # For the tiny unresolved inner map disk use odd radial continuation.
        inner=np.minimum(r/rad[0],1.)
        au*=inner;av*=inner
        return co*au-si*av,si*au+co*av
    return fn

def precision_profile(obj,fn,arrays=False):
    history=[]
    def fun(ll):
        r=obj.evaluate(fn,float(ll),return_arrays=False);history.append(dict(loglambda=float(ll),**compact(r)))
        return -r['score']
    opt=optimize.minimize_scalar(fun,bounds=(-2.,13.),method='bounded',options={'xatol':.01,'maxiter':28})
    r=obj.evaluate(fn,float(opt.x),return_arrays=arrays)
    return r,dict(success=bool(opt.success),message=str(opt.message),nfev=int(opt.nfev),loglambda=float(opt.x),history=history)

def positivity(obj,fn,ll,unconstrained):
    r=obj.evaluate(fn,ll,return_arrays=True);n=obj.ns**2
    D=np.column_stack([obj.B,r['lens'][obj.mask],obj.points[0,obj.mask],obj.points[1,obj.mask],np.ones(obj.mask.sum())])
    W=D/obj.noise[obj.mask,None];y=obj.data[obj.mask]/obj.noise[obj.mask]
    Q=linalg.block_diag(np.exp(ll)*obj.R,np.diag([1e-8,1e-8,1e-8,.01]));H=W.T@W+Q;b=W.T@y
    def fun(c):return .5*c@H@c-b@c,H@c-b
    c0=r['coef'].copy();c0[:n]=np.maximum(c0[:n],0.)
    z=optimize.minimize(fun,c0,jac=True,method='L-BFGS-B',bounds=[(0,None)]*n+[(None,None)]*4,
        options={'maxiter':1200,'maxls':35,'ftol':1e-12,'gtol':2e-6,'maxcor':30})
    c=z.x;grad=H@c-b;pg=grad.copy();pg[:n]=np.where(c[:n]<=1e-10,np.minimum(grad[:n],0),grad[:n])
    res=y-W@c
    return dict(scope='Fixed nonlinear model/precision nonnegative-source MAP; not truncated-Gaussian evidence.',
        success=bool(z.success),message=str(z.message),iterations=int(z.nit),projected_gradient_inf=float(max(abs(pg))),
        chi2=float(res@res),delta_chi2=float(res@res-unconstrained['chi2']),source_zero_fraction=float(np.mean(c[:n]<=1e-10)))

def figure(obj,aqual,sie,path):
    models=[]
    for r in [aqual,sie]:
        im=np.full(obj.data.shape,np.nan);im[obj.mask]=r['model'];models.append(im)
    fig,ax=plt.subplots(2,3,figsize=(12,8));stretch=np.percentile(obj.data[obj.mask],99)/8
    for j,(r,im,label) in enumerate(zip([aqual,sie],models,['AQUAL','matched SIE'])):
        for a,p,t in zip(ax[j],[np.arcsinh(im/stretch),np.where(obj.mask,(obj.data-im)/obj.noise,np.nan),r['source']],
                         [label+' total model',label+' residual/RMS',label+' Gaussian source']):
            a.imshow(p,origin='lower',cmap='RdBu_r' if 'residual' in t else 'magma',vmin=-4 if 'residual' in t else None,vmax=4 if 'residual' in t else None);a.set_title(t)
    fig.tight_layout();fig.savefig(path,dpi=140);plt.close(fig)

def spherical_benchmark(out):
    start=time.time();light=np.array([0.,0.,np.log(1.),np.log(4.),1.,0.]);mass=11.4
    f=field_for(light,mass,qi=1.)
    theta=np.array([.2,.5,1.,2.,3.])
    au,av=al.projected_deflection(f,theta,np.zeros(5),zl=ZL,zs=ZS,nlos=256)
    lr,ld=al.spherical_density_table(4.,nodes=512);r=np.exp(lr)
    mf=cumulative_trapezoid(4*np.pi*np.exp(ld)*r**3,lr,initial=0)
    z,w=np.polynomial.legendre.leggauss(512);t=(z+1)*np.pi/4;w*=np.pi/4
    radius=theta[:,None]*SCALE/np.cos(t)
    fraction=np.interp(np.log(radius/SCALE),lr,mf,right=1.)
    gn=al.G*10**mass*fraction/radius**2;a=al.fv.a0_kpc(A0)
    g=.5*(gn+np.sqrt(gn*gn+4*a*gn))
    reference=4*theta*SCALE/al.C**2*BETA*al.ARCSEC*np.sum(g/np.cos(t)*w,axis=-1)
    rel=au/reference-1
    result=dict(theta=theta.tolist(),field_alpha=au.tolist(),independent_spherical_alpha=reference.tolist(),relative_difference=rel.tolist(),
        minor_alpha=av.tolist(),exact_Abel_mass_integral=float(mf[-1]),field=field_metadata(f),seconds=time.time()-start)
    save(out/'spherical_benchmark.json',result)
    assert max(abs(rel))<.015 and max(abs(av))<1e-6
    return result

def main(out):
    out=Path(out);out.mkdir(exist_ok=True,parents=True);start=time.time();results=[]
    benchmark=spherical_benchmark(out)
    save(out/'progress.json',dict(stage='benchmark completed',seconds=time.time()-start,benchmark=benchmark))
    light0,chosen0=light_for('run_04')
    c=json.loads((T/'inputs/results/coolest.json').read_text())['lensing_entities'][0]['mass_model'][0]['parameters']
    cx=c['center_x']['point_estimate']['value'];cy=c['center_y']['point_estimate']['value']
    theta,q,pa=chosen0['params'][4:7]
    pure_sie=lambda x,y:sie_deflection(x,y,theta,q,pa,cx,cy,0.,0.)
    # Independent adapter benchmark against unchanged standard-SIE Host.
    original=Host();rp=original.run(np.array(chosen0['params']),True)
    adapted=FieldAdapter(light0);ra=adapted.evaluate(pure_sie,chosen0['params'][7],True)
    adaptercheck=dict(score_difference=ra['score']-rp['score'],max_model_difference=float(np.max(abs(ra['model']-rp['model']))))
    assert abs(adaptercheck['score_difference'])<1e-9 and adaptercheck['max_model_difference']<1e-10
    save(out/'adapter_benchmark.json',adaptercheck)
    for tag in ['run_04','run_03']:
        light,chosen=light_for(tag);dest=out/tag;dest.mkdir();obj=FieldAdapter(light)
        records=[];maps=[]
        for i,m in enumerate(MASS):
            t0=time.time();field=field_for(light,m);amap=project_map(field)
            maps.append(amap);rec=dict(logmass=float(m),seconds=time.time()-t0,**field_metadata(field));records.append(rec)
            # Durable partial library/progress if the bounded process is interrupted.
            np.savez_compressed(dest/'library.npz',logmass=MASS[:i+1],rad=RAD,angle=ANG,alpha=np.array(maps),light=light)
            save(dest/'fields.json',records)
            save(out/'progress.json',dict(stage='library',fixture=tag,finished_fields=i+1,total_fields=len(MASS),seconds=time.time()-start,last=rec))
            print(json.dumps(dict(stage='library',fixture=tag,logmass=float(m),seconds=rec['seconds'],total_seconds=time.time()-start)),flush=True)
        maps=np.array(maps)
        profile=[]
        for m in MASS:
            fn=mapped(light,maps,masses=MASS,mass=float(m));r,opt=precision_profile(obj,fn)
            profile.append(dict(logmass=float(m),loglambda=opt['loglambda'],precision_success=opt['success'],**compact(r)))
            save(dest/'mass_profile.json',profile)
        initial=max(profile,key=lambda x:x['score']);history=[]
        def objective(z):
            r=obj.evaluate(mapped(light,maps,masses=MASS,mass=float(z[0])),float(z[1]),False)
            history.append(dict(logmass=float(z[0]),loglambda=float(z[1]),score=r['score'],chi2=r['chi2']))
            return -r['score']
        opts=[]
        for z in [[initial['logmass'],initial['loglambda']],[initial['logmass']+.025,initial['loglambda']+.7]]:
            z=np.clip(z,[MASS[0],-2],[MASS[-1],13])
            o=optimize.minimize(objective,z,method='Powell',bounds=[(MASS[0],MASS[-1]),(-2,13)],options={'maxiter':12,'maxfev':220,'xtol':2e-4,'ftol':2e-7})
            opts.append(dict(parameters=o.x.tolist(),success=bool(o.success),message=str(o.message),nfev=int(o.nfev),score=float(-o.fun)))
        best=max(opts,key=lambda x:x['score']);m,ll=best['parameters'];fn=mapped(light,maps,masses=MASS,mass=m);r=obj.evaluate(fn,ll,True)
        sie,sopt=precision_profile(obj,pure_sie,True)
        # Exact-mass direct solve removes mass interpolation; repeated standard map
        # separates that effect from field/grid/LOS refinement.
        f=field_for(light,m);baseline=project_map(f);bfn=mapped(light,baseline)
        baseline_result=obj.evaluate(bfn,ll,False)
        refined=field_for(light,m,nr=448,nt=80);rrad=np.geomspace(.002,8.,192);rang=np.linspace(0,np.pi/2,97)
        for name,ff in [('best_field',f),('best_field_refined',refined)]:
            gg=ff['grid']
            np.savez_compressed(dest/(name+'.npz'),phi=ff['phi'],gr=ff['gr'],gt=ff['gt'],
                xf=gg.xf,xc=gg.xc,tf=gg.tf,tc=gg.tc,rf=gg.rf,rc=gg.rc,
                logmass=m,light=light,zl=ZL,zs=ZS,a0=A0)
        high=project_map(refined,rrad,rang,nlos=256);hfn=mapped(light,high,rrad,rang)
        high_result=obj.evaluate(hfn,ll,False)
        # Compare direct rays and maps at actual points plus fixed asymmetric probes.
        probes=np.vstack([obj.A,obj.C,light[:2]+np.array([.4,.3]),light[:2]+np.array([-1.3,.7]),light[:2]+np.array([2.,-1.5])])
        co=np.cos(light[5]);si=np.sin(light[5]);d=probes-light[:2];u=co*d[:,0]+si*d[:,1];v=-si*d[:,0]+co*d[:,1]
        # projected_deflection supports signed major/minor coordinates directly.
        du,dv=al.projected_deflection(refined,u,v,zl=ZL,zs=ZS,nlos=512)
        direct=np.array([co*du-si*dv,si*du+co*dv])
        low=np.array(fn(probes[:,0],probes[:,1]));hi=np.array(hfn(probes[:,0],probes[:,1]))
        numerical=dict(exact_mass_same_grid=compact(baseline_result),refined=compact(high_result),
            exact_field=field_metadata(f),refined_field=field_metadata(refined),probes_west_north=probes.tolist(),
            direct_refined_LOS512=direct.tolist(),library_probes=low.tolist(),refined_map_probes=hi.tolist(),
            max_library_direct_vector_delta_arcsec=float(np.max(np.linalg.norm(low-direct,axis=0))),
            max_refined_map_direct_vector_delta_arcsec=float(np.max(np.linalg.norm(hi-direct,axis=0))))
        # Fixed nonlinear best-mass source representation controls, not new optima.
        controls=[]
        for ns,h,ss in [(25,.06,2),(21,.045,2),(21,.06,3)]:
            alt=FieldAdapter(light,ns=ns,step=h,supersample=ss)
            cr,_=precision_profile(alt,fn)
            sr,_=precision_profile(alt,pure_sie)
            controls.append(dict(ns=ns,h=h,supersample=ss,aqual=compact(cr),sie=compact(sr),score_difference=cr['score']-sr['score']))
        pos=positivity(obj,fn,ll,r)
        result=dict(fixture=tag,light_parameters=light.tolist(),physical_light=chosen['physical_light'],best=compact(r),
            logmass_total=m,infinite_total_mass_msun=10**m,loglambda=ll,optimizer_starts=opts,mass_boundary=bool(m-MASS[0]<.005 or MASS[-1]-m<.005),
            matched_sie=compact(sie),matched_sie_precision_optimizer=sopt,
            score_difference=r['score']-sie['score'],chi2_difference=r['chi2']-sie['chi2'],
            numerical_checks=numerical,source_representation_controls=controls,positive_source_fixed_model=pos)
        np.savez_compressed(dest/'reconstruction.npz',source=r['source'],model_valid=r['model'],coefficient=r['coef'],
            sie_source=sie['source'],sie_model_valid=sie['model'],mask=obj.mask,data=obj.data,noise=obj.noise,lens=r['lens'])
        save(dest/'optimization_history.json',history);save(dest/'result.json',result);figure(obj,r,sie,dest/'comparison.png')
        results.append(result);save(out/'progress.json',dict(stage='fixture completed',fixture=tag,seconds=time.time()-start,results=results))
        print(json.dumps(dict(stage='fixture completed',fixture=tag,seconds=time.time()-start,logmass=m,score=r['score'],chi2=r['chi2'],shear=r['shear_magnitude'])),flush=True)
    result=dict(assertion_tested='Finite fixed-a0 isolated unscreened oblate AQUAL host image test under two fixed SIE-deblend light fixtures.',
        seconds=time.time()-start,a0_si=A0,zl=ZL,zs=ZS,kpc_per_arcsec=SCALE,Dls_over_Ds=BETA,mass_definition='infinite-total constant-M/L Sersic normalization; not aperture mass',
        source_operator=dict(n=21,h=.06,supersample=2),field_grid=dict(nr=320,nt=64,LOS=192,rmax_Re=500.,rmin_Re=1e-5),
        spherical_benchmark=benchmark,adapter_benchmark=adaptercheck,fixtures=results,
        non_claims=['No full screened action test','No independent stellar mass prior or measurement','No calibrated Bayes factor or p-value',
                    'Two point positions are fitted by unrestricted shear; host pixels supply additional conditional information',
                    'Fixed SIE-derived light profiles, constant M/L, edge-on inclination, zero convergence and diagonal image noise',
                    'Gaussian source may be negative; positivity check is fixed-model MAP only','Bounded local optimization, no global optimum proof'])
    save(out/'result.json',result);print(json.dumps(dict(stage='completed',seconds=result['seconds'])),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)

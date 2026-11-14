"""Same-field host operator quadrature and converged positive-source QP controls.

No additional AQUAL solve, SED prior or statistical evidence calibration.
"""
import sys,json,time,argparse
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
import run_host as rh
import numpy as np
from scipy import optimize,linalg

class FixedState:
    """Exact same Gaussian score, caching the fixed ray operator for lambda scans."""
    def __init__(self,obj,fn):
        r=obj.evaluate(fn,3.,True);self.template=r;self.n=obj.ns**2;self.ns=obj.ns
        self.D=np.column_stack([obj.B,r['lens'][obj.mask],obj.points[0,obj.mask],obj.points[1,obj.mask],np.ones(obj.mask.sum())])
        self.W=self.D/obj.noise[obj.mask,None];self.y=obj.data[obj.mask]/obj.noise[obj.mask]
        self.H0=self.W.T@self.W;self.b=self.W.T@self.y;self.R=obj.R;self.ldR=obj.logdetR
        self.nu=np.array([1e-8,1e-8,1e-8,.01])
        self.edges=np.pad(np.zeros((obj.ns-2,obj.ns-2),bool),1,constant_values=True)
        checked=self.evaluate(3.,True)
        assert abs(checked['score']-r['score'])<1e-7 and np.max(abs(checked['coef']-r['coef']))<1e-7
    def evaluate(self,ll,arrays=False):
        n=self.n;lam=np.exp(ll);H=self.H0.copy();H[:n,:n]+=lam*self.R
        H[n:,n:]+=np.diag(self.nu);cf=linalg.cho_factor(H,lower=True);c=linalg.cho_solve(cf,self.b)
        res=self.y-self.W@c;chi=float(res@res);pen=float(lam*c[:n]@self.R@c[:n]+np.sum(self.nu*c[n:]**2))
        ldH=2*np.log(np.diag(cf[0])).sum();ldQ=n*ll+self.ldR+np.log(self.nu).sum()
        score=float(-.5*(chi+pen+ldH-ldQ));r=rh.compact(self.template).copy();r['params']=list(r['params']);r['params'][7]=float(ll)
        source=c[:n].reshape(self.ns,self.ns)
        r.update(score=score,chi2=chi,prior_penalty=pen,linear_flux_lens_A_B_sky=c[-4:].tolist(),
            negative_source_fraction=float(np.mean(c[:n]<0)),source_edge_abs_fraction=float(abs(source[self.edges]).sum()/max(abs(source).sum(),1e-30)))
        if arrays:r.update(source=source,coef=c,model=self.D@c,lens=self.template['lens'])
        return r

def profile_state(state,arrays=False):
    opt=optimize.minimize_scalar(lambda ll:-state.evaluate(float(ll))['score'],bounds=(-2.,13.),method='bounded',options={'xatol':.01,'maxiter':28})
    return state.evaluate(float(opt.x),arrays),dict(loglambda=float(opt.x),success=bool(opt.success),nfev=int(opt.nfev))

def precision_profile(obj,fn,arrays=False):return profile_state(FixedState(obj,fn),arrays)

def positive_qp(obj,fn,ll):
    r=obj.evaluate(fn,ll,True);n=obj.ns**2
    D=np.column_stack([obj.B,r['lens'][obj.mask],obj.points[0,obj.mask],obj.points[1,obj.mask],np.ones(obj.mask.sum())])
    W=D/obj.noise[obj.mask,None];y=obj.data[obj.mask]/obj.noise[obj.mask]
    Q=linalg.block_diag(np.exp(ll)*obj.R,np.diag([1e-8,1e-8,1e-8,.01]));H=W.T@W+Q;b=W.T@y
    c_unc=linalg.cho_solve(linalg.cho_factor(H,lower=True),b)
    assert np.max(abs(c_unc-r['coef']))<1e-6
    # Analytically eliminate four unconstrained coefficients. Diagonally whiten
    # the SPD source Schur complement; Lawson-Hanson NNLS solves this QP exactly
    # up to measured float tolerances, unlike an unscaled ftol termination.
    B=H[:n,n:];C=H[n:,n:];Cf=linalg.cho_factor(C,lower=True)
    S=H[:n,:n]-B@linalg.cho_solve(Cf,B.T)
    a=b[:n]-B@linalg.cho_solve(Cf,b[n:]);scale=np.sqrt(np.diag(S))
    K=S/scale[:,None]/scale[None,:];rhs=a/scale
    L=linalg.cholesky(K,lower=True);target=linalg.solve_triangular(L,rhs,lower=True)
    z,_=optimize.nnls(L.T,target,maxiter=10000,atol=1e-9)
    s=z/scale;u=linalg.cho_solve(Cf,b[n:]-B.T@s);coef=np.r_[s,u]
    residual=y-W@coef;grad=H@coef-b;g=K@z-rhs
    pg=np.where(z<=1e-10,np.minimum(g,0),g)
    # Convex SPD QP: nonnegative feasibility plus zero projected gradient is KKT.
    kkt=float(np.max(abs(pg)));freegrad=float(np.max(abs(grad[n:])))
    assert np.min(s)>=0 and kkt<1e-6 and freegrad<1e-5
    result=dict(scope='Fixed nonlinear field and fixed Gaussian-best precision nonnegative-source MAP. No truncated-Gaussian evidence.',
        method='Analytic nuisance Schur complement, diagonal whitening, Cholesky least squares, Lawson-Hanson NNLS',
        chi2=float(residual@residual),unconstrained_chi2=r['chi2'],delta_chi2=float(residual@residual-r['chi2']),
        prior_penalty=float(coef@Q@coef),source_zero_fraction=float(np.mean(s<=1e-10)),
        projected_gradient_scaled_inf=kkt,nuisance_gradient_inf=freegrad,
        coefficient_complementarity_inf=float(np.max(abs(s*grad[:n]))),min_active_source_gradient=float(np.min(grad[:n][s<=1e-10])),
        nonlinear_loglambda=ll,linear_lens_quasar_A_B_sky=u.tolist())
    return result,coef,D@coef

def main(old,out):
    old=Path(old);out=Path(out);out.mkdir(parents=True,exist_ok=True);start=time.time();results=[]
    base=json.loads((old/'result.json').read_text());ref=base['fixtures'][0]
    _,chosen=rh.light_for('run_04');p=chosen['params'];theta,q,angle=p[4:7]
    cc=json.loads((rh.T/'inputs/results/coolest.json').read_text())['lensing_entities'][0]['mass_model'][0]['parameters']
    cx=cc['center_x']['point_estimate']['value'];cy=cc['center_y']['point_estimate']['value']
    pure_sie=lambda x,y:rh.sie_deflection(x,y,theta,q,angle,cx,cy,0.,0.)
    for initial in base['fixtures']:
        tag=initial['fixture'];dest=out/tag;dest.mkdir();f=np.load(old/tag/'library.npz')
        light=f['light'];maps=f['alpha'];masses=f['logmass'];rad=f['rad'];ang=f['angle']
        getfn=lambda mass:rh.mapped(light,maps,rad,ang,masses,float(mass))
        quadrature=[];m0=initial['logmass_total'];ll0=initial['loglambda']
        for ss in [1,2,3,4,6,8]:
            obj=rh.FieldAdapter(light,ns=21,step=.06,supersample=ss)
            fixed=obj.evaluate(getfn(m0),ll0,False)
            ar,_=precision_profile(obj,getfn(m0));sr,_=precision_profile(obj,pure_sie)
            quadrature.append(dict(supersample=ss,aqual_fixed_precision=rh.compact(fixed),aqual=rh.compact(ar),sie=rh.compact(sr)))
            rh.save(dest/'quadrature.json',quadrature)
        # Refit actual mass and precision with 6x6 pixel quadrature, not merely
        # reevaluate the low-quadrature optimum. Retain full coarse mass profile.
        obj=rh.FieldAdapter(light,ns=21,step=.06,supersample=6);profile=[]
        for mass in masses:
            ar,opt=precision_profile(obj,getfn(mass))
            profile.append(dict(logmass=float(mass),loglambda=opt['loglambda'],**rh.compact(ar)))
            rh.save(dest/'mass_profile_ss6.json',profile)
        seed=max(profile,key=lambda x:x['score']);history=[];cache=[]
        def fun(z):
            mass=float(z[0]);matched=[s for m,s in cache if m==mass]
            if matched:state=matched[0]
            else:
                state=FixedState(obj,getfn(mass));cache.append((mass,state))
                if len(cache)>2:cache.pop(0)
            r=state.evaluate(float(z[1]));history.append(dict(logmass=mass,loglambda=float(z[1]),score=r['score'],chi2=r['chi2']))
            return -r['score']
        optimizers=[]
        for seedmass in [seed['logmass'],m0]:
            o=optimize.minimize(fun,[seedmass,seed['loglambda']],method='Powell',bounds=[(masses[0],masses[-1]),(-2,13)],options={'maxiter':12,'maxfev':220,'xtol':1e-4,'ftol':1e-7})
            optimizers.append(dict(parameters=o.x.tolist(),score=float(-o.fun),success=bool(o.success),message=str(o.message),nfev=int(o.nfev)))
        best=max(optimizers,key=lambda x:x['score']);mass,ll=best['parameters'];fn=getfn(mass)
        ar=FixedState(obj,fn).evaluate(ll,True);sr,sopt=precision_profile(obj,pure_sie,True)
        positive_a,ca,ma=positive_qp(obj,fn,ll)
        positive_s,cs,ms=positive_qp(obj,pure_sie,sopt['loglambda'])
        refined=[]
        for ss in [8,12]:
            alt=rh.FieldAdapter(light,ns=21,step=.06,supersample=ss)
            aa,_=precision_profile(alt,fn);sss,_=precision_profile(alt,pure_sie)
            refined.append(dict(supersample=ss,aqual=rh.compact(aa),sie=rh.compact(sss)))
        result=dict(fixture=tag,light=light.tolist(),initial_ss2_mass=m0,initial_quadrature_sweep=quadrature,
            ss6_logmass_total=mass,ss6_mass_msun=10**mass,ss6_loglambda=ll,mass_boundary=bool(min(mass-masses[0],masses[-1]-mass)<.005),
            ss6_aqual=rh.compact(ar),ss6_sie=rh.compact(sr),score_difference=ar['score']-sr['score'],chi2_difference=ar['chi2']-sr['chi2'],
            optimizers=optimizers,high_quadrature_fixed_mass=refined,positive_aqual=positive_a,positive_sie=positive_s)
        rh.save(dest/'result.json',result);rh.save(dest/'optimization_history.json',history)
        np.savez_compressed(dest/'reconstruction.npz',source=ar['source'],model_valid=ar['model'],coefficient=ar['coef'],
            sie_source=sr['source'],sie_model_valid=sr['model'],mask=obj.mask,data=obj.data,noise=obj.noise,
            positive_aqual_source=ca[:441].reshape(21,21),positive_sie_source=cs[:441].reshape(21,21),
            positive_aqual_model_valid=ma,positive_sie_model_valid=ms)
        rh.figure(obj,ar,sr,dest/'comparison_ss6.png');results.append(result)
        rh.save(out/'progress.json',dict(seconds=time.time()-start,fixtures=results))
        print(json.dumps(dict(fixture=tag,seconds=time.time()-start,logmass=mass,chi2=ar['chi2'],score=ar['score'],shear=ar['shear_magnitude'])),flush=True)
    result=dict(assertion_tested='Fixed stored AQUAL libraries; pixel quadrature and positive-source quadratic-MAP sensitivity; conditional mass/precision refit at ss6.',
        seconds=time.time()-start,base_run=str(old),fixtures=results,
        non_claims=['No new field solver check','No empirical pass or calibrated model evidence','Fixed deblend fixtures and source grid; no independent mass prior',
                    'Positive MAP is fixed nonlinear mass/shear and precision, not a fully reoptimized nonnegative source model'])
    rh.save(out/'result.json',result)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args();main(a.input,a.output)

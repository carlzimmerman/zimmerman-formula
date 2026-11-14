"""Physical nonnegative-source conditional penalized-MAP mass profiles.

Fixed common log source precisions0/2/4 are sensitivity fixtures. No truncated
Gaussian marginal likelihood or ranking among precision fixtures is computed.
"""
import sys,json,time,argparse
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
import run_host as rh
import operator_controls as oc
from final_field_check import snapshot
import numpy as np
from scipy import optimize,linalg

class PositiveState:
    def __init__(self,obj,fn):
        self.s=oc.FixedState(obj,fn);self.obj=obj;n=self.s.n;H=self.s.H0;b=self.s.b
        self.B=H[:n,n:];C=H[n:,n:]+np.diag(self.s.nu);self.Cf=linalg.cho_factor(C,lower=True)
        self.S0=H[:n,:n]-self.B@linalg.cho_solve(self.Cf,self.B.T)
        self.a=b[:n]-self.B@linalg.cho_solve(self.Cf,b[n:])
    def evaluate(self,ll,arrays=False):
        st=self.s;n=st.n;lam=np.exp(ll);S=self.S0+lam*st.R;scale=np.sqrt(np.diag(S))
        K=S/scale[:,None]/scale[None,:];rhs=self.a/scale;L=linalg.cholesky(K,lower=True)
        target=linalg.solve_triangular(L,rhs,lower=True);z,_=optimize.nnls(L.T,target,maxiter=10000,atol=1e-9)
        source=z/scale;u=linalg.cho_solve(self.Cf,st.b[n:]-self.B.T@source);coef=np.r_[source,u]
        res=st.y-st.W@coef;chi=float(res@res);pen=float(lam*source@st.R@source+np.sum(st.nu*u*u))
        g=K@z-rhs;pg=np.where(z<=1e-10,np.minimum(g,0),g)
        grad=st.H0@coef-st.b;grad[:n]+=lam*st.R@source;grad[n:]+=st.nu*u
        kkt=float(max(abs(pg)));ng=float(max(abs(grad[n:])))
        assert min(source)>=0 and kkt<1e-6 and ng<1e-5
        r=rh.compact(st.template).copy();r.pop('score',None);r['params']=list(r['params']);r['params'][7]=float(ll)
        r.update(chi2=chi,prior_penalty=pen,penalized_MAP_objective=.5*(chi+pen),
            source_zero_fraction=float(np.mean(source<=1e-10)),negative_source_fraction=0.,
            source_edge_abs_fraction=float(source.reshape(st.ns,st.ns)[st.edges].sum()/max(source.sum(),1e-30)),
            projected_gradient_scaled_inf=kkt,nuisance_gradient_inf=ng,
            complementarity_inf=float(max(abs(source*grad[:n]))),linear_flux_lens_A_B_sky=u.tolist())
        if arrays:r.update(coef=coef,source=source.reshape(st.ns,st.ns),model=st.D@coef,lens=st.template['lens'])
        return r

def main(base,out):
    base=Path(base);out=Path(out);out.mkdir(parents=True,exist_ok=True);start=time.time();results=[]
    _,chosen=rh.light_for('run_04');theta,q,angle=chosen['params'][4:7]
    cp=json.loads((rh.T/'inputs/results/coolest.json').read_text())['lensing_entities'][0]['mass_model'][0]['parameters']
    cx=cp['center_x']['point_estimate']['value'];cy=cp['center_y']['point_estimate']['value']
    pure_sie=lambda x,y:rh.sie_deflection(x,y,theta,q,angle,cx,cy,0.,0.)
    for tag in ['run_04','run_03']:
        dest=out/tag;dest.mkdir();lib=np.load(base/tag/'library.npz');light=lib['light']
        maps=lib['alpha'];masses=lib['logmass'];rad=lib['rad'];ang=lib['angle']
        fn=lambda mass:rh.mapped(light,maps,rad,ang,masses,float(mass))
        obj=rh.FieldAdapter(light,ns=21,step=.06,supersample=6);cache=[]
        def state(m):
            m=float(m);got=[s for k,s in cache if k==m]
            if got:return got[0]
            st=PositiveState(obj,fn(m));cache.append((m,st))
            if len(cache)>8:cache.pop(0)
            return st
        grid=np.round(np.arange(11.2,11.50001,.01),8);profiles={str(ll):[] for ll in [0.,2.,4.]}
        def scan(points):
            for mass in points:
                st=state(mass)
                for ll in [0.,2.,4.]:
                    if any(abs(x['logmass']-mass)<1e-8 for x in profiles[str(ll)]):continue
                    r=st.evaluate(ll);profiles[str(ll)].append(dict(logmass=float(mass),**r))
                rh.save(dest/'mass_profiles.json',profiles)
        scan(grid)
        expanded=any(min(profiles[str(ll)],key=lambda r:r['penalized_MAP_objective'])['logmass'] in (grid[0],grid[-1]) for ll in [0.,2.,4.])
        if expanded:scan(np.round(np.arange(11.,11.80001,.02),8))
        sie_state=PositiveState(obj,pure_sie);cases=[]
        for ll in [0.,2.,4.]:
            profile=sorted(profiles[str(ll)],key=lambda r:r['logmass']);trials=[]
            # Optimize up to three separated minima of the actual finite scan.
            local=[i for i,r in enumerate(profile) if (i==0 or r['penalized_MAP_objective']<=profile[i-1]['penalized_MAP_objective']) and (i==len(profile)-1 or r['penalized_MAP_objective']<=profile[i+1]['penalized_MAP_objective'])]
            local=sorted(local,key=lambda i:profile[i]['penalized_MAP_objective'])[:3]
            for i in local:
                lo=profile[max(i-1,0)]['logmass'];hi=profile[min(i+1,len(profile)-1)]['logmass']
                if lo==hi:continue
                opt=optimize.minimize_scalar(lambda m:state(m).evaluate(ll)['penalized_MAP_objective'],bounds=(lo,hi),method='bounded',options={'xatol':1e-5,'maxiter':40})
                trials.append(dict(logmass=float(opt.x),objective=float(opt.fun),success=bool(opt.success),nfev=int(opt.nfev),bounds=[lo,hi]))
            finite=min(profile,key=lambda r:r['penalized_MAP_objective']);trials.append(dict(logmass=finite['logmass'],objective=finite['penalized_MAP_objective'],success=False,scope='best exact grid node'))
            best=min(trials,key=lambda r:r['objective']);mass=best['logmass'];r=state(mass).evaluate(ll,True);sr=sie_state.evaluate(ll,True)
            alt=rh.FieldAdapter(light,ns=21,step=.06,supersample=8)
            ar8=PositiveState(alt,fn(mass)).evaluate(ll);sr8=PositiveState(alt,pure_sie).evaluate(ll)
            label='lnlambda_'+str(int(ll));case_dir=dest/label;case_dir.mkdir()
            ff=rh.field_for(light,mass);snapshot(case_dir,'best_field',ff,mass,light)
            # Direct exact-mass field projection validation for central precision.
            direct=None
            if ll==2.:
                dm=rh.project_map(ff);dr=PositiveState(obj,rh.mapped(light,dm)).evaluate(ll)
                direct=dict(result=dr,delta_chi2=dr['chi2']-r['chi2'],delta_penalized_MAP_objective=dr['penalized_MAP_objective']-r['penalized_MAP_objective'])
            case=dict(loglambda=ll,logmass_total=mass,mass_msun=10**mass,aqual=rh.compact(r),sie=rh.compact(sr),
                delta_chi2=r['chi2']-sr['chi2'],delta_penalized_MAP_objective=r['penalized_MAP_objective']-sr['penalized_MAP_objective'],
                optimizer_trials=trials,mass_boundary=bool(min(mass-masses[0],masses[-1]-mass)<.005),
                scan_edge=bool(min(mass-profile[0]['logmass'],profile[-1]['logmass']-mass)<.001),
                ss8_aqual=rh.compact(ar8),ss8_sie=rh.compact(sr8),direct_exact_mass_check=direct)
            rh.save(case_dir/'result.json',case)
            np.savez_compressed(case_dir/'reconstruction.npz',source=r['source'],model_valid=r['model'],coefficient=r['coef'],
                sie_source=sr['source'],sie_model_valid=sr['model'],mask=obj.mask,data=obj.data,noise=obj.noise)
            rh.figure(obj,r,sr,case_dir/'positive_comparison.png');cases.append(case)
            print(json.dumps(dict(fixture=tag,loglambda=ll,logmass=mass,chi2=r['chi2'],sie_chi2=sr['chi2'],gamma=r['shear_magnitude'],seconds=time.time()-start)),flush=True)
        result=dict(fixture=tag,light=light.tolist(),source_operator=dict(ns=21,h=.06,supersample=6),expanded_scan=expanded,cases=cases)
        rh.save(dest/'result.json',result);results.append(result);rh.save(out/'progress.json',dict(seconds=time.time()-start,fixtures=results))
    rh.save(out/'result.json',dict(assertion_tested='Nonnegative-source conditional penalized-MAP mass profiles at fixed common ln(lambda)0/2/4 through matched SS6 operators, source/nuisance priors and independent-PSF treatment.',
        seconds=time.time()-start,fixtures=results,non_claims=['No comparison among different regularization fixtures by their MAP values',
            'Not truncated-Gaussian evidence, Bayes factor, p-value or posterior','No independent SED prior, physical environment, full screened action or empirical theory pass',
            'Fixed deblend profiles, source grid, edge-on inclination, zero convergence and diagonal RMS',
            'Finite scan/local minimization not a universal global optimizer certificate']))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--output',required=True);a=p.parse_args();main(a.base,a.output)

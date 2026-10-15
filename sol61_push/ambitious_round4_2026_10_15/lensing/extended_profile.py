import argparse,json,time
from model import *
from scipy.optimize import brentq

def mbfun(x,u):
    x=np.asarray(x);return x**3/(x*x+u*u)**1.5

def mexfun(x,u):
    m=mbfun(x,u);return .5*(np.sqrt(m*m+4*x*x*m)-m)

def dmex(x,u):
    x=np.asarray(x);m=mbfun(x,u);mp=3*x*x*u*u/(x*x+u*u)**2.5
    return .5*((2*m*mp+8*x*m+4*x*x*mp)/(2*np.sqrt(m*m+4*x*x*m))-mp)

def extended(lm,rb,r,order=64):
    old,n,mt,e0,rm=edge(lm);u=rb*1e6/rm
    e=e0 if u==0 else brentq(lambda xx:float(mexfun(xx,u))-SUP*n,e0,e0+10*u+1,xtol=1e-11)
    x=np.asarray(r)*1e6/rm
    cold=SUP*n/(np.pi*x*x);inside=x<e
    if np.any(inside):
        xx=x[inside];umax=np.arccosh(e/xx);nodes,w=GL(order)
        tt=(nodes[None,:]+1)*umax[:,None]/2;radius=xx[:,None]*np.cosh(tt);deriv=dmex(radius,u)
        sig=np.sum(w*deriv/radius,axis=1)*umax/(4*np.pi)
        caps=np.sum(w*deriv*xx[:,None]*np.sinh(tt)**2/np.cosh(tt),axis=1)*umax/2
        cold[inside]=(SUP*n-caps)/(np.pi*xx**2)-sig
    bary=x*x/(np.pi*(x*x+u*u)**2)
    return (cold+bary)*10**lm/rm**2,e*rm/1e6

class ExtFitter(Fitter):
    def predict(self,pars):
        ones=[];twos=[];edges=[]
        for b,lm in enumerate(pars[:4]):
            rb=pars[4+b];one,ex=extended(lm,rb,self.r[b]);ones.append(one)
            twos.append(np.array([v(ex) for v in self.interp]));edges.append(ex)
        ov=np.array(ones).ravel();tv=np.zeros((60,4))
        for b,t in enumerate(twos):tv[b*15:(b+1)*15,b]=t
        wo=solve_triangular(self.chol,ov,lower=True);wt=solve_triangular(self.chol,tv,lower=True)
        bias=nnls(wt,self.wy-wo)[0];res=self.wy-wo-wt@bias
        return res,ov,tv,bias,edges

p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--cache',required=True);a=p.parse_args();t=time.monotonic()
cache=np.load(a.cache);r,y,c=data();controls=[];positive=[];boundary=[]
for lm in (10.,10.8,11.5):
    for rb in (0.,.03,.1,.3):
        v,e=extended(lm,rb,r[0]);vr,_=extended(lm,rb,r[0],order=128);controls.append(floor_relative(v,vr))
        if rb==0:controls.append(floor_relative(v,onehalo(lm,r[0],True)))
        old,n,mt,ed,rm=edge(lm);u=rb*1e6/rm;positive.append(float(dmex(np.geomspace(1e-5,1e3,1000),u).min()));boundary.append(abs(float(mexfun(e*1e6/rm,u))/(SUP*n)-1))
gate=max(controls)<.001 and min(positive)>=0 and max(boundary)<1e-9
if not gate:
    Path(a.output).write_text(json.dumps(dict(status='CONTROL FAILED',max_projection_discrepancy=max(controls),min_density_derivative=min(positive),max_mass_boundary_relative=max(boundary)),indent=2)+'\n');raise SystemExit(1)
f=ExtFitter(cache['edge_grid'],cache['table'],True);starts=[[10.38,10.87,11.,11.18,0.,.03,.06,.1],[10.4,10.9,11.1,11.3,.05,.1,.1,.1],[10.2,10.7,11.,11.2,.01,.01,.03,.05],[10.7,11.,11.2,11.5,.1,.2,.2,.3]];bounds=[(9.5,12)]*4+[(0,.3)]*4;runs=[];best=None
for st in starts:
    opt=minimize(f.objective,st,method='L-BFGS-B',bounds=bounds,options=dict(maxiter=250,ftol=1e-11,gtol=1e-6,maxls=40))
    runs.append(dict(start=st,chi2=float(opt.fun),parameters=opt.x.tolist(),success=bool(opt.success),message=str(opt.message),nfev=int(opt.nfev)))
    if best is None or opt.fun<best.fun:best=opt
alt=least_squares(lambda pp:f.predict(pp)[0],best.x,bounds=([9.5]*4+[0]*4,[12]*4+[.3]*4),max_nfev=300,ftol=1e-11,xtol=1e-11,gtol=1e-8)
altchi=float(alt.fun@alt.fun)
if altchi<best.fun:best.x=alt.x;best.fun=altchi
res,ov,tv,bb,edges=f.predict(best.x);pred=ov+tv@bb;raw=y.ravel()-pred;pr=np.linalg.solve(c,raw)
env=Environment(power_points=131072,padding=64);dtv=np.zeros_like(tv)
for b,e in enumerate(edges):dtv[15*b:15*(b+1),b]=env.los(r[b],e,order=1536,rmax=480.)
direct_raw=y.ravel()-ov-dtv@bb;direct_chi=float(direct_raw@np.linalg.solve(c,direct_raw))
ss=sorted(v['chi2'] for v in runs if v['success']);agreement=len(ss)>1 and ss[1]-ss[0]<.05 and abs(altchi-best.fun)<.5
result=dict(status='COMPUTED',post_data=True,controls=dict(max_projection_discrepancy=max(controls),min_density_derivative=min(positive),max_mass_boundary_relative=max(boundary)),chi2=float(best.fun),nominal_dof=48,nominal_p=float(chi2.sf(best.fun,48)),logMb=best.x[:4].tolist(),Plummer_radii_Mpc=best.x[4:].tolist(),biases=bb.tolist(),edges_physical_Mpc=edges,starts=runs,independent_least_squares=dict(chi2=altchi,success=bool(alt.success),nfev=int(alt.nfev)),optimizer_agreement=agreement,direct_environment_chi2=direct_chi,direct_environment_chi2_difference=direct_chi-best.fun,predictions=pred.reshape(4,15).tolist(),onehalo=ov.reshape(4,15).tolist(),residuals=raw.reshape(4,15).tolist(),conditional_pulls=(pr/np.sqrt(np.diag(np.linalg.inv(c)))).reshape(4,15).tolist(),signed_additive_bin_chi2=[float(raw[15*b:15*(b+1)]@pr[15*b:15*(b+1)]) for b in range(4)],elapsed_seconds=time.monotonic()-t,interpretation='Additional 12-nuisance Plummer/exact-law finite-excess profile diagnostic; no physical production, isolation selection, external baryon-radius validation or theory-closure claim.')
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('starts','predictions','onehalo','residuals','conditional_pulls')}))

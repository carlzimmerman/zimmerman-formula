#!/usr/bin/env python3
"""Known answers and cross-resolution forward models before grid execution."""
import math,time,resource,platform
import engine as E
import numpy as np
import scipy
from scipy.optimize import minimize_scalar
from scipy.special import ndtr
checks=[];start=time.time()
def check(name,passed,value):checks.append(dict(name=name,passed=bool(passed),value=value))
edges=np.linspace(-12,12,301)
a=np.diff(ndtr(edges));b=np.diff(np.array([.5*(1+math.erf(x/math.sqrt(2))) for x in edges]))
err=float(np.max(abs(a-b)));check('Gaussian_channel_integral',err<=1e-12,err)
forward=[]
for tid in range(12):
    for foot in E.FOOTS:
        models=[]
        for rung in [1,2]:
            t,cm,g,mh2,d,gas,noise,m=E.truth(tid,rung,foot,0,'flat',True);models.append(m)
            normerr=abs(float(cm.psf_ft[0,0].real)-1.)
            check(f'PSF_DC_{tid}_{foot}_{rung}',normerr<=1e-12,normerr)
            if tid==0:
                fit=E.F.Fitter(cm,None,np.ones(m.shape),E.F.LawMass(mh2,E.FOOTS[foot]),'law',sighi_fixed=6.)
                theta=np.array([g[k] for k in E.F.GEO]+[g['sig0'],t['logM']])
                def fun(lm):
                    theta[10]=lm
                    return float(np.sum((fit.model(theta)-m)**2))
                sol=minimize_scalar(fun,bounds=(t['logM']-1,t['logM']+1),method='bounded',options={'xatol':1e-8})
                diff=abs(float(sol.x)-t['logM']);check(f'one_parameter_mass_{foot}_{rung}',sol.success and diff<=.001,diff)
        diff=float(np.linalg.norm(models[0]-models[1])/np.linalg.norm(models[1]))
        forward.append(dict(template=tid,footing=foot,relative=diff,passed=diff<=.005))
x=np.tile([-.4,0,.4],12);sigma=.2;S=float(x@x);variance=sigma*sigma/S
X=np.column_stack([np.ones(len(x)),x]);inv=np.linalg.inv(X.T@X)
check('linear_slope_variance',abs(variance-sigma*sigma*inv[1,1])<=1e-14,variance)
truth=.6;y=.3+truth*x;coef=np.linalg.lstsq(X,y,rcond=None)[0]
check('linear_exact_slope',abs(coef[1]-truth)<=1e-12,float(coef[1]))
rng=np.random.default_rng(2026110545);draws=y+rng.normal(0,sigma,(20000,len(x)))
slopes=draws@x/S;coverage=float(np.mean(abs(slopes-truth)<=1.959963984540054*math.sqrt(variance)))
tol=3*math.sqrt(.95*.05/len(slopes));check('linear_95percent_coverage',abs(coverage-.95)<=tol,dict(coverage=coverage,tolerance=tol))
out=dict(status='known answers plus forward-resolution audit; no nonlinear population verdict',checks=checks,
         passed=sum(c['passed'] for c in checks),total=len(checks),forward_pairs=forward,
         source_hashes=E.hashes(),versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
         scope='kappa = 1/2 FITTED; not theory closed')
E.atomic(E.HERE/'controls.json',out)
E.atomic(E.HERE/'controls_runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print('known answers',out['passed'],'/',out['total'],'forward passed',sum(x['passed'] for x in forward),'/',len(forward),flush=True)
raise SystemExit(int(not all(c['passed'] for c in checks) or not all(c['passed'] for c in forward)))

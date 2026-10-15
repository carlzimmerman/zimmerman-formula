import argparse,json,time
from extended_model import *
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--cache',required=True);a=p.parse_args();t=time.monotonic()
class Common(ExtFitter):
    def predict(self,pars):return super().predict(np.r_[pars[:4],np.repeat(pars[4],4)])
cache=np.load(a.cache);f=Common(cache['edge_grid'],cache['table'],True);starts=[[10.38,10.87,11.,11.18,.0],[10.4,11.,11.2,11.4,.02],[10.2,10.7,11.,11.2,.05],[10.7,11.,11.2,11.5,.1]];runs=[];best=None
for st in starts:
    opt=minimize(f.objective,st,method='L-BFGS-B',bounds=[(9.5,12)]*4+[(0,.3)],options=dict(maxiter=250,ftol=1e-11,gtol=1e-6,maxls=40))
    runs.append(dict(start=st,chi2=float(opt.fun),parameters=opt.x.tolist(),success=bool(opt.success),message=str(opt.message),nfev=int(opt.nfev)))
    if best is None or opt.fun<best.fun:best=opt
alt=least_squares(lambda pp:f.predict(pp)[0],best.x,bounds=([9.5]*4+[0],[12]*4+[.3]),max_nfev=200,ftol=1e-11,xtol=1e-11,gtol=1e-8);altchi=float(alt.fun@alt.fun)
if altchi<best.fun:best.x=alt.x;best.fun=altchi
res,ov,tv,bb,edges=f.predict(best.x);pred=ov+tv@bb;raw=f.y.ravel()-pred;pr=np.linalg.solve(f.c,raw);env=Environment(power_points=131072,padding=64);direct=np.zeros_like(tv)
for b,e in enumerate(edges):direct[15*b:15*(b+1),b]=env.los(f.r[b],e,order=1536,rmax=480.)
dr=f.y.ravel()-ov-direct@bb;dc=float(dr@np.linalg.solve(f.c,dr));ss=sorted(v['chi2'] for v in runs if v['success'])
result=dict(chi2=float(best.fun),nominal_dof=51,nominal_p=float(chi2.sf(best.fun,51)),logMb=best.x[:4].tolist(),common_Plummer_radius_Mpc=float(best.x[4]),biases=bb.tolist(),edges_physical_Mpc=edges,starts=runs,independent_least_squares=dict(chi2=altchi,success=bool(alt.success)),optimizer_agreement=(len(ss)>1 and ss[1]-ss[0]<.05 and abs(altchi-best.fun)<.5),direct_environment_chi2_difference=dc-best.fun,predictions=pred.reshape(4,15).tolist(),residuals=raw.reshape(4,15).tolist(),conditional_pulls=(pr/np.sqrt(np.diag(np.linalg.inv(f.c)))).reshape(4,15).tolist(),post_data=True,elapsed_seconds=time.monotonic()-t)
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('starts','predictions','residuals','conditional_pulls')}))

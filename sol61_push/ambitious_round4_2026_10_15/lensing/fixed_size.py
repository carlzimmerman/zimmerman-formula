import argparse,json,time
from extended_model import *
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--cache',required=True);p.add_argument('--radius-kpc',type=float,required=True);a=p.parse_args();t=time.monotonic()
class Fixed(ExtFitter):
    def predict(self,pars):return super().predict(np.r_[pars,np.repeat(a.radius_kpc/1000,4)])
cache=np.load(a.cache);f=Fixed(cache['edge_grid'],cache['table'],True);fit=f.fit();fit.update(fixed_Plummer_radius_kpc=a.radius_kpc,post_data=True,elapsed_seconds=time.monotonic()-t)
env=Environment(power_points=131072,padding=64);_,ov,tv,bb,edges=f.predict(fit['logMb']);direct=np.zeros_like(tv)
for b,e in enumerate(edges):direct[15*b:15*(b+1),b]=env.los(f.r[b],e,order=1536,rmax=480.)
raw=f.y.ravel()-ov-direct@bb;dchi=float(raw@np.linalg.solve(f.c,raw));fit.update(direct_environment_chi2=dchi,direct_environment_chi2_difference=dchi-fit['chi2'])
Path(a.output).write_text(json.dumps(fit,indent=2)+'\n');print(json.dumps({k:fit[k] for k in ('fixed_Plummer_radius_kpc','chi2','nominal_p','logMb','biases','optimizer_agreement','direct_environment_chi2_difference','elapsed_seconds')}))

import argparse,json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from photons import Radiation,escape,environment,PROFILES,PREV
from fast import FastChemistry
from kinetics_v3 import Rates
BASE=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
 base=json.loads((BASE/'run_photons/results.json').read_text())
 chosen=next(r for r in base['rows'] if r['alpha']==.2 and r['mass']==1e7)
 rad=Radiation(6);refined=[]
 for Mb,b in PROFILES:
  s=rad.run(.2,1e7,Mb,b,rtol=2e-9);refined.append(s);print('refine',Mb,s['molecular_mass_fraction'],flush=True)
 rad9=Radiation(9);finest=[rad9.run(.2,1e7,Mb,b,rtol=2e-9) for Mb,b in PROFILES[2:]]
 refinement=dict(order6=refined,order9_disk_cluster=finest,relative_change_3_to_6=[s['molecular_mass_fraction']/o['molecular_mass_fraction']-1 for s,o in zip(refined,chosen['states'])],relative_change_6_to_9=[s['molecular_mass_fraction']/o['molecular_mass_fraction']-1 for s,o in zip(finest,refined[2:])])
 # Direct independent quadrature for the escape geometry.
 zz,ww=leggauss(100);u=zz+1;w=ww
 geom=[]
 for tau in [.0001,.01,.1,1,10,100]:
  beta=float(np.dot(w,.75*(1-u*u/4)*np.exp(-tau*u)))
  ff,df=escape(np.array([tau]));expected=tau*beta/(1-beta)
  h=1e-5*tau;fd=(escape(np.array([tau+h]))[0][0]-escape(np.array([tau-h]))[0][0])/(2*h)
  geom.append(dict(tau=tau,relative_value_error=float(ff[0]/expected-1),derivative_error=float(abs(fd-df[0]))))
 assert max(abs(x['relative_value_error']) for x in geom)<1e-8
 # Analytic Jacobian against a deterministic directional derivative.
 fun,(n,Ti,L,age)=rad.system(.2,1e7,6e10,3,closed=True)
 y=np.zeros(rad.nm+rad.nq+1);y[0]=.1;y[1:rad.nb+1]=1e-4;y[rad.nm-1]=.01;y[rad.nm:-1]=1e-8
 v=np.sin(np.arange(len(y))+1.);v[rad.nm:-1]*=1e-7;v[rad.nm-1]*=.001
 h=1e-7;fd=(fun(y+h*v)-fun(y-h*v))/(2*h);jv=fun(y,True)@v
 jacerr=float(np.linalg.norm(fd-jv)/np.linalg.norm(jv));assert jacerr<1e-7
 ledger=np.r_[-.5,-(.5+rad.D),1,rad.omega,1]
 f=fun(y);ledgererr=float(abs(ledger@f)/max(np.linalg.norm(f),1e-100));assert ledgererr<1e-12
 # Exact thermal stationarity of individual discrete forward/reverse channels.
 thermal=[];ch=FastChemistry(rad,n)
 for T in [.006,.008,.02]:
  s=ch.state(T);occ=1/np.expm1(np.minimum(rad.omega/T,700));phot=.2**3*rad.G/n*occ
  prod=np.r_[s['x']*s['c'],np.full(rad.nb,s['a']*s['x'])]
  forward=.2**3*prod[:,None]*rad.coefficients(T)*(1+occ)
  reverse=s['targets'][:,None]*rad.sig*phot
  err=float(np.sum(abs(forward-reverse))/max(np.sum(abs(forward)+abs(reverse)),1e-300))
  eps=1e-5;fd=(ch.state(T*np.exp(eps))['U']-ch.state(T*np.exp(-eps))['U'])/(2*eps)
  thermal.append(dict(T=T,relative_stationarity_error=err,heat_capacity_relative_error=float(fd/s['capacity']-1)))
 assert max(x['relative_stationarity_error'] for x in thermal)<1e-10
 # Closed-box photon-count/chemical invariant in addition to energy.
 closed=rad.run(.2,1e7,6e10,3,closed=True,end=1e-4)
 t=closed['molecular_mass_fraction']*101/201
 closed['photon_chemical_count_error']=closed['photon_number']-closed['atomic_fraction']-2*t
 assert abs(closed['photon_chemical_count_error'])<1e-8
 # Direct spectral integral versus group quadrature: genuine frequency-resolution diagnostic.
 prior=Rates(PREV/'run_refine/results.json');coverage=[]
 for T in [6.4e-8,1e-6,.001,.03,.05]:
  k,_=prior.at(T);group=rad.coefficients(T).sum(axis=1)
  coverage.append(dict(T=T,atomic_relative_error=float(group[0]/k[0]-1),molecular_relative_error=float(sum(group[1:])/sum(k[1:])-1)))
 W=float(sum(rad.deg[1:]));ratio=(100*101/201)**1.5/W
 equilibrium_cap=201/101/(2+np.sqrt(ratio))
 out=dict(refinement=refinement,geometry=geom,jacobian_relative_error=jacerr,instantaneous_ledger_relative_error=ledgererr,thermal=thermal,closed=closed,rate_quadrature=coverage,equilibrium_rotational_weight=W,equilibrium_uniform_mass_cap=equilibrium_cap)
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print('refinement',refinement['relative_change_3_to_6'],refinement['relative_change_6_to_9']);print('cap',equilibrium_cap)
if __name__=='__main__':main()

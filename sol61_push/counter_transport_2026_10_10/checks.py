"""Finite-width, positive-density counter-transport: energy and Fourier gate.
An isolated one-component NFW toy, not the framework's fitted halo population.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad

p=argparse.ArgumentParser()
p.add_argument('--output',required=True)
p.add_argument('--mutate',action='store_true')
args=p.parse_args()
bands=[(.05,.15),(.25,.35),(.7,.9)]
cuts=sorted(set([0.,1.]+[v for band in bands for v in band]))
checks=[]
def ck(name, passed): checks.append({'name':name,'pass':bool(passed)})
def integrate(fn): return sum(quad(fn,lo,hi,epsabs=2e-11,epsrel=2e-10,limit=150)[0] for lo,hi in zip(cuts[:-1],cuts[1:]))
results=[]
for c in [5.,15.,40.]:
 norm=math.log1p(c)-c/(1+c)
 def M(r): return (math.log1p(c*r)-c*r/(1+c*r))/norm
 def dm(r): return c*c*r/((1+c*r)**2*norm)
 masses=[M(hi)-M(lo) for lo,hi in bands]
 def F(j,r):
  lo,hi=bands[j]
  return 0. if r<=lo else (1. if r>=hi else (M(r)-M(lo))/masses[j])
 def Ai(r): return F(0,r)-F(1,r)
 def Ao(r): return F(2,r)-F(1,r)
 moments=[quad(lambda r:r*r*dm(r),lo,hi,epsabs=1e-13)[0]/m for (lo,hi),m in zip(bands,masses)]
 R2=(moments[1]-moments[0])/(moments[2]-moments[1])
 a=-integrate(lambda r: M(r)*Ai(r)/(r*r) if r else 0.)
 bb=-integrate(lambda r: M(r)*Ao(r)/(r*r) if r else 0.)
 cc=-.5*integrate(lambda r: Ai(r)**2/(r*r) if r else 0.)
 dd=-integrate(lambda r: Ai(r)*Ao(r)/(r*r) if r else 0.)
 ee=-.5*integrate(lambda r: Ao(r)**2/(r*r) if r else 0.)
 W0=-.5*(integrate(lambda r:M(r)**2/r**2 if r else 0.)+1.)
 def deltaW(mi,mo): return a*mi+bb*mo+cc*mi*mi+dd*mi*mo+ee*mo*mo
 def j0(x): return float(np.sinc(x/math.pi))
 for donor_fraction in [.02,.1,.3]:
  mi=donor_fraction*masses[1]
  choices={'inward_only':0.,'moment_neutral':R2*mi}
  roots=np.roots([ee,bb+dd*mi,a*mi+cc*mi*mi])
  physical=sorted(float(x.real) for x in roots if abs(x.imag)<1e-9 and 0<x.real<=masses[1]-mi)
  if physical: choices['energy_neutral']=physical[0]
  row={'c_at_outer_radius':c,'donor_fraction_moved_in':donor_fraction,'donor_mass':masses[1],
       'mi':mi,'R2':R2,'R_energy_linear':-a/bb,'W0':W0,'branches':{}}
  for branch,mo in choices.items():
   # Negative control under-removes donor mass, caught by total mass.
   donor=(mi+mo)*(.99 if args.mutate else 1.)
   mass_error=mi+mo-donor
   I2=mi*moments[0]-donor*moments[1]+mo*moments[2]
   def changed(r): return M(r)+mi*F(0,r)-donor*F(1,r)+mo*F(2,r)
   Wdirect=-.5*(integrate(lambda r:changed(r)**2/r**2 if r else 0.)+changed(1.)**2)
   DW=deltaW(mi,mo)
   ck('mass_'+str((c,donor_fraction,branch)),abs(mass_error)<1e-12)
   ck('positive_density_'+str((c,donor_fraction,branch)),donor<=masses[1]+1e-12)
   ck('energy_identity_'+str((c,donor_fraction,branch)),abs(Wdirect-W0-DW)<1e-10)
   if branch=='moment_neutral':
    ck('moment_cancel_'+str((c,donor_fraction)),abs(I2)<1e-12)
    ck('energy_release_'+str((c,donor_fraction)),DW<0)
   if branch=='energy_neutral':
    ck('energy_zero_'+str((c,donor_fraction)),abs(DW)<1e-12)
    ck('outward_second_moment_'+str((c,donor_fraction)),I2>0)
   transforms=[]
   for k in [.01,.1,1.,3.,10.]:
    U0=integrate(lambda r:j0(k*r)*dm(r))
    Uj=[quad(lambda r:j0(k*r)*dm(r),lo,hi,epsabs=1e-12)[0]/m for (lo,hi),m in zip(bands,masses)]
    dU=mi*Uj[0]-donor*Uj[1]+mo*Uj[2]
    transforms.append({'k_R':k,'delta_U':dU,'halo_U_squared_ratio':((U0+dU)/U0)**2})
   row['branches'][branch]={'mo':mo,'mo_over_mi':mo/mi,'donor_used_fraction':donor/masses[1],
     'mass_error':mass_error,'delta_I2':I2,'delta_W':DW,'direct_energy_residual':Wdirect-W0-DW,
     'linear_outward_energy_fraction':mo*bb/(-mi*a),'transforms':transforms}
  results.append(row)
  print(json.dumps({'c':c,'inward_donor_fraction':donor_fraction,'R2':R2,'R_E':physical[0]/mi if physical else None,
   'moment_energy_fraction':R2*bb/(-a),'energy_branch_donor_used':(mi+physical[0])/masses[1] if physical else None,
   'U2_ratio_kR3':{n:v['transforms'][3]['halo_U_squared_ratio'] for n,v in row['branches'].items()}}))
out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'base':'433d42278ccaab3279d9c54f66ff266c358a3c63','mutate':args.mutate,
 'bands':bands,'results':results,'checks':checks,'non_claims':['Not an RAR halo or observational fit',
 'No stationary DF, angular momentum transport, timescale or entropy proof',
 'Energy-neutral W is only a necessary isolated-virial equilibrium condition']},indent=2)+'\n')
print('checks',sum(x['pass'] for x in checks),'/',len(checks))
raise SystemExit(0 if all(x['pass'] for x in checks) else 1)

from pathlib import Path
import json,math,sys,resource,time
import numpy as np
from scipy.integrate import solve_bvp, simpson
M=100.;Lq=1.99;aq=200.;rows=[];checks=[]
def solve(Q,L,N,seed=None):
 r=np.linspace(1e-4,L,N)
 if seed is None:
  om=.94;I=50.;r0=(3*Q/(8*math.pi*om*I))**(1/3)
  f=math.sqrt(I)/(1+np.exp((r-r0)/1.2));fp=-math.sqrt(I)*np.exp((r-r0)/1.2)/(1.2*(1+np.exp((r-r0)/1.2))**2)
  h=-.02*f*f;hp=-.04*f*fp
  integrand=8*math.pi*om*r*r*f*f/Q
  q=np.concatenate([[0.],np.cumsum((integrand[1:]+integrand[:-1])/2*np.diff(r))]);q/=q[-1]
  y=np.array([f,fp,h,hp,q])
 else:
  om=seed.p[0];y=seed.sol(np.minimum(r,seed.x[-1]));y[0:4,r>seed.x[-1]]=0.;y[4,r>seed.x[-1]]=1.
 def fun(r,y,p):
  f,u,h,v,q=y;om=p[0]
  return np.vstack([u,(1-om*om+2*Lq*f*f+aq*h)*f-2*u/r,v,M*M*h-3*M/8*h*h+h**3+aq*f*f-2*v/r,8*math.pi*om*r*r*f*f/Q])
 def bc(ya,yb,p):return np.array([ya[1],ya[3],ya[4],yb[0],yb[2],yb[4]-1])
 t=time.time();s=solve_bvp(fun,bc,r,y,p=[om],tol=1e-7,max_nodes=6000,verbose=0)
 rr=np.linspace(1e-4,L,20001);f,u,h,v,q=s.sol(rr);om=float(s.p[0]);wt=4*math.pi*rr*rr
 U=.5*M*M*h*h-M/8*h**3+.25*h**4
 rot=float(simpson(wt*om*om*f*f,x=rr));grad=float(simpson(wt*(u*u+.5*v*v),x=rr));pot=float(simpson(wt*(f*f+Lq*f**4+aq*h*f*f+U),x=rr));energy=rot+grad+pot
 charge=float(simpson(wt*2*om*f*f,x=rr));vir=(grad+3*pot-3*rot)/energy
 tail=float(simpson((wt*(om*om*f*f+u*u+.5*v*v+f*f+Lq*f**4+aq*h*f*f+U))[rr>.8*L],x=rr[rr>.8*L]))/energy
 rec={'Q_target':Q,'L':L,'N_initial':N,'status':int(s.status),'message':s.message,'nodes':len(s.x),'omega':om,'Q_integrated':charge,'E':energy,'E_over_Q':energy/charge,'grad':grad,'rot':rot,'potential':pot,'virial_relative':vir,'fmax':float(f.max()),'fmin':float(f.min()),'hmax':float(h.max()),'tail_energy_fraction_outer20percent':tail,'max_rms_residual':float(max(s.rms_residuals)),'runtime_s':time.time()-t}
 rows.append(rec);print(json.dumps(rec),flush=True)
 return s,rec

a=solve(79200.,60.,1000)[1]
b=solve(80000.,60.,1000)[1]
c=solve(80800.,60.,1000)[1]
d=solve(160000.,60.,1100)[1]
for x in rows:
 checks.extend([{'name':str(x['Q_target'])+' tighter collocation','pass':x['status']==0},{'name':str(x['Q_target'])+' tighter Q','pass':abs(x['Q_integrated']/x['Q_target']-1)<1e-7},{'name':str(x['Q_target'])+' tighter virial','pass':abs(x['virial_relative'])<1e-6},{'name':str(x['Q_target'])+' nodeless bound branch','pass':0<x['omega']<1 and x['E_over_Q']<1 and x['fmin']>-1e-7}])
deriv=(c['E']-a['E'])/1600
checks.append({'name':'dE/dQ agrees omega central finite difference','pass':abs(deriv/b['omega']-1)<1e-5})
prior=json.loads((Path(__file__).parent/'run_001/results.json').read_text())
for x in [b,d]:
 z=next(t for t in prior['rows'] if t['Q_target']==x['Q_target'] and t['L']==60)
 checks.append({'name':str(x['Q_target'])+' tight energy convergence','pass':abs(x['E']/z['E']-1)<1e-6})
result={'rows':rows,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(x['pass'] for x in checks),'dE_dQ_finite_difference':deriv,'omega_at_Q':b['omega'],'incremental_merger_energy_at_tight_profiles':2*b['E']-d['E'],'incremental_release_fraction_of_initial_two_profile_energy':(2*b['E']-d['E'])/(2*b['E']),'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Stationary nodeless spherical branch, not proved global minima or nonlinear stability. Gap is energetically available if merger reaches this state, not measured emitted E/Q/J or collision efficiency.'}
assert result['peak_rss_bytes_macos']<200000000
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');sys.exit(0 if result['all_checks_pass'] else 1)

"""Controls for exact projected quantum angular integration and Jacobian."""
import sys,json,time,resource,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
from network import ROOT
from angular_exact import AngularExact,exponential_moments,exact_events
from reaction import full_events
from consistent_background_frozen import ConsistentVertexBackground

def segmented_reference(ev,f,av,order=32):
 z,w=leggauss(order);rhs=np.zeros(len(f));gross=np.zeros(len(f));v=f[ev.index];a=av[ev.index]
 with np.errstate(divide='ignore'):lf=np.log(v);la=np.log(a)
 for u,weight in zip(z,w):
  weights=ev.a+u*ev.b
  with np.errstate(invalid='ignore'):
   forward=np.exp(lf[:,0]+np.sum(np.where(weights[:,1:]>0,weights[:,1:]*la[:,1:],0),axis=1));reverse=np.exp(la[:,0]+np.sum(np.where(weights[:,1:]>0,weights[:,1:]*lf[:,1:],0),axis=1))
  p=ev.coefficient*weight*(forward-reverse);g=ev.coefficient*weight*(forward+reverse);rhs+=np.asarray(ev.Sa@p+u*(ev.Sb@p)).ravel();gross+=np.asarray(abs(ev.Sa)@g+u*(ev.Sb@g)).ravel()
 return rhs,gross

def main(out):
 start=time.monotonic();rng=np.random.default_rng(1729);moment=[]
 for B in (-100.,-40.,-5.,-.1,-.001,0.,.001,.1,5.,40.,100.):
  A=-2-abs(B);got=exponential_moments(A-B,A+B);ref=np.array([quad(lambda u:u**k*math.exp(A+B*u),-1,1,epsabs=1e-14,epsrel=1e-12)[0] for k in range(3)]);moment.append(dict(B=B,error=float(max(abs(got-ref))),relative_scale_error=float(max(abs(got-ref))/max(abs(ref)))))
 synthetic=[]
 for duplicate in (False,True):
  idx=[[0,1,2,1 if duplicate else 3,2 if duplicate else 4]];energy=np.array([3.,1.,2.] if duplicate else [3.,1.,2.,1.,2.]);measure=np.arange(1,len(energy)+1,dtype=float);eta=np.array([1.]+[-1.]*(len(energy)-1));ev=AngularExact(idx,[[1,.5,.5,.5,.5]],[[0,-.3,.3,.3,-.3]],[.7],measure,energy,eta);f=rng.uniform(.05,.6,len(energy));av=1+eta*f;rhs=ev.number_rhs(f,av);J=ev.number_jacobian(f,av);direction=rng.normal(size=len(f))*.1;eps=1e-5;plus=ev.number_rhs(f+eps*direction,1+eta*(f+eps*direction));minus=ev.number_rhs(f-eps*direction,1+eta*(f-eps*direction));ref=(plus-minus)/(2*eps);jerr=float(np.linalg.norm(J@(measure*direction)-ref)/max(np.linalg.norm(ref),1e-300));numerical,_=segmented_reference(ev,f,av,64);f_eq=1/(np.exp(energy/.8)-eta);audit=ev.audit(f_eq);synthetic.append(dict(duplicate=duplicate,Jacobian_relative_error=jerr,reference_relative_error=float(np.linalg.norm(rhs-numerical)/max(np.linalg.norm(rhs),1e-300)),energy_residual=ev.energy_residual,entropy_production=ev.audit(f)['entropy_production'],detailed_balance=audit['detailed_balance_RHS_relative']))
 checkpoint=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/warm_checkpoint001.json').read_text());q=np.array(checkpoint['case']['q']);W=np.array(checkpoint['case']['W']);Y=np.array(checkpoint['state']['Y']);t=.004657258204883617*math.exp(-checkpoint['state']['N']);bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');cases=[]
 for x in (3.6,3.83742513487,4.08,25.4000254000381):
  d=bg.at(x);ev=exact_events(d,t,q,W,source=d['current_source']);f=Y/ev.measure;av=1+ev.eta*f;exact=ev.number_rhs(f,av);gross=ev.number_gross(f,av);reference,reference_gross=segmented_reference(ev,f,av,32);scale=max(sum(abs(exact)),1e-300);direction=f*av*rng.normal(size=len(f));eps=1e-5;plus=ev.number_rhs(f+eps*direction,av+eps*ev.eta*direction);minus=ev.number_rhs(f-eps*direction,av-eps*ev.eta*direction);fd=(plus-minus)/(2*eps);J=ev.number_jacobian(f,av);jacerr=float(np.linalg.norm(J@(ev.measure*direction)-fd)/max(np.linalg.norm(fd),1e-300));f_eq=1/(np.exp(np.minimum(ev.energy/.008,700))-ev.eta);audit=ev.audit(f_eq);comparisons=[]
  for order in (2,4,8,16,32,64):
   old=full_events(d,t,q,W,angles=order,source=d['current_source']);oldrhs=np.asarray(old.S@old.flux(f)).ravel();comparisons.append(dict(angles=order,relative_RHS_L1=float(sum(abs(oldrhs-exact))/scale)))
  row=dict(x=x,segments=len(ev.coefficient),event_energy_residual=ev.energy_residual,energy_rhs_relative=float(abs(ev.energy@exact)/max(sum(gross)*max(ev.energy),1e-300)),entropy_production=ev.audit(f,av)['entropy_production'],detailed_balance_RHS_relative=audit['detailed_balance_RHS_relative'],segmented32_RHS_L1_relative=float(sum(abs(reference-exact))/scale),segmented32_gross_L1_relative=float(sum(abs(reference_gross-gross))/max(sum(gross),1e-300)),Jacobian_direction_relative_error=jacerr,global_angle_comparisons=comparisons);cases.append(row);print(row,flush=True)
 checks=dict(moment_integrals=max(m['relative_scale_error'] for m in moment)<1e-11,synthetic_Jacobians=max(r['Jacobian_relative_error'] for r in synthetic)<1e-7,synthetic_duplicates=max(r['reference_relative_error'] for r in synthetic)<1e-11,event_energy=max(r['event_energy_residual'] for r in cases)<1e-11,energy_RHS=max(r['energy_rhs_relative'] for r in cases)<1e-10,thermal_detailed_balance=max(r['detailed_balance_RHS_relative'] for r in cases)<1e-10,actual_Jacobian_directions=max(r['Jacobian_direction_relative_error'] for r in cases)<1e-5,actual_segmented_reference=max(r['segmented32_RHS_L1_relative'] for r in cases)<1e-6,entropy_nonnegative=min(r['entropy_production'] for r in cases)>-1e-20)
 checks={k:bool(v) for k,v in checks.items()};result=dict(claim_id='CC10_EXACT_ANGULAR_QUANTUM_OPERATOR_CONTROLS',moments=moment,synthetic=synthetic,cases=cases,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Exact angular integration for finite energy/entropy interpolation; derivative and independent segmented quadrature controls onactualwarmandpole masses/distribution. No momentum-grid convergence or history claim.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,result['runtime_seconds']);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])

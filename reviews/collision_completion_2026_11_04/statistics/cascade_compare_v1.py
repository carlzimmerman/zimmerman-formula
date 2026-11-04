"""Actual 25-group cascade: quantum versus classical factors, both inverse.

Input source files are immutable. This adds no portal or annihilation channel.
"""
import sys,json,time,resource,math
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import coo_matrix,diags
from numpy.polynomial.legendre import leggauss
from quantum import ROOT,background,ReactionEvents,entropy
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from network import table
from reaction import full_events,moments,serial_moments,thermal

class Classical:
 def __init__(self,ev):self.__dict__.update(ev.__dict__)
 def products(self,f):
  v=np.maximum(np.asarray(f)[self.index],0.)
  with np.errstate(divide='ignore',invalid='ignore'):
   logs=np.log(v[:,1:]);rev=np.exp(np.sum(np.where(self.weights[:,1:]>0,self.weights[:,1:]*logs,0.),axis=1))
  return v[:,0],rev,v,np.ones_like(v)
 def flux(self,f):
  a,b,_,_=self.products(f);return self.coefficient*(a-b)
 def rhs(self,f):return np.asarray(self.S@self.flux(f)).ravel()/self.measure
 def rhs_jacobian(self,f):
  a,b,v,_=self.products(f);deriv=np.zeros_like(v);deriv[:,0]=1.;deriv[:,1:]=-self.weights[:,1:]*b[:,None]/np.maximum(v[:,1:],1e-30)
  D=coo_matrix(((self.coefficient[:,None]*deriv).ravel(),(np.repeat(np.arange(len(a)),5),self.index.ravel())),shape=(len(a),len(f))).tocsr()
  return diags(1/self.measure)@self.S@D

def grid(n=8):
 z,w=leggauss(n);q=[];W=[]
 for lo,hi in zip([0.,.1,1.,5.,20.],[.1,1.,5.,20.,80.]):
  nodes=(lo+hi)/2+(hi-lo)*z/2;q.extend(nodes);W.extend((hi-lo)*w/2*nodes**2)
 return np.asarray(q),np.asarray(W)

def simulate(ev,mode,scale,zend=20.):
 solver=ev if mode=='quantum' else Classical(ev);n=len(ev.q);f0=np.zeros(len(ev.measure));f0[ev.by['Fc_0']*n:(ev.by['Fc_0']+1)*n]=1/(np.exp(ev.q)+1)
 start=time.monotonic();sol=solve_ivp(lambda z,f:solver.rhs(f)/scale,(0,zend),f0,method='BDF',jac=lambda z,f:solver.rhs_jacobian(f)/scale,rtol=1e-5,atol=2e-12,t_eval=np.r_[0.,np.geomspace(.001,zend,40)])
 initial=moments(ev,f0);n0=initial['charged_number'];E0=initial['total_energy'];hist=[];n=len(ev.q);measure=ev.measure.reshape((-1,n));eta=ev.eta
 for z,f in zip(sol.t,sol.y.T):
  m=serial_moments(ev,f);groupf=f.reshape((-1,n));counts=np.sum(measure*groupf,axis=1);sm=2*math.pi**2/45*106.75*(ev.t/.02)**3;u1=ev.by['F1_1'];p=ev.t*ev.q;den=counts[u1]
  m.update(B3_lifetimes=float(z),time_mu=float(z/scale),charged_fraction=m['charged_number']/n0,energy_relative_error=(m['total_energy']-E0)/E0,min_f=float(min(f)),max_fermion_f=float(max(f[eta<0])),U1_yield=float(counts[u1]*ev.t**3/sm),U1_mean_p_over_mu=float(measure[u1]@(groupf[u1]*p)/den) if den else 0.,U1_max_f=float(max(groupf[u1])),soft_U1_number_fraction=float(measure[u1]@(groupf[u1]*(ev.q<.1))/den) if den else 0.)
  if mode=='quantum':m['quantum_entropy_mu3']=entropy(f,ev.measure,eta)*ev.t**3
  hist.append(m)
 print('case',ev.x,mode,sol.success,sol.nfev,hist[-1]['charged_fraction'],hist[-1]['U1_yield'],hist[-1]['U1_max_f'],flush=True)
 return dict(mode=mode,success=bool(sol.success),message=sol.message,nfev=sol.nfev,njev=sol.njev,runtime_seconds=time.monotonic()-start,history=hist,initial_f=f0.tolist(),final_f=sol.y[:,-1].tolist())

def run(out):
 start=time.monotonic();cases=[];q,W=grid(8);checks={}
 def save():
  Path(out).write_text(json.dumps(dict(claim_id='CC10_CASCADE_QUANTUM_CLASSICAL_V1',checks=checks,cases=cases,q=q.tolist(),W=W.tolist(),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual25group physical tree FFS/SSS network, leadingcurrent replacement oflowest F/C andgaugino masses. Fixedx3,5Tc.004, physicalFonlyFD. QuantumPauli/Bose vsclassicalavailability1, BOTH retain inverse. Diagonalneutralparents, missingvectors/2to2/coherence; notcosmology.'),indent=2)+'\n')
 for x in [3.,5.]:
  data=table(x);source=background(x);ev=full_events(data,.004,q,W,angles=6,source=source);B3=next(g for g in data['groups'] if g['id']=='S8_1');scale=B3['width'];eq=thermal(ev,.008);audit=ev.audit(eq)
  # Independent entropy chain-rule comparison at an interior non-equilibrium
  # state, without using ReactionEvents.affinity in the first expression.
  test=eq*np.exp(.04*np.sin(np.arange(len(eq))));phi=np.log(test/(1+ev.eta*test));lhs=-float((ev.measure*phi)@ev.rhs(test));rhs=float(ev.flux(test)@ev.affinity(test));entropy_relative=abs(lhs-rhs)/max(abs(lhs),abs(rhs),1e-300)
  runs=[simulate(ev,mode,scale) for mode in ['quantum','classical']];A=runs[0]['history'][-1];B=runs[1]['history'][-1]
  comparison={k:dict(quantum=A[k],classical=B[k],quantum_over_classical=A[k]/B[k] if B[k] else None) for k in ['charged_fraction','U1_yield','U1_mean_p_over_mu','U1_max_f','neutral_force','neutral_massive_energy']}
  cases.append(dict(x=x,Tc=.004,scale_B3_width=scale,groups=ev.groups,channels=ev.channels,events=len(ev.coefficient),audit=audit,entropy_chainrule_relative=entropy_relative,runs=runs,comparison=comparison));save()
 checks.update(completed=all(r['success'] for c in cases for r in c['runs']),event_energy=max(c['audit']['energy_residual'] for c in cases)<1e-11,detailed_balance=max(c['audit']['detailed_balance_relative'] for c in cases)<1e-9,entropy_chainrule=max(c['entropy_chainrule_relative'] for c in cases)<1e-11,energy=max(abs(h['energy_relative_error']) for c in cases for r in c['runs'] for h in r['history'])<1e-7,quantum_pauli=max(h['max_fermion_f'] for c in cases for r in c['runs'] if r['mode']=='quantum' for h in r['history'])<1+1e-7,positive=min(h['min_f'] for c in cases for r in c['runs'] for h in r['history'])>-1e-7)
 save();print(json.dumps(checks),flush=True);assert all(checks.values())
if __name__=='__main__':run(sys.argv[1])

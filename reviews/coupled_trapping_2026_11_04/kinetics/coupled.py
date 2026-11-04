"""CT09 phase-space scalar absorption + action-averaged field evolution.
This is an explicitly conditional limiting network, not the actual cascade.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq,minimize_scalar
from numpy.polynomial.legendre import leggauss
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic'))
from stationary import light
MASS=62.;DEG=24.;PREF=DEG/(2*math.pi**2)

class Model:
 def __init__(self,point,spin,bins=48,orbitn=16,stride=1,closure='bins'):
  self.point=point;self.mu=point['mu_GeV'];self.t0=spin['TD_over_mu'];self.x0=spin['X_over_mu'];self.closure=closure;self.stride=stride
  self.v=CubicSpline(point['grid'],point['T0_potential_mu4'],bc_type=((1,point['origin_force']),(2,0)))
  self.grid=np.unique(np.r_[0,np.linspace(.001,10,100),np.linspace(10,40,80),np.linspace(40,200,40)])
  # Uniform bins to q=20 and a low-occupation tail to q=50.
  self.edges=np.r_[np.linspace(0,20,bins+1),25.,30.,40.,50.];a=self.edges[:-1];b=self.edges[1:]
  self.W=(b**3-a**3)/3;self.q=.75*(b**4-a**4)/(b**3-a**3);self.f0=1/(np.exp(self.q)+1)
  self.z,self.zw=leggauss(orbitn);self.theta=(self.z+1)*math.pi/2;self.tw=self.zw*math.pi/2
  self.kz,self.kw=leggauss(4)
  self.tables=json.loads((HERE/'run_spectrum_001/result.json').read_text())['cases'][::stride]
  self.calls=0;self.max_hierarchy=0
 def H(self,N):return math.sqrt(math.pi**2*106.75/90)*(self.t0*math.exp(-N))**2*self.mu/(2.435e18*.02**2)
 def gas(self,x,t,f):
  xx=np.atleast_1d(x);ms=np.array([light(float(a))[0] for a in xx]);en=np.sqrt(ms[:,None]**2+(t*self.q[None,:])**2);rho=PREF*t**3*(en@(self.W*f));press=PREF*t**3/3*((t*self.q)**2/en)@(self.W*f)
  return rho,press,en
 def potential(self,x,t,f):return self.v(x)+self.gas(x,t,f)[0]
 def orbital(self,N,f,J=None,E=None):
  t=self.t0*math.exp(-N);ug=self.potential(self.grid,t,f);imin=int(np.argmin(ug));left=self.grid[max(0,imin-1)];right=self.grid[min(len(self.grid)-1,imin+1)]
  mini=minimize_scalar(lambda x:float(self.potential(x,t,f)[0]),bounds=(left,right),method='bounded',options={'xatol':1e-10});xm=mini.x;emin=mini.fun;elim=min(float(ug[0]),float(ug[-1]))
  if not emin<elim:raise RuntimeError('no bounded positive-x well in tested potential domain')
  def make(en,full=False):
   if en<=emin:en=emin+max(1e-30,abs(emin)*1e-14)
   xl=brentq(lambda x:float(self.potential(x,t,f)[0])-en,0,xm,xtol=1e-11);xr=brentq(lambda x:float(self.potential(x,t,f)[0])-en,xm,200,xtol=1e-11)
   mid=(xl+xr)/2;half=(xr-xl)/2;xs=mid-half*np.cos(self.theta);dx=half*np.sin(self.theta);rho,pr,ee=self.gas(xs,t,f);delta=np.maximum(en-self.v(xs)-rho,1e-35);w=self.tw*dx/np.sqrt(delta);period=math.sqrt(2*MASS)*sum(w);weights=w/sum(w);action=math.sqrt(2*MASS)/math.pi*sum(self.tw*dx*np.sqrt(delta))
   if not full:return action
   return dict(E=en,J=action,xl=xl,xr=xr,xm=xm,period=period,xs=xs,weights=weights,rho=rho,pr=pr,en=ee,kin2=2*delta,t=t,minimum=emin)
  if E is None:
   jmax=make(elim-max(1e-30,abs(elim)*1e-12));
   if J>=jmax:raise RuntimeError('positive-x separatrix reached; full signed-X extension required')
   E=brentq(lambda en:make(en)-J,emin+max(1e-30,abs(emin)*1e-14),elim-max(1e-30,abs(elim)*1e-12),xtol=1e-23,rtol=1e-12)
  return make(E,True)
 def kernel(self,x,t):
  m=light(x)[0];ei=np.sqrt(m*m+(t*self.edges)**2);elo=ei[:-1];ehi=ei[1:];de=ehi-elo;K=np.zeros((len(de),len(de)));position=x/(.1*self.stride);i=min(int(position),len(self.tables)-2);mix=position-i
  for row,fac in ((self.tables[i],1-mix),(self.tables[i+1],mix)):
   if fac<=0:continue
   for parent,width in row['parents']:
    if parent<=2*m:continue
    beta=math.sqrt(1-4*m*m/parent**2);c=(parent*parent-2*m*m)/2;d=math.sqrt(max(0,c*c-m**4));aa=np.zeros_like(K)
    for z,w in zip(self.kz,self.kw):
     e1=(elo+ehi)/2+de*z/2;p1=np.sqrt(np.maximum(0,e1*e1-m*m));low=(c*c+m*m*p1*p1)/(c*e1+p1*d);high=(c*e1+p1*d)/max(m*m,1e-200);overlap=np.maximum(0,np.minimum(high[:,None],ehi[None,:])-np.maximum(low[:,None],elo[None,:]));aa+=w*de[:,None]/2*overlap
    aa=(aa+aa.T)/2;K+=fac*2*width*parent/(DEG*beta)*aa
  return K
 def collision(self,x,t,f):return -f*(self.kernel(x,t)@f)/(t**3*self.W)
 def setup(self):
  r0=self.gas(self.x0,self.t0,self.f0)[0][0];E0=float(self.v(self.x0))+r0;orb=self.orbital(0,self.f0,E=E0);self.J0=orb['J'];self.E0=E0;self.scale=r0
  return np.r_[np.log(self.f0),0.,0.,0.]
 def rhs(self,N,y,loss=True,detail=False):
  self.calls+=1;n=len(self.f0);f=np.exp(np.clip(y[:n],-700,0));J=self.J0*math.exp(y[n]);orb=self.orbital(N,f,J=J);w=orb['weights'];t=orb['t'];H=self.H(N);dens=PREF*t**3*self.W
  if loss:
   cs=np.array([self.collision(x,t,f) for x in orb['xs']]);cavg=w@cs;ecavg=w@(orb['en']*cs);eavg=w@orb['en'];cov=float(dens@(ecavg-eavg*cavg));q=-float(dens@ecavg)
   if self.closure=='amplitude':
    cavg=f*float((self.W@cavg)/(self.W@f));cov=0.;q=-float(dens@(eavg*cavg))
  else:cavg=np.zeros_like(f);cov=0.;q=0
  rate=float(-self.W@cavg/(self.W@f));hier=rate*orb['period']/(2*math.pi);self.max_hierarchy=max(self.max_hierarchy,hier)
  lnJ=-3+orb['period']/(2*math.pi*H*J)*cov
  rad=y[n+1]*self.scale*math.exp(-4*N);losswork=3*float(w@(orb['kin2']+orb['rho']+orb['pr']))+4*rad
  dy=np.r_[cavg/np.maximum(f,1e-300)/H,lnJ,math.exp(4*N)*q/H/self.scale,losswork/self.scale]
  if detail:
   num=PREF*t**3*float(self.W@f);s=2*math.pi**2/45*106.75*(t/.02)**3;shape=f/self.f0;meaningful=self.W*self.f0>max(self.W*self.f0)*1e-5
   return dict(N=N,Tc_over_mu=t,x_inner=orb['xl'],x_outer=orb['xr'],x_minimum=orb['xm'],energy=orb['E'],action=J,rate_over_H=rate/H,rate_over_oscillation=hier,H_over_oscillation=H*orb['period']/(2*math.pi),survival=float((self.W@f)/(self.W@self.f0)),Y_charged=num/s,shape_suppression_range=[float(min(shape[meaningful])),float(max(shape[meaningful]))],momentum_rms_over_T=math.sqrt(float((self.W*self.q*self.q)@f/(self.W@f))),radiation_energy_mu4=rad,energy_ledger_error=(orb['E']+rad+y[n+2]*self.scale-self.E0)/self.scale,action_collision_term=lnJ+3,mean_energy_N=-3*float(w@(orb['kin2']+orb['rho']+orb['pr']))-q/H)
  return dy

def evolve(model,loss,Nend,tol=.002):
 y=model.setup();N=0.;step=.001;history=[model.rhs(N,y,loss,True)];accepted=0;rejected=0;reason='target cooling reached';last=None
 while N<Nend-1e-13:
  step=min(step,Nend-N,.02)
  try:
   a=model.rhs(N,y,loss);yn=y+step*a;b=model.rhs(N+step,yn,loss);yh=y+step*(a+b)/2
   # Shape errors matter only where initial number weight is appreciable.
   n=len(model.f0);weight=model.W*model.f0;active=weight>max(weight)*1e-5;err=max(float(max(abs((yh-yn)[:n][active]))),abs(float(yh[n]-yn[n])),abs(float((yh-yn)[n+1]))*.1)
   if err>tol:
    rejected+=1;step*=max(.15,.8*math.sqrt(tol/err));continue
   N+=step;y=yh;accepted+=1;last=model.rhs(N,y,loss,True)
   if accepted==1 or N-history[-1]['N']>.025 or N>=Nend-1e-13:history.append(last)
   if last['rate_over_oscillation']>.1:reason='averaging hierarchy failed';break
   if abs(last['energy_ledger_error'])>.02:reason='energy ledger tolerance failed';break
   step*=min(2.,max(.5,.9*math.sqrt(tol/max(err,1e-14))))
   if accepted>12000:reason='step budget reached';break
  except RuntimeError as exc:reason=str(exc);break
 if last is not None and history[-1]['N']!=last['N']:history.append(last)
 f=np.exp(np.clip(y[:len(model.f0)],-700,0));return dict(closure=model.closure,loss=loss,reason=reason,accepted=accepted,rejected=rejected,rhs_calls=model.calls,max_rate_over_oscillation=model.max_hierarchy,history=history,q_edges=model.edges.tolist(),q_centers=model.q.tolist(),initial_f=model.f0.tolist(),final_f=f.tolist(),final_N=N,final_logJ=float(y[len(model.f0)]),numerical_tolerance=tol)

def main(out,mode='main'):
 start=time.monotonic();stat=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text());spins=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text());cases=[]
 if mode=='controls':
  # Independent momentum integral for a constant test parent, FD and MB.
  from nonthermal import phase_integral
  controls=[]
  for bins in (48,96,192):
   p=stat['points'][0];s=next(z for z in spins['points'] if z['kind']==p['kind'])['spins'][0];m=Model(p,s,bins=bins);m.tables=[{'parents':[[.03,1e-9]]},{'parents':[[.03,1e-9]]}];m.stride=100000
   for x,t in ((.1,.004),(3,.004),(5,.003)):
    mass=light(x)[0];loss=m.collision(x,t,m.f0);gamma=-PREF*t**3*float(m.W@loss)/2;ref=1e-9*.03*t*t/(2*math.pi**2)*phase_integral(.03,mass,t,192);controls.append(dict(bins=bins,x=x,t=t,gamma=gamma,parent_integral=ref,relative_error=abs(gamma/ref-1)))
  result=dict(claim_id='CT09_PHASE_SPACE_KERNEL_CONTROLS',controls=controls,checks={'finest_inverse_integral_agreement':max(z['relative_error'] for z in controls if z['bins']==192)<.01},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 else:
  for p in stat['points']:
   s=next(z for z in spins['points'] if z['kind']==p['kind'])['spins'][0];Nend=math.log(s['TD_over_mu']/.0005)
   configs=[(False,'bins',48,16,1,.001),(True,'bins',48,16,1,.001),(True,'amplitude',48,16,1,.001)] if mode=='main' else [(True,'bins',72,24,1,.0004),(True,'bins',48,16,2,.0004)]
   for loss,closure,bins,orb,st,tol in configs:
    model=Model(p,s,bins=bins,orbitn=orb,stride=st,closure=closure);run=evolve(model,loss,Nend,tol);run.update(kind=p['kind'],mu_GeV=p['mu_GeV'],bins=bins,orbit_nodes=orb,rate_table_stride=st);cases.append(run);print(p['kind'],loss,closure,run['reason'],run['final_N'],run['history'][-1]['survival'],flush=True)
  result=dict(claim_id='CT09_COUPLED_ABSORPTION_LIMIT',cases=cases,checks={'all_completed_to_cooling':all(z['reason']=='target cooling reached' for z in cases),'energy_ledger':all(max(abs(h['energy_ledger_error']) for h in z['history'])<.02 for z in cases),'occupation_monotone':all(all(a>=b-1e-14 for a,b in zip(z['initial_f'],z['final_f'])) for z in cases),'averaging_hierarchy':all(z['max_rate_over_oscillation']<.1 for z in cases)},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Conditional action-averaged positive-X leading rigid-fermion phase-space calculation. Scalar inverse-decay parents are either all irreversibly absorbed or ignored (zero-loss number limit). Radiation receives exact binwise removed energy. Actual carrier-preserving scalar conversion/cascade and photino sources omitted. FD-amplitude evolution is diagnostic only. No complete kinetic network or DE/DM solution.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));assert all(result['checks'].values()),result['checks']
if __name__=='__main__':main(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'main')

"""CT09 two charged distributions, actual vacuum conversions, parent absorption.
Conditional empty gaugino bath: Pauli blocking/inverse reactions are omitted.
"""
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize_scalar
from numpy.polynomial.legendre import leggauss
from averaged_v2 import Model,ROOT,HERE,PREF,MASS,DEG

class Two(Model):
 def __init__(self,*args,absorbing=True,**kw):
  super().__init__(*args,**kw)
  self.edges=np.unique(np.r_[0,.05,.1,.2,.35,.5,.75,1.,np.linspace(1.25,20,kw.get('bins',16)),25.,30.,40.,50.,75.,100.]);aa=self.edges[:-1];bb=self.edges[1:];self.W=(bb**3-aa**3)/3;self.q=.75*(bb**4-aa**4)/(bb**3-aa**3);self.f0=1/(np.exp(self.q)+1);self.n=len(self.W);self.norm=float(self.W@self.f0);self.absorbing=absorbing;self.maxlocal=0;self.maxnum=0;self.overflow=0;self.floor_count=0
  self.scalar=json.loads((HERE/'run_scalar_table_001/result.json').read_text())['cases'];self.sx=np.array([r['x'] for r in self.scalar]);self.sources=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/photino/run_source004/result.json').read_text())['grid'];self.rx=np.array([r['x'] for r in self.sources]);self.az,self.aw=leggauss(8)
 def gas(self,x,t,f):
  x=np.atleast_1d(x);F=self.mass(x);S=.003/2*np.sqrt(x*x+2/(31*.003));p=t*self.q;en=np.c_[np.sqrt(F[:,None]**2+p[None,:]**2),np.sqrt(S[:,None]**2+p[None,:]**2)];wf=np.tile(self.W,2)*f;rho=PREF*t**3*(en@wf);pr=PREF*t**3/3*((np.tile(p,2)**2/en)@wf);return rho,pr,en
 def setup(self):
  self.initf=np.r_[self.f0,np.zeros(self.n)];r0=self.gas(self.x0,self.t0,self.initf)[0][0];self.E0=float(self.v(self.x0))+r0;self.scale=r0;orb=super().orbital(0,self.initf,E=self.E0);self.J0=orb['J'];return np.r_[self.W*self.f0/self.norm,np.zeros(self.n),0.,0.,0.,0.]
 def orbital(self,N,f,J=None,E=None):
  if E is not None or J>self.J0*1e-6:return super().orbital(N,f,J=J,E=E)
  self.floor_count+=1;t=self.t0*math.exp(-N);ug=self.potential(self.grid,t,f);mins=np.where((ug[1:-1]<ug[:-2])&(ug[1:-1]<ug[2:]))[0]+1
  if not len(mins):raise RuntimeError('no local minimum in harmonic orbit continuation')
  i=int(mins[0]);r=minimize_scalar(lambda x:float(self.potential(x,t,f)[0]),bounds=(self.grid[i-1],self.grid[i+1]),method='bounded',options={'xatol':1e-10});xm=r.x;h=.001;k=(float(self.potential(xm+h,t,f)[0])+float(self.potential(xm-h,t,f)[0])-2*r.fun)/h**2
  if k<=0:raise RuntimeError('nonpositive harmonic-well curvature')
  omega=math.sqrt(k/MASS);amp=math.sqrt(2*J*omega/k);xs=xm-amp*np.cos(self.theta);rho,pr,en=self.gas(xs,t,f);weights=self.tw/math.pi;delta=J*omega*np.sin(self.theta)**2
  return dict(E=r.fun+omega*J,J=J,xl=xm-amp,xr=xm+amp,xm=xm,period=2*math.pi/omega,xs=xs,weights=weights,rho=rho,pr=pr,en=en,kin2=2*delta,t=t,minimum=r.fun)
 def scalar_kernel(self,x,t):
  m=.003/2*math.sqrt(x*x+2/(31*.003));i=min(max(0,int(np.searchsorted(self.sx,x)-1)),len(self.sx)-2);alpha=min(1,max(0,(x-self.sx[i])/(self.sx[i+1]-self.sx[i])));parents=[]
  for row,fac in ((self.scalar[i],1-alpha),(self.scalar[i+1],alpha)):
   for M,W in row['parents']:
    if fac<=0 or M<=2*m:continue
    b0=math.sqrt(max(0,1-4*row['mS']**2/M**2))
    if b0>1e-10:parents.append((M,fac*W/b0))
  if not parents:return np.zeros((self.n,self.n))
  pw=np.array(parents);pm=pw[:,0];coef=pw[:,1];ei=np.sqrt(m*m+(t*self.edges)**2);lo=ei[:-1];hi=ei[1:];de=hi-lo;c=(pm*pm-2*m*m)/2;d=np.sqrt(np.maximum(0,c*c-m**4));e1=(lo+hi)[None,:]/2+self.kz[:,None]*de[None,:]/2;p1=np.sqrt(np.maximum(0,e1*e1-m*m));ce=c[:,None,None]*e1[None,:,:];pd=d[:,None,None]*p1[None,:,:];lower=(c[:,None,None]**2+m*m*p1[None,:,:]**2)/(ce+pd);upper=(ce+pd)/(m*m);over=np.maximum(0,np.minimum(upper[:,:,:,None],hi[None,None,None,:])-np.maximum(lower[:,:,:,None],lo[None,None,None,:]));aa=np.einsum('kqij,q,i->kij',over,self.kw,de/2,optimize=True);aa=(aa+aa.transpose(0,2,1))/2
  return np.einsum('k,kij->ij',8*coef*pm/DEG,aa,optimize=True)
 def conversion(self,x,t):
  n=self.n;p=t*self.q;F=float(self.mass(x));S=.003/2*math.sqrt(x*x+2/(31*.003));masses=(F,S);A=np.zeros((2*n,2*n));events=np.zeros(2*n)
  for a,b,key in ((0,1,'gauge_channels_total_over_mu'),(1,0,'reverse_gauge_channels_total_over_mu')):
   gamma=float(np.interp(x,self.rx,[r[key] for r in self.sources]));ma=masses[a];mb=masses[b]
   if gamma<=0 or ma<=mb:continue
   ea=np.sqrt(ma*ma+p*p);eb=np.sqrt(mb*mb+p*p);estar=(ma*ma+mb*mb)/(2*ma);pstar=(ma*ma-mb*mb)/(2*ma);rate=gamma*ma/ea;P=np.zeros((n,n))
   for z,w in zip(self.az,self.aw):
    target=(ea*estar+p*pstar*z)/ma;pos=np.searchsorted(eb,target);below=pos==0;above=pos==n;self.overflow=max(self.overflow,float(max(np.maximum(eb[0]-target,target-eb[-1]))));lo=np.clip(pos-1,0,n-2);hi=lo+1;alpha=np.clip((target-eb[lo])/(eb[hi]-eb[lo]),0,1);jj=np.arange(n);P[lo,jj]+=w/2*(1-alpha);P[hi,jj]+=w/2*alpha
   aa=slice(a*n,(a+1)*n);bb=slice(b*n,(b+1)*n);A[aa,aa]-=np.diag(rate);A[bb,aa]+=P*rate[None,:];events[aa]=rate
  return A,events
 def rate(self,N,y,detail=False):
  n=self.n;u=np.maximum(y[:2*n],0);f=u*self.norm/np.tile(self.W,2);J=self.J0*math.exp(max(-30,float(y[2*n])));orb=self.orbital(N,f,J=J);w=orb['weights'];t=orb['t'];H=self.H(N);Bs=[];es=[]
  for x in orb['xs']:
   B,event=self.conversion(float(x),t)
   if self.absorbing:
    rf=super().kernel(float(x),t)@f[:n]/(t**3*self.W);rs=self.scalar_kernel(float(x),t)@f[n:]/(t**3*self.W);B-=np.diag(np.r_[rf,rs])
   Bs.append(B);es.append(event)
  Bs=np.array(Bs);es=np.array(es);Bavg=np.einsum('k,kij->ij',w,Bs);cu=np.einsum('kij,j->ki',Bs,u);cavg=Bavg@u;eavg=w@orb['en'];ecavg=w@(orb['en']*cu);pref=PREF*t**3*self.norm;cov=pref*float(sum(ecavg-eavg*cavg));Q=-pref*float(sum(ecavg));lnJ=-3+orb['period']/(2*math.pi*H*J)*cov
  if y[2*n]<-20:lnJ=max(-3.,lnJ)
  rad=y[2*n+1]*self.scale*math.exp(-4*N);work=3*float(w@(orb['kin2']+orb['rho']+orb['pr']))+4*rad;events=float(w@(es@u))/H;local=max(float(max(-np.diagonal(B))) for B in Bs)*orb['period']/(2*math.pi);self.maxlocal=max(self.maxlocal,local);numberloss=-float(sum(cavg));self.maxnum=max(self.maxnum,numberloss/max(sum(u),1e-300)*orb['period']/(2*math.pi));d=np.array([lnJ,math.exp(4*N)*Q/H/self.scale,work/self.scale,events])
  if not detail:return Bavg/H,d
  entropy=2*math.pi**2/45*106.75*(t/.02)**3;shape=bool(np.all(u>=0));return dict(N=N,Tc_over_mu=t,x_inner=orb['xl'],x_outer=orb['xr'],x_minimum=orb['xm'],energy=orb['E'],action=J,survival=float(sum(u)),fermion_number_fraction=float(sum(u[:n])),scalar_number_fraction=float(sum(u[n:])),Y_charged=pref*float(sum(u))/entropy,radiation_energy_mu4=rad,gauge_events_per_initial_carrier=float(y[-1]),energy_ledger_error=(orb['E']+rad+y[2*n+2]*self.scale-self.E0)/self.scale,rate_over_oscillation=local,numberloss_over_H=numberloss/max(sum(u),1e-300)/H,H_over_oscillation=H*orb['period']/(2*math.pi))

def evolve_two(model,Nend,tol=.0015):
 y=model.setup();n=model.n;N=0.;step=1e-5;accepted=0;rejected=0;history=[model.rate(N,y,True)];reason='target cooling reached'
 while N<Nend-1e-12:
  step=min(step,.01,Nend-N)
  try:
   A,a=model.rate(N,y);yp=np.r_[expm(step*A)@y[:2*n],y[2*n:]+step*a];B,b=model.rate(N+step,yp);yn=np.r_[expm(step*(A+B)/2)@y[:2*n],y[2*n:]+step*(a+b)/2];err=max(float(sum(abs(yn[:2*n]-yp[:2*n])))/max(float(sum(yn[:2*n])),1e-4),abs(float(yn[2*n]-yp[2*n]))*.1,abs(float(yn[2*n+1]-yp[2*n+1]))*.05)
   if err>tol:rejected+=1;step*=max(.15,.8*math.sqrt(tol/err));continue
   N+=step;y=yn;accepted+=1;last=model.rate(N,y,True)
   if accepted==1 or N-history[-1]['N']>.02 or N>=Nend-1e-12:history.append(last)
   if model.maxlocal>.1:reason='local collision averaging hierarchy failed';break
   if abs(last['energy_ledger_error'])>.02:reason='energy ledger tolerance failed';break
   step*=min(2,max(.5,.9*math.sqrt(tol/max(err,1e-14))))
   if accepted>15000:reason='step budget reached';break
  except RuntimeError as exc:
   rejected+=1;step*=.25
   if step<1e-11:reason=str(exc);break
 if history[-1]['N']!=N:history.append(model.rate(N,y,True))
 return dict(reason=reason,accepted=accepted,rejected=rejected,history=history,final_N=N,q_edges=model.edges.tolist(),q_centers=model.q.tolist(),initial_f_F=model.f0.tolist(),final_f_F=(y[:n]*model.norm/model.W).tolist(),final_f_S_number_normalization=(y[n:2*n]*model.norm/model.W).tolist(),scalar_actual_occupation_multiplier=2,max_local_rate_over_oscillation=model.maxlocal,max_numberloss_over_oscillation=model.maxnum,max_daughter_energy_grid_overflow=model.overflow,harmonic_floor_evaluations=model.floor_count,tolerance=tol)

def main(out,kind,absorb='yes',retune='no'):
 start=time.monotonic();stat=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text());spins=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text());p=next(z for z in stat['points'] if z['kind']==kind);s=next(z for z in spins['points'] if z['kind']==kind)['spins'][0]
 if retune=='yes':
  r=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/gravity_resonance/run_001/result.json').read_text())['rows'][-1]['global_profile'];p=dict(p);p.update(grid=r['grid'],T0_potential_mu4=r['V0_origin_subtracted_mu4'],origin_force=r['origin_force'],origin_curvature=r['origin_curvature'])
 model=Two(p,s,bins=16,orbitn=12,absorbing=absorb=='yes')
 if retune=='yes':model.grid=np.unique(np.r_[0,np.linspace(.001,10,100),np.linspace(10,40,160)])
 run=evolve_two(model,math.log(s['TD_over_mu']/.0005));run.update(kind=kind,absorbing_parents=absorb=='yes',retuned_gravity=retune=='yes',mu_GeV=p['mu_GeV']);result=dict(claim_id='CT09_TWO_CHARGED_SPECIES',case=run,checks={'cooling_reached':run['reason']=='target cooling reached','energy_ledger':bool(max(abs(h['energy_ledger_error']) for h in run['history'])<.02),'local_averaging_hierarchy':bool(model.maxlocal<.1)},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Conditional unblocked twocharged momentumdistributions, vacuumF↔S+gaugino widths, isotropic two-bodymomentum redistribution and energyconservingdaughter interpolation, scalarparentsallabsorbedorignored. Allgauginos assignedmasslessredshiftingenergy afterbirth; inverse andPauli terms omitted despiteindependentfillobstruction. No actualneutralcascade, scalarresonancecoherentexit orfinalphotinohistory;16bulk bins, leadingglobalpotential, finiteactionaveraging. Retunedrunchangesphysicalprotectedε andkeepspriorconditionalinitialx,T.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));print(kind,absorb,retune,run['reason'],run['history'][-1]);assert all(result['checks'].values())
if __name__=='__main__':main(*sys.argv[1:])

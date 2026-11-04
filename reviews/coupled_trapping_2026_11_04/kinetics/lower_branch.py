"""Instantaneous lowerchargedmass envelope with diagonal scalarparents absorbed.
Diagnostic only: actual conversions are slow compared with firstroll and χ fills.
"""
import sys,os
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,time,resource
import numpy as np
from averaged_v2 import Model,evolve,ROOT,HERE,DEG
class LowerMass:
 def __init__(self,F):self.F=F
 def __call__(self,x,nu=0):
  x=np.asarray(x);S=.003/2*np.sqrt(x*x+2/(31*.003));F=self.F(x)
  if nu==0:return np.minimum(F,S)
  return np.where(F<S,self.F(x,nu),.003*x/(2*np.sqrt(x*x+2/(31*.003))))
class Lower(Model):
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw);self.Fmass=self.mass;self.mass=LowerMass(self.mass);self.Ftable=self.tables;raw=json.loads((HERE/'run_scalar_table_001/result.json').read_text())['cases'];self.Sx=np.array([r['x'] for r in raw]);self.Stable=raw;self.max_local_hierarchy=0
 def kernel(self,x,t):
  F=float(self.Fmass(x));S=.003/2*math.sqrt(x*x+2/(31*.003));m=min(F,S)
  if F<=S:return super().kernel(x,t)
  i=min(max(0,int(np.searchsorted(self.Sx,x)-1)),len(self.Sx)-2);alpha=min(1,max(0,(x-self.Sx[i])/(self.Sx[i+1]-self.Sx[i])));parents=[]
  for row,fac in ((self.Stable[i],1-alpha),(self.Stable[i+1],alpha)):
   for M,W in row['parents']:
    if fac<=0 or M<=2*m:continue
    b0=math.sqrt(max(0,1-4*row['mS']**2/M**2))
    if b0>1e-10:parents.append((M,fac*W/b0))
  if not parents:return np.zeros((len(self.W),len(self.W)))
  # W/beta removes the exact scalarthreshold phase-spacefactor. The retained
  # f represents gF=24; gS=12 gives fS=2f, hence scalarinverse rates multiply4.
  pw=np.array(parents);pm=pw[:,0];coef=pw[:,1];ei=np.sqrt(m*m+(t*self.edges)**2);elo=ei[:-1];ehi=ei[1:];de=ehi-elo;c=(pm*pm-2*m*m)/2;d=np.sqrt(np.maximum(0,c*c-m**4));e1=(elo+ehi)[None,:]/2+self.kz[:,None]*de[None,:]/2;p1=np.sqrt(np.maximum(0,e1*e1-m*m));ce=c[:,None,None]*e1[None,:,:];pd=d[:,None,None]*p1[None,:,:];low=(c[:,None,None]**2+m*m*p1[None,:,:]**2)/(ce+pd);high=(ce+pd)/(m*m);overlap=np.maximum(0,np.minimum(high[:,:,:,None],ehi[None,None,None,:])-np.maximum(low[:,:,:,None],elo[None,None,None,:]));aa=np.einsum('kqij,q,i->kij',overlap,self.kw,de/2,optimize=True);aa=(aa+aa.transpose(0,2,1))/2
  return np.einsum('k,kij->ij',8*coef*pm/DEG,aa,optimize=True)
def main(out,kind):
 start=time.monotonic();stat=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text());spins=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text());p=next(z for z in stat['points'] if z['kind']==kind);s=next(z for z in spins['points'] if z['kind']==kind)['spins'][0];model=Lower(p,s,bins=32,orbitn=16);run=evolve(model,True,math.log(s['TD_over_mu']/.0005),.0008);run.update(kind=kind,mu_GeV=p['mu_GeV'])
 result=dict(claim_id='CT09_LOWER_CHARGED_BRANCH_DIAGNOSTIC',case=run,checks={'reached_cooling':run['reason']=='target cooling reached','energy_ledger':bool(max(abs(z['energy_ledger_error']) for z in run['history'])<.02),'averaging_numberrate':bool(run['max_rate_over_oscillation']<.1)},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Artificial instantaneousmin(mF,mS) chargedcarrierenergy envelope. Initial24fermiondegrees retainedasnumbermeasure; scalarfS=2f aftercrossing, so scalarpair inverse ratefactor4. Exactactuallightscalarpairwidths, narrowdiagonalparentabsorption, thresholdΓ/beta interpolation. No returningcharged/neutraldaughterforce, finiteconversiondistribution, χemission/Pauli/inversereactions or parentdegeneracyinterference. No completephysicalhistory; neitherbranch norannihilationfinalstate isguaranteed bythisdiagnostic.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));print(kind,run['reason'],run['history'][-1]);assert all(result['checks'].values())
if __name__=='__main__':main(*sys.argv[1:])

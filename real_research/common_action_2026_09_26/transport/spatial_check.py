#!/usr/bin/env python3
"""Bounded 1D field-transport control, fixed Z=0; no gravity/gate/cosmological fit."""
import argparse,json,math
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
checks={};rows=[]
def yes(name,p):
 assert bool(p),name;checks[name]=True

def run(N,g2,seed):
 L=128.;dx=L/N;x=(np.arange(N)+.5)*dx-L/2;dt=12.8/N;steps=round(30/dt);dt=30/steps
 shape=np.exp(-(x/12)**8);R=.1+.9*shape
 q=np.array([R,np.zeros(N),seed*shape]);p=np.array([np.zeros(N),math.sqrt(3)*R,np.zeros(N)])
 mask=abs(x)<10
 def force(q):
  r2=q[0]**2+q[1]**2;s=q[2]
  grad=np.array([(1+2*r2-g2*s*s)*q[0],(1+2*r2-g2*s*s)*q[1],(.5+2*s*s-g2*r2)*s])
  return (np.roll(q,1,axis=1)+np.roll(q,-1,axis=1)-2*q)/(dx*dx)-grad
 def energy(q,p):
  r2=q[0]**2+q[1]**2;s=q[2]
  V=.5*r2+.5*r2*r2+.25*s*s+.5*s**4-.5*g2*r2*s*s
  return dx*np.sum(.5*np.sum(p*p,axis=0)+.5*np.sum((np.roll(q,-1,axis=1)-q)**2,axis=0)/(dx*dx)+V)
 def charge(q,p):return q[0]*p[1]-q[1]*p[0]
 def region_rate(q):
  # qdotcharge_i = (I_right-I_left)/dx, J=-I; exact semidiscrete boundary flux.
  I=(q[0]*np.roll(q[1],-1)-q[1]*np.roll(q[0],-1))/dx
  return np.sum((I-np.roll(I,1))[mask])
 E0=energy(q,p);Q0=dx*np.sum(charge(q,p));Qr0=dx*np.sum(charge(q,p)[mask]);ledger=0.;maxE=maxQ=maxledger=0.;maxs=seed
 samples=[]
 for j in range(steps):
  ledger+=dt*region_rate(q)/2
  p+=dt*force(q)/2;q+=dt*p;p+=dt*force(q)/2
  ledger+=dt*region_rate(q)/2
  if j%max(1,steps//300)==0 or j==steps-1:
   e=energy(q,p);cq=charge(q,p);Qr=dx*sum(cq[mask]);maxE=max(maxE,abs(e/E0-1));maxQ=max(maxQ,abs(dx*sum(cq)/Q0-1));maxledger=max(maxledger,abs(Qr-Qr0-ledger)/Qr0);maxs=max(maxs,float(max(abs(q[2]))))
   samples.append([float((j+1)*dt),float(Qr/Qr0)])
 return dict(N=N,g2=g2,seed=seed,steps=steps,dt=dt,region_charge_retention=float(dx*sum(charge(q,p)[mask])/Qr0),outward_charge_fraction=float(-ledger/Qr0),max_energy_relative_error=float(maxE),max_charge_relative_error=float(maxQ),max_region_flux_ledger_error=float(maxledger),max_abs_s=maxs,samples=samples)
for N in [256,512,1024]:
 for g,seed in [(0,.001),(1,.001)]:
  r=run(N,g,seed);rows.append(r);tag=f'N{N}_g{g}'
  yes(tag+' charge conserved',r['max_charge_relative_error']<1e-11)
  yes(tag+' local charge flux accounts for retention',r['max_region_flux_ledger_error']<1e-11)
  yes(tag+' energy bounded integration error',r['max_energy_relative_error']<1e-3)
for g,seed in [(0,0),(1,0),(1,.01)]:rows.append(run(512,g,seed))
control0=[r for r in rows if r['N']==512 and r['g2']==0 and r['seed']==0][0]
control1=[r for r in rows if r['N']==512 and r['g2']==1 and r['seed']==0][0]
yes('zero seed nonlinear flow equals no coupling',control0['region_charge_retention']==control1['region_charge_retention'])
yes('zero seed remains invariant',control1['max_abs_s']==0)
conv={}
for g in [0,1]:
 rr=[r for r in rows if r['g2']==g and r['seed']==.001]
 changes=[abs(rr[1]['region_charge_retention']-rr[0]['region_charge_retention']),abs(rr[2]['region_charge_retention']-rr[1]['region_charge_retention'])]
 conv[str(g)]={'retention_grid_differences':changes,'difference_ratio':changes[0]/changes[1]}
 yes('refinement reduces retention error g'+str(g),changes[1]<changes[0])
fin={g:next(r for r in rows if r['N']==1024 and r['g2']==g)for g in [0,1]}
delta=fin[1]['region_charge_retention']-fin[0]['region_charge_retention']
# Direction is a measured outcome, not a preordained required pass.
out={'result':'bounded spatial field transport control completed','checks':checks,'check_count':len(checks),'rows':rows,'convergence':conv,'transition_minus_no_coupling_retention':delta,'interpretation':'transition retains more charge in this fixed region' if delta>0 else 'transition loses more charge in this fixed region','non_claims':['No full evolving auxiliary gate or selfgravity','No cold/cosmological halo fit','One-dimensional finite time and finite grid','No derived random kick law']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');brief={k:v for k,v in out.items()if k!='rows'};brief['rows']=[{k:v for k,v in r.items()if k!='samples'}for r in rows];print(json.dumps(brief,indent=2))

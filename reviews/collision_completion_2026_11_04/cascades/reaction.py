"""Actual CC10 25-group 1<->2 event operator and massive occupation forces.

Uses the statistics package's energy-linear, entropy-variable projection.
No terminal-state/radiation replacement occurs here.
"""
import sys,math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from network import signed_lift
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'statistics'))
from quantum import ReactionEvents

def full_events(data,t,q,W,angles=4,signed=False,source=None):
 groups,channels=signed_lift(data) if signed else ([dict(z) for z in data['groups']],[dict(z) for z in data['channels']])
 by={g['id']:i for i,g in enumerate(groups)};n=len(q);ns=len(groups)
 # Replace, rather than add, the current-projected F/C/gaugino conversions.
 # Other FFS/SSS channels retain the rigid tree approximation.
 replacements={}
 if source is not None:
  if signed:raise ValueError('current replacement presently for charge-symmetric groups only')
  for name,gid in (('U1','F1_1'),('SU2','F3_0'),('SU3','F8_0')):
   groups[by[gid]]['mass']=source['gauginos_over_mu'][name]
   replacements[('Fc_0','Sc_0',gid)]=source['widths_over_mu'][name]
   replacements[('Sc_0','Fc_0',gid)]=source['reverse_lightest_scalar_widths_over_mu'][name]
  filtered=[]
  for c in channels:
   key=tuple([c['parent']]+sorted(c['daughters']))
   if any(c['parent']==p and sorted(c['daughters'])==sorted([d,g]) for p,d,g in replacements):continue
   filtered.append(c)
  for (p,d,g),w in replacements.items():
   if w>0:filtered.append(dict(parent=p,daughters=[d,g],width=w,kind='FS',carrier_delta=0))
  channels=filtered
 masses=np.array([g['mass'] for g in groups]);energies=np.sqrt(masses[:,None]**2+(t*np.asarray(q)[None,:])**2)
 deg=np.array([g['degeneracy'] for g in groups]);measure=(deg[:,None]*W[None,:]/(2*math.pi**2)).ravel();eta=np.repeat([1. if g['kind']=='S' else -1. for g in groups],n)
 az,aw=leggauss(angles);indices=[];weights=[];coefs=[];labels=[];omitted=np.zeros(ns*n);included=np.zeros(ns*n)
 def split(E,target):
  lo=np.clip(np.searchsorted(E,target)-1,0,n-2);hi=lo+1
  alpha=np.clip((target-E[lo])/(E[hi]-E[lo]),0,1)
  valid=(target>=E[0]-2e-13)&(target<=E[-1]+2e-13)
  return lo,hi,1-alpha,alpha,valid
 for ci,c in enumerate(channels):
  a=by[c['parent']];j,k=[by[d] for d in c['daughters']];M,m1,m2=masses[[a,j,k]]
  if c['width']<=0 or M<=m1+m2+1e-14:continue
  e1=(M*M+m1*m1-m2*m2)/(2*M);star=math.sqrt(max(0,(M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2)))/(2*M)
  ep=energies[a];p=t*q
  for z,w in zip(az,aw):
   target1=(ep*e1+p*star*z)/M;target2=ep-target1
   b=split(energies[j],target1);d=split(energies[k],target2);valid=b[4]&d[4]
   coeff=measure[a*n:(a+1)*n]*c['width']*M/ep*w/2
   omitted[a*n:(a+1)*n]+=coeff*(~valid);included[a*n:(a+1)*n]+=coeff*valid
   idx=np.stack([a*n+np.arange(n),j*n+b[0],j*n+b[1],k*n+d[0],k*n+d[1]],axis=1)
   wt=np.stack([np.ones(n),b[2],b[3],d[2],d[3]],axis=1)
   indices.append(idx[valid]);weights.append(wt[valid]);coefs.append(coeff[valid]);labels.extend([(a,j,k,ci)]*int(sum(valid)))
 arr=np.concatenate(indices) if indices else np.empty((0,5),int);wei=np.concatenate(weights) if weights else np.empty((0,5));coef=np.concatenate(coefs) if coefs else np.empty(0)
 out=ReactionEvents(arr,wei,coef,measure,energies.ravel(),eta,labels);out.groups=groups;out.by=by;out.channels=channels;out.masses=masses;out.energies=energies;out.q=np.asarray(q);out.W=np.asarray(W);out.t=t;out.x=data['x'];out.omitted_by_parent=omitted;out.included_by_parent=included
 return out

def moments(events,f):
 n=len(events.q);ns=len(events.groups);f=np.asarray(f).reshape(ns,n);w=events.measure.reshape(ns,n)*events.t**3;en=events.energies
 number=np.sum(w*f,axis=1);energy=np.sum(w*f*en,axis=1);pressure=np.sum(w*f*(events.t*events.q[None,:])**2/(3*np.maximum(en,1e-300)),axis=1)
 slopes=np.array([g.get('dm2_dx',0.) for g in events.groups]);force=np.sum(w*f*slopes[:,None]/(2*np.maximum(en,1e-300)),axis=1)
 charged=np.array([g['charged'] for g in events.groups]);sign=np.array([g.get('charge',0.) for g in events.groups])
 return dict(number=number,energy=energy,pressure=pressure,force=force,charged_number=float(number@charged),signed_charge=float(number@sign),neutral_force=float(force@(~charged)),charged_force=float(force@charged),neutral_massive_energy=float(energy@((~charged)&(events.masses>1e-12))),total_energy=float(energy.sum()),total_pressure=float(pressure.sum()),omitted_weighted_rate=float(events.omitted_by_parent@f.ravel()),included_weighted_rate=float(events.included_by_parent@f.ravel()))

def thermal(events,T,charge_chemical=0.):
 n=len(events.q);mu=np.repeat([charge_chemical*g.get('charge',0.) for g in events.groups],n)
 return 1/(np.exp(np.clip((events.energy-mu)/T,-700,700))-events.eta)

def serial_moments(events,f):
 m=moments(events,f);m={k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in m.items()};m['species']=[g['id'] for g in events.groups];return m

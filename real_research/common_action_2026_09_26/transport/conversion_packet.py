#!/usr/bin/env python3
"""Full nonlinear classical conversion packet; all pump and radiation energy evolved."""
import argparse,json,math
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
checks={}
def yes(n,p):assert bool(p),n;checks[n]=True

def run(N,gamma):
 M=3.;m=1.;mu=.5;A=1.;gref=.2
 L=256.;dx=L/N;dt=.1*dx;steps=round(100/dt);dt=100/steps;x=(np.arange(N)+.5)*dx-L/2;mask=abs(x)<20
 # Use the same seed initial data for both couplings, based on the coupled linear resonance.
 ue2=mu*mu+2*gref*gref*m*m*A*A;k=math.sqrt(((M*M-m*m-ue2)**2-4*m*m*ue2)/(4*M*M));wc=math.sqrt(m*m+k*k);ws=math.sqrt(ue2+k*k)
 C=.001*np.exp(-(x/8)**2);D=-1j*math.sqrt(wc/ws)*C
 P=np.full(N,A,dtype=complex);X=C*np.exp(1j*k*x);s=2*np.real(D*np.exp(-1j*k*x))
 pP=-1j*M*P;pX=-1j*wc*X;ps=2*np.real(-1j*ws*D*np.exp(-1j*k*x))
 def lap(q):return (np.roll(q,1)+np.roll(q,-1)-2*q)/dx**2
 def forces(P,X,s):
  Y=X+gamma*s*P
  return lap(P)-M*M*P-gamma*m*m*s*Y,lap(X)-m*m*Y,lap(s)-mu*mu*s-2*gamma*m*m*np.real(P.conj()*Y)
 def energy(P,X,s,pP,pX,ps):
  kin=abs(pP)**2+abs(pX)**2+ps*ps/2
  grad=(abs(np.roll(P,-1)-P)**2+abs(np.roll(X,-1)-X)**2+(np.roll(s,-1)-s)**2/2)/dx**2
  V=M*M*abs(P)**2+m*m*abs(X+gamma*s*P)**2+mu*mu*s*s/2
  return float(dx*sum(kin+grad+V))
 def charge(P,p):return -2*np.imag(P.conj()*p)
 def flux(q):
  J=2*np.imag(q.conj()*np.roll(q,-1))/dx
  return float(sum((J-np.roll(J,1))[mask]))
 def conv(P,X,s):return float(-2*gamma*m*m*dx*sum((s*np.imag(P.conj()*X))[mask]))
 E0=energy(P,X,s,pP,pX,ps);Qp0=dx*sum(charge(P,pP));Qx0=dx*sum(charge(X,pX));Q0=Qp0+Qx0;Qr0=dx*sum((charge(P,pP)+charge(X,pX))[mask]);Qxr0=dx*sum(charge(X,pX)[mask]);fluxTot=fluxX=sourceX=0.;maxE=maxQ=maxLocal=maxXlocal=0.;maxX=0.
 samples=[]
 for j in range(steps):
  fluxTot+=dt*(flux(P)+flux(X))/2;fluxX+=dt*flux(X)/2;sourceX+=dt*conv(P,X,s)/2
  fP,fX,fs=forces(P,X,s);pP+=dt*fP/2;pX+=dt*fX/2;ps+=dt*fs/2
  P+=dt*pP;X+=dt*pX;s+=dt*ps
  fP,fX,fs=forces(P,X,s);pP+=dt*fP/2;pX+=dt*fX/2;ps+=dt*fs/2
  fluxTot+=dt*(flux(P)+flux(X))/2;fluxX+=dt*flux(X)/2;sourceX+=dt*conv(P,X,s)/2
  if j%max(1,steps//200)==0 or j==steps-1:
   Qp=dx*sum(charge(P,pP));Qx=dx*sum(charge(X,pX));Qr=dx*sum((charge(P,pP)+charge(X,pX))[mask]);Qxr=dx*sum(charge(X,pX)[mask]);maxE=max(maxE,abs(energy(P,X,s,pP,pX,ps)/E0-1));maxQ=max(maxQ,abs((Qp+Qx)/Q0-1));maxLocal=max(maxLocal,abs(Qr-Qr0+fluxTot)/Qr0);maxXlocal=max(maxXlocal,abs(Qxr-Qxr0+fluxX-sourceX)/Qr0);maxX=max(maxX,float(max(abs(X))))
   samples.append([float((j+1)*dt),float(Qr/Qr0),float(Qx),float(Qxr),float(sourceX),float(fluxX)])
 return {'N':N,'gamma':gamma,'initial_energy':E0,'initial_total_charge':float(Q0),'initial_chi_charge':float(Qx0),'final_chi_charge':float(Qx),'final_pump_charge_loss':float(Qp0-Qp),'region_total_retention':float(Qr/Qr0),'region_chi_charge':float(Qxr),'outward_total_charge_fraction':float(fluxTot/Qr0),'outward_chi_charge':float(fluxX),'region_chi_conversion_source':float(sourceX),'max_energy_relative_error':float(maxE),'max_charge_relative_error':float(maxQ),'max_local_flux_error':float(maxLocal),'max_local_conversion_ledger_error':float(maxXlocal),'max_abs_chi':maxX,'steps':steps,'dt':dt,'k_seed':k,'samples':samples}
rows=[]
for N,gamma in [(1024,0),(1024,.2),(2048,.2)]:
 r=run(N,gamma);rows.append(r);tag=f'N{N}gamma{gamma}'
 yes(tag+' total charge conserved',r['max_charge_relative_error']<1e-10)
 yes(tag+' total local flux closes',r['max_local_flux_error']<1e-10)
 yes(tag+' separate conversion flux closes',r['max_local_conversion_ledger_error']<1e-10)
 yes(tag+' bounded energy integration error',r['max_energy_relative_error']<1e-3)
yes('no coupling no charge conversion',abs(rows[0]['final_chi_charge']/rows[0]['initial_chi_charge']-1)<1e-10)
yes('full evolution converts pump charge',rows[2]['final_chi_charge']>100*rows[2]['initial_chi_charge'])
yes('full evolution exports converted charge',rows[2]['outward_chi_charge']>0)
yes('refinement bounded charge conversion change',abs(rows[1]['final_chi_charge']/rows[2]['final_chi_charge']-1)<.1)
out={'result':'full nonlinear conservative classical conversion packet completed','checks':checks,'check_count':len(checks),'rows':rows,'comparison':'fixed Z0, no gravity; uniform pump with localized paired seeds; initial gradients are included in Hamiltonian','non_claims':['No cosmological halo clearing','No geometric trigger derived','Fast dimensionless packet differs from slow-wave Floquet witness','No global timelike phase inferred','Finite periodic box before central wraparound, not full outgoing boundary theorem']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({**out,'rows':[{k:v for k,v in r.items()if k!='samples'}for r in rows]},indent=2))

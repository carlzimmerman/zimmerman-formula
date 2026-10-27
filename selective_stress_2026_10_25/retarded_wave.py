"""Autonomous conversion coupled to spherical outgoing scalar waves.

Positive energy, reciprocal derivative coupling, mass fraction periodic in q.
Discrete-gradient q and midpoint wave integration conserve H+escape.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.linalg.lapack import dgttrf,dgttrs

def run(g=500.,h=.05,dt=.04,duration=2000.,domain=12000.,c=500.,sample_every=20):
 edges=np.r_[np.arange(0,2+.1*h,h),np.geomspace(2,domain,401)[1:]];n=len(edges)-1;r=(edges[:-1]+edges[1:])/2;vol=np.diff(edges**3)/3;rf=edges[1:-1];w=rf**2/np.diff(r)
 off=w;diag=np.r_[w[0],w[:-1]+w[1:],w[-1]]
 def lap(x):
  z=-diag*x;z[:-1]+=off*x[1:];z[1:]+=off*x[:-1];return z/vol
 # A smooth normalized source confined to the converted object r<1.
 source=np.maximum(1-r*r,0)**2;source/=vol@source
 gamma=.8*np.maximum((r-12*c)/(domain-12*c),0)**2
 A_diag=1+dt**2*c*c/4*diag/vol+dt*gamma/2
 A_lower=-dt**2*c*c/4*off/vol[1:];A_upper=-dt**2*c*c/4*off/vol[:-1]
 lu=dgttrf(A_lower.copy(),A_diag.copy(),A_upper.copy());assert lu[-1]==0
 def inv(z):
  out,info=dgttrs(*lu[:-1],np.asfortranarray(z[:,None]));assert info==0;return out[:,0]
 ah=inv(source);Hah=float(vol@(source*ah));q=1e-4;P=0.;chi=np.zeros(n);v=np.zeros(n);Q=0.;charge_sink=0.;I=1.;D=.25
 def fraction(q):return np.sin(np.pi*q/2)**2
 def energy(q,P,chi,v):return P*P/(2*I)+D*(1-fraction(q))+.5*(vol@(v*v)+c*c*(w@np.diff(chi)**2))
 E0=energy(q,P,chi,v);C0=g*fraction(q);maxerr=0.;maxcharge=0.;maxdrive=0.;trace=[]
 for j in range(int(round(duration/dt))):
  base=inv(v+dt*c*c/2*lap(chi));Hb=float(vol@(source*base));old=q;N0=fraction(q);q1=q+dt*P/I
  def eq(q1):
   d=q1-old;DN=np.pi/2*np.sin(np.pi*(q1+old)/2)*np.sinc(d/2);dN=DN*d
   return 2*I*d/dt**2-2*P/dt+DN*(-D-g*Hb+g*g/2*Hah*dN)
  for k in range(12):
   z=eq(q1)
   if abs(z)<1e-11:break
   eps=1e-6;der=(eq(q1+eps)-eq(q1-eps))/(2*eps);q1-=z/der
  assert abs(eq(q1))<1e-8
  dN=fraction(q1)-N0;vmid=base-g/2*ah*dN
  chi=chi+dt*vmid;v=2*vmid-v;P=2*I*(q1-old)/dt-P;q=q1
  Q+=dt*(vol@(gamma*vmid*vmid));charge_sink+=dt*(vol@(gamma*vmid))
  E=energy(q,P,chi,v);maxerr=max(maxerr,abs((E+Q)/E0-1));maxcharge=max(maxcharge,abs(vol@v+g*fraction(q)+charge_sink-C0)/max(1,g))
  maxdrive=max(maxdrive,float(max(abs(g*vmid[r>1.2]))/D))
  if j%sample_every==0:trace.append([dt*(j+1),Q/E0,fraction(q),(P*P/(2*I)+D*(1-fraction(q)))/E0])
 out={'coupling':g,'c':c,'spacing':h,'dt':dt,'duration':duration,'domain':domain,'source_radius':1.,'inverse_bare_conversion_frequency':1/np.sqrt(D*np.pi*np.pi/2),'radiated_fraction':float(Q/E0),'remaining_total_energy_fraction':float(E/E0),'final_converted_fraction':float(fraction(q)),'energy_ledger_relative_error':float(maxerr),'shift_charge_ledger_error':float(maxcharge),'maximum_exterior_chemical_drive_over_conversion_energy_per_fraction':float(maxdrive),'initial_angular_energy':0.,'initial_conversion_potential_fraction':1.,'trace':trace}
 assert maxerr<1e-6 and maxcharge<1e-7
 return out

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[],'non_claims':['One autonomous conversion coordinate with fixed spherical source profile, not mobile galactic density or moving boundary','Phenomenological derivative coupling and subluminal scalar speed, not a microscopic derivation','Sponge escape is checked by energy and charge ledgers; it approximates outgoing transport']}
 for g in [500.]:
  r=run(g=g);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k!='trace'},flush=True)

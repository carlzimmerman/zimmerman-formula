"""Autonomous conversion coupled to spherical outgoing scalar waves.

Positive energy, reciprocal derivative coupling, mass fraction periodic in q.
Discrete-gradient q and midpoint wave integration conserve H+escape.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.linalg.lapack import dgttrf,dgttrs

def run(g=3.,h=.025,dt=.01,duration=500.,domain=24.,c=1.,sample_every=20,Ival=8.8843050915094,gap=12.5,exact=False):
 n=int(round(domain/h));edges=np.linspace(0,domain,n+1);r=(edges[:-1]+edges[1:])/2;vol=np.diff(edges**3)/3;rf=(r[:-1]+r[1:])/2;w=rf**2/h
 off=w;diag=np.r_[w[0],w[:-1]+w[1:],w[-1]]
 def lap(x):
  z=-diag*x;z[:-1]+=off*x[1:];z[1:]+=off*x[:-1];return z/vol
 # Conservatively sampled measured halo T profile, confined to r<1.
 halo=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());rr=np.array(halo['r'])/halo['scaled_boundary_kpc'];oldedges=[0.]
 for ri in rr:oldedges.append(2*ri-oldedges[-1])
 cum=np.r_[0,np.cumsum(np.array(halo['mass'])*halo['q'])];source_mass=np.diff(np.interp(np.minimum(edges,1.)**3,np.array(oldedges)**3,cum));source=source_mass/vol;source/=vol@source
 gamma=.8*np.maximum((r-12)/(domain-12),0)**2
 A_diag=1+dt**2*c*c/4*diag/vol+dt*gamma/2
 A_lower=-dt**2*c*c/4*off/vol[1:];A_upper=-dt**2*c*c/4*off/vol[:-1]
 lu=dgttrf(A_lower.copy(),A_diag.copy(),A_upper.copy());assert lu[-1]==0
 def inv(z):
  out,info=dgttrs(*lu[:-1],np.asfortranarray(z[:,None]));assert info==0;return out[:,0]
 ah=inv(source);Hah=float(vol@(source*ah));q=1e-4;P=0.;chi=np.zeros(n);v=np.zeros(n);Q=0.;charge_sink=0.;I=Ival;D=.25;Pmax=np.sqrt(I*gap)
 def Tkin(P):
  if not exact:return P*P/(2*I)
  z=(P/Pmax)**2;assert z<1;return gap*z/(1+np.sqrt(1-z))
 def fraction(q):return np.sin(np.pi*q/2)**2
 def energy(q,P,chi,v):return Tkin(P)+D*(1-fraction(q))+.5*(vol@(v*v)+c*c*(w@np.diff(chi)**2))
 E0=energy(q,P,chi,v);C0=g*fraction(q);maxerr=0.;maxcharge=0.;maxdrive=0.;trace=[];probes=np.array([1.2,2.,4.,8.]);probe_ids=np.array([np.argmin(abs(r-x)) for x in probes]);pulse=[]
 for j in range(int(round(duration/dt))):
  base=inv(v+dt*c*c/2*lap(chi));Hb=float(vol@(source*base));old=q;N0=fraction(q);q1=q+dt*P/I
  def kick(q1):
   d=q1-old;DN=np.pi/2*np.sin(np.pi*(q1+old)/2)*np.sinc(d/2);dN=DN*d
   return P+dt*DN*(D+g*Hb-g*g/2*Hah*dN)
  def eq(q1):
   P1=kick(q1);den=(np.sqrt(1-(P/Pmax)**2)+np.sqrt(1-(P1/Pmax)**2)) if exact else 2.
   return (q1-old)/dt-(P+P1)/(I*den)
  for k in range(12):
   z=eq(q1)
   if abs(z)<1e-11:break
   eps=1e-6;der=(eq(q1+eps)-eq(q1-eps))/(2*eps);q1-=z/der
  assert abs(eq(q1))<1e-8
  dN=fraction(q1)-N0;vmid=base-g/2*ah*dN
  Pnew=kick(q1);chi=chi+dt*vmid;v=2*vmid-v;P=Pnew;q=q1
  Q+=dt*(vol@(gamma*vmid*vmid));charge_sink+=dt*(vol@(gamma*vmid))
  E=energy(q,P,chi,v);maxerr=max(maxerr,abs((E+Q)/E0-1));maxcharge=max(maxcharge,abs(vol@v+g*fraction(q)+charge_sink-C0)/max(1,g))
  maxdrive=max(maxdrive,float(max(abs(g*vmid[r>1.2]))/D))
  if j%sample_every==0:
   trace.append([dt*(j+1),Q/E0,fraction(q),(Tkin(P)+D*(1-fraction(q)))/E0]);pulse.append([dt*(j+.5),*(g*vmid[probe_ids]).tolist()])
 out={'coupling':g,'derived_material_inertia':I,'exact_gapped_state_kinetic':exact,'alignment_half_gap':gap,'c':c,'spacing':h,'dt':dt,'duration':duration,'domain':domain,'source_radius':1.,'inverse_bare_conversion_frequency':np.sqrt(I/(D*np.pi*np.pi/2)),'radiated_fraction':float(Q/E0),'remaining_total_energy_fraction':float(E/E0),'final_converted_fraction':float(fraction(q)),'energy_ledger_relative_error':float(maxerr),'shift_charge_ledger_error':float(maxcharge),'maximum_exterior_chemical_drive_over_conversion_energy_per_fraction':float(maxdrive),'initial_angular_energy':0.,'initial_conversion_potential_fraction':1.,'trace':trace,'pulse':pulse,'probe_r_over_R':r[probe_ids].tolist()}
 assert maxerr<1e-6 and maxcharge<1e-7
 return out

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[],'non_claims':['Scalar propagation now c; conversion inertia from the stated gapped internal-state completion. Source follows the measured benchmark T mass profile, but its density and boundary remain fixed; V is a reduced conversion potential','Phenomenological derivative coupling and canonical alignment-dominated inertia; no microscopic derivation','Sponge escape is checked by energy and charge ledgers; it approximates outgoing transport']}
 inertia=json.loads(Path('selective_stress_2026_10_25/run_spinor_inertia/results.json').read_text());cases=inertia['cases'];Db=cases[0]['conversion_potential_Eunit']
 for case,h,dt,exact in [(cases[0],.025,.01,False),(cases[0],.025,.01,True),(cases[1],.025,.01,False),(cases[1],.025,.01,True),(cases[0],.0125,.005,True)]:
  Dreal=case['conversion_potential_Eunit'];g=3*np.sqrt(Db/Dreal);I=case['prototype_material_inertia_at_D_point25'];gap=inertia['converted_mass_Mb']*inertia['alignment_J']/(2*(Dreal/.25))
  r=run(g=g,h=h,dt=dt,sample_every=1,Ival=I,gap=gap,exact=exact);z=np.array(r['trace']);ids=np.where(z[:,1]>=.977191)[0];r['first_sampled_heat_threshold_time']=float(z[ids[0],0]) if len(ids) else None;r['case']=case['case'];r['physical_time_unit_Myr']=case['R_over_c_Myr'];r['threshold_time_Myr']=r['first_sampled_heat_threshold_time']*r['physical_time_unit_Myr'] if len(ids) else None;r['potential_Eunit']=Dreal
  # Keep full pulse for the whole-release exact case for a separate response audit.
  if not (exact and case['case']=='whole_release_hypothesis'):r.pop('pulse')
  out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['trace','pulse']},flush=True)

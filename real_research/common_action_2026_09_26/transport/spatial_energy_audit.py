#!/usr/bin/env python3
"""Independent complex-coordinate integrator and initial-energy ledger."""
import argparse,json,math
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
here=Path(__file__).resolve().parent
prior=json.loads((here/'run_spatial_001/results.json').read_text())
checks={}
def yes(n,p):assert bool(p),n;checks[n]=True

def evolve(N,g2,dt,seed=.001):
 dx=128/N;x=(np.arange(N)+.5)*dx-64;f=np.exp(-(x/12)**8);z=(.1+.9*f).astype(complex);s=seed*f;p=1j*math.sqrt(3)*z;ps=np.zeros(N);mask=abs(x)<10
 steps=round(30/dt);dt=30/steps
 def forces(z,s):
  return ((np.roll(z,1)+np.roll(z,-1)-2*z)/dx**2-(1+2*abs(z)**2-g2*s*s)*z,
          (np.roll(s,1)+np.roll(s,-1)-2*s)/dx**2-(.5+2*s*s-g2*abs(z)**2)*s)
 def ledger(z,s,p,ps):
  r2=abs(z)**2
  return {'kinetic_phi':float(dx*sum(abs(p)**2)/2),'kinetic_s':float(dx*sum(ps*ps)/2),
          'gradient_phi':float(sum(abs(np.roll(z,-1)-z)**2)/(2*dx)),'gradient_s':float(sum((np.roll(s,-1)-s)**2)/(2*dx)),
          'bare_phi_potential':float(dx*sum(.5*r2+.5*r2*r2)),
          'bare_s_potential':float(dx*sum(.25*s*s+.5*s**4)),
          'interaction':float(-.5*g2*dx*sum(r2*s*s))}
 initial_energy=ledger(z,s,p,ps);q0=float(dx*sum(np.imag(z.conj()*p)));qr0=float(dx*sum(np.imag(z.conj()*p)[mask]))
 for j in range(steps):
  fz,fs=forces(z,s);p+=dt*fz/2;ps+=dt*fs/2;z+=dt*p;s+=dt*ps;fz,fs=forces(z,s);p+=dt*fz/2;ps+=dt*fs/2
 q=float(dx*sum(np.imag(z.conj()*p)));qr=float(dx*sum(np.imag(z.conj()*p)[mask]));final_energy=ledger(z,s,p,ps)
 return {'N':N,'g2':g2,'dt':dt,'initial_energy_terms':initial_energy,'initial_total_energy':sum(initial_energy.values()),'initial_charge':q0,'initial_region_charge':qr0,'retention':qr/qr0,'relative_charge_error':abs(q/q0-1),'final_energy_relative_error':abs(sum(final_energy.values())/sum(initial_energy.values())-1)}
rows=[]
for g in [0,1]:
 for dt in [.025,.0125]:
  r=evolve(512,g,dt);rows.append(r);yes(f'complex coordinate charge g{g}dt{dt}',r['relative_charge_error']<1e-11)
 old=next(r for r in prior['rows']if r['N']==512 and r['g2']==g and r['seed']==.001)
 yes('independent real versus complex integration g'+str(g),abs(rows[-2]['retention']-old['region_charge_retention'])<1e-11)
 yes('time refinement bound g'+str(g),abs(rows[-1]['retention']-rows[-2]['retention'])<1e-3)
g0=rows[1];g1=rows[3]
yes('initial charge matches exactly',g0['initial_charge']==g1['initial_charge'])
yes('initial energy difference accounted',abs((g1['initial_total_energy']-g0['initial_total_energy'])-g1['initial_energy_terms']['interaction'])<1e-12)
yes('refined time still greater retention with transition',g1['retention']>g0['retention'])
out={'result':'initial energy ledger and independent timestep audit accepted','checks':checks,'check_count':len(checks),'rows':rows,'refined_transition_minus_control_retention':g1['retention']-g0['retention'],'non_claims':['Initial gradients and seed energy are paid initial data','The compared Hamiltonians differ by explicit interaction energy','No selfgravity, dynamical gate or cosmological fit']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

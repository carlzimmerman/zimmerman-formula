"""Linear carrier response to an outgoing massless phase packet on actual outer halo."""
import argparse,json
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);base=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());units=json.loads(Path('physical_completion_2026_10_25/run_units/results.json').read_text());form=json.loads(Path('physical_completion_2026_10_25/run_free_finish/results.json').read_text());kpc=3.085677581491367e19;c=299792458.;B=.001;ellv=.01;ell=3*np.sqrt(.5);decay=ellv/(np.pi*np.sqrt(B/2));Rphys=1.2*base['scaled_boundary_kpc'];R0=Rphys/decay;R1=3*R0;Etot=form['released_energy_Eunit']*units['Eunit_J'];duration=1e8*31557600;eta=Etot/(4*np.pi*(Rphys*kpc)**2*c*duration*units['phase_volume_energy_J_per_m3']);k=.5;A=2*R0*np.sqrt(eta)/(np.pi*k);width=20.;center0=R0-100;mass=np.array(base['mass']);q=np.array(base['q']);MT=float(mass@q);rad0=np.array(base['r']);ed=[0.]
for rr in rad0:ed.append(2*rr-ed[-1])
rho0=mass/(np.diff(np.array(ed)**3)/3)*units['rM_kpc']**3
out={'scope':'Linear vacuum-carrier response with matter density and spin frozen during a fast prescribed angular packet; response-weighted gradient and alignment restoring term included. Not coupled galaxy formation or full nonlinear transport. Lorentz time completion Z/c^2 is an explicit assumption.','radiative_duration_assumption_years':1e8,'mean_wave_energy_over_B_at_entry':eta,'entry_radius_kpc':Rphys,'carrier_vacuum_decay_length_kpc':decay,'runs':[]}
def packet(s):
 env=np.exp(-s*s/(2*width**2));return A*env*np.cos(k*s),A*env*(-s/width**2*np.cos(k*s)-k*np.sin(k*s))
ss=np.linspace(-8*width,8*width,20001);incoming=float(np.trapz(packet(ss)[1]**2,ss))
for requested_dr,dt in [(.125,.025)]:
 N=int(np.ceil((R1-R0)/requested_dr));r=np.linspace(R0,R1,N+1);dr=r[1]-r[0];rp=r*decay;uT=MT/(rp/units['rM_kpc'])**2;F=uT*uT/(1-uT);rho=np.interp(rp,rad0,rho0,left=rho0[0],right=0);Z=1+(ell/ellv)**2*F;Med=(2*4*.95*F+np.pi**2/2*(B+30*rho))/(np.pi**2*B/2);V=Med+np.gradient(Z,dr)/r;Ze=(Z[1:]+Z[:-1])/2;gamma=.15*(np.maximum((R0+30-r)/30,0)**2+np.maximum((r-(R1-30))/30,0)**2);u=np.zeros(N+1);v=u.copy();diss=0.;work=0.;maxE=0.;maxu=0.;maxbalance=0.;trace=[]
 def source(t):
  f,fp=packet(t-r+center0);return -2*f*fp/r**2-f*f/r**3
 def force(u,S):
  ans=np.zeros_like(u);ans[1:-1]=((Ze[1:]*(u[2:]-u[1:-1])-Ze[:-1]*(u[1:-1]-u[:-2]))/dr**2-V[1:-1]*u[1:-1]+S[1:-1])/Z[1:-1];return ans
 def energy():return .5*dr*float(np.sum(Z*v*v+V*u*u))+.5/dr*float(np.sum(Ze*np.diff(u)**2))
 steps=int(round(1200/dt));dec=np.exp(-gamma*dt/2)
 for j in range(steps):
  t=j*dt;before=.5*dr*np.sum(Z*v*v);v*=dec;diss+=float(before-.5*dr*np.sum(Z*v*v));S=source(t);dv=.5*dt*force(u,S);work+=float(.5*dt*dr*np.sum(S*(v+.5*dv)));v+=dv;u+=dt*v;u[0]=u[-1]=0;S=source(t+dt);dv=.5*dt*force(u,S);work+=float(.5*dt*dr*np.sum(S*(v+.5*dv)));v+=dv;v[0]=v[-1]=0;before=.5*dr*np.sum(Z*v*v);v*=dec;diss+=float(before-.5*dr*np.sum(Z*v*v));E=energy();maxE=max(maxE,E);maxu=max(maxu,float(max(abs(u/r))));maxbalance=max(maxbalance,abs(E+diss-work))
  if j%100==0:trace.append([t+dt,float(max(abs(u/r))),E,diss,work])
 result=dict(dr=float(dr),dt=dt,maximum_carrier_displacement=maxu,instantaneous_alignment_q_bound=float(np.sin(np.pi*maxu/2)**2),maximum_carrier_energy_over_incoming=maxE/incoming,energy_balance_error_over_incoming=maxbalance/incoming,energy_balance_error_over_max_response=maxbalance/maxE,maximum_Z=float(max(Z)),minimum_carrier_potential=float(min(V)),trace=trace);assert result['energy_balance_error_over_max_response']<.05 and maxu<.01;out['runs'].append(result);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in result.items() if k!='trace'},flush=True)
previous=json.loads(Path('physical_completion_2026_10_25/run_goldstone_pulse/results.json').read_text())['runs'][-1];out['relative_response_change_under_refinement']=abs(out['runs'][0]['maximum_carrier_displacement']/previous['maximum_carrier_displacement']-1);dest.write_text(json.dumps(out,indent=2)+'\n')

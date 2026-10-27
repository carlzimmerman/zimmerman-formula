#!/usr/bin/env python3
"""SI scale calculations, independently checked against radial dynamics."""
import math,json,sys
from pathlib import Path
from scipy.integrate import solve_ivp
G=6.67430e-11;c=299792458.;h=6.62607015e-34;electronvolt=1.602176634e-19
checks=[];rows=[]
for r0 in [.1,1.]:
 for fraction in [.05,.1,.2]:
  x=r0*fraction;t=1.;u=1-fraction
  B=math.acos(math.sqrt(u))+math.sqrt(u*(1-u))
  M=r0**3*B**2/(2*G*t*t)
  sol=solve_ivp(lambda t,y:[y[1],-G*M/y[0]**2],[0,t],[r0,0],rtol=1e-11,atol=1e-13,method='DOP853')
  actual=sol.y[0,-1]
  checks.append(dict(name=f'radial displacement r0={r0} fraction={fraction}',passed=bool(sol.success and abs(actual-(r0-x))<1e-10)))
  rows.append(dict(initial_separation_m=r0,displacement_m=x,time_s=t,source_mass_kg=M,
                   equivalent_added_stored_energy_J=M*c*c,initial_acceleration_m_s2=G*M/r0**2))
m_eV=1e6;u=.02;gap=2*m_eV*u*u/(math.sqrt(1+u*u)+1)
photon=h*c/(550e-9*electronvolt)
r=dict(all_passed=all(a['passed'] for a in checks),checks=checks,radial_cases=rows,
       constants=dict(G=G,c=c,h=h,joules_per_eV=electronvolt),
       carrier_example=dict(m_eV=m_eV,u=u,available_gap_eV=gap,photon_550nm_eV=photon),
       light=dict(stored_energy_J=100,separation_m=.1,acceleration_m_s2=G*100/(c*c*.1**2),
                  intercepted_power_W=100,absorption_force_N=100/c,
                  ideal_reflection_force_N=200/c,
                  free_1g_displacement_1s_absorption_m=.5*100/c/.001),
       scope='Newtonian point-source radial motion and closed-apparatus added-energy benchmark. No gravity amplification, optical spectrum, eye-safety classification, or photon-portal coupling derived.')
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
sys.exit(0 if r['all_passed'] else 1)

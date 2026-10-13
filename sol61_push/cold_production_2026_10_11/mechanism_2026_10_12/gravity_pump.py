"""Phase-averaged Hamiltonian energy transfer from prescribed potential cycles."""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
P=Path(__file__).parent
rows=[];checks=[]
def cycle(f,tdown,tup):
 def freq(t):
  if t<=tdown:
   z=t/tdown;return 1-f*(1-math.cos(math.pi*z))/2,-f*math.pi*math.sin(math.pi*z)/(2*tdown)
  z=(t-tdown)/tup;return 1-f+f*(1-math.cos(math.pi*z))/2,f*math.pi*math.sin(math.pi*z)/(2*tup)
 def rhs(t,y):
  w2,dw2=freq(t);a,b,c,work=y
  return [2*b,c-w2*a,-2*w2*b,.5*dw2*a]
 sol=solve_ivp(rhs,(0,tdown+tup),[1.,0.,1.,0.],method='DOP853',rtol=2e-11,atol=2e-12,max_step=.15)
 a,b,c,work=sol.y[:,-1];energy=(a+c)/2
 return dict(energy_ratio=float(energy),driver_work=float(work),energy_work_error=float(abs(energy-1-work)),covariance_determinant_error=float(abs(a*c-b*b-1)),completed=sol.success)
for f in [.1,.3,.5]:
 fast=cycle(f,.001,200);slow=cycle(f,200,200)
 exact=(1-f/2)/math.sqrt(1-f)
 checks.extend([dict(name=f'work_identity_{f}',passed=fast['energy_work_error']<1e-8 and slow['energy_work_error']<1e-8),dict(name=f'impulse_adiabatic_{f}',passed=abs(fast['energy_ratio']-exact)<2e-4),dict(name=f'adiabatic_control_{f}',passed=abs(slow['energy_ratio']-1)<2e-4),dict(name=f'hamiltonian_area_{f}',passed=max(fast['covariance_determinant_error'],slow['covariance_determinant_error'])<1e-7)])
 rows.append(dict(fractional_frequency_squared_drop=f,rapid_out_slow_return=fast,slow_out_slow_return=slow,impulse_adiabatic_limit=exact,independent_phase_impulse_return_limit=(2-f)**2/(4*(1-f))))
R=dict(rows=rows,checks=checks,all_pass=all(x['passed'] for x in checks),scope='Unit-mass harmonic well, omega0=1, phase-uniform covariance; imposed potential histories with tracked work',non_claims=['No actual gas history generated','No full halo or spatial density prediction','No new a0 derivation','Ensemble heating is phase-averaged; microscopic Hamiltonian evolution remains reversible'])
(P/'gravity_pump_run'/'results.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps(R,indent=2));assert R['all_pass']

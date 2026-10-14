import math,json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
T=10.
def ramp(t):
 if t>=T:return 1.,0.
 z=t/T;return 3*z*z-2*z*z*z,(6*z-6*z*z)/T

def run(C,sigma,err):
 calls=[0]
 def rhs(t,y):
  calls[0]+=1
  if calls[0]>12000:raise RuntimeError("evaluation cap")
  R,Rp=ramp(t);a=complex(*y);Delta=-C*R*R+sigma
  F=Rp+.5*R+1j*sigma*R
  da=-(.5+1j*(Delta+C*(1+err)*abs(a)**2))*a-1j*F
  return [da.real,da.imag]
 def lost(t,y):
  return .1-math.hypot(y[0],y[1]+ramp(t)[0])
 lost.terminal=True;lost.direction=-1
 try:
  sol=solve_ivp(rhs,[0,20],[0,0],events=lost,method='Radau',rtol=2e-9,atol=1e-11,max_step=.1)
 except RuntimeError as exc:
  assert str(exc)=='evaluation cap'
  return dict(C=C,sigma=sigma,coefficient_fractional_error=err,status='inconclusive-evaluation-cap',rhs_calls=calls[0])
 assert sol.success
 targets=np.array([ramp(t)[0] for t in sol.t]);errnorm=np.hypot(sol.y[0],sol.y[1]+targets)
 return dict(status='completed',C=C,sigma=sigma,coefficient_fractional_error=err,final_population=float(sum(sol.y[:,-1]**2)),reached_end=bool(sol.t[-1]>=20),stop_time=float(sol.t[-1]),
  max_amplitude_tracking_error=float(max(errnorm)),rhs_evaluations=sol.nfev)
old=json.loads((Path(__file__).parent/'INPUT_RESONANCE.json').read_text())
Cs=[old['physical'][i]['shift_over_full_linewidth'] for i in [0,1]]
rows=[]
for C in Cs:
 for sigma in [0,.5]:
  for err in [0,1e-6,-1e-6]:
   r=run(C,sigma,err);rows.append(r);print(r,flush=True)
# Analytic target Jacobian and detuning-bias stability.
linear=[]
for row in old['physical']:
 C=row['shift_over_full_linewidth']
 J=np.array([[-.5,.5+2*C],[-.5,-.5]])
 ev=np.linalg.eigvals(J);assert np.allclose(ev.real,-.5)
 linear.append(dict(C=C,target_eigenvalue_real_part=float(ev[0].real),oscillation_frequency_over_width=math.sqrt(.5*(.5+2*C)),
  steady_intensity_over_exact_resonance=math.sqrt(2),
  exact_resonance_max_transient_amplitude_gain_lower_bound=4*C/math.e))
assert all(r['status']=='completed' and r['reached_end'] and r['max_amplitude_tracking_error']<1e-4 for r in rows if r['coefficient_fractional_error']==0 and r['sigma']==.5)
out=dict(rows=rows,linear=linear,ramp_duration_width_units=T,
 scope='Nonlinear single-mode oscillator with prescribed complex optical envelope and frequency; two C values simulated, third only local linear stability. No field propagation, measurement feedback or confinement.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')

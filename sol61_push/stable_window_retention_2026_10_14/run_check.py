import json,sys,subprocess,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
out=Path(sys.argv[1]);base=Path(__file__).parent
for script,name in [('check.py','retention.json'),('source.py','source.json')]:
 subprocess.run([sys.executable,str(base/script),str(out.parent/name)],check=True,capture_output=True,text=True)
r=json.loads((out.parent/'retention.json').read_text());s=json.loads((out.parent/'source.json').read_text());rows=[];checks=[]
for source in s['rows']:
 poles=[x for x in r['rows'] if x['candidate']==source['candidate']];pole=poles[-1];tau=pole['lifetime_s'];k=1/tau;O=source['pair_drive_per_s'];t=source['weak_no_loss_time_for_probability_001_s']
 for linewidth in [0.,1e-6,.001]:
  gamma=4*math.pi*linewidth
  matrix=np.array([[-k,2*O,0],[2*O,-k-gamma,O],[0,0,0.]])
  y=expm(matrix*t)@np.array([0.,0.,1.]);assert y[0]>=0
  growth=-(2*k+gamma)/2+math.sqrt((gamma/2)**2+4*O*O)
  stationary=2*O*O/(k*(k+gamma)-4*O*O) if growth<0 else None
  if stationary is not None:
   yy=np.array([stationary,k*stationary/(2*O),1.]);error=float(max(abs(matrix@yy)))
   assert error<1e-14;checks.append(dict(name='stationary_moments',error=error,tolerance=1e-14))
  rows.append(dict(candidate=source['candidate'],single_particle_lifetime_s=tau,drive_per_s=O,common_laser_linewidth_Hz=linewidth,comparison_time_s=t,mean_occupation_per_charge=y[0],asymptotic_moment_growth_per_s=growth,stationary_mean_occupation_per_charge=stationary))
# Independent zero-loss/no-noise squeezed-vacuum moment identity.
O=.3;t=.7;matrix=np.array([[0,2*O,0],[2*O,0,O],[0,0,0.]])
y=expm(matrix*t)@np.array([0.,0.,1.]);error=abs(y[0]-math.sinh(O*t)**2);assert error<1e-14
checks.append(dict(name='lossless_squeezed_vacuum_moment',error=error,tolerance=1e-14))
result=dict(scope='Two-mode leading quadratic quantum moment model with independent tunneling loss and specified phase diffusion; mean occupation is not a one-pair probability, high-occupation growth neglects nonlinear saturation',rows=rows,checks=checks,passed=len(checks),retention_checks=r['passed'],source_checks=s['passed'])
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

import numpy as np,json,os
from pathlib import Path
from event_step import localize
late=os.environ.get('MUTATE')=='1'
# Exact constant-acceleration trial: turnaround at t=.37, not endpoint1.
propose=lambda h:np.array([.37*h-.5*h*h,.37-h])
h,state,event=localize(propose,lambda z:np.array([z[1]]),np.array([.37]),1.,relative_tol=1e-8,late=late)
checks={'localized_turnaround_time':abs(h-.37)<1e-8,'localized_velocity_residual':abs(state[1])<1e-8,'bracket_width':event['bracket_width']<1e-8}
# Independently known smooth pressure crossing at .63.
h2,_,ev2=localize(lambda h:np.array([h]),lambda z:np.array([.63-z[0]]),np.array([.63]),1.,relative_tol=1e-8,late=late)
checks['pressure_crossing_time']=abs(h2-.63)<1e-8
# No-trigger KDK harmonic trajectory against analytic (cos t,-sin t).
errors=[]
for n in [20,40,80]:
 x=1.;v=0.;dt=1/n
 for _ in range(n):
  olda=-x;x+=dt*(v+.5*dt*olda);v+=.5*dt*(olda-x)
 errors.append(float(np.hypot(x-np.cos(1),v+np.sin(1))))
checks['no_trigger_second_order']=all(3.8<errors[i]/errors[i+1]<4.2 for i in range(2))
# Mass split is exactly fraction bookkeeping, independently of event localization.
from exact_moments import kick_moments
fe,_,_=kick_moments(np.array([3.,0.,5.]),np.array([4.,0.,0.]),np.array([-20.,-10.,-100.]),6.)
m=np.array([2.,3.,7.]);checks['kick_mass_accounting']=abs(np.sum(m*(1-fe))+np.sum(m*fe)-m.sum())<1e-13
j={'mutation':late,'checks':{k:bool(v) for k,v in checks.items()},'turnaround':float(h),'pressure_event':float(h2),'harmonic_errors':errors}
Path(__file__).with_name('controls_mutation.json' if late else 'controls_main.json').write_text(json.dumps(j,indent=2));print(json.dumps(j,indent=2));raise SystemExit(0 if all(checks.values()) else 1)

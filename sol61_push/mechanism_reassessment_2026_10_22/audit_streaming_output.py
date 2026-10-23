import json,sys,ctypes
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=Path(__file__).parent;N=32;eps=1e-8;m=np.arange(1,N+1)/N
lib=ctypes.CDLL(str((p/'collapse_force.dylib').resolve()))
lib.collapse_rhs.argtypes=[ctypes.c_int,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
lib.collapse_rhs.restype=None
def rhs(t,y):
    out=np.empty_like(y);lib.collapse_rhs(N,eps,y.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),out.ctypes.data_as(ctypes.POINTER(ctypes.c_double)));return out
floor=np.sqrt(m/(1-eps))
def event(t,y):return float(np.min(y[:N]-floor))
event.terminal=True;event.direction=-1
y=np.r_[6*m**(1/3),3.,np.zeros(N+1)]
options=dict(method='DOP853',rtol=2e-11,atol=2e-13,max_step=.025,events=event)
a=solve_ivp(rhs,(0,8),y,dense_output=True,**options)
b=solve_ivp(rhs,(0,8),y,t_eval=np.arange(81)/10,dense_output=False,**options)
difference=float(np.max(abs(a.sol(b.t)-b.y)))
event_difference=float(np.max(abs(a.y_events[0]-b.y_events[0])))
checks=dict(first_event_reached=len(a.t_events[0])==1 and len(b.t_events[0])==1,
    sample_equivalence=difference<1e-10,event_equivalence=event_difference<1e-10,
    no_persistent_interpolant=b.sol is None)
out=dict(checks=checks,all_pass=all(checks.values()),sample_max_difference=difference,
    event_state_max_difference=event_difference,event_time=float(a.t_events[0][0]),
    scope='N32 trajectory through first barrier event only; tests output-retention change, not physical convergence.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)

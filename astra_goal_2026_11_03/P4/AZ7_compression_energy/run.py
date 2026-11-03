import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
from scipy.integrate import quad

def w(R):return 2/(0.5*R+math.sqrt(0.25*R*R+12))
def calculate():
    errors=[abs(0.5*R*w(R)+3*w(R)**2-1) for R in [1,0.1,0.01]]
    limit=(1/3)**0.25;rel=abs(math.sqrt(w(1e-6))/limit-1)
    t=quad(lambda R:1/math.sqrt(w(R)),0,1,epsabs=1e-12)[0]
    t2=sum(quad(lambda R:1/math.sqrt(w(R)),a,b,epsabs=1e-12)[0] for a,b in [(0,.5),(.5,1)])
    mut=abs(.5*w(1)+w(1)**2-1)
    checks={'energy_known_answer':max(errors)<=1e-10,'asymptotic_known_answer':rel<=1e-6,'quadrature':abs(t-t2)<=1e-10,'mutate_bites':mut>0.1}
    label='FAIL' if all(checks.values()) else 'NO VERDICT'
    return {'assertion_tested':'positive quartic compression term does not prevent finite-time homogeneous collapse in reduced mechanics','label':label,'footings':{f:{'label':label,'empirical_label':'NOT EVALUABLE','time_to_zero':t,'limiting_speed':limit,'relative_asymptotic_error':rel,'energy_error':max(errors),'quadrature_difference':abs(t-t2),'mutate_energy_error':mut} for f in ['canonical','alt']},'bounds':{'M_B_C':[1,1,1],'p':2,'R_energy':[1,.1,.01],'R_asymptotic':1e-6,'R_time':[0,1]},'checks':[{'name':k,'passed':bool(v)} for k,v in checks.items()],'free_physical_numbers':['kappa=1/2 FITTED','C undetermined: FITTED if chosen physically','p=2 proposed operator choice, not derived from data; general finite p treated analytically'],'residual_risks':['reduced mechanics only, not covariant field equations','no statement about boundary pressure or arbitrary nonlocal completions']}
record(__file__,calculate)

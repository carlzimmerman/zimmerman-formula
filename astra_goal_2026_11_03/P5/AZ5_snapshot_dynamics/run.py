import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
from scipy.integrate import quad

def calculate():
    x=1.;f=lambda v:math.exp(-(x*x+v*v)/2)/(2*math.pi)
    n=math.exp(-x*x/2)/math.sqrt(2*math.pi)
    moment=lambda w,wrong=False:quad(lambda v:v*(1+(w*w) if wrong else 1-w*w)*x*v*f(v),-math.inf,math.inf,epsabs=1e-12)[0]
    stat=moment(1);dynamic=moment(2);mut=moment(2,True)
    density=quad(f,-math.inf,math.inf,epsabs=1e-12)[0]
    second=quad(lambda v:v*v*f(v),-math.inf,math.inf,epsabs=1e-12)[0]
    errs={'stationary':abs(stat),'density':abs(density-n),'second_moment':abs(second-n),'time_derivative':abs(dynamic+3*x*n)}
    checks={k:v<=1e-10 for k,v in errs.items()};checks['mutate_bites']=abs(mut+3*x*n)>1e-2
    vals={'n':n,'omega1_flux_derivative':stat,'omega2_flux_derivative':dynamic,'oracle':-3*x*n,'mutate_flux_derivative':mut,'mutate_error':abs(mut+3*x*n),'errors':errs}
    return {'assertion_tested':'same Gaussian phase-space snapshot permits distinct attractive harmonic forces with different time derivatives','label':'NO VERDICT','scope':'P5 observational closure not identified','footings':{f:{'label':'NO VERDICT','identity_label':'PASS' if all(checks.values()) else 'NO VERDICT','values':vals} for f in ['canonical','alt']},'bounds':{'x':1,'omega':[1,2],'v_domain':'real line'},'checks':[{'name':k,'passed':bool(v)} for k,v in checks.items()],'free_physical_numbers':['kappa=1/2 FITTED','real tracer history and initial distribution unspecified; FITTED if adjusted to residuals'],'residual_risks':['no measured IC1613 or MW time derivatives','synthetic 1D identifiability result, not a galaxy evolution model']}
record(__file__,calculate)

import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
from scipy.integrate import quad

def calculate():
    integ=lambda f:quad(f,0,2*math.pi,epsabs=1e-12)[0]
    u=lambda x:1+.5*math.cos(x);up=lambda x:-.5*math.sin(x);upp=lambda x:-.5*math.cos(x)
    v=lambda x:1+.25*math.cos(2*x);vp=lambda x:-.5*math.sin(2*x)
    def action(e,variable):
        def fn(x):
            U=u(x);P=up(x);D=.01*(1+U*U) if variable else .01;Dp=.02*U if variable else 0
            rho=U-D*upp(x)-Dp*P*P
            z=U+e*v(x);zp=P+e*vp(x);dz=.01*(1+z*z) if variable else .01
            return .5*z*z+.5*dz*zp*zp-rho*z
        return integ(fn)
    h=1e-5;fd=(action(h,True)-action(-h,True))/(2*h);oracle=integ(lambda x:.01*u(x)*up(x)**2*v(x))
    constant=(action(h,False)-action(-h,False))/(2*h)
    mass_extra=integ(lambda x:.01*u(x)*up(x)**2);analytic=.01*math.pi/4
    checks={'variation_known_answer':abs(fd-oracle)<=1e-8,'constant_D_known_answer':abs(constant)<=1e-8,'mass_integral':abs(mass_extra-analytic)<=1e-10,'mutate_bites':abs(fd)>1e-4}
    label='FAIL' if all(checks.values()) else 'NO VERDICT'
    vals={'action_directional_derivative':fd,'Euler_oracle':oracle,'variation_error':abs(fd-oracle),'constant_D_derivative':constant,'extra_integrated_source':mass_extra,'mass_oracle':analytic,'mutate_missing_term_error':abs(fd)}
    return {'assertion_tested':'plug-in D(u) conservative filter omits Euler term and is not the proposed action variation','label':label,'footings':{f:{'label':label,'empirical_label':'NOT EVALUABLE','values':vals} for f in ['canonical','alt']},'bounds':{'x':[0,2*math.pi],'h':h,'u':'1+0.5 cos x','D':'0.01(1+u^2)','v':'1+0.25 cos(2x)'},'checks':[{'name':k,'passed':bool(v)} for k,v in checks.items()],'free_physical_numbers':['kappa=1/2 FITTED','physical D unspecified, every selected coefficient FITTED'],'residual_risks':['a coefficient depending on a separate gravitational field requires its own coupled variation, not excluded here']}
record(__file__,calculate)

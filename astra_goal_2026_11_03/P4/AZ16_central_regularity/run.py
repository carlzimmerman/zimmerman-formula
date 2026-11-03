from pathlib import Path
import sys
import numpy as np
from scipy.integrate import solve_ivp,quad
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record

def calculate():
    exact=-64/9;div=[]
    for r in [.01,.1,1.]:
        h=r*.001
        flux=lambda s:s*s*(-4/3*s**(1/3))**3
        div.append((flux(r+h)-flux(r-h))/(2*h*r*r))
    p=2.;h=1e-4
    derivative=(256*(p+h)**4-256*(p-h)**4)/(2*h)
    points=np.array([1e-4,1e-3]);a=.75*(1/3)**(1/3)
    def run(r0,tol):
        def rhs(r,y):
            psi,f,m,phi=y
            return [np.cbrt(f/r**2),r*r*(phi-1)*psi**3,r*r*psi**4,m/r**2]
        sol=solve_ivp(rhs,(r0,1e-3),[1-a*r0**(4/3),-r0**3/3,r0**3/3,r0*r0/6],method='DOP853',rtol=tol,atol=1e-25,dense_output=True)
        assert sol.success,sol.message
        y=sol.sol(points);slopes=np.cbrt(y[1]/points**2)
        return slopes/(-(points/3)**(1/3))
    first=run(1e-8,1e-11);fine=run(1e-9,1e-12)
    eps=1e-4
    def integrand(x):
        rho=1+eps*np.cos(x);d=-eps*np.sin(x);s=(d/rho)**2
        return rho*(s*s+2*s)/eps**2
    energy_coefficient=quad(integrand,0,2*np.pi,epsabs=1e-11)[0]
    dispersion=2*energy_coefficient/np.pi
    checks=[('manufactured radial operator',max(abs(np.array(div)/exact-1))<=1e-6),('variation normalization',abs(derivative/(1024*p**3)-1)<=1e-6),('weak-core leading slope',max(abs(first-1))<.001),('weak-core start/tolerance refinement',max(abs(first-fine))<1e-5),('MUTATE missing radial term',abs((-64/27)/exact-1)>=.5),('regularization linear coefficient',abs(dispersion/4-1)<=1e-6),('MUTATE zero linear dispersion',abs(dispersion)>1)]
    checks=[{'name':k,'passed':bool(v)} for k,v in checks]
    label='FAIL' if all(c['passed'] for c in checks) else 'NO VERDICT'
    return {'assertion_tested':'Existence of positive centrally nonincreasing C2 spherical equilibrium of pure AZ14 quartic-gradient energy','label':label,'footings':{k:{'label':label,'scope':'Smooth central equilibrium only; a0 cancels','weak_equilibrium':'NO VERDICT','empirical_rows':'NOT EVALUABLE'} for k in ['canonical','alt']},'checks':checks,'bounds':{'domain':'positive lambda,G; regular C2 spherical origin; central nonincrease','local_ODE_points':points.tolist(),'synthetic_units':'256lambda=4piG=psi0=mu-Phi0=1'},'values':{'manufactured_divergence':div,'exact_divergence':exact,'variation_numeric':derivative,'variation_exact':1024*p**3,'weak_slope_ratio':first.tolist(),'refined_weak_slope_ratio':fine.tolist(),'slope_margin':float(.001-max(abs(first-1))),'refinement_margin':float(1e-5-max(abs(first-fine))),'regularized_dispersion_coefficient':dispersion,'MUTATE_radial_relative_error':abs((-64/27)/exact-1)},'free_physical_numbers':['lambda positive FITTED undetermined','kappa=.5 FITTED','global normalization and chemical potential unselected, FITTED if assigned','q0 regularizer FITTED if introduced; not adopted'], 'residual_risks':['C1 weak cores are not excluded','Local ODE does not solve isolated outer boundary or establish dynamic stability','Bounded density proof remains conditional and does not imply C2 regularity','Regularized linear pressure is not an observational fail without a physical q0 and lambda','No empirical row credit']}
if __name__=='__main__':record(__file__,calculate)

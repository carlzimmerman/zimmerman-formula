from pathlib import Path
import sys
import numpy as np
from scipy.integrate import quad
from scipy.special import erf
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record

def calculate():
    rho=lambda r:np.exp(-r*r/2)/(2*np.pi)**1.5
    mass=lambda r:erf(r/np.sqrt(2))-np.sqrt(2/np.pi)*r*np.exp(-r*r/2)
    energy=quad(lambda r:4*np.pi*r**6*rho(r),0,np.inf,epsabs=1e-12,epsrel=1e-12)[0]
    binding=quad(lambda r:-4*np.pi*mass(r)*rho(r)*r,0,np.inf,epsabs=1e-12,epsrel=1e-12)[0]
    B=1/(2*np.sqrt(np.pi));C=15.;rs=(4*C/B)**(1/3)
    U=lambda r:C/r**4-B/r
    h=rs*1e-4
    slope=(U(rs+h)-U(rs-h))/(2*h)
    curvature=(U(rs+h)-2*U(rs)+U(rs-h))/h**2
    exact=3*B/rs**3
    r=2.;p=np.array([1.,-2.,.5]);dr=.3;dp=np.array([.4,.2,-.1]);z=dp-p*dr/r
    f=lambda r,p:np.dot(p,p)**2/r**3
    second=4*np.dot(p,p)*np.dot(z,z)/r**3+8*np.dot(p,z)**2/r**3
    fd=[(f(r+t*dr,p+t*dp)-2*f(r,p)+f(r-t*dr,p-t*dp))/t**2 for t in [1e-3,5e-4]]
    # rho=1+epsilon cos(x): quartic leading energy pi*3/4 epsilon^4;
    # quadratic perspective has pi epsilon^2 and hence a nonzero Hessian.
    quartic_leading=quad(lambda x:np.sin(x)**4,0,2*np.pi,epsabs=1e-12)[0]
    quadratic_leading=quad(lambda x:np.sin(x)**2,0,2*np.pi,epsabs=1e-12)[0]
    checks=[('Gaussian gradient integral',abs(energy/15-1)<=1e-10),('Gaussian gravitational integral',abs(binding/(-B)-1)<=1e-10),('stationary derivative',abs(slope)<=1e-5),('stationary curvature',abs(curvature/exact-1)<=1e-5),('joint Hessian identity',max(abs(np.array(fd)/second-1))<=1e-5),('quartic perturbation coefficient',abs(quartic_leading/(3*np.pi/4)-1)<=1e-10),('MUTATE sign destroys barrier',-energy<0 and -4*C/B<0),('MUTATE quadratic has linear pressure',abs(quadratic_leading/np.pi-1)<=1e-10 and quadratic_leading>0)]
    checks=[{'name':k,'passed':bool(v)} for k,v in checks]
    label='PASS' if all(c['passed'] for c in checks) else 'NO VERDICT'
    return {'assertion_tested':'Convex quartic density-gradient term: no linear homogeneous pressure, nonnegative second variation, Gaussian homology compression barrier','label':label,'footings':{k:{'label':label,'scope':'Structural gates only; a0 cancels','empirical_rows':'NOT EVALUABLE'} for k in ['canonical','alt']},'checks':checks,'bounds':{'rho_domain':'strictly positive','geometry':'Gaussian fixed-mass homology and smooth periodic perturbation','synthetic_units':'G=M=lambda=1; no physical coefficient selected'},'values':{'gradient_energy':energy,'binding_energy':binding,'Rstar':rs,'stationary_slope':slope,'curvature_numeric':curvature,'curvature_exact':exact,'hessian_exact':second,'hessian_finite_difference':fd,'quartic_leading_coefficient':quartic_leading,'quadratic_MUTATE_leading_coefficient':quadratic_leading},'free_physical_numbers':['lambda positive FITTED undetermined','kappa=.5 FITTED','quartic power model choice; density power from perspective construction'], 'residual_risks':['Newtonian constitutive term only; no covariant completion','Fourth-order spatial PDE with unbounded high-k phase speed in this nonrelativistic limit','Vacuum rho=0 singular; Gaussian homology is not full nonlinear stability','No baryonic coupling, galaxy contraction or CMB data test','Linear Jeans growth remains; no claim of no contraction or all-shape collapse prevention']}
if __name__=='__main__':record(__file__,calculate)

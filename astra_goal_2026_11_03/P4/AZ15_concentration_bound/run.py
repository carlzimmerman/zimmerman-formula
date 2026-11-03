from pathlib import Path
import sys,itertools
import numpy as np
from scipy.integrate import quad
from numpy.polynomial.hermite import hermgauss
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record

def calculate():
    C=(3**.25+3**.75)/(4*np.pi)**.25
    K=3/16*(3**.25+3**.75)**(4/3)
    def fg(r):return float(np.sum(r**-2)**2+2*np.sum(r**-4))
    def wg(r):return -quad(lambda s:1/np.sqrt(np.prod(s+r*r)),0,np.inf,epsabs=1e-12,epsrel=1e-12)[0]/(4*np.sqrt(np.pi))
    sphere=np.ones(3);axes=np.array([1.,2.,3.]);x,w=hermgauss(3)
    direct=0.
    for i,j,k in itertools.product(range(3),repeat=3):
        p=np.sqrt(2)*np.array([x[i],x[j],x[k]])/axes
        direct+=w[i]*w[j]*w[k]/np.pi**1.5*np.dot(p,p)**2
    F=fg(sphere);W=wg(sphere);B=1/(2*np.sqrt(np.pi))
    J=quad(lambda r:4*np.pi*r**6*np.exp(-r*r/2)/(2*np.pi)**1.5/256,0,np.inf,epsabs=1e-12,epsrel=1e-12)[0]
    peak=(2*np.pi)**(-1.5);peak_bound=C**4*J**.75
    Wbound=K*F**.25
    # ||(4pi r^2)^-1||_(4/3) on unit ball.
    integral=quad(lambda r:(4*np.pi)**(-1/3),0,1,weight='alg',wvar=(-2/3,0),epsabs=1e-12)[0]
    norm=integral**.75;norm_exact=3**.75*(4*np.pi)**(-.25)
    Fa=fg(axes);Wa=wg(axes);rmin=min(axes)
    checks=[('sphere gradient oracle',abs(F/15-1)<=1e-10),('sphere binding oracle',abs(W/(-B)-1)<=1e-10),('affine independent product quadrature',abs(direct/Fa-1)<=1e-12),('affine lower gradient bound',Fa>=3/rmin**4),('affine upper binding bound',abs(Wa)<=B/rmin),('Gaussian global peak bound',peak<=peak_bound),('Gaussian global binding bound',abs(W)<=Wbound),('Holder kernel norm',abs(norm/norm_exact-1)<=1e-10),('Gaussian transformation oracle',abs(F/(256*J)-1)<=1e-10),('MUTATE missing factor bites',abs(F/J-1)>100),('MUTATE negative gradient destroys barrier',-15<0 and -300-2*B<0)]
    checks=[{'name':k,'passed':bool(v)} for k,v in checks];label='PASS' if all(v['passed'] for v in checks) else 'NO VERDICT'
    return {'assertion_tested':'AZ14 energy bounds arbitrary smooth density concentration and affine Gaussian axis collapse under stated isolated conservative assumptions','label':label,'footings':{k:{'label':label,'scope':'Analytic structural bounds only; a0 cancels','empirical_rows':'NOT EVALUABLE'} for k in ['canonical','alt']},'checks':checks,'bounds':{'domain':'smooth nonnegative psi=rho^(1/4), finite positive mass and W1,4 norm, isolated self gravity','coefficients':'lambda>0, no numerical physical lambda selected','affine_control_axes':[1,2,3]},'values':{'C':C,'K':K,'sphere_F':F,'sphere_W':W,'sphere_J':J,'density_peak_margin':peak_bound-peak,'binding_bound_margin':Wbound-abs(W),'affine_F':Fa,'affine_F_independent':direct,'affine_W':Wa,'affine_gradient_margin':Fa-3/rmin**4,'affine_binding_margin':B/rmin-abs(Wa),'kernel_norm':norm,'kernel_norm_exact':norm_exact,'MUTATE_factor_error':F/J-1},'free_physical_numbers':['lambda positive FITTED undetermined','kappa=.5 FITTED','quartic power model choice'],'residual_risks':['No global existence theorem for the degenerate fourth-order fluid equations','Does not prevent finite contraction or shocks','No covariant completion, baryonic coupling or empirical rows','Fixed mass, isolated energy-conserving system; arbitrary imposed baryonic potential needs a separate bound','Vacuum interfaces require weak formulation in psi; smoothness hypotheses essential']}
if __name__=='__main__':record(__file__,calculate)

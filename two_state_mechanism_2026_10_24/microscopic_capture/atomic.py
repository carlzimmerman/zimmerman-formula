"""Ground-state Coulomb radiative channel; energies/masses in eV (c=1).

Returns cross sections in cm^2 and thermal coefficients in cm^3/s.
Degeneracy ratio g_atom/(g_X*g_C)=1; both photon polarizations included.
Leading nonrelativistic electric-dipole theory, no collisional ionization.
"""
import math
import numpy as np
from scipy.integrate import quad, solve_ivp

HC=1.973269804e-5  # hbar*c in eV cm
LIGHT=2.99792458e10  # cm/s


class Atom:
    def __init__(self, alpha, mC, mX):
        if not (0 < alpha < 1 and mC > 0 and mX > 0):
            raise ValueError('positive masses and 0<alpha<1 required')
        self.alpha=alpha; self.mC=mC; self.mX=mX
        self.mu=mC*mX/(mC+mX)
        self.binding=.5*alpha**2*self.mu
        self.radius=HC/(alpha*self.mu)
        self.threshold=512*math.pi**2/(3*math.e**4)*alpha*self.radius**2

    @staticmethod
    def shape(excess):
        """Photoionization cross section / threshold, excess=(omega-B)/B."""
        if excess < 0: return 0.
        if excess == 0: return 1.
        t=math.sqrt(excess)
        return math.exp(4-4*math.atan(t)/t)/(-math.expm1(-2*math.pi/t))/(1+excess)**4

    def photo(self, omega):
        return self.threshold*self.shape((omega-self.binding)/self.binding)

    def capture(self,E):
        """Spontaneous inverse cross section; E is positive relative KE."""
        if E<=0: raise ValueError('E>0 required; zero-energy cross section diverges')
        return (self.binding+E)**2/(self.mu*E)*self.photo(self.binding+E)

    def recombination(self,T,Tgamma=0.):
        """(rate coefficient, mean incident relative energy per event)."""
        if T<=0 or Tgamma<0: raise ValueError('T>0, Tgamma>=0 required')
        theta=T/self.binding
        def weight(u):
            if u>740: return 0.
            e=theta*u; omega=self.binding+T*u
            stimulated=1. if Tgamma==0 else 1/(-math.expm1(-omega/Tgamma))
            return (1+e)**2*self.shape(e)*math.exp(-u)*stimulated
        j=quad(weight,0,np.inf,epsabs=1e-11,epsrel=1e-9)[0]
        j1=quad(lambda u:u*weight(u),0,np.inf,epsabs=1e-11,epsrel=1e-9)[0]
        pref=2*math.sqrt(2/math.pi)*LIGHT*self.binding**2*self.threshold/(self.mu**1.5*math.sqrt(T))
        return pref*j,T*j1/j

    def photo_rate(self,Tgamma):
        """(per-atom absorption rate, mean absorbed photon energy)."""
        if Tgamma<0: raise ValueError('negative photon temperature')
        if Tgamma==0: return 0.,0.
        b=self.binding/Tgamma
        if b>740: return 0.,self.binding
        theta=1/b
        def weight(u):
            if u>740:return 0.
            e=theta*u
            return (1+e)**2*self.shape(e)*math.exp(-u)/(-math.expm1(-(b+u)))
        j=quad(weight,0,np.inf,epsabs=1e-11,epsrel=1e-9)[0]
        j1=quad(lambda u:u*weight(u),0,np.inf,epsabs=1e-11,epsrel=1e-9)[0]
        pref=LIGHT*Tgamma*self.binding**2*self.threshold/(math.pi**2*HC**3)*math.exp(-b)
        return pref*j,self.binding+Tgamma*j1/j

    def saha(self,T):
        return (self.mu*T/(2*math.pi*HC**2))**1.5*math.exp(-self.binding/T)


def parcel(atom,theta0,tau_end=10.,rtol=1e-9):
    """Constant-volume, no incoming photons; tau=n*k_initial*t.

    Includes thermal energy, negative atomic binding energy and escaped radiation.
    Maxwellian rethermalization is a closure, not resolved particle dynamics.
    """
    k0=atom.recombination(theta0*atom.binding)[0]
    def rhs(t,y):
        x,theta,q=y
        k,E=atom.recombination(theta*atom.binding)
        event=x*x*k/k0
        dx=-event; dq=event*(1+E/atom.binding)
        dtheta=(-dq-(1+1.5*theta)*dx)/(1.5*(1+x))
        return [dx,dtheta,dq]
    sol=solve_ivp(rhs,(0,tau_end),[1.,theta0,0.],rtol=rtol,atol=rtol*1e-2,
                  t_eval=np.linspace(0,tau_end,201))
    if not sol.success:raise RuntimeError(sol.message)
    x,theta,q=sol.y
    if np.any((x<0)|(x>1)|(theta<=0)|(q<0)):raise RuntimeError('nonphysical parcel')
    H=1.5*(1+x)*theta-(1-x)+q
    return dict(theta0=theta0,tau_end=tau_end,bound_fraction=float(1-x[-1]),
                temperature_over_binding=float(theta[-1]),radiation_per_binding=float(q[-1]),
                max_energy_error=float(np.max(np.abs(H-3*theta0))/max(1,3*theta0)),
                evaluations=sol.nfev)

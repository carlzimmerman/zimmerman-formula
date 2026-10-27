"""Manufactured scattering data for software checks only; never halo evidence."""
import unittest
import numpy as np
from scipy.integrate import solve_ivp
from coupling import thermal_loss, collision_source

class ConservativeCollisionTests(unittest.TestCase):
    def test_unit_loss_maxwell_integral(self):
        E=np.geomspace(1e-12,100.,20000)
        for T in [.001,.1,1.]:
            rate,tail=thermal_loss(T,E,np.ones_like(E),mu=201/202)
            exact=np.sqrt(2*np.pi)/(201/202)**1.5/np.sqrt(T)
            self.assertLess(abs(rate/exact-1),3e-6)
            self.assertLess(tail/exact,1e-8)
    def test_invalid_probability_rejected(self):
        with self.assertRaises(ValueError):thermal_loss(.1,np.array([.01,1.]),np.array([.1,1.01]))
    def test_energy_charge_and_detailed_balance(self):
        D=np.array([.08,.02]);g=np.array([1.,3.]);T=.2;n=.4;age=2.
        a=.2;t=np.array([.1,.03]);k=np.array([.3,.7]);y=np.r_[a,t,1.]
        z=collision_source(y,T,n,age,D,g,k)
        self.assertAlmostEqual(z[-1]-.5*z[0]-np.dot(.5+D,z[1:-1]),0.,places=14)
        dx=-z[0]-2*sum(z[1:-1]);dc=-z[0]-sum(z[1:-1])
        self.assertAlmostEqual(dx+sum(z[1:-1])-dc,0.,places=14)
        self.assertAlmostEqual(dx,0.,places=14)
        # Construct a genuine retained-network equilibrium independently.
        from scipy.optimize import brentq
        mu=100*101/201
        ka=(T/(2*np.pi))**1.5*np.exp(-.5/T)
        kb=(mu*T/(2*np.pi))**1.5*np.exp(-D/T)/g
        q=n/ka;r=sum(n/kb)
        x=brentq(lambda x:q*r*x**3+q*(1+r)*x*x+x-1,0,1,xtol=1e-15)
        a=(1-x)/(1+2*r*x);tb=(n/kb)*a*x
        z=collision_source(np.r_[a,tb,1.],T,n,age,D,g,k)
        self.assertLess(max(abs(z)),1e-13)
    def test_collision_evolution_conserves_energy(self):
        D=np.array([.08,.02]);g=np.array([1.,3.]);y0=np.array([.2,.1,.03,.6])
        def fun(time,y):
            x=1-y[0]-2*sum(y[1:-1]);T=y[-1]/(1.5*(1+x))
            return collision_source(y,T,.1,100.,D,g,np.array([.3,.7])/np.sqrt(T))
        sol=solve_ivp(fun,(0,1),y0,method='BDF',rtol=1e-10,atol=1e-13)
        self.assertTrue(sol.success)
        energy=sol.y[-1]-.5*sol.y[0]-(.5+D)@sol.y[1:-1]
        self.assertLess(max(abs(energy-energy[0])),1e-12)
        self.assertGreaterEqual(float(np.min(sol.y)),0.)
if __name__=='__main__':unittest.main()

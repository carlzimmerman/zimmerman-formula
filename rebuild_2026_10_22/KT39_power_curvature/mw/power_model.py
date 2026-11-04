"""KT39 power-family energy on the checked KT37 compatible Hessian; no historical edits."""
from pathlib import Path
import sys
sys.dont_write_bytecode=True
RB=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(RB/'KT37_generalized_action/mw'))
import generalized_v3 as J
M,E,L,np=J.M,J.E,J.L,J.np


POWER=1.5

def set_power(p):
    global POWER
    if not 1. <= p <= 2.: raise ValueError("power must lie in [1,2]")
    POWER=float(p)


class PowerCurvature(J.Generalized):
    """P=xR(x+s^POWER), s=ell^2 H:H, in the inherited a0/kpc units."""
    @staticmethod
    def coefficients(gg,hh,ell,newtonian=False):
        x=np.sum(gg*gg,axis=0)
        h2=np.sum(J.Generalized.multiplicity[:,None]*hh*hh,axis=0)
        s=ell*ell*h2;z=x+s**POWER
        A=np.zeros_like(gg);B=np.zeros_like(hh);energy=np.zeros_like(x)
        if newtonian:return A,B,energy,z
        active=z>0
        if np.any(active):
            zz=z[active];ratio=x[active]/zz
            excess=L.Rminus1(zz);dd=L.zRprime(zz)
            cc=excess+ratio*dd
            A[:,active]=cc*gg[:,active]
            B[:,active]=(POWER*ell*ell*s[active]**(POWER-1)*ratio*dd)*hh[:,active]
            energy[active]=x[active]*excess
        return A,B,energy,z


Generalized=PowerCurvature

"""Sharp spherical gradient-energy capacity and inherited stability thresholds."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from angular_gate import Field
from model import G,A0,PROFILES

XIN=2/np.pi*np.arcsin(np.sqrt(.95));XOUT=2/np.pi*np.arcsin(np.sqrt(.05))
DX=XIN-XOUT

def threshold(mass,b,n):
    field=Field(mass,b,n,1,grid='uniform')
    C=field.kinematics(.95)['C'];curv,_=field.stability(20,C)
    D=field.mobility_denom;L=field.Lmat
    def ev(ell):
        return float(eigh_tridiagonal((curv+ell**2*np.diag(L))/D,
          ell**2*np.diag(L,1)/np.sqrt(D[:-1]*D[1:]),select='i',select_range=(0,0),
          eigvals_only=True,lapack_driver='stebz',tol=1e-10)[0])
    uniform_rayleigh=float(sum(curv)/sum(D))
    if uniform_rayleigh<0:
        return dict(n=n,status='uniform direction unstable for any stiffness',uniform_rayleigh=uniform_rayleigh,
                    threshold_kpc=None,ev30=ev(30))
    es=np.geomspace(1e-6,1e4,81);vals=[ev(e) for e in es]
    hits=[i for i in range(1,len(es)) if vals[i]>=0 and vals[i-1]<0]
    if not hits:
        return dict(n=n,status='unbracketed',uniform_rayleigh=uniform_rayleigh,threshold_kpc=None,ev30=ev(30))
    i=hits[0];root=brentq(ev,es[i-1],es[i],xtol=1e-9)
    return dict(n=n,status='bracketed',threshold_kpc=root,ev_below=ev(root*.99),ev_above=ev(root*1.01),
                uniform_rayleigh=uniform_rayleigh,ev30=ev(30))

def checks():
    errors=[]
    for a,b in [(1,2),(2,30),(.1,1e3)]:
        B=DX/(1/a-1/b)
        def x(r):return XOUT+B*(1/r-1/b)
        integral=quad(lambda r:B*B/r**2,a,b,epsabs=1e-10)[0]
        exact=DX*DX/(1/a-1/b)
        errors.extend([abs(integral/exact-1),abs(x(a)-XIN),abs(x(b)-XOUT)])
    # Physical check of a0² ell² R/(2G), expressed as Msun (km/s)².
    kpc=3.085677581491367e19;msun=1.98847e30
    si=(9.3603e-11)**2*(30*kpc)**2*(5*kpc)*DX**2/(2*6.67430e-11)/(msun*1e6)
    mixed=A0*A0*30**2*5*DX**2/(2*G)
    assert max(errors)<1e-9 and abs(si/mixed-1)<1e-4
    return dict(capacity_equality_max_relative_error=max(errors),SI_unit_relative_error=abs(si/mixed-1))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    rows=[]
    for index,(name,mass,b,_) in enumerate(PROFILES):
        kap=A0*b*b/(G*mass);unit=G*mass*mass/b
        stability=[threshold(mass,b,n) for n in [64,128,256]]
        costs=[]
        for rin in [.5,2,5]:
            coefficient=.5*kap**2*rin*DX**2/b**2 # cost per ell_kpc²
            costs.append(dict(Rin_over_b=rin,cost_at_30kpc=900*coefficient,
                cost_msun_km2_s2=900*coefficient*unit,
                max_ell_kpc_for_work={str(w):float(np.sqrt(w/coefficient)) for w in [1,1.29,10,100]}))
        rows.append(dict(profile=index,name=name,mass=mass,b=b,kappa=kap,costs=costs,stability=stability))
        print(json.dumps(rows[-1]),flush=True)
    Path(args.output).write_text(json.dumps(dict(checks=checks(),dx=DX,profiles=rows),indent=2)+'\n')

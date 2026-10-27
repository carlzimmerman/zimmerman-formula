"""CE-FM-011: exact auxiliary-foliation static map and conditional clock signs."""
import json,sys
from pathlib import Path
import numpy as np
import sympy as s

K,a0,g,u,n=s.symbols('K a0 g u gN',positive=True)
W=(-a0*u-a0*a0*s.log(1-u/a0))/K
ustar=a0*g/(a0+g)
F=a0*g-a0*a0*s.log(1+g/a0)
checks=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)

legendre=s.expand_log(s.simplify(g*ustar-K*W.subs(u,ustar)),force=True)
check('canonical Legendre map',s.simplify(s.expand_log(legendre-F,force=True))==0,str(F))
fbar=-2*F;fp=s.factor(s.diff(fbar,g));fpp=s.factor(s.diff(fbar,g,2))
mu=s.simplify(1+fp/(2*g))
check('covariant simple mu',s.simplify(mu-g/(g+a0))==0,str(mu))
check('clock no-ghost transverse factor',s.simplify(-fp/(2*g)-a0/(g+a0))==0,str(-fp/(2*g)))
check('clock no-ghost longitudinal factor',s.simplify(-fpp/2-a0*a0/(g+a0)**2)==0,str(-fpp/2))
gap=s.factor(g*fpp-fp)
check('symmetric source positivity condition',s.simplify(gap-2*a0*g*g/(g+a0)**2)==0,str(gap))

lam=(n+s.sqrt(n*n+4*a0*n))/2
lp=s.diff(lam,n)
positive2=s.factor(lam-n*lp)
check('spherical phantom positive term',s.simplify(positive2-a0*n/s.sqrt(n*n+4*a0*n))==0,str(positive2))
check('inverse slope positivity witness',s.expand((n+2*a0)**2-(n*n+4*a0*n))==4*a0*a0,'lambda_prime>1 from squared-positive-root comparison')

# Derive the two weak metric gradients independently, prior to solvingPsi=Phi.
xp,xq=s.symbols('gradPhi gradPsi',positive=True)
weak=(-2*xp*xq+xq*xq+2*F.subs(g,xp))/(2*K)
jpsi=s.diff(weak,xq);jphi=s.diff(weak,xp)
check('spatial metric gradient gives harmonic slip',s.simplify(jpsi-(xq-xp)/K)==0,str(jpsi))
check('lapse gradient gives canonical polarization flux',s.simplify(jphi-(-xq+ustar.subs(g,xp))/K)==0,str(jphi))
check('high acceleration boundary is not constant',s.limit(fbar/g,g,s.oo)==-2*a0,'fbar/g->-2a0, violates fbar->constant condition')
check('relative high acceleration correction vanishes',s.limit(fbar/g**2,g,s.oo)==0,'Relative toEH gradient term')

ys=np.geomspace(1e-6,1e6,2001)
hperp=1/(1+ys);hpar=1/(1+ys)**2
check('finite positive kinetic factors',np.all(hperp>0)&np.all(hpar>0),{'hperp_min':float(hperp.min()),'hpar_min':float(hpar.min())})
check('nonuniform coercivity at high acceleration',s.limit(-fpp/2,g,s.oo)==0,'No uniform positive clock kinetic floor at arbitrarily largeg')

result=dict(checks=checks,F=str(F),fbar=str(fbar),fprime=str(fp),fsecond=str(fpp),mu=str(mu),
            weak_metric_fluxes={'Psi':str(jpsi),'Phi':str(jphi)},
            scope='Auxiliary static field completion in assumedEinstein/clock family; conditional symmetric clock-mode signs, not inertial carrier/anchor/metric closure.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

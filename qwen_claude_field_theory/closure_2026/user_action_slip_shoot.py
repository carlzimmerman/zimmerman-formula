"""Bounded search for preservation of initially matched logarithmic potentials.

P+B=0 is the leading weak-field no-slip condition in the isotropic spatial
coordinate dz=exp(-B)dx. This is not a measured PPN gamma calculation.
"""
import json
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import user_action_curved_branch as model

def data(slope):
    y=np.array([0.,0.,.5,.02,-.02,slope])
    zero=float(model.efun(*y,0.))
    flux=-zero/(float(model.efun(*y,1.))-zero)
    return y,flux

def flow(y,flux):
    return np.r_[y[3:],np.linalg.solve(model.hfun(*y,flux),np.asarray(model.ffun(*y,flux)).ravel())]

def curvature(slope):
    y,flux=data(slope);derivative=flow(y,flux)
    return float(derivative[3]+derivative[4])

grid=np.linspace(-5,5,201);values=[curvature(v) for v in grid]
roots=[]
for lo,hi,fl,fh in zip(grid[:-1],grid[1:],values[:-1],values[1:]):
    if fl*fh<0:
        root=brentq(curvature,lo,hi,xtol=1e-12)
        if abs(curvature(root))<1e-8:roots.append(root)
runs=[]
for root in roots:
    y,flux=data(root)
    sol=solve_ivp(lambda x,y:flow(y,flux),(0,.1),y,rtol=1e-10,atol=1e-12,dense_output=True)
    sample=sol.sol(np.linspace(0,.1,101)) if sol.success else sol.y
    runs.append(dict(initial_vprime=root,initial_slip_curvature=curvature(root),
        success=sol.success,max_logarithmic_slip=float(np.max(abs(sample[0]+sample[1]))),
        max_energy_constraint=float(max(abs(model.efun(*z,flux)) for z in sample.T))))
print(json.dumps(dict(scope=__doc__,full_theory='OPEN',search_interval=[-5,5],samples=201,
    curvature_min=min(values),curvature_max=max(values),roots=roots,runs=runs,
    limitation='One illustrative parameter point and fixed other initial data; sign-change search does not exclude tangential or out-of-range roots.'),indent=2))

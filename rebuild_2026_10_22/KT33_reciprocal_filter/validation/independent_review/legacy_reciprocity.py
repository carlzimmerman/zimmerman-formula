"""Independent fixed-size weighted Jacobian check of inherited UX5 QUMOND.

Finite assertion: two nonspherical zero-mass perturbations on a 48x32 full
axisymmetric FV domain, with analytic Jacobian (not finite differences).
No claim of astrophysical convergence or isolated-boundary correctness.
"""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time

for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
sys.dont_write_bytecode=True
import numpy as np
import scipy
from scipy.sparse.linalg import splu

SOURCE=Path('/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_solver.py')
before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('review_p4',SOURCE)
p4=importlib.util.module_from_spec(spec); spec.loader.exec_module(p4)
start=time.monotonic()
g=p4.Grid(np.geomspace(.02,30,49),np.linspace(0,math.pi,33))
lu=splu(g.Lap.tocsc())
r,th=g.r2d,g.t2d
R,z=r*np.sin(th),r*np.cos(th)
rho=np.exp(-R*R/3-(z-.5)**2/.6)+.25*np.exp(-R*R/1.2-(z+1.2)**2/2)
base=np.exp(-r*r/4)
f=np.exp(-R*R/2-(z-1)**2/.3)
h=np.exp(-(R-1.5)**2/.8-(z+.7)**2/.5)
f-=base*np.dot(g.vol,f)/np.dot(g.vol,base)
h-=base*np.dot(g.vol,h)/np.dot(g.vol,base)
pn=lu.solve(4*math.pi*rho)
dnf=lu.solve(4*math.pi*f); dnh=lu.solve(4*math.pi*h)

def coefficients(a,b):
    q=np.hypot(a,b)
    root=np.sqrt(.25+1/q)
    return root-.5,-.5/(q*q*q*root)

def old_jac(v):
    out=np.zeros(g.n)
    for D,T,Div in ((g.Dr,g.Tr,g.Divr),(g.Dt,g.Tt,g.Divt)):
        d,t=D@pn,T@pn
        a,b=coefficients(d,t)
        out+=Div@(a*(D@v)+b*d*(d*(D@v)+t*(T@v)))
    d=g.Do@pn
    a,b=coefficients(d,np.zeros_like(d))
    out+=g.Divo@((a+b*d*d)*(g.Do@v))
    return lu.solve(out)

def energy_jac(v):
    d,t=g.Crr@pn,g.Cth@pn
    dd,dt=g.Crr@v,g.Cth@v
    a,b=coefficients(d,t)
    contract=d*dd+t*dt
    fluxd=a*dd+b*d*contract
    fluxt=a*dt+b*t*contract
    div=-(g.Crr.T@(g.vol*fluxd)+g.Cth.T@(g.vol*fluxt))/g.vol
    return lu.solve(div)

def pair(jac):
    ab=float(np.dot(g.vol*f,jac(dnh)))
    ba=float(np.dot(g.vol*h,jac(dnf)))
    return dict(ab=ab,ba=ba,absolute=abs(ab-ba),relative=abs(ab-ba)/max(abs(ab),abs(ba)))

out=dict(assertion_tested=__doc__,grid=[g.Nr,g.Nt],domain=[float(g.re[0]),float(g.re[-1])],
         inherited_flux=pair(old_jac),cell_energy=pair(energy_jac),
         perturbation_masses=[float(np.dot(g.vol,f)),float(np.dot(g.vol,h))],
         source_file=str(SOURCE),source_sha256_before=before,
         source_sha256_after=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
         versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__),
         wall_seconds=time.monotonic()-start)
Path('/private/tmp/kt33_review/legacy_reciprocity.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

#!/usr/bin/env python3
"""Frozen radial quadrature gate and independent spherical oracle checks."""
import json,platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import quad
import spherical_boundary as R
import bullet_source as B
import audit_inputs as A
checks=[];records=[]
def check(name,ok,value=None): checks.append(dict(name=name,passed=bool(ok),value=value))
for foot in B.A0:
 eps=B.normalization(foot)['epsilon']
 for halfwidth in [4000.,8000.]:
  maxr=1.1*np.sqrt(3)*halfwidth/B.L0_KPC
  coarse=R.RadialPotential(eps,maxr,4096);fine=R.RadialPotential(eps,maxr,8192)
  # Boundary radii span face centres to corners, independent of Cartesian N.
  radii=np.linspace(halfwidth/B.L0_KPC,np.sqrt(3)*halfwidth/B.L0_KPC,1001)
  amplitude=float(fine(np.sqrt(3)*halfwidth/B.L0_KPC))
  error=float(np.max(abs(coarse(radii)-fine(radii)))/amplitude)
  check(f'{foot}_{halfwidth}_quadrature_pair',error<=1e-6,error)
  independent=[]
  for radius in radii[[0,500,1000]]:
   truth=quad(lambda r:float(R.radial_derivative(r,eps)),0,float(radius),epsabs=1e-11,epsrel=1e-11)[0]
   independent.append(abs(float(fine(radius))-truth)/amplitude)
  check(f'{foot}_{halfwidth}_adaptive_integral',max(independent)<=1e-6,max(independent))
  records.append(dict(footing=foot,half_width_kpc=halfwidth,pair_error=error,independent_errors=independent))
 # One centred Plummer: analytic derivative of enclosed mass vs direct density.
 rows=np.array([[2e14,565.,0.,0.,0.]])
 r=np.array([0.,.3,.5,1.,2.,5.])*565/B.L0_KPC
 radial,tangent=R.radial_eigenvalues(r,eps,rows)
 source=B.density(r*B.L0_KPC,0.,0.,rows)/B.RHO_REF
 residual=eps*(radial+2*tangent)+4*radial*tangent+2*tangent*tangent-source
 check(foot+'_spherical_equation',np.max(abs(residual))/max(1.,np.max(source))<=1e-12,float(np.max(abs(residual))))
 check(foot+'_centre_isotropic',radial[0]==tangent[0] and abs(float(B.selector(np.eye(3)*radial[0]))-1)<1e-12)
 step=1e-5*r[1:]
 derivative=(R.radial_derivative(r[1:]+step,eps,rows)-R.radial_derivative(r[1:]-step,eps,rows))/(2*step)
 err=float(np.max(abs(derivative-radial[1:]))/np.max(abs(radial[1:])))
 check(foot+'_radial_derivative_independent',err<=1e-8,err)
 check(foot+'_positive_principal',np.min(np.minimum(eps+4*tangent,eps+2*(radial+tangent)))>0)
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),records=records,versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(R.__file__).resolve(),Path(B.__file__).resolve(),A.HERE/'FROZEN_BULLET.md']},scope='Spherical boundary/oracle only; no 3D nonlinear solve. kappa=1/2 FITTED; not theory closed')
A.atomic(A.HERE/'spherical_boundary_checks.json',obj)
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],failed=[c for c in checks if not c['passed']]),indent=2))
raise SystemExit(int(obj['passed']!=obj['total']))

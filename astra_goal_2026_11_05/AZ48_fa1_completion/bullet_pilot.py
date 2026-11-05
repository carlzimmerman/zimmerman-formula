#!/usr/bin/env python3
"""Bounded N8/N16 implementation pilots, never Bullet physical grades."""
import json,platform
from pathlib import Path
import numpy as np
import scipy
import grid3d as D
import bullet_source as B
import spherical_boundary as R
import newton3d as N
import audit_inputs as A
results=[]
for n in [8,16]:
 for foot in B.A0:
  eps=B.normalization(foot)['epsilon'];g=D.Grid(n,centre_kpc=B.centroid());x,y,z=g.coordinates()
  radius=np.sqrt(sum((v-c/B.L0_KPC)**2 for v,c in zip([x,y,z],g.centre_kpc)))
  initial=R.RadialPotential(eps,1.1*np.sqrt(3)*4)(radius)
  source=B.density(x*B.L0_KPC,y*B.L0_KPC,z*B.L0_KPC)/B.RHO_REF
  _,report=N.solve(g,source[1:-1,1:-1,1:-1],eps,initial)
  print(n,foot,report['status'],report['residual'],report['updates'])
  results.append(dict(n=n,footing=foot,report=report))
obj=dict(results=results,versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(N.__file__).resolve(),Path(R.__file__).resolve(),Path(D.__file__).resolve(),Path(B.__file__).resolve(),B.SOURCE,A.HERE/'FROZEN_BULLET.md']},scope='N8/N16 implementation pilot only; no field convergence or Bullet classification. kappa=1/2 FITTED; not theory closed')
A.atomic(A.HERE/'bullet_pilot.json',obj)

#!/usr/bin/env python3
"""Exact symbolic check of the timelike gradient-normal vorticity witness."""
import json
from pathlib import Path
import sympy as s
import audit_inputs as A
x0,x,y,z,a=s.symbols('x0 x y z a',real=True)
coords=[x0,x,y,z];eta=s.diag(-1,1,1,1)
normalization=1/s.sqrt(1-a*a*(x*x+z*z))
T=x0-a*x*z;u=s.Matrix([-normalization*s.diff(T,q) for q in coords]);raised=eta*u
P=s.eye(4)+u*raised.T
antisymmetric=s.Matrix(4,4,lambda i,j:(s.diff(u[j],coords[i])-s.diff(u[i],coords[j]))/2)
projected=(P*antisymmetric*P.T).applyfunc(s.simplify)
norm=s.simplify((u.T*eta*u)[0])
velocity=[s.simplify(raised[i]/raised[0]) for i in (1,2,3)]
checks=[dict(name='unit_timelike_normal',passed=norm==-1),
        dict(name='velocity_is_symmetric_strain',passed=velocity==[a*z,0,a*x]),
        dict(name='all_projected_vorticity_components_zero',passed=projected==s.zeros(4))]
# Independent rigid rotation at the origin; same projected z velocity at z=0.
rot=s.Matrix([-normalization,-normalization*a*z,0,normalization*a*x])
rotanti=s.Matrix(4,4,lambda i,j:(s.diff(rot[j],coords[i])-s.diff(rot[i],coords[j]))/2)
rotP=s.eye(4)+rot*(eta*rot).T
rotomega=(rotP*rotanti*rotP.T).subs({x:0,z:0}).applyfunc(s.simplify)
checks.append(dict(name='rigid_rotation_control_nonzero',passed=rotomega[1,3]==a and rotomega[3,1]==-a))
obj=dict(checks=checks,passed=sum(bool(c['passed']) for c in checks),total=len(checks),
    scalar_T=str(T),u_covariant=[str(v) for v in u],norm=str(norm),velocity_over_c=[str(v) for v in velocity],
    projected_vorticity=[[str(projected[i,j]) for j in range(4)] for i in range(4)],
    rotation_control_at_origin=[[str(rotomega[i,j]) for j in range(4)] for i in range(4)],
    domain='a^2*(x^2+z^2)<1; a=gamma/c; coordinates x0=ct,x,y,z',sympy_version=s.__version__,
    source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),A.HERE/'FROZEN_KINEMATICS.md']},
    scope='Exact local kinematic witness, not a solution of the full gravity/gas action; applies to either footing; kappa=1/2 FITTED; not theory closed')
A.atomic(A.HERE/'covariant_witness.json',obj);print(json.dumps(dict(passed=obj['passed'],total=obj['total']),indent=2));raise SystemExit(int(obj['passed']!=obj['total']))
